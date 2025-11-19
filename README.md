tqdm

# DOTA v1.0 Data Validation Guide

This guide explains how to set up and run a visual verification step for DOTA v1.0 raw OBB (Oriented Bounding Box) labels. The goal is to visually confirm that label boxes align with the satellite imagery before filtering or training.

## Directory Structure

Organize your project root like this:

```
Your_Project_Root/
├── venv/                  # Virtual environment (auto-generated)
├── requirements.txt       # Dependencies list
├── verify_all_classes.py  # The validation script
└── sample_test/           # Your 100-sample subset
    ├── images/            # .png or .tif files
    └── labels/            # .txt files
```

## Prerequisites

- Python 3.7+ installed
- `pip` available

## Environment Initialization

Open a terminal in the project root and create/activate a virtual environment.

PowerShell (Windows):

```powershell
python -m venv venv
.\\venv\\Scripts\\Activate.ps1   # or: .\\venv\\Scripts\\activate
```

macOS / Linux:

```bash
python3 -m venv venv
source venv/bin/activate
```

Install dependencies:

```powershell
pip install -r requirements.txt
```

Add this to `requirements.txt` if not present:

```
opencv-python
numpy
tqdm
```

## Verification Script

Create `verify_all_classes.py` in the project root. It:

- Skips DOTA metadata lines (`imagesource`, `gsd`).
- Visualizes classes with distinct colors.
- Marks the starting point `(x1, y1)` with a yellow dot (to check OBB orientation).


## Execution

Run the script from the project root (with the virtual environment active):

```powershell
python verify_all_classes.py
```

## Audit Checklist

- **Yellow Dot Position:** Confirm the yellow dot (start point) appears consistently on the corners of boxes. For planes, check if it marks the nose or tail.
- **Box Tightness:** The colored lines should closely follow object boundaries.
- **Class Accuracy:** Verify the visual class color matches the object (e.g., plane, ship).
- **Drift / Coordinate Errors:** If boxes are offset (e.g., consistently shifted by ~10px), inspect the labeling coordinate system or preprocessing steps.

## Troubleshooting

- If images are not found, confirm `IMG_DIR` and `LABEL_DIR` values at the top of `verify_all_classes.py`.
- If OpenCV fails to read images, ensure required image codecs are available and images are not corrupted.

## Notes

- The verification script is intended for manual visual inspection prior to downstream data filtering or training.

---

Happy validating — check `sample_test/debug_all_classes` for outputs.
