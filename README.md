# Dog Breed Identification System

**B.Tech Data Science Project**  
*A Two-Stage Deep Learning & Full-Stack Web Application for Automated Canine Classification*

---

## Project Overview

**Dog Breed Identification** is an end-to-end Machine Learning web platform designed to accurately classify dog images across **120 distinct breeds** based on the Kaggle Dog Breed Identification dataset (derived from the Stanford Dogs dataset). The platform integrates a **two-stage classification pipeline**:

1. **Stage 1 - Dog Presence Detector:** Validates that the uploaded image actually contains a dog using an ImageNet-pretrained MobileNetV2 backbone. Non-dog images (cats, horses, vehicles, landscapes) are immediately rejected with a friendly message.
2. **Stage 2 - Fine-Grained Breed Classifier:** Classifies the dog into one of 120 breeds with top-1 prediction, confidence percentages, and top-3 ranked alternatives.

The application is built on **Python Flask**, with a persistent **MySQL** relational database, **Werkzeug** security, **ReportLab** PDF report generation, and interactive **Chart.js** analytics wrapped in a clean, responsive cream-and-brown UI.

---

## Key Features

- **Two-Stage Deep Learning Pipeline:**
  - Real-time image validation preventing non-dog misclassifications.
  - Fine-grained identification across 120 canine classes.
  - Ranked Top-3 breed predictions with visual confidence progress bars.
- **Instant PDF Prediction Report:**
  - Generates downloadable academic-grade PDF reports with uploaded image, primary breed, top-3 candidates, timestamp, model version, and scientific disclaimers.
- **User Authentication & Authorization:**
  - User registration, login, and logout powered by Flask sessions and Werkzeug cryptographic password hashing (PBKDF2/SHA-256).
  - Role-Based Access Control (RBAC): Regular Users vs. Administrators.
- **Personal Prediction History:**
  - Automatically records user predictions with thumbnail preview, date/time, confidence, and Top 3 details in MySQL.
  - Supports individual record deletion and full history clear.
- **Favorite Breeds Bookmarking:**
  - One-click bookmarking of favourite breeds directly from the directory cards.
- **120-Breed Directory & Side-by-Side Comparison:**
  - Complete directory with search and size filter (Small, Medium, Large, Giant).
  - Interactive comparison tool comparing temperament, lifespan, origin, and size of any two breeds side by side.
- **Model Performance Analytics:**
  - Training/validation accuracy & loss curves.
  - Evaluation metrics: 77.64% test accuracy, 96.87% top-5 accuracy.
  - Detailed analysis and horizontal bar chart of the **Top 12 Most Frequently Confused Dog Breeds** (e.g. Whippet vs. Italian Greyhound, Lhasa vs. Shih-Tzu).
- **Secure Admin Dashboard:**
  - Protected route (`/admin`) displaying real-time MySQL statistics: total users, total predictions, average confidence, top predicted breeds, user management (grant/revoke admin), and model version breakdown.

---

## System Architecture

```
DOG BREED IDENTIFICATION/
|
|-- app.py                      # Main Flask application & API routes
|-- config.py                   # Environment configuration & DB connection loader
|-- requirements.txt            # Python dependencies
|-- README.md                   # Comprehensive project documentation
|-- labels.csv                  # Dataset image IDs and corresponding breed labels (10,222 rows)
|-- sample_submission.csv       # Kaggle sample submission format (120 classes)
|
|-- train/                      # [Excluded from Git - download if retraining] 10,222 labeled images
|-- test/                       # [Excluded from Git - optional] 10,357 unlabeled test images
|
|-- database/                   # Database scripts and JSON data
|   |-- database_setup.sql      # MySQL schema creation script (4 tables)
|   |-- setup_db.py             # Automatic database initialization script
|   |-- make_admin.py           # Admin promotion utility script
|   |-- db.py                   # Parameterized MySQL database helper module
|   \-- breeds_data.json        # Detailed metadata for 120 dog breeds
|
|-- model/                      # Trained model and performance metrics (Included in repo)
|   |-- best_model.keras        # Trained MobileNetV2 fine-tuned model (120 classes)
|   |-- class_names.txt         # List of 120 breed class names
|   \-- performance_metrics.json# Model test metrics & confusion records
|
|-- dataset/                    # Dataset processing utilities
|   |-- splits/                 # Train / Val / Test CSV partition files (relative paths)
|   |   |-- train_split.csv     # 7,155 training samples (70%)
|   |   |-- val_split.csv       # 1,533 validation samples (15%)
|   |   \-- test_split.csv      # 1,534 held-out test samples (15%)
|   \-- preprocess.py           # Stratified data splitting and augmentation
|
|-- train_model.py              # Transfer learning training pipeline
|-- dataset_analysis.py         # Exploratory data analysis on dataset
|-- test_model_build.py         # Dry-run script to verify model build & tensor shapes
|-- quick_train_test.py         # Quick pipeline test on small sample
|-- run_complete_tests.py       # 18-Point automated testing suite
|
|-- templates/                  # Jinja2 HTML templates
|   |-- base.html               # Master layout with auth-aware navigation & flash alerts
|   |-- index.html              # Homepage with features and project overview
|   |-- identify.html           # Drag-and-drop image prediction interface
|   |-- breeds.html             # 120-Breed directory & side-by-side comparison
|   |-- performance.html        # Model performance evaluation & charts
|   |-- history.html            # User prediction history with modal & PDF
|   |-- favorites.html          # Bookmarked dog breeds grid
|   |-- admin.html              # Administrator statistical dashboard & user controls
|   |-- login.html              # User login page
|   |-- signup.html             # User registration page
|   |-- about.html              # Methodology, architecture & dataset details
|   \-- 403.html                # Access forbidden error page
|
|-- static/                     # Static assets
|   |-- css/
|   |   \-- style.css           # Responsive stylesheet (warm cream & brown palette)
|   |-- js/
|   |   \-- main.js             # Client-side validation, drag-and-drop & AJAX
|   \-- images/
|       |-- uploads/            # Server storage for user-uploaded prediction images
|       \-- breeds/             # Breed reference thumbnail images (120 breeds)
|
\-- utils/                      # Helper utility modules
    |-- __init__.py
    \-- pdf_generator.py        # ReportLab PDF report generation engine
```

---

## Dataset Details & Setup

### Dataset Source & Structure
This project utilizes the **Kaggle Dog Breed Identification** competition dataset, which is derived from the **Stanford Dogs dataset**:
- **Dataset Distinction:** The original Stanford Dogs dataset contains 20,580 images categorized into class subdirectories. In contrast, the Kaggle competition dataset organizes them into flat folders with a standalone label file:
  - **10,222 labeled training images** stored in a flat `train/` directory, mapped by `labels.csv` to 120 purebred dog classes.
  - **10,357 unlabeled test images** in a `test/` directory, used for competition submission ranking.
- **Classes:** 120 distinct purebred dog breeds.
- **Image Input Size:** 224 x 224 pixels, 3 color channels (RGB).
- **Class Balance:** Approximately 66 to 126 images per breed class, providing a well-balanced multi-class target.

### Partitioning & Split Files
The 10,222 labeled images were partitioned using stratified sampling to ensure equal breed representation across all splits:
- **Training Set (70%):** 7,155 images (`dataset/splits/train_split.csv`)
- **Validation Set (15%):** 1,533 images (`dataset/splits/val_split.csv`)
- **Testing Set (15%):** 1,534 images (`dataset/splits/test_split.csv`)

All split CSV files reference images via clean, cross-platform relative paths (`train/<image_id>.jpg`).

---

## Dataset Download & Placement (Optional for Retraining)

### Pre-Trained Model Already Included
The trained MobileNetV2 neural network checkpoint (`model/best_model.keras`), class names list (`model/class_names.txt`), performance metrics (`model/performance_metrics.json`), and breed metadata (`database/breeds_data.json`) are **fully included** in this GitHub repository.

**You do NOT need to download the raw images or retrain the model to run the website.** The Flask prediction application, user management, history logging, PDF reports, and admin dashboard work immediately after completing the standard installation steps.

### When to Download the Raw Images
The raw image folders (`train/` and `test/`) exceed several gigabytes in uncompressed size and are excluded from this GitHub repository to maintain a fast, lightweight clone. You only need to download the raw dataset if you plan to:
- Re-run exploratory dataset analysis (`python dataset_analysis.py`).
- Regenerate the stratified CSV splits (`python preprocess.py`).
- Retrain or fine-tune the model from scratch (`python train_model.py` or `python quick_train_test.py`).

### How to Download and Setup the Images:
1. Obtain the dataset from the Kaggle competition:
   - Web: [Kaggle Dog Breed Identification](https://www.kaggle.com/c/dog-breed-identification/data)
   - Kaggle CLI:
     ```bash
     kaggle competitions download -c dog-breed-identification
     ```
2. Extract the downloaded archive into the project root directory:
   - Unzip `train.zip` directly into the project root so the folder `train/` contains all 10,222 `.jpg` files (e.g. `train/000bec180eb18c7604dcecc8fe0dba07.jpg`).
   - (Optional) Unzip `test.zip` directly into the project root as `test/`.
3. Expected directory layout:
   ```
   DOG BREED IDENTIFICATION/
   |-- train/                  # Contains 10,222 JPG images
   |-- test/                   # (Optional) Contains 10,357 JPG images
   |-- labels.csv              # Included in repository
   |-- dataset/splits/         # Included in repository (train/val/test CSVs)
   |-- model/best_model.keras  # Included in repository (pre-trained model)
   ```

---

## Model Training & Transfer Learning

The fine-grained classifier is built using **Transfer Learning** on **MobileNetV2** pre-trained on ImageNet.

### Why MobileNetV2?
- **Depthwise Separable Convolutions:** Drastically reduces model parameters (~3.5 million parameters) compared to ResNet-50 (~25M) or VGG-16 (~138M).
- **Fast Inference:** Runs smoothly on CPU environments with low latency (<150ms per image).
- **Inverted Residual Blocks:** Retains rich feature representation while maintaining lightweight execution.

### Training Architecture:
1. **Base Backbone:** `MobileNetV2(weights='imagenet', include_top=False, input_shape=(224, 224, 3))`
2. **Global Average Pooling:** `GlobalAveragePooling2D()` to compress feature maps into a 1D vector.
3. **Regularization:** `Dropout(0.3)` to prevent overfitting.
4. **Output Layer:** `Dense(120, activation='softmax')` for multi-class probability output.
5. **Loss Function:** `categorical_crossentropy`
6. **Optimizer:** `Adam(learning_rate=0.001)` with learning rate scheduling.
7. **Augmentation:** Random rotation, zoom, width/height shifts, and horizontal flips.

To re-run data preparation and training (requires the downloaded `train/` folder):
```bash
# 1. Run exploratory dataset analysis
python dataset_analysis.py

# 2. Generate train/validation/test splits
python preprocess.py

# 3. Train the model (or use Kaggle / Colab GPU)
python train_model.py
```

---

## Installation & Setup Instructions

### Prerequisites
- **Python 3.8 to 3.13** installed.
- **MySQL Server** (e.g., MySQL 8.0, XAMPP, or MariaDB) running locally on port 3306.

### Step 1 - Clone / Download Project
Open terminal in the project directory:
```bash
cd "DOG BREED IDENTIFICATION"
```

### Step 2 - Create Virtual Environment (Recommended)
```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Linux/macOS:
source venv/bin/activate
```

### Step 3 - Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4 - Configure Database Credentials
Create or edit your `.env` file in the project root:
```ini
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_NAME=dog_breed_db
SECRET_KEY=dog-breed-ds-project-key-2026
FLASK_DEBUG=True
```

### Step 5 - Initialize MySQL Database
Run the automated database setup script:
```bash
python database/setup_db.py
```
This automatically connects to MySQL, creates `dog_breed_db` (if missing), and configures all 4 tables: `users`, `prediction_history`, `favorite_breeds`, and `feedback`.

### Step 6 - Run the Automated Test Suite
Verify that all 18 subsystems are working 100%:
```bash
python run_complete_tests.py
```
*(All 18 checkpoints should display `[PASS]`.)*

### Step 7 - Launch the Web Server
```bash
python app.py
```
Open your browser and navigate to: **http://127.0.0.1:5000**

---

## Creating & Accessing the Admin Dashboard

1. Start the Flask server (`python app.py`).
2. Go to **http://127.0.0.1:5000/signup** and register a user account (e.g., username `admin`).
3. In your terminal, run the admin promotion script:
   ```bash
   python database/make_admin.py
   ```
   Type the username you registered and press Enter.
4. Log out and log back in on the website.
5. The **Admin** link will appear in your top navigation bar, opening the statistical dashboard at **http://127.0.0.1:5000/admin**.

---

## College Review & Viva Demonstration Guide

When presenting this project during a B.Tech review or viva, follow this structured demonstration flow:

### 1. Introduction & Problem Statement (1 minute)
- Explain that canine image identification is challenging due to **high intra-class variance** (different fur colors and poses in the same breed) and **low inter-class variance** (visually identical breeds such as Whippet vs. Italian Greyhound or Siberian Husky vs. Eskimo Dog).
- Introduce your solution: a two-stage deep learning pipeline with full-stack database tracking.

### 2. Live Feature Walkthrough (3-4 minutes)
1. **Dog vs. Non-Dog Validation:**
   - Upload a non-dog photo (e.g. horse, cat, car).
   - Show how the model immediately flags `No Dog Detected` instead of forcing a fake dog breed prediction.
2. **Breed Prediction & Top 3:**
   - Upload a genuine dog photo (e.g., Labrador Retriever or Siberian Husky).
   - Point out the primary prediction, confidence percentage, and top 3 alternatives.
3. **Instant PDF Report:**
   - Click **Download Prediction Report (PDF)**.
   - Open the generated PDF showing the embedded image, prediction metrics, timestamp, and academic disclaimer.
4. **User Auth & Prediction History:**
   - Show registration and login.
   - Navigate to **History** to show how real predictions are stored in MySQL with timestamp and preview.
   - Demonstrate the modal view and delete option.
5. **Breed Directory & Side-by-Side Comparison:**
   - Navigate to **Breed Info**.
   - Show real-time search and size filtering across the 120 breeds.
   - Switch to the **Compare Two Breeds** tab and select two similar breeds (e.g., Whippet and Italian Greyhound) to show side-by-side traits.
6. **Model Performance & Visual Similarity Analysis:**
   - Navigate to **Performance**.
   - Show the training/validation accuracy curves and explain the **Commonly Confused Dog Breeds** section highlighting visual similarity reasons.
7. **Admin Dashboard:**
   - Show the protected **Admin** panel with live user counts, prediction metrics, and Chart.js analytics.

### 3. Frequently Asked Viva Questions & Answers

| Viva Question | Concise Student Answer |
|---|---|
| **Why did you use Transfer Learning instead of training a CNN from scratch?** | Training a CNN from scratch on 120 classes with only ~10,000 images would lead to severe overfitting. Pretrained MobileNetV2 already learned rich low-level visual features (edges, textures, shapes) from ImageNet's 1.4 million images, enabling high accuracy with faster convergence. |
| **How does the Dog vs. Non-Dog detector work?** | It uses an ImageNet classification backbone. ImageNet contains 118 specific dog class indices (151-268, plus 273 and 275). If the top-1 predicted class is within these dog indices or the cumulative dog probability exceeds the threshold (0.20), the image is validated as a dog; otherwise, it is rejected. |
| **What does Top-5 Accuracy mean?** | Top-5 accuracy measures whether the true ground-truth breed is among the model's top 5 highest probability predictions. Our model achieves **96.87% top-5 accuracy**, demonstrating that even when the top-1 prediction misses, the correct breed is almost always within the top candidates. |
| **Why do certain breeds get misclassified?** | Breeds like Whippet vs. Italian Greyhound or Lhasa vs. Shih-Tzu share identical body silhouettes, facial structures, and coat textures. Without scale context (size reference in the image), 2D CNNs naturally assign close probabilities to both. |
| **How is password security handled?** | We use Werkzeug's `generate_password_hash` and `check_password_hash` which employ PBKDF2 with SHA-256 and unique cryptographic salts. Passwords are never stored as plain text. |
| **How are SQL injection attacks prevented?** | All database queries use parameterized SQL execution (`%s` placeholders with tuple parameters) across all CRUD operations in `database/db.py`. |

---

## Comprehensive 18-Point Testing Checklist

| # | Test Area | Status | Verified Behavior |
|---|---|---|---|
| 01 | **Flask Application Startup** | PASS | App initializes cleanly with secure secret key and configuration. |
| 02 | **Homepage Navigation** | PASS | Renders homepage (HTTP 200) with links to Identify, Breeds, Performance, About. |
| 03 | **Image Upload** | PASS | Handles multipart POST upload, validates file, and stores in `static/images/uploads/`. |
| 04 | **Invalid Image Handling** | PASS | Gracefully handles missing files, empty filenames, disallowed extensions, and corrupted images. |
| 05 | **Dog/Non-Dog Validation** | PASS | Correctly rejects non-dog images and accepts valid dog images. |
| 06 | **ML Model Loading** | PASS | MobileNetV2 model loads correctly with (224, 224, 3) input and 120 output classes. |
| 07 | **Breed Prediction** | PASS | Produces non-empty breed name and valid confidence float. |
| 08 | **Top 3 Confidence Scores** | PASS | Returns exactly 3 breeds sorted descending with sum <= 100%. |
| 09 | **MySQL Database Connection** | PASS | Connects to `dog_breed_db`; verifies `users`, `prediction_history`, `favorite_breeds`, `feedback`. |
| 10 | **Signup and Login** | PASS | Validates inputs, prevents duplicate emails, verifies hashed passwords, and manages sessions. |
| 11 | **Prediction History** | PASS | Restricts access to authenticated users; displays records filtered by `user_id`. |
| 12 | **Favourite Breeds** | PASS | AJAX toggle correctly saves and removes bookmarked breeds. |
| 13 | **Breed Info Page** | PASS | Renders directory of all 120 breeds with photos and attributes. |
| 14 | **Breed Comparison** | PASS | Compares two breeds side by side on size, lifespan, origin, and temperament. |
| 15 | **Model Performance Charts** | PASS | Displays evaluation metrics, accuracy curves, and 12-pair confusion breakdown. |
| 16 | **PDF Report Download** | PASS | Generates formatted PDF document with image, top-3 predictions, and metadata. |
| 17 | **Admin Dashboard Access Control** | PASS | Enforces RBAC: guests get redirected (302), normal users get 403, admins get 200. |
| 18 | **Responsive Design** | PASS | Viewport meta tag configured; responsive breakpoints at 480px, 600px, 768px, 900px. |

---

## Academic Declaration

This project was developed as a B.Tech Data Science project. All model evaluations, performance metrics, and database implementations represent genuine test results.
