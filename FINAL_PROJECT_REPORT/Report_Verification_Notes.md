# REPORT VERIFICATION NOTES & INSTITUTIONAL PLACEHOLDERS
**Project Title:** Dog Breed Identification Using Deep Learning and Transfer Learning  
**Degree:** Bachelor of Technology (B.Tech) in Computer Science and Engineering / Data Science  
**Academic Year:** 2025 – 2026  

---

## 1. PROJECT TEAM DETAILS

| S.No. | Student Candidate Name | Roll Number | Individual Responsibility |
|:---:|---|:---:|---|
| 1 | **K Goutham Nayak** | **CS24B1081** | Backend Architecture, MySQL Database and PDF Reporting |
| 2 | **K Adithya** | **CS24B1091** | Deep Learning Model Architecture and Fine-Tuning |
| 3 | **R Mahesh Rathod** | **CS24B1071** | Two-Stage Canine Presence Detection and Validation |
| 4 | **G Vishnu Vardhan** | **CS24B1028** | Frontend UI/UX, Breed Directory and Trait Comparison |

---

## 2. STRUCTURAL INDEPENDENCE & ORIGINALITY SUMMARY

This report was developed as an original academic thesis specifically tailored to the **Dog Breed Identification** project. While inspired by traditional academic presentation standards (as seen in peer engineering reports):

1. **Original 7-Chapter Organization:** Organized according to the real software and machine learning lifecycle of our canine classification platform:
   - Front Matter (Title Page, Project Specifications, Abstract, Contents, List of Figures, List of Tables)
   - Chapter 1: Introduction (Background, Problem Statement, Motivation, Objectives, Scope, Proposed Approach)
   - Chapter 2: Literature Review (Canine FGVC, CNN Models, Transfer Learning, 12-Paper Survey Table, Gap Analysis, Selection of MobileNetV2)
   - Chapter 3: Dataset and Image Preparation (Stanford Dogs benchmark, 120 Breeds, 70/15/15 Splitting, Normalization, Augmentation, Challenges)
   - Chapter 4: Proposed Methodology (Multi-tier Architecture, Image Validation, Stage 1 Canine Detector, MobileNetV2 Feature Extractor, Two-Phase Fine-Tuning, Head Design, Top-3 Confidence Ranking, Complete Algorithmic Workflow)
   - Chapter 5: Model Development and Web Application (Environment, Training Parameters, Model Integration, Flask Architecture, Drag-and-Drop Uploads, PBKDF2 Authentication, Breed Comparison, Prediction History, MySQL Schema, ReportLab PDF Generation, Admin Dashboard)
   - Chapter 6: Results and Discussion (Training Convergence, Accuracy/Loss Curves, Top-1/Top-5 Accuracies, Precision/Recall/F1, Prediction Examples, Dog/Non-Dog Testing, Confused Breeds Analysis, 18-Point Test Suite, Latency and Memory Observations)
   - Chapter 7: Conclusion and Future Enhancements (Project Summary, Learning Outcomes, Limitations, Future Roadmap)
   - References (18 IEEE-formatted citations)
   - Team Contributions (Detailed individual role breakdown and shared responsibilities)

2. **Strict Exclusions Enforced:**
   - No Bonafide Certificate.
   - No Candidate Declaration.
   - No Student Declaration.
   - No Certificate of Completion.
   - No Acknowledgement.
   - No Faculty or HOD signature pages or approval forms.
   - Starts directly with the Title Page, followed immediately by Project Specifications and Abstract.

3. **Academic Pagination:**
   - Title Page: Suppressed headers, footers, and page numbers.
   - Project Specifications: Numbered 1.
   - Front Matter (Abstract, Contents, Lists): Roman numerals (`i`, `ii`, `iii`, `iv`).
   - Chapters 1 to 7, References, Team Contributions: Arabic numerals (`1`, `2`, `3`...).

---

## 3. VERIFIED TECHNICAL METRICS (FROM WORKSPACE ARTIFACTS)

All quantitative results in the report are taken directly from the project's actual training history, model files, database, and automated test scripts:

| Metric / Dimension | Verified Value | Originating Artifact |
|---|---|---|
| **Total Images in Corpus** | **10,222 images** | `labels.csv` |
| **Total Breed Classes** | **120 classes** | `labels.csv` & `database/breeds_data.json` |
| **Training Partition (70%)** | **7,155 images** | `dataset/splits/train_split.csv` |
| **Validation Partition (15%)** | **1,533 images** | `dataset/splits/val_split.csv` |
| **Testing Partition (15%)** | **1,534 images** | `dataset/splits/test_split.csv` |
| **Top-1 Test Accuracy** | **77.64%** | `model/performance_metrics.json` |
| **Top-5 Test Accuracy** | **96.87%** | `model/performance_metrics.json` |
| **Test Categorical Loss** | **0.7036** | `model/performance_metrics.json` |
| **Macro Average Precision** | **78.58%** | `model/performance_metrics.json` |
| **Macro Average Recall** | **76.98%** | `model/performance_metrics.json` |
| **Macro Average F1-Score** | **76.91%** | `model/performance_metrics.json` |
| **Weighted Average Precision** | **78.75%** | `model/performance_metrics.json` |
| **Weighted Average Recall** | **77.64%** | `model/performance_metrics.json` |
| **Weighted Average F1-Score** | **77.35%** | `model/performance_metrics.json` |
| **Stage 1 Detection Threshold** | **$P(\text{dog}) \ge 0.20$** | `app.py` & `preprocess.py` (118 ImageNet dog classes) |
| **Automated System Tests** | **18 of 18 PASSED (100%)** | `run_complete_tests.py` |
| **Average CPU Inference Latency** | **120 – 160 ms** | Live forward-pass benchmarking |
| **Model Weight Storage Size** | **~14 MB** | `best_model.keras` |

---

## 4. VERIFIED COMMONLY CONFUSED BREED PAIRS

From the evaluation on the 1,534 held-out test images, the top 12 confused pairs verified in `model/performance_metrics.json` are:
1. **Whippet vs. Italian Greyhound:** 7 images (Sighthound posture, identical sleek coat, differing mainly in scale)
2. **Lhasa Apso vs. Shih-Tzu:** 6 images (Closely related Tibetan companion breeds with obscuring facial fur)
3. **Eskimo Dog vs. Siberian Husky:** 5 images (Arctic spitz breeds with erect ears, thick coats, curled tails)
4. **Australian Terrier vs. Silky Terrier:** 4 images (Terrier proportions with similar wiry/silky coats)
5. **Kuvasz vs. Great Pyrenees:** 4 images (Flock-guarding breeds with solid white double coats)
6. **Maltese Dog vs. West Highland White Terrier:** 4 images (Small white companions with similar fur)
7. **Samoyed vs. Great Pyrenees:** 4 images (Large white fluffy breeds)
8. **Staffordshire Bull Terrier vs. American Staffordshire Terrier:** 4 images (Bully head silhouette)
9. **Cardigan Welsh Corgi vs. Pembroke Welsh Corgi:** 3 images (Welsh Corgis differing primarily in tail length)
10. **Collie vs. Shetland Sheepdog:** 3 images (Herding breeds sharing identical facial markings and ruffs)
11. **Irish Wolfhound vs. Scottish Deerhound:** 3 images (Rough-coated sighthounds)
12. **Lakeland Terrier vs. Soft-Coated Wheaten Terrier:** 3 images (Tan bearded terrier profile)

---

## 5. INSTITUTIONAL PLACEHOLDERS TO COMPLETE

The team can customize the following placeholders in `Dog_Breed_Identification_Project_Report.docx`:

| Placeholder Tag | Description | Example / Recommendation |
|---|---|---|
| `[INDIAN INSTITUTE OF INFORMATION TECHNOLOGY / INSTITUTION NAME]` | Full college name | Indian Institute of Information Technology... |
| `[DEPARTMENT OF COMPUTER SCIENCE AND ENGINEERING / DATA SCIENCE]` | Official department name | Department of Computer Science and Engineering |
| `[Faculty Guide Name, Designation]` | Faculty guide's name | Dr. / Prof. [Guide Name], Associate Professor |
| `[Date of Submission]` | Official submission date | April 2026 |
| `[College Location / City]` | Campus city | Kancheepuram / Chennai / Hyderabad |

---

## 6. DELIVERABLES PACKAGE

All four deliverables have been generated and copied to both target directories:
- `C:\Users\gouth\Downloads\DOG BREED IDENTIFICATION\FINAL_PROJECT_REPORT\`
- `C:\Users\gouth\Downloads\FINAL_PROJECT_REPORT\`

Files:
1. **`Dog_Breed_Identification_Project_Report.docx`** (~939 KB) – Fully editable Word document with Times New Roman, 1.5 line spacing, 10 styled tables, 7 embedded high-resolution figures, and 7 chapters.
2. **`Dog_Breed_Identification_Project_Report.pdf`** (~1.1 MB) – Print-ready academic PDF with dual-numbering (Roman front matter, Arabic chapters), running headers/footers, and embedded diagrams.
3. **`Dog_Breed_Identification_Project_Report.md`** (~70 KB) – Clean Markdown source.
4. **`Report_Verification_Notes.md`** (~8 KB) – Verification notes, metrics log, and viva demonstration guide.

---

## 7. COLLEGE REVIEW DEMONSTRATION GUIDE

When presenting the project to examiners:
1. **Explain the Motivation & FGVC Challenge:** Highlight low inter-class variance (Whippet vs Italian Greyhound) and high intra-class variance.
2. **Demonstrate Stage 1 Rejection:** Upload a non-dog photo (`Black-Horse-Names-with-Meanings.jpeg`). Show how the ImageNet filter halts with "No Dog Detected".
3. **Demonstrate Stage 2 Classification & Top-3 Scores:** Upload a genuine dog photo (`dog.jpg`). Show the primary breed match (69.34%) and Top-3 ranked bars.
4. **Showcase Automated PDF Report:** Click "Download Report (PDF)" and show the generated certificate.
5. **Showcase 120-Breed Directory & Comparison:** Open `/breeds` and demonstrate side-by-side comparison.
6. **Showcase Admin Dashboard & Database:** Open `/admin` to display live SQL metrics and the Chart.js top predicted breeds chart.
7. **Highlight Automated Test Verification:** Note that all 18 test cases in `run_complete_tests.py` passed with 100% success.
