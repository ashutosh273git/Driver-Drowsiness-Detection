"""Driver Drowsiness Detection - webcam or video-file runner."""
import argparse,json,os,time,cv2
import numpy as np
from src.detector import FaceLandmarkDetector
from src.features import landmarks_to_features
from src.monitor import DrowsinessMonitor,CSVLogger
from src.alert import AlertSound

def main():
    ap=argparse.ArgumentParser(description="Camera-based driver drowsiness detection")
    ap.add_argument("--source",default=None,help="Camera index or video file path")
    ap.add_argument("--config",default="config.json")
    ap.add_argument("--no-sound",action="store_true")
    ap.add_argument("--no-log",action="store_true")
    args=ap.parse_args()
    with open(args.config,encoding="utf-8") as f: cfg=json.load(f)
    source=args.source if args.source is not None else str(cfg.get("camera_index",0))
    source=int(source) if str(source).isdigit() else source
    cap=cv2.VideoCapture(source)
    if not cap.isOpened(): raise SystemExit(f"Cannot open source: {source}. Check camera permissions/index or video path.")
    w,h=int(cfg["frame_width"]),int(cfg["frame_height"])
    cap.set(cv2.CAP_PROP_FRAME_WIDTH,w); cap.set(cv2.CAP_PROP_FRAME_HEIGHT,h)
    detector=FaceLandmarkDetector()
    monitor=DrowsinessMonitor(cfg["ear_threshold"],cfg["eye_closed_seconds"],cfg["mar_yawn_threshold"],cfg["yawn_seconds"],cfg["smoothing_alpha"])
    sound=AlertSound(cfg.get("enable_sound",True) and not args.no_sound,cfg.get("alert_cooldown_seconds",2))
    logger=None if args.no_log else CSVLogger("logs/session.csv")
    start=time.monotonic(); last_frame=start; fps=0; previous="ALERT"
    print("Running. Press Q or Esc in the video window to quit.")
    try:
        while True:
            ok,frame=cap.read()
            if not ok: break
            frame=cv2.resize(frame,(w,h)); now=time.monotonic()
            instant=1/max(now-last_frame,1e-6); last_frame=now
            fps=instant if fps==0 else .9*fps+.1*instant
            landmarks=detector.detect(frame)
            if landmarks is None:
                monitor.reset(); status="FACE NOT DETECTED"
                cv2.putText(frame,status,(22,42),cv2.FONT_HERSHEY_SIMPLEX,.8,(0,165,255),2)
                cv2.putText(frame,"Move into view / improve lighting",(22,75),cv2.FONT_HERSHEY_SIMPLEX,.55,(255,255,255),1)
            else:
                ear,mar,pts=landmarks_to_features(landmarks,w,h)
                result=monitor.update(ear,mar,now); status=result["status"]
                if cfg.get("show_landmarks",True):
                    for name in ("left_eye","right_eye"):
                        poly=np.array(pts[name],dtype=np.int32)
                        cv2.polylines(frame,[poly],True,(0,220,0),1)
                        for p in poly: cv2.circle(frame,tuple(p),2,(0,255,255),-1)
                    for p in pts["mouth"]: cv2.circle(frame,tuple(p),2,(255,180,0),-1)
                if status=="DROWSINESS ALERT" and previous!="DROWSINESS ALERT": sound.play()
                if logger: logger.write(now-start,result)
                color=(0,0,255) if status=="DROWSINESS ALERT" else ((0,165,255) if status=="POSSIBLE FATIGUE" else (0,180,0))
                cv2.putText(frame,status,(22,42),cv2.FONT_HERSHEY_SIMPLEX,.8,color,2)
                cv2.putText(frame,f'EAR: {result["ear"]:.3f}  MAR: {result["mar"]:.3f}',(22,75),cv2.FONT_HERSHEY_SIMPLEX,.56,(255,255,255),2)
                cv2.putText(frame,result["reason"],(22,106),cv2.FONT_HERSHEY_SIMPLEX,.5,color,1)
            previous=status
            cv2.putText(frame,f"FPS: {fps:.1f}",(w-130,32),cv2.FONT_HERSHEY_SIMPLEX,.55,(255,255,255),2)
            cv2.imshow("Driver Drowsiness Detection | Q to quit",frame)
            key=cv2.waitKey(1)&0xFF
            if key in (ord("q"),27): break
    finally:
        cap.release(); detector.close(); cv2.destroyAllWindows()
        if logger: logger.close()
    print("Session ended.", "CSV log saved to logs/session.csv" if logger else "Logging disabled.")
if __name__=="__main__": main()
