"""
preprocess.py
=============
Dog Breed Identification -- Image Preprocessing Pipeline
B.Tech Data Science Project

What this script does:
  1. Loads image IDs and breed labels from labels.csv
  2. Builds full file paths for each image
  3. Encodes breed names as integer class indices
  4. Splits data into Train / Validation / Test sets (70 / 15 / 15)
     using stratified sampling so every breed is represented equally
     in all three splits
  5. Creates Keras ImageDataGenerators:
       - Training   : resize + RGB + normalise + augmentation
       - Validation : resize + RGB + normalise only  (NO augmentation)
       - Test       : resize + RGB + normalise only  (NO augmentation)
  6. Creates dataset iterators using flow_from_dataframe
     (works with the flat Kaggle folder + CSV format)
  7. Saves split info CSV files for future reference
  8. Prints a detailed summary

Normalisation note:
  We use MobileNetV2's preprocess_input which scales pixel values
  from [0, 255] to [-1, 1].  This is the correct normalisation
  for MobileNetV2 / MobileNetV3 transfer learning.
  If you later choose VGG16 use:  tf.keras.applications.vgg16.preprocess_input
  If you later choose ResNet50 use: tf.keras.applications.resnet50.preprocess_input

Usage:
  python preprocess.py

Output files (saved to dataset/splits/):
  train_split.csv       -- image paths + labels for training set
  val_split.csv         -- image paths + labels for validation set
  test_split.csv        -- image paths + labels for test set
  class_names.txt       -- ordered list of the 120 breed class names
"""

import os
import random

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

# ── Suppress TensorFlow info / warning messages for clean output ───────────────
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input

SEPARATOR = "=" * 62


# ══════════════════════════════════════════════════════════════════
#  CONFIGURATION  -- change values here if needed
# ══════════════════════════════════════════════════════════════════

# Image dimensions required by MobileNetV2 (and many other CNNs)
IMG_HEIGHT = 224
IMG_WIDTH  = 224

# Colour mode -- always RGB for CNNs
COLOUR_MODE = 'rgb'

# Batch size: how many images are loaded at once during training
BATCH_SIZE = 32

# Random seed -- keep this fixed for reproducible splits every run
RANDOM_SEED = 42

# Split ratios
TRAIN_RATIO = 0.70   # 70% of data  -> training
VAL_RATIO   = 0.15   # 15% of data  -> validation
TEST_RATIO  = 0.15   # 15% of data  -> test
# Note: VAL_RATIO + TEST_RATIO must equal 1 - TRAIN_RATIO

# ── Paths ─────────────────────────────────────────────────────────
BASE_DIR    = os.path.dirname(os.path.abspath(__file__))
TRAIN_DIR   = os.path.join(BASE_DIR, 'train')        # flat image folder
LABELS_CSV  = os.path.join(BASE_DIR, 'labels.csv')  # id,breed mapping
SPLITS_DIR  = os.path.join(BASE_DIR, 'dataset', 'splits')

os.makedirs(SPLITS_DIR, exist_ok=True)


# ══════════════════════════════════════════════════════════════════
#  STEP 1 -- Fix random seeds for full reproducibility
# ══════════════════════════════════════════════════════════════════
print(SEPARATOR)
print("  DOG BREED IDENTIFICATION -- Preprocessing Pipeline")
print(SEPARATOR)
print(f"\n[Step 1] Setting random seeds (seed = {RANDOM_SEED}) ...")

random.seed(RANDOM_SEED)
np.random.seed(RANDOM_SEED)
tf.random.set_seed(RANDOM_SEED)

print("         Done. All random operations will produce the same")
print("         results every time you run this script.")


# ══════════════════════════════════════════════════════════════════
#  STEP 2 -- Load labels.csv
# ══════════════════════════════════════════════════════════════════
print(f"\n[Step 2] Loading labels from: {LABELS_CSV}")

df = pd.read_csv(LABELS_CSV)

# Build relative file path for each image (portable across environments)
# The Kaggle dataset stores images as <id>.jpg in the train/ folder
df['filepath'] = df['id'].apply(
    lambda img_id: f"train/{img_id}.jpg"
)

# Confirm files exist on disk (resolved against BASE_DIR)
missing = df[~df['filepath'].apply(lambda p: os.path.exists(os.path.join(BASE_DIR, p)))]
if len(missing) > 0:
    print(f"         [WARNING] {len(missing)} image files not found on disk!")
    print(f"         First missing: {missing['filepath'].iloc[0]}")
else:
    print(f"         All {len(df)} image files found on disk.")

print(f"         Total images : {len(df)}")
print(f"         Columns      : {list(df.columns)}")
print(f"         Sample rows  :")
print(df[['id', 'breed']].head(3).to_string(index=False))


# ══════════════════════════════════════════════════════════════════
#  STEP 3 -- Encode breed names as integers
# ══════════════════════════════════════════════════════════════════
print(f"\n[Step 3] Encoding breed names as class indices ...")

# LabelEncoder converts strings -> integers
# e.g. 'afghan_hound' -> 0, 'beagle' -> 5, etc.
encoder = LabelEncoder()
df['label'] = encoder.fit_transform(df['breed'])

class_names = list(encoder.classes_)   # sorted list of 120 breed names
num_classes = len(class_names)

print(f"         Number of unique breeds : {num_classes}")
print(f"         First 5 class names     : {class_names[:5]}")
print(f"         breed column -> label column example:")
print(df[['breed', 'label']].head(3).to_string(index=False))

# Save class names to a text file for later use during inference
class_names_path = os.path.join(SPLITS_DIR, 'class_names.txt')
with open(class_names_path, 'w') as f:
    for name in class_names:
        f.write(name + '\n')
print(f"         Class names saved -> {class_names_path}")


# ══════════════════════════════════════════════════════════════════
#  STEP 4 -- Stratified Train / Validation / Test split
# ══════════════════════════════════════════════════════════════════
print(f"\n[Step 4] Splitting data into Train / Val / Test ...")
print(f"         Ratios  : Train={TRAIN_RATIO:.0%}  "
      f"Val={VAL_RATIO:.0%}  Test={TEST_RATIO:.0%}")
print(f"         Seed    : {RANDOM_SEED}  (fixed for reproducibility)")

# ── Why stratified? ───────────────────────────────────────────────
# Without stratify, random chance could put all images of a rare
# breed into the test set and none in training.
# stratify=df['label'] ensures each breed gets the correct proportion
# in every split.

# First split: separate out TRAINING set (70%)
#   remaining_df will be 30% of data
df_train, df_remaining = train_test_split(
    df,
    test_size=(1.0 - TRAIN_RATIO),   # 0.30
    random_state=RANDOM_SEED,
    stratify=df['label']             # keep breed proportions equal
)

# Second split: split the remaining 30% equally into Val (15%) and Test (15%)
#   val_ratio_of_remaining = 0.15 / 0.30 = 0.50
val_ratio_of_remaining = VAL_RATIO / (VAL_RATIO + TEST_RATIO)

df_val, df_test = train_test_split(
    df_remaining,
    test_size=(1.0 - val_ratio_of_remaining),  # 0.50
    random_state=RANDOM_SEED,
    stratify=df_remaining['label']
)

# Reset index so iterators work cleanly
df_train = df_train.reset_index(drop=True)
df_val   = df_val.reset_index(drop=True)
df_test  = df_test.reset_index(drop=True)

print(f"\n         Split results:")
print(f"           Train set : {len(df_train):>5} images  "
      f"({len(df_train)/len(df)*100:.1f}%)")
print(f"           Val set   : {len(df_val):>5} images  "
      f"({len(df_val)/len(df)*100:.1f}%)")
print(f"           Test set  : {len(df_test):>5} images  "
      f"({len(df_test)/len(df)*100:.1f}%)")
print(f"           Total     : {len(df_train)+len(df_val)+len(df_test):>5} images")

# Verify stratification -- check breed distribution is roughly even
# Pick 3 sample breeds and show their counts in each split
sample_breeds = class_names[:3]
print(f"\n         Stratification check (first 3 breeds):")
print(f"           {'Breed':<30} {'Train':>7} {'Val':>7} {'Test':>7}")
print(f"           {'-'*54}")
for breed in sample_breeds:
    t = (df_train['breed'] == breed).sum()
    v = (df_val['breed']   == breed).sum()
    s = (df_test['breed']  == breed).sum()
    print(f"           {breed:<30} {t:>7} {v:>7} {s:>7}")


# ══════════════════════════════════════════════════════════════════
#  STEP 5 -- Save split CSVs for reference
# ══════════════════════════════════════════════════════════════════
print(f"\n[Step 5] Saving split CSV files to {SPLITS_DIR} ...")

df_train.to_csv(os.path.join(SPLITS_DIR, 'train_split.csv'), index=False)
df_val.to_csv(os.path.join(SPLITS_DIR, 'val_split.csv'),     index=False)
df_test.to_csv(os.path.join(SPLITS_DIR, 'test_split.csv'),   index=False)

print(f"         train_split.csv  -> {len(df_train)} rows")
print(f"         val_split.csv    -> {len(df_val)} rows")
print(f"         test_split.csv   -> {len(df_test)} rows")


# ══════════════════════════════════════════════════════════════════
#  STEP 6 -- Define Image Data Generators
# ══════════════════════════════════════════════════════════════════
print(f"\n[Step 6] Creating ImageDataGenerators ...")
print(f"         Image size       : {IMG_HEIGHT} x {IMG_WIDTH} pixels")
print(f"         Colour mode      : {COLOUR_MODE.upper()}")
print(f"         Normalisation    : MobileNetV2 preprocess_input -> [-1, 1]")

# ── Training generator -- includes augmentation ────────────────────
# Augmentation artificially increases dataset variety by applying
# random (but realistic) transformations to training images.
# This helps the model generalise better and reduces overfitting.
#
# Parameters explained:
#   preprocessing_function : applies MobileNetV2 normalisation [-1, 1]
#   horizontal_flip        : randomly mirror the image left-right (50% chance)
#   rotation_range         : randomly rotate by up to +/-15 degrees
#   zoom_range             : randomly zoom in/out by up to +/-10%
#   width_shift_range      : randomly shift image left/right by up to 10%
#   height_shift_range     : randomly shift image up/down by up to 10%
#   fill_mode              : 'nearest' fills empty corners with nearest pixel
train_datagen = ImageDataGenerator(
    preprocessing_function=preprocess_input,  # normalise to [-1, 1]
    horizontal_flip=True,                     # mirror image left-right
    rotation_range=15,                        # rotate up to +/-15 degrees
    zoom_range=0.10,                          # zoom in/out by +/-10%
    width_shift_range=0.10,                   # shift left/right by +/-10%
    height_shift_range=0.10,                  # shift up/down by +/-10%
    fill_mode='nearest'                       # fill empty corners
)

# ── Validation generator -- NO augmentation ────────────────────────
# We NEVER augment validation or test images.
# Augmentation is only for training -- it teaches the model to handle
# variations. Evaluation must use real, unmodified images so results
# accurately reflect model performance on unseen data.
val_datagen = ImageDataGenerator(
    preprocessing_function=preprocess_input   # only normalise, nothing else
)

# ── Test generator -- NO augmentation ─────────────────────────────
test_datagen = ImageDataGenerator(
    preprocessing_function=preprocess_input   # only normalise, nothing else
)

print(f"         Training augmentations:")
print(f"           horizontal_flip    : True")
print(f"           rotation_range     : +/-15 degrees")
print(f"           zoom_range         : +/-10%")
print(f"           width_shift_range  : +/-10%")
print(f"           height_shift_range : +/-10%")
print(f"         Val / Test           : No augmentation (normalise only)")


# ══════════════════════════════════════════════════════════════════
#  STEP 7 -- Create dataset iterators using flow_from_dataframe
# ══════════════════════════════════════════════════════════════════
print(f"\n[Step 7] Creating dataset iterators ...")

# flow_from_dataframe is perfect for the Kaggle flat-folder format.
# It reads image file paths from a DataFrame column and loads them
# batch by batch. This is memory-efficient -- images are loaded on
# demand, not all at once.
#
# Parameters:
#   dataframe      : the split DataFrame (has 'filepath' and 'breed' columns)
#   x_col          : column name containing full image file paths
#   y_col          : column name containing class labels (breed names)
#   target_size    : resize every image to (height, width)
#   color_mode     : 'rgb' -- always use 3 channels for CNNs
#   class_mode     : 'categorical' -- one-hot encoded labels for multi-class
#   batch_size     : number of images per batch
#   seed           : for reproducibility of shuffling
#   shuffle        : True for training (randomises order each epoch)
#                    False for val/test (keeps order consistent)

train_iterator = train_datagen.flow_from_dataframe(
    dataframe=df_train,
    directory=BASE_DIR,
    x_col='filepath',       # column with image path (relative to BASE_DIR)
    y_col='breed',          # column with class label (breed name)
    target_size=(IMG_HEIGHT, IMG_WIDTH),
    color_mode=COLOUR_MODE,
    class_mode='categorical',
    batch_size=BATCH_SIZE,
    shuffle=True,           # shuffle training data every epoch
    seed=RANDOM_SEED
)

val_iterator = val_datagen.flow_from_dataframe(
    dataframe=df_val,
    directory=BASE_DIR,
    x_col='filepath',
    y_col='breed',
    target_size=(IMG_HEIGHT, IMG_WIDTH),
    color_mode=COLOUR_MODE,
    class_mode='categorical',
    batch_size=BATCH_SIZE,
    shuffle=False,          # do NOT shuffle -- consistent evaluation order
    seed=RANDOM_SEED
)

test_iterator = test_datagen.flow_from_dataframe(
    dataframe=df_test,
    directory=BASE_DIR,
    x_col='filepath',
    y_col='breed',
    target_size=(IMG_HEIGHT, IMG_WIDTH),
    color_mode=COLOUR_MODE,
    class_mode='categorical',
    batch_size=BATCH_SIZE,
    shuffle=False,          # do NOT shuffle -- consistent evaluation order
    seed=RANDOM_SEED
)

# Calculate number of steps needed to cover the full dataset each epoch
train_steps = int(np.ceil(len(df_train) / BATCH_SIZE))
val_steps   = int(np.ceil(len(df_val)   / BATCH_SIZE))
test_steps  = int(np.ceil(len(df_test)  / BATCH_SIZE))

print(f"         train_iterator : {len(df_train)} images, "
      f"{train_steps} batches of {BATCH_SIZE}")
print(f"         val_iterator   : {len(df_val)} images, "
      f"{val_steps} batches of {BATCH_SIZE}")
print(f"         test_iterator  : {len(df_test)} images, "
      f"{test_steps} batches of {BATCH_SIZE}")


# ══════════════════════════════════════════════════════════════════
#  STEP 8 -- Verify: load one batch and check shapes & pixel range
# ══════════════════════════════════════════════════════════════════
print(f"\n[Step 8] Verifying one batch from training iterator ...")

# Load a single batch of images and labels
images_batch, labels_batch = next(train_iterator)

print(f"         Batch image tensor shape : {images_batch.shape}")
print(f"         Expected shape           : ({BATCH_SIZE}, {IMG_HEIGHT}, "
      f"{IMG_WIDTH}, 3)")
print(f"         Batch labels shape       : {labels_batch.shape}")
print(f"         Num classes in labels    : {labels_batch.shape[1]}")
print(f"         Pixel value range        : "
      f"[{images_batch.min():.3f}, {images_batch.max():.3f}]")
print(f"         (MobileNetV2 expects     :  [-1.0, 1.0]  -- OK)")
print(f"         Image dtype              : {images_batch.dtype}")

# Check one label is one-hot encoded correctly
sample_label = labels_batch[0]
print(f"         Sample label (one-hot)   : "
      f"{int(sample_label.sum())} active class out of {num_classes}")

# Reset iterators to epoch start so training begins from scratch
train_iterator.reset()
val_iterator.reset()
test_iterator.reset()
print(f"         Iterators reset to start.")


# ══════════════════════════════════════════════════════════════════
#  STEP 9 -- Save preprocessing config for use in training script
# ══════════════════════════════════════════════════════════════════
print(f"\n[Step 9] Saving preprocessing config ...")

config_path = os.path.join(SPLITS_DIR, 'preprocess_config.txt')
with open(config_path, 'w') as f:
    f.write(f"img_height={IMG_HEIGHT}\n")
    f.write(f"img_width={IMG_WIDTH}\n")
    f.write(f"batch_size={BATCH_SIZE}\n")
    f.write(f"num_classes={num_classes}\n")
    f.write(f"random_seed={RANDOM_SEED}\n")
    f.write(f"train_size={len(df_train)}\n")
    f.write(f"val_size={len(df_val)}\n")
    f.write(f"test_size={len(df_test)}\n")
    f.write(f"train_steps={train_steps}\n")
    f.write(f"val_steps={val_steps}\n")
    f.write(f"test_steps={test_steps}\n")
    f.write(f"normalisation=mobilenetv2_preprocess_input\n")
    f.write(f"pixel_range=[-1, 1]\n")

print(f"         Config saved -> {config_path}")


# ══════════════════════════════════════════════════════════════════
#  FINAL SUMMARY
# ══════════════════════════════════════════════════════════════════
print(f"\n{SEPARATOR}")
print("  PREPROCESSING SUMMARY")
print(SEPARATOR)
print(f"  Total images             : {len(df)}")
print(f"  Number of breed classes  : {num_classes}")
print(f"  Image size               : {IMG_HEIGHT} x {IMG_WIDTH} x 3 (RGB)")
print(f"  Pixel normalisation      : [-1, 1]  (MobileNetV2 standard)")
print(f"  Random seed              : {RANDOM_SEED}")
print(f"")
print(f"  Dataset split:")
print(f"    Train  : {len(df_train):>5} images  ({len(df_train)/len(df)*100:.1f}%)")
print(f"    Val    : {len(df_val):>5} images  ({len(df_val)/len(df)*100:.1f}%)")
print(f"    Test   : {len(df_test):>5} images  ({len(df_test)/len(df)*100:.1f}%)")
print(f"")
print(f"  Training augmentations   : flip, rotate, zoom, shift")
print(f"  Val / Test augmentation  : None")
print(f"  Batch size               : {BATCH_SIZE}")
print(f"  Steps per epoch (train)  : {train_steps}")
print(f"  Steps per epoch (val)    : {val_steps}")
print(f"")
print(f"  Output files (dataset/splits/):")
print(f"    train_split.csv        : {len(df_train)} rows")
print(f"    val_split.csv          : {len(df_val)} rows")
print(f"    test_split.csv         : {len(df_test)} rows")
print(f"    class_names.txt        : {num_classes} breed names")
print(f"    preprocess_config.txt  : config for training script")
print(SEPARATOR)
print("  Preprocessing complete! Ready to train.")
print(SEPARATOR)
print()
print("  Next step:  python train.py")
print()

# ══════════════════════════════════════════════════════════════════
#  EXPOSE iterators for use in other scripts (e.g. train.py)
# ══════════════════════════════════════════════════════════════════
# When train.py does:  from preprocess import get_iterators
# it can call get_iterators() to get all three dataset iterators
# without re-running the full script.

def get_iterators():
    """
    Return (train_iterator, val_iterator, test_iterator,
            num_classes, class_names, train_steps, val_steps, test_steps)
    for use in train.py.
    """
    return (
        train_iterator,
        val_iterator,
        test_iterator,
        num_classes,
        class_names,
        train_steps,
        val_steps,
        test_steps,
    )
