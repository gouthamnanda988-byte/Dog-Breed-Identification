"""
quick_train_test.py
===================
A FAST test run of train_model.py logic.

Uses only 500 training images and 2 epochs.
Purpose: verify the full training pipeline works on your machine.
This is NOT the real training -- use Kaggle/Colab for full training.

Run with:  python quick_train_test.py
Expected time: 3 to 8 minutes on CPU.
"""

import os
import numpy as np
import pandas as pd

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

import tensorflow as tf
from tensorflow.keras import Model
from tensorflow.keras.layers import GlobalAveragePooling2D, Dense, Dropout
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.callbacks import EarlyStopping

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

BASE_DIR   = os.path.dirname(os.path.abspath(__file__))
SPLITS_DIR = os.path.join(BASE_DIR, 'dataset', 'splits')
MODEL_DIR  = os.path.join(BASE_DIR, 'model')
os.makedirs(MODEL_DIR, exist_ok=True)

# -- Small test settings --
SAMPLE_SIZE = 500    # use only 500 images for speed
BATCH_SIZE  = 16
EPOCHS      = 2      # just 2 epochs to verify the pipeline

print("=" * 55)
print("  QUICK PIPELINE TEST  (not real training)")
print("=" * 55)
print(f"  Images used  : {SAMPLE_SIZE}  (of 7155 available)")
print(f"  Epochs       : {EPOCHS}")
print(f"  Batch size   : {BATCH_SIZE}")
print()

# Load class names
with open(os.path.join(SPLITS_DIR, 'class_names.txt')) as f:
    class_names = [l.strip() for l in f.readlines()]
num_classes = len(class_names)

# Load a small sample of training data
df_train = pd.read_csv(os.path.join(SPLITS_DIR, 'train_split.csv'))
df_val   = pd.read_csv(os.path.join(SPLITS_DIR, 'val_split.csv'))

# Use only a subset to run fast
df_small_train = df_train.sample(n=SAMPLE_SIZE, random_state=42).reset_index(drop=True)
df_small_val   = df_val.sample(n=100, random_state=42).reset_index(drop=True)

print(f"[1] Loaded {SAMPLE_SIZE} train samples and 100 val samples.")

# Data generators
train_gen = ImageDataGenerator(
    preprocessing_function=preprocess_input,
    horizontal_flip=True,
    rotation_range=15
)
val_gen = ImageDataGenerator(preprocessing_function=preprocess_input)

train_iter = train_gen.flow_from_dataframe(
    df_small_train, directory=BASE_DIR, x_col='filepath', y_col='breed',
    target_size=(224, 224), color_mode='rgb',
    class_mode='categorical', batch_size=BATCH_SIZE, shuffle=True, seed=42
)
val_iter = val_gen.flow_from_dataframe(
    df_small_val, directory=BASE_DIR, x_col='filepath', y_col='breed',
    target_size=(224, 224), color_mode='rgb',
    class_mode='categorical', batch_size=BATCH_SIZE, shuffle=False
)

print(f"[2] Data generators ready.")

# Build model
base = MobileNetV2(input_shape=(224,224,3), include_top=False, weights='imagenet')
base.trainable = False
x = GlobalAveragePooling2D()(base.output)
x = Dropout(0.3)(x)
out = Dense(num_classes, activation='softmax')(x)
model = Model(inputs=base.input, outputs=out)

model.compile(
    optimizer=tf.keras.optimizers.Adam(1e-3),
    loss='categorical_crossentropy',
    metrics=['accuracy']
)
print(f"[3] Model built. Trainable params: {sum(tf.size(w).numpy() for w in model.trainable_weights):,}")

# Train for 2 epochs
print(f"\n[4] Training for {EPOCHS} epochs on {SAMPLE_SIZE} images ...")
print(f"    (This should take 3-8 minutes on CPU)\n")

train_steps = int(np.ceil(SAMPLE_SIZE / BATCH_SIZE))
val_steps   = int(np.ceil(100 / BATCH_SIZE))

history = model.fit(
    train_iter,
    steps_per_epoch=train_steps,
    epochs=EPOCHS,
    validation_data=val_iter,
    validation_steps=val_steps,
    verbose=1
)

# Save a quick graph
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))
ax1.plot(history.history['accuracy'], color='#8B5E3C', label='Train')
ax1.plot(history.history['val_accuracy'], color='#D4A574', linestyle='--', label='Val')
ax1.set_title('Accuracy (quick test)'); ax1.legend(); ax1.grid(True, alpha=0.3)
ax2.plot(history.history['loss'], color='#8B5E3C', label='Train')
ax2.plot(history.history['val_loss'], color='#D4A574', linestyle='--', label='Val')
ax2.set_title('Loss (quick test)'); ax2.legend(); ax2.grid(True, alpha=0.3)
fig.patch.set_facecolor('#FFF8ED')
plt.tight_layout()
graph_path = os.path.join(MODEL_DIR, 'quick_test_graph.png')
plt.savefig(graph_path, dpi=100, bbox_inches='tight')
plt.close()

print("\n" + "=" * 55)
print("  PIPELINE TEST PASSED")
print("=" * 55)
print(f"  Train accuracy (epoch 2) : {history.history['accuracy'][-1]*100:.2f}%")
print(f"  Val   accuracy (epoch 2) : {history.history['val_accuracy'][-1]*100:.2f}%")
print()
print("  NOTE: These numbers are low because:")
print("    - Only 500 images used (real training uses 7155)")
print("    - Only 2 epochs run   (real training uses up to 25)")
print("    - No accuracy claim is made from this test")
print()
print("  Graph saved -> model/quick_test_graph.png")
print()
print("  NEXT STEP:")
print("  Upload your files to Kaggle or Google Colab")
print("  with GPU enabled, then run: python train_model.py")
print("=" * 55)
