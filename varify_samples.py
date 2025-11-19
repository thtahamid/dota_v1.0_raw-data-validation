import os
import cv2
import numpy as np
from tqdm import tqdm

# --- CONFIGURATION ---
# Update these to match where you have your sample images and labels
IMG_DIR = "sample_images"
LABEL_DIR = "sample_labels"
OUTPUT_DIR = "debug_verification"
# ---------------------

# Define distinct colors for visualization (BGR format)
COLORS = {
    'plane': (0, 255, 255),          # Yellow
    'ship': (255, 0, 0),             # Blue
    'storage-tank': (0, 0, 255),     # Red
    'baseball-diamond': (255, 0, 255), # Magenta
    'tennis-court': (0, 255, 0),     # Green
    'basketball-court': (128, 0, 0), # Navy
    'ground-track-field': (0, 128, 128), # Olive
    'harbor': (128, 128, 0),         # Teal
    'bridge': (0, 0, 128),           # Maroon
    'large-vehicle': (255, 165, 0),  # Orange
    'small-vehicle': (255, 192, 203),# Pink
    'helicopter': (75, 0, 130),      # Indigo
    'roundabout': (255, 20, 147),    # Deep Pink
    'soccer-ball-field': (0, 255, 127), # Spring Green
    'swimming-pool': (240, 230, 140) # Khaki
}

def get_color(class_name):
    return COLORS.get(class_name, (255, 255, 255)) # Default to white if unknown

def verify_data():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    img_files = [f for f in os.listdir(IMG_DIR) if f.lower().endswith(('.png', '.jpg', '.tif'))]
    print(f"Verifying {len(img_files)} images for ALL classes...")

    for img_file in tqdm(img_files):
        img_path = os.path.join(IMG_DIR, img_file)
        label_file = os.path.splitext(img_file)[0] + ".txt"
        label_path = os.path.join(LABEL_DIR, label_file)

        img = cv2.imread(img_path)
        if img is None: continue

        if os.path.exists(label_path):
            with open(label_path, 'r') as f:
                lines = f.readlines()

            for line in lines:
                line = line.strip()
                if not line: continue

                # --- METADATA HANDLING ---
                # Skip lines that are metadata (gsd, imagesource)
                # logic: if it contains letters but doesn't look like coordinate data
                if 'imagesource' in line or 'gsd' in line:
                    continue
                
                parts = line.split()
                
                # Robust check: A valid data line needs at least 8 coords + 1 category + 1 difficulty
                if len(parts) < 10: 
                    continue

                try:
                    # Extract coordinates (first 8 items)
                    coords = list(map(float, parts[:8]))
                    
                    # Extract Class and Difficulty
                    category = parts[8]
                    difficulty = parts[9] # 0 or 1
                    
                    # --- DRAWING LOGIC ---
                    
                    # 1. Reshape to polygon
                    poly = np.array(coords, dtype=np.int32).reshape((-1, 1, 2))
                    
                    # Get color for this class
                    color = get_color(category)
                    
                    # If difficulty is 1, use thin lines, otherwise thick
                    thickness = 1 if difficulty == '1' else 2
                    
                    # Draw the main box
                    cv2.polylines(img, [poly], isClosed=True, color=color, thickness=thickness)
                    
                    # 2. VISUALIZE STARTING POINT (x1, y1)
                    # DOTA specs say x1,y1 is significant. We draw a solid circle there.
                    start_point = (int(coords[0]), int(coords[1]))
                    # Draw a filled circle (radius 5) in Yellow (0, 255, 255) to match documentation
                    cv2.circle(img, start_point, 5, (0, 255, 255), -1) 
                    
                    # 3. Put Text Label
                    label_text = f"{category}"
                    cv2.putText(img, label_text, start_point, cv2.FONT_HERSHEY_SIMPLEX, 
                                0.6, color, 2)

                except ValueError:
                    # This catches lines that aren't metadata but also aren't valid numbers
                    continue

        # Save the annotated image
        cv2.imwrite(os.path.join(OUTPUT_DIR, "checked_" + img_file), img)

    print(f"Done. Check {OUTPUT_DIR} for visual validation.")

if __name__ == "__main__":
    verify_data()