import csv,os,time
class DrowsinessMonitor:
    def __init__(self,ear_threshold=.21,eye_closed_seconds=1.5,mar_yawn_threshold=.65,yawn_seconds=1.2,smoothing_alpha=.35):
        self.ear_threshold=ear_threshold; self.eye_closed_seconds=eye_closed_seconds
        self.mar_yawn_threshold=mar_yawn_threshold; self.yawn_seconds=yawn_seconds; self.alpha=smoothing_alpha
        self.reset()
    def reset(self):
        self.smoothed_ear=None; self.eye_since=None; self.yawn_since=None
    def update(self,ear,mar,now=None):
        now=time.monotonic() if now is None else now
        self.smoothed_ear=ear if self.smoothed_ear is None else self.alpha*ear+(1-self.alpha)*self.smoothed_ear
        if self.smoothed_ear<self.ear_threshold:
            if self.eye_since is None: self.eye_since=now
        else: self.eye_since=None
        if mar>=self.mar_yawn_threshold:
            if self.yawn_since is None: self.yawn_since=now
        else: self.yawn_since=None
        eye=0 if self.eye_since is None else now-self.eye_since
        yawn=0 if self.yawn_since is None else now-self.yawn_since
        if eye>=self.eye_closed_seconds: status,reason="DROWSINESS ALERT","Prolonged eye closure"
        elif yawn>=self.yawn_seconds: status,reason="POSSIBLE FATIGUE","Sustained mouth opening (possible yawn)"
        else: status,reason="ALERT","No sustained fatigue cue"
        return {"status":status,"reason":reason,"ear":self.smoothed_ear,"mar":mar,"eye_closed_seconds":eye,"yawn_seconds":yawn}
class CSVLogger:
    def __init__(self,path):
        os.makedirs(os.path.dirname(path) or ".",exist_ok=True); self.file=open(path,"w",newline="",encoding="utf-8")
        self.writer=csv.writer(self.file); self.writer.writerow(["elapsed_seconds","status","reason","ear","mar","eye_closed_seconds","yawn_seconds"])
    def write(self,elapsed,r):
        self.writer.writerow([f"{elapsed:.3f}",r["status"],r["reason"],f'{r["ear"]:.4f}',f'{r["mar"]:.4f}',f'{r["eye_closed_seconds"]:.3f}',f'{r["yawn_seconds"]:.3f}'])
    def close(self): self.file.close()
