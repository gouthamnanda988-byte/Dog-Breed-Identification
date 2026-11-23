"""
generate_docx_report_v2.py
==========================
Generates a professional academic Word (.docx) project report for:
DOG BREED IDENTIFICATION USING DEEP LEARNING AND TRANSFER LEARNING

Features:
- Academic layout inspired by IDSE3.pdf (clean title page, specifications, abstract, contents, list of figures, list of tables)
- Strict exclusion of certificates, declarations, and signature pages
- Times New Roman typography, 1.5 line spacing, clean borders and shaded table headers
- Embedded high-resolution diagrams and screenshots
"""

import os
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def set_cell_background(cell, hex_color):
    tc_pr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>')
    tc_pr.append(shd)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tc_pr = cell._tc.get_or_add_tcPr()
    tc_mar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="{top}" w:type="dxa"/><w:bottom w:w="{bottom}" w:type="dxa"/><w:left w:w="{left}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/></w:tcMar>')
    tc_pr.append(tc_mar)

def create_docx(output_path):
    doc = Document()

    # A4 Page Setup
    section = doc.sections[0]
    section.page_width = Inches(8.27)
    section.page_height = Inches(11.69)
    section.top_margin = Inches(1.0)
    section.bottom_margin = Inches(1.0)
    section.left_margin = Inches(1.0)
    section.right_margin = Inches(1.0)

    # Base Styles
    style_normal = doc.styles['Normal']
    font = style_normal.font
    font.name = 'Times New Roman'
    font.size = Pt(12)
    font.color.rgb = RGBColor(0x22, 0x22, 0x22)
    style_normal.paragraph_format.line_spacing = 1.5
    style_normal.paragraph_format.space_after = Pt(6)
    style_normal.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY

    # Helpers
    def add_p(text, bold_prefix="", space_after=6):
        p = doc.add_paragraph()
        p.paragraph_format.line_spacing = 1.5
        p.paragraph_format.space_after = Pt(space_after)
        p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        if bold_prefix:
            r_bold = p.add_run(bold_prefix)
            r_bold.font.name = 'Times New Roman'
            r_bold.font.size = Pt(12)
            r_bold.bold = True
        r_text = p.add_run(text)
        r_text.font.name = 'Times New Roman'
        r_text.font.size = Pt(12)
        return p

    def add_h1(title):
        h = doc.add_heading(level=1)
        h.paragraph_format.space_before = Pt(18)
        h.paragraph_format.space_after = Pt(8)
        h.paragraph_format.keep_with_next = True
        r = h.add_run(title)
        r.font.name = 'Times New Roman'
        r.font.size = Pt(16)
        r.font.bold = True
        r.font.color.rgb = RGBColor(0x1A, 0x2B, 0x4C)
        return h

    def add_h2(title):
        h = doc.add_heading(level=2)
        h.paragraph_format.space_before = Pt(14)
        h.paragraph_format.space_after = Pt(6)
        h.paragraph_format.keep_with_next = True
        r = h.add_run(title)
        r.font.name = 'Times New Roman'
        r.font.size = Pt(13.5)
        r.font.bold = True
        r.font.color.rgb = RGBColor(0x2A, 0x43, 0x65)
        return h

    def add_h3(title):
        h = doc.add_heading(level=3)
        h.paragraph_format.space_before = Pt(10)
        h.paragraph_format.space_after = Pt(4)
        h.paragraph_format.keep_with_next = True
        r = h.add_run(title)
        r.font.name = 'Times New Roman'
        r.font.size = Pt(12)
        r.font.bold = True
        r.font.color.rgb = RGBColor(0x31, 0x54, 0x7A)
        return h

    def add_fig(img_path, caption, width=Inches(6.0)):
        if os.path.exists(img_path):
            p_img = doc.add_paragraph()
            p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_img.paragraph_format.space_before = Pt(10)
            p_img.paragraph_format.space_after = Pt(4)
            p_img.add_run().add_picture(img_path, width=width)
            
            p_cap = doc.add_paragraph()
            p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_cap.paragraph_format.space_after = Pt(12)
            r = p_cap.add_run(caption)
            r.font.name = 'Times New Roman'
            r.font.size = Pt(10)
            r.italic = True
            r.font.color.rgb = RGBColor(0x44, 0x44, 0x44)

    # =========================================================================
    # 1. TITLE / COVER PAGE (Academic layout matching IDSE3.pdf style)
    # =========================================================================
    p_inst = doc.add_paragraph()
    p_inst.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_inst.paragraph_format.space_before = Pt(20)
    p_inst.paragraph_format.space_after = Pt(4)
    r = p_inst.add_run("[INDIAN INSTITUTE OF INFORMATION TECHNOLOGY / INSTITUTION NAME]\n"
                       "[DEPARTMENT OF COMPUTER SCIENCE AND ENGINEERING / DATA SCIENCE]")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(14)
    r.bold = True

    p_acad = doc.add_paragraph()
    p_acad.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_acad.paragraph_format.space_after = Pt(24)
    r = p_acad.add_run("B.Tech 3rd Year / Final Year – Academic Year 2025–2026\n"
                       "INTRODUCTION TO DATA SCIENCE FOR ENGINEERS / CAPSTONE PROJECT REPORT")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(11)
    r.font.color.rgb = RGBColor(0x1A, 0x52, 0x76)
    r.bold = True

    # Divider Line
    p_div = doc.add_paragraph()
    p_div.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_div.paragraph_format.space_after = Pt(20)
    r = p_div.add_run("______________________________________________________________________")
    r.font.color.rgb = RGBColor(0x7F, 0x8C, 0x8D)

    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_after = Pt(12)
    r = p_title.add_run("DOG BREED IDENTIFICATION USING DEEP LEARNING AND TRANSFER LEARNING")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(20)
    r.bold = True
    r.font.color.rgb = RGBColor(0x1A, 0x2B, 0x4C)

    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_sub.paragraph_format.space_after = Pt(36)
    r = p_sub.add_run("An End-to-End Fine-Grained Canine Classification System Utilizing MobileNetV2,\n"
                      "Two-Stage Image Validation, and a Full-Stack Web Platform")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(12)
    r.italic = True

    p_by = doc.add_paragraph()
    p_by.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_by.paragraph_format.space_after = Pt(8)
    r = p_by.add_run("PROJECT TEAM MEMBERS")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(13)
    r.bold = True

    # Student Table on Cover Page (exactly as IDSE3.pdf)
    t_team = doc.add_table(rows=5, cols=4)
    t_team.alignment = WD_TABLE_ALIGNMENT.CENTER
    team_data = [
        ("S.No.", "Name", "Roll Number", "Responsibility"),
        ("1", "K Goutham Nayak", "CS24B1081", "Backend Architecture, MySQL Database and PDF Reporting"),
        ("2", "K Adithya", "CS24B1091", "Deep Learning Model Architecture and Fine-Tuning"),
        ("3", "R Mahesh Rathod", "CS24B1071", "Two-Stage Canine Presence Detection and Validation"),
        ("4", "G Vishnu Vardhan", "CS24B1028", "Frontend UI/UX, Breed Directory and Trait Comparison")
    ]
    col_widths = [Inches(0.6), Inches(1.8), Inches(1.3), Inches(2.8)]
    for row_idx, row_vals in enumerate(team_data):
        row = t_team.rows[row_idx]
        for c_idx, val in enumerate(row_vals):
            cell = row.cells[c_idx]
            cell.width = col_widths[c_idx]
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER if c_idx < 3 else WD_ALIGN_PARAGRAPH.LEFT
            r = p.add_run(val)
            r.font.name = 'Times New Roman'
            r.font.size = Pt(10)
            if row_idx == 0:
                r.bold = True
                set_cell_background(cell, "EAECEE")
            set_cell_margins(cell, 60, 60, 80, 80)

    p_guide = doc.add_paragraph()
    p_guide.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_guide.paragraph_format.space_before = Pt(36)
    p_guide.paragraph_format.space_after = Pt(2)
    r = p_guide.add_run("Under the Guidance of: [Faculty Guide Name, Designation]")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(11)
    r.bold = True

    p_guide_dept = doc.add_paragraph()
    p_guide_dept.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_guide_dept.paragraph_format.space_after = Pt(0)
    r = p_guide_dept.add_run("[Department of Computer Science and Engineering / Data Science]\n"
                             "[Institution / College Name, Affiliated to University Name]\n"
                             "Academic Year: 2025 – 2026")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(11)

    doc.add_page_break()

    # =========================================================================
    # 2. PROJECT SPECIFICATIONS (Page 2, matching IDSE3.pdf)
    # =========================================================================
    add_h1("PROJECT SPECIFICATIONS")
    
    specs = [
        ("Course", "Introduction to Data Science for Engineers / Capstone Project"),
        ("Academic Degree", "Bachelor of Technology (B.Tech) in Computer Science / Data Science"),
        ("Core Deep Learning Model", "MobileNetV2 with Inverted Residuals and Linear Bottlenecks"),
        ("Transfer Learning Source", "ImageNet Pretrained Weights (1.4M images, 1,000 classes)"),
        ("Benchmark Dataset", "Stanford Dogs / Kaggle Dog Breed Identification"),
        ("Total Photographic Images", "10,222 labeled JPEG photographs"),
        ("Canine Breed Classes", "120 purebred domestic dog varieties"),
        ("Input Image Resolution", "224 × 224 pixels (3-channel RGB)"),
        ("Inference Pipeline", "Two-Stage Architecture (Stage 1: Canine Filter; Stage 2: Breed Classifier)"),
        ("Web Application Framework", "Python Flask 3.0 (REST APIs, Session Management, Jinja2)"),
        ("Database Management", "MySQL 8.0 Server (dog_breed_db with 4 relational tables)"),
        ("Reporting Engine", "Python ReportLab 5.1 (Dynamic PDF prediction certificate generation)"),
        ("Top-1 Test Accuracy", "77.64% (on 1,534 held-out evaluation test images)"),
        ("Top-5 Test Accuracy", "96.87% (on 1,534 held-out evaluation test images)"),
        ("Average Inference Latency", "120 to 160 milliseconds per image on standard CPU"),
        ("Model Weight Storage Size", "~14 MB (best_model.keras)")
    ]

    t_specs = doc.add_table(rows=len(specs), cols=2)
    t_specs.alignment = WD_TABLE_ALIGNMENT.CENTER
    for idx, (k, v) in enumerate(specs):
        row = t_specs.rows[idx]
        row.cells[0].width = Inches(2.5)
        row.cells[1].width = Inches(4.0)
        p1 = row.cells[0].paragraphs[0]
        p2 = row.cells[1].paragraphs[0]
        p1.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p2.alignment = WD_ALIGN_PARAGRAPH.LEFT
        
        r1 = p1.add_run(k)
        r2 = p2.add_run(v)
        r1.font.name = 'Times New Roman'
        r2.font.name = 'Times New Roman'
        r1.font.size = Pt(11)
        r2.font.size = Pt(11)
        r1.bold = True
        set_cell_margins(row.cells[0], 60, 60, 100, 100)
        set_cell_margins(row.cells[1], 60, 60, 100, 100)
        if idx % 2 == 1:
            set_cell_background(row.cells[0], "F8F9FA")
            set_cell_background(row.cells[1], "F8F9FA")

    doc.add_page_break()

    # =========================================================================
    # 3. ABSTRACT (Page 3)
    # =========================================================================
    add_h1("Abstract")
    add_p("Domestic canines (Canis lupus familiaris) represent the most morphologically diverse mammal on Earth, encompassing hundreds of purebred varieties characterized by subtle variations in cranial geometry, ear carriage, muzzle length, coat pigmentation, and grooming profiles. Automatically classifying dog breeds from digital photographs is a quintessential challenge in Fine-Grained Visual Categorization (FGVC). Unlike coarse-grained object detection where classes exhibit distinct silhouettes (such as distinguishing a vehicle from a dog), fine-grained canine classification must resolve two competing computer vision difficulties: low inter-class variance, where biologically related breeds exhibit virtually identical physical appearances (for instance, Whippets and Italian Greyhounds, or Lhasa Apsos and Shih-Tzus), and high intra-class variance, where dogs of the same breed differ markedly across coat patterns, colors, age, body postures, and photographic lighting.")

    add_p("In this project, we designed, implemented, and thoroughly evaluated an end-to-end canine identification platform utilizing transfer learning with MobileNetV2 and backed by a full-stack relational web architecture. Using the benchmark Stanford Dogs / Kaggle Dog Breed dataset comprising 10,222 labeled photographs across 120 purebred categories, we established a stratified 70% training (7,155 images), 15% validation (1,533 images), and 15% testing (1,534 images) partition.")

    add_p("To resolve a pervasive limitation in existing classification systems—where non-dog inputs are arbitrarily forced into canine classes—we formulated an innovative two-stage prediction pipeline. In Stage 1, an upstream ImageNet-pretrained MobileNetV2 network evaluates whether an uploaded photograph contains a canine by monitoring 118 domestic and wild dog output categories, rejecting non-dog uploads (such as horses, felines, or vehicles) when the cumulative canine probability falls below 0.20. In Stage 2, verified canine images are classified by our fine-tuned MobileNetV2 architecture equipped with Global Average Pooling, 30% dropout regularization, and a 120-unit Softmax output layer.")

    add_p("Experimental evaluation on the 1,534 held-out test images demonstrated a Top-1 test accuracy of 77.64%, an exceptional Top-5 test accuracy of 96.87%, a test categorical cross-entropy loss of 0.7036, and a macro F1-score of 76.91%. On consumer CPU hardware, a complete forward pass completes in 120 to 160 milliseconds with a compact model weight footprint of 14 MB.")

    add_p("Beyond model development, we engineered a complete web platform using Python Flask and MySQL. The application provides drag-and-drop image uploads, Top-3 ranked candidate scores with animated confidence bars, an interactive 120-breed directory with trait comparison, automated PDF report downloads via ReportLab, personal prediction histories, and an administrative analytics dashboard. The completed system was verified using an automated 18-point testing suite, with all tests passing successfully.")

    p_kw = add_p("Dog Breed Identification, Deep Learning, Transfer Learning, MobileNetV2, Fine-Grained Visual Categorization, Computer Vision, Flask, MySQL, ReportLab.", bold_prefix="Keywords: ")
    p_kw.paragraph_format.space_before = Pt(12)

    doc.add_page_break()

    # =========================================================================
    # 4. CONTENTS (Table of Contents)
    # =========================================================================
    add_h1("Contents")
    toc_data = [
        ("Project Specifications", "1"),
        ("Abstract", "i"),
        ("List of Figures", "iii"),
        ("List of Tables", "iv"),
        ("Chapter 1 – Introduction", "1"),
        ("    Background of Dog Breed Identification", "1"),
        ("    Problem Statement", "1"),
        ("    Motivation", "2"),
        ("    Objectives", "2"),
        ("    Scope", "3"),
        ("    Proposed Approach", "3"),
        ("Chapter 2 – Literature Review", "4"),
        ("    Research on Dog Breed Classification", "4"),
        ("    CNN-Based Classification", "4"),
        ("    Transfer Learning Approaches", "4"),
        ("    Comparison of Existing Research", "5"),
        ("    Research Gap", "6"),
        ("    Selection of MobileNetV2", "7"),
        ("Chapter 3 – Dataset and Image Preparation", "8"),
        ("    Stanford Dogs Dataset", "8"),
        ("    Breed Categories", "8"),
        ("    Dataset Organization", "8"),
        ("    Training, Validation and Testing Split", "9"),
        ("    Image Resizing and Normalization", "9"),
        ("    Data Augmentation", "10"),
        ("    Dataset Challenges", "10"),
        ("Chapter 4 – Proposed Methodology", "11"),
        ("    Overall System Architecture", "11"),
        ("    Image Input and Validation", "11"),
        ("    Dog Presence Verification", "12"),
        ("    MobileNetV2 Feature Extraction", "13"),
        ("    Transfer Learning and Fine-Tuning", "13"),
        ("    Breed Classification", "14"),
        ("    Prediction Confidence and Top-3 Results", "14"),
        ("    Complete Prediction Workflow", "15"),
        ("Chapter 5 – Model Development and Web Application", "16"),
        ("    Development Environment", "16"),
        ("    Model Training", "16"),
        ("    Model Integration", "17"),
        ("    Flask Application Architecture", "17"),
        ("    Image Upload and Prediction", "18"),
        ("    User Authentication", "18"),
        ("    Breed Information and Trait Comparison", "18"),
        ("    Prediction History", "19"),
        ("    Database Design", "19"),
        ("    Other Implemented Features", "20"),
        ("Chapter 6 – Results and Discussion", "21"),
        ("    Training and Validation Performance", "21"),
        ("    Accuracy and Loss", "21"),
        ("    Top-1 and Top-5 Accuracy", "22"),
        ("    Precision, Recall and F1-Score", "22"),
        ("    Prediction Examples", "23"),
        ("    Dog and Non-Dog Image Testing", "23"),
        ("    Commonly Confused Breeds", "24"),
        ("    Application Testing", "25"),
        ("    Observations", "26"),
        ("Chapter 7 – Conclusion and Future Enhancements", "27"),
        ("    Project Summary", "27"),
        ("    Learning Outcomes", "27"),
        ("    Limitations", "28"),
        ("    Future Improvements", "28"),
        ("References", "29"),
        ("Team Contributions", "31")
    ]
    t_toc = doc.add_table(rows=len(toc_data), cols=2)
    t_toc.alignment = WD_TABLE_ALIGNMENT.CENTER
    for idx, (title, page_num) in enumerate(toc_data):
        row = t_toc.rows[idx]
        row.cells[0].width = Inches(5.5)
        row.cells[1].width = Inches(1.0)
        p1 = row.cells[0].paragraphs[0]
        p2 = row.cells[1].paragraphs[0]
        p1.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p2.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        r1 = p1.add_run(title)
        r2 = p2.add_run(page_num)
        r1.font.name = 'Times New Roman'
        r2.font.name = 'Times New Roman'
        r1.font.size = Pt(11)
        r2.font.size = Pt(11)
        if "Chapter" in title or "Abstract" in title or "Specifications" in title or "References" in title or "Team" in title or "List" in title:
            r1.bold = True
            r2.bold = True
        set_cell_margins(row.cells[0], 20, 20, 40, 40)
        set_cell_margins(row.cells[1], 20, 20, 40, 40)

    doc.add_page_break()

    # =========================================================================
    # 5. LIST OF FIGURES & LIST OF TABLES (Pages 5 & 6)
    # =========================================================================
    add_h1("List of Figures")
    figs = [
        ("Figure 3.1", "Sample Distribution Across 120 Dog Breeds in the Stanford Dogs Dataset", "10"),
        ("Figure 4.1", "Overall Multi-Tier System Architecture of the Dog Breed Identification Platform", "11"),
        ("Figure 4.2", "Two-Stage Canine Detection and Fine-Grained Breed Classification Workflow", "12"),
        ("Figure 4.3", "Transfer Learning Neural Network Architecture with MobileNetV2 Backbone", "13"),
        ("Figure 5.1", "Administrative Dashboard Interface Displaying Real-Time Database Metrics and Top Breeds", "20"),
        ("Figure 6.1", "Training and Validation Accuracy and Loss Curves Across 15 Epochs", "21"),
        ("Figure 6.2", "Top 12 Most Frequently Confused Dog Breed Pairs in Evaluation Set", "24")
    ]
    t_fig = doc.add_table(rows=len(figs), cols=3)
    t_fig.alignment = WD_TABLE_ALIGNMENT.CENTER
    for idx, (num, desc, pg) in enumerate(figs):
        row = t_fig.rows[idx]
        row.cells[0].width = Inches(1.2)
        row.cells[1].width = Inches(4.5)
        row.cells[2].width = Inches(0.8)
        p0 = row.cells[0].paragraphs[0]
        p1 = row.cells[1].paragraphs[0]
        p2 = row.cells[2].paragraphs[0]
        p0.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p1.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p2.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        r0 = p0.add_run(num)
        r1 = p1.add_run(desc)
        r2 = p2.add_run(pg)
        for r in [r0, r1, r2]:
            r.font.name = 'Times New Roman'
            r.font.size = Pt(11)
        r0.bold = True
        set_cell_margins(row.cells[0], 25, 25, 40, 40)
        set_cell_margins(row.cells[1], 25, 25, 40, 40)
        set_cell_margins(row.cells[2], 25, 25, 40, 40)

    doc.add_page_break()

    add_h1("List of Tables")
    tables_list = [
        ("Table 1.1", "Comparison Between Conventional Identification and Proposed System", "3"),
        ("Table 2.1", "Structured Comparison of Existing Research on Canine Breed Classification", "5"),
        ("Table 3.1", "Dataset Partitioning into Training, Validation, and Testing Sets", "9"),
        ("Table 4.1", "Neural Network Layer Progression and Parameter Distribution", "13"),
        ("Table 5.1", "Model Training Hyperparameter Configuration", "16"),
        ("Table 5.2", "Relational Database Schema Design (dog_breed_db)", "19"),
        ("Table 5.3", "Core Software Technologies and Functional Roles", "17"),
        ("Table 6.1", "Model Performance Metrics on Held-Out Test Set (1,534 Images)", "22"),
        ("Table 6.2", "Top 12 Most Frequently Confused Dog Breed Pairs with Visual Reasons", "24"),
        ("Table 6.3", "Complete 18-Point Automated Application Test Suite Verification", "25")
    ]
    t_tbl = doc.add_table(rows=len(tables_list), cols=3)
    t_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    for idx, (num, desc, pg) in enumerate(tables_list):
        row = t_tbl.rows[idx]
        row.cells[0].width = Inches(1.2)
        row.cells[1].width = Inches(4.5)
        row.cells[2].width = Inches(0.8)
        p0 = row.cells[0].paragraphs[0]
        p1 = row.cells[1].paragraphs[0]
        p2 = row.cells[2].paragraphs[0]
        p0.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p1.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p2.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        r0 = p0.add_run(num)
        r1 = p1.add_run(desc)
        r2 = p2.add_run(pg)
        for r in [r0, r1, r2]:
            r.font.name = 'Times New Roman'
            r.font.size = Pt(11)
        r0.bold = True
        set_cell_margins(row.cells[0], 25, 25, 40, 40)
        set_cell_margins(row.cells[1], 25, 25, 40, 40)
        set_cell_margins(row.cells[2], 25, 25, 40, 40)

    doc.add_page_break()

    # =========================================================================
    # CHAPTER 1 – INTRODUCTION
    # =========================================================================
    add_h1("Chapter 1 – Introduction")
    
    add_h2("Background of Dog Breed Identification")
    add_p("Computer vision has experienced extraordinary progress over the past decade through the emergence of deep Convolutional Neural Networks (CNNs). In traditional object recognition tasks, models are tasked with discriminating between broad object categories that possess fundamentally distinct shapes, edges, and silhouettes—such as separating a car from an airplane, or an animal from a building.")
    add_p("In contrast, canine breed classification belongs to the specialized and challenging domain of Fine-Grained Visual Categorization (FGVC). Canines belong to the same biological species (Canis lupus familiaris), yet selective breeding practiced by humans over hundreds of years has produced more than 300 globally recognized domestic breeds. These breeds display remarkable morphological diversity: they range from miniature toy lapdogs like the Chihuahua (weighing under 2 kg) to giant draft and guard dogs like the Saint Bernard and Mastiff (weighing over 80 kg).")
    add_p("Developing an automated system capable of recognizing 120 distinct breeds directly from user photographs requires a neural network to look beyond coarse silhouettes and learn subtle, discriminative anatomical markers—such as the curl of a tail, muzzle-to-skull proportions, ear posture, coat texture, and facial pigmentation patterns.")

    add_h2("Problem Statement")
    add_p("Accurately determining a dog's breed from an unconstrained digital photograph is notoriously difficult, even for experienced canine professionals, veterinarians, and animal shelter intake officers. The primary challenges include:")
    add_p("1. Low Inter-Class Variance: Biologically related breeds often look almost identical to the human eye. For example, a Whippet and an Italian Greyhound share an identical aerodynamic sighthound posture and sleek short coat, differing primarily in physical scale that cannot be measured from a 2D photograph lacking reference objects. Similarly, a Lhasa Apso and a Shih-Tzu both feature long, flowing facial fur that completely conceals underlying facial bone structure.")
    add_p("2. High Intra-Class Variance: Canines of the same recognized purebred breed display substantial variations in fur color morphs, coat trimming styles, age, facial expressions, and body weight.")
    add_p("3. Unconstrained Photographic Conditions: Real-world photographs submitted by users often feature poor illumination, cluttered domestic or outdoor backgrounds, partial occlusions by humans or furniture, and non-standard camera angles.")
    add_p("4. The Non-Dog False Prediction Problem: A significant flaw in existing classification systems is their closed-world assumption: if a user uploads a photograph of a horse, a cat, or a car, a single-stage 120-class classifier will forcefully output one of the 120 dog breeds with arbitrary confidence.")
    add_p("An automated, reliable, and user-friendly system is required that can first verify whether a photograph contains a dog, and then accurately identify the breed with ranked probability scores and detailed breed profiles.")

    add_h2("Motivation")
    add_p("The motivation behind this project is driven by both practical real-world utility and academic learning:")
    add_p("• Veterinary Medicine and Animal Shelters: Animal welfare organizations and veterinary clinics frequently need to determine a dog's breed to anticipate hereditary health vulnerabilities (such as gastric torsion in deep-chested breeds, hip dysplasia in German Shepherds, or respiratory distress in brachycephalic dogs like French Bulldogs).")
    add_p("• Lost and Found Animal Recovery: In municipal animal shelters, correctly identifying a lost pet's breed accelerates matching with owner lost-pet reports and adoption records.")
    add_p("• Academic Exploration of Transfer Learning: As B.Tech Data Science students, fine-grained canine classification provided an ideal capstone project to investigate transfer learning, mitigate overfitting on small datasets, design multi-tier web applications, and implement relational database architectures.")

    add_h2("Objectives")
    add_p("The primary objectives of this project are:")
    add_p("1. Prepare and preprocess the Stanford Dogs benchmark dataset across 120 breeds.")
    add_p("2. Build an upstream Stage 1 canine presence filter utilizing ImageNet MobileNetV2 to reject non-dog uploads.")
    add_p("3. Fine-tune a lightweight MobileNetV2 architecture for 120-breed classification using a two-phase training procedure.")
    add_p("4. Extract and present ranked Top-3 candidate predictions with animated confidence bars.")
    add_p("5. Construct a responsive, modern web portal using Python Flask and cream-and-brown styled CSS.")
    add_p("6. Implement a persistent MySQL relational database storing user accounts, prediction history, favorites, and feedback.")
    add_p("7. Develop dynamic PDF prediction report generation using Python ReportLab.")
    add_p("8. Integrate an interactive 120-breed directory and side-by-side trait comparison tool.")
    add_p("9. Build an administrative analytics dashboard computing real-time SQL aggregates.")
    add_p("10. Validate system stability through an automated 18-point testing suite.")

    add_h2("Scope")
    add_p("The functional scope of this project is defined as follows:")
    add_p("• Target Categories: 120 recognized purebred dog breeds as defined by the Stanford Dogs benchmark.")
    add_p("• Input Modality: Single-subject canine photographs in JPG, JPEG, or PNG formats up to 10 MB in file size.")
    add_p("• Core Processing: 224 x 224 RGB image normalization and inference via TensorFlow / Keras MobileNetV2.")
    add_p("• Web Interface: Cross-browser responsive web application accessible on desktop, tablet, and mobile viewport widths.")
    add_p("• System Boundaries: The current system is designed for single-dog photographs and does not support multi-dog instance segmentation or mixed-breed genetic percentage estimation.")

    add_h2("Proposed Approach")
    add_p("Our proposed approach addresses the limitations of conventional and command-line identification systems by coupling deep learning transfer learning with a multi-tier web architecture:")

    # Table 1.1
    p_tcap = doc.add_paragraph()
    p_tcap.paragraph_format.space_before = Pt(8)
    p_tcap.paragraph_format.space_after = Pt(2)
    r = p_tcap.add_run("Table 1.1: Comparison Between Conventional Identification and Proposed System")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(11)
    r.bold = True

    t_comp = doc.add_table(rows=8, cols=3)
    t_comp.alignment = WD_TABLE_ALIGNMENT.CENTER
    comp_headers = ["Feature / Dimension", "Conventional / Existing Systems", "Our Proposed Implementation"]
    comp_rows = [
        ("Identification Method", "Manual visual inspection using kennel books or memory", "Automated two-stage deep learning inference pipeline"),
        ("Speed and Accessibility", "Slow, subjective, requires domain expertise", "Instant inference (<150 ms per image) accessible via web browser"),
        ("Non-Dog Input Handling", "Typically produces a false positive dog prediction", "Stage 1 ImageNet filter validates canine presence and rejects non-dogs"),
        ("Model Architecture", "Heavy models (VGG16, ResNet50) requiring dedicated GPUs", "Lightweight MobileNetV2 (~3.5M parameters) optimized for CPU deployment"),
        ("Output Information", "Single hard predicted label", "Primary breed match, confidence percentage, and ranked Top-3 alternatives"),
        ("Data Persistence", "Stateless or desktop command-line scripts", "Persistent MySQL database tracking individual user history and feedback"),
        ("Reporting", "Manual screenshotting or logging", "One-click automated PDF prediction report generation via ReportLab")
    ]
    for c_idx, h_text in enumerate(comp_headers):
        cell = t_comp.rows[0].cells[c_idx]
        cell.paragraphs[0].text = h_text
        cell.paragraphs[0].runs[0].bold = True
        set_cell_background(cell, "EAECEE")
        set_cell_margins(cell, 60, 60, 80, 80)
    for r_idx, (f1, f2, f3) in enumerate(comp_rows):
        row = t_comp.rows[r_idx + 1]
        for c_idx, val in enumerate([f1, f2, f3]):
            cell = row.cells[c_idx]
            cell.paragraphs[0].text = val
            set_cell_margins(cell, 50, 50, 70, 70)
            if r_idx % 2 == 1:
                set_cell_background(cell, "F8F9FA")

    doc.add_page_break()

    # =========================================================================
    # CHAPTER 2 – LITERATURE REVIEW
    # =========================================================================
    add_h1("Chapter 2 – Literature Review")
    
    add_h2("Research on Dog Breed Classification")
    add_p("Research in automated animal identification has transitioned from classical hand-crafted feature extractors (such as SIFT, HOG, and color histograms) to deep convolutional neural networks. Early approaches struggled with canine classification because coat patterns and lighting variations caused high intra-class variance that manual mathematical descriptors could not effectively capture.")

    add_h2("CNN-Based Classification")
    add_p("Convolutional Neural Networks transformed the field by learning hierarchical feature representations directly from raw pixels. The initial convolutional layers learn low-level primitives like edges, lines, and color gradients; intermediate layers combine these into textures and ear or eye contours; and deeper layers synthesize full facial and body representations. However, training a deep CNN entirely from scratch on 120 dog breeds requires hundreds of thousands of labeled images, which are rarely available for specialized fine-grained domains.")

    add_h2("Transfer Learning Approaches")
    add_p("Transfer learning addresses data scarcity by taking a network pre-trained on a massive visual corpus—most notably ImageNet, which contains 1.4 million images across 1,000 diverse categories—and transferring its learned feature representations to a target domain. Because ImageNet already includes 118 classes of domestic dogs and wild canids, its pre-trained convolutional filters already possess specialized knowledge of fur textures, canine ear structures, and facial geometry.")

    add_h2("Comparison of Existing Research")
    add_p("We conducted a comprehensive literature survey examining twelve recent peer-reviewed research papers focusing on canine breed recognition, transfer learning, and out-of-distribution detection:")

    # Table 2.1
    p_tcap = doc.add_paragraph()
    p_tcap.paragraph_format.space_before = Pt(8)
    p_tcap.paragraph_format.space_after = Pt(2)
    r = p_tcap.add_run("Table 2.1: Structured Comparison of Existing Research on Canine Breed Classification")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(11)
    r.bold = True

    t_lit = doc.add_table(rows=13, cols=6)
    t_lit.alignment = WD_TABLE_ALIGNMENT.CENTER
    lit_headers = ["Paper & Authors", "Year", "Model / Technique", "Dataset Used", "Reported Result", "Key Limitation Observed"]
    lit_data = [
        ("Selvaraj et al.", "2023", "ResNet50 Transfer Learning", "Stanford Dogs (10,222 images)", "93.0% Accuracy", "High compute cost; 120 breeds only"),
        ("Borwarnginn et al.", "2021", "NASNet + Face Cropping", "Columbia Dogs (8,111 images)", "89.92% Accuracy", "Fails if facial crop fails"),
        ("Bokhari et al.", "2022", "MobileNetV2 Feature Extractor", "Stanford Dogs (120 breeds)", "85% (50 cl.) / 64% (120 cl.)", "Steep drop on scaling to 120 classes"),
        ("Kumaravel et al.", "2023", "DenseNet201 + Augmentation", "Stanford + Kaggle (120k aug)", "87.34% Accuracy", "Diminishing returns beyond saturation"),
        ("Banakar et al.", "2023", "VGG-19 + Client/Server", "Stanford Dogs (120 breeds)", "High fine-tuned accuracy", "Bulky model weights (~550 MB)"),
        ("Valarmathi et al.", "2023", "Hybrid InceptionV3 + Xception", "Stanford Dogs (10,222 images)", "92.4% Val Acc (98.4% Train)", "Massive compute cost; slow inference"),
        ("Basha et al.", "2021", "VGG16 in PyTorch", "Canine breed image set", "CNN representation verified", "Vulnerable to lighting and pose shifts"),
        ("Hussain et al.", "2025", "InceptionV3 + Background Rem.", "Stanford Dogs (20,580 images)", "91.2% Accuracy", "Segmentation clips anatomical edges"),
        ("Ghotra et al.", "2023", "MobileNetV2 + Flask + Ngrok", "Kaggle Dog Breeds (>10,222)", "99.89% Train Accuracy", "High overfitting risk; no non-dog check"),
        ("Bankar et al.", "2025", "CNN + Facial Keypoint Hub", "Online set (8,350 images)", "90% Train / 70% Test", "Severe 20% overfitting gap"),
        ("Zou et al.", "2020", "WS-DAN, TBMSL-Net, PMG", "Tsinghua Dogs (70,428 images)", "WS-DAN: 86.4%, TBMSL: 83.7%", "Complex multi-stage attention networks"),
        ("Perera & Patel", "2019", "Deep Novelty Detection", "Stanford Dogs + Multi-dataset", "AUC: 0.825, Acc: 80.1%", "Sensitive to activation thresholds")
    ]
    for c_idx, h_text in enumerate(lit_headers):
        cell = t_lit.rows[0].cells[c_idx]
        cell.paragraphs[0].text = h_text
        cell.paragraphs[0].runs[0].bold = True
        set_cell_background(cell, "EAECEE")
        set_cell_margins(cell, 60, 60, 60, 60)
    for r_idx, row_vals in enumerate(lit_data):
        row = t_lit.rows[r_idx + 1]
        for c_idx, val in enumerate(row_vals):
            cell = row.cells[c_idx]
            cell.paragraphs[0].text = val
            set_cell_margins(cell, 40, 40, 50, 50)
            if r_idx % 2 == 1:
                set_cell_background(cell, "F8F9FA")

    add_h2("Research Gap")
    add_p("Our comparative analysis revealed four critical shortcomings across the surveyed research:")
    add_p("1. Absence of Out-of-Distribution Validation: All surveyed web applications assume the user will only upload valid dog photographs. If a user uploads an image of a cat, horse, or car, these systems return a false canine breed prediction with high confidence.")
    add_p("2. Computational Footprint vs. Speed Trade-Off: Heavy ensemble architectures (Valarmathi et al.) and deep networks (Banakar et al.) achieve high accuracy but require dedicated GPU acceleration and take 1.5–3 seconds per image. Conversely, basic MobileNet implementations (Bokhari et al.) suffered a sharp accuracy collapse (64%) when scaled to 120 breeds without fine-tuning.")
    add_p("3. Lack of Uncertainty Transparency: Almost all implementations output a single hard class label. In fine-grained classification where breeds look nearly identical, concealing the model's alternative predictions hides important uncertainty from users.")
    add_p("4. Lack of Full-Stack Data Management: Prior works operated primarily as standalone machine learning scripts without user authentication, database persistence, or dynamic reporting.")

    add_h2("Selection of MobileNetV2")
    add_p("To overcome these gaps, we selected MobileNetV2 as our core neural backbone. MobileNetV2 is specifically designed for high-efficiency mobile and edge vision applications through its innovative Inverted Residuals and Linear Bottlenecks:")
    add_p("- Standard convolutional layers apply spatial filtering and channel transformation simultaneously, requiring huge parameter matrices.")
    add_p("- MobileNetV2 splits this operation into a 1x1 expansion convolution (increasing channels by an expansion factor t=6), a 3x3 depthwise convolution (applying spatial filtering independently on each channel), and a 1x1 pointwise linear projection (compressing channels without non-linear ReLU distortion).")
    add_p("- This architecture requires only ~3.5 million parameters, resulting in a trained model file of just ~14 MB. On a standard multi-core CPU, MobileNetV2 executes a forward pass in under 150 milliseconds, making it ideal for interactive web serving without needing a costly dedicated GPU.")

    doc.add_page_break()

    # =========================================================================
    # CHAPTER 3 – DATASET AND IMAGE PREPARATION
    # =========================================================================
    add_h1("Chapter 3 – Dataset and Image Preparation")
    
    add_h2("Stanford Dogs Dataset")
    add_p("Our project utilizes the widely respected Stanford Dogs / Kaggle Dog Breed Identification dataset. Originally compiled by Aditya Khosla et al. at Stanford University from ImageNet, the dataset consists of 10,222 labeled photographs covering 120 recognized purebred dog breeds. The photographs were taken under natural, unconstrained real-world conditions, encompassing varied domestic living rooms, outdoor parks, diverse focal distances, and natural canine activities.")

    add_h2("Breed Categories")
    add_p("The 120 canine categories represent a broad cross-section of global kennel classifications, including:")
    add_p("• Toy Companions: Chihuahua, Pomeranian, Maltese Dog, Shih-Tzu, Pug, Yorkshire Terrier.")
    add_p("• Working & Herding Breeds: German Shepherd, Collie, Border Collie, Rottweiler, Bernese Mountain Dog, Great Dane.")
    add_p("• Sporting & Retrievers: Golden Retriever, Labrador Retriever, Cocker Spaniel, Irish Setter.")
    add_p("• Hounds & Sighthounds: Beagle, Bloodhound, Basset Hound, Whippet, Afghan Hound, Saluki.")
    add_p("• Terriers: Scottish Terrier, Bull Terrier, Airedale Terrier, Kerry Blue Terrier.")

    add_h2("Dataset Organization")
    add_p("The dataset is structured around an image directory containing 10,222 JPEG files named by unique 32-character hexadecimal identifiers, paired with labels.csv mapping each ID to its ground-truth breed. File headers were verified using JPEG magic bytes (0xFFD8), confirming 100% data integrity across all 10,222 files.")

    add_h2("Training, Validation and Testing Split")
    add_p("To ensure unbiased academic evaluation, we partitioned the 10,222 images using a stratified 70% / 15% / 15% split governed by a fixed random seed (seed = 42):")

    # Table 3.1
    p_tcap = doc.add_paragraph()
    p_tcap.paragraph_format.space_before = Pt(8)
    p_tcap.paragraph_format.space_after = Pt(2)
    r = p_tcap.add_run("Table 3.1: Dataset Partitioning into Training, Validation, and Testing Sets")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(11)
    r.bold = True

    t_split = doc.add_table(rows=5, cols=4)
    t_split.alignment = WD_TABLE_ALIGNMENT.CENTER
    split_headers = ["Partition Subset", "Image Count", "Percentage (%)", "Functional Purpose"]
    split_data = [
        ("Training Set", "7,155 images", "70.0%", "Model parameter optimization and backpropagation"),
        ("Validation Set", "1,533 images", "15.0%", "Hyperparameter tuning, early stopping, and checkpoint selection"),
        ("Testing Set (Held-Out)", "1,534 images", "15.0%", "Unbiased final evaluation and confusion matrix computation"),
        ("Total Corpus", "10,222 images", "100.0%", "Complete Stanford Dogs benchmark across 120 breeds")
    ]
    for c_idx, h_text in enumerate(split_headers):
        cell = t_split.rows[0].cells[c_idx]
        cell.paragraphs[0].text = h_text
        cell.paragraphs[0].runs[0].bold = True
        set_cell_background(cell, "EAECEE")
        set_cell_margins(cell, 60, 60, 80, 80)
    for r_idx, row_vals in enumerate(split_data):
        row = t_split.rows[r_idx + 1]
        for c_idx, val in enumerate(row_vals):
            cell = row.cells[c_idx]
            cell.paragraphs[0].text = val
            set_cell_margins(cell, 50, 50, 70, 70)
            if r_idx == 3:
                cell.paragraphs[0].runs[0].bold = True
                set_cell_background(cell, "EAECEE")
            elif r_idx % 2 == 1:
                set_cell_background(cell, "F8F9FA")

    add_p("The class distribution shows an average of 85.18 images per breed (median: 82.0). The dataset exhibits mild class imbalance: Scottish Deerhound has the highest representation with 126 images, while Briard and Eskimo Dog possess the minimum representation with 66 images each.")

    add_fig("dataset/breed_distribution.png", "Figure 3.1: Sample Distribution Across 120 Dog Breeds in the Stanford Dogs Dataset", width=Inches(6.0))

    add_h2("Image Resizing and Normalization")
    add_p("Raw photographs possess varying dimensions and aspect ratios. Before batch processing, images pass through an automated preprocessing pipeline:")
    add_p("1. RGB Format Standardization: Single-channel grayscale and 4-channel CMYK images are converted into standard 3-channel RGB.")
    add_p("2. Bilinear Spatial Resizing: Images are resized to uniform 224 x 224 pixel dimensions.")
    add_p("3. Pixel Value Normalization: Pixel integers in [0, 255] are converted to floating-point values in [-1.0, +1.0] using MobileNetV2's scaling formula: x_norm = (x / 127.5) - 1.0.")
    add_p("4. Batch Dimension Expansion: Reshaped into a 4-dimensional tensor (1, 224, 224, 3) suitable for neural inference.")

    add_h2("Data Augmentation")
    add_p("Because 7,155 training images across 120 classes yields only ~60 images per breed in training, training without augmentation would lead to rapid overfitting. We applied real-time stochastic augmentation during training:")
    add_p("• Random Horizontal Flipping (50% probability): Teaches the model that canine orientation is invariant to breed identity.")
    add_p("• Random Rotation (+/- 15 degrees): Accommodates slight camera tilting.")
    add_p("• Random Zoom (+/- 10%): Simulates variations in subject-to-camera distance.")
    add_p("• Random Width and Height Shifts (+/- 10%): Simulates off-center framing.")
    add_p("• Nearest Boundary Filling: Prevents artificial black borders during rotation and shifting.")

    add_h2("Dataset Challenges")
    add_p("Exploratory data analysis revealed three key visual challenges:")
    add_p("• Subtle Facial Distinctions: Closely related terriers (such as Australian Terrier vs. Silky Terrier) differ primarily in fur texture and ear fringe rather than skull morphology.")
    add_p("• Background Clutter: Canines photographed on green grass, snow, or carpets create misleading background correlations that the model must learn to ignore.")
    add_p("• Posture Diversity: Dogs lying down, curled up, jumping, or panting present vastly different visual silhouettes compared to standard standing kennel poses.")

    doc.add_page_break()

    # =========================================================================
    # CHAPTER 4 – PROPOSED METHODOLOGY
    # =========================================================================
    add_h1("Chapter 4 – Proposed Methodology")
    
    add_h2("Overall System Architecture")
    add_p("We engineered the system as a decoupled, multi-tier web application consisting of four distinct tiers: Presentation Tier (Browser Client), Application Tier (Flask Web Framework), Deep Learning Tier (TensorFlow / Keras), and Database Tier (MySQL Server).")

    add_fig("model/report_assets/system_architecture.png", "Figure 4.1: Overall Multi-Tier System Architecture of the Dog Breed Identification Platform", width=Inches(6.0))

    add_h2("Image Input and Validation")
    add_p("When a user uploads an image, the client-side JavaScript (main.js) verifies that the file format is valid (.jpg, .jpeg, .png) and the size does not exceed 10 MB. On the server side, app.py sanitizes the filename using Werkzeug's secure_filename() to prevent path traversal attacks and loads the image into memory using PIL.")

    add_h2("Dog Presence Verification")
    add_p("To prevent non-dog images from receiving false dog breed predictions, we implemented an upstream canine presence filter:")
    add_p("- An input tensor is passed through a MobileNetV2 model pre-trained on the full 1,000-class ImageNet dataset.")
    add_p("- ImageNet contains 118 classes corresponding to domestic dog breeds and wild canids (indices 151 through 268, plus 273 and 275).")
    add_p("- The pipeline computes the cumulative probability score across all 118 canine indices: P(dog) = SUM(y_hat_k for k in ImageNet_Dog_Indices).")
    add_p("- Decision Logic: If the Top-1 predicted ImageNet class is a canine or P(dog) >= 0.20, the image is confirmed as a dog and forwarded to Stage 2. If P(dog) < 0.20, the pipeline halts immediately and returns an informative HTTP JSON warning ('No Dog Detected. Please upload a valid dog image.') without executing the breed classifier.")

    add_fig("model/report_assets/two_stage_pipeline.png", "Figure 4.2: Two-Stage Canine Detection and Fine-Grained Breed Classification Workflow", width=Inches(6.0))

    add_h2("MobileNetV2 Feature Extraction")
    add_p("Confirmed canine images are processed by our customized MobileNetV2 architecture. The network extracts rich spatial features through 155 layers of depthwise separable convolutions and inverted residual bottlenecks, outputting a high-level feature map of shape (7, 7, 1280).")

    add_fig("model/report_assets/cnn_architecture.png", "Figure 4.3: Transfer Learning Neural Network Architecture with MobileNetV2 Backbone", width=Inches(5.8))

    add_h2("Transfer Learning and Fine-Tuning")
    add_p("Model training was conducted systematically in two sequential phases:")
    add_p("Phase 1: Feature Extraction (Frozen Base): All 155 layers of the pre-trained MobileNetV2 base were frozen. A newly initialized classification head (GlobalAveragePooling2D, Dropout 0.3, Dense 120 Softmax) was trained for 10 epochs using Adam (learning rate = 1e-3). This established stable classification weights without disturbing the pre-trained ImageNet feature filters.")
    add_p("Phase 2: Deep Fine-Tuning (Top 30 Layers Unfrozen): The base model was unfrozen, and the top 30 convolutional layers were set to trainable. Training continued for 5 epochs using Adam with a substantially reduced learning rate (1e-5) to avoid disrupting pre-trained weights while adapting high-level filters to canine facial and coat textures. Callbacks included EarlyStopping (patience=5), ModelCheckpoint saving best_model.keras, and ReduceLROnPlateau (factor=0.5, patience=3).")

    add_h2("Breed Classification")
    add_p("Above the 155-layer MobileNetV2 base, we appended:")
    add_p("1. GlobalAveragePooling2D: Reduces the spatial dimensions from 7 x 7 x 1280 to a 1,280-dimensional feature vector, replacing heavy fully connected layers and preventing overfitting.")
    add_p("2. Dropout (0.3): Randomly deactivates 30% of neurons during training passes to force the network to learn robust, distributed representations.")
    add_p("3. Dense (120, Softmax): Produces normalized probabilities summing to 1.0 across all 120 dog breeds.")

    # Table 4.1
    p_tcap = doc.add_paragraph()
    p_tcap.paragraph_format.space_before = Pt(8)
    p_tcap.paragraph_format.space_after = Pt(2)
    r = p_tcap.add_run("Table 4.1: Neural Network Layer Progression and Parameter Distribution")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(11)
    r.bold = True

    t_layer = doc.add_table(rows=6, cols=4)
    t_layer.alignment = WD_TABLE_ALIGNMENT.CENTER
    layer_headers = ["Layer Component", "Output Shape", "Parameters", "Function in Architecture"]
    layer_data = [
        ("InputLayer", "(None, 224, 224, 3)", "0", "Accepts normalized RGB image tensors"),
        ("MobileNetV2 Base (155 layers)", "(None, 7, 7, 1280)", "2,257,984", "Depthwise separable feature extraction"),
        ("GlobalAveragePooling2D", "(None, 1280)", "0", "Spatial pooling to 1D feature vector"),
        ("Dropout (0.3 rate)", "(None, 1280)", "0", "Regularization preventing co-adaptation"),
        ("Dense (Softmax)", "(None, 120)", "153,720", "Class probability output across 120 breeds")
    ]
    for c_idx, h_text in enumerate(layer_headers):
        cell = t_layer.rows[0].cells[c_idx]
        cell.paragraphs[0].text = h_text
        cell.paragraphs[0].runs[0].bold = True
        set_cell_background(cell, "EAECEE")
        set_cell_margins(cell, 60, 60, 70, 70)
    for r_idx, row_vals in enumerate(layer_data):
        row = t_layer.rows[r_idx + 1]
        for c_idx, val in enumerate(row_vals):
            cell = row.cells[c_idx]
            cell.paragraphs[0].text = val
            set_cell_margins(cell, 40, 40, 60, 60)
            if r_idx % 2 == 1:
                set_cell_background(cell, "F8F9FA")

    add_h2("Prediction Confidence and Top-3 Results")
    add_p("Rather than returning only a single class label, our system extracts the top 3 highest probabilities: the top-1 class is identified as the primary breed match, while the 2nd and 3rd highest probabilities are extracted as candidate alternatives. Displaying Top-3 predictions provides full transparency to users, especially when the photograph depicts a mixed breed or a breed with visual similarity to another class.")

    add_h2("Complete Prediction Workflow")
    add_p("Algorithm 1: Two-Stage Canine Identification and Logging\n"
          "--------------------------------------------------------------------------------\n"
          "Input : Uploaded image file F, User session S\n"
          "Output: JSON response containing prediction details or rejection notice\n\n"
          "1.  IF F is empty OR extension(F) NOT IN {jpg, jpeg, png} THEN\n"
          "2.      RETURN Error('Invalid file format')\n"
          "3.  END IF\n"
          "4.  filename <- secure_filename(F.name)\n"
          "5.  save_path <- Save(F, UPLOAD_FOLDER, filename)\n"
          "6.  img <- Resize(ConvertToRGB(LoadImage(save_path)), (224, 224))\n"
          "7.  tensor <- ExpandDims(MobileNetV2_Preprocess(img), axis=0)\n"
          "8.  // Stage 1: Dog Presence Detection\n"
          "9.  imagenet_preds <- DogDetectorModel.predict(tensor)\n"
          "10. top1_idx <- argmax(imagenet_preds)\n"
          "11. dog_prob <- SUM(imagenet_preds[k] for k in IMAGENET_DOG_INDICES)\n"
          "12. IF top1_idx NOT IN IMAGENET_DOG_INDICES AND dog_prob < 0.20 THEN\n"
          "13.     RETURN Json(success=False, is_dog=False, message='No dog detected')\n"
          "14. END IF\n"
          "15. // Stage 2: Breed Classification\n"
          "16. breed_probs <- BreedClassifierModel.predict(tensor)\n"
          "17. top3_indices <- SortDescendingIndices(breed_probs)[0..2]\n"
          "18. top3_results <- []\n"
          "19. FOR EACH idx IN top3_indices DO\n"
          "20.     top3_results.append({'breed': FormatBreedName(class_names[idx]),\n"
          "                                 'confidence': Round(breed_probs[idx] * 100, 2)})\n"
          "21. END FOR\n"
          "22. primary_match <- top3_results[0]\n"
          "23. user_id <- S.get('user_id')\n"
          "24. prediction_id <- InsertPredictionRecord(user_id, filename, primary_match.breed,\n"
          "                                            primary_match.confidence, top3_results)\n"
          "25. RETURN Json(success=True, top_breed=primary_match.breed,\n"
          "                confidence=primary_match.confidence, top3=top3_results,\n"
          "                prediction_id=prediction_id)")

    doc.add_page_break()

    # =========================================================================
    # CHAPTER 5 – MODEL DEVELOPMENT AND WEB APPLICATION
    # =========================================================================
    add_h1("Chapter 5 – Model Development and Web Application")
    
    add_h2("Development Environment")
    add_p("The software was developed and validated under Microsoft Windows 11 (64-bit), utilizing Python 3.13 / 3.11, TensorFlow 2.21.0, Flask 3.0.0, and MySQL Server 8.0.")

    add_h2("Model Training")
    add_p("Training hyperparameters across both phases are summarized below:")

    # Table 5.1
    p_tcap = doc.add_paragraph()
    p_tcap.paragraph_format.space_before = Pt(8)
    p_tcap.paragraph_format.space_after = Pt(2)
    r = p_tcap.add_run("Table 5.1: Model Training Hyperparameter Configuration")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(11)
    r.bold = True

    t_cfg = doc.add_table(rows=11, cols=3)
    t_cfg.alignment = WD_TABLE_ALIGNMENT.CENTER
    cfg_headers = ["Hyperparameter / Parameter", "Phase 1: Feature Extraction", "Phase 2: Fine-Tuning"]
    cfg_data = [
        ("Base Model Layers", "155 layers (Frozen)", "Top 30 layers Unfrozen (125 Frozen)"),
        ("Trainable Parameters", "153,720 parameters", "1,212,504 parameters"),
        ("Non-Trainable Parameters", "2,257,984 parameters", "1,199,200 parameters"),
        ("Batch Size", "32", "32"),
        ("Optimizer", "Adam (beta1=0.9, beta2=0.999)", "Adam (beta1=0.9, beta2=0.999)"),
        ("Initial Learning Rate", "1e-3 (0.001)", "1e-5 (0.00001)"),
        ("Loss Function", "Categorical Cross-Entropy", "Categorical Cross-Entropy"),
        ("Epochs Executed", "10 epochs", "5 epochs (EarlyStopping trigger)"),
        ("Regularization", "Dropout (30%) + Augmentation", "Dropout (30%) + Augmentation"),
        ("Callbacks Active", "ModelCheckpoint, ReduceLROnPlateau", "EarlyStopping, ModelCheckpoint")
    ]
    for c_idx, h_text in enumerate(cfg_headers):
        cell = t_cfg.rows[0].cells[c_idx]
        cell.paragraphs[0].text = h_text
        cell.paragraphs[0].runs[0].bold = True
        set_cell_background(cell, "EAECEE")
        set_cell_margins(cell, 60, 60, 70, 70)
    for r_idx, row_vals in enumerate(cfg_data):
        row = t_cfg.rows[r_idx + 1]
        for c_idx, val in enumerate(row_vals):
            cell = row.cells[c_idx]
            cell.paragraphs[0].text = val
            set_cell_margins(cell, 40, 40, 60, 60)
            if r_idx % 2 == 1:
                set_cell_background(cell, "F8F9FA")

    add_h2("Model Integration")
    add_p("In app.py, the trained model model/best_model.keras is loaded once during server initialization using tf.keras.models.load_model(). The model instance is cached in memory, eliminating per-request loading latency and enabling immediate inference for concurrent user requests.")

    add_h2("Flask Application Architecture")
    add_p("The backend application (app.py) follows modular WSGI design principles:")
    add_p("• / (home): Renders the main landing page with system features and quick navigation.")
    add_p("• /identify (identify): Interactive prediction portal with drag-and-drop upload zone and preview.")
    add_p("• /predict (predict, POST): Core API endpoint that accepts multipart image uploads, runs the two-stage inference pipeline, persists prediction metadata to MySQL, and returns structured JSON responses.")
    add_p("• /breeds (breed_info): Comprehensive 120-breed directory with live search, size filters, and comparison tabs.")
    add_p("• /api/breeds (api_breeds): REST API returning complete breed metadata from database/breeds_data.json.")
    add_p("• /performance (performance): Interactive evaluation dashboard displaying accuracy curves, loss curves, confusion tables, and Chart.js graphs.")
    add_p("• /history (history): Authenticated user prediction history displaying thumbnails, dates, confidence scores, and Top-3 modals.")
    add_p("• /download_report and /download_report/<id>: Compiles and streams personalized PDF prediction certificates.")
    add_p("• /favorites & /api/favorites/toggle: Manages bookmarked user breeds.")
    add_p("• /feedback: Collects user star ratings and written reviews.")
    add_p("• /signup, /login, /logout: Authentication routes.")
    add_p("• /admin & /admin/grant: Administrative dashboard displaying real-time database aggregates and user role management.")

    # Table 5.3 Tech Stack
    p_tcap = doc.add_paragraph()
    p_tcap.paragraph_format.space_before = Pt(8)
    p_tcap.paragraph_format.space_after = Pt(2)
    r = p_tcap.add_run("Table 5.3: Core Software Technologies and Functional Roles")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(11)
    r.bold = True

    t_tech = doc.add_table(rows=8, cols=3)
    t_tech.alignment = WD_TABLE_ALIGNMENT.CENTER
    tech_headers = ["Technology", "Version / Category", "Functional Role in Project"]
    tech_data = [
        ("Python", "3.13 / 3.11", "Primary programming language across ML pipeline and backend"),
        ("TensorFlow / Keras", "2.21.0", "Model training, transfer learning, fine-tuning, and inference"),
        ("MobileNetV2", "ImageNet Backbone", "Convolutional feature extractor for Stage 1 and Stage 2"),
        ("Flask", "3.0.0", "Backend WSGI web framework, session management, and REST APIs"),
        ("MySQL & Connector", "8.0 Server / Connector", "Relational persistence for user accounts, history, and feedback"),
        ("ReportLab", "5.1.0", "Academic PDF prediction report generation engine"),
        ("Chart.js & Matplotlib", "4.4.0 / 3.9.0", "Interactive web analytics and static publication charts")
    ]
    for c_idx, h_text in enumerate(tech_headers):
        cell = t_tech.rows[0].cells[c_idx]
        cell.paragraphs[0].text = h_text
        cell.paragraphs[0].runs[0].bold = True
        set_cell_background(cell, "EAECEE")
        set_cell_margins(cell, 60, 60, 80, 80)
    for r_idx, row_vals in enumerate(tech_data):
        row = t_tech.rows[r_idx + 1]
        for c_idx, val in enumerate(row_vals):
            cell = row.cells[c_idx]
            cell.paragraphs[0].text = val
            set_cell_margins(cell, 50, 50, 70, 70)
            if r_idx % 2 == 1:
                set_cell_background(cell, "F8F9FA")

    add_h2("Image Upload and Prediction")
    add_p("The front-end interface provides a clean, responsive drag-and-drop drop zone. Once an image is selected, client-side JavaScript generates an immediate local preview with dimensions. Clicking Predict Breed triggers an asynchronous fetch() POST request. If Stage 1 detects a non-dog, a warning card is shown; if verified as a dog, the primary breed match, confidence percentage, and animated Top-3 probability bars appear smoothly.")

    add_h2("User Authentication")
    add_p("User security is implemented using Werkzeug's cryptographic PBKDF2/SHA-256 password hashing. Passwords are never stored in plaintext. Secure session cookies track user identity across requests. Two custom Python decorators enforce route protection: @login_required (redirects unauthenticated users to /login) and @admin_required (restricts administrative routes to users with is_admin = 1, returning HTTP 403 Forbidden to regular users).")

    add_h2("Breed Information and Trait Comparison")
    add_p("To provide educational value beyond raw predictions, we curated a comprehensive JSON database (database/breeds_data.json) covering all 120 breeds. Each breed entry includes origin, size, typical lifespan, temperament tags, and physical descriptions. Users can select any two breeds for side-by-side comparison across height, weight, activity level, and care requirements.")

    add_h2("Prediction History")
    add_p("Every successful prediction is recorded in MySQL. Authenticated users can visit /history to review their previous uploads, examine past confidence scores, and re-download prediction reports. Guests can also view recent session predictions.")

    add_h2("Database Design")
    add_p("The relational database dog_breed_db maintains four normalized tables:")

    # Table 5.2
    p_tcap = doc.add_paragraph()
    p_tcap.paragraph_format.space_before = Pt(8)
    p_tcap.paragraph_format.space_after = Pt(2)
    r = p_tcap.add_run("Table 5.2: Relational Database Schema Design (dog_breed_db)")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(11)
    r.bold = True

    t_db = doc.add_table(rows=5, cols=4)
    t_db.alignment = WD_TABLE_ALIGNMENT.CENTER
    db_headers = ["Table Name", "Primary Key", "Foreign Keys", "Key Attributes Stored"]
    db_data = [
        ("users", "user_id (INT)", "None", "username, email, password_hash, is_admin, created_at"),
        ("prediction_history", "prediction_id (INT)", "user_id -> users(user_id)", "image_path, predicted_breed, confidence, top3_results (JSON), model_version, created_at"),
        ("favorite_breeds", "favorite_id (INT)", "user_id -> users(user_id)", "breed_name, created_at (Unique compound: user_id, breed_name)"),
        ("feedback", "feedback_id (INT)", "user_id -> users(user_id)", "rating (1–5), message (TEXT), created_at")
    ]
    for c_idx, h_text in enumerate(db_headers):
        cell = t_db.rows[0].cells[c_idx]
        cell.paragraphs[0].text = h_text
        cell.paragraphs[0].runs[0].bold = True
        set_cell_background(cell, "EAECEE")
        set_cell_margins(cell, 60, 60, 70, 70)
    for r_idx, row_vals in enumerate(db_data):
        row = t_db.rows[r_idx + 1]
        for c_idx, val in enumerate(row_vals):
            cell = row.cells[c_idx]
            cell.paragraphs[0].text = val
            set_cell_margins(cell, 40, 40, 60, 60)
            if r_idx % 2 == 1:
                set_cell_background(cell, "F8F9FA")

    add_h2("Other Implemented Features")
    add_p("• ReportLab PDF Report Generation: Produces a standardized, academic prediction report containing the project title, uploaded photograph, primary match, confidence score, Top-3 candidate breakdown, model version, timestamp, and a scientific machine learning disclaimer.")
    add_p("• Star Rating Feedback System: Allows users to submit 1-to-5 star ratings and comments stored directly in MySQL.")
    add_p("• Admin Analytics Dashboard: Calculates live SQL metrics (total users, total predictions, average confidence, total feedback) and visualizes the top 10 most frequently identified breeds using a Chart.js horizontal bar chart.")

    add_fig("model/report_assets/admin_dashboard.png", "Figure 5.1: Administrative Dashboard Interface Displaying Real-Time Database Metrics and Top Breeds", width=Inches(5.0))

    doc.add_page_break()

    # =========================================================================
    # CHAPTER 6 – RESULTS AND DISCUSSION
    # =========================================================================
    add_h1("Chapter 6 – Results and Discussion")
    
    add_h2("Training and Validation Performance")
    add_p("Training proceeded smoothly across 15 epochs without gradient instability. In Phase 1 (frozen base), the newly attached classification head learned decision boundaries rapidly:")
    add_p("• Epoch 1: Training Accuracy = 31.2%, Validation Accuracy = 48.5%, Validation Loss = 2.124")
    add_p("• Epoch 5: Training Accuracy = 72.1%, Validation Accuracy = 73.6%, Validation Loss = 0.985")
    add_p("• Epoch 10: Training Accuracy = 86.4%, Validation Accuracy = 79.8%, Validation Loss = 0.742")
    add_p("• Epoch 15 (Fine-Tuning): Unfreezing the top 30 layers increased training accuracy to 92.3%, validation accuracy to 82.4%, and lowered validation loss to 0.661.")

    add_fig("model/report_assets/training_curves.png", "Figure 6.1: Training and Validation Accuracy and Loss Curves Across 15 Epochs", width=Inches(6.0))

    add_h2("Accuracy and Loss")
    add_p("The smooth decrease in validation loss across both phases confirmed that our learning rate reduction strategy (1e-3 down to 1e-5) and 30% dropout regularization successfully prevented severe memorization on the 7,155 training images.")

    add_h2("Top-1 and Top-5 Accuracy")
    add_p("The fine-tuned model was evaluated on the 1,534 held-out test images that were never seen during training or validation:")

    # Table 6.1
    p_tcap = doc.add_paragraph()
    p_tcap.paragraph_format.space_before = Pt(8)
    p_tcap.paragraph_format.space_after = Pt(2)
    r = p_tcap.add_run("Table 6.1: Model Performance Metrics on Held-Out Test Set (1,534 Images)")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(11)
    r.bold = True

    t_met = doc.add_table(rows=10, cols=3)
    t_met.alignment = WD_TABLE_ALIGNMENT.CENTER
    met_headers = ["Evaluation Metric", "Measured Value", "Operational Interpretation"]
    met_rows = [
        ("Top-1 Test Accuracy", "77.64%", "Exact ground-truth breed match on held-out test images"),
        ("Top-5 Test Accuracy", "96.87%", "Correct breed present within model's top 5 candidates"),
        ("Test Categorical Cross-Entropy Loss", "0.7036", "Cross-entropy loss on unaugmented test images"),
        ("Macro Average Precision", "78.58%", "Unweighted mean precision across all 120 categories"),
        ("Macro Average Recall", "76.98%", "Unweighted mean recall across all 120 categories"),
        ("Macro Average F1-Score", "76.91%", "Harmonic mean of macro precision and recall"),
        ("Weighted Average Precision", "78.75%", "Support-weighted precision reflecting class sample sizes"),
        ("Weighted Average Recall", "77.64%", "Support-weighted recall matching overall accuracy"),
        ("Weighted Average F1-Score", "77.35%", "Support-weighted harmonic mean across all test samples")
    ]
    for c_idx, h_text in enumerate(met_headers):
        cell = t_met.rows[0].cells[c_idx]
        cell.paragraphs[0].text = h_text
        cell.paragraphs[0].runs[0].bold = True
        set_cell_background(cell, "EAECEE")
        set_cell_margins(cell, 60, 60, 80, 80)
    for r_idx, row_vals in enumerate(met_rows):
        row = t_met.rows[r_idx + 1]
        for c_idx, val in enumerate(row_vals):
            cell = row.cells[c_idx]
            cell.paragraphs[0].text = val
            set_cell_margins(cell, 45, 45, 60, 60)
            if r_idx < 2:
                cell.paragraphs[0].runs[0].bold = True
                set_cell_background(cell, "FEF9E7")
            elif r_idx % 2 == 1:
                set_cell_background(cell, "F8F9FA")

    add_p("The Top-5 accuracy of 96.87% is especially meaningful for practical canine identification: in almost 97 out of 100 cases, the correct breed is present among the top 5 candidates ranked by the model.")

    add_h2("Precision, Recall and F1-Score")
    add_p("Examining individual breed performance showed that the network achieved strong discriminative power across the majority of breeds:")
    add_p("• Top-Performing Breeds (100% Precision, Recall, and F1-Score): African Hunting Dog (unique tri-color patchwork coat), Keeshond (distinctive silver-black ruff and eye spectacles), Papillon (prominent butterfly ears), and Bloodhound (heavy jowls and facial skin folds).")
    add_p("• Challenging Breeds: Italian Greyhound (F1 = 54.1%, confused with Whippet), Kuvasz (F1 = 53.3%, confused with Great Pyrenees), and Cardigan Welsh Corgi (F1 = 52.6%, confused with Pembroke Welsh Corgi).")

    add_h2("Prediction Examples")
    add_p("When evaluating real-world test images:")
    add_p("• An input photograph of a Labrador Retriever (dog.jpg) passed Stage 1 with a canine probability of 92.4% and received a primary prediction of Labrador Retriever with 69.34% confidence (#2: Golden Retriever at 9.37%, #3: Chesapeake Bay Retriever at 8.08%).")
    add_p("• A Siberian Husky photograph (doog1.jpg) passed Stage 1 with 98.7% canine probability and was correctly classified as Siberian Husky (#2: Eskimo Dog, #3: Alaskan Malamute).")

    add_h2("Dog and Non-Dog Image Testing")
    add_p("Stage 1 canine presence detection was validated against both positive dog images and negative non-canine samples:")
    add_p("• Positive Canine Images: Produced canine probabilities exceeding 88%, correctly continuing to Stage 2 breed prediction.")
    add_p("• Negative Control Images (e.g., horse photograph Black-Horse-Names-with-Meanings.jpeg, vehicles, landscapes): The top predicted ImageNet class was non-canine (sorrel, Arabian horse), with total canine probability below 0.02. The system halted cleanly, returning the expected No Dog Detected alert.")

    add_h2("Commonly Confused Breeds")
    add_p("Analysis of the test confusion matrix revealed 12 prominent pairs of confused dog breeds. In all 12 cases, the confusion is biologically justified by identical coat textures, ancestral lineages, or anatomical proportions:")

    add_fig("model/report_assets/confused_breeds_chart.png", "Figure 6.2: Top 12 Most Frequently Confused Dog Breed Pairs in Evaluation Set", width=Inches(6.0))

    # Table 6.2
    p_tcap = doc.add_paragraph()
    p_tcap.paragraph_format.space_before = Pt(8)
    p_tcap.paragraph_format.space_after = Pt(2)
    r = p_tcap.add_run("Table 6.2: Top 12 Most Frequently Confused Dog Breed Pairs with Visual Reasons")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(11)
    r.bold = True

    t_conf = doc.add_table(rows=13, cols=5)
    t_conf.alignment = WD_TABLE_ALIGNMENT.CENTER
    conf_headers = ["No.", "Actual Breed", "Predicted Breed", "Count", "Visual Similarity Reason"]
    conf_data = [
        ("1", "Whippet", "Italian Greyhound", "7 images", "Identical slender sighthound posture and sleek coat"),
        ("2", "Lhasa Apso", "Shih-Tzu", "6 images", "Closely related Tibetan companion dogs with long facial fur"),
        ("3", "Eskimo Dog", "Siberian Husky", "5 images", "Arctic spitz breeds with erect ears, double coats, curled tails"),
        ("4", "Australian Terrier", "Silky Terrier", "4 images", "Related terrier types sharing wiry/silky coats and silhouettes"),
        ("5", "Kuvasz", "Great Pyrenees", "4 images", "Large flock-guarding breeds with solid white double coats"),
        ("6", "Maltese Dog", "West Highland White Terrier", "4 images", "Similar fine-grained facial features, fur texture, and white color"),
        ("7", "Samoyed", "Great Pyrenees", "4 images", "Large breeds sharing solid white, fluffy double coats"),
        ("8", "Staffordshire Bull Terrier", "American Staffordshire Terrier", "4 images", "Closely related bully breeds sharing blocky heads and muscular frames"),
        ("9", "Cardigan Welsh Corgi", "Pembroke Welsh Corgi", "3 images", "Both Welsh Corgi breeds, differing primarily in tail length"),
        ("10", "Collie", "Shetland Sheepdog", "3 images", "Herding breeds sharing identical facial markings and long ruffs"),
        ("11", "Irish Wolfhound", "Scottish Deerhound", "3 images", "Similar rough-coated wiry body structure and sighthound build"),
        ("12", "Lakeland Terrier", "Soft-Coated Wheaten Terrier", "3 images", "Similar tan/wheaten coat colors and bearded facial profiles")
    ]
    for c_idx, h_text in enumerate(conf_headers):
        cell = t_conf.rows[0].cells[c_idx]
        cell.paragraphs[0].text = h_text
        cell.paragraphs[0].runs[0].bold = True
        set_cell_background(cell, "EAECEE")
        set_cell_margins(cell, 60, 60, 60, 60)
    for r_idx, row_vals in enumerate(conf_data):
        row = t_conf.rows[r_idx + 1]
        for c_idx, val in enumerate(row_vals):
            cell = row.cells[c_idx]
            cell.paragraphs[0].text = val
            set_cell_margins(cell, 40, 40, 50, 50)
            if r_idx % 2 == 1:
                set_cell_background(cell, "F8F9FA")

    add_h2("Application Testing")
    add_p("To verify that all subsystems operate reliably without runtime crashes or database errors, we implemented an automated test suite (run_complete_tests.py) comprising 18 test cases. All 18 tests passed with a 100% success rate:")

    # Table 6.3
    p_tcap = doc.add_paragraph()
    p_tcap.paragraph_format.space_before = Pt(8)
    p_tcap.paragraph_format.space_after = Pt(2)
    r = p_tcap.add_run("Table 6.3: Complete 18-Point Automated Application Test Suite Verification")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(11)
    r.bold = True

    t_test = doc.add_table(rows=19, cols=5)
    t_test.alignment = WD_TABLE_ALIGNMENT.CENTER
    test_headers = ["Test ID", "Subsystem", "Expected Behavior", "Actual Measured Outcome", "Status"]
    test_data = [
        ("TC-01", "Flask Startup", "Initializes cleanly with secret key", "App initialized; secret key verified", "PASS"),
        ("TC-02", "Homepage Navigation", "HTTP 200 on /; renders navbar links", "Status 200; Navigation links present", "PASS"),
        ("TC-03", "Image Upload", "Multipart POST saves image", "Status 200; Saved to uploads/", "PASS"),
        ("TC-04", "Invalid Image Handling", "Rejects bad format & corrupted files", "Proper error messages returned", "PASS"),
        ("TC-05", "Canine Validation", "Blocks non-dogs; accepts dogs", "Horse rejected; Dog accepted", "PASS"),
        ("TC-06", "Model Loading", "MobileNetV2 loaded (224, 224, 3)", "Input (224, 224, 3); 120 classes", "PASS"),
        ("TC-07", "Breed Prediction", "Returns valid breed and confidence", "Predicted Labrador (69.34%)", "PASS"),
        ("TC-08", "Top-3 Ranked Scores", "Exactly 3 breeds sorted descending", "Scores: #1 69.3%, #2 9.4%, #3 8.1%", "PASS"),
        ("TC-09", "MySQL Connection", "Connects to dog_breed_db; 4 tables", "Connected; all 4 tables verified", "PASS"),
        ("TC-10", "Signup & Login", "Creates user, hashes password", "Signup OK; session created; logout OK", "PASS"),
        ("TC-11", "Prediction History", "Restricts unauthenticated users", "Guest -> 302; Authenticated -> 200", "PASS"),
        ("TC-12", "Favorite Breeds", "AJAX toggle bookmarks breed", "Bookmark added & removed correctly", "PASS"),
        ("TC-13", "Breed Directory", "/breeds renders 120 breeds", "Status 200; 120 breeds loaded", "PASS"),
        ("TC-14", "Breed Comparison", "Verifies comparison selectors", "Side-by-side attributes verified", "PASS"),
        ("TC-15", "Performance Charts", "Returns accuracy and confusion data", "Status 200; 77.64% test accuracy", "PASS"),
        ("TC-16", "PDF Report Download", "Streams valid PDF binary", "Status 200; Mime: application/pdf", "PASS"),
        ("TC-17", "Admin Access Control", "Enforces RBAC on /admin", "Guest -> 302; User -> 403; Admin -> 200", "PASS"),
        ("TC-18", "Responsive Design", "Viewport meta tag & media queries", "Breakpoints (480, 600, 768, 900px)", "PASS")
    ]
    for c_idx, h_text in enumerate(test_headers):
        cell = t_test.rows[0].cells[c_idx]
        cell.paragraphs[0].text = h_text
        cell.paragraphs[0].runs[0].bold = True
        set_cell_background(cell, "EAECEE")
        set_cell_margins(cell, 60, 60, 60, 60)
    for r_idx, row_vals in enumerate(test_data):
        row = t_test.rows[r_idx + 1]
        for c_idx, val in enumerate(row_vals):
            cell = row.cells[c_idx]
            cell.paragraphs[0].text = val
            set_cell_margins(cell, 35, 35, 45, 45)
            if c_idx == 4:
                cell.paragraphs[0].runs[0].bold = True
            if r_idx % 2 == 1:
                set_cell_background(cell, "F8F9FA")

    add_h2("Observations")
    add_p("• Inference Latency: On standard consumer CPU hardware, a single prediction forward pass (preprocessing, Stage 1 check, Stage 2 prediction, and database insertion) takes 120 to 160 milliseconds, well within the 500 ms benchmark for interactive web responsiveness.")
    add_p("• Memory Footprint: MobileNetV2 requires only ~14 MB of disk storage and minimal RAM, enabling rapid application startup and stable hosting on lightweight server environments.")

    doc.add_page_break()

    # =========================================================================
    # CHAPTER 7 – CONCLUSION AND FUTURE ENHANCEMENTS
    # =========================================================================
    add_h1("Chapter 7 – Conclusion and Future Enhancements")
    
    add_h2("Project Summary")
    add_p("In this B.Tech capstone project, we designed, developed, and deployed an end-to-end canine breed identification platform using transfer learning with MobileNetV2 and full-stack web engineering. Our work demonstrates that lightweight convolutional networks can achieve high diagnostic performance in complex fine-grained visual classification tasks while maintaining low computational latency.")
    add_p("Key accomplishments of the project include:")
    add_p("1. Architected a Two-Stage Pipeline: Introduced an upstream ImageNet canine presence filter that prevents non-dog uploads from receiving false dog breed predictions.")
    add_p("2. Attained Strong Academic Accuracy: Achieved 77.64% Top-1 test accuracy and 96.87% Top-5 test accuracy across 120 breeds on 1,534 held-out evaluation images.")
    add_p("3. Engineered a Full-Stack Web Platform: Implemented a secure Flask application with MySQL database persistence, PBKDF2 password hashing, role-based access control, and dynamic PDF prediction report compilation.")
    add_p("4. Delivered Rich User Features: Integrated a 120-breed interactive directory, side-by-side trait comparison, individual prediction history tracking, user feedback, and an administrative dashboard.")
    add_p("5. Validated Reliability: Executed an automated 18-point verification testing suite with a 100% pass rate.")

    add_h2("Learning Outcomes")
    add_p("Through the development of this project, our team acquired valuable engineering experience:")
    add_p("• Practical understanding of deep transfer learning, inverted residual bottlenecks, and the delicate balance required during two-phase fine-tuning.")
    add_p("• Experience with dataset splitting strategies, data augmentation, and handling fine-grained visual classification challenges.")
    add_p("• Full-stack web engineering skills connecting deep learning models to Flask web applications and MySQL databases.")
    add_p("• Automated testing practices to ensure software stability across database transactions, session cookies, and API endpoints.")

    add_h2("Limitations")
    add_p("The system exhibits three practical limitations:")
    add_p("1. Resolution Downscaling: Resizing images to 224 x 224 pixels inevitably discards micro-level textures (such as fine fur whisker curls) that could help differentiate closely related terrier varieties.")
    add_p("2. Single-Subject Assumption: The model assumes that a single primary canine is centered in the photograph. If multiple dogs appear together, their feature maps blend, leading to lower prediction confidence.")
    add_p("3. Absence of Physical Scale Reference: In a 2D photograph lacking reference objects, an Italian Greyhound (weighing 4 kg) looks identical in proportions to a Whippet (weighing 13 kg). Without physical scale measurements, 2D CNNs cannot exploit size differences.")

    add_h2("Future Improvements")
    add_p("Several promising directions exist for future enhancement:")
    add_p("1. Upstream Object Detection & Bounding Box Localization: Incorporating a lightweight YOLOv8 detector to crop the canine body from cluttered backgrounds before classification.")
    add_p("2. Mobile Edge Deployment: Quantizing the trained MobileNetV2 model to TensorFlow Lite (TFLite) or ONNX format for on-device inference on Android and iOS devices without requiring internet connectivity.")
    add_p("3. Vision Transformers (ViT) & Attention Mechanisms: Exploring part-attention networks to explicitly focus convolutional attention on diagnostic anatomical regions (ears, snout, tail posture).")
    add_p("4. Mixed-Breed Percentage Estimation: Expanding the classification head to estimate breed composition percentages for mixed-breed dogs.")

    doc.add_page_break()

    # =========================================================================
    # REFERENCES
    # =========================================================================
    add_h1("References")
    refs = [
        "1. S. Selvaraj, R. Thangarajan, S. Anbukkarasi, and S. Yuvan Prasad, \"ResNet50 Architecture Based Dog Breed Identification Using Deep Learning,\" in Proc. Int. Conf. on Computational Intelligence and Knowledge Economy, 2023.",
        "2. P. Borwarnginn, W. Kusakunniran, S. Karnjanapreechakorn, and K. Thongkanchorn, \"Knowing Your Dog Breed: Identifying a Dog Breed with Deep Learning,\" in Proc. Int. Conf. on Information Technology, 2021.",
        "3. S. A. Bokhari, P. Mukherjee, A. S. Singh, S. Shaik, and J. K. Mathew, \"Convolutional Neural Network Based Dog Breed Classification,\" in Proc. Int. Conf. on Innovative Computing and Communication, 2022.",
        "4. T. Kumaravel, P. Natesan, V. E. Sathishkumar, S. S. N, S. G, and U. V, \"Automatic Dog Breed Classification Using Deep Learning,\" in Proc. Int. Conf. on Smart Systems and Inventive Technology, 2023.",
        "5. N. Banakar, Raghavendra B. U., S. G. S., T. K. Vani, and V. M. Vishnu, \"Dog Breed Identification Using Deep Learning,\" International Journal of Advanced Research in Computer Science and Software Engineering, vol. 13, no. 5, 2023.",
        "6. B. Valarmathi, N. S. Gupta, G. Prakash, R. H. Reddy, S. Saravanan, and P. Shanmugasundaram, \"Hybrid Deep Learning Algorithms for Dog Breed Identification—A Comparative Analysis,\" IEEE Access, vol. 11, pp. 45120–45132, 2023.",
        "7. S. R. Basha, I. Ganesh, G. R. Reddy, and A. Hans, \"Dogs Breed Classification Using Deep Learning,\" in Proc. Int. Conf. on Artificial Intelligence and Smart Systems, 2021.",
        "8. S. S. Hussain, K. S. R. Murthy, C. S. Rani, T. Nanuvala, C. R. Kumar, and G. Sathar, \"Automated Dog Breed Recognition Using CNN-Based Transfer Learning,\" in Proc. Int. Conf. on Advances in Computer Engineering & Communication Systems, 2025.",
        "9. A. S. Ghotra, H. Kour, A. Hasan, and A. Khan, \"Dog Breed Identification,\" in Proc. Int. Conf. on Data Science and Machine Learning, 2023.",
        "10. J. Bankar, A. Nalawade, S. Wali, A. Rane, and H. Matlani, \"AI Based Dog Breed Prediction Model and Virtual Canine Hub,\" International Journal of Computer Applications, vol. 186, no. 14, 2025.",
        "11. D.-N. Zou, S.-H. Zhang, T.-J. Mu, and M. Zhang, \"A New Dataset of Dog Breed Images and a Benchmark for Fine-Grained Classification,\" Computational Visual Media, vol. 6, no. 4, pp. 477–487, 2020.",
        "12. P. Perera and V. M. Patel, \"Deep Transfer Learning for Multiple Class Novelty Detection,\" in Proc. IEEE/CVF Conf. on Computer Vision and Pattern Recognition (CVPR), 2019, pp. 1154–1162.",
        "13. A. Khosla, N. Jayadevaprakash, B. Yao, and L. Fei-Fei, \"Novel Dataset for Fine-Grained Image Categorization: Stanford Dogs,\" in Proc. CVPR Workshop on Fine-Grained Visual Categorization, 2011.",
        "14. M. Sandler, A. Howard, M. Zhu, A. Zhmoginov, and L.-C. Chen, \"MobileNetV2: Inverted Residuals and Linear Bottlenecks,\" in Proc. IEEE/CVF Conf. on Computer Vision and Pattern Recognition (CVPR), 2018, pp. 4510–4520.",
        "15. M. Abadi et al., \"TensorFlow: A System for Large-Scale Machine Learning,\" in Proc. 12th USENIX Symp. on Operating Systems Design and Implementation (OSDI), 2016, pp. 265–283.",
        "16. A. Grinberg, Flask Web Development: Developing Web Applications with Python, 2nd ed. Sebastopol, CA: O'Reilly Media, 2018.",
        "17. ReportLab Europe Ltd., ReportLab PDF Generation User Guide, Version 5.1, London, UK, 2024.",
        "18. Oracle Corporation, MySQL 8.0 Reference Manual, Redwood Shores, CA: Oracle, 2024."
    ]
    for r_text in refs:
        p_ref = doc.add_paragraph()
        p_ref.paragraph_format.space_after = Pt(6)
        p_ref.paragraph_format.left_indent = Inches(0.4)
        p_ref.paragraph_format.first_line_indent = Inches(-0.4)
        r = p_ref.add_run(r_text)
        r.font.name = 'Times New Roman'
        r.font.size = Pt(11)

    doc.add_page_break()

    # =========================================================================
    # TEAM CONTRIBUTIONS
    # =========================================================================
    add_h1("Team Contributions")
    add_p("This project was divided into four major areas to ensure that each team member contributed to a specific part of the development process.")

    add_h2("K Goutham Nayak – CS24B1081")
    add_h3("Backend Architecture, MySQL Database and PDF Reporting")
    add_p("• Implemented Flask application routing and asynchronous REST APIs.")
    add_p("• Designed the MySQL relational database schema (dog_breed_db) across 4 tables.")
    add_p("• Developed password hashing using Werkzeug PBKDF2/SHA-256 and role-based decorators (@login_required, @admin_required).")
    add_p("• Built the automated ReportLab PDF prediction report generator.")
    add_p("• Configured individual prediction history and favorites management.")

    add_h2("K Adithya – CS24B1091")
    add_h3("Deep Learning Model Architecture and Fine-Tuning")
    add_p("• Implemented MobileNetV2 transfer learning using TensorFlow / Keras.")
    add_p("• Configured the two-phase training strategy (Phase 1 frozen feature extraction; Phase 2 top 30 unfrozen fine-tuning).")
    add_p("• Applied learning rate scheduling, early stopping, and model checkpointing.")
    add_p("• Computed quantitative evaluation metrics (Top-1 77.64%, Top-5 96.87%, test loss 0.7036, macro/weighted F1).")
    add_p("• Generated training convergence curves and confusion matrix artifacts.")

    add_h2("R Mahesh Rathod – CS24B1071")
    add_h3("Two-Stage Canine Presence Detection and Validation")
    add_p("• Formulated and implemented the Stage 1 ImageNet canine presence filter.")
    add_p("• Mapped 118 domestic and wild canine ImageNet class indices.")
    add_p("• Calibrated the cumulative canine probability threshold (P(dog) >= 0.20).")
    add_p("• Validated the system against negative non-dog images (horses, vehicles, landscapes).")
    add_p("• Conducted error analysis on the 12 most frequently confused dog breed pairs.")

    add_h2("G Vishnu Vardhan – CS24B1028")
    add_h3("Frontend UI/UX, Breed Directory and Trait Comparison")
    add_p("• Designed the responsive HTML5/CSS3 cream-and-brown web interface.")
    add_p("• Developed the drag-and-drop file upload logic and image preview in JavaScript.")
    add_p("• Built the 120-breed interactive directory with search and size filtering.")
    add_p("• Implemented the side-by-side breed trait comparison tool.")
    add_p("• Integrated Chart.js for the administrative dashboard and model performance charts.")

    add_h2("Shared Group Responsibilities")
    add_p("• Extracted and evaluated methodology and limitations across 12 research papers in the literature survey.")
    add_p("• Partitioned the 10,222 images into stratified 70% / 15% / 15% train, validation, and test sets.")
    add_p("• Executed and validated all 18 test cases in the automated application test suite (run_complete_tests.py).")
    add_p("• Prepared and proofread the comprehensive B.Tech project report.")

    p_end = doc.add_paragraph()
    p_end.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_end.paragraph_format.space_before = Pt(30)
    r = p_end.add_run("— END OF REPORT —")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(11)
    r.bold = True

    # Save
    doc.save(output_path)
    print(f"[OK] Generated Word Document Report: {output_path}")

if __name__ == '__main__':
    create_docx('Dog_Breed_Identification_Project_Report.docx')
