"""
Quick dry-run: build the model, print summary, check shapes.
Does NOT train. Run with: python test_model_build.py
"""
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow.keras import Model
from tensorflow.keras.layers import GlobalAveragePooling2D, Dense, Dropout
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from tensorflow.keras.preprocessing.image import ImageDataGenerator

SPLITS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'dataset', 'splits')

print("=" * 55)
print("  MODEL BUILD DRY-RUN")
print("=" * 55)

# 1. Load class names
with open(os.path.join(SPLITS_DIR, 'class_names.txt'), 'r') as f:
    class_names = [l.strip() for l in f.readlines()]
num_classes = len(class_names)
print(f"\n[1] Classes loaded     : {num_classes}")

# 2. Load split sizes
df_train = pd.read_csv(os.path.join(SPLITS_DIR, 'train_split.csv'))
df_val   = pd.read_csv(os.path.join(SPLITS_DIR, 'val_split.csv'))
df_test  = pd.read_csv(os.path.join(SPLITS_DIR, 'test_split.csv'))
print(f"[2] Train/Val/Test     : {len(df_train)} / {len(df_val)} / {len(df_test)}")

# 3. Build model (same code as train_model.py)
print("\n[3] Building MobileNetV2 model ...")
base_model = MobileNetV2(
    input_shape=(224, 224, 3),
    include_top=False,
    weights='imagenet'
)
base_model.trainable = False
x = base_model.output
x = GlobalAveragePooling2D()(x)
x = Dropout(0.3)(x)
predictions = Dense(num_classes, activation='softmax')(x)
model = Model(inputs=base_model.input, outputs=predictions)

# 4. Compile
model.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=1e-3),
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

# 5. Count parameters
total_params     = model.count_params()
trainable_params = sum(tf.size(w).numpy() for w in model.trainable_weights)
frozen_params    = total_params - trainable_params

print(f"\n[4] Model summary:")
print(f"    Input shape          : (None, 224, 224, 3)")
print(f"    Base model           : MobileNetV2 (imagenet weights)")
print(f"    Base layers          : {len(base_model.layers)}")
print(f"    Head layers          : GlobalAveragePooling2D -> Dropout(0.3) -> Dense({num_classes}, softmax)")
print(f"    Total parameters     : {total_params:,}")
print(f"    Trainable (Phase 1)  : {trainable_params:,}  (head only)")
print(f"    Frozen   (Phase 1)   : {frozen_params:,}  (MobileNetV2 base)")
print(f"    Output shape         : (None, {num_classes})")

# 6. Verify a dummy forward pass with random data
print("\n[5] Running dummy forward pass ...")
dummy_input  = np.random.uniform(-1, 1, (2, 224, 224, 3)).astype('float32')
dummy_output = model.predict(dummy_input, verbose=0)
print(f"    Input  shape         : {dummy_input.shape}")
print(f"    Output shape         : {dummy_output.shape}  (2 images, {num_classes} class probs)")
print(f"    Output sum (row 0)   : {dummy_output[0].sum():.6f}  (should be ~1.0)")
print(f"    Max prob  (row 0)    : {dummy_output[0].max():.4f}")
print(f"    Argmax    (row 0)    : class {dummy_output[0].argmax()} = {class_names[dummy_output[0].argmax()]}")

# 7. Verify iterator build
print("\n[6] Verifying data iterator construction ...")
gen = ImageDataGenerator(preprocessing_function=preprocess_input)
it  = gen.flow_from_dataframe(
    dataframe=df_train.head(64),
    x_col='filepath', y_col='breed',
    target_size=(224, 224), color_mode='rgb',
    class_mode='categorical', batch_size=8, shuffle=False
)
batch_x, batch_y = next(it)
print(f"    Mini-batch images    : {batch_x.shape}")
print(f"    Mini-batch labels    : {batch_y.shape}")
print(f"    Pixel range          : [{batch_x.min():.3f}, {batch_x.max():.3f}]  (expect -1 to 1)")
print(f"    Label sum (row 0)    : {batch_y[0].sum():.1f}  (one-hot, expect 1)")

print("\n" + "=" * 55)
print("  DRY-RUN PASSED -- model is ready for training.")
print("  Run:  python train_model.py")
print("=" * 55)
