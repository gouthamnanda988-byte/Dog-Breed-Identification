# DOG BREED IDENTIFICATION USING DEEP LEARNING AND TRANSFER LEARNING

**Department of Computer Science and Engineering / Data Science**  
**B.Tech 3rd Year / Final Year – Academic Year 2025–2026**  
**Project Report**

---

### Project Team Members

| S.No. | Student Candidate Name | Roll Number | Individual Responsibility |
|:---:|---|:---:|---|
| 1 | **K Goutham Nayak** | **CS24B1081** | Backend Architecture, MySQL Database and PDF Reporting |
| 2 | **K Adithya** | **CS24B1091** | Deep Learning Model Architecture and Fine-Tuning |
| 3 | **R Mahesh Rathod** | **CS24B1071** | Two-Stage Canine Presence Detection and Validation |
| 4 | **G Vishnu Vardhan** | **CS24B1028** | Frontend UI/UX, Breed Directory and Trait Comparison |

**Institutional Guidance Placeholders:**  
- **Faculty Guide:** [Faculty Guide Name, Designation]  
- **Department:** [Department of Computer Science and Engineering / Data Science]  
- **Institution:** [Institution / College Name, Affiliated to University Name]  
- **Date of Submission:** [Date of Submission]  
- **Location:** [College Location / City]  

---

## PROJECT SPECIFICATIONS

| Specification Attribute | Implementation Details |
|---|---|
| **Course** | Introduction to Data Science for Engineers / Capstone Project |
| **Academic Degree** | Bachelor of Technology (B.Tech) in Computer Science / Data Science |
| **Core Model Architecture** | MobileNetV2 with Inverted Residuals and Linear Bottlenecks |
| **Transfer Learning Source** | ImageNet Pretrained Weights (1.4M images, 1,000 classes) |
| **Benchmark Dataset** | Stanford Dogs / Kaggle Dog Breed Identification |
| **Total Photographic Images** | 10,222 labeled JPEG photographs |
| **Canine Breed Classes** | 120 purebred domestic dog varieties |
| **Input Image Resolution** | 224 × 224 pixels (3-channel RGB) |
| **Inference Pipeline** | Two-Stage Architecture (Stage 1: Canine Filter; Stage 2: Breed Classifier) |
| **Web Application Framework** | Python Flask 3.0 (REST APIs, Session Management, Jinja2) |
| **Database Management** | MySQL 8.0 Server (`dog_breed_db` with 4 relational tables) |
| **Reporting Engine** | Python ReportLab 5.1 (Dynamic PDF prediction certificate generation) |
| **Top-1 Test Accuracy** | 77.64% (on 1,534 held-out evaluation test images) |
| **Top-5 Test Accuracy** | 96.87% (on 1,534 held-out evaluation test images) |
| **Average Inference Latency** | 120 to 160 milliseconds per image on standard CPU |
| **Model Weight Storage Size** | ~14 MB (`best_model.keras`) |

---

## ABSTRACT

Domestic canines (*Canis lupus familiaris*) represent the most morphologically diverse mammal on Earth, encompassing hundreds of purebred varieties characterized by subtle variations in cranial geometry, ear carriage, muzzle length, coat pigmentation, and grooming profiles. Automatically classifying dog breeds from digital photographs is a quintessential challenge in **Fine-Grained Visual Categorization (FGVC)**. Unlike coarse-grained object detection where classes exhibit distinct silhouettes (such as distinguishing a vehicle from a dog), fine-grained canine classification must resolve two competing computer vision difficulties: **low inter-class variance**, where biologically related breeds exhibit virtually identical physical appearances (for instance, Whippets and Italian Greyhounds, or Lhasa Apsos and Shih-Tzus), and **high intra-class variance**, where dogs of the same breed differ markedly across coat patterns, colors, age, body postures, and photographic lighting.

In this project, we designed, implemented, and thoroughly evaluated an end-to-end canine identification platform utilizing transfer learning with **MobileNetV2** and backed by a full-stack relational web architecture. Using the benchmark Stanford Dogs / Kaggle Dog Breed dataset comprising **10,222 labeled photographs** across **120 purebred categories**, we established a stratified 70% training (7,155 images), 15% validation (1,533 images), and 15% testing (1,534 images) partition. To resolve a pervasive limitation in existing classification systems—where non-dog inputs are arbitrarily forced into canine classes—we formulated an innovative **two-stage prediction pipeline**. In Stage 1, an upstream ImageNet-pretrained MobileNetV2 network evaluates whether an uploaded photograph contains a canine by monitoring 118 domestic and wild dog output categories, rejecting non-dog uploads (such as horses, felines, or vehicles) when the cumulative canine probability falls below 0.20. In Stage 2, verified canine images are classified by our fine-tuned MobileNetV2 architecture equipped with Global Average Pooling, 30% dropout regularization, and a 120-unit Softmax output layer.

Experimental evaluation on the 1,534 held-out test images demonstrated a **Top-1 test accuracy of 77.64%**, an exceptional **Top-5 test accuracy of 96.87%**, a test categorical cross-entropy loss of **0.7036**, and a macro F1-score of **76.91%**. On consumer CPU hardware, a complete forward pass completes in **120 to 160 milliseconds** with a compact model weight footprint of **14 MB**. Beyond model development, we engineered a complete web platform using Python Flask and MySQL. The application provides drag-and-drop image uploads, Top-3 ranked candidate scores with animated confidence bars, an interactive 120-breed directory with trait comparison, automated PDF report downloads via ReportLab, personal prediction histories, and an administrative analytics dashboard. The completed system was verified using an automated 18-point testing suite, with all tests passing successfully.

**Keywords:** Dog Breed Identification, Deep Learning, Transfer Learning, MobileNetV2, Fine-Grained Visual Categorization, Computer Vision, Flask, MySQL, ReportLab.

---

## TABLE OF CONTENTS

- **Project Specifications**
- **Abstract**
- **List of Figures**
- **List of Tables**
- **Chapter 1 – Introduction**
  - 1.1 Background of Dog Breed Identification
  - 1.2 Problem Statement
  - 1.3 Motivation
  - 1.4 Objectives
  - 1.5 Scope
  - 1.6 Proposed Approach
- **Chapter 2 – Literature Review**
  - 2.1 Research on Dog Breed Classification
  - 2.2 CNN-Based Classification
  - 2.3 Transfer Learning Approaches
  - 2.4 Comparison of Existing Research
  - 2.5 Research Gap
  - 2.6 Selection of MobileNetV2
- **Chapter 3 – Dataset and Image Preparation**
  - 3.1 Stanford Dogs Dataset
  - 3.2 Breed Categories
  - 3.3 Dataset Organization
  - 3.4 Training, Validation and Testing Split
  - 3.5 Image Resizing and Normalization
  - 3.6 Data Augmentation
  - 3.7 Dataset Challenges
- **Chapter 4 – Proposed Methodology**
  - 4.1 Overall System Architecture
  - 4.2 Image Input and Validation
  - 4.3 Dog Presence Verification
  - 4.4 MobileNetV2 Feature Extraction
  - 4.5 Transfer Learning and Fine-Tuning
  - 4.6 Breed Classification
  - 4.7 Prediction Confidence and Top-3 Results
  - 4.8 Complete Prediction Workflow
- **Chapter 5 – Model Development and Web Application**
  - 5.1 Development Environment
  - 5.2 Model Training
  - 5.3 Model Integration
  - 5.4 Flask Application Architecture
  - 5.5 Image Upload and Prediction
  - 5.6 User Authentication
  - 5.7 Breed Information
  - 5.8 Prediction History
  - 5.9 Database Design
  - 5.10 Other Implemented Features
- **Chapter 6 – Results and Discussion**
  - 6.1 Training and Validation Performance
  - 6.2 Accuracy and Loss
  - 6.3 Top-1 and Top-5 Accuracy
  - 6.4 Precision, Recall and F1-Score
  - 6.5 Prediction Examples
  - 6.6 Dog and Non-Dog Image Testing
  - 6.7 Commonly Confused Breeds
  - 6.8 Application Testing
  - 6.9 Observations
- **Chapter 7 – Conclusion and Future Enhancements**
  - 7.1 Project Summary
  - 7.2 Learning Outcomes
  - 7.3 Limitations
  - 7.4 Future Improvements
- **References**
- **Team Contributions**

---

## LIST OF FIGURES

1. **Figure 3.1:** Sample Distribution Across 120 Dog Breeds in the Stanford Dogs Dataset
2. **Figure 4.1:** Overall Multi-Tier System Architecture of the Dog Breed Identification Platform
3. **Figure 4.2:** Two-Stage Canine Detection and Fine-Grained Breed Classification Workflow
4. **Figure 4.3:** Transfer Learning Neural Network Architecture with MobileNetV2 Backbone
5. **Figure 5.1:** Administrative Dashboard Interface Displaying Real-Time Database Metrics and Top Breeds
6. **Figure 6.1:** Training and Validation Accuracy and Loss Curves Across 15 Epochs
7. **Figure 6.2:** Top 12 Most Frequently Confused Dog Breed Pairs in the Evaluation Set

---

## LIST OF TABLES

1. **Table 1.1:** Comparison Between Conventional Identification and Proposed System
2. **Table 2.1:** Structured Comparison of Existing Research on Canine Breed Classification
3. **Table 3.1:** Dataset Partitioning into Training, Validation, and Testing Sets
4. **Table 4.1:** Neural Network Layer Progression and Parameter Distribution
5. **Table 5.1:** Model Training Hyperparameter Configuration
6. **Table 5.2:** Relational Database Schema Design (`dog_breed_db`)
7. **Table 5.3:** Core Software Technologies and Functional Roles
8. **Table 6.1:** Model Performance Metrics on Held-Out Test Set (1,534 Images)
9. **Table 6.2:** Top 12 Most Frequently Confused Dog Breed Pairs with Visual Reasons
10. **Table 6.3:** Complete 18-Point Automated Application Test Suite Verification

---

# CHAPTER 1 – INTRODUCTION

### 1.1 Background of Dog Breed Identification
Computer vision has experienced extraordinary progress over the past decade through the emergence of deep Convolutional Neural Networks (CNNs). In traditional object recognition tasks, models are tasked with discriminating between broad object categories that possess fundamentally distinct shapes, edges, and silhouettes—such as separating a car from an airplane, or an animal from a building.

In contrast, canine breed classification belongs to the specialized and challenging domain of **Fine-Grained Visual Categorization (FGVC)**. Canines belong to the same biological species (*Canis lupus familiaris*), yet selective breeding practiced by humans over hundreds of years has produced more than 300 globally recognized domestic breeds. These breeds display remarkable morphological diversity: they range from miniature toy lapdogs like the Chihuahua (weighing under 2 kg) to giant draft and guard dogs like the Saint Bernard and Mastiff (weighing over 80 kg).

Developing an automated system capable of recognizing 120 distinct breeds directly from user photographs requires a neural network to look beyond coarse silhouettes and learn subtle, discriminative anatomical markers—such as the curl of a tail, muzzle-to-skull proportions, ear posture, coat texture, and facial pigmentation patterns.

### 1.2 Problem Statement
Accurately determining a dog's breed from an unconstrained digital photograph is notoriously difficult, even for experienced canine professionals, veterinarians, and animal shelter intake officers. The primary challenges include:

1. **Low Inter-Class Variance:** Biologically related breeds often look almost identical to the human eye. For example, a Whippet and an Italian Greyhound share an identical aerodynamic sighthound posture and sleek short coat, differing primarily in physical scale that cannot be measured from a 2D photograph lacking reference objects. Similarly, a Lhasa Apso and a Shih-Tzu both feature long, flowing facial fur that completely conceals underlying facial bone structure.
2. **High Intra-Class Variance:** Canines of the same recognized purebred breed display substantial variations in fur color morphs, coat trimming styles, age, facial expressions, and body weight.
3. **Unconstrained Photographic Conditions:** Real-world photographs submitted by users often feature poor illumination, cluttered domestic or outdoor backgrounds, partial occlusions by humans or furniture, and non-standard camera angles.
4. **The "Non-Dog" False Prediction Problem:** A significant flaw in existing classification systems is their closed-world assumption: if a user uploads a photograph of a horse, a cat, or a car, a single-stage 120-class classifier will forcefully output one of the 120 dog breeds with arbitrary confidence.

An automated, reliable, and user-friendly system is required that can first verify whether a photograph contains a dog, and then accurately identify the breed with ranked probability scores and detailed breed profiles.

### 1.3 Motivation
The motivation behind this project is driven by both practical real-world utility and academic learning:

- **Veterinary Medicine and Animal Shelters:** Animal welfare organizations and veterinary clinics frequently need to determine a dog's breed to anticipate hereditary health vulnerabilities (such as gastric torsion in deep-chested breeds, hip dysplasia in German Shepherds, or respiratory distress in brachycephalic dogs like French Bulldogs).
- **Lost and Found Animal Recovery:** In municipal animal shelters, correctly identifying a lost pet's breed accelerates matching with owner lost-pet reports and adoption records.
- **Academic Exploration of Transfer Learning:** As B.Tech Data Science students, fine-grained canine classification provided an ideal capstone project to investigate transfer learning, mitigate overfitting on small datasets, design multi-tier web applications, and implement relational database architectures.

### 1.4 Objectives
The primary objectives of this project are:
1. To develop a two-stage computer vision inference pipeline that first verifies canine presence and then performs fine-grained classification.
2. To classify canine images accurately across all 120 breeds represented in the benchmark Stanford Dogs dataset.
3. To leverage transfer learning with MobileNetV2 to achieve high diagnostic accuracy with lightweight parameter requirements suitable for rapid CPU-based web inference.
4. To display ranked Top-3 candidate breed predictions accompanied by visual confidence percentages.
5. To construct an interactive, responsive web portal using Python Flask and modern CSS allowing drag-and-drop image uploads.
6. To implement a secure MySQL relational database storing user accounts, individual prediction history, bookmarked favorites, and feedback.
7. To generate downloadable academic-grade PDF prediction reports using ReportLab.
8. To develop an interactive breed directory and side-by-side trait comparison tool across all 120 classes.
9. To provide transparent model performance evaluation pages with interactive Chart.js graphs and commonly confused breed analyses.
10. To validate the entire software application using an automated 18-point verification test suite.

### 1.5 Scope
The functional scope of this project is defined as follows:
- **Target Categories:** 120 recognized purebred dog breeds as defined by the Stanford Dogs benchmark.
- **Input Modality:** Single-subject canine photographs in JPG, JPEG, or PNG formats up to 10 MB in file size.
- **Core Processing:** 224 × 224 RGB image normalization and inference via TensorFlow / Keras MobileNetV2.
- **Web Interface:** Cross-browser responsive web application accessible on desktop, tablet, and mobile viewport widths.
- **System Boundaries:** The current system is designed for single-dog photographs and does not support multi-dog instance segmentation or mixed-breed genetic percentage estimation.

### 1.6 Proposed Approach
Our proposed approach addresses the limitations of conventional and command-line identification systems by coupling deep learning transfer learning with a multi-tier web architecture:

| Feature / Dimension | Conventional / Existing Systems | Our Proposed Implementation |
|---|---|---|
| **Identification Method** | Manual visual inspection using kennel books or veterinarian memory | Automated two-stage deep learning inference pipeline |
| **Speed and Accessibility** | Slow, subjective, requires domain expertise | Instant inference (<150 ms per image) accessible via web browser |
| **Non-Dog Input Handling** | Typically produces a false positive dog prediction | Stage 1 ImageNet filter validates canine presence and rejects non-dogs |
| **Model Architecture** | Heavy models (VGG16, ResNet50) requiring dedicated GPUs | Lightweight MobileNetV2 (~3.5M parameters) optimized for CPU deployment |
| **Output Information** | Single hard predicted label | Primary breed match, confidence percentage, and ranked Top-3 alternatives |
| **Data Persistence** | Stateless or desktop command-line scripts | Persistent MySQL database tracking individual user history and feedback |
| **Reporting** | Manual screenshotting or logging | One-click automated PDF prediction report generation via ReportLab |

---

# CHAPTER 2 – LITERATURE REVIEW

### 2.1 Research on Dog Breed Classification
Research in automated animal identification has transitioned from classical hand-crafted feature extractors (such as SIFT, HOG, and color histograms) to deep convolutional neural networks. Early approaches struggled with canine classification because coat patterns and lighting variations caused high intra-class variance that manual mathematical descriptors could not effectively capture.

### 2.2 CNN-Based Classification
Convolutional Neural Networks transformed the field by learning hierarchical feature representations directly from raw pixels. The initial convolutional layers learn low-level primitives like edges, lines, and color gradients; intermediate layers combine these into textures and ear or eye contours; and deeper layers synthesize full facial and body representations. However, training a deep CNN entirely from scratch on 120 dog breeds requires hundreds of thousands of labeled images, which are rarely available for specialized fine-grained domains.

### 2.3 Transfer Learning Approaches
Transfer learning addresses data scarcity by taking a network pre-trained on a massive visual corpus—most notably ImageNet, which contains 1.4 million images across 1,000 diverse categories—and transferring its learned feature representations to a target domain. Because ImageNet already includes 118 classes of domestic dogs and wild canids, its pre-trained convolutional filters already possess specialized knowledge of fur textures, canine ear structures, and facial geometry.

### 2.4 Comparison of Existing Research
We conducted a comprehensive literature survey examining twelve recent peer-reviewed research papers focusing on canine breed recognition, transfer learning, and out-of-distribution detection:

| Paper & Authors | Year | Model / Technique | Dataset Used | Reported Result | Key Limitation Observed |
|---|:---:|---|---|---|---|
| **Selvaraj et al.** | 2023 | ResNet50 Transfer Learning | Stanford Dogs (10,222 images) | 93.0% Accuracy | High compute cost; 120 breeds only |
| **Borwarnginn et al.** | 2021 | NASNet + Face Cropping | Columbia Dogs (8,111 images) | 89.92% Accuracy | Fails if facial crop fails |
| **Bokhari et al.** | 2022 | MobileNetV2 Feature Extractor | Stanford Dogs (120 breeds) | 85% (50 cl.) / 64% (120 cl.) | Steep drop on scaling to 120 classes |
| **Kumaravel et al.** | 2023 | DenseNet201 + Augmentation | Stanford + Kaggle (120k aug) | 87.34% Accuracy | Diminishing returns beyond saturation |
| **Banakar et al.** | 2023 | VGG-19 + Client/Server | Stanford Dogs (120 breeds) | High fine-tuned accuracy | Bulky model weights (~550 MB) |
| **Valarmathi et al.** | 2023 | Hybrid InceptionV3 + Xception | Stanford Dogs (10,222 images) | 92.4% Val Acc (98.4% Train) | Massive compute cost; slow inference |
| **Basha et al.** | 2021 | VGG16 in PyTorch | Canine breed image set | CNN representation verified | Vulnerable to lighting and pose shifts |
| **Hussain et al.** | 2025 | InceptionV3 + Background Rem. | Stanford Dogs (20,580 images) | 91.2% Accuracy | Segmentation clips anatomical edges |
| **Ghotra et al.** | 2023 | MobileNetV2 + Flask + Ngrok | Kaggle Dog Breeds (>10,222) | 99.89% Train Accuracy | High overfitting risk; no non-dog check |
| **Bankar et al.** | 2025 | CNN + Facial Keypoint Hub | Online set (8,350 images) | 90% Train / 70% Test | Severe 20% overfitting gap |
| **Zou et al.** | 2020 | WS-DAN, TBMSL-Net, PMG | Tsinghua Dogs (70,428 images) | WS-DAN: 86.4%, TBMSL: 83.7% | Complex multi-stage attention networks |
| **Perera & Patel** | 2019 | Deep Novelty Detection | Stanford Dogs + Multi-dataset | AUC: 0.825, Acc: 80.1% | Sensitive to activation thresholds |

### 2.5 Research Gap
Our comparative analysis revealed four critical shortcomings across the surveyed research:
1. **Absence of Out-of-Distribution Validation:** All surveyed web applications assume the user will only upload valid dog photographs. If a user uploads an image of a cat, horse, or car, these systems return a false canine breed prediction with high confidence.
2. **Computational Footprint vs. Speed Trade-Off:** Heavy ensemble architectures (Valarmathi et al.) and deep networks (Banakar et al.) achieve high accuracy but require dedicated GPU acceleration and take 1.5–3 seconds per image. Conversely, basic MobileNet implementations (Bokhari et al.) suffered a sharp accuracy collapse (64%) when scaled to 120 breeds without fine-tuning.
3. **Lack of Uncertainty Transparency:** Almost all implementations output a single hard class label. In fine-grained classification where breeds look nearly identical, concealing the model's alternative predictions hides important uncertainty from users.
4. **Lack of Full-Stack Data Management:** Prior works operated primarily as standalone machine learning scripts without user authentication, database persistence, or dynamic reporting.

### 2.6 Selection of MobileNetV2
To overcome these gaps, we selected **MobileNetV2** as our core neural backbone. MobileNetV2 is specifically designed for high-efficiency mobile and edge vision applications through its innovative **Inverted Residuals and Linear Bottlenecks**:
- Standard convolutional layers apply spatial filtering and channel transformation simultaneously, requiring huge parameter matrices.
- MobileNetV2 splits this operation into a $1 	imes 1$ expansion convolution (increasing channels by an expansion factor $t=6$), a $3 	imes 3$ depthwise convolution (applying spatial filtering independently on each channel), and a $1 	imes 1$ pointwise linear projection (compressing channels without non-linear ReLU distortion).
- This architecture requires only **~3.5 million parameters**, resulting in a trained model file of just **~14 MB**. On a standard multi-core CPU, MobileNetV2 executes a forward pass in **under 150 milliseconds**, making it ideal for interactive web serving without needing a costly dedicated GPU.

---

# CHAPTER 3 – DATASET AND IMAGE PREPARATION

### 3.1 Stanford Dogs Dataset
Our project utilizes the widely respected Stanford Dogs / Kaggle Dog Breed Identification dataset. Originally compiled by Aditya Khosla et al. at Stanford University from ImageNet, the dataset consists of **10,222 labeled photographs** covering **120 recognized purebred dog breeds**. The photographs were taken under natural, unconstrained real-world conditions, encompassing varied domestic living rooms, outdoor parks, diverse focal distances, and natural canine activities.

### 3.2 Breed Categories
The 120 canine categories represent a broad cross-section of global kennel classifications, including:
- **Toy Companions:** Chihuahua, Pomeranian, Maltese Dog, Shih-Tzu, Pug, Yorkshire Terrier.
- **Working & Herding Breeds:** German Shepherd, Collie, Border Collie, Rottweiler, Bernese Mountain Dog, Great Dane.
- **Sporting & Retrievers:** Golden Retriever, Labrador Retriever, Cocker Spaniel, Irish Setter.
- **Hounds & Sighthounds:** Beagle, Bloodhound, Basset Hound, Whippet, Afghan Hound, Saluki.
- **Terriers:** Scottish Terrier, Bull Terrier, Airedale Terrier, Kerry Blue Terrier.

### 3.3 Dataset Organization
The dataset is structured around an image directory containing 10,222 JPEG files named by unique 32-character hexadecimal identifiers, paired with `labels.csv` mapping each ID to its ground-truth breed. File headers were verified using JPEG magic bytes (`0xFFD8`), confirming 100% data integrity across all 10,222 files.

### 3.4 Training, Validation and Testing Split
To ensure unbiased academic evaluation, we partitioned the 10,222 images using a stratified 70% / 15% / 15% split governed by a fixed random seed (`seed = 42`):

| Partition Subset | Image Count | Percentage (%) | Functional Purpose |
|---|:---:|:---:|---|
| **Training Set** | 7,155 images | 70.0% | Model parameter optimization and backpropagation |
| **Validation Set** | 1,533 images | 15.0% | Hyperparameter tuning, early stopping, and checkpoint selection |
| **Testing Set (Held-Out)** | 1,534 images | 15.0% | Unbiased final evaluation and confusion matrix computation |
| **Total Corpus** | **10,222 images** | **100.0%** | Complete Stanford Dogs benchmark across 120 breeds |

The class distribution shows an average of 85.18 images per breed (median: 82.0). The dataset exhibits mild class imbalance: Scottish Deerhound has the highest representation with 126 images, while Briard and Eskimo Dog possess the minimum representation with 66 images each.

### 3.5 Image Resizing and Normalization
Raw photographs possess varying dimensions and aspect ratios. Before batch processing, images pass through an automated preprocessing pipeline:
1. **RGB Format Standardization:** Single-channel grayscale and 4-channel CMYK images are converted into standard 3-channel RGB.
2. **Bilinear Spatial Resizing:** Images are resized to uniform $224 	imes 224$ pixel dimensions.
3. **Pixel Value Normalization:** Pixel integers in $[0, 255]$ are converted to floating-point values in $[-1.0, +1.0]$ using MobileNetV2's scaling formula:
   $$x_{	ext{norm}} = rac{x}{127.5} - 1.0$$
4. **Batch Dimension Expansion:** Reshaped into a 4-dimensional tensor $(1, 224, 224, 3)$ suitable for neural inference.

### 3.6 Data Augmentation
Because 7,155 training images across 120 classes yields only ~60 images per breed in training, training without augmentation would lead to rapid overfitting. We applied real-time stochastic augmentation during training:
- **Random Horizontal Flipping (50% probability):** Teaches the model that canine orientation is invariant to breed identity.
- **Random Rotation ($\pm 15^\circ$):** Accommodates slight camera tilting.
- **Random Zoom ($\pm 10\%$):** Simulates variations in subject-to-camera distance.
- **Random Width and Height Shifts ($\pm 10\%$):** Simulates off-center framing.
- **Nearest Boundary Filling:** Prevents artificial black borders during rotation and shifting.

### 3.7 Dataset Challenges
Exploratory data analysis revealed three key visual challenges:
- **Subtle Facial Distinctions:** Closely related terriers (such as Australian Terrier vs. Silky Terrier) differ primarily in fur texture and ear fringe rather than skull morphology.
- **Background Clutter:** Canines photographed on green grass, snow, or carpets create misleading background correlations that the model must learn to ignore.
- **Posture Diversity:** Dogs lying down, curled up, jumping, or panting present vastly different visual silhouettes compared to standard standing kennel poses.

---

# CHAPTER 4 – PROPOSED METHODOLOGY

### 4.1 Overall System Architecture
We engineered the system as a decoupled, multi-tier web application consisting of four distinct tiers:
1. **Presentation Tier (Browser Client):** Responsive HTML5/CSS3 interface providing drag-and-drop image upload, local preview, animated prediction bars, trait comparison tools, and Chart.js analytics.
2. **Application Tier (Flask Web Framework):** Handles incoming HTTP requests, session management, user authentication, model inference orchestration, and dynamic PDF compilation.
3. **Deep Learning Tier (TensorFlow / Keras):** Houses the Two-Stage Inference Pipeline, executing Stage 1 canine presence verification and Stage 2 fine-grained breed prediction.
4. **Database Tier (MySQL Server):** Provides persistent storage for registered users, password hashes, individual prediction history, bookmarked favorites, and feedback.

### 4.2 Image Input and Validation
When a user uploads an image, the client-side JavaScript (`main.js`) verifies that the file format is valid (`.jpg`, `.jpeg`, `.png`) and the size does not exceed 10 MB. On the server side, `app.py` sanitizes the filename using Werkzeug's `secure_filename()` to prevent path traversal attacks and loads the image into memory using PIL.

### 4.3 Dog Presence Verification (Stage 1)
To prevent non-dog images from receiving false dog breed predictions, we implemented an upstream canine presence filter:
- An input tensor is passed through a MobileNetV2 model pre-trained on the full 1,000-class ImageNet dataset.
- ImageNet contains 118 classes corresponding to domestic dog breeds and wild canids (indices 151 through 268, plus 273 and 275).
- The pipeline computes the cumulative probability score across all 118 canine indices:
  $$P(	ext{dog}) = \sum_{k \in \mathcal{C}_{	ext{dog}}} \hat{y}_k^{	ext{ImageNet}}$$
- **Decision Logic:** If the Top-1 predicted ImageNet class is a canine or $P(	ext{dog}) \ge 0.20$, the image is confirmed as a dog and forwarded to Stage 2. If $P(	ext{dog}) < 0.20$, the pipeline halts immediately and returns an informative HTTP JSON warning (`No Dog Detected. Please upload a valid dog image.`) without executing the breed classifier.

### 4.4 MobileNetV2 Feature Extraction
Confirmed canine images are processed by our customized MobileNetV2 architecture. The network extracts rich spatial features through 155 layers of depthwise separable convolutions and inverted residual bottlenecks, outputting a high-level feature map of shape $(7, 7, 1280)$.

### 4.5 Transfer Learning and Fine-Tuning
Model training was conducted systematically in two sequential phases:

#### Phase 1: Feature Extraction (Frozen Base)
- All 155 layers of the pre-trained MobileNetV2 base were frozen (`trainable = False`).
- A newly initialized classification head (GlobalAveragePooling2D, Dropout 0.3, Dense 120 Softmax) was trained for 15 epochs using the Adam optimizer with an initial learning rate $\eta = 1 	imes 10^{-3}$.
- Categorical cross-entropy loss was minimized:
  $$\mathcal{L} = -\sum_{k=1}^{120} y_k \log(\hat{y}_k)$$
- This established stable classification weights without disturbing the pre-trained ImageNet feature filters.

#### Phase 2: Deep Fine-Tuning (Top 30 Layers Unfrozen)
- The base model was unfrozen, and the top 30 convolutional layers were set to trainable.
- Training continued for 10 epochs using Adam with a substantially reduced learning rate $\eta = 1 	imes 10^{-5}$ to avoid disrupting pre-trained weights while adapting high-level filters to canine facial and coat textures.
- Callbacks included `EarlyStopping` (patience=5), `ModelCheckpoint` saving `best_model.keras`, and `ReduceLROnPlateau` (factor=0.5, patience=3).

### 4.6 Breed Classification Head
Above the 155-layer MobileNetV2 base, we appended:
1. **GlobalAveragePooling2D:** Reduces the spatial dimensions from $7 	imes 7 	imes 1280$ to a 1,280-dimensional feature vector, replacing heavy fully connected layers and preventing overfitting.
2. **Dropout (0.3):** Randomly deactivates 30% of neurons during training passes to force the network to learn robust, distributed representations.
3. **Dense (120, Softmax):** Produces normalized probabilities summing to 1.0 across all 120 dog breeds:
   $$\hat{y}_i = rac{e^{z_i}}{\sum_{j=1}^{120} e^{z_j}}$$

### 4.7 Prediction Confidence and Top-3 Results
Rather than returning only a single class label, our system extracts the top 3 highest probabilities:
- The top-1 class is identified as the primary breed match.
- The 2nd and 3rd highest probabilities are extracted as candidate alternatives.
- Displaying Top-3 predictions provides full transparency to users, especially when the photograph depicts a mixed breed or a breed with visual similarity to another class.

### 4.8 Complete Prediction Workflow
The end-to-end inference algorithm is formalized below:

```
Algorithm 1: Two-Stage Canine Identification and Logging
Input : Uploaded image file F, User session S
Output: JSON response containing prediction details or rejection notice

1. IF F is empty OR extension(F) NOT IN {jpg, jpeg, png} THEN
2.     RETURN Error('Invalid file format')
3. END IF
4. filename <- secure_filename(F.name)
5. save_path <- Save(F, UPLOAD_FOLDER, filename)
6. img <- Resize(ConvertToRGB(LoadImage(save_path)), (224, 224))
7. tensor <- ExpandDims(MobileNetV2_Preprocess(img), axis=0)

// --- STAGE 1: Canine Presence Detection ---
8. imagenet_preds <- DogDetectorModel.predict(tensor)
9. top1_idx <- argmax(imagenet_preds)
10. dog_prob <- SUM(imagenet_preds[k] for k in IMAGENET_DOG_INDICES)
11. IF top1_idx NOT IN IMAGENET_DOG_INDICES AND dog_prob < 0.20 THEN
12.     RETURN Json(success=False, is_dog=False, message='No dog detected')
13. END IF

// --- STAGE 2: Fine-Grained Breed Classification ---
14. breed_probs <- BreedClassifierModel.predict(tensor)
15. top3_indices <- SortDescendingIndices(breed_probs)[0..2]
16. top3_results <- []
17. FOR EACH idx IN top3_indices DO
18.     top3_results.append({'breed': FormatBreedName(class_names[idx]),
                             'confidence': Round(breed_probs[idx] * 100, 2)})
19. END FOR
20. primary_match <- top3_results[0]

// --- STAGE 3: Database Persistence ---
21. user_id <- S.get('user_id')
22. prediction_id <- InsertPredictionRecord(user_id, filename, primary_match.breed,
                                            primary_match.confidence, top3_results)
23. RETURN Json(success=True, top_breed=primary_match.breed,
                confidence=primary_match.confidence, top3=top3_results,
                prediction_id=prediction_id)
```

---

# CHAPTER 5 – MODEL DEVELOPMENT AND WEB APPLICATION

### 5.1 Development Environment
The software was developed and validated under the following configuration:
- **Operating System:** Microsoft Windows 11 (64-bit)
- **Deep Learning Framework:** TensorFlow 2.21.0 / Keras
- **Programming Language:** Python 3.13 / 3.11
- **Web Framework:** Flask 3.0.0
- **Database Engine:** MySQL Server 8.0 with `mysql-connector-python`
- **PDF Generation Engine:** ReportLab 5.1.0
- **Frontend Tools:** HTML5, CSS3, JavaScript (ES6+), Chart.js 4.4.0

### 5.2 Model Training
Training was executed with the following finalized hyperparameter setup:

| Hyperparameter / Parameter | Phase 1: Feature Extraction | Phase 2: Fine-Tuning |
|---|---|---|
| **Base Model Layers** | 155 layers (Frozen) | Top 30 layers Unfrozen (125 Frozen) |
| **Trainable Parameters** | 153,720 parameters | 1,212,504 parameters |
| **Non-Trainable Parameters** | 2,257,984 parameters | 1,199,200 parameters |
| **Batch Size** | 32 | 32 |
| **Optimizer** | Adam ($eta_1=0.9, eta_2=0.999$) | Adam ($eta_1=0.9, eta_2=0.999$) |
| **Initial Learning Rate** | $1 	imes 10^{-3}$ | $1 	imes 10^{-5}$ |
| **Loss Function** | Categorical Cross-Entropy | Categorical Cross-Entropy |
| **Epochs Executed** | 10 epochs | 5 epochs (EarlyStopping trigger) |
| **Regularization** | Dropout (30%) + Data Augmentation | Dropout (30%) + Data Augmentation |

### 5.3 Model Integration
In `app.py`, the trained model `model/best_model.keras` is loaded once during server initialization using `tf.keras.models.load_model()`. The model instance is cached in memory, eliminating per-request loading latency and enabling immediate inference for concurrent user requests.

### 5.4 Flask Application Architecture
The backend application (`app.py`) follows modular WSGI design principles:
- `/` (`home`): Renders the main landing page with system features and quick navigation.
- `/identify` (`identify`): Interactive prediction portal with drag-and-drop upload zone and preview.
- `/predict` (`predict`, POST): Core API endpoint that accepts multipart image uploads, runs the two-stage inference pipeline, persists prediction metadata to MySQL, and returns structured JSON responses.
- `/breeds` (`breed_info`): Comprehensive 120-breed directory with live search, size filters, and comparison tabs.
- `/api/breeds` (`api_breeds`): REST API returning complete breed metadata from `database/breeds_data.json`.
- `/performance` (`performance`): Interactive evaluation dashboard displaying accuracy curves, loss curves, confusion tables, and Chart.js graphs.
- `/history` (`history`): Authenticated user prediction history displaying thumbnails, dates, confidence scores, and Top-3 modals.
- `/download_report` and `/download_report/<id>`: Compiles and streams personalized PDF prediction certificates.
- `/favorites` & `/api/favorites/toggle`: Manages bookmarked user breeds.
- `/feedback`: Collects user star ratings and written reviews.
- `/signup`, `/login`, `/logout`: Authentication routes.
- `/admin` & `/admin/grant`: Administrative dashboard displaying real-time database aggregates and user role management.

### 5.5 Image Upload and Prediction
The front-end interface provides a clean, responsive drag-and-drop drop zone. Once an image is selected, client-side JavaScript generates an immediate local preview with dimensions. Clicking **Predict Breed** triggers an asynchronous `fetch()` POST request. If Stage 1 detects a non-dog, a warning card is shown; if verified as a dog, the primary breed match, confidence percentage, and animated Top-3 probability bars appear smoothly.

### 5.6 User Authentication
User security is implemented using Werkzeug's cryptographic PBKDF2/SHA-256 password hashing. Passwords are never stored in plaintext. Secure session cookies track user identity across requests. Two custom Python decorators enforce route protection:
- `@login_required`: Redirects unauthenticated users to `/login`.
- `@admin_required`: Restricts administrative routes to users with `is_admin = 1`, returning HTTP 403 Forbidden to regular users.

### 5.7 Breed Information and Trait Comparison
To provide educational value beyond raw predictions, we curated a comprehensive JSON database (`database/breeds_data.json`) covering all 120 breeds. Each breed entry includes origin, size, typical lifespan, temperament tags, and physical descriptions. Users can select any two breeds for side-by-side comparison across height, weight, activity level, and care requirements.

### 5.8 Prediction History
Every successful prediction is recorded in MySQL. Authenticated users can visit `/history` to review their previous uploads, examine past confidence scores, and re-download prediction reports. Guests can also view recent session predictions.

### 5.9 Database Design
The relational database `dog_breed_db` maintains four normalized tables:

| Table Name | Primary Key | Foreign Keys | Key Attributes Stored |
|---|---|---|---|
| **`users`** | `user_id` (INT) | None | `username`, `email`, `password_hash`, `is_admin`, `created_at` |
| **`prediction_history`** | `prediction_id` (INT) | `user_id` $ightarrow$ `users(user_id)` | `image_path`, `predicted_breed`, `confidence`, `top3_results` (JSON), `model_version`, `created_at` |
| **`favorite_breeds`** | `favorite_id` (INT) | `user_id` $ightarrow$ `users(user_id)` | `breed_name`, `created_at` (Unique compound: `user_id, breed_name`) |
| **`feedback`** | `feedback_id` (INT) | `user_id` $ightarrow$ `users(user_id)` | `rating` (1–5), `message` (TEXT), `created_at` |

### 5.10 Other Implemented Features
- **ReportLab PDF Report Generation:** Produces a standardized, academic prediction report containing the project title, uploaded photograph, primary match, confidence score, Top-3 candidate breakdown, model version, timestamp, and a scientific machine learning disclaimer.
- **Star Rating Feedback System:** Allows users to submit 1-to-5 star ratings and comments stored directly in MySQL.
- **Admin Analytics Dashboard:** Calculates live SQL metrics (total users, total predictions, average confidence, total feedback) and visualizes the top 10 most frequently identified breeds using a Chart.js horizontal bar chart.

---

# CHAPTER 6 – RESULTS AND DISCUSSION

### 6.1 Training and Validation Performance
Training proceeded smoothly across 15 epochs without gradient instability. In Phase 1 (frozen base), the newly attached classification head learned decision boundaries rapidly:
- **Epoch 1:** Training Accuracy = 31.2%, Validation Accuracy = 48.5%, Validation Loss = 2.124
- **Epoch 5:** Training Accuracy = 72.1%, Validation Accuracy = 73.6%, Validation Loss = 0.985
- **Epoch 10:** Training Accuracy = 86.4%, Validation Accuracy = 79.8%, Validation Loss = 0.742
- **Epoch 15 (Fine-Tuning):** Unfreezing the top 30 layers increased training accuracy to **92.3%**, validation accuracy to **82.4%**, and lowered validation loss to **0.661**.

### 6.2 Accuracy and Loss
The smooth decrease in validation loss across both phases confirmed that our learning rate reduction strategy ($\eta = 1 	imes 10^{-3} ightarrow 1 	imes 10^{-5}$) and 30% dropout regularization successfully prevented severe memorization on the 7,155 training images.

### 6.3 Top-1 and Top-5 Accuracy
The fine-tuned model was evaluated on the **1,534 held-out test images** that were never seen during training or validation:

| Evaluation Metric | Measured Value | Operational Interpretation |
|---|:---:|---|
| **Top-1 Test Accuracy** | **77.64%** | Exact ground-truth breed match on held-out test images |
| **Top-5 Test Accuracy** | **96.87%** | Correct breed present within model's top 5 candidates |
| **Test Categorical Cross-Entropy Loss** | **0.7036** | Cross-entropy loss on unaugmented test images |
| **Macro Average Precision** | **78.58%** | Unweighted mean precision across all 120 categories |
| **Macro Average Recall** | **76.98%** | Unweighted mean recall across all 120 categories |
| **Macro Average F1-Score** | **76.91%** | Harmonic mean of macro precision and recall |
| **Weighted Average Precision** | **78.75%** | Support-weighted precision reflecting class sample sizes |
| **Weighted Average Recall** | **77.64%** | Support-weighted recall matching overall accuracy |
| **Weighted Average F1-Score** | **77.35%** | Support-weighted harmonic mean across all test samples |

The **Top-5 accuracy of 96.87%** is especially meaningful for practical canine identification: in almost 97 out of 100 cases, the correct breed is present among the top 5 candidates ranked by the model.

### 6.4 Precision, Recall and F1-Score
Examining individual breed performance showed that the network achieved strong discriminative power across the majority of breeds:
- **Top-Performing Breeds (100% Precision, Recall, and F1-Score):** African Hunting Dog (unique tri-color patchwork coat), Keeshond (distinctive silver-black ruff and eye spectacles), Papillon (prominent butterfly ears), and Bloodhound (heavy jowls and facial skin folds).
- **Challenging Breeds:** Italian Greyhound (F1 = 54.1%, confused with Whippet), Kuvasz (F1 = 53.3%, confused with Great Pyrenees), and Cardigan Welsh Corgi (F1 = 52.6%, confused with Pembroke Welsh Corgi).

### 6.5 Prediction Examples
When evaluating real-world test images:
- An input photograph of a Labrador Retriever (`dog.jpg`) passed Stage 1 with a canine probability of 92.4% and received a primary prediction of `Labrador Retriever` with **69.34% confidence** (#2: Golden Retriever at 9.37%, #3: Chesapeake Bay Retriever at 8.08%).
- A Siberian Husky photograph (`doog1.jpg`) passed Stage 1 with 98.7% canine probability and was correctly classified as `Siberian Husky` (#2: Eskimo Dog, #3: Alaskan Malamute).

### 6.6 Dog and Non-Dog Image Testing
Stage 1 canine presence detection was validated against both positive dog images and negative non-canine samples:
- **Positive Canine Images:** Produced canine probabilities exceeding 88%, correctly continuing to Stage 2 breed prediction.
- **Negative Control Images (e.g., horse photograph `Black-Horse-Names-with-Meanings.jpeg`, vehicles, landscapes):** The top predicted ImageNet class was non-canine (`sorrel`, `Arabian horse`), with total canine probability below 0.02. The system halted cleanly, returning the expected `No Dog Detected` alert.

### 6.7 Commonly Confused Breeds
Analysis of the test confusion matrix revealed 12 prominent pairs of confused dog breeds. In all 12 cases, the confusion is biologically justified by identical coat textures, ancestral lineages, or anatomical proportions:

| No. | Actual Breed | Predicted Breed | Confused Count | Visual Similarity Reason |
|:---:|---|---|:---:|---|
| 1 | **Whippet** | Italian Greyhound | 7 images | Identical slender sighthound posture and sleek coat |
| 2 | **Lhasa Apso** | Shih-Tzu | 6 images | Closely related Tibetan companion dogs with long facial fur |
| 3 | **Eskimo Dog** | Siberian Husky | 5 images | Arctic spitz breeds with erect ears, double coats, curled tails |
| 4 | **Australian Terrier** | Silky Terrier | 4 images | Related terrier types sharing wiry/silky coats and silhouettes |
| 5 | **Kuvasz** | Great Pyrenees | 4 images | Large flock-guarding breeds with solid white double coats |
| 6 | **Maltese Dog** | West Highland White Terrier | 4 images | Similar fine-grained facial features, fur texture, and white color |
| 7 | **Samoyed** | Great Pyrenees | 4 images | Large breeds sharing solid white, fluffy double coats |
| 8 | **Staffordshire Bull Terrier** | American Staffordshire Terrier | 4 images | Closely related bully breeds sharing blocky heads and muscular frames |
| 9 | **Cardigan Welsh Corgi** | Pembroke Welsh Corgi | 3 images | Both Welsh Corgi breeds, differing primarily in tail length |
| 10 | **Collie** | Shetland Sheepdog | 3 images | Herding breeds sharing identical facial markings and long ruffs |
| 11 | **Irish Wolfhound** | Scottish Deerhound | 3 images | Similar rough-coated wiry body structure and sighthound build |
| 12 | **Lakeland Terrier** | Soft-Coated Wheaten Terrier | 3 images | Similar tan/wheaten coat colors and bearded facial profiles |

### 6.8 Application Testing
To verify that all subsystems operate reliably without runtime crashes or database errors, we implemented an automated test suite ([`run_complete_tests.py`](file:///c:/Users/gouth/Downloads/DOG%20BREED%20IDENTIFICATION/run_complete_tests.py)) comprising 18 test cases. All 18 tests passed with a **100% success rate**:

| Test ID | Subsystem | Expected Behavior | Actual Measured Outcome | Status |
|:---:|---|---|---|:---:|
| **TC-01** | Flask Startup | Initializes cleanly with secret key | App initialized; secret key verified | **PASS** |
| **TC-02** | Homepage Navigation | HTTP 200 on `/`; renders navbar links | Status 200; Navigation links present | **PASS** |
| **TC-03** | Image Upload | Multipart POST saves image | Status 200; Saved to `uploads/` | **PASS** |
| **TC-04** | Invalid Image Handling | Rejects bad format & corrupted files | Proper error messages returned | **PASS** |
| **TC-05** | Canine Validation | Blocks non-dogs; accepts dogs | Horse rejected; Dog accepted | **PASS** |
| **TC-06** | Model Loading | MobileNetV2 loaded $(224, 224, 3)$ | Input $(224, 224, 3)$; 120 classes | **PASS** |
| **TC-07** | Breed Prediction | Returns valid breed and confidence | Predicted Labrador (69.34%) | **PASS** |
| **TC-08** | Top-3 Ranked Scores | Exactly 3 breeds sorted descending | Scores: #1 69.3%, #2 9.4%, #3 8.1% | **PASS** |
| **TC-09** | MySQL Connection | Connects to `dog_breed_db`; 4 tables | Connected; all 4 tables verified | **PASS** |
| **TC-10** | Signup & Login | Creates user, hashes password | Signup OK; session created; logout OK | **PASS** |
| **TC-11** | Prediction History | Restricts unauthenticated users | Guest $ightarrow$ 302; Authenticated $ightarrow$ 200 | **PASS** |
| **TC-12** | Favorite Breeds | AJAX toggle bookmarks breed | Bookmark added & removed correctly | **PASS** |
| **TC-13** | Breed Directory | `/breeds` renders 120 breeds | Status 200; 120 breeds loaded | **PASS** |
| **TC-14** | Breed Comparison | Verifies comparison selectors | Side-by-side attributes verified | **PASS** |
| **TC-15** | Performance Charts | Returns accuracy and confusion data | Status 200; 77.64% test accuracy | **PASS** |
| **TC-16** | PDF Report Download | Streams valid PDF binary | Status 200; Mime: `application/pdf` | **PASS** |
| **TC-17** | Admin Access Control | Enforces RBAC on `/admin` | Guest $ightarrow$ 302; User $ightarrow$ 403; Admin $ightarrow$ 200 | **PASS** |
| **TC-18** | Responsive Design | Viewport meta tag & media queries | Breakpoints (480, 600, 768, 900px) | **PASS** |

### 6.9 Observations
- **Inference Latency:** On standard consumer CPU hardware, a single prediction forward pass (preprocessing, Stage 1 check, Stage 2 prediction, and database insertion) takes **120 to 160 milliseconds**, well within the 500 ms benchmark for interactive web responsiveness.
- **Memory Footprint:** MobileNetV2 requires only **~14 MB** of disk storage and minimal RAM, enabling rapid application startup and stable hosting on lightweight server environments.

---

# CHAPTER 7 – CONCLUSION AND FUTURE ENHANCEMENTS

### 7.1 Project Summary
In this B.Tech capstone project, we designed, developed, and deployed an end-to-end canine breed identification platform using transfer learning with MobileNetV2 and full-stack web engineering. Our work demonstrates that lightweight convolutional networks can achieve high diagnostic performance in complex fine-grained visual classification tasks while maintaining low computational latency.

Key accomplishments of the project include:
1. **Architected a Two-Stage Pipeline:** Introduced an upstream ImageNet canine presence filter that prevents non-dog uploads from receiving false dog breed predictions.
2. **Attained Strong Academic Accuracy:** Achieved **77.64% Top-1 test accuracy** and **96.87% Top-5 test accuracy** across 120 breeds on 1,534 held-out evaluation images.
3. **Engineered a Full-Stack Web Platform:** Implemented a secure Flask application with MySQL database persistence, PBKDF2 password hashing, role-based access control, and dynamic PDF prediction report compilation.
4. **Delivered Rich User Features:** Integrated a 120-breed interactive directory, side-by-side trait comparison, individual prediction history tracking, user feedback, and an administrative dashboard.
5. **Validated Reliability:** Executed an automated 18-point verification testing suite with a 100% pass rate.

### 7.2 Learning Outcomes
Through the development of this project, our team acquired valuable engineering experience:
- Practical understanding of deep transfer learning, inverted residual bottlenecks, and the delicate balance required during two-phase fine-tuning.
- Experience with dataset splitting strategies, data augmentation, and handling fine-grained visual classification challenges.
- Full-stack web engineering skills connecting deep learning models to Flask web applications and MySQL databases.
- Automated testing practices to ensure software stability across database transactions, session cookies, and API endpoints.

### 7.3 Limitations
The system exhibits three practical limitations:
1. **Resolution Downscaling:** Resizing images to $224 	imes 224$ pixels inevitably discards micro-level textures (such as fine fur whisker curls) that could help differentiate closely related terrier varieties.
2. **Single-Subject Assumption:** The model assumes that a single primary canine is centered in the photograph. If multiple dogs appear together, their feature maps blend, leading to lower prediction confidence.
3. **Absence of Physical Scale Reference:** In a 2D photograph lacking reference objects, an Italian Greyhound (weighing 4 kg) looks identical in proportions to a Whippet (weighing 13 kg). Without physical scale measurements, 2D CNNs cannot exploit size differences.

### 7.4 Future Improvements
Several promising directions exist for future enhancement:
1. **Upstream Object Detection & Bounding Box Localization:** Incorporating a lightweight YOLOv8 detector to crop the canine body from cluttered backgrounds before classification.
2. **Mobile Edge Deployment:** Quantizing the trained MobileNetV2 model to TensorFlow Lite (TFLite) or ONNX format for on-device inference on Android and iOS devices without requiring internet connectivity.
3. **Vision Transformers (ViT) & Attention Mechanisms:** Exploring part-attention networks to explicitly focus convolutional attention on diagnostic anatomical regions (ears, snout, tail posture).
4. **Mixed-Breed Percentage Estimation:** Expanding the classification head to estimate breed composition percentages for mixed-breed dogs.

---

## REFERENCES

1. S. Selvaraj, R. Thangarajan, S. Anbukkarasi, and S. Yuvan Prasad, "ResNet50 Architecture Based Dog Breed Identification Using Deep Learning," in *Proc. Int. Conf. on Computational Intelligence and Knowledge Economy*, 2023.
2. P. Borwarnginn, W. Kusakunniran, S. Karnjanapreechakorn, and K. Thongkanchorn, "Knowing Your Dog Breed: Identifying a Dog Breed with Deep Learning," in *Proc. Int. Conf. on Information Technology*, 2021.
3. S. A. Bokhari, P. Mukherjee, A. S. Singh, S. Shaik, and J. K. Mathew, "Convolutional Neural Network Based Dog Breed Classification," in *Proc. Int. Conf. on Innovative Computing and Communication*, 2022.
4. T. Kumaravel, P. Natesan, V. E. Sathishkumar, S. S. N, S. G, and U. V, "Automatic Dog Breed Classification Using Deep Learning," in *Proc. Int. Conf. on Smart Systems and Inventive Technology*, 2023.
5. N. Banakar, Raghavendra B. U., S. G. S., T. K. Vani, and V. M. Vishnu, "Dog Breed Identification Using Deep Learning," *International Journal of Advanced Research in Computer Science and Software Engineering*, vol. 13, no. 5, 2023.
6. B. Valarmathi, N. S. Gupta, G. Prakash, R. H. Reddy, S. Saravanan, and P. Shanmugasundaram, "Hybrid Deep Learning Algorithms for Dog Breed Identification—A Comparative Analysis," *IEEE Access*, vol. 11, pp. 45120–45132, 2023.
7. S. R. Basha, I. Ganesh, G. R. Reddy, and A. Hans, "Dogs Breed Classification Using Deep Learning," in *Proc. Int. Conf. on Artificial Intelligence and Smart Systems*, 2021.
8. S. S. Hussain, K. S. R. Murthy, C. S. Rani, T. Nanuvala, C. R. Kumar, and G. Sathar, "Automated Dog Breed Recognition Using CNN-Based Transfer Learning," in *Proc. Int. Conf. on Advances in Computer Engineering & Communication Systems*, 2025.
9. A. S. Ghotra, H. Kour, A. Hasan, and A. Khan, "Dog Breed Identification," in *Proc. Int. Conf. on Data Science and Machine Learning*, 2023.
10. J. Bankar, A. Nalawade, S. Wali, A. Rane, and H. Matlani, "AI Based Dog Breed Prediction Model and Virtual Canine Hub," *International Journal of Computer Applications*, vol. 186, no. 14, 2025.
11. D.-N. Zou, S.-H. Zhang, T.-J. Mu, and M. Zhang, "A New Dataset of Dog Breed Images and a Benchmark for Fine-Grained Classification," *Computational Visual Media*, vol. 6, no. 4, pp. 477–487, 2020.
12. P. Perera and V. M. Patel, "Deep Transfer Learning for Multiple Class Novelty Detection," in *Proc. IEEE/CVF Conf. on Computer Vision and Pattern Recognition (CVPR)*, 2019, pp. 1154–1162.
13. A. Khosla, N. Jayadevaprakash, B. Yao, and L. Fei-Fei, "Novel Dataset for Fine-Grained Image Categorization: Stanford Dogs," in *Proc. CVPR Workshop on Fine-Grained Visual Categorization*, 2011.
14. M. Sandler, A. Howard, M. Zhu, A. Zhmoginov, and L.-C. Chen, "MobileNetV2: Inverted Residuals and Linear Bottlenecks," in *Proc. IEEE/CVF Conf. on Computer Vision and Pattern Recognition (CVPR)*, 2018, pp. 4510–4520.
15. M. Abadi et al., "TensorFlow: A System for Large-Scale Machine Learning," in *Proc. 12th USENIX Symp. on Operating Systems Design and Implementation (OSDI)*, 2016, pp. 265–283.
16. A. Grinberg, *Flask Web Development: Developing Web Applications with Python*, 2nd ed. Sebastopol, CA: O'Reilly Media, 2018.
17. ReportLab Europe Ltd., *ReportLab PDF Generation User Guide*, Version 5.1, London, UK, 2024.
18. Oracle Corporation, *MySQL 8.0 Reference Manual*, Redwood Shores, CA: Oracle, 2024.

---

## TEAM CONTRIBUTIONS

This project was developed collaboratively by four B.Tech Data Science students. While all members contributed to system design, review presentations, and testing, individual responsibilities were divided as follows:

### K Goutham Nayak – CS24B1081
**Backend Architecture, MySQL Database and PDF Reporting**
- Implemented Flask application routing and asynchronous REST APIs.
- Designed the MySQL relational database schema (`dog_breed_db`) across 4 tables.
- Developed password hashing using Werkzeug PBKDF2/SHA-256 and role-based decorators (`@login_required`, `@admin_required`).
- Built the automated ReportLab PDF prediction report generator.
- Configured individual prediction history and favorites management.

### K Adithya – CS24B1091
**Deep Learning Model Architecture and Fine-Tuning**
- Implemented MobileNetV2 transfer learning using TensorFlow / Keras.
- Configured the two-phase training strategy (Phase 1 frozen feature extraction; Phase 2 top 30 unfrozen fine-tuning).
- Applied learning rate scheduling, early stopping, and model checkpointing.
- Computed quantitative evaluation metrics (Top-1 77.64%, Top-5 96.87%, test loss 0.7036, macro/weighted F1).
- Generated training convergence curves and confusion matrix artifacts.

### R Mahesh Rathod – CS24B1071
**Two-Stage Canine Presence Detection and Validation**
- Formulated and implemented the Stage 1 ImageNet canine presence filter.
- Mapped 118 domestic and wild canine ImageNet class indices.
- Calibrated the cumulative canine probability threshold ($P(	ext{dog}) \ge 0.20$).
- Validated the system against negative non-dog images (horses, vehicles, landscapes).
- Conducted error analysis on the 12 most frequently confused dog breed pairs.

### G Vishnu Vardhan – CS24B1028
**Frontend UI/UX, Breed Directory and Trait Comparison**
- Designed the responsive HTML5/CSS3 cream-and-brown web interface.
- Developed the drag-and-drop file upload logic and image preview in JavaScript.
- Built the 120-breed interactive directory with search and size filtering.
- Implemented the side-by-side breed trait comparison tool.
- Integrated Chart.js for the administrative dashboard and model performance charts.

### Shared Group Responsibilities
- Extracted and evaluated methodology and limitations across 12 research papers in the literature survey.
- Partitioned the 10,222 images into stratified 70% / 15% / 15% train, validation, and test sets.
- Executed and validated all 18 test cases in the automated application test suite (`run_complete_tests.py`).
- Prepared and proofread the comprehensive B.Tech project report.

— END OF REPORT —
