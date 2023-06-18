import os
import cx_Freeze, sys

base = None

if sys.platform == 'win32':
    base = "Win32GUI"


# Get the current working directory
current_dir = os.getcwd()

# Specify the relative path to folder1 from the current working directory
folder1_path = os.path.join(current_dir, "deep_sort_pytorch")

executables = [cx_Freeze.Executable("vehicle_monitoring.py", base=base)]

cx_Freeze.setup(
    name="Vehicle Monitoring",
    options={"build_exe": {"packages": ["tkinter", "urllib3","PIL", "numpy", "torch", "hydra", "cv2", "pandas", "numpy", "ultralytics", "pytesseract"],
    "include_files": ["bg.jpg", "output.xlsx", "ocr.py", "yolov8n.pt", folder1_path
    ]}},
    version="1.0",
    description="Vehicle Classification, Tracking, Counting",
    executables=executables
)