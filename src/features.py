"""Facial geometry helpers."""
import numpy as np
LEFT_EYE=[362,385,387,263,373,380]
RIGHT_EYE=[33,160,158,133,153,144]
def dist(a,b):
    return float(np.linalg.norm(np.asarray(a,dtype=np.float32)-np.asarray(b,dtype=np.float32)))
def eye_aspect_ratio(p):
    if len(p)!=6: raise ValueError("EAR requires six points")
    horizontal=dist(p[0],p[3])
    return 0.0 if horizontal<=1e-8 else (dist(p[1],p[5])+dist(p[2],p[4]))/(2*horizontal)
def mouth_aspect_ratio(top,bottom,left,right):
    width=dist(left,right)
    return 0.0 if width<=1e-8 else dist(top,bottom)/width
def landmarks_to_features(landmarks,w,h):
    def pt(i):
        lm=landmarks[i]
        return (int(lm.x*w),int(lm.y*h))
    left=[pt(i) for i in LEFT_EYE]; right=[pt(i) for i in RIGHT_EYE]
    ear=(eye_aspect_ratio(left)+eye_aspect_ratio(right))/2
    mar=mouth_aspect_ratio(pt(13),pt(14),pt(78),pt(308))
    return ear,mar,{"left_eye":left,"right_eye":right,"mouth":[pt(i) for i in (13,14,78,308)]}
