"""
train_model.py
==============
Dog Breed Identification -- Phase 6: Model Training
B.Tech Data Science Project

MODEL ARCHITECTURE (simple explanation):
-----------------------------------------
We use "Transfer Learning" with MobileNetV2.
Transfer learning means we borrow a model already trained on
1.4 million ImageNet images and re-use its ability to detect
visual features (edges, textures, shapes, colours).
We only need to teach the last few layers to distinguish dog breeds.

Layers added on top:
  GlobalAveragePooling2D  -- compresses the feature map to a 1D vector
  Dropout(0.3)            -- randomly turns off 30% of neurons during
                             training to prevent overfitting
  Dense(120, softmax)     -- outputs a probability for each of 120 breeds

Training happens in 2 phases:
  Phase 1 -- Freeze all MobileNetV2 layers, train only our new layers
  Phase 2 -- Unfreeze the last 30 MobileNetV2 layers and fine-tune them
             at a much lower learning rate

Usage:
  python train_model.py

Output files (saved to model/):
  best_model.keras         -- the best model checkpoint
  class_names.txt          -- 120 breed names (1 per line)
  training_phase1.png      -- accuracy and loss graphs for Phase 1
  training_phase2.png      -- accuracy and loss graphs for Phase 2
  evaluation_results.txt   -- test set metrics
"""

import os
import numpy as np
import pandas as pd

# -- Suppress TensorFlow startup messages for cleaner output --
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

import tensorflow as tf
from tensorflow.keras import Model
from tensorflow.keras.layers import GlobalAveragePooling2D, Dense, Dropout
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.callbacks import (
    EarlyStopping,
    ModelCheckpoint,
    ReduceLROnPlateau
)

import matplotlib
matplotlib.use('Agg')          # save plots to file without opening a window
import matplotlib.pyplot as plt

SEPARATOR = "=" * 62

# ==============================================================
#  CONFIGURATION  -- edit these values if needed
# ==============================================================

IMG_SIZE    = 224              # MobileNetV2 expects 224 x 224
BATCH_SIZE  = 32
RANDOM_SEED = 42

# Phase 1: train only the new classification head
EPOCHS_PHASE1 = 15            # EarlyStopping will stop sooner if needed
LR_PHASE1     = 1e-3          # standard Adam learning rate

# Phase 2: fine-tune the top layers of MobileNetV2
FINE_TUNE        = True        # set False to skip fine-tuning
FINE_TUNE_LAYERS = 30          # unfreeze the last 30 layers
EPOCHS_PHASE2    = 10
LR_PHASE2        = 1e-5        # much smaller lr for fine-tuning

DROPOUT_RATE = 0.3             # fraction of neurons to drop

# -- Paths --
BASE_DIR    = os.path.dirname(os.path.abspath(__file__))
SPLITS_DIR  = os.path.join(BASE_DIR, 'dataset', 'splits')
TRAIN_DIR   = os.path.join(BASE_DIR, 'train')
MODEL_DIR   = os.path.join(BASE_DIR, 'model')
os.makedirs(MODEL_DIR, exist_ok=True)

MODEL_PATH       = os.path.join(MODEL_DIR, 'best_model.keras')
CLASS_NAMES_PATH = os.path.join(MODEL_DIR, 'class_names.txt')
EVAL_PATH        = os.path.join(MODEL_DIR, 'evaluation_results.txt')
GRAPH1_PATH      = os.path.join(MODEL_DIR, 'training_phase1.png')
GRAPH2_PATH      = os.path.join(MODEL_DIR, 'training_phase2.png')


# ==============================================================
#  HELPER: plot training history
# ==============================================================

def save_training_graph(history, save_path, phase_label):
    """
    Plot accuracy and loss for both training and validation.
    Saves the figure to save_path instead of showing it on screen.
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    fig.suptitle(f'Training History -- {phase_label}', fontsize=14)

    epochs_ran = range(1, len(history.history['accuracy']) + 1)

    # -- Accuracy plot --
    ax1.plot(epochs_ran, history.history['accuracy'],
             color='#8B5E3C', linewidth=2, label='Train Accuracy')
    ax1.plot(epochs_ran, history.history['val_accuracy'],
             color='#D4A574', linewidth=2, linestyle='--', label='Val Accuracy')
    ax1.set_title('Accuracy')
    ax1.set_xlabel('Epoch')
    ax1.set_ylabel('Accuracy')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    ax1.set_facecolor('#FFF8ED')

    # -- Loss plot --
    ax2.plot(epochs_ran, history.history['loss'],
             color='#8B5E3C', linewidth=2, label='Train Loss')
    ax2.plot(epochs_ran, history.history['val_loss'],
             color='#D4A574', linewidth=2, linestyle='--', label='Val Loss')
    ax2.set_title('Loss')
    ax2.set_xlabel('Epoch')
    ax2.set_ylabel('Loss')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    ax2.set_facecolor('#FFF8ED')

    fig.patch.set_facecolor('#FFF8ED')
    plt.tight_layout()
    plt.savefig(save_path, dpi=120, bbox_inches='tight')
    plt.close()
    print(f"    Graph saved -> {save_path}")


# ==============================================================
#  STEP 1 -- Load class names and split CSVs
# ==============================================================
print(SEPARATOR)
print("  DOG BREED IDENTIFICATION -- Model Training")
print(SEPARATOR)

print("\n[Step 1] Loading class names and dataset splits ...")

# Read class names saved by preprocess.py
with open(os.path.join(SPLITS_DIR, 'class_names.txt'), 'r') as f:
    class_names = [line.strip() for line in f.readlines()]

num_classes = len(class_names)
print(f"    Number of breed classes : {num_classes}")
print(f"    First 5 classes         : {class_names[:5]}")

# Load the pre-split DataFrames
df_train = pd.read_csv(os.path.join(SPLITS_DIR, 'train_split.csv'))
df_val   = pd.read_csv(os.path.join(SPLITS_DIR, 'val_split.csv'))
df_test  = pd.read_csv(os.path.join(SPLITS_DIR, 'test_split.csv'))

print(f"    Train images : {len(df_train)}")
print(f"    Val images   : {len(df_val)}")
print(f"    Test images  : {len(df_test)}")

# Copy class names into model/ folder for use during inference
with open(CLASS_NAMES_PATH, 'w') as f:
    for name in class_names:
        f.write(name + '\n')
print(f"    Class names saved -> {CLASS_NAMES_PATH}")


# ==============================================================
#  STEP 2 -- Create ImageDataGenerators and iterators
# ==============================================================
print("\n[Step 2] Creating data generators ...")

# Training generator: normalise + augmentation
train_gen = ImageDataGenerator(
    preprocessing_function=preprocess_input,
    horizontal_flip=True,
    rotation_range=15,
    zoom_range=0.10,
    width_shift_range=0.10,
    height_shift_range=0.10,
    fill_mode='nearest'
)

# Validation and test generators: normalise only, no augmentation
val_gen  = ImageDataGenerator(preprocessing_function=preprocess_input)
test_gen = ImageDataGenerator(preprocessing_function=preprocess_input)

train_iter = train_gen.flow_from_dataframe(
    dataframe=df_train,
    directory=BASE_DIR,
    x_col='filepath',
    y_col='breed',
    target_size=(IMG_SIZE, IMG_SIZE),
    color_mode='rgb',
    class_mode='categorical',  # one-hot labels for 120 classes
    batch_size=BATCH_SIZE,
    shuffle=True,
    seed=RANDOM_SEED
)

val_iter = val_gen.flow_from_dataframe(
    dataframe=df_val,
    directory=BASE_DIR,
    x_col='filepath',
    y_col='breed',
    target_size=(IMG_SIZE, IMG_SIZE),
    color_mode='rgb',
    class_mode='categorical',
    batch_size=BATCH_SIZE,
    shuffle=False
)

test_iter = test_gen.flow_from_dataframe(
    dataframe=df_test,
    directory=BASE_DIR,
    x_col='filepath',
    y_col='breed',
    target_size=(IMG_SIZE, IMG_SIZE),
    color_mode='rgb',
    class_mode='categorical',
    batch_size=BATCH_SIZE,
    shuffle=False
)

train_steps = int(np.ceil(len(df_train) / BATCH_SIZE))
val_steps   = int(np.ceil(len(df_val)   / BATCH_SIZE))
test_steps  = int(np.ceil(len(df_test)  / BATCH_SIZE))


# ==============================================================
#  STEP 3 -- Build the model
# ==============================================================
print("\n[Step 3] Building MobileNetV2 transfer learning model ...")

# Load MobileNetV2 pretrained on ImageNet.
# include_top=False means we remove the original 1000-class head.
# We will add our own output layer for 120 dog breeds.
base_model = MobileNetV2(
    input_shape=(IMG_SIZE, IMG_SIZE, 3),
    include_top=False,          # remove the ImageNet head
    weights='imagenet'          # use pre-trained ImageNet weights
)

# Freeze ALL base model layers for Phase 1.
# This means only our new layers will learn during Phase 1.
# The base model weights stay fixed.
base_model.trainable = False

# Add our classification head on top
x = base_model.output

# GlobalAveragePooling2D:
# Takes the final feature map (7 x 7 x 1280) and averages each
# feature channel into a single number -> output shape: (1280,)
x = GlobalAveragePooling2D()(x)

# Dropout:
# During training, randomly sets 30% of neurons to zero.
# This forces the model not to rely too heavily on any single
# neuron, which prevents overfitting.
x = Dropout(DROPOUT_RATE)(x)

# Dense output layer:
# 120 neurons, one for each dog breed.
# Softmax converts raw scores to probabilities that sum to 1.0
predictions = Dense(num_classes, activation='softmax')(x)

# Combine base + head into one model
model = Model(inputs=base_model.input, outputs=predictions)

# Count trainable vs frozen parameters
total_params     = model.count_params()
trainable_params = sum(
    tf.size(w).numpy() for w in model.trainable_weights
)
frozen_params = total_params - trainable_params

print(f"    Total parameters      : {total_params:,}")
print(f"    Trainable (Phase 1)   : {trainable_params:,}  (new head only)")
print(f"    Frozen (Phase 1)      : {frozen_params:,}  (MobileNetV2 base)")
print(f"    Base model layers     : {len(base_model.layers)}")


# ==============================================================
#  STEP 4 -- Compile the model
# ==============================================================
print("\n[Step 4] Compiling model for Phase 1 ...")

# categorical_crossentropy: correct loss for multi-class with one-hot labels
# Adam: a popular optimiser that adapts the learning rate automatically
model.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=LR_PHASE1),
    loss='categorical_crossentropy',
    metrics=['accuracy']
)
print(f"    Optimizer  : Adam  (lr = {LR_PHASE1})")
print(f"    Loss       : categorical_crossentropy")
print(f"    Metric     : accuracy")


# ==============================================================
#  STEP 5 -- Define callbacks
# ==============================================================
print("\n[Step 5] Setting up callbacks ...")

# ModelCheckpoint: saves the model only when val_accuracy improves
# This ensures we always keep the best version, not the last version
checkpoint_cb = ModelCheckpoint(
    filepath=MODEL_PATH,
    monitor='val_accuracy',
    save_best_only=True,
    mode='max',
    verbose=1
)

# EarlyStopping: stops training if val_loss does not improve for 5 epochs
# restore_best_weights=True reloads the best weights when stopping
early_stop_cb = EarlyStopping(
    monitor='val_loss',
    patience=5,
    restore_best_weights=True,
    verbose=1
)

# ReduceLROnPlateau: if val_loss stops improving for 3 epochs,
# automatically cut the learning rate in half
reduce_lr_cb = ReduceLROnPlateau(
    monitor='val_loss',
    factor=0.5,
    patience=3,
    min_lr=1e-7,
    verbose=1
)

callbacks_phase1 = [checkpoint_cb, early_stop_cb, reduce_lr_cb]
print("    ModelCheckpoint    : save best val_accuracy")
print("    EarlyStopping      : patience=5, monitor val_loss")
print("    ReduceLROnPlateau  : patience=3, factor=0.5")


# ==============================================================
#  STEP 6 -- Phase 1 Training (frozen base)
# ==============================================================
print(f"\n[Step 6] Phase 1 Training (classification head only) ...")
print(f"    Max epochs : {EPOCHS_PHASE1}  (EarlyStopping may stop earlier)")
print(f"    Batch size : {BATCH_SIZE}")
print(f"    Train steps per epoch : {train_steps}")
print()

history1 = model.fit(
    train_iter,
    steps_per_epoch=train_steps,
    epochs=EPOCHS_PHASE1,
    validation_data=val_iter,
    validation_steps=val_steps,
    callbacks=callbacks_phase1,
    verbose=1
)

# Save Phase 1 graph
print("\n    Saving Phase 1 training graph ...")
save_training_graph(history1, GRAPH1_PATH, "Phase 1 - Head Training")

# Phase 1 best results
best_val_acc1 = max(history1.history['val_accuracy'])
best_val_loss1 = min(history1.history['val_loss'])
print(f"\n    Phase 1 results:")
print(f"      Best val_accuracy : {best_val_acc1:.4f} ({best_val_acc1*100:.2f}%)")
print(f"      Best val_loss     : {best_val_loss1:.4f}")
print(f"      Epochs trained    : {len(history1.history['accuracy'])}")


# ==============================================================
#  STEP 7 -- Phase 2 Fine-tuning (optional)
# ==============================================================
history2 = None

if FINE_TUNE:
    print(f"\n[Step 7] Phase 2 Fine-tuning (last {FINE_TUNE_LAYERS} base layers) ...")
    print(f"    Learning rate : {LR_PHASE2}  (much smaller than Phase 1)")
    print()

    # Unfreeze the LAST N layers of the base model.
    # The early layers learn basic features (edges, colours) that apply
    # to all images. The later layers learn more specific features.
    # We only need to fine-tune those later, dog-specific features.
    base_model.trainable = True
    for layer in base_model.layers[:-FINE_TUNE_LAYERS]:
        layer.trainable = False   # keep early layers frozen

    # Count newly trainable parameters
    trainable_now = sum(
        tf.size(w).numpy() for w in model.trainable_weights
    )
    print(f"    Trainable parameters now : {trainable_now:,}")
    print(f"    (Base layers unfrozen    : last {FINE_TUNE_LAYERS})")

    # Recompile with a much lower learning rate
    # Using a high lr during fine-tuning would destroy the pre-trained weights
    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=LR_PHASE2),
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )

    # Different callbacks for Phase 2 (longer patience since lr is tiny)
    checkpoint_cb2 = ModelCheckpoint(
        filepath=MODEL_PATH,
        monitor='val_accuracy',
        save_best_only=True,
        mode='max',
        verbose=1
    )
    early_stop_cb2 = EarlyStopping(
        monitor='val_loss',
        patience=5,
        restore_best_weights=True,
        verbose=1
    )
    callbacks_phase2 = [checkpoint_cb2, early_stop_cb2]

    history2 = model.fit(
        train_iter,
        steps_per_epoch=train_steps,
        epochs=EPOCHS_PHASE2,
        validation_data=val_iter,
        validation_steps=val_steps,
        callbacks=callbacks_phase2,
        verbose=1
    )

    print("\n    Saving Phase 2 training graph ...")
    save_training_graph(history2, GRAPH2_PATH, "Phase 2 - Fine-tuning")

    best_val_acc2 = max(history2.history['val_accuracy'])
    best_val_loss2 = min(history2.history['val_loss'])
    print(f"\n    Phase 2 results:")
    print(f"      Best val_accuracy : {best_val_acc2:.4f} ({best_val_acc2*100:.2f}%)")
    print(f"      Best val_loss     : {best_val_loss2:.4f}")
    print(f"      Epochs trained    : {len(history2.history['accuracy'])}")

else:
    print("\n[Step 7] Fine-tuning skipped  (FINE_TUNE = False)")


# ==============================================================
#  STEP 8 -- Evaluate on the test set
# ==============================================================
print("\n[Step 8] Evaluating on the test set ...")
print("    Loading best saved model ...")

# Load the best model checkpoint saved during training
best_model = tf.keras.models.load_model(MODEL_PATH)

# Evaluate: returns [loss, accuracy] on the full test set
test_loss, test_accuracy = best_model.evaluate(
    test_iter,
    steps=test_steps,
    verbose=1
)

print(f"\n    Test Loss     : {test_loss:.4f}")
print(f"    Test Accuracy : {test_accuracy:.4f} ({test_accuracy*100:.2f}%)")


# ==============================================================
#  STEP 9 -- Save evaluation results to file
# ==============================================================
print(f"\n[Step 9] Saving evaluation results ...")

with open(EVAL_PATH, 'w') as f:
    f.write("DOG BREED IDENTIFICATION -- Model Evaluation Results\n")
    f.write("=" * 50 + "\n\n")
    f.write(f"Model Architecture    : MobileNetV2 + custom head\n")
    f.write(f"Number of classes     : {num_classes}\n")
    f.write(f"Image size            : {IMG_SIZE} x {IMG_SIZE}\n")
    f.write(f"Batch size            : {BATCH_SIZE}\n\n")

    f.write("Dataset split:\n")
    f.write(f"  Train : {len(df_train)} images\n")
    f.write(f"  Val   : {len(df_val)} images\n")
    f.write(f"  Test  : {len(df_test)} images\n\n")

    f.write("Phase 1 (Head training):\n")
    f.write(f"  Epochs trained    : {len(history1.history['accuracy'])}\n")
    f.write(f"  Best val_accuracy : {max(history1.history['val_accuracy']):.4f}\n")
    f.write(f"  Best val_loss     : {min(history1.history['val_loss']):.4f}\n\n")

    if history2:
        f.write("Phase 2 (Fine-tuning):\n")
        f.write(f"  Layers unfrozen   : last {FINE_TUNE_LAYERS}\n")
        f.write(f"  Epochs trained    : {len(history2.history['accuracy'])}\n")
        f.write(f"  Best val_accuracy : {max(history2.history['val_accuracy']):.4f}\n")
        f.write(f"  Best val_loss     : {min(history2.history['val_loss']):.4f}\n\n")

    f.write("Test Set Evaluation (measured on held-out data):\n")
    f.write(f"  Test Loss         : {test_loss:.4f}\n")
    f.write(f"  Test Accuracy     : {test_accuracy:.4f} ({test_accuracy*100:.2f}%)\n")

print(f"    Saved -> {EVAL_PATH}")


# ==============================================================
#  FINAL SUMMARY
# ==============================================================
print(f"\n{SEPARATOR}")
print("  TRAINING COMPLETE -- SUMMARY")
print(SEPARATOR)
print(f"  Dataset:")
print(f"    Train / Val / Test : {len(df_train)} / {len(df_val)} / {len(df_test)}")
print(f"    Classes            : {num_classes} breeds")
print()
print(f"  Phase 1 (head only, lr={LR_PHASE1}):")
print(f"    Epochs run         : {len(history1.history['accuracy'])}")
print(f"    Best val_accuracy  : {max(history1.history['val_accuracy'])*100:.2f}%")
if history2:
    print(f"  Phase 2 (fine-tune last {FINE_TUNE_LAYERS} layers, lr={LR_PHASE2}):")
    print(f"    Epochs run         : {len(history2.history['accuracy'])}")
    print(f"    Best val_accuracy  : {max(history2.history['val_accuracy'])*100:.2f}%")
print()
print(f"  Test Accuracy (measured): {test_accuracy*100:.2f}%")
print()
print(f"  Saved files (model/):")
print(f"    best_model.keras        -- trained model")
print(f"    class_names.txt         -- 120 breed names")
print(f"    training_phase1.png     -- Phase 1 graphs")
if history2:
    print(f"    training_phase2.png     -- Phase 2 graphs")
print(f"    evaluation_results.txt  -- test set metrics")
print(SEPARATOR)
print()
print("  Next step: integrate model into the Flask app (predict route)")
print()
