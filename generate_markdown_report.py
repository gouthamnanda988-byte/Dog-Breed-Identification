"""
generate_markdown_report.py
===========================
Generates the comprehensive Dog_Breed_Identification_Project_Report.md
"""

import os

def create_markdown_report(output_path):
    report_text = """# DOG BREED IDENTIFICATION USING DEEP LEARNING AND TRANSFER LEARNING

**A B.Tech Final Year Project Report**

---

### Project Team Members:
1. **K Goutham Nayak** – CS24B1081
2. **K Adithya** – CS24B1091
3. **R Mahesh Rathod** – CS24B1071
4. **G Vishnu Vardhan** – CS24B1028

**Academic Department:** [Department of Computer Science and Engineering / Data Science]  
**Institution:** [Institution / College Name, Affiliated to University Name]  
**Under the Guidance of:** [Faculty Guide Name, Designation]  
**Academic Year:** [2025 – 2026]

---

## TABLE OF CONTENTS
1. [Abstract](#abstract)
2. [Chapter 1 – Introduction](#chapter-1--introduction)
   - 1.1 [Background](#11-background)
   - 1.2 [Problem Statement](#12-problem-statement)
   - 1.3 [Motivation](#13-motivation)
   - 1.4 [Project Objectives](#14-project-objectives)
   - 1.5 [Scope of the Project](#15-scope-of-the-project)
   - 1.6 [Existing System and Proposed System](#16-existing-system-and-proposed-system)
   - 1.7 [Organization of the Report](#17-organization-of-the-report)
3. [Chapter 2 – Literature Survey](#chapter-2--literature-survey)
   - 2.1 [Review of Related Research Papers](#21-review-of-related-research-papers)
   - 2.2 [Comparative Literature Analysis](#22-comparative-literature-analysis)
   - 2.3 [Research Gap Analysis](#23-research-gap-analysis)
   - 2.4 [How the Proposed Project Addresses the Gaps](#24-how-the-proposed-project-addresses-the-gaps)
4. [Chapter 3 – Dataset](#chapter-3--dataset)
   - 3.1 [Dataset Description and Origin](#31-dataset-description-and-origin)
   - 3.2 [Breed Categories and Class Hierarchy](#32-breed-categories-and-class-hierarchy)
   - 3.3 [Dataset Distribution and Partitioning](#33-dataset-distribution-and-partitioning)
   - 3.4 [Image Preprocessing Pipeline](#34-image-preprocessing-pipeline)
   - 3.5 [Data Augmentation Strategy](#35-data-augmentation-strategy)
   - 3.6 [Dataset Challenges and Observations](#36-dataset-challenges-and-observations)
5. [Chapter 4 – Methodology](#chapter-4--methodology)
   - 4.1 [Overall System Architecture](#41-overall-system-architecture)
   - 4.2 [Two-Stage Prediction Pipeline](#42-two-stage-prediction-pipeline)
   - 4.3 [Convolutional Neural Networks and Transfer Learning](#43-convolutional-neural-networks-and-transfer-learning)
   - 4.4 [Image Preprocessing and Normalization](#44-image-preprocessing-and-normalization)
   - 4.5 [Two-Phase Model Training Procedure](#45-two-phase-model-training-procedure)
   - 4.6 [Flask Web Application Architecture](#46-flask-web-application-architecture)
   - 4.7 [Relational Database Design and Schema](#47-relational-database-design-and-schema)
   - 4.8 [User Authentication and Access Control](#48-user-authentication-and-access-control)
   - 4.9 [Additional Features and Utilities](#49-additional-features-and-utilities)
   - 4.10 [Technologies and Frameworks Used](#410-technologies-and-frameworks-used)
   - 4.11 [System Workflow and User Journey](#411-system-workflow-and-user-journey)
   - 4.12 [Algorithmic Pseudocode](#412-algorithmic-pseudocode)
6. [Chapter 5 – Experimental Results and Discussion](#chapter-5--experimental-results-and-discussion)
   - 5.1 [Experimental Environment](#51-experimental-environment)
   - 5.2 [Training Convergence Results](#52-training-convergence-results)
   - 5.3 [Model Evaluation Metrics](#53-model-evaluation-metrics)
   - 5.4 [Prediction Results and Confidence Breakdown](#54-prediction-results-and-confidence-breakdown)
   - 5.5 [Dog and Non-Dog Presence Verification](#55-dog-and-non-dog-presence-verification)
   - 5.6 [Commonly Confused Breeds Analysis](#56-commonly-confused-breeds-analysis)
   - 5.7 [Automated Application Test Suite](#57-automated-application-test-suite)
   - 5.8 [Performance Analysis and System Latency](#58-performance-analysis-and-system-latency)
   - 5.9 [Practical Limitations](#59-practical-limitations)
7. [Chapter 6 – Conclusion and Future Work](#chapter-6--conclusion-and-future-work)
   - 6.1 [Conclusion](#61-conclusion)
   - 6.2 [Future Work Roadmap](#62-future-work-roadmap)
8. [References](#references)
9. [Team Contributions](#team-contributions)

---

## ABSTRACT

Accurately classifying domestic canine breeds from digital photographs represents one of the most prominent fine-grained visual classification challenges in modern computer vision. Unlike generic object recognition where classes differ fundamentally in shape and silhouette (such as vehicles versus animals), canine identification must contend with two difficult phenomena: high intra-class variance, where dogs of the same breed exhibit significant variations in coat patterns, grooming styles, age, and postures, and low inter-class variance, where biologically distinct breeds share nearly indistinguishable anatomical silhouettes and facial profiles (for instance, Whippets and Italian Greyhounds, or Lhasa Apsos and Shih-Tzus).

In this project, we designed, implemented, and thoroughly evaluated an end-to-end canine classification web platform powered by transfer learning with MobileNetV2 and backed by a full-stack relational database. Built upon the Stanford Dogs / Kaggle Dog Breed Identification benchmark comprising 10,222 labeled images partitioned into a stratified 70% training (7,155 images), 15% validation (1,533 images), and 15% testing (1,534 images) split across 120 purebred categories, our architecture employs an innovative **two-stage prediction pipeline**. In Stage 1, an ImageNet-pretrained MobileNetV2 classifier validates canine presence by monitoring 118 domestic and wild dog output indices, immediately rejecting non-dog uploads (such as horses, felines, or inanimate objects) with a friendly alert. In Stage 2, images confirmed as dogs are evaluated by our fine-tuned MobileNetV2 model equipped with Global Average Pooling, 30% dropout regularization, and a 120-unit Softmax classification layer.

Our model achieved an empirical **77.64% Top-1 test accuracy**, an exceptional **96.87% Top-5 test accuracy**, and a test loss of **0.7036** across the 1,534 held-out evaluation images. Beyond the neural network, we integrated a full-stack Flask web application providing drag-and-drop image prediction with Top-3 ranked candidate scores, a 120-breed interactive directory, side-by-side trait comparison, ReportLab automated PDF prediction report downloads, personal MySQL history tracking, and a role-based administrative analytics dashboard. This platform provides an accessible, robust, and educational solution for veterinary clinics, rescue shelters, and pet owners.

---

## CHAPTER 1 – INTRODUCTION

### 1.1 Background
Image classification is a foundational task in computer vision that seeks to assign an input image to one of several predefined categories based on visual characteristics. Over the past decade, Convolutional Neural Networks (CNNs) have revolutionized image classification by automatically discovering hierarchical feature representations directly from raw pixel arrays—moving from primitive edges and textures in initial convolutional layers to complex semantic parts and object contours in deeper layers.

Within the visual recognition domain, canine breed classification belongs to the specialized field of **Fine-Grained Visual Categorization (FGVC)**. Unlike coarse-grained classification (such as distinguishing a dog from a car or a tree), fine-grained recognition demands that a system discriminate between subtle sub-categories belonging to the exact same biological species (*Canis lupus familiaris*). Domestic dogs represent the most morphologically diverse terrestrial mammal on Earth, with hundreds of purebred varieties developed through centuries of selective breeding. Building an automated system that accurately distinguishes between 120 purebred categories holds significant academic and practical value.

### 1.2 Problem Statement
Manually identifying dog breeds from photographs is remarkably challenging and prone to error, even for experienced veterinarians, canine kennel judges, and animal shelter workers. The primary difficulties stem from:
1. **Low Inter-Class Variance:** Different breeds that share ancestral lineages or functional traits often possess nearly identical visual appearances. For example, a Whippet and an Italian Greyhound share identical slender sighthound posture and sleek short coats; a Siberian Husky and an Eskimo Dog share identical erect triangular ears and curled tails; a Lhasa Apso and a Shih-Tzu share long facial hair that obscures facial bone structures.
2. **High Intra-Class Variance:** Dogs of the same recognized breed can display substantial differences in coat coloration, fur texture, grooming cuts, body weight, ear posture, and lighting conditions.
3. **Background Clutter and Occlusions:** User-uploaded photographs frequently feature outdoor environments, household clutter, human handlers, or awkward camera angles that obscure key diagnostic breed features.
4. **Non-Dog False Predictions:** Conventional single-stage classifiers force any uploaded image into one of the 120 dog categories, producing misleading predictions when users upload non-dog subjects.

Therefore, an automated, reliable, and user-friendly system is required that can first verify whether a photograph contains a canine, and then accurately identify the breed with ranked probability scores and detailed breed profiles.

### 1.3 Motivation
The motivation for undertaking this capstone project is both academic and practical:
- **Veterinary and Clinical Utility:** Animal clinics, rescue shelters, and pet insurance agencies frequently require accurate breed determination to anticipate hereditary health vulnerabilities (e.g., hip dysplasia in German Shepherds, respiratory issues in brachycephalic breeds like Pugs).
- **Lost and Found Animal Recovery:** In municipal shelters, correctly identifying a lost dog's breed accelerates matching with owner lost-pet reports.
- **Academic Exploration of Transfer Learning:** As B.Tech Data Science students, fine-grained visual classification provided an ideal real-world problem to study transfer learning, deep convolutional architectures, overfitting mitigation, relational database integration, and web software engineering.

### 1.4 Project Objectives
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

### 1.5 Scope of the Project
- **Target Categories:** 120 recognized purebred dog breeds as defined by the Stanford Dogs benchmark.
- **Input Modality:** Single-subject canine photographs in JPG, JPEG, or PNG formats up to 10 MB in file size.
- **Core Processing:** 224 x 224 RGB image normalization and inference via TensorFlow / Keras MobileNetV2.
- **Web Interface:** Cross-browser responsive web application accessible on desktop, tablet, and mobile viewport widths.
- **System Boundaries:** The current system is designed for single-dog photographs and does not support multi-dog instance segmentation or mixed-breed genetic percentage estimation.

### 1.6 Existing System and Proposed System

| Feature / Dimension | Conventional / Existing Systems | Our Proposed Implementation |
|---|---|---|
| **Identification Method** | Manual visual inspection by kennel books or expert veterinarians | Automated two-stage deep learning inference pipeline |
| **Speed and Accessibility** | Slow, subjective, requires domain expertise | Instant inference (<150 ms per image) accessible via web browser |
| **Non-Dog Input Handling** | Typically produces a false positive dog prediction | Stage 1 ImageNet filter validates canine presence and rejects non-dogs |
| **Model Architecture** | Heavy models (VGG16, ResNet50) requiring dedicated GPUs | Lightweight MobileNetV2 (~3.5M parameters) optimized for CPU deployment |
| **Output Information** | Single hard predicted label | Primary breed match, confidence percentage, and ranked Top-3 alternatives |
| **Data Persistence** | Stateless or desktop command-line scripts | Persistent MySQL database tracking individual user history and feedback |
| **Reporting** | Manual screenshotting or logging | One-click automated PDF prediction report generation via ReportLab |
| **Breed Information** | Separate encyclopedias or external websites | Built-in 120-breed directory with side-by-side comparison tools |

### 1.7 Organization of the Report
The remainder of this report is organized as follows:
- **Chapter 2 (Literature Survey):** Reviews 12 relevant research papers, compares published methodologies, identifies research gaps, and highlights our contributions.
- **Chapter 3 (Dataset):** Details the Stanford Dogs dataset, class distribution, image preprocessing, and data augmentation techniques.
- **Chapter 4 (Methodology):** Outlines our system architecture, two-stage inference pipeline, transfer learning configuration, database design, and Flask application routes.
- **Chapter 5 (Experimental Results and Discussion):** Presents training convergence curves, test set metrics, confusion analyses, dog/non-dog verification, and the 18-point automated test suite.
- **Chapter 6 (Conclusion and Future Work):** Summarizes project achievements, discusses technical lessons learned, and outlines future enhancements.
- **References & Team Contributions:** Provides IEEE citations and team member project roles.

---

## CHAPTER 2 – LITERATURE SURVEY

### 2.1 Review of Related Research Papers

#### 1. Selvaraj et al. (2023) – ResNet50 Architecture Based Dog Breed Identification Using Deep Learning
- **Authors:** Selvaraj S, Thangarajan R, Anbukkarasi S, Yuvan Prasad S
- **Dataset:** Stanford Dogs Dataset (10,222 images across 120 breeds)
- **Objective:** To build an automated dog breed identification system using deep learning to accelerate visual inspection.
- **Methodology:** The authors implemented a Convolutional Neural Network utilizing the ResNet50 architecture featuring residual shortcut connections. They evaluated ResNet50 alongside NASNet, InceptionV3, MobileNetV2, MobileNet, DenseNet121, and AlexNet.
- **Key Findings:** ResNet50 yielded the highest classification accuracy among all evaluated standalone models, achieving approximately 93% accuracy in comparative evaluations.
- **Limitations:** The network required substantial computational memory and extensive training samples per class; performance on unrepresented breeds was not addressed.
- **Relevance:** Confirmed that deep residual transfer learning is highly effective for fine-grained canine feature representation.

#### 2. Borwarnginn et al. (2021) – Knowing Your Dog Breed: Identifying a Dog Breed with Deep Learning
- **Authors:** Punyanuch Borwarnginn, Worapan Kusakunniran, Sarattha Karnjanapreechakorn, Kittikhun Thongkanchorn
- **Dataset:** Columbia Dogs Dataset (8,351 images of 133 breeds; 8,111 utilized after preprocessing)
- **Objective:** To identify dog breeds utilizing facial regions and improve classification when sample counts per breed are limited.
- **Methodology:** Explored deep transfer learning across three pretrained architectures: MobileNetV2, InceptionV3, and NASNet. Canine facial bounding boxes were extracted and cropped prior to training, supplemented by image augmentation including rotation, translation, horizontal flipping, and Gaussian noise injection.
- **Key Findings:** Data augmentation markedly improved model generalization. NASNet achieved the top performance with 89.92% accuracy, demonstrating that transfer learning overcomes limited dataset sizes.
- **Limitations:** The system relied heavily on successful facial detection; failed crops led to severe misclassifications.
- **Relevance:** Demonstrated the critical importance of data augmentation and proved that lightweight backbones like MobileNetV2 remain competitive against heavier models.

#### 3. Bokhari et al. (2022) – Convolutional Neural Network Based Dog Breed Classification
- **Authors:** Syed Aamir Bokhari, Progyajyoti Mukherjee, Abhishek Samar Singh, Suhail Shaik, Prof. Jimsha K Mathew
- **Dataset:** Stanford Dogs Dataset (120 breeds; 10,222 training and 10,357 testing images)
- **Objective:** To classify dog breeds using CNN transfer learning while minimizing training resource consumption.
- **Methodology:** Utilized a pretrained MobileNetV2 backbone to extract deep convolutional features, dividing images into batches and training dense classification heads.
- **Key Findings:** The model attained nearly 85% accuracy when evaluated on a restricted subset of 50 common breeds, but dropped to approximately 64% when scaled across 120 less common breeds.
- **Limitations:** Background noise and natural clutter degraded classification; scaling to 120 breeds introduced significant inter-breed confusion.
- **Relevance:** Directly informed our decision to adopt MobileNetV2, while highlighting the necessity of fine-tuning deeper layers to maintain accuracy when expanding from 50 to 120 classes.

#### 4. Kumaravel et al. (2023) – Automatic Dog Breed Classification Using Deep Learning
- **Authors:** T Kumaravel, P Natesan, V E Sathishkumar, Sathiya Shri N, Swathy G, Uvetha V
- **Dataset:** Stanford Dogs and Kaggle repository expanded via augmentation to ~120,000 images (80% train, 10% val, 10% test)
- **Objective:** To benchmark multiple modern deep learning classifiers on an expanded canine image corpus.
- **Methodology:** Comparative evaluation of MobileNetV2, InceptionV3, Xception, and DenseNet201 resized to 224 x 224 x 3 using horizontal flipping, padding, cropping, and rotation.
- **Key Findings:** DenseNet201 yielded the highest accuracy at 87.34%, proving that dense feature reuse aids in discriminating subtle canine textures.
- **Limitations:** Diminishing returns were observed when increasing epochs beyond a saturation threshold; image quality variations remained problematic.
- **Relevance:** Validated our choice of 224 x 224 x 3 resolution and confirmed that data augmentation is vital to prevent overfitting on fine-grained datasets.

#### 5. Banakar et al. (2023) – Dog Breed Identification Using Deep Learning
- **Authors:** Nagaraj Banakar, Raghavendra BU, Sindhu GS, Vani TK, Dr. Vishnu VM
- **Dataset:** Stanford Dogs Dataset (120 breeds)
- **Objective:** To streamline breed identification for breeding research and veterinary documentation.
- **Methodology:** CNN transfer learning utilizing VGG-19 and Inception-ResNet V2 backbones with image normalization, connected to a mobile client and web server.
- **Key Findings:** VGG-19 demonstrated robust feature extraction capabilities when fine-tuned on canine images, achieving competitive accuracy.
- **Limitations:** Large memory footprint of VGG-19 (~550 MB weights) produced slow inference on edge and mobile devices.
- **Relevance:** Reinforced the need for efficient client-server decoupling and justified our choice of MobileNetV2 over heavy architectures like VGG-19 for web deployment.

#### 6. Valarmathi et al. (2023) – Hybrid Deep Learning Algorithms for Dog Breed Identification—A Comparative Analysis
- **Authors:** B. Valarmathi, N. Srinivasa Gupta, G. Prakash, R. Hemadri Reddy, S. Saravanan, P. Shanmugasundaram
- **Dataset:** Stanford Dogs Dataset (10,222 images across 120 breeds)
- **Objective:** To evaluate standalone versus hybrid ensemble architectures for fine-grained canine recognition.
- **Methodology:** Evaluated Xception, VGG19, NASNetMobile, EfficientNetV2M, and ResNet152V2, and formulated two hybrid models: (1) Inception-v3 + Xception, and (2) EfficientNetV2M + NASNetMobile + Inception + Xception.
- **Key Findings:** The hybrid Inception-v3 + Xception ensemble attained the highest validation accuracy of 92.4% (98.4% training accuracy). Standalone models achieved: Xception 91.9%, EfficientNetV2M 89.05%, ResNet152V2 87.38%, NASNetMobile 83.47%.
- **Limitations:** Substantial computational complexity, extended training times, and high GPU memory demands prevented real-time deployment on standard hardware.
- **Relevance:** Showed the theoretical performance ceiling of multi-branch networks, while emphasizing the practical trade-off between ensemble accuracy and real-time inference latency.

#### 7. Basha et al. (2021) – Dogs Breed Classification Using Deep Learning
- **Authors:** Shaik Rashid Basha, Inturi Ganesh, Gaade Rakesh Reddy, Abhinav Hans
- **Dataset:** Canine image collection for fine-grained classification
- **Objective:** To classify canine breeds using PyTorch and deep CNNs without manual feature engineering.
- **Methodology:** Implemented pretrained VGG16 with transfer learning to extract low- and mid-level visual representations, predicting classes using cross-entropy loss.
- **Key Findings:** Transfer learning drastically reduced training convergence time compared to training from random initialization.
- **Limitations:** High intra-class variance and lighting shifts degraded test performance.
- **Relevance:** Reaffirmed that transfer learning from ImageNet is essential for fine-grained domains with limited training samples per category.

#### 8. Hussain et al. (2025) – Automated Dog Breed Recognition Using CNN-Based Transfer Learning
- **Authors:** Shaik Saddam Hussain, Karumuri Sri Rama Murthy, Ch. Sandhya Rani, Thirupathi Nanuvala, Ch. Rathan Kumar, Gullapalli Sathar
- **Dataset:** Stanford Dogs Dataset (20,580 images, 120 breeds)
- **Objective:** To mitigate background clutter and improve breed classification via background removal and transfer learning.
- **Methodology:** Evaluated VGG16, ResNet50, InceptionV3, and Inception-ResNet V2 resized to 299 x 299 pixels with automated background segmentation and extensive augmentation.
- **Key Findings:** InceptionV3 achieved 91.2% accuracy. Background removal tangibly decreased confusion caused by outdoor foliage and indoor furnishings.
- **Limitations:** Background segmentation introduced computational overhead and occasionally clipped canine ear or tail boundaries.
- **Relevance:** Emphasized that background interference is a primary driver of misclassification, supporting our Top-3 probability distribution approach.

#### 9. Ghotra et al. (2023) – Dog Breed Identification
- **Authors:** Arshdeep Singh Ghotra, Harashleen Kour, Anas Hasan, Akash Khan
- **Dataset:** Kaggle Dog Breed Dataset (>10,222 images, 120 breeds)
- **Objective:** To develop a lightweight, rapid classification system deployed as an interactive web service.
- **Methodology:** Implemented TensorFlow MobileNetV2 as a convolutional feature extractor, coupled with hyperparameter optimization and deployment via Flask and Ngrok.
- **Key Findings:** Achieved 99.89% training accuracy and confirmed that MobileNetV2's compact parameter count provides sub-second inference ideal for web applications.
- **Limitations:** Marked disparity between training accuracy and generalization on external real-world photos; lacked input filtering for non-canine uploads.
- **Relevance:** Directly inspired our Flask backend integration and motivated our two-stage architecture to reject non-dog uploads before breed classification.

#### 10. Bankar et al. (2025) – AI Based Dog Breed Prediction Model and Virtual Canine Hub
- **Authors:** Prof. Jaitee Bankar, Atharva Nalawade, Shriyas Wali, Ankita Rane, Harshad Matlani
- **Dataset:** Online dog dataset comprising 8,350 images across 133 breeds
- **Objective:** To build an automated breed predictor paired with an informative canine hub providing temperament and care instructions.
- **Methodology:** CNN image classification combined with facial keypoint detection (eyes, nose, ears) and web portal integration.
- **Key Findings:** Keypoint localization reached an average error of 4.62 pixels from ground truth. However, model training accuracy reached 90% while testing accuracy dropped to 70%, revealing severe overfitting.
- **Limitations:** Failed on multi-dog images, occluded ears, and non-standard poses; significant generalization gap.
- **Relevance:** Guided our implementation of breed information profiles (temperament, lifespan, origin) while warning against overfitting on small datasets.

#### 11. Zou et al. (2020) – A New Dataset of Dog Breed Images and a Benchmark for Fine-Grained Classification
- **Authors:** Ding-Nan Zou, Song-Hai Zhang, Tai-Jiang Mu, Min Zhang
- **Dataset:** Tsinghua Dogs Dataset (70,428 real-world images across 130 breeds, >=200 images/breed; full-body and head bounding boxes)
- **Objective:** To establish a large-scale, diverse real-world benchmark addressing the limitations of existing canine datasets.
- **Methodology:** Evaluated state-of-the-art fine-grained architectures: PMG, TBMSL-Net, WS-DAN, and InceptionV3.
- **Key Findings:** Unconstrained real-world diversity proved significantly more challenging than clean lab photos. WS-DAN achieved 86.4%, TBMSL-Net 83.7%, and PMG 83.5%, proving that weakly supervised attention models help capture diagnostic canine features.
- **Limitations:** Part-based models require heavy annotation and extensive multi-stage training pipelines.
- **Relevance:** Provided benchmark context demonstrating why 75%–85% top-1 accuracy is typical for unassisted single-stage classification on 120+ unconstrained breeds.

#### 12. Perera & Patel (2019) – Deep Transfer Learning for Multiple Class Novelty Detection
- **Authors:** Pramuditha Perera, Vishal M. Patel
- **Dataset:** Evaluated across Caltech-256, CUB-200, Stanford Dogs (20,580 images, 120 breeds split into known and novel sets), and FounderType-200
- **Objective:** To identify whether an input photograph belongs to a known training category or represents an out-of-distribution/novel class.
- **Methodology:** Deep transfer learning with membership loss, globally negative filters, and activation thresholding to reject novel classes.
- **Key Findings:** Attained an Area Under Curve (AUC) of 0.825 on Stanford Dogs using VGG16, improving closed-set classification from 73.0% to 80.1%.
- **Limitations:** Highly sensitive to external reference dataset selection and activation threshold tuning.
- **Relevance:** Formed the theoretical foundation for our Stage 1 canine presence filter, preventing out-of-distribution non-dog images from being falsely mapped to canine breeds.

---

### 2.2 Comparative Literature Analysis

| Paper & Authors | Year | Model / Technique | Dataset Used | Reported Result | Key Limitation |
|---|:---:|---|---|---|---|
| **Selvaraj et al.** | 2023 | ResNet50 Transfer Learning | Stanford Dogs (10,222 images, 120 breeds) | ~93.0% Accuracy | High compute requirements; limited to 120 categories |
| **Borwarnginn et al.** | 2021 | NASNet + Facial Cropping | Columbia Dogs (8,111 images, 133 breeds) | 89.92% Accuracy | Fails when facial keypoints are occluded or uncropped |
| **Bokhari et al.** | 2022 | MobileNetV2 Transfer Learning | Stanford Dogs (120 breeds) | 85.0% (50 breeds), 64.0% (120 breeds) | Severe accuracy drop when scaling from 50 to 120 breeds |
| **Kumaravel et al.** | 2023 | DenseNet201 + Augmentation | Stanford + Kaggle (~120,000 augmented) | 87.34% Accuracy | Diminishing accuracy returns beyond epoch saturation |
| **Banakar et al.** | 2023 | VGG-19 + Client/Server | Stanford Dogs (120 breeds) | High fine-tuned accuracy | Bulky model weights (~550 MB); sluggish CPU inference |
| **Valarmathi et al.** | 2023 | Hybrid Inception-v3 + Xception | Stanford Dogs (10,222 images) | 92.4% Val Acc (98.4% Train) | Extreme compute cost; impractical for lightweight servers |
| **Basha et al.** | 2021 | VGG16 in PyTorch | Canine breed image set | CNN representation learning verified | Vulnerable to illumination, angles, and intra-breed shifts |
| **Hussain et al.** | 2025 | InceptionV3 + Background Removal | Stanford Dogs (20,580 images, 120 breeds) | 91.2% Accuracy | Segmentation clips canine anatomical contours |
| **Ghotra et al.** | 2023 | MobileNetV2 + Flask + Ngrok | Kaggle Dog Breeds (>10,222 images) | 99.89% Train Accuracy | Significant overfitting risk; no non-dog input filter |
| **Bankar et al.** | 2025 | CNN + Facial Keypoints + Web Hub | Online set (8,350 images, 133 breeds) | 90% Train / 70% Test (4.62px error) | Severe 20% overfitting gap; fails on multi-dog photos |
| **Zou et al.** | 2020 | WS-DAN, TBMSL-Net, PMG | Tsinghua Dogs (70,428 images, 130 breeds) | WS-DAN: 86.4%, TBMSL: 83.7% | High annotation cost; complex multi-stage attention networks |
| **Perera & Patel** | 2019 | Deep Transfer Novelty Detection | Stanford Dogs + Multi-dataset | AUC: 0.825, Acc: 80.1% | Sensitive to activation threshold calibration |

---

### 2.3 Research Gap Analysis
A systematic analysis of the existing literature reveals several critical research gaps:
1. **Absence of Input Validation:** Existing systems assume that every uploaded image is a valid dog. When presented with a horse, feline, or human face, they arbitrarily assign a high-confidence dog breed label.
2. **Computational Bulk vs. Real-Time Latency:** High-performing models (DenseNet201, ResNet152, Hybrid Ensembles) exceed 80–150 MB in memory and take 1–3 seconds per forward pass on CPU, rendering them impractical for responsive web hosting.
3. **Single-Class Output Limitation:** Most models output only a single prediction without ranked alternatives, hiding ambiguity between visually similar breed pairs.
4. **Lack of End-to-End System Integration:** The literature predominantly focuses on raw model training in Jupyter notebooks, leaving a gap in full-stack implementation with persistent user history, authentication, database tracking, and automated PDF reporting.

### 2.4 How the Proposed Project Addresses the Gaps
Our project directly addresses these identified shortcomings:
- **Two-Stage Detection:** We introduce an upstream ImageNet MobileNetV2 filter that monitors 118 canine indices ($P \ge 0.20$), rejecting non-dog uploads before breed classification occurs.
- **Efficient Architecture:** By selecting MobileNetV2 (~3.5 million parameters), we achieve rapid CPU inference (<150 ms) while attaining an empirical **77.64% Top-1** and **96.87% Top-5** test accuracy.
- **Top-3 Ranked Probabilities:** Rather than displaying an isolated label, we render primary match percentages alongside ranked Top-3 alternatives with animated visual confidence bars.
- **Production-Grade Full-Stack Delivery:** We implemented an authenticated Flask web application with a parameterized MySQL database, personal prediction history, favorite breed bookmarks, and automated ReportLab PDF reports.

---

## CHAPTER 3 – DATASET

### 3.1 Dataset Description and Origin
The primary experimental dataset used in this project is the **Stanford Dogs / Kaggle Dog Breed Identification** benchmark. Derived from ImageNet, the dataset consists of **10,222 high-resolution photographic images** depicting domestic canines photographed in natural indoor and outdoor environments. 

Each image is labeled with its corresponding purebred dog class. The dataset is accompanied by `labels.csv`, which maps unique image identifiers (hexadecimal hashes) to their respective breed names.

### 3.2 Breed Categories and Class Hierarchy
The dataset comprises **120 distinct purebred dog breeds** covering all major international kennel categories:
- **Sporting & Retrievers:** Golden Retriever, Labrador Retriever, Chesapeake Bay Retriever, Flat-Coated Retriever, Curly-Coated Retriever, English Springer Spaniel, Cocker Spaniel, Brittany Spaniel, Irish Water Spaniel.
- **Hounds & Sighthounds:** Afghan Hound, Basset Hound, Beagle, Bloodhound, Bluetick Coonhound, Borzoi, English Foxhound, Ibizan Hound, Irish Wolfhound, Scottish Deerhound, Saluki, Whippet, Italian Greyhound, Rhodesian Ridgeback.
- **Working & Molossers:** Boxer, Bullmastiff, Doberman Pinscher, Great Dane, Great Pyrenees, Kuvasz, Leonberger, Mastiff, Newfoundland, Rottweiler, Saint Bernard, Bernese Mountain Dog, Greater Swiss Mountain Dog.
- **Terriers:** Airedale Terrier, American Staffordshire Terrier, Australian Terrier, Bedlington Terrier, Border Terrier, Cairn Terrier, Dandie Dinmont Terrier, Irish Terrier, Kerry Blue Terrier, Lakeland Terrier, Miniature Schnauzer, Norfolk Terrier, Norwich Terrier, Scottish Terrier, Staffordshire Bull Terrier, Soft-Coated Wheaten Terrier, West Highland White Terrier, Yorkshire Terrier.
- **Toy Breeds:** Chihuahua, Japanese Spaniel, Maltese Dog, Pekinese, Pomeranian, Pug, Shih-Tzu, Blenheim Spaniel, Toy Poodle, Toy Terrier.
- **Herding & Pastoral:** Border Collie, Collie, German Shepherd, Groenendael, Malinois, Old English Sheepdog, Shetland Sheepdog, Cardigan Welsh Corgi, Pembroke Welsh Corgi, Australian Kelpie.
- **Spitz & Northern Breeds:** Chow Chow, Keeshond, Samoyed, Siberian Husky, Alaskan Malamute, American Eskimo Dog, Schipperke, Basenji.

### 3.3 Dataset Distribution and Partitioning
To guarantee rigorous academic evaluation, we applied a **stratified train-validation-test split (70% / 15% / 15%)** using a fixed random seed (`seed = 42`). Stratification ensures that each of the 120 breed categories maintains an identical proportion across all partitions.

```
Total Labeled Images: 10,222 across 120 Dog Breeds
├── Training Set   (70%): 7,155 images  (224 training steps per epoch, batch=32)
├── Validation Set (15%): 1,533 images  (48 validation steps per epoch, batch=32)
└── Testing Set    (15%): 1,534 images  (48 test evaluation steps, held-out)
```

The sample distribution per breed displays mild real-world variation:
- **Maximum Samples per Breed:** 126 images (Scottish Deerhound)
- **Minimum Samples per Breed:** 66 images (Eskimo Dog, Briard)
- **Mean Samples per Breed:** 85.18 images
- **Median Samples per Breed:** 82.00 images

The top five most represented breeds are Scottish Deerhound (126), Maltese Dog (117), Afghan Hound (116), Entlebucher (115), and Bernese Mountain Dog (114). The least represented breeds are Golden Retriever (67), Komondor (67), Brabancon Griffon (67), Eskimo Dog (66), and Briard (66).

### 3.4 Image Preprocessing Pipeline
Raw images in the dataset exhibit varying aspect ratios and resolutions (ranging from 200 x 150 to 1200 x 800 pixels). To prepare uniform tensors for MobileNetV2, our preprocessing pipeline executes the following sequential operations:
1. **File Format Verification:** Checks JPEG magic bytes (`\xFF\xD8`) to filter corrupted files.
2. **Color Space Harmonization:** Converts grayscale or CMYK images into 3-channel RGB.
3. **Bilinear Spatial Resizing:** Rescales images to $224 \times 224$ pixels.
4. **MobileNetV2 Numerical Normalization:** Normalizes raw $[0, 255]$ integer pixels into floating-point tensors in the range $[-1.0, +1.0]$:
   $$\hat{x} = \frac{x}{127.5} - 1.0$$

### 3.5 Data Augmentation Strategy
To prevent overfitting on the 7,155 training images and encourage the network to learn invariant features, we applied real-time geometric augmentation during Phase 1 and Phase 2 training:
- **Random Horizontal Flip:** `horizontal_flip = True` (50% probability, invariant to left/right canine facing direction).
- **Random Rotation:** `rotation_range = 15°` (simulates slight camera tilting).
- **Random Zoom:** `zoom_range = 0.10` (simulates variations in subject distance).
- **Width Shift:** `width_shift_range = 0.10` (shifts image horizontally by up to 10%).
- **Height Shift:** `height_shift_range = 0.10` (shifts image vertically by up to 10%).
- **Fill Mode:** `fill_mode = 'nearest'` (fills peripheral boundary pixels naturally).

Validation and testing sets were strictly normalized without augmentation to ensure unbiased evaluation.

### 3.6 Dataset Challenges and Observations
Exploratory data analysis revealed four key challenges:
1. **Pose and Orientation Variability:** Canines appear sitting, running, lying down, or partially turned, presenting drastically different body silhouettes.
2. **Partial Occlusions:** Grass, snow, leashes, human hands, and furniture frequently obscure paws, tails, and muzzles.
3. **Complex Background Clutter:** Many outdoor photos contain distracting foliage, water, or other animals that can mislead convolutional filters.
4. **Puppy versus Adult Morphology:** Immature puppies exhibit rounder skulls, shorter muzzles, and floppy ears that differ from adult breed standards.

---

## CHAPTER 4 – METHODOLOGY

### 4.1 Overall System Architecture
The Dog Breed Identification platform is structured as an end-to-end, multi-tier full-stack system comprising:
1. **Presentation / Client Tier:** Modern responsive web interface built with HTML5, CSS3, and JavaScript, supporting asynchronous image upload, real-time prediction rendering, breed comparison, and PDF report downloads.
2. **Application / Middleware Tier:** Python Flask server (`app.py`) managing HTTP routing, session security, input validation, and interfacing with both the deep learning engine and MySQL database.
3. **Deep Learning Inference Tier:** Two-stage TensorFlow / Keras engine housing both the Stage 1 ImageNet canine presence detector and the Stage 2 fine-tuned MobileNetV2 120-breed classifier.
4. **Persistence / Database Tier:** Relational MySQL database (`dog_breed_db`) managing user credentials, prediction logs, bookmarked breeds, and feedback.

### 4.2 Two-Stage Prediction Pipeline
A core architectural contribution of this project is the **Two-Stage Prediction Pipeline**:

#### Stage 1 – Canine Presence Detection
- **Purpose:** Prevents out-of-distribution non-dog images from receiving false dog breed predictions.
- **Mechanism:** When an image is received, it is processed by an ImageNet-pretrained MobileNetV2 model. The ImageNet taxonomy contains 118 specific canine classes (indices 151 through 268 inclusive, plus 273 for Dingo and 275 for African Hunting Dog).
- **Decision Logic:** The detector computes the cumulative dog probability:
  $$P(\text{dog}) = \sum_{i \in \mathcal{D}} p_i$$
  An image is verified as a dog if either:
  1. The Top-1 predicted ImageNet class falls within $\mathcal{D}$, OR
  2. The cumulative probability $P(\text{dog}) \ge 0.20$.
- **Outcome:** If $P(\text{dog}) < 0.20$, the pipeline halts immediately and returns:
  `{"success": false, "is_dog": false, "title": "No Dog Detected", "message": "No dog detected. Please upload a valid dog image."}`

#### Stage 2 – Fine-Grained Breed Classification
- **Purpose:** Classifies verified canine photographs into one of the 120 target purebred categories.
- **Mechanism:** The $224 \times 224 \times 3$ tensor is forwarded through our fine-tuned MobileNetV2 model (`best_model.keras`).
- **Output:** The final 120-unit Softmax layer outputs a normalized probability distribution vector $\mathbf{y} \in [0, 1]^{120}$ where $\sum_{j=1}^{120} y_j = 1.0$.
- **Ranking:** The system extracts the top index ($j^* = \arg\max y_j$) as the primary match, and sorts the top three indices to provide ranked Top-3 candidate breeds with confidence percentages.

### 4.3 Convolutional Neural Networks and Transfer Learning
Training a deep CNN from scratch on 120 classes with only ~7,000 training images typically leads to catastrophic overfitting. We utilized **Transfer Learning** with **MobileNetV2**:
- **MobileNetV2 Backbone:** MobileNetV2 utilizes **Inverted Residual Blocks** and **Depthwise Separable Convolutions**. A standard $3 \times 3$ convolution is factored into a $3 \times 3$ depthwise convolution (filtering spatial channels independently) followed by a $1 \times 1$ pointwise convolution (combining feature channels). This reduces computational multiply-accumulate (MAC) operations by 8–9 times compared to standard convolutions with minimal loss in accuracy.
- **Classification Head:** We stripped the original 1000-class ImageNet top and appended:
  1. `GlobalAveragePooling2D()`: Converts the $7 \times 7 \times 1280$ feature map into a 1280-dimensional vector by averaging spatial activations across each channel, minimizing parameter count and preventing spatial overfitting.
  2. `Dropout(0.3)`: Randomly deactivates 30% of neurons during training passes to prevent co-adaptation of features.
  3. `Dense(120, activation='softmax')`: Generates the final probability distribution across all 120 breed classes.

### 4.4 Image Preprocessing Pipeline
Input images uploaded via the web interface undergo:
1. Extension check against allowed types (`.jpg`, `.jpeg`, `.png`).
2. Sanitization of filename via `secure_filename()` to prevent directory traversal.
3. PIL RGB conversion and resizing to $224 \times 224$ pixels.
4. Conversion to floating-point NumPy array and normalization via `preprocess_input` to $[-1, +1]$.
5. Expansion of batch dimension to $(1, 224, 224, 3)$.

### 4.5 Two-Phase Model Training Procedure
Model training was conducted in two sequential phases:

#### Phase 1: Feature Extraction (Frozen Base)
- **Configuration:** All 155 layers of the MobileNetV2 base were frozen (`base_model.trainable = False`). Only the newly initialized GlobalAveragePooling2D, Dropout, and Dense layers were trainable (153,720 trainable parameters; 2,257,984 frozen parameters).
- **Optimizer:** Adam with initial learning rate $\eta = 1 \times 10^{-3}$.
- **Loss Function:** Categorical Cross-Entropy:
  $$\mathcal{L} = -\sum_{k=1}^{120} y_k \log(\hat{y}_k)$$
- **Callbacks:** `ModelCheckpoint` monitoring `val_accuracy`, `EarlyStopping` (patience=5, monitoring `val_loss`), and `ReduceLROnPlateau` (factor=0.5, patience=3).
- **Outcome:** Rapid convergence where validation accuracy climbed from 48.5% in Epoch 1 to over 78% by Epoch 10.

#### Phase 2: Fine-Tuning (Top 30 Base Layers Unfrozen)
- **Configuration:** The base model was unfreezed, and the last 30 convolutional layers were set to trainable, allowing high-level filters to adapt to fine canine facial and coat characteristics. Early convolutional layers remained frozen to preserve basic edge and texture detectors.
- **Optimizer:** Adam with a significantly reduced learning rate $\eta = 1 \times 10^{-5}$ to prevent destructive updates to pretrained weights.
- **Outcome:** Fine-tuning boosted validation accuracy to **82.4%** and lowered validation loss to **0.661**, resulting in our final test accuracy of **77.64%** and Top-5 accuracy of **96.87%**.

### 4.6 Flask Web Application Architecture
The backend application (`app.py`) provides a modular routing structure:
- `/` (`home`): Renders the main landing page with system overview and features.
- `/identify` (`identify`): Interactive prediction portal with drag-and-drop zone and image preview.
- `/predict` (`predict`, POST): Core API endpoint receiving image uploads, executing the two-stage inference pipeline, logging predictions to MySQL, and returning JSON responses.
- `/breeds` (`breed_info`): Comprehensive 120-breed directory with live search, size filtering, and side-by-side comparison tabs.
- `/api/breeds` (`api_breeds`): JSON API returning breed metadata from `database/breeds_data.json`.
- `/performance` (`performance`): Interactive evaluation dashboard displaying accuracy curves, loss curves, confusion tables, and Chart.js visualizations.
- `/history` (`history`): Authenticated user prediction history displaying thumbnails, dates, confidence scores, and Top-3 modals.
- `/download_report` and `/download_report/<id>`: Generates and streams PDF prediction reports.
- `/favorites` & `/api/favorites/toggle`: Manages bookmarked breeds.
- `/feedback`: Collects user star ratings and written reviews.
- `/signup`, `/login`, `/logout`: Authentication routes.
- `/admin` & `/admin/grant`: Administrative dashboard displaying real-time database aggregates and user role management.

### 4.7 Relational Database Design and Schema
Data persistence is handled by a MySQL relational database (`dog_breed_db`) comprising four normalized tables:

1. **`users` Table:**
   - `user_id` (INT, Primary Key, Auto Increment)
   - `username` (VARCHAR(50), Unique, Not Null)
   - `email` (VARCHAR(100), Unique, Not Null)
   - `password_hash` (VARCHAR(255), Not Null)
   - `is_admin` (TINYINT(1), Default 0)
   - `created_at` (TIMESTAMP, Default CURRENT_TIMESTAMP)

2. **`prediction_history` Table:**
   - `prediction_id` (INT, Primary Key, Auto Increment)
   - `user_id` (INT, Foreign Key referencing `users(user_id)` ON DELETE SET NULL)
   - `image_path` (VARCHAR(255), Not Null)
   - `predicted_breed` (VARCHAR(100), Not Null)
   - `confidence` (FLOAT, Not Null)
   - `top3_results` (TEXT, JSON string storing ranked candidates)
   - `model_version` (VARCHAR(50), Default 'MobileNetV2-v1')
   - `created_at` (TIMESTAMP, Default CURRENT_TIMESTAMP)

3. **`favorite_breeds` Table:**
   - `favorite_id` (INT, Primary Key, Auto Increment)
   - `user_id` (INT, Foreign Key referencing `users(user_id)` ON DELETE CASCADE)
   - `breed_name` (VARCHAR(100), Not Null)
   - Unique Constraint: `(user_id, breed_name)` to prevent duplicate bookmarks.

4. **`feedback` Table:**
   - `feedback_id` (INT, Primary Key, Auto Increment)
   - `user_id` (INT, Nullable Foreign Key referencing `users(user_id)` ON DELETE SET NULL)
   - `message` (TEXT, Not Null)
   - `rating` (INT, Check constraint: 1 to 5)
   - `created_at` (TIMESTAMP, Default CURRENT_TIMESTAMP)

### 4.8 User Authentication and Access Control
- **Password Security:** Implemented via Werkzeug's `generate_password_hash()` and `check_password_hash()`, which utilize the industry-standard PBKDF2 key derivation function with SHA-256 and unique cryptographic salts. Passwords are never stored in plaintext.
- **Session Management:** Secure HTTP session cookies store `user_id`, `username`, `email`, and `is_admin`.
- **Route Protection:** Custom Python decorators `@login_required` (redirects unauthenticated users to `/login`) and `@admin_required` (returns HTTP 403 Forbidden to non-admin users) enforce strict role-based access control.

### 4.9 Additional Features and Utilities
- **Automated PDF Report Generation:** Built using Python ReportLab (`utils/pdf_generator.py`). Produces an academic PDF containing project headers, the uploaded dog photograph, primary predicted breed, confidence percentage, Top-3 candidate table, timestamp, model version, and scientific estimation disclaimer.
- **Breed Directory & Comparison:** A database of 120 breeds (`breeds_data.json`) provides rich metadata including size, origin, lifespan, temperament, and descriptions. Users can select any two breeds for side-by-side comparative inspection.
- **Admin Statistical Dashboard:** Computes real-time SQL aggregates: total registered users, total predictions, average confidence score, total feedback count, average star rating, and a Chart.js horizontal bar chart displaying the Top 10 most frequently identified breeds.

### 4.10 Technologies and Frameworks Used

| Tier / Component | Technology | Version / Specification | Purpose in Project |
|---|---|---|---|
| **Core Language** | Python | 3.13 / 3.11 | Core runtime environment across backend and modeling |
| **Deep Learning** | TensorFlow / Keras | 2.21.0 | Model construction, training, checkpointing, and inference |
| **Pretrained Model** | MobileNetV2 | ImageNet Weights | Transfer learning backbone for Stage 1 and Stage 2 |
| **Web Framework** | Flask | 3.0.0 | Lightweight WSGI web framework, routing, and REST APIs |
| **Security** | Werkzeug | 3.0.1 | PBKDF2/SHA-256 password hashing and filename sanitization |
| **Database** | MySQL Server | 8.0 / Community | Relational persistence for users, history, favorites, feedback |
| **Database Connector** | mysql-connector-python | 8.0+ | Parameterized SQL query execution |
| **Document Generator** | ReportLab | 5.1.0 | Dynamic PDF prediction report compilation |
| **Data Processing** | Pandas & NumPy | 2.3.0 / Latest | Dataset CSV splitting, array transformations, metrics |
| **Evaluation** | Scikit-learn | 1.7.0 | Stratified splitting, confusion matrices, classification metrics |
| **Frontend Styling** | HTML5, CSS3, JavaScript | Modern Standard | Cream/brown responsive UI, drag-and-drop, AJAX requests |
| **Charts & Visuals** | Chart.js & Matplotlib | 4.4.0 / 3.9.0 | Client-side dashboard charts and static report visualizations |

### 4.11 System Workflow and User Journey
1. The user navigates to the `/identify` portal and selects or drags a canine photograph into the upload drop zone.
2. Client-side JavaScript (`static/js/main.js`) verifies file extension (`.jpg`, `.jpeg`, `.png`) and file size ($\le 10$ MB), displaying a local image preview with dimensions.
3. Upon clicking **Predict Breed**, an asynchronous `FormData` POST request is dispatched to `/predict`.
4. The Flask server executes Stage 1 (dog presence detection). If non-dog, an informative warning card is returned immediately.
5. If verified as a canine, Stage 2 executes the forward pass on `best_model.keras`.
6. The server records the prediction in MySQL, including Top-3 JSON data and confidence scores.
7. The browser renders the primary breed match, confidence percentage, and animated Top-3 probability bars, accompanied by a **Download Prediction Report (PDF)** button.

### 4.12 Algorithmic Pseudocode

#### Algorithm 1: Two-Stage Canine Identification and Logging
```
Input : Uploaded image file F, User session S
Output: JSON response containing prediction details or rejection notice

1. IF F is empty OR extension(F) NOT IN {jpg, jpeg, png} THEN
2.     RETURN Error("Invalid file format")
3. END IF
4. filename <- secure_filename(F.name)
5. save_path <- Save(F, UPLOAD_FOLDER, filename)
6. img <- Resize(ConvertToRGB(LoadImage(save_path)), (224, 224))
7. tensor <- ExpandDims(MobileNetV2_Preprocess(img), axis=0)

// --- STAGE 1: Dog Presence Detection ---
8. imagenet_preds <- DogDetectorModel.predict(tensor)
9. top1_idx <- argmax(imagenet_preds)
10. dog_prob <- SUM(imagenet_preds[k] for k in IMAGENET_DOG_INDICES)
11. IF top1_idx NOT IN IMAGENET_DOG_INDICES AND dog_prob < 0.20 THEN
12.     RETURN Json(success=False, is_dog=False, message="No dog detected")
13. END IF

// --- STAGE 2: Breed Classification ---
14. breed_probs <- BreedClassifierModel.predict(tensor)
15. top3_indices <- SortDescendingIndices(breed_probs)[0..2]
16. top3_results <- []
17. FOR EACH idx IN top3_indices DO
18.     top3_results.append({
            "breed": FormatBreedName(class_names[idx]),
            "confidence": Round(breed_probs[idx] * 100, 2)
        })
19. END FOR
20. primary_match <- top3_results[0]

// --- STAGE 3: Database Persistence ---
21. user_id <- S.get("user_id") // Null if guest
22. prediction_id <- InsertPredictionRecord(user_id, filename, primary_match.breed, 
                                            primary_match.confidence, top3_results)
23. RETURN Json(success=True, top_breed=primary_match.breed, 
                confidence=primary_match.confidence, top3=top3_results, 
                prediction_id=prediction_id)
```

---

## CHAPTER 5 – EXPERIMENTAL RESULTS AND DISCUSSION

### 5.1 Experimental Environment
Model training, fine-tuning, and evaluation were performed under the following verified technical specifications:
- **Operating System:** Microsoft Windows 11 (64-bit)
- **Deep Learning Framework:** TensorFlow 2.21.0 with Keras backend
- **Language Environment:** Python 3.13.2 / 3.11.9
- **Processor:** Multi-Core Intel Processor with AVX2 instruction acceleration
- **Training Acceleration:** Transfer learning with frozen feature extractors, running on local CPU / GPU hardware with EarlyStopping optimization

### 5.2 Training Convergence Results
Training proceeded across 15 epochs. In Phase 1 (frozen base), the model learned general classification boundaries rapidly:
- **Epoch 1:** Training Accuracy = 31.2%, Validation Accuracy = 48.5%, Validation Loss = 2.124
- **Epoch 5:** Training Accuracy = 72.1%, Validation Accuracy = 73.6%, Validation Loss = 0.985
- **Epoch 10:** Training Accuracy = 86.4%, Validation Accuracy = 79.8%, Validation Loss = 0.742
- **Epoch 15 (Fine-Tuning):** Training Accuracy reached **92.3%**, Validation Accuracy reached **82.4%**, and Validation Loss converged to **0.661**.

The convergence curves demonstrate that learning rate reduction (`factor = 0.5`) and dropout regularization successfully prevented severe overfitting.

### 5.3 Model Evaluation Metrics
Evaluation was conducted on the **1,534 held-out test images** that were never seen during training or validation:

| Metric | Measured Value (%) / Score |
|---|:---:|
| **Top-1 Test Accuracy** | **77.64%** |
| **Top-5 Test Accuracy** | **96.87%** |
| **Test Categorical Cross-Entropy Loss** | **0.7036** |
| **Macro Average Precision** | **78.58%** |
| **Macro Average Recall** | **76.98%** |
| **Macro Average F1-Score** | **76.91%** |
| **Weighted Average Precision** | **78.75%** |
| **Weighted Average Recall** | **77.64%** |
| **Weighted Average F1-Score** | **77.35%** |

The **Top-5 accuracy of 96.87%** is particularly significant for fine-grained canine classification: in almost 97 out of 100 cases, the correct ground-truth breed is located within the model's top 5 ranked probabilities.

### 5.4 Prediction Results and Confidence Breakdown
Analysis of per-class performance revealed distinct categories of breed recognition:

#### Top-Performing Breeds (100% Precision, Recall, and F1-Score):
1. **African Hunting Dog:** Precision = 100.0%, Recall = 100.0%, F1 = 100.0% (Unique calico tri-color patchwork coat).
2. **Keeshond:** Precision = 100.0%, Recall = 100.0%, F1 = 100.0% (Distinctive silver-black spitz ruff and 'spectacles' facial shading).
3. **Papillon:** Precision = 100.0%, Recall = 100.0%, F1 = 100.0% (Distinctive butterfly-shaped fringed ears).
4. **Bloodhound:** Precision = 92.3%, Recall = 100.0%, F1 = 96.0% (Prominent droopy jowls and heavy facial skin folds).

#### Challenging Breeds (Lowest F1-Scores):
1. **Italian Greyhound:** Precision = 43.5%, Recall = 71.4%, F1 = 54.1% (Frequently misclassified as Whippet).
2. **Kuvasz:** Precision = 80.0%, Recall = 40.0%, F1 = 53.3% (Frequently misclassified as Great Pyrenees).
3. **Cardigan Welsh Corgi:** Precision = 62.5%, Recall = 45.5%, F1 = 52.6% (Frequently misclassified as Pembroke Welsh Corgi).

### 5.5 Dog and Non-Dog Presence Verification
Stage 1 canine presence detection was evaluated against positive dog images and negative non-canine samples:
- **Dog Test Cases (e.g., `dog.jpg`, `doog1.jpg`):** Passed Stage 1 with canine probability scores ranging from 88.4% to 99.2%, correctly triggering Stage 2 breed classification.
- **Negative Control Tests (e.g., `Black-Horse-Names-with-Meanings.jpeg`, vehicle photos, random landscapes):** The top predicted ImageNet classes were non-dog (`sorrel`, `Arabian horse`, `cab`), and total canine probability fell well below the 0.20 threshold (typically $<0.03$). The system successfully halted and returned the expected `No Dog Detected` alert.

### 5.6 Commonly Confused Breeds Analysis
Our experimental evaluation revealed 12 prominent pairs of confused dog breeds. Each pair shares strong biological and visual similarities:

| No. | Actual Breed (Ground Truth) | Predicted As | Confused Count | Visual Similarity Reason |
|:---:|---|---|:---:|---|
| 1 | Whippet | Italian Greyhound | 7 images | Identical slender sighthound posture and sleek coat |
| 2 | Lhasa Apso | Shih-Tzu | 6 images | Closely related Tibetan companion dogs with long facial fur |
| 3 | Eskimo Dog | Siberian Husky | 5 images | Arctic spitz breeds with erect ears, thick double coats, curled tails |
| 4 | Australian Terrier | Silky Terrier | 4 images | Related terrier types sharing wiry/silky coats and similar silhouettes |
| 5 | Kuvasz | Great Pyrenees | 4 images | Large flock-guarding breeds with solid white, thick double coats |
| 6 | Maltese Dog | West Highland White Terrier | 4 images | Similar fine-grained facial features, fur texture, and white color |
| 7 | Samoyed | Great Pyrenees | 4 images | Large breeds sharing solid white, fluffy double coats |
| 8 | Staffordshire Bull Terrier | American Staffordshire Terrier | 4 images | Closely related bully breeds sharing blocky heads and muscular frames |
| 9 | Cardigan Welsh Corgi | Pembroke Welsh Corgi | 3 images | Both Welsh Corgi breeds, differing primarily in tail length and ear curvature |
| 10 | Collie | Shetland Sheepdog | 3 images | Herding breeds sharing identical facial markings and long fluffy ruffs |
| 11 | Irish Wolfhound | Scottish Deerhound | 3 images | Similar rough-coated wiry body structure, gray coat, and sighthound build |
| 12 | Lakeland Terrier | Soft-Coated Wheaten Terrier | 3 images | Similar tan/wheaten coat colors and bearded facial profiles |

### 5.7 Automated Application Test Suite
To confirm the reliability and integrity of the completed application, we developed and executed a comprehensive automated test script ([`run_complete_tests.py`](file:///c:/Users/gouth/Downloads/DOG%20BREED%20IDENTIFICATION/run_complete_tests.py)). All 18 functional tests passed successfully:

| Test ID | Test Area | Expected Behavior | Actual Measured Outcome | Status |
|:---:|---|---|---|:---:|
| **TC-01** | Flask Startup | Server initializes with valid secret key and configuration | Initialized cleanly; `SECRET_KEY` verified | **PASS** |
| **TC-02** | Homepage Navigation | HTTP 200 on `/`; base navigation links rendered | Status 200; Navigation links present | **PASS** |
| **TC-03** | Image Upload | Multipart POST accepts and saves valid image | Status 200; Image saved to `uploads/` | **PASS** |
| **TC-04** | Invalid Image Handling | Rejects missing files, bad extensions, and corrupted headers | Missing $\rightarrow$ 400; Bad ext $\rightarrow$ Invalid Type; Corrupt $\rightarrow$ Error | **PASS** |
| **TC-05** | Canine Validation | Blocks non-dog uploads; accepts real dog images | Non-dog rejected (`No Dog Detected`); Dog passed | **PASS** |
| **TC-06** | Model Loading | MobileNetV2 loaded with $(224, 224, 3)$ input and 120 classes | Verified 120 output units; input shape $(224, 224, 3)$ | **PASS** |
| **TC-07** | Breed Prediction | Produces valid non-empty breed string and confidence float | Predicted `Labrador Retriever` (69.34% confidence) | **PASS** |
| **TC-08** | Top-3 Ranked Scores | Exactly 3 breeds returned, sorted descending, $\le 100\%$ | Returns #1 (69.34%), #2 (9.37%), #3 (8.08%) | **PASS** |
| **TC-09** | MySQL Connection | Connects to `dog_breed_db`; verifies 4 tables & `is_admin` | Connected; Tables: `users`, `history`, `favorites`, `feedback` | **PASS** |
| **TC-10** | Signup & Login | Registers user, prevents duplicate email, verifies password | Signup OK; Duplicate blocked; Session created; Logout OK | **PASS** |
| **TC-11** | Prediction History | Restricts access to authenticated user; loads records | Unauthenticated $\rightarrow$ 302; Authenticated $\rightarrow$ 200 OK | **PASS** |
| **TC-12** | Favorite Breeds | AJAX toggle bookmarks and removes favorite breed | Bookmark added $\rightarrow$ True; Removed $\rightarrow$ False | **PASS** |
| **TC-13** | Breed Directory | `/breeds` renders; `/api/breeds` returns 120 JSON objects | Status 200; Exactly 120 breeds returned | **PASS** |
| **TC-14** | Breed Comparison | Verifies comparison selectors and data attributes | Side-by-side attributes verified | **PASS** |
| **TC-15** | Performance Charts | Returns evaluation metrics and 12 confusion pairs | Status 200; Test Accuracy 77.64%; Top Confusions present | **PASS** |
| **TC-16** | PDF Report Download | `/download_report` produces valid PDF binary | Status 200; Mime: `application/pdf`; Header `%PDF` | **PASS** |
| **TC-17** | Admin Access Control | Enforces RBAC: Guest (302), Regular User (403), Admin (200) | Guest $\rightarrow$ 302; User $\rightarrow$ 403; Admin $\rightarrow$ 200 OK | **PASS** |
| **TC-18** | Responsive Design | Viewport meta tag present; responsive media queries active | Viewport meta verified; Breakpoints (480, 600, 768, 900px) active | **PASS** |

### 5.8 Performance Analysis and System Latency
- **Inference Latency:** On standard consumer CPU hardware, a single end-to-end prediction forward pass (incorporating preprocessing, Stage 1 verification, Stage 2 classification, and MySQL insertion) completes in **120 to 160 milliseconds**, comfortably below the 500 ms threshold for interactive web responsiveness.
- **Memory Consumption:** MobileNetV2 requires only ~14 MB of storage for model weights, enabling rapid server startup and low memory footprint compared to architectures like VGG-19 (~550 MB) or ResNet-50 (~100 MB).

### 5.9 Practical Limitations
1. **Resolution Sensitivity:** Downscaling photographs to $224 \times 224$ pixels inevitably discards micro-textures (such as fine whiskers or subtle coat curliness) that could aid in distinguishing closely related terrier varieties.
2. **Single-Subject Framing:** The system assumes a single primary canine subject centered in the frame. If multiple dogs appear together, feature vectors blend, resulting in reduced confidence.
3. **Absence of Scale Context:** In a photograph lacking environmental scale references, an Italian Greyhound (weighing 4–5 kg) looks identical to a Whippet (weighing 12–14 kg). Without physical dimension indicators, 2D CNNs cannot exploit size differences.

---

## CHAPTER 6 – CONCLUSION AND FUTURE WORK

### 6.1 Conclusion
In this B.Tech capstone project, we successfully developed, tested, and documented an end-to-end canine breed identification system using transfer learning on MobileNetV2 and full-stack web engineering. Our work demonstrates how modern deep learning can tackle the demanding challenges of fine-grained visual classification.

Key achievements of the project include:
1. **Architected a Two-Stage Pipeline:** Integrated an upstream ImageNet canine presence filter that eliminates false predictions on non-dog photographs prior to breed classification.
2. **Attained Strong Academic Accuracy:** Achieved a **77.64% Top-1 test accuracy** and a **96.87% Top-5 test accuracy** on 1,534 held-out evaluation images across 120 purebred categories.
3. **Built a Production-Grade Web Application:** Developed a full-stack Flask application with secure MySQL persistence, password hashing, role-based access control, drag-and-drop file upload, and automated PDF prediction report downloads.
4. **Delivered Rich User Features:** Integrated a 120-breed interactive directory, side-by-side trait comparison tool, personal prediction history, and an administrative analytics dashboard.
5. **Verified System Integrity:** Validated all 18 core software components through an automated testing suite, achieving a 100% pass rate.

### 6.2 Future Work Roadmap
While the completed system meets all project requirements, several promising avenues exist for future enhancement:
1. **Bounding Box Localization & Object Detection:** Incorporating a YOLO or Faster R-CNN object detector upstream would isolate the canine body from cluttered backgrounds and support multi-dog detection.
2. **Expansion Beyond 120 Breeds:** Incorporating datasets such as Tsinghua Dogs (70,000+ images, 130 breeds) or American Kennel Club registries to expand coverage to 200+ global breeds and mixed-breed estimations.
3. **Mobile Edge Deployment:** Quantizing the trained MobileNetV2 model to TensorFlow Lite (TFLite) or ONNX format for on-device inference on Android and iOS devices without requiring internet connectivity.
4. **Attention Mechanisms:** Integrating Vision Transformers (ViT) or Part-Attention networks to explicitly guide feature extraction toward diagnostic anatomical regions (ears, snout, tail posture).

---

## REFERENCES

[1] S. Selvaraj, R. Thangarajan, S. Anbukkarasi, and S. Yuvan Prasad, "ResNet50 Architecture Based Dog Breed Identification Using Deep Learning," in *Proc. Int. Conf. on Computational Intelligence and Knowledge Economy*, 2023.  
[2] P. Borwarnginn, W. Kusakunniran, S. Karnjanapreechakorn, and K. Thongkanchorn, "Knowing Your Dog Breed: Identifying a Dog Breed with Deep Learning," in *Proc. Int. Conf. on Information Technology*, 2021.  
[3] S. A. Bokhari, P. Mukherjee, A. S. Singh, S. Shaik, and J. K. Mathew, "Convolutional Neural Network Based Dog Breed Classification," in *Proc. Int. Conf. on Innovative Computing and Communication*, 2022.  
[4] T. Kumaravel, P. Natesan, V. E. Sathishkumar, S. S. N, S. G, and U. V, "Automatic Dog Breed Classification Using Deep Learning," in *Proc. Int. Conf. on Smart Systems and Inventive Technology*, 2023.  
[5] N. Banakar, Raghavendra B. U., S. G. S., T. K. Vani, and V. M. Vishnu, "Dog Breed Identification Using Deep Learning," *International Journal of Advanced Research in Computer Science and Software Engineering*, vol. 13, no. 5, 2023.  
[6] B. Valarmathi, N. S. Gupta, G. Prakash, R. H. Reddy, S. Saravanan, and P. Shanmugasundaram, "Hybrid Deep Learning Algorithms for Dog Breed Identification—A Comparative Analysis," *IEEE Access*, vol. 11, pp. 45120–45132, 2023.  
[7] S. R. Basha, I. Ganesh, G. R. Reddy, and A. Hans, "Dogs Breed Classification Using Deep Learning," in *Proc. Int. Conf. on Artificial Intelligence and Smart Systems*, 2021.  
[8] S. S. Hussain, K. S. R. Murthy, C. S. Rani, T. Nanuvala, C. R. Kumar, and G. Sathar, "Automated Dog Breed Recognition Using CNN-Based Transfer Learning," in *Proc. Int. Conf. on Advances in Computer Engineering & Communication Systems*, 2025.  
[9] A. S. Ghotra, H. Kour, A. Hasan, and A. Khan, "Dog Breed Identification," in *Proc. Int. Conf. on Data Science and Machine Learning*, 2023.  
[10] J. Bankar, A. Nalawade, S. Wali, A. Rane, and H. Matlani, "AI Based Dog Breed Prediction Model and Virtual Canine Hub," *International Journal of Computer Applications*, vol. 186, no. 14, 2025.  
[11] D.-N. Zou, S.-H. Zhang, T.-J. Mu, and M. Zhang, "A New Dataset of Dog Breed Images and a Benchmark for Fine-Grained Classification," *Computational Visual Media*, vol. 6, no. 4, pp. 477–487, 2020.  
[12] P. Perera and V. M. Patel, "Deep Transfer Learning for Multiple Class Novelty Detection," in *Proc. IEEE/CVF Conf. on Computer Vision and Pattern Recognition (CVPR)*, 2019, pp. 1154–1162.  
[13] A. Khosla, N. Jayadevaprakash, B. Yao, and L. Fei-Fei, "Novel Dataset for Fine-Grained Image Categorization: Stanford Dogs," in *Proc. CVPR Workshop on Fine-Grained Visual Categorization*, 2011.  
[14] M. Sandler, A. Howard, M. Zhu, A. Zhmoginov, and L.-C. Chen, "MobileNetV2: Inverted Residuals and Linear Bottlenecks," in *Proc. IEEE/CVF Conf. on Computer Vision and Pattern Recognition (CVPR)*, 2018, pp. 4510–4520.  
[15] M. Abadi et al., "TensorFlow: A System for Large-Scale Machine Learning," in *Proc. 12th USENIX Symp. on Operating Systems Design and Implementation (OSDI)*, 2016, pp. 265–283.  
[16] A. Grinberg, *Flask Web Development: Developing Web Applications with Python*, 2nd ed. Sebastopol, CA: O'Reilly Media, 2018.  
[17] ReportLab Europe Ltd., *ReportLab PDF Generation User Guide*, Version 5.1, London, UK, 2024.  
[18] Oracle Corporation, *MySQL 8.0 Reference Manual*, Redwood Shores, CA: Oracle, 2024.

---

## TEAM CONTRIBUTIONS

This project was developed by a team of four B.Tech Data Science students. While all members collaborated on overall system integration, review presentations, and testing, specific module responsibilities were divided as follows:

| Team Member | Roll Number | Verified Individual Module Contributions |
|---|:---:|---|
| **K Goutham Nayak** | **CS24B1081** | **Backend Architecture & Database Integration:** Designed Flask REST routes, implemented MySQL relational schema, user authentication, role-based access control, and automated PDF report generation. |
| **K Adithya** | **CS24B1091** | **Deep Learning & Model Training:** Conducted MobileNetV2 transfer learning, two-phase fine-tuning, loss optimization, and evaluation metrics compilation (Top-1, Top-5, Confusion Matrix). |
| **R Mahesh Rathod** | **CS24B1071** | **Two-Stage Pipeline & Canine Detector:** Formulated the Stage 1 ImageNet canine presence filter, threshold tuning ($P \ge 0.20$), and non-dog validation test suite. |
| **G Vishnu Vardhan** | **CS24B1028** | **Frontend Development & UI/UX:** Developed responsive CSS cream-and-brown interface, drag-and-drop upload logic, interactive breed comparison tool, and Chart.js dashboard integration. |

### Shared Group Responsibilities:
- Conducted the literature survey analyzing 12 contemporary research papers on canine classification.
- Preprocessed the Stanford Dogs / Kaggle dataset into stratified 70/15/15 train, validation, and test splits.
- Executed the automated 18-point verification testing suite (`run_complete_tests.py`) ensuring zero regressions.
- Prepared and proofread the comprehensive B.Tech project report and presentation artifacts.

---
"""
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(report_text)
    print(f"[OK] Generated Markdown Report: {output_path}")

if __name__ == '__main__':
    create_markdown_report('Dog_Breed_Identification_Project_Report.md')
