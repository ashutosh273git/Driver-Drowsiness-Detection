import cv2
import mediapipe as mp
class FaceLandmarkDetector:
    def __init__(self):
        self.mesh=mp.solutions.face_mesh.FaceMesh(static_image_mode=False,max_num_faces=1,
            refine_landmarks=True,min_detection_confidence=0.5,min_tracking_confidence=0.5)
    def detect(self,frame):
        rgb=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB); rgb.flags.writeable=False
        result=self.mesh.process(rgb)
        return result.multi_face_landmarks[0].landmark if result.multi_face_landmarks else None
    def close(self): self.mesh.close()
