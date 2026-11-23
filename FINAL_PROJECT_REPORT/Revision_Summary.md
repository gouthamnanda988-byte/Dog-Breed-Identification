# REVISION SUMMARY: DOG BREED IDENTIFICATION PROJECT REPORT

**Course:** Introduction to Data Science for Engineers (2026)  
**Institution:** Indian Institute of Information Technology, Design and Manufacturing, Kancheepuram  
**Document:** Project Report Clean Student Revision Summary  
**Date:** November 23, 2026  

---

## 1. Executive Summary

This final revision has restructured the Dog Breed Identification academic project report into a clean, highly readable, student-written B.Tech project report matching the academic presentation, spacing, and tone of `IDSE3.pdf`. 

All user specifications have been strictly fulfilled:
- **Zero Figures / Images:** All diagrams, flowcharts, architecture schemas, training curves, confusion matrix graphs, and application/dashboard screenshots have been completely removed.
- **Removed List of Figures:** The entire List of Figures has been eliminated, and only the List of Tables is retained.
- **Fixed Encoding Glitches:** Every corrupted character (such as `â€¢`, `â€“`, `â€”`, `Ã—`) has been replaced with clean bullet points, numbered lists, or standard typography.
- **Simplified Chapter 4 (Methodology):** Restructured into eight concise, student-friendly sections (4.1 to 4.8) without pseudocode or unnecessary math.
- **Streamlined Chapter 6 (Experimental Results):** Removed sections 6.3, 6.4, 6.5, and 6.6. Retained only 6.1 (Model Training Progress in text) and 6.2 (Quantitative Evaluation Metrics in a clean table).
- **Rewritten Chapter 7 (Conclusion and Future Enhancements):** Crafted in an authentic B.Tech student voice with 7.1 Conclusion (4 paragraphs), 7.2 Limitations, and 7.3 Future Enhancements.
- **Preserved 12 Literature Survey References:** Maintained all 12 research papers in Chapter 2 and the References section.
- **Enhanced Typography:** Times New Roman, 12 pt body font, 1.5 line spacing, clear headings, and readable tables with cell padding.

---

## 2. Deliverables in `FINAL_REVISED_DOG_BREED_REPORT/`

| File Name | Format | Status | Description |
| :--- | :---: | :---: | :--- |
| `Dog_Breed_Identification_Final_Report.docx` | Word DOCX | Generated | Fully styled, figure-free academic report with readable tables and 12 pt Times New Roman text. |
| `Dog_Breed_Identification_Final_Report.pdf` | PDF | Generated | Clean PDF compiled via ReportLab with dual pagination, running academic headers/footers, and clean vector layout. |
| `Revision_Summary.md` | Markdown | Generated | Detailed audit checklist documenting all structural and textual changes. |

---

## 3. Detailed Audit of Revisions

### 3.1 Title Page
- **Institution:** `INDIAN INSTITUTE OF INFORMATION TECHNOLOGY, DESIGN AND MANUFACTURING, KANCHEEPURAM`
- **Course & Academic Year:** `COURSE: INTRODUCTION TO DATA SCIENCE FOR ENGINEERS` | `ACADEMIC YEAR: 2026`
- **Document Type:** `PROJECT REPORT`
- **Project Title:** `DOG BREED IDENTIFICATION USING DEEP LEARNING AND TRANSFER LEARNING`
- **Team Roster:** Clean table with all four student members (K Goutham Nayak CS24B1081, K Adithya CS24B1091, R Mahesh Rathod CS24B1071, G Vishnu Vardhan CS24B1028).
- **Exclusions:** No Capstone Project text, no subtitle, and no guide/departmental placeholders.

### 3.2 Removal of All Figures and Images
- Removed `Figure 3.1` (Breed distribution bar chart).
- Removed `Figure 4.1` (System architecture diagram).
- Removed `Figure 4.2` (Preprocessing flowchart).
- Removed `Figure 4.3` (Stage 1 detector diagram).
- Removed `Figure 4.4` (Stage 2 classifier diagram).
- Removed `Figure 4.5` (Complete workflow flowchart).
- Removed `Figure 5.1` (Admin dashboard screenshot).
- Removed `Figure 6.1` (Training and validation curves).
- Removed `Figure 6.2` (Confusion matrix chart).
- Deleted the entire **List of Figures** from the Front Matter and Table of Contents.
- Removed all inline references to figures in the text.

### 3.3 Encoding and Character Cleaning
- Purged all corrupted characters (`â€¢`, `â€“`, `â€”`, `Ã—`, etc.).
- Replaced with standard clean bullets (`•`), formatted numbered items (`1.`, `2.`), and standard punctuation.

### 3.4 Simplified Chapter 4 – Methodology
- **4.1 System Overview:** High-level student-written summary of the end-to-end system.
- **4.2 Dataset and Image Input:** Explanation of image upload, formats, and file size checks.
- **4.3 Image Preprocessing:** Four numbered steps (Validation, RGB conversion, 224 x 224 Resizing, Pixel normalization).
- **4.4 MobileNetV2 Model:** Clear explanation of depthwise separable convolutions, inverted residuals, ~3.4M parameters, and ~14 MB size.
- **4.5 Transfer Learning and Model Training:** Phase 1 (frozen base, 10 epochs) and Phase 2 (fine-tuning top 30 layers, 5 epochs) with Table 4.1 layer progression.
- **4.6 Breed Prediction:** Softmax probability generation and Top-3 candidate ranking.
- **4.7 Web Application and Database Integration:** Connection between Flask, UI, model, and MySQL database.
- **4.8 Overall Working Procedure:** Clean 8-step numbered list tracking user upload to database logging.

### 3.5 Streamlined Chapter 6 – Experimental Results
- **Removed Sections:** Completely deleted 6.3 (Explanation of Metrics), 6.4 (Per-breed table & unsupported 100% claims), 6.5 (Confusion matrix analysis), and 6.6 (Automated test suite).
- **6.1 Model Training Progress:** Clear explanation of Phase 1 and Phase 2 training progress in pure paragraphs without charts.
- **6.2 Quantitative Evaluation Metrics:** Clean, readable table (Table 6.1) displaying verified results:
  - Top-1 Test Accuracy: **77.64%**
  - Top-5 Test Accuracy: **96.87%**
  - Test Categorical Cross-Entropy Loss: **0.7036**
  - Macro Average F1-Score: **76.91%**
  - Weighted Average F1-Score: **77.35%**

### 3.6 Chapter 7 – Conclusion and Future Enhancements
- **7.1 Conclusion:** Four cohesive paragraphs summarizing problem, dataset, MobileNetV2 transfer learning, results, Flask/MySQL integration, and student learnings.
- **7.2 Limitations:** Realistic, honest discussion of single-dog assumption, purebred bias, lighting sensitivity, and closely related breeds.
- **7.3 Future Enhancements:** Practical future directions (multi-dog detection with YOLO, mixed-breed ancestry regression, mobile TFLite deployment, expanded breed catalogs).
- **Zero Hype:** Fully purged of promotional buzzwords.

### 3.7 Literature Survey & References
- Preserved all 12 research papers from the literature survey in Chapter 2 and Table 2.1.
- IEEE-style references matching citations in the text.
- Project Team Contribution Details table included at the end.
