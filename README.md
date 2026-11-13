# Driver Drowsiness Detection System

**Course:** CSET344 – Image and Video Processing Lab  
**Student:** Ashutosh Kumar Gupta  
**Enrollment:** S24CSEU2477  
**Project type:** Individual

## Features
- Webcam or recorded-video input using OpenCV.
- Facial landmark detection using MediaPipe Face Mesh.
- Eye Aspect Ratio (EAR) and Mouth Aspect Ratio (MAR).
- Time-persistent eye-closure and mouth-opening checks to avoid reacting to a single frame.
- On-screen state, landmarks, EAR/MAR and approximate FPS.
- Best-effort warning beep and CSV session log.

> This is an academic prototype, not a certified vehicle safety product or medical diagnostic tool. Never rely on it as the sole safety mechanism. Do not intentionally drive while sleepy to test it.

## Requirements
Python 3.10 or 3.11 recommended; webcam or video file. Internet is needed for first-time package installation.

## Windows setup (PowerShell)
Run from this folder:
```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```
If activation is blocked:
```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

## Run
Webcam (camera 0):
```powershell
python main.py
```
Another camera:
```powershell
python main.py --source 1
```
Video file:
```powershell
python main.py --source "data\sample.mp4"
```
Press **Q** or **Esc** in the preview window to exit.

Optional:
```powershell
python main.py --no-sound
python main.py --no-log
python main.py --config config.json
```

## Configuration
Edit `config.json`:
- `ear_threshold`: EAR below this value is treated as eye closure (initial value 0.21).
- `eye_closed_seconds`: continuous closure duration before drowsiness warning (1.5 s).
- `mar_yawn_threshold`: mouth ratio above which sustained opening is tracked (0.65).
- `yawn_seconds`: sustained opening duration for possible-fatigue status (1.2 s).
- `smoothing_alpha`: exponential smoothing factor.
- Frame size and sound/logging options are also configurable.

These are starting parameters, not universal values. Calibrate and evaluate on labelled recordings before reporting performance.

## Output
- Annotated preview window.
- `logs/session.csv` containing elapsed time, status, reason, EAR, MAR and cue durations.

No accuracy or FPS results are fabricated. Measure these on a labelled test set and record the protocol, confusion matrix and hardware.

## Tests
```powershell
python -m unittest discover -s tests -v
```
These unit tests check the geometry functions only; still perform end-to-end webcam/video testing.

## Structure
```text
driver_drowsiness_detection/
├── main.py
├── config.json
├── requirements.txt
├── README.md
├── src/
│   ├── alert.py
│   ├── detector.py
│   ├── features.py
│   └── monitor.py
├── tests/test_features.py
└── logs/  (session.csv created at runtime)
```

## Troubleshooting
- **Cannot open source:** close apps using the camera, check OS camera permissions, or try `--source 1`.
- **Face not detected:** improve front lighting and face the camera.
- **Low FPS:** reduce frame dimensions in `config.json`.
- **Install failure:** use a fresh Python 3.10/3.11 virtual environment and reinstall from requirements.
- **Warnings too frequent/rare:** calibrate EAR threshold and persistence duration against labelled recordings.

## References
[1] P. Viola and M. Jones, “Rapid object detection using a boosted cascade of simple features,” *Proc. IEEE CVPR*, 2001.  
[2] T. Soukupová and J. Čech, “Real-Time Eye Blink Detection using Facial Landmarks,” *Computer Vision Winter Workshop*, 2016.  
[3] Google AI for Developers, “Face landmark detection guide,” MediaPipe documentation, https://ai.google.dev/edge/mediapipe/solutions/vision/face_landmarker.
