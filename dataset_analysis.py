"""
dataset_analysis.py
===================
Dog Breed Identification - Dataset Analysis Script
B.Tech Data Science Project

This script analyses the Kaggle Dog Breed Identification dataset.
It reads labels.csv, counts images per breed, checks for missing or
corrupted images, generates a summary CSV, and saves a bar chart.

Dataset structure (Kaggle flat format):
  train/          <-- all training images (JPG, named by ID)
  test/           <-- all test images (JPG, named by ID)
  labels.csv      <-- id,breed mapping for training images
  sample_submission.csv  <-- lists all 120 breed class names

Usage:
  python dataset_analysis.py

Output files:
  dataset/breed_counts.csv      -- breed name + image count
  dataset/breed_distribution.png -- bar chart of images per breed
"""

import os
import csv
import struct
import sys

# ── Try to import optional libraries ──────────────────────────────────────────
try:
    import matplotlib
    matplotlib.use('Agg')          # non-interactive backend (no GUI needed)
    import matplotlib.pyplot as plt
    import matplotlib.ticker as ticker
    HAS_MATPLOTLIB = True
except ImportError:
    HAS_MATPLOTLIB = False
    print("[WARNING] matplotlib not installed. Bar chart will be skipped.")
    print("          Run:  pip install matplotlib\n")

# ── Paths ─────────────────────────────────────────────────────────────────────
BASE_DIR    = os.path.dirname(os.path.abspath(__file__))
TRAIN_DIR   = os.path.join(BASE_DIR, 'train')
TEST_DIR    = os.path.join(BASE_DIR, 'test')
LABELS_CSV  = os.path.join(BASE_DIR, 'labels.csv')
SAMPLE_CSV  = os.path.join(BASE_DIR, 'sample_submission.csv')
DATASET_DIR = os.path.join(BASE_DIR, 'dataset')
OUT_CSV     = os.path.join(DATASET_DIR, 'breed_counts.csv')
OUT_CHART   = os.path.join(DATASET_DIR, 'breed_distribution.png')

os.makedirs(DATASET_DIR, exist_ok=True)

SEPARATOR = "=" * 60


# ── Helper: check if a JPG file is valid (not corrupted) ──────────────────────
def is_valid_jpg(filepath):
    """
    Check the first 2 bytes of a file for the JPEG magic number (FF D8).
    Returns True if the file looks like a valid JPEG.
    """
    try:
        with open(filepath, 'rb') as f:
            header = f.read(2)
        return header == b'\xff\xd8'
    except Exception:
        return False


# ── Step 1: Verify paths exist ────────────────────────────────────────────────
print(SEPARATOR)
print("  DOG BREED IDENTIFICATION - Dataset Analysis")
print(SEPARATOR)

for path, label in [(TRAIN_DIR, 'train/'), (LABELS_CSV, 'labels.csv')]:
    if not os.path.exists(path):
        print(f"[ERROR] Required path not found: {path}")
        print("        Please make sure the dataset is placed in the project root.")
        sys.exit(1)

print("[OK] Required files found.\n")


# ── Step 2: Read labels.csv ───────────────────────────────────────────────────
print(f"[1] Reading {LABELS_CSV} ...")

id_to_breed = {}   # { image_id : breed_name }
with open(LABELS_CSV, newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        id_to_breed[row['id'].strip()] = row['breed'].strip()

total_labels = len(id_to_breed)
print(f"    Total labelled images in labels.csv : {total_labels}")


# ── Step 3: Get unique breeds from labels.csv ─────────────────────────────────
breeds_in_labels = sorted(set(id_to_breed.values()))
num_breeds_labels = len(breeds_in_labels)
print(f"    Unique breed classes in labels.csv  : {num_breeds_labels}")


# ── Step 4: Get breed list from sample_submission.csv (ground truth) ──────────
breeds_official = []
if os.path.exists(SAMPLE_CSV):
    with open(SAMPLE_CSV, newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        header = next(reader)        # first row is the header
    breeds_official = header[1:]     # skip the 'id' column
    print(f"    Official breed classes (sample_submission): {len(breeds_official)}")
else:
    print(f"    [WARNING] sample_submission.csv not found, skipping official count.")


# ── Step 5: Count images in train/ folder ─────────────────────────────────────
print(f"\n[2] Scanning train/ folder: {TRAIN_DIR}")

train_files = [f for f in os.listdir(TRAIN_DIR) if f.lower().endswith('.jpg')]
print(f"    Total JPG files in train/ : {len(train_files)}")

# ── Step 6: Check for missing images (in labels.csv but not on disk) ──────────
print(f"\n[3] Checking for missing images ...")
missing_images = []
for img_id in id_to_breed:
    expected_path = os.path.join(TRAIN_DIR, img_id + '.jpg')
    if not os.path.exists(expected_path):
        missing_images.append(img_id)

if missing_images:
    print(f"    [!] Missing images (in CSV but not on disk): {len(missing_images)}")
    for m in missing_images[:10]:    # show first 10 only
        print(f"        - {m}.jpg")
    if len(missing_images) > 10:
        print(f"        ... and {len(missing_images) - 10} more.")
else:
    print(f"    [OK] No missing images. All labelled IDs found on disk.")


# ── Step 7: Check for corrupted images ────────────────────────────────────────
print(f"\n[4] Checking for corrupted images (JPEG header validation) ...")
corrupted = []
for img_id in id_to_breed:
    fpath = os.path.join(TRAIN_DIR, img_id + '.jpg')
    if os.path.exists(fpath) and not is_valid_jpg(fpath):
        corrupted.append(img_id)

if corrupted:
    print(f"    [!] Corrupted images found : {len(corrupted)}")
    for c in corrupted[:5]:
        print(f"        - {c}.jpg")
else:
    print(f"    [OK] No corrupted images detected.")


# ── Step 8: Count images per breed ────────────────────────────────────────────
print(f"\n[5] Counting images per breed ...")

breed_counts = {}
for img_id, breed in id_to_breed.items():
    breed_counts[breed] = breed_counts.get(breed, 0) + 1

# Sort by count descending
sorted_breeds = sorted(breed_counts.items(), key=lambda x: x[1], reverse=True)

print(f"    Top 5 breeds by image count:")
for breed, count in sorted_breeds[:5]:
    print(f"        {breed:<35} {count} images")

print(f"\n    Bottom 5 breeds by image count:")
for breed, count in sorted_breeds[-5:]:
    print(f"        {breed:<35} {count} images")

counts = [c for _, c in sorted_breeds]
print(f"\n    Min images in a breed : {min(counts)}")
print(f"    Max images in a breed : {max(counts)}")
print(f"    Avg images per breed  : {sum(counts) / len(counts):.1f}")


# ── Step 9: Verify 120-breed claim ────────────────────────────────────────────
print(f"\n[6] Verifying breed count ...")
if num_breeds_labels == 120:
    print(f"    [OK] Confirmed: dataset has exactly 120 breed classes.")
elif breeds_official and len(breeds_official) == 120:
    print(f"    [OK] Official submission has 120 classes.")
    print(f"    [NOTE] labels.csv shows {num_breeds_labels} breeds (all 120 may not appear equally).")
else:
    print(f"    [NOTE] Found {num_breeds_labels} breeds in labels.csv.")
    print(f"            Expected 120. Some breeds may have no training samples.")


# ── Step 10: Save breed_counts.csv ────────────────────────────────────────────
print(f"\n[7] Saving breed counts to {OUT_CSV} ...")

with open(OUT_CSV, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['breed', 'image_count'])
    for breed, count in sorted_breeds:
        writer.writerow([breed, count])

print(f"    [OK] Saved: {OUT_CSV}")


# ── Step 11: Save bar chart ────────────────────────────────────────────────────
if HAS_MATPLOTLIB:
    print(f"\n[8] Generating bar chart ...")

    breed_names  = [b for b, _ in sorted_breeds]
    breed_values = [c for _, c in sorted_breeds]

    # Colours matching the cream/brown UI theme
    BAR_COLOR    = '#8B5E3C'
    BG_COLOR     = '#FFF8ED'
    GRID_COLOR   = '#E0CDB8'
    TEXT_COLOR   = '#3E2515'

    fig, ax = plt.subplots(figsize=(22, 10))
    fig.patch.set_facecolor(BG_COLOR)
    ax.set_facecolor(BG_COLOR)

    bars = ax.bar(breed_names, breed_values, color=BAR_COLOR,
                  edgecolor='#5C3A1E', linewidth=0.4)

    ax.set_title('Dog Breed Identification — Images per Breed',
                 fontsize=16, fontweight='bold', color=TEXT_COLOR, pad=20)
    ax.set_xlabel('Breed', fontsize=11, color=TEXT_COLOR, labelpad=10)
    ax.set_ylabel('Number of Images', fontsize=11, color=TEXT_COLOR, labelpad=10)

    ax.set_xticks(range(len(breed_names)))
    ax.set_xticklabels(breed_names, rotation=90, fontsize=6.5, color=TEXT_COLOR)
    ax.yaxis.set_major_locator(ticker.MaxNLocator(integer=True))
    ax.tick_params(axis='y', colors=TEXT_COLOR)

    ax.yaxis.grid(True, color=GRID_COLOR, linewidth=0.8, linestyle='--')
    ax.set_axisbelow(True)

    for spine in ax.spines.values():
        spine.set_edgecolor(GRID_COLOR)

    plt.tight_layout()
    plt.savefig(OUT_CHART, dpi=120, bbox_inches='tight')
    plt.close()
    print(f"    [OK] Chart saved: {OUT_CHART}")
else:
    print(f"\n[8] Skipping chart (matplotlib not installed).")


# ── Summary ───────────────────────────────────────────────────────────────────
print(f"\n{SEPARATOR}")
print("  ANALYSIS SUMMARY")
print(SEPARATOR)
print(f"  Training images      : {len(train_files)}")
print(f"  Labelled entries     : {total_labels}")
print(f"  Unique breeds found  : {num_breeds_labels}")
print(f"  Missing images       : {len(missing_images)}")
print(f"  Corrupted images     : {len(corrupted)}")
print(f"  Output CSV           : dataset/breed_counts.csv")
if HAS_MATPLOTLIB:
    print(f"  Output chart         : dataset/breed_distribution.png")
print(SEPARATOR)
print("  Analysis complete!")
print(SEPARATOR)
