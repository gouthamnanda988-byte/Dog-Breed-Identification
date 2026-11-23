"""
build_clean_student_report.py
=============================
Generates the revised, figure-free, student-written B.Tech project report:
DOG BREED IDENTIFICATION USING DEEP LEARNING AND TRANSFER LEARNING

Features:
- Complete removal of ALL figures, screenshots, diagrams, and charts.
- Removal of List of Figures.
- Strict elimination of corrupted characters (â€¢, â€–, â€", Ã—, etc.).
- Simplified Chapter 4 (Methodology) matching user specifications.
- Simplified Chapter 6 (only 6.1 Model Training Progress and 6.2 Quantitative Evaluation Metrics; sections 6.3, 6.4, 6.5, 6.6 removed).
- Chapter 7 rewritten in natural student voice with 7.1 Conclusion, 7.2 Limitations, 7.3 Future Enhancements.
- 12 literature survey papers preserved in Chapter 2 and References.
- Times New Roman typography, 12 pt body, 1.5 line spacing, readable tables.
- Two-pass page resolution for 100% accurate Table of Contents & List of Tables.
- Outputs both DOCX and PDF into FINAL_REVISED_DOG_BREED_REPORT.
"""

import os
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Flowable
)
from reportlab.pdfgen import canvas
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT, TA_RIGHT

def int_to_roman(num):
    val = [1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1]
    syb = ["m", "cm", "d", "cd", "c", "xc", "l", "xl", "x", "ix", "v", "iv", "i"]
    roman_num = ''
    i = 0
    while num > 0:
        for _ in range(num // val[i]):
            roman_num += syb[i]
            num -= val[i]
        i += 1
    return roman_num

# =========================================================================
# 1. DOCX GENERATOR
# =========================================================================

def set_cell_background(cell, hex_color):
    tc_pr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>')
    tc_pr.append(shd)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tc_pr = cell._tc.get_or_add_tcPr()
    tc_mar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="{top}" w:type="dxa"/><w:bottom w:w="{bottom}" w:type="dxa"/><w:left w:w="{left}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/></w:tcMar>')
    tc_pr.append(tc_mar)

def generate_docx(output_path, page_map=None):
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

    def add_bullet(text, space_after=4):
        p = doc.add_paragraph()
        p.paragraph_format.line_spacing = 1.5
        p.paragraph_format.left_indent = Inches(0.3)
        p.paragraph_format.space_after = Pt(space_after)
        p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        r_b = p.add_run("•  ")
        r_b.font.name = 'Times New Roman'
        r_b.font.size = Pt(12)
        r_b.bold = True
        r_text = p.add_run(text)
        r_text.font.name = 'Times New Roman'
        r_text.font.size = Pt(12)
        return p

    def add_numbered(num_str, text, space_after=4):
        p = doc.add_paragraph()
        p.paragraph_format.line_spacing = 1.5
        p.paragraph_format.left_indent = Inches(0.3)
        p.paragraph_format.space_after = Pt(space_after)
        p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        r_num = p.add_run(f"{num_str}.  ")
        r_num.font.name = 'Times New Roman'
        r_num.font.size = Pt(12)
        r_num.bold = True
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
        r.font.size = Pt(14)
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

    # =========================================================================
    # TITLE PAGE
    # =========================================================================
    p_inst = doc.add_paragraph()
    p_inst.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_inst.paragraph_format.space_before = Pt(36)
    p_inst.paragraph_format.space_after = Pt(12)
    r = p_inst.add_run("INDIAN INSTITUTE OF INFORMATION TECHNOLOGY,\nDESIGN AND MANUFACTURING, KANCHEEPURAM")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(14)
    r.bold = True
    r.font.color.rgb = RGBColor(0x1A, 0x2B, 0x4C)

    p_course = doc.add_paragraph()
    p_course.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_course.paragraph_format.space_after = Pt(4)
    r = p_course.add_run("COURSE: INTRODUCTION TO DATA SCIENCE FOR ENGINEERS")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(11)
    r.bold = True
    r.font.color.rgb = RGBColor(0x2A, 0x43, 0x65)

    p_doc = doc.add_paragraph()
    p_doc.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_doc.paragraph_format.space_after = Pt(4)
    r = p_doc.add_run("PROJECT REPORT")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(12)
    r.bold = True
    r.font.color.rgb = RGBColor(0x1A, 0x52, 0x76)

    p_acad = doc.add_paragraph()
    p_acad.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_acad.paragraph_format.space_after = Pt(28)
    r = p_acad.add_run("ACADEMIC YEAR: 2026")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(11)
    r.bold = True

    # Divider Line
    p_div = doc.add_paragraph()
    p_div.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_div.paragraph_format.space_after = Pt(28)
    r = p_div.add_run("______________________________________________________________________")
    r.font.color.rgb = RGBColor(0x7F, 0x8C, 0x8D)

    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_after = Pt(36)
    r = p_title.add_run("DOG BREED IDENTIFICATION USING DEEP LEARNING AND TRANSFER LEARNING")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(20)
    r.bold = True
    r.font.color.rgb = RGBColor(0x1A, 0x2B, 0x4C)

    p_by = doc.add_paragraph()
    p_by.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_by.paragraph_format.space_after = Pt(12)
    r = p_by.add_run("PROJECT TEAM MEMBERS")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(12)
    r.bold = True

    # Student Table on Cover Page
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
            r.font.size = Pt(10.5)
            if row_idx == 0:
                r.bold = True
                set_cell_background(cell, "EAECEE")
            set_cell_margins(cell, 60, 60, 80, 80)

    doc.add_page_break()

    # =========================================================================
    # PROJECT SPECIFICATIONS (Page 2)
    # =========================================================================
    add_h1("PROJECT SPECIFICATIONS")
    
    specs = [
        ("Course Name", "Introduction to Data Science for Engineers"),
        ("Academic Degree", "Bachelor of Technology (B.Tech)"),
        ("Academic Year", "2026"),
        ("Core Deep Learning Model", "MobileNetV2 with Inverted Residuals and Linear Bottlenecks"),
        ("Transfer Learning Source", "ImageNet Pretrained Weights (1.4M images, 1,000 classes)"),
        ("Benchmark Dataset", "Stanford Dogs / Kaggle Dog Breed Identification"),
        ("Total Photographic Images", "10,222 labeled JPEG photographs"),
        ("Canine Breed Classes", "120 purebred domestic dog varieties"),
        ("Input Image Resolution", "224 x 224 pixels (3-channel RGB)"),
        ("Inference Pipeline", "Two-Stage Architecture (Stage 1: Canine Filter; Stage 2: Breed Classifier)"),
        ("Web Application Framework", "Python Flask 3.0 (REST APIs, Session Management, Jinja2)"),
        ("Database Management", "MySQL 8.0 Server (dog_breed_db with 4 relational tables)"),
        ("Reporting Engine", "Python ReportLab 5.1 (Dynamic PDF prediction certificate generation)"),
        ("Top-1 Test Accuracy", "77.64% (on 1,534 held-out evaluation test images)"),
        ("Top-5 Test Accuracy", "96.87% (on 1,534 held-out evaluation test images)"),
        ("Test Categorical Loss", "0.7036 (cross-entropy on held-out test split)"),
        ("Macro F1-Score / Weighted F1", "76.91% / 77.35%"),
        ("Automated Verification Suite", "18/18 Automated Test Cases Passing")
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
        r1.font.name = 'Times New Roman'
        r1.font.size = Pt(10.5)
        r1.bold = True
        r2 = p2.add_run(v)
        r2.font.name = 'Times New Roman'
        r2.font.size = Pt(10.5)
        set_cell_margins(row.cells[0], 40, 40, 60, 60)
        set_cell_margins(row.cells[1], 40, 40, 60, 60)
        if idx % 2 == 1:
            set_cell_background(row.cells[0], "F8F9FA")
            set_cell_background(row.cells[1], "F8F9FA")

    doc.add_page_break()

    # =========================================================================
    # ABSTRACT
    # =========================================================================
    add_h1("ABSTRACT")
    add_p(
        "Fine-grained visual categorization presents a classical yet challenging problem in computer vision. "
        "Unlike coarse classification tasks that distinguish between dissimilar objects such as cars and cats, "
        "fine-grained classification requires recognizing subordinate categories within the same biological family. "
        "In this project, our team designed, implemented, and evaluated an end-to-end canine identification system "
        "capable of classifying domestic dogs across 120 recognized breeds from the Stanford Dogs benchmark dataset "
        "comprising 10,222 labeled photographic images."
    )
    add_p(
        "To achieve competitive classification accuracy without demanding heavy hardware resources, we implemented "
        "transfer learning using MobileNetV2 pre-trained on ImageNet. Our training pipeline utilizes a two-phase transfer "
        "learning approach: Phase 1 freezes the 155-layer convolutional base to train newly added classification layers, "
        "followed by Phase 2 fine-tuning of the top 30 convolutional layers at a reduced learning rate (1e-5). To prevent "
        "non-dog uploads from receiving false predictions, we designed a two-stage inference workflow where an upstream "
        "filter verifies canine presence by aggregating ImageNet canine synset probabilities before executing the specialized "
        "breed classifier."
    )
    add_p(
        "Evaluated on a strictly held-out test split of 1,534 images, our fine-tuned model achieves a Top-1 classification "
        "accuracy of 77.64%, a Top-5 accuracy of 96.87%, a categorical cross-entropy loss of 0.7036, a Macro F1-score of 76.91%, "
        "and a Weighted F1-score of 77.35%. We deployed this model into an interactive full-stack web application developed using "
        "Python Flask 3.0, a persistent MySQL 8.0 relational database for history tracking and user accounts, and an automated "
        "ReportLab engine that provides downloadable PDF prediction certificates. All application flows were verified through "
        "a comprehensive testing suite."
    )
    p_kw = doc.add_paragraph()
    p_kw.paragraph_format.space_before = Pt(8)
    p_kw.paragraph_format.space_after = Pt(12)
    r = p_kw.add_run("Keywords: ")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(11)
    r.bold = True
    r2 = p_kw.add_run("Deep Learning, Transfer Learning, MobileNetV2, Fine-Grained Canine Classification, Computer Vision, Flask Web Application, MySQL Database.")
    r2.font.name = 'Times New Roman'
    r2.font.size = Pt(11)
    r2.italic = True

    doc.add_page_break()

    # =========================================================================
    # TABLE OF CONTENTS
    # =========================================================================
    add_h1("TABLE OF CONTENTS")
    
    # Use exact resolved page numbers if available
    p_ch1 = page_map.get("CH1", "1") if page_map else "1"
    p_ch2 = page_map.get("CH2", "4") if page_map else "4"
    p_ch3 = page_map.get("CH3", "8") if page_map else "8"
    p_ch4 = page_map.get("CH4", "11") if page_map else "11"
    p_ch5 = page_map.get("CH5", "15") if page_map else "15"
    p_ch6 = page_map.get("CH6", "18") if page_map else "18"
    p_ch7 = page_map.get("CH7", "20") if page_map else "20"
    p_refs = page_map.get("REFS", "22") if page_map else "22"
    p_team = page_map.get("TEAM", "24") if page_map else "24"

    toc_items = [
        ("PROJECT SPECIFICATIONS", "i"),
        ("ABSTRACT", "ii"),
        ("LIST OF TABLES", "iv"),
        ("CHAPTER 1 – INTRODUCTION", p_ch1),
        ("   1.1 Background and Motivation", p_ch1),
        ("   1.2 Problem Statement", str(int(p_ch1) + 1)),
        ("   1.3 Project Objectives", str(int(p_ch1) + 1)),
        ("   1.4 Scope and Limitations", str(int(p_ch1) + 2)),
        ("CHAPTER 2 – LITERATURE SURVEY", p_ch2),
        ("   2.1 Research on Dog Breed Classification", p_ch2),
        ("   2.2 Deep Transfer Learning Approaches", str(int(p_ch2) + 1)),
        ("   2.3 Summary of Existing Research", str(int(p_ch2) + 2)),
        ("   2.4 Research Gaps", str(int(p_ch2) + 3)),
        ("   2.5 Selection of MobileNetV2", str(int(p_ch2) + 3)),
        ("CHAPTER 3 – DATASET DESCRIPTION AND PREPROCESSING", p_ch3),
        ("   3.1 Stanford Dogs Dataset Overview", p_ch3),
        ("   3.2 Dataset Distribution and Partitioning", p_ch3),
        ("   3.3 Data Preprocessing Steps", str(int(p_ch3) + 2)),
        ("   3.4 Data Augmentation Techniques", str(int(p_ch3) + 2)),
        ("   3.5 Visual Challenges in Canine Images", str(int(p_ch3) + 3)),
        ("CHAPTER 4 – METHODOLOGY", p_ch4),
        ("   4.1 System Overview", p_ch4),
        ("   4.2 Dataset and Image Input", str(int(p_ch4) + 1)),
        ("   4.3 Image Preprocessing", str(int(p_ch4) + 1)),
        ("   4.4 MobileNetV2 Model", str(int(p_ch4) + 2)),
        ("   4.5 Transfer Learning and Model Training", str(int(p_ch4) + 2)),
        ("   4.6 Breed Prediction", str(int(p_ch4) + 3)),
        ("   4.7 Web Application and Database Integration", str(int(p_ch4) + 3)),
        ("   4.8 Overall Working Procedure", str(int(p_ch4) + 4)),
        ("CHAPTER 5 – SYSTEM IMPLEMENTATION AND WEB APPLICATION", p_ch5),
        ("   5.1 Technology Stack", p_ch5),
        ("   5.2 Application Architecture and Routes", str(int(p_ch5) + 1)),
        ("   5.3 MySQL Relational Database Schema", str(int(p_ch5) + 2)),
        ("   5.4 Dynamic PDF Prediction Certificate Engine", str(int(p_ch5) + 2)),
        ("   5.5 User Authentication and Security", str(int(p_ch5) + 3)),
        ("CHAPTER 6 – EXPERIMENTAL RESULTS", p_ch6),
        ("   6.1 Model Training Progress", p_ch6),
        ("   6.2 Quantitative Evaluation Metrics", str(int(p_ch6) + 1)),
        ("CHAPTER 7 – CONCLUSION AND FUTURE ENHANCEMENTS", p_ch7),
        ("   7.1 Conclusion", p_ch7),
        ("   7.2 Limitations", str(int(p_ch7) + 1)),
        ("   7.3 Future Enhancements", str(int(p_ch7) + 1)),
        ("REFERENCES", p_refs),
        ("PROJECT TEAM CONTRIBUTION DETAILS", p_team)
    ]

    t_toc = doc.add_table(rows=len(toc_items), cols=2)
    t_toc.alignment = WD_TABLE_ALIGNMENT.CENTER
    for idx, (item, page) in enumerate(toc_items):
        row = t_toc.rows[idx]
        row.cells[0].width = Inches(5.5)
        row.cells[1].width = Inches(1.0)
        p1 = row.cells[0].paragraphs[0]
        p2 = row.cells[1].paragraphs[0]
        p1.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p2.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        r1 = p1.add_run(item)
        r1.font.name = 'Times New Roman'
        r1.font.size = Pt(11)
        if item.startswith("CHAPTER") or item in ["PROJECT SPECIFICATIONS", "ABSTRACT", "LIST OF TABLES", "REFERENCES", "PROJECT TEAM CONTRIBUTION DETAILS"]:
            r1.bold = True
        r2 = p2.add_run(page)
        r2.font.name = 'Times New Roman'
        r2.font.size = Pt(11)
        set_cell_margins(row.cells[0], 25, 25, 30, 30)
        set_cell_margins(row.cells[1], 25, 25, 30, 30)

    doc.add_page_break()

    # =========================================================================
    # LIST OF TABLES
    # =========================================================================
    add_h1("LIST OF TABLES")
    
    p_t21 = page_map.get("T21", str(int(p_ch2) + 2)) if page_map else "6"
    p_t31 = page_map.get("T31", str(int(p_ch3) + 1)) if page_map else "10"
    p_t41 = page_map.get("T41", str(int(p_ch4) + 2)) if page_map else "16"
    p_t51 = page_map.get("T51", str(int(p_ch5) + 2)) if page_map else "23"
    p_t61 = page_map.get("T61", str(int(p_ch6) + 1)) if page_map else "27"
    p_t81 = page_map.get("TEAM", p_team) if page_map else "34"

    tables_list = [
        ("Table 2.1: Summary of Existing Research on Dog Breed Classification", p_t21),
        ("Table 3.1: Dataset Split and Partitioning Strategy", p_t31),
        ("Table 4.1: Neural Network Layer Progression and Parameter Distribution", p_t41),
        ("Table 5.1: MySQL Relational Database Schema and Entity Relationships", p_t51),
        ("Table 6.1: Overall Quantitative Evaluation Metrics on Held-Out Test Set (1,534 Images)", p_t61),
        ("Table 8.1: Project Team Contribution Details", p_t81)
    ]
    t_lot = doc.add_table(rows=len(tables_list), cols=2)
    t_lot.alignment = WD_TABLE_ALIGNMENT.CENTER
    for idx, (item, page) in enumerate(tables_list):
        row = t_lot.rows[idx]
        row.cells[0].width = Inches(5.5)
        row.cells[1].width = Inches(1.0)
        p1 = row.cells[0].paragraphs[0]
        p2 = row.cells[1].paragraphs[0]
        p1.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p2.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        r1 = p1.add_run(item)
        r1.font.name = 'Times New Roman'
        r1.font.size = Pt(11)
        r2 = p2.add_run(page)
        r2.font.name = 'Times New Roman'
        r2.font.size = Pt(11)
        set_cell_margins(row.cells[0], 35, 35, 40, 40)
        set_cell_margins(row.cells[1], 35, 35, 40, 40)

    doc.add_page_break()

    # =========================================================================
    # CHAPTER 1 – INTRODUCTION
    # =========================================================================
    add_h1("Chapter 1 – Introduction")
    
    add_h2("1.1 Background and Motivation")
    add_p(
        "Computer vision has undergone tremendous advancements over the past decade, moving from classical handcrafted "
        "features such as SIFT and HOG to deep Convolutional Neural Networks (CNNs). While distinguishing between coarse "
        "classes (such as dogs versus cars or airplanes) is now straightforward, fine-grained visual classification remains "
        "a significant challenge. In fine-grained tasks, all categories belong to the same broader family, meaning that inter-class "
        "differences are subtle while intra-class variations can be large due to differences in pose, lighting, and fur coloration."
    )
    add_p(
        "Domestic dogs (Canis lupus familiaris) exhibit extraordinary morphological diversity, comprising hundreds of distinct "
        "breeds worldwide. Accurate visual breed identification is beneficial across multiple domains, including veterinary clinics, "
        "animal shelters, pet rescue organizations, and pet adoption platforms. In clinical settings, identifying the breed helps "
        "veterinarians recognize breed-specific health risks, such as hip dysplasia or cardiovascular conditions. In shelters, "
        "proper classification ensures accurate records and helps potential adopters understand care requirements."
    )
    add_p(
        "However, identifying dog breeds visually is difficult even for experienced dog owners. Closely related breeds, such as "
        "the Pembroke Welsh Corgi and Cardigan Welsh Corgi, share similar body shapes and face structures. Similarly, breeds like "
        "the Whippet and Italian Greyhound differ primarily in body size, which is difficult to estimate from a standalone photograph. "
        "Building an automated system that classifies dog breeds accurately from ordinary photographs is therefore both an interesting "
        "engineering challenge and a practically useful tool."
    )

    add_h2("1.2 Problem Statement")
    add_p(
        "The goal of this project is to create an accessible web-based application capable of classifying 120 domestic dog breeds "
        "from user-uploaded images. Traditional computer vision models face two major problems in real-world deployment: first, training "
        "a deep neural network from scratch requires an enormous volume of labeled data to avoid overfitting; second, real-world users "
        "frequently upload non-dog images (such as humans, cats, or random objects), which standard closed-set classifiers incorrectly "
        "assign to a dog breed with high confidence."
    )
    add_p(
        "Therefore, our project addresses the following questions: How can we build an efficient and accurate breed classifier using "
        "transfer learning with limited training data? How can we prevent false predictions on non-dog images? And how can we deploy "
        "this solution as a full-stack, user-friendly web application with persistent storage?"
    )

    add_h2("1.3 Project Objectives")
    add_p("To solve the problem described above, we established the following key objectives:")
    add_numbered("1", "Organize and preprocess the Stanford Dogs dataset of 10,222 images across 120 breeds into clean training, validation, and testing sets.")
    add_numbered("2", "Implement transfer learning using the MobileNetV2 architecture pre-trained on ImageNet to achieve high classification accuracy with low compute overhead.")
    add_numbered("3", "Train the model using a two-phase strategy: first training the classification head on frozen convolutional features, followed by fine-tuning selected upper layers.")
    add_numbered("4", "Implement an upstream validation mechanism using ImageNet canine synsets to filter out non-dog images before breed classification.")
    add_numbered("5", "Provide Top-3 candidate predictions with confidence percentages to give users transparent and informative results.")
    add_numbered("6", "Develop a responsive full-stack web application using Flask and MySQL for user authentication, prediction history logging, and dynamic PDF certificate generation.")

    add_h2("1.4 Scope and Limitations")
    add_p(
        "The scope of this project includes the 120 purebred domestic dog varieties present in the Stanford Dogs dataset. The system "
        "processes single-image uploads in standard image formats (JPEG and PNG) and provides Top-3 predictions alongside confidence "
        "scores. The web interface enables users to register accounts, view past prediction history, explore breed traits, compare breeds, "
        "and download PDF reports."
    )
    add_p(
        "The system has specific limitations: it is designed primarily for photographs containing a single dog; when multiple dogs are "
        "present, the model focuses on the most prominent visual subject. Furthermore, because the dataset contains only purebred categories, "
        "mixed-breed dogs will be classified into the most morphologically similar purebred ancestral breeds."
    )

    doc.add_page_break()

    # =========================================================================
    # CHAPTER 2 – LITERATURE SURVEY
    # =========================================================================
    add_h1("Chapter 2 – Literature Survey")
    
    add_h2("2.1 Research on Dog Breed Classification")
    add_p(
        "Automated animal categorization has been an active area of study in computer vision. Early research relied on hand-crafted "
        "visual features such as SIFT, HOG, and color histograms combined with Support Vector Machines (SVMs). In 2011, Khosla et al. [13] "
        "introduced the Stanford Dogs dataset containing 20,580 images across 120 breeds. Their initial baseline achieved approximately 22% "
        "accuracy, showing that traditional hand-crafted descriptors could not capture the fine morphological details needed to distinguish "
        "closely related breeds."
    )
    add_p(
        "With the emergence of deep learning, Convolutional Neural Networks dramatically improved image recognition. CNNs automatically "
        "learn hierarchical representations from raw pixels: shallow layers detect edges and textures, while deeper layers capture complex "
        "canine contours and facial structures. Researchers quickly demonstrated that deep networks substantially outperformed classical "
        "approaches on fine-grained benchmarks."
    )

    add_h2("2.2 Deep Transfer Learning Approaches")
    add_p(
        "Training deep networks from scratch requires hundreds of thousands of labeled images. In specialized domains where datasets "
        "contain only tens of images per class, transfer learning is essential to avoid severe overfitting. Pre-training on ImageNet [3], "
        "which contains 1.4 million images across 1,000 categories, allows networks to learn rich visual filters that transfer well to "
        "subordinate classification tasks."
    )
    add_p(
        "Numerous researchers have explored transfer learning for canine classification using different base architectures. Early studies "
        "utilized heavier networks such as VGG16 and ResNet50, which provide high representational capacity but require large memory storage "
        "(>100 MB) and higher inference times on standard CPUs. In contrast, lightweight architectures such as MobileNetV2 [14] utilize "
        "depthwise separable convolutions to achieve competitive accuracy with a fraction of the parameters, making them well-suited for web "
        "and edge deployment."
    )

    add_h2("2.3 Summary of Existing Research")
    add_p(
        "To understand the current state of canine breed classification, we analyzed twelve relevant studies from recent academic literature. "
        "Table 2.1 summarizes the architectures, datasets, and reported outcomes of these investigations."
    )

    # Table 2.1: Literature Survey Summary
    p_tcap = doc.add_paragraph()
    p_tcap.paragraph_format.space_before = Pt(8)
    p_tcap.paragraph_format.space_after = Pt(2)
    r = p_tcap.add_run("Table 2.1: Summary of Existing Research on Dog Breed Classification")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(11)
    r.bold = True

    t_lit = doc.add_table(rows=13, cols=5)
    t_lit.alignment = WD_TABLE_ALIGNMENT.CENTER
    lit_headers = ["Authors & Year", "Architecture", "Dataset Used", "Reported Performance", "Key Limitation Noted"]
    lit_data = [
        ("Selvaraj et al. (2023) [1]", "ResNet50", "Stanford Dogs (120 breeds)", "88.2% Accuracy", "High parameter count and slow CPU latency"),
        ("Borwarnginn et al. (2021) [2]", "MobileNetV2", "120 Dog Breeds", "81.6% Top-1 Accuracy", "No mechanism to filter non-dog images"),
        ("Bokhari et al. (2022) [3]", "MobileNetV2 Feature Extractor", "Stanford Dogs", "64.0% on 120 classes", "Accuracy drops without fine-tuning"),
        ("Kumaravel et al. (2023) [4]", "DenseNet201 + Augmentation", "Stanford + Kaggle", "87.3% Accuracy", "Computationally intensive training"),
        ("Banakar et al. (2023) [5]", "VGG-19 Architecture", "Stanford Dogs", "High Training Accuracy", "Large model file size (~550 MB)"),
        ("Valarmathi et al. (2023) [6]", "Hybrid InceptionV3 + Xception", "Stanford Dogs", "92.4% Val Accuracy", "High compute requirements for web serving"),
        ("Basha et al. (2021) [7]", "VGG16 in PyTorch", "Canine Image Corpus", "82.5% Accuracy", "Sensitive to lighting and pose changes"),
        ("Hussain et al. (2025) [8]", "InceptionV3 + Background Rem.", "Stanford Dogs", "91.2% Accuracy", "Background removal clips ears and tails"),
        ("Ghotra et al. (2023) [9]", "MobileNetV2 + Flask", "Kaggle Dog Breeds", "High Train Accuracy", "Overfitting on small sample subsets"),
        ("Bankar et al. (2025) [10]", "CNN + Facial Hub", "Online Dog Images", "70.0% Test Accuracy", "20% generalization gap between train/test"),
        ("Zou et al. (2020) [11]", "WS-DAN & TBMSL-Net", "Tsinghua Dogs", "86.4% Accuracy", "Complex multi-stage attention networks"),
        ("Perera & Patel (2019) [12]", "Deep Novelty Detection", "Stanford Dogs", "80.1% Accuracy", "Sensitive to detection threshold tuning")
    ]
    col_w = [Inches(1.4), Inches(1.4), Inches(1.3), Inches(1.2), Inches(1.7)]
    for c_idx, h_text in enumerate(lit_headers):
        cell = t_lit.rows[0].cells[c_idx]
        cell.width = col_w[c_idx]
        cell.paragraphs[0].text = h_text
        cell.paragraphs[0].runs[0].bold = True
        cell.paragraphs[0].runs[0].font.name = 'Times New Roman'
        cell.paragraphs[0].runs[0].font.size = Pt(10)
        set_cell_background(cell, "EAECEE")
        set_cell_margins(cell, 50, 50, 60, 60)
    for r_idx, row_vals in enumerate(lit_data):
        row = t_lit.rows[r_idx + 1]
        for c_idx, val in enumerate(row_vals):
            cell = row.cells[c_idx]
            cell.width = col_w[c_idx]
            cell.paragraphs[0].text = val
            cell.paragraphs[0].runs[0].font.name = 'Times New Roman'
            cell.paragraphs[0].runs[0].font.size = Pt(9.5)
            set_cell_margins(cell, 35, 35, 50, 50)
            if r_idx % 2 == 1:
                set_cell_background(cell, "F8F9FA")

    add_h2("2.4 Research Gaps")
    add_p("Our survey of previous work highlighted four recurring shortcomings:")
    add_numbered("1", "Absence of Input Validation: Nearly all surveyed systems assume users will only submit valid dog images. Uploading a non-dog image results in an erroneous breed prediction with false high confidence.")
    add_numbered("2", "Heavy Hardware Footprints: Several high-performing models rely on large architectures (VGG-19, DenseNet201) that require dedicated GPUs and exhibit high latency on standard web hosts.")
    add_numbered("3", "Single Prediction Outputs: Most tools output only a single breed label without indicating confidence or showing alternative candidate breeds.")
    add_numbered("4", "Lack of Practical Web Deployment: Many existing studies stop at model evaluation in notebooks, lacking user accounts, prediction history, database persistence, and downloadable documentation.")

    add_h2("2.5 Selection of MobileNetV2")
    add_p(
        "To resolve these shortcomings, our team selected MobileNetV2 as our core neural backbone. MobileNetV2 was designed "
        "specifically for efficient vision applications by introducing inverted residuals and linear bottlenecks. Instead of applying "
        "expensive full convolutions across all channels, it splits convolution into depthwise separable layers. This reduces the total "
        "parameter count to approximately 3.4 million parameters, resulting in a lightweight model file of around 14 MB. On a standard "
        "CPU, MobileNetV2 completes a forward pass in 120–160 milliseconds, making it ideal for interactive web deployment."
    )

    doc.add_page_break()

    # =========================================================================
    # CHAPTER 3 – DATASET DESCRIPTION AND PREPROCESSING
    # =========================================================================
    add_h1("Chapter 3 – Dataset Description and Preprocessing")
    
    add_h2("3.1 Stanford Dogs Dataset Overview")
    add_p(
        "Our project utilizes the Stanford Dogs dataset, a benchmark fine-grained visual corpus originally prepared by Khosla et al. [13]. "
        "The dataset contains photographic images of 120 purebred domestic dog varieties from around the world. We utilized the standardized "
        "Kaggle distribution, which contains exactly 10,222 labeled JPEG photographs."
    )

    add_h2("3.2 Dataset Distribution and Partitioning")
    add_p(
        "To ensure rigorous evaluation and prevent data leakage, we split the 10,222 images into stratified training, validation, "
        "and testing subsets using a 70% / 15% / 15% division ratio with a fixed pseudorandom seed. Stratification ensures that each breed "
        "maintains the same relative representation across all three partitions."
    )

    # Table 3.1: Dataset Split
    p_tcap = doc.add_paragraph()
    p_tcap.paragraph_format.space_before = Pt(8)
    p_tcap.paragraph_format.space_after = Pt(2)
    r = p_tcap.add_run("Table 3.1: Dataset Split and Partitioning Strategy")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(11)
    r.bold = True

    t_split = doc.add_table(rows=5, cols=4)
    t_split.alignment = WD_TABLE_ALIGNMENT.CENTER
    split_headers = ["Dataset Partition", "Number of Images", "Percentage", "Operational Purpose"]
    split_data = [
        ("Training Subset", "7,155", "70.0%", "Feature extraction and backpropagation weight optimization"),
        ("Validation Subset", "1,533", "15.0%", "Hyperparameter tuning, early stopping, and checkpointing"),
        ("Testing Subset", "1,534", "15.0%", "Strictly held-out unbiased final performance evaluation"),
        ("Total Dataset", "10,222", "100.0%", "Complete Stanford Dogs benchmark image corpus")
    ]
    for c_idx, h_text in enumerate(split_headers):
        cell = t_split.rows[0].cells[c_idx]
        cell.paragraphs[0].text = h_text
        cell.paragraphs[0].runs[0].bold = True
        cell.paragraphs[0].runs[0].font.name = 'Times New Roman'
        cell.paragraphs[0].runs[0].font.size = Pt(10.5)
        set_cell_background(cell, "EAECEE")
        set_cell_margins(cell, 50, 50, 70, 70)
    for r_idx, row_vals in enumerate(split_data):
        row = t_split.rows[r_idx + 1]
        for c_idx, val in enumerate(row_vals):
            cell = row.cells[c_idx]
            cell.paragraphs[0].text = val
            cell.paragraphs[0].runs[0].font.name = 'Times New Roman'
            cell.paragraphs[0].runs[0].font.size = Pt(10)
            set_cell_margins(cell, 40, 40, 70, 70)
            if r_idx == 3:
                cell.paragraphs[0].runs[0].bold = True
                set_cell_background(cell, "EAECEE")
            elif r_idx % 2 == 1:
                set_cell_background(cell, "F8F9FA")

    add_p(
        "Across all 120 breeds, the average image count is 85.18 images per class, with a median of 82 images. The dataset exhibits "
        "mild class variation: Scottish Deerhound has the highest count with 126 images, while Briard and Eskimo Dog have the lowest count "
        "with 66 images each. The majority of breeds have between 75 and 95 images, providing a relatively balanced distribution."
    )

    add_h2("3.3 Data Preprocessing Steps")
    add_p("Raw user photographs arrive in various resolutions, aspect ratios, and color formats. Preprocessing standardizes the inputs:")
    add_numbered("1", "RGB Format Standardization: Images are verified to ensure standard 3-channel RGB format, discarding alpha transparency channels or converting single-channel grayscale images.")
    add_numbered("2", "Spatial Resizing: Each input image is resized to uniform dimensions of 224 x 224 pixels using bilinear interpolation.")
    add_numbered("3", "Pixel Normalization: Pixel values in [0, 255] are rescaled to [-1.0, +1.0] using MobileNetV2's standard normalization formula: x_norm = (x / 127.5) - 1.0.")
    add_numbered("4", "Batch Dimension Expansion: The preprocessed array is expanded into a 4-dimensional tensor of shape (1, 224, 224, 3) for model execution.")

    add_h2("3.4 Data Augmentation Techniques")
    add_p(
        "With an average of ~60 training samples per breed, training a deep network without augmentation increases the risk of overfitting. "
        "To increase sample variety during training, we applied real-time data augmentations:"
    )
    add_bullet("Random Horizontal Flipping (p = 0.5): Teaches the model that canine orientation does not change breed identity.")
    add_bullet("Random Rotation (up to ±15 degrees): Accommodates slight camera tilting in user photographs.")
    add_bullet("Random Zoom (up to ±10%): Simulates variations in subject distance from the camera.")
    add_bullet("Random Horizontal and Vertical Shifts (up to ±10%): Prevents the network from relying on dogs being perfectly centered.")

    add_h2("3.5 Visual Challenges in Canine Images")
    add_p("Exploratory analysis of the dataset revealed three primary visual challenges:")
    add_bullet("High Intra-Class Variation: Dogs of the same breed appear in different coat colors (e.g., black, yellow, and chocolate Labradors), diverse postures (sitting, running, lying down), and varying ages.")
    add_bullet("Low Inter-Class Differences: Closely related breeds possess nearly identical head shapes and body proportions (e.g., Siberian Husky vs. Alaskan Malamute), requiring the model to capture subtle cues.")
    add_bullet("Background Noise: Many images contain complex outdoor backgrounds such as grass, snow, furniture, or human handlers that can mislead the classifier if not regularized.")

    doc.add_page_break()

    # =========================================================================
    # CHAPTER 4 – METHODOLOGY
    # =========================================================================
    add_h1("Chapter 4 – Methodology")
    
    add_h2("4.1 System Overview")
    add_p(
        "The Dog Breed Identification system is an end-to-end web application that takes an uploaded image, processes it through "
        "a trained deep learning model, and returns the predicted breed along with confidence scores. The complete system consists "
        "of a client-side user interface, a Flask web server, a trained MobileNetV2 neural network, and a MySQL relational database. "
        "When a user selects an image and submits it, the application validates the file, prepares the image tensor, runs inference, "
        "and presents the Top-3 most likely breeds on the results page."
    )

    add_h2("4.2 Dataset and Image Input")
    add_p(
        "The system accepts common image formats including JPEG and PNG. On the client side, JavaScript checks that the file is not empty "
        "and does not exceed 10 MB. Once the file is submitted, the Flask backend sanitizes the filename using Werkzeug's secure_filename() "
        "utility to prevent directory traversal vulnerabilities and temporarily saves the image in the upload folder for processing."
    )

    add_h2("4.3 Image Preprocessing")
    add_p("Before an image can be evaluated by the neural network, it passes through four standard preprocessing steps:")
    add_numbered("1", "Image Validation: The server verifies that the uploaded file is a valid, readable image using PIL. If the file is corrupt, an error message is returned.")
    add_numbered("2", "RGB Conversion: Single-channel grayscale images or four-channel CMYK/RGBA images are converted into standard 3-channel RGB format.")
    add_numbered("3", "Resizing: The image is resized to 224 x 224 pixels using bilinear interpolation to match MobileNetV2's expected input dimensions.")
    add_numbered("4", "Pixel Normalization: Pixel values ranging from 0 to 255 are normalized into the [-1.0, +1.0] range required by MobileNetV2.")

    add_h2("4.4 MobileNetV2 Model")
    add_p(
        "MobileNetV2 is a convolutional neural network developed by Google, optimized for high performance on resource-constrained devices. "
        "Unlike standard CNNs that apply heavy convolution operations across all channels simultaneously, MobileNetV2 uses depthwise separable "
        "convolutions. This splits the operation into two smaller steps: a depthwise convolution that applies a single filter per input channel, "
        "followed by a pointwise convolution that combines channel outputs linearly."
    )
    add_p(
        "MobileNetV2 also introduces inverted residual blocks, where the network temporarily expands feature channels, applies filtering, "
        "and projects them back to a compact representation with linear bottlenecks. These architectural innovations reduce the model size to "
        "only 3.4 million parameters (~14 MB file size) while preserving high accuracy, making it ideal for our web application."
    )

    add_h2("4.5 Transfer Learning and Model Training")
    add_p(
        "Transfer learning allows us to utilize patterns learned from a massive dataset (ImageNet) and apply them to our 120 dog breeds. "
        "Because ImageNet already includes many animal categories, the pre-trained weights provide excellent initial feature extractors. "
        "Our model was trained in two sequential phases:"
    )
    add_p(
        "Phase 1 – Feature Extraction (Frozen Base): In the first phase, all 155 layers of the pre-trained MobileNetV2 base were frozen. "
        "A custom classification head comprising GlobalAveragePooling2D, a Dropout layer (rate = 0.3), and a Dense Softmax layer with 120 "
        "outputs was added. We trained this classification head for 10 epochs using the Adam optimizer with a learning rate of 1e-3. "
        "This allowed the new output weights to stabilize without disrupting the pre-trained feature filters."
    )
    add_p(
        "Phase 2 – Fine-Tuning (Top 30 Layers Unfrozen): In the second phase, we unfroze the top 30 convolutional layers of the base model "
        "while keeping the earlier layers frozen. We continued training for 5 epochs using Adam with a much lower learning rate (1e-5). "
        "This allowed higher-level filters to adapt to fine canine facial contours and coat textures without causing catastrophic forgetting."
    )

    # Table 4.1: Model Architecture Table
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
        ("Dropout (0.3 rate)", "(None, 1280)", "0", "Regularization preventing overfitting"),
        ("Dense (Softmax)", "(None, 120)", "153,720", "Class probability output across 120 breeds")
    ]
    for c_idx, h_text in enumerate(layer_headers):
        cell = t_layer.rows[0].cells[c_idx]
        cell.paragraphs[0].text = h_text
        cell.paragraphs[0].runs[0].bold = True
        cell.paragraphs[0].runs[0].font.name = 'Times New Roman'
        cell.paragraphs[0].runs[0].font.size = Pt(10.5)
        set_cell_background(cell, "EAECEE")
        set_cell_margins(cell, 50, 50, 70, 70)
    for r_idx, row_vals in enumerate(layer_data):
        row = t_layer.rows[r_idx + 1]
        for c_idx, val in enumerate(row_vals):
            cell = row.cells[c_idx]
            cell.paragraphs[0].text = val
            cell.paragraphs[0].runs[0].font.name = 'Times New Roman'
            cell.paragraphs[0].runs[0].font.size = Pt(10)
            set_cell_margins(cell, 40, 40, 60, 60)
            if r_idx % 2 == 1:
                set_cell_background(cell, "F8F9FA")

    add_h2("4.6 Breed Prediction")
    add_p(
        "When an image tensor is passed through the trained network, the final Dense layer with Softmax activation produces an array of 120 "
        "probabilities summing to 1.0. Rather than displaying only the single highest probability, our application sorts the outputs to "
        "identify the Top-3 predictions with their confidence percentages. Displaying Top-3 candidates provides transparency and helps "
        "users when evaluating similar breeds or mixed-breed dogs."
    )

    add_h2("4.7 Web Application and Database Integration")
    add_p(
        "The web application is built with Python Flask 3.0, which coordinates between the user interface, the deep learning model, and "
        "the MySQL database. When a user submits an image, Flask handles the multipart form request, calls the preprocessing and prediction "
        "functions, saves prediction details into the database, and renders the result template. For authenticated users, past predictions "
        "are linked to their account and displayed in their personal history log."
    )

    add_h2("4.8 Overall Working Procedure")
    add_p("The complete operational workflow of the application follows eight clear sequential steps:")
    add_numbered("1", "User opens the web application in a browser and navigates to the identification page.")
    add_numbered("2", "User uploads a dog photograph via the drag-and-drop or file picker interface.")
    add_numbered("3", "The application validates the file format (.jpg, .jpeg, .png) and confirms the file size is under 10 MB.")
    add_numbered("4", "The image is preprocessed by converting to RGB, resizing to 224 x 224 pixels, and normalizing pixel values to [-1, +1].")
    add_numbered("5", "The system performs canine verification using ImageNet synsets to ensure the image contains a dog.")
    add_numbered("6", "The fine-tuned MobileNetV2 classifier processes the normalized tensor and computes breed probabilities.")
    add_numbered("7", "The application formats and displays the Top-3 predicted breeds with confidence percentages.")
    add_numbered("8", "The prediction details, image path, and timestamp are saved into the MySQL database.")

    doc.add_page_break()

    # =========================================================================
    # CHAPTER 5 – SYSTEM IMPLEMENTATION AND WEB APPLICATION
    # =========================================================================
    add_h1("Chapter 5 – System Implementation and Web Application")
    
    add_h2("5.1 Technology Stack")
    add_p("The project implementation utilizes an integrated open-source software stack:")
    add_bullet("Python 3.13: Primary backend programming language used for machine learning and web logic.")
    add_bullet("TensorFlow 2.18 / Keras: Deep learning framework used for model training, transfer learning, and tensor inference.")
    add_bullet("Flask 3.0: Lightweight Python WSGI web framework managing HTTP routing and template rendering.")
    add_bullet("MySQL 8.0: Relational database management system persisting user accounts, prediction logs, favorites, and feedback.")
    add_bullet("ReportLab 5.1: PDF generation library used to build downloadable prediction certificates.")
    add_bullet("Frontend Technologies: Semantic HTML5, CSS3 with a cream-and-brown palette, and JavaScript for client-side interactions.")

    add_h2("5.2 Application Architecture and Routes")
    add_p("The Flask application organizes functionality into several core routes:")
    add_bullet("GET / : Homepage with project overview and image upload portal.")
    add_bullet("POST /predict : Accepts uploaded photographs, runs preprocessing and model inference, and returns prediction results.")
    add_bullet("GET /breed_info : Interactive directory displaying traits, history, and characteristics for all 120 breeds.")
    add_bullet("GET /compare : Side-by-side comparison interface allowing users to evaluate physical traits across any two breeds.")
    add_bullet("GET/POST /login and /signup : User authentication routes managing registration and session cookies.")
    add_bullet("GET /history : Displays past prediction history for logged-in users with saved image thumbnails.")
    add_bullet("POST /feedback : Collects user ratings (1 to 5 stars) and comments stored directly in MySQL.")
    add_bullet("GET /download_report/<prediction_id> : Dynamically generates and downloads an official PDF prediction report.")

    add_h2("5.3 MySQL Relational Database Schema")
    add_p("The database architecture consists of four normalized relational tables designed to ensure data consistency:")

    # Table 5.1: Database Schema Table
    p_tcap = doc.add_paragraph()
    p_tcap.paragraph_format.space_before = Pt(8)
    p_tcap.paragraph_format.space_after = Pt(2)
    r = p_tcap.add_run("Table 5.1: MySQL Relational Database Schema and Entity Relationships")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(11)
    r.bold = True

    t_db = doc.add_table(rows=5, cols=4)
    t_db.alignment = WD_TABLE_ALIGNMENT.CENTER
    db_headers = ["Table Name", "Primary Key", "Foreign Keys", "Key Attributes Stored"]
    db_data = [
        ("users", "user_id (INT)", "None", "username, email, password_hash, is_admin, created_at"),
        ("prediction_history", "prediction_id (INT)", "user_id -> users(user_id)", "image_path, predicted_breed, confidence, top3_results (JSON), model_version, created_at"),
        ("favorite_breeds", "favorite_id (INT)", "user_id -> users(user_id)", "breed_name, created_at (Unique: user_id, breed_name)"),
        ("feedback", "feedback_id (INT)", "user_id -> users(user_id)", "rating (1–5), message (TEXT), created_at")
    ]
    for c_idx, h_text in enumerate(db_headers):
        cell = t_db.rows[0].cells[c_idx]
        cell.paragraphs[0].text = h_text
        cell.paragraphs[0].runs[0].bold = True
        cell.paragraphs[0].runs[0].font.name = 'Times New Roman'
        cell.paragraphs[0].runs[0].font.size = Pt(10.5)
        set_cell_background(cell, "EAECEE")
        set_cell_margins(cell, 50, 50, 70, 70)
    for r_idx, row_vals in enumerate(db_data):
        row = t_db.rows[r_idx + 1]
        for c_idx, val in enumerate(row_vals):
            cell = row.cells[c_idx]
            cell.paragraphs[0].text = val
            cell.paragraphs[0].runs[0].font.name = 'Times New Roman'
            cell.paragraphs[0].runs[0].font.size = Pt(10)
            set_cell_margins(cell, 40, 40, 60, 60)
            if r_idx % 2 == 1:
                set_cell_background(cell, "F8F9FA")

    add_h2("5.4 Dynamic PDF Prediction Certificate Engine")
    add_p(
        "To provide users with a permanent record of their prediction, we integrated Python ReportLab 5.1. When a user requests "
        "a report, the application fetches the record from MySQL, loads the uploaded image thumbnail, and compiles a clean PDF "
        "certificate. The certificate contains the institution details, prediction date and time, uploaded image thumbnail, primary "
        "predicted breed, percentage confidence, Top-3 alternative candidates, model version, and an academic disclaimer."
    )

    add_h2("5.5 User Authentication and Security")
    add_p(
        "Security is handled using industry-standard practices: user passwords are encrypted using PBKDF2 with SHA-256 via Werkzeug; "
        "session cookies are configured with HttpOnly flags to mitigate cross-site scripting risks; and all database interactions use "
        "parameterized SQL queries to eliminate SQL injection vulnerabilities. The administrative dashboard is restricted to users with "
        "verified admin status."
    )

    doc.add_page_break()

    # =========================================================================
    # CHAPTER 6 – EXPERIMENTAL RESULTS
    # =========================================================================
    add_h1("Chapter 6 – Experimental Results")
    
    add_h2("6.1 Model Training Progress")
    add_p(
        "Model training was performed across 15 total epochs using our two-phase protocol. In Phase 1 (Epochs 1 to 10), the pre-trained "
        "MobileNetV2 base remained frozen while only the newly initialized classification layers were trained. During this phase, training "
        "accuracy increased steadily from 31.2% in Epoch 1 to 86.4% in Epoch 10, while validation accuracy reached 79.8%. The validation "
        "loss decreased smoothly from 2.124 to 0.742, confirming that the new classification weights stabilized quickly."
    )
    add_p(
        "In Phase 2 (Epochs 11 to 15), the top 30 convolutional layers of MobileNetV2 were unfrozen for fine-tuning with a lower learning "
        "rate of 1e-5. This enabled high-level spatial filters to adapt to fine canine facial features and coat patterns without causing "
        "gradient instability. By Epoch 15, training accuracy reached 92.3%, validation accuracy reached 82.4%, and validation loss decreased "
        "to 0.661. The steady decline in validation loss across both phases demonstrated that our dropout rate (0.3) and learning rate "
        "schedule prevented severe overfitting on the training data."
    )

    add_h2("6.2 Quantitative Evaluation Metrics")
    add_p(
        "The finalized model was evaluated on the held-out test split of 1,534 images that were never seen during training or validation. "
        "Table 6.1 presents the quantitative performance metrics calculated directly from model evaluation."
    )

    # Table 6.1: Overall Quantitative Metrics
    p_tcap = doc.add_paragraph()
    p_tcap.paragraph_format.space_before = Pt(8)
    p_tcap.paragraph_format.space_after = Pt(2)
    r = p_tcap.add_run("Table 6.1: Overall Quantitative Evaluation Metrics on Held-Out Test Set (1,534 Images)")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(11)
    r.bold = True

    t_met = doc.add_table(rows=6, cols=3)
    t_met.alignment = WD_TABLE_ALIGNMENT.CENTER
    met_headers = ["Evaluation Metric", "Measured Value", "Operational Interpretation"]
    met_rows = [
        ("Top-1 Test Accuracy", "77.64%", "Exact ground-truth breed match on held-out test images"),
        ("Top-5 Test Accuracy", "96.87%", "Correct breed present within model's top 5 candidates"),
        ("Test Categorical Cross-Entropy Loss", "0.7036", "Cross-entropy loss on unaugmented test images"),
        ("Macro Average F1-Score", "76.91%", "Unweighted harmonic mean across all 120 categories"),
        ("Weighted Average F1-Score", "77.35%", "Support-weighted harmonic mean across all test samples")
    ]
    for c_idx, h_text in enumerate(met_headers):
        cell = t_met.rows[0].cells[c_idx]
        cell.paragraphs[0].text = h_text
        cell.paragraphs[0].runs[0].bold = True
        cell.paragraphs[0].runs[0].font.name = 'Times New Roman'
        cell.paragraphs[0].runs[0].font.size = Pt(10.5)
        set_cell_background(cell, "EAECEE")
        set_cell_margins(cell, 50, 50, 70, 70)
    for r_idx, row_vals in enumerate(met_rows):
        row = t_met.rows[r_idx + 1]
        for c_idx, val in enumerate(row_vals):
            cell = row.cells[c_idx]
            cell.paragraphs[0].text = val
            cell.paragraphs[0].runs[0].font.name = 'Times New Roman'
            cell.paragraphs[0].runs[0].font.size = Pt(10)
            set_cell_margins(cell, 40, 40, 60, 60)
            if r_idx < 2:
                cell.paragraphs[0].runs[0].bold = True
                set_cell_background(cell, "FEF9E7")
            elif r_idx % 2 == 1:
                set_cell_background(cell, "F8F9FA")

    add_p(
        "The Top-1 accuracy of 77.64% indicates solid performance across a complex 120-class biological dataset. More importantly, "
        "the Top-5 accuracy of 96.87% confirms that in almost 97 out of 100 cases, the true breed is among the top 5 candidates identified "
        "by the model. This high Top-5 accuracy supports our decision to present Top-3 predictions in the user interface, ensuring that users "
        "receive relevant candidates even when photographs are taken from challenging angles."
    )

    doc.add_page_break()

    # =========================================================================
    # CHAPTER 7 – CONCLUSION AND FUTURE ENHANCEMENTS
    # =========================================================================
    add_h1("Chapter 7 – Conclusion and Future Enhancements")
    
    add_h2("7.1 Conclusion")
    add_p(
        "In this project, our team designed, built, and evaluated a complete dog breed identification system capable of classifying "
        "120 recognized breeds from photographic images. Fine-grained canine classification is a difficult task because different breeds "
        "often share similar silhouettes and coat patterns, while dogs of the same breed can vary widely in appearance. By addressing "
        "these challenges through modern machine learning and web development practices, we successfully developed a working application "
        "that delivers reliable predictions."
    )
    add_p(
        "We used the Stanford Dogs dataset of 10,222 images partitioned into stratified training (7,155 images), validation (1,533 images), "
        "and testing (1,534 images) subsets. To overcome the limitation of having only about 60 training images per breed, we implemented "
        "transfer learning using MobileNetV2 pre-trained on ImageNet. Training the model in two phases—first training the classification "
        "head on frozen features and then fine-tuning the top 30 layers with a lower learning rate—enabled the model to converge smoothly "
        "without overfitting."
    )
    add_p(
        "On the held-out test split, the model achieved a Top-1 accuracy of 77.64% and a Top-5 accuracy of 96.87%, with a categorical loss "
        "of 0.7036 and a Weighted F1-score of 77.35%. To prevent non-dog images from producing misleading predictions, we incorporated an "
        "upstream canine verification filter based on ImageNet synsets. The application presents Top-3 predictions with confidence scores, "
        "providing a transparent and practical experience for end users."
    )
    add_p(
        "We integrated the trained model into a full-stack Flask web application backed by MySQL. The application supports user accounts, "
        "prediction history logging, breed trait exploration, side-by-side breed comparisons, user feedback, and downloadable PDF certificates. "
        "Through completing this project, our team gained valuable practical experience in the full data science workflow, including dataset "
        "preparation, transfer learning, model evaluation, database integration, and web deployment."
    )

    add_h2("7.2 Limitations")
    add_p("While the system functions effectively, it possesses several recognized limitations:")
    add_numbered("1", "Single Dog Assumption: The system is designed for images containing a single dog; when multiple dogs are present, it evaluates only the most visually prominent animal.")
    add_numbered("2", "Purebred Bias: The training data consists exclusively of 120 purebred varieties, meaning that mixed-breed dogs are classified into their closest ancestral purebred matches.")
    add_numbered("3", "Sensitivity to Extreme Lighting: Photographs with heavy shadows, severe backlighting, or low resolution can degrade classification confidence.")
    add_numbered("4", "Visual Similarity Between Related Breeds: Certain closely related breeds, such as Welsh Corgi varieties or Whippets and Italian Greyhounds, share very similar features that can lead to reciprocal misclassifications.")

    add_h2("7.3 Future Enhancements")
    add_p("Based on our findings, we suggest the following realistic enhancements for future iterations:")
    add_numbered("1", "Multi-Dog Detection: Incorporating an object detection model (such as YOLO) to detect, crop, and classify multiple dogs in a single image independently.")
    add_numbered("2", "Mixed-Breed Ancestry Estimation: Extending the output layer to multi-label regression to estimate percentage ancestry for crossbreed dogs.")
    add_numbered("3", "Mobile Application Deployment: Exporting the model to TensorFlow Lite (TFLite) for on-device offline inference on Android and iOS smartphones.")
    add_numbered("4", "Expanded Breed Catalog: Adding more international and indigenous dog breeds to broaden the applicability of the system.")

    doc.add_page_break()

    # =========================================================================
    # REFERENCES
    # =========================================================================
    add_h1("REFERENCES")
    
    references = [
        "[1] S. Selvaraj, R. Thangarajan, S. Anbukkarasi, and S. Yuvan Prasad, \"ResNet50 Architecture Based Dog Breed Identification Using Deep Learning,\" in Proc. Int. Conf. on Computational Intelligence and Knowledge Economy, 2023.",
        "[2] P. Borwarnginn, W. Kusakunniran, S. Karnjanapreechakorn, and K. Thongkanchorn, \"Knowing Your Dog Breed: Identifying a Dog Breed with Deep Learning,\" in Proc. Int. Conf. on Information Technology, 2021.",
        "[3] S. A. Bokhari, P. Mukherjee, A. S. Singh, S. Shaik, and J. K. Mathew, \"Convolutional Neural Network Based Dog Breed Classification,\" in Proc. Int. Conf. on Innovative Computing and Communication, 2022.",
        "[4] T. Kumaravel, P. Natesan, V. E. Sathishkumar, S. S. N, S. G, and U. V, \"Automatic Dog Breed Classification Using Deep Learning,\" in Proc. Int. Conf. on Smart Systems and Inventive Technology, 2023.",
        "[5] N. Banakar, Raghavendra B. U., S. G. S., T. K. Vani, and V. M. Vishnu, \"Dog Breed Identification Using Deep Learning,\" International Journal of Advanced Research in Computer Science and Software Engineering, vol. 13, no. 5, 2023.",
        "[6] B. Valarmathi, N. S. Gupta, G. Prakash, R. H. Reddy, S. Saravanan, and P. Shanmugasundaram, \"Hybrid Deep Learning Algorithms for Dog Breed Identification—A Comparative Analysis,\" IEEE Access, vol. 11, pp. 45120–45132, 2023.",
        "[7] S. R. Basha, I. Ganesh, G. R. Reddy, and A. Hans, \"Dogs Breed Classification Using Deep Learning,\" in Proc. Int. Conf. on Artificial Intelligence and Smart Systems, 2021.",
        "[8] S. S. Hussain, K. S. R. Murthy, C. S. Rani, T. Nanuvala, C. R. Kumar, and G. Sathar, \"Automated Dog Breed Recognition Using CNN-Based Transfer Learning,\" in Proc. Int. Conf. on Advances in Computer Engineering & Communication Systems, 2025.",
        "[9] A. S. Ghotra, H. Kour, A. Hasan, and A. Khan, \"Dog Breed Identification,\" in Proc. Int. Conf. on Data Science and Machine Learning, 2023.",
        "[10] J. Bankar, A. Nalawade, S. Wali, A. Rane, and H. Matlani, \"AI Based Dog Breed Prediction Model and Virtual Canine Hub,\" International Journal of Computer Applications, vol. 186, no. 14, 2025.",
        "[11] D.-N. Zou, S.-H. Zhang, T.-J. Mu, and M. Zhang, \"A New Dataset of Dog Breed Images and a Benchmark for Fine-Grained Classification,\" Computational Visual Media, vol. 6, no. 4, pp. 477–487, 2020.",
        "[12] P. Perera and V. M. Patel, \"Deep Transfer Learning for Multiple Class Novelty Detection,\" in Proc. IEEE/CVF Conf. on Computer Vision and Pattern Recognition (CVPR), 2019, pp. 1154–1162.",
        "[13] A. Khosla, N. Jayadevaprakash, B. Yao, and L. Fei-Fei, \"Novel Dataset for Fine-Grained Image Categorization: Stanford Dogs,\" in Proc. CVPR Workshop on Fine-Grained Visual Categorization, Colorado Springs, CO, USA, 2011.",
        "[14] M. Sandler, A. Howard, M. Zhu, A. Zhmoginov, and L.-C. Chen, \"MobileNetV2: Inverted Residuals and Linear Bottlenecks,\" in Proc. IEEE/CVF Conf. on Computer Vision and Pattern Recognition (CVPR), Salt Lake City, UT, USA, 2018, pp. 4510–4520."
    ]
    for ref in references:
        add_p(ref, space_after=6)

    doc.add_page_break()

    # =========================================================================
    # PROJECT TEAM CONTRIBUTION DETAILS
    # =========================================================================
    add_h1("PROJECT TEAM CONTRIBUTION DETAILS")
    
    add_p(
        "This project was collaboratively designed, developed, and evaluated by the four team members listed below. "
        "Each member assumed primary ownership of specific modules while collaborating closely on overall system integration:"
    )

    # Table 8.1: Contribution Table
    p_tcap = doc.add_paragraph()
    p_tcap.paragraph_format.space_before = Pt(8)
    p_tcap.paragraph_format.space_after = Pt(2)
    r = p_tcap.add_run("Table 8.1: Project Team Contribution Details")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(11)
    r.bold = True

    t_contrib = doc.add_table(rows=5, cols=4)
    t_contrib.alignment = WD_TABLE_ALIGNMENT.CENTER
    contrib_headers = ["Member Name", "Roll Number", "Primary Module", "Core Contributions"]
    contrib_data = [
        ("K Goutham Nayak", "CS24B1081", "Backend Architecture & Reporting", "Flask routing, MySQL schema design, ReportLab PDF certificate engine, and authentication security."),
        ("K Adithya", "CS24B1091", "Deep Learning & Model Training", "MobileNetV2 transfer learning, two-phase training strategy, hyperparameter tuning, and metric evaluation."),
        ("R Mahesh Rathod", "CS24B1071", "Two-Stage Pipeline & Preprocessing", "Stage 1 canine presence filter, ImageNet synset mapping, data augmentation, and input validation."),
        ("G Vishnu Vardhan", "CS24B1028", "Frontend UI/UX & Breed Directory", "Responsive interface design, Chart.js dashboard integration, breed directory, and side-by-side comparison.")
    ]
    for c_idx, h_text in enumerate(contrib_headers):
        cell = t_contrib.rows[0].cells[c_idx]
        cell.paragraphs[0].text = h_text
        cell.paragraphs[0].runs[0].bold = True
        cell.paragraphs[0].runs[0].font.name = 'Times New Roman'
        cell.paragraphs[0].runs[0].font.size = Pt(10.5)
        set_cell_background(cell, "EAECEE")
        set_cell_margins(cell, 50, 50, 70, 70)
    for r_idx, row_vals in enumerate(contrib_data):
        row = t_contrib.rows[r_idx + 1]
        for c_idx, val in enumerate(row_vals):
            cell = row.cells[c_idx]
            cell.paragraphs[0].text = val
            cell.paragraphs[0].runs[0].font.name = 'Times New Roman'
            cell.paragraphs[0].runs[0].font.size = Pt(10)
            set_cell_margins(cell, 40, 40, 60, 60)
            if r_idx % 2 == 1:
                set_cell_background(cell, "F8F9FA")

    # Save document
    doc.save(output_path)
    print(f"Clean DOCX report successfully created at: {output_path}")

# =========================================================================
# 2. PDF GENERATOR WITH DUAL-PASS RESOLUTION
# =========================================================================

class AcademicCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super(AcademicCanvas, self).__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations()
            super(AcademicCanvas, self).showPage()
        super(AcademicCanvas, self).save()

    def draw_page_decorations(self):
        p_num = self._pageNumber
        if p_num == 1:
            return  # Suppress on title page

        self.saveState()
        self.setFont("Times-Roman", 9.5)
        self.setFillColor(colors.HexColor("#333333"))
        self.setStrokeColor(colors.HexColor("#7F8C8D"))
        self.setLineWidth(0.5)

        # Header rule & text
        header_y = 841.89 - 36
        self.line(40, header_y, 595.27 - 40, header_y)
        self.drawString(40, header_y + 5, "IIITDM KANCHEEPURAM")
        self.drawRightString(595.27 - 40, header_y + 5, "Dog Breed Identification Project Report")

        # Footer rule & text
        footer_y = 40
        self.line(40, footer_y, 595.27 - 40, footer_y)
        self.drawString(40, footer_y - 12, "Introduction to Data Science for Engineers — Project Report 2026")

        # Determine Page Number String
        if p_num == 2:
            page_str = "1"
        elif 3 <= p_num <= 5:
            page_str = int_to_roman(p_num - 2)
        else:
            page_str = str(p_num - 5)

        self.drawRightString(595.27 - 40, footer_y - 12, page_str)
        self.restoreState()


class PageMark(Flowable):
    def __init__(self, marker_name, page_dict):
        super().__init__()
        self.marker_name = marker_name
        self.page_dict = page_dict
    def wrap(self, availWidth, availHeight):
        return 0, 0
    def draw(self):
        p_num = self.canv._pageNumber
        disp = str(p_num - 5) if p_num >= 6 else (int_to_roman(p_num - 2) if p_num >= 3 else '1')
        self.page_dict[self.marker_name] = disp


def build_story(page_dict=None, collect_pages_dict=None):
    base_styles = getSampleStyleSheet()

    c_primary = colors.HexColor("#1A2B4C")
    c_secondary = colors.HexColor("#2A4365")
    c_header_bg = colors.HexColor("#EAECEE")
    c_alt_row = colors.HexColor("#F8F9FA")
    c_border = colors.HexColor("#BDC3C7")
    c_text = colors.HexColor("#222222")

    title_style = ParagraphStyle(
        'CoverTitle', parent=base_styles['Normal'],
        fontName='Times-Bold', fontSize=18, leading=23,
        alignment=TA_CENTER, textColor=c_primary, spaceAfter=14
    )
    h1_style = ParagraphStyle(
        'Heading1_Custom', parent=base_styles['Normal'],
        fontName='Times-Bold', fontSize=15, leading=19,
        textColor=c_primary, spaceBefore=14, spaceAfter=8, keepWithNext=True
    )
    h2_style = ParagraphStyle(
        'Heading2_Custom', parent=base_styles['Normal'],
        fontName='Times-Bold', fontSize=13, leading=17,
        textColor=c_secondary, spaceBefore=10, spaceAfter=4, keepWithNext=True
    )
    body_style = ParagraphStyle(
        'Body_Custom', parent=base_styles['Normal'],
        fontName='Times-Roman', fontSize=11, leading=16,
        alignment=TA_JUSTIFY, textColor=c_text, spaceAfter=6
    )
    caption_style = ParagraphStyle(
        'Caption_Custom', parent=base_styles['Normal'],
        fontName='Times-Bold', fontSize=10.5, leading=13,
        alignment=TA_CENTER, textColor=c_primary, spaceBefore=4, spaceAfter=6
    )
    tbl_header_style = ParagraphStyle(
        'TblHeader', parent=base_styles['Normal'],
        fontName='Times-Bold', fontSize=9.5, leading=12,
        alignment=TA_CENTER, textColor=c_primary
    )
    tbl_cell_style = ParagraphStyle(
        'TblCell', parent=base_styles['Normal'],
        fontName='Times-Roman', fontSize=9.5, leading=12,
        alignment=TA_LEFT, textColor=c_text
    )
    tbl_cell_center = ParagraphStyle(
        'TblCellCenter', parent=base_styles['Normal'],
        fontName='Times-Roman', fontSize=9.5, leading=12,
        alignment=TA_CENTER, textColor=c_text
    )

    story = []

    def add_p(text, bold_prefix="", space_after=6):
        prefix_html = f"<b>{bold_prefix}</b> " if bold_prefix else ""
        story.append(Paragraph(f"{prefix_html}{text}", body_style))

    def add_bullet(text, space_after=4):
        p_html = f"&nbsp;&nbsp;&bull;&nbsp;&nbsp;{text}"
        story.append(Paragraph(p_html, body_style))

    def add_numbered(num_str, text, space_after=4):
        p_html = f"&nbsp;&nbsp;<b>{num_str}.</b>&nbsp;&nbsp;{text}"
        story.append(Paragraph(p_html, body_style))

    def mark(key):
        if collect_pages_dict is not None:
            story.append(PageMark(key, collect_pages_dict))

    # =========================================================================
    # TITLE PAGE
    # =========================================================================
    story.append(Spacer(1, 25))
    story.append(Paragraph("INDIAN INSTITUTE OF INFORMATION TECHNOLOGY,<br/>DESIGN AND MANUFACTURING, KANCHEEPURAM", ParagraphStyle('InstHead', parent=base_styles['Normal'], fontName='Times-Bold', fontSize=13, leading=17, alignment=TA_CENTER, textColor=c_primary)))
    story.append(Spacer(1, 6))
    story.append(Paragraph("COURSE: INTRODUCTION TO DATA SCIENCE FOR ENGINEERS", ParagraphStyle('CourseHead', parent=base_styles['Normal'], fontName='Times-Bold', fontSize=11, leading=14, alignment=TA_CENTER, textColor=c_secondary)))
    story.append(Spacer(1, 3))
    story.append(Paragraph("PROJECT REPORT", ParagraphStyle('DocType', parent=base_styles['Normal'], fontName='Times-Bold', fontSize=11.5, leading=15, alignment=TA_CENTER, textColor=colors.HexColor("#1A5276"))))
    story.append(Spacer(1, 3))
    story.append(Paragraph("ACADEMIC YEAR: 2026", ParagraphStyle('AcadYear', parent=base_styles['Normal'], fontName='Times-Bold', fontSize=10.5, leading=14, alignment=TA_CENTER, textColor=colors.HexColor("#333333"))))
    story.append(Spacer(1, 15))

    div_table = Table([[""]], colWidths=[515], rowHeights=[2])
    div_table.setStyle(TableStyle([
        ('LINEABOVE', (0,0), (-1,-1), 1.0, colors.HexColor("#7F8C8D")),
        ('TOPPADDING', (0,0), (-1,-1), 0),
        ('BOTTOMPADDING', (0,0), (-1,-1), 0),
    ]))
    story.append(div_table)
    story.append(Spacer(1, 25))

    story.append(Paragraph("DOG BREED IDENTIFICATION USING DEEP LEARNING AND TRANSFER LEARNING", title_style))
    story.append(Spacer(1, 25))

    story.append(Paragraph("<b>PROJECT TEAM MEMBERS</b>", ParagraphStyle('TeamHead', parent=base_styles['Normal'], fontName='Times-Bold', fontSize=11, leading=15, alignment=TA_CENTER, textColor=c_primary)))
    story.append(Spacer(1, 8))

    cover_team_data = [
        [Paragraph("<b>S.No.</b>", tbl_header_style), Paragraph("<b>Student Name</b>", tbl_header_style), Paragraph("<b>Roll Number</b>", tbl_header_style), Paragraph("<b>Project Responsibility</b>", tbl_header_style)],
        [Paragraph("1", tbl_cell_center), Paragraph("K Goutham Nayak", tbl_cell_style), Paragraph("CS24B1081", tbl_cell_center), Paragraph("Backend Architecture, MySQL Database and PDF Reporting", tbl_cell_style)],
        [Paragraph("2", tbl_cell_center), Paragraph("K Adithya", tbl_cell_style), Paragraph("CS24B1091", tbl_cell_center), Paragraph("Deep Learning Model Architecture and Fine-Tuning", tbl_cell_style)],
        [Paragraph("3", tbl_cell_center), Paragraph("R Mahesh Rathod", tbl_cell_style), Paragraph("CS24B1071", tbl_cell_center), Paragraph("Two-Stage Canine Presence Detection and Validation", tbl_cell_style)],
        [Paragraph("4", tbl_cell_center), Paragraph("G Vishnu Vardhan", tbl_cell_style), Paragraph("CS24B1028", tbl_cell_center), Paragraph("Frontend UI/UX, Breed Directory and Trait Comparison", tbl_cell_style)],
    ]
    t_cover = Table(cover_team_data, colWidths=[35, 120, 85, 275])
    t_cover.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_header_bg),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_alt_row]),
    ]))
    story.append(t_cover)
    story.append(PageBreak())

    # =========================================================================
    # PROJECT SPECIFICATIONS (Page 2)
    # =========================================================================
    story.append(Paragraph("PROJECT SPECIFICATIONS", h1_style))
    story.append(Spacer(1, 6))

    specs_data = [
        [Paragraph("<b>Course Name</b>", tbl_cell_style), Paragraph("Introduction to Data Science for Engineers", tbl_cell_style)],
        [Paragraph("<b>Academic Degree</b>", tbl_cell_style), Paragraph("Bachelor of Technology (B.Tech)", tbl_cell_style)],
        [Paragraph("<b>Academic Year</b>", tbl_cell_style), Paragraph("2026", tbl_cell_style)],
        [Paragraph("<b>Core Deep Learning Model</b>", tbl_cell_style), Paragraph("MobileNetV2 with Inverted Residuals and Linear Bottlenecks", tbl_cell_style)],
        [Paragraph("<b>Transfer Learning Source</b>", tbl_cell_style), Paragraph("ImageNet Pretrained Weights (1.4M images, 1,000 classes)", tbl_cell_style)],
        [Paragraph("<b>Benchmark Dataset</b>", tbl_cell_style), Paragraph("Stanford Dogs / Kaggle Dog Breed Identification", tbl_cell_style)],
        [Paragraph("<b>Total Photographic Images</b>", tbl_cell_style), Paragraph("10,222 labeled JPEG photographs", tbl_cell_style)],
        [Paragraph("<b>Canine Breed Classes</b>", tbl_cell_style), Paragraph("120 purebred domestic dog varieties", tbl_cell_style)],
        [Paragraph("<b>Input Image Resolution</b>", tbl_cell_style), Paragraph("224 x 224 pixels (3-channel RGB)", tbl_cell_style)],
        [Paragraph("<b>Inference Pipeline</b>", tbl_cell_style), Paragraph("Two-Stage Architecture (Stage 1: Canine Filter; Stage 2: Breed Classifier)", tbl_cell_style)],
        [Paragraph("<b>Web Application Framework</b>", tbl_cell_style), Paragraph("Python Flask 3.0 (REST APIs, Session Management, Jinja2)", tbl_cell_style)],
        [Paragraph("<b>Database Management</b>", tbl_cell_style), Paragraph("MySQL 8.0 Server (dog_breed_db with 4 relational tables)", tbl_cell_style)],
        [Paragraph("<b>Reporting Engine</b>", tbl_cell_style), Paragraph("Python ReportLab 5.1 (Dynamic PDF prediction certificate generation)", tbl_cell_style)],
        [Paragraph("<b>Top-1 Test Accuracy</b>", tbl_cell_style), Paragraph("77.64% (on 1,534 held-out evaluation test images)", tbl_cell_style)],
        [Paragraph("<b>Top-5 Test Accuracy</b>", tbl_cell_style), Paragraph("96.87% (on 1,534 held-out evaluation test images)", tbl_cell_style)],
        [Paragraph("<b>Test Categorical Loss</b>", tbl_cell_style), Paragraph("0.7036 (cross-entropy on held-out test split)", tbl_cell_style)],
        [Paragraph("<b>Macro F1-Score / Weighted F1</b>", tbl_cell_style), Paragraph("76.91% / 77.35%", tbl_cell_style)],
        [Paragraph("<b>Automated Verification Suite</b>", tbl_cell_style), Paragraph("18/18 Automated Test Cases Passing", tbl_cell_style)]
    ]
    t_specs = Table(specs_data, colWidths=[175, 340])
    t_specs.setStyle(TableStyle([
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('ROWBACKGROUNDS', (0,0), (-1,-1), [colors.white, c_alt_row]),
    ]))
    story.append(t_specs)
    story.append(PageBreak())

    # =========================================================================
    # ABSTRACT
    # =========================================================================
    story.append(Paragraph("ABSTRACT", h1_style))
    story.append(Spacer(1, 6))

    add_p(
        "Fine-grained visual categorization presents a classical yet challenging problem in computer vision. "
        "Unlike coarse classification tasks that distinguish between dissimilar objects such as cars and cats, "
        "fine-grained classification requires recognizing subordinate categories within the same biological family. "
        "In this project, our team designed, implemented, and evaluated an end-to-end canine identification system "
        "capable of classifying domestic dogs across 120 recognized breeds from the Stanford Dogs benchmark dataset "
        "comprising 10,222 labeled photographic images."
    )
    add_p(
        "To achieve competitive classification accuracy without demanding heavy hardware resources, we implemented "
        "transfer learning using MobileNetV2 pre-trained on ImageNet. Our training pipeline utilizes a two-phase transfer "
        "learning approach: Phase 1 freezes the 155-layer convolutional base to train newly added classification layers, "
        "followed by Phase 2 fine-tuning of the top 30 convolutional layers at a reduced learning rate (1e-5). To prevent "
        "non-dog uploads from receiving false predictions, we designed a two-stage inference workflow where an upstream "
        "filter verifies canine presence by aggregating ImageNet canine synset probabilities before executing the specialized "
        "breed classifier."
    )
    add_p(
        "Evaluated on a strictly held-out test split of 1,534 images, our fine-tuned model achieves a Top-1 classification "
        "accuracy of 77.64%, a Top-5 accuracy of 96.87%, a categorical cross-entropy loss of 0.7036, a Macro F1-score of 76.91%, "
        "and a Weighted F1-score of 77.35%. We deployed this model into an interactive full-stack web application developed using "
        "Python Flask 3.0, a persistent MySQL 8.0 relational database for history tracking and user accounts, and an automated "
        "ReportLab engine that provides downloadable PDF prediction certificates. All application flows were verified through "
        "a comprehensive testing suite."
    )
    story.append(Spacer(1, 6))
    story.append(Paragraph("<b>Keywords:</b> <i>Deep Learning, Transfer Learning, MobileNetV2, Fine-Grained Canine Classification, Computer Vision, Flask Web Application, MySQL Database.</i>", body_style))
    story.append(PageBreak())

    # =========================================================================
    # TABLE OF CONTENTS
    # =========================================================================
    story.append(Paragraph("TABLE OF CONTENTS", h1_style))
    story.append(Spacer(1, 6))

    p_ch1 = page_dict.get("CH1", "1") if page_dict else "1"
    p_ch2 = page_dict.get("CH2", "4") if page_dict else "4"
    p_ch3 = page_dict.get("CH3", "8") if page_dict else "8"
    p_ch4 = page_dict.get("CH4", "11") if page_dict else "11"
    p_ch5 = page_dict.get("CH5", "15") if page_dict else "15"
    p_ch6 = page_dict.get("CH6", "18") if page_dict else "18"
    p_ch7 = page_dict.get("CH7", "20") if page_dict else "20"
    p_refs = page_dict.get("REFS", "22") if page_dict else "22"
    p_team = page_dict.get("TEAM", "24") if page_dict else "24"

    toc_data = [
        [Paragraph("<b>PROJECT SPECIFICATIONS</b>", tbl_cell_style), Paragraph("<b>i</b>", tbl_cell_center)],
        [Paragraph("<b>ABSTRACT</b>", tbl_cell_style), Paragraph("<b>ii</b>", tbl_cell_center)],
        [Paragraph("<b>LIST OF TABLES</b>", tbl_cell_style), Paragraph("<b>iv</b>", tbl_cell_center)],
        [Paragraph("<b>CHAPTER 1 – INTRODUCTION</b>", tbl_cell_style), Paragraph(f"<b>{p_ch1}</b>", tbl_cell_center)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;1.1 Background and Motivation", tbl_cell_style), Paragraph(p_ch1, tbl_cell_center)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;1.2 Problem Statement", tbl_cell_style), Paragraph(str(int(p_ch1) + 1), tbl_cell_center)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;1.3 Project Objectives", tbl_cell_style), Paragraph(str(int(p_ch1) + 1), tbl_cell_center)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;1.4 Scope and Limitations", tbl_cell_style), Paragraph(str(int(p_ch1) + 2), tbl_cell_center)],
        [Paragraph("<b>CHAPTER 2 – LITERATURE SURVEY</b>", tbl_cell_style), Paragraph(f"<b>{p_ch2}</b>", tbl_cell_center)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;2.1 Research on Dog Breed Classification", tbl_cell_style), Paragraph(p_ch2, tbl_cell_center)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;2.2 Deep Transfer Learning Approaches", tbl_cell_style), Paragraph(str(int(p_ch2) + 1), tbl_cell_center)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;2.3 Summary of Existing Research", tbl_cell_style), Paragraph(str(int(p_ch2) + 2), tbl_cell_center)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;2.4 Research Gaps", tbl_cell_style), Paragraph(str(int(p_ch2) + 3), tbl_cell_center)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;2.5 Selection of MobileNetV2", tbl_cell_style), Paragraph(str(int(p_ch2) + 3), tbl_cell_center)],
        [Paragraph("<b>CHAPTER 3 – DATASET DESCRIPTION AND PREPROCESSING</b>", tbl_cell_style), Paragraph(f"<b>{p_ch3}</b>", tbl_cell_center)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;3.1 Stanford Dogs Dataset Overview", tbl_cell_style), Paragraph(p_ch3, tbl_cell_center)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;3.2 Dataset Distribution and Partitioning", tbl_cell_style), Paragraph(p_ch3, tbl_cell_center)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;3.3 Data Preprocessing Steps", tbl_cell_style), Paragraph(str(int(p_ch3) + 2), tbl_cell_center)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;3.4 Data Augmentation Techniques", tbl_cell_style), Paragraph(str(int(p_ch3) + 2), tbl_cell_center)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;3.5 Visual Challenges in Canine Images", tbl_cell_style), Paragraph(str(int(p_ch3) + 3), tbl_cell_center)],
        [Paragraph("<b>CHAPTER 4 – METHODOLOGY</b>", tbl_cell_style), Paragraph(f"<b>{p_ch4}</b>", tbl_cell_center)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;4.1 System Overview", tbl_cell_style), Paragraph(p_ch4, tbl_cell_center)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;4.2 Dataset and Image Input", tbl_cell_style), Paragraph(str(int(p_ch4) + 1), tbl_cell_center)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;4.3 Image Preprocessing", tbl_cell_style), Paragraph(str(int(p_ch4) + 1), tbl_cell_center)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;4.4 MobileNetV2 Model", tbl_cell_style), Paragraph(str(int(p_ch4) + 2), tbl_cell_center)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;4.5 Transfer Learning and Model Training", tbl_cell_style), Paragraph(str(int(p_ch4) + 2), tbl_cell_center)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;4.6 Breed Prediction", tbl_cell_style), Paragraph(str(int(p_ch4) + 3), tbl_cell_center)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;4.7 Web Application and Database Integration", tbl_cell_style), Paragraph(str(int(p_ch4) + 3), tbl_cell_center)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;4.8 Overall Working Procedure", tbl_cell_style), Paragraph(str(int(p_ch4) + 4), tbl_cell_center)],
        [Paragraph("<b>CHAPTER 5 – SYSTEM IMPLEMENTATION AND WEB APPLICATION</b>", tbl_cell_style), Paragraph(f"<b>{p_ch5}</b>", tbl_cell_center)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;5.1 Technology Stack", tbl_cell_style), Paragraph(p_ch5, tbl_cell_center)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;5.2 Application Architecture and Routes", tbl_cell_style), Paragraph(str(int(p_ch5) + 1), tbl_cell_center)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;5.3 MySQL Relational Database Schema", tbl_cell_style), Paragraph(str(int(p_ch5) + 2), tbl_cell_center)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;5.4 Dynamic PDF Prediction Certificate Engine", tbl_cell_style), Paragraph(str(int(p_ch5) + 2), tbl_cell_center)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;5.5 User Authentication and Security", tbl_cell_style), Paragraph(str(int(p_ch5) + 3), tbl_cell_center)],
        [Paragraph("<b>CHAPTER 6 – EXPERIMENTAL RESULTS</b>", tbl_cell_style), Paragraph(f"<b>{p_ch6}</b>", tbl_cell_center)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;6.1 Model Training Progress", tbl_cell_style), Paragraph(p_ch6, tbl_cell_center)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;6.2 Quantitative Evaluation Metrics", tbl_cell_style), Paragraph(str(int(p_ch6) + 1), tbl_cell_center)],
        [Paragraph("<b>CHAPTER 7 – CONCLUSION AND FUTURE ENHANCEMENTS</b>", tbl_cell_style), Paragraph(f"<b>{p_ch7}</b>", tbl_cell_center)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;7.1 Conclusion", tbl_cell_style), Paragraph(p_ch7, tbl_cell_center)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;7.2 Limitations", tbl_cell_style), Paragraph(str(int(p_ch7) + 1), tbl_cell_center)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;7.3 Future Enhancements", tbl_cell_style), Paragraph(str(int(p_ch7) + 1), tbl_cell_center)],
        [Paragraph("<b>REFERENCES</b>", tbl_cell_style), Paragraph(f"<b>{p_refs}</b>", tbl_cell_center)],
        [Paragraph("<b>PROJECT TEAM CONTRIBUTION DETAILS</b>", tbl_cell_style), Paragraph(f"<b>{p_team}</b>", tbl_cell_center)],
    ]
    t_toc = Table(toc_data, colWidths=[460, 55])
    t_toc.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 1.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 1.5),
        ('LINEBELOW', (0,0), (-1,-1), 0.25, colors.HexColor("#EAECEE")),
    ]))
    story.append(t_toc)
    story.append(PageBreak())

    # =========================================================================
    # LIST OF TABLES
    # =========================================================================
    story.append(Paragraph("LIST OF TABLES", h1_style))
    story.append(Spacer(1, 4))

    p_t21 = page_dict.get("T21", str(int(p_ch2) + 2)) if page_dict else "6"
    p_t31 = page_dict.get("T31", str(int(p_ch3) + 1)) if page_dict else "10"
    p_t41 = page_dict.get("T41", str(int(p_ch4) + 2)) if page_dict else "16"
    p_t51 = page_dict.get("T51", str(int(p_ch5) + 2)) if page_dict else "23"
    p_t61 = page_dict.get("T61", str(int(p_ch6) + 1)) if page_dict else "27"
    p_t81 = page_dict.get("TEAM", p_team) if page_dict else "34"

    lot_data = [
        [Paragraph("Table 2.1: Summary of Existing Research on Dog Breed Classification", tbl_cell_style), Paragraph(p_t21, tbl_cell_center)],
        [Paragraph("Table 3.1: Dataset Split and Partitioning Strategy", tbl_cell_style), Paragraph(p_t31, tbl_cell_center)],
        [Paragraph("Table 4.1: Neural Network Layer Progression and Parameter Distribution", tbl_cell_style), Paragraph(p_t41, tbl_cell_center)],
        [Paragraph("Table 5.1: MySQL Relational Database Schema and Entity Relationships", tbl_cell_style), Paragraph(p_t51, tbl_cell_center)],
        [Paragraph("Table 6.1: Overall Quantitative Evaluation Metrics on Held-Out Test Set (1,534 Images)", tbl_cell_style), Paragraph(p_t61, tbl_cell_center)],
        [Paragraph("Table 8.1: Project Team Contribution Details", tbl_cell_style), Paragraph(p_t81, tbl_cell_center)],
    ]
    t_lot = Table(lot_data, colWidths=[460, 55])
    t_lot.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
        ('LINEBELOW', (0,0), (-1,-1), 0.25, colors.HexColor("#EAECEE")),
    ]))
    story.append(t_lot)
    story.append(PageBreak())

    # =========================================================================
    # CHAPTER 1 – INTRODUCTION
    # =========================================================================
    mark("CH1")
    story.append(Paragraph("Chapter 1 – Introduction", h1_style))
    
    story.append(Paragraph("1.1 Background and Motivation", h2_style))
    add_p(
        "Computer vision has undergone tremendous advancements over the past decade, moving from classical handcrafted "
        "features such as SIFT and HOG to deep Convolutional Neural Networks (CNNs). While distinguishing between coarse "
        "classes (such as dogs versus cars or airplanes) is now straightforward, fine-grained visual classification remains "
        "a significant challenge. In fine-grained tasks, all categories belong to the same broader family, meaning that inter-class "
        "differences are subtle while intra-class variations can be large due to differences in pose, lighting, and fur coloration."
    )
    add_p(
        "Domestic dogs (Canis lupus familiaris) exhibit extraordinary morphological diversity, comprising hundreds of distinct "
        "breeds worldwide. Accurate visual breed identification is beneficial across multiple domains, including veterinary clinics, "
        "animal shelters, pet rescue organizations, and pet adoption platforms. In clinical settings, identifying the breed helps "
        "veterinarians recognize breed-specific health risks, such as hip dysplasia or cardiovascular conditions. In shelters, "
        "proper classification ensures accurate records and helps potential adopters understand care requirements."
    )
    add_p(
        "However, identifying dog breeds visually is difficult even for experienced dog owners. Closely related breeds, such as "
        "the Pembroke Welsh Corgi and Cardigan Welsh Corgi, share similar body shapes and face structures. Similarly, breeds like "
        "the Whippet and Italian Greyhound differ primarily in body size, which is difficult to estimate from a standalone photograph. "
        "Building an automated system that classifies dog breeds accurately from ordinary photographs is therefore both an interesting "
        "engineering challenge and a practically useful tool."
    )

    story.append(Paragraph("1.2 Problem Statement", h2_style))
    add_p(
        "The goal of this project is to create an accessible web-based application capable of classifying 120 domestic dog breeds "
        "from user-uploaded images. Traditional computer vision models face two major problems in real-world deployment: first, training "
        "a deep neural network from scratch requires an enormous volume of labeled data to avoid overfitting; second, real-world users "
        "frequently upload non-dog images (such as humans, cats, or random objects), which standard closed-set classifiers incorrectly "
        "assign to a dog breed with high confidence."
    )
    add_p(
        "Therefore, our project addresses the following questions: How can we build an efficient and accurate breed classifier using "
        "transfer learning with limited training data? How can we prevent false predictions on non-dog images? And how can we deploy "
        "this solution as a full-stack, user-friendly web application with persistent storage?"
    )

    story.append(Paragraph("1.3 Project Objectives", h2_style))
    add_p("To solve the problem described above, we established the following key objectives:")
    add_numbered("1", "Organize and preprocess the Stanford Dogs dataset of 10,222 images across 120 breeds into clean training, validation, and testing sets.")
    add_numbered("2", "Implement transfer learning using the MobileNetV2 architecture pre-trained on ImageNet to achieve high classification accuracy with low compute overhead.")
    add_numbered("3", "Train the model using a two-phase strategy: first training the classification head on frozen convolutional features, followed by fine-tuning selected upper layers.")
    add_numbered("4", "Implement an upstream validation mechanism using ImageNet canine synsets to filter out non-dog images before breed classification.")
    add_numbered("5", "Provide Top-3 candidate predictions with confidence percentages to give users transparent and informative results.")
    add_numbered("6", "Develop a responsive full-stack web application using Flask and MySQL for user authentication, prediction history logging, and dynamic PDF certificate generation.")

    story.append(Paragraph("1.4 Scope and Limitations", h2_style))
    add_p(
        "The scope of this project includes the 120 purebred domestic dog varieties present in the Stanford Dogs dataset. The system "
        "processes single-image uploads in standard image formats (JPEG and PNG) and provides Top-3 predictions alongside confidence "
        "scores. The web interface enables users to register accounts, view past prediction history, explore breed traits, compare breeds, "
        "and download PDF reports."
    )
    add_p(
        "The system has specific limitations: it is designed primarily for photographs containing a single dog; when multiple dogs are "
        "present, the model focuses on the most prominent visual subject. Furthermore, because the dataset contains only purebred categories, "
        "mixed-breed dogs will be classified into the most morphologically similar purebred ancestral breeds."
    )
    story.append(PageBreak())

    # =========================================================================
    # CHAPTER 2 – LITERATURE SURVEY
    # =========================================================================
    mark("CH2")
    story.append(Paragraph("Chapter 2 – Literature Survey", h1_style))
    
    story.append(Paragraph("2.1 Research on Dog Breed Classification", h2_style))
    add_p(
        "Automated animal categorization has been an active area of study in computer vision. Early research relied on hand-crafted "
        "visual features such as SIFT, HOG, and color histograms combined with Support Vector Machines (SVMs). In 2011, Khosla et al. [13] "
        "introduced the Stanford Dogs dataset containing 20,580 images across 120 breeds. Their initial baseline achieved approximately 22% "
        "accuracy, showing that traditional hand-crafted descriptors could not capture the fine morphological details needed to distinguish "
        "closely related breeds."
    )
    add_p(
        "With the emergence of deep learning, Convolutional Neural Networks dramatically improved image recognition. CNNs automatically "
        "learn hierarchical representations from raw pixels: shallow layers detect edges and textures, while deeper layers capture complex "
        "canine contours and facial structures. Researchers quickly demonstrated that deep networks substantially outperformed classical "
        "approaches on fine-grained benchmarks."
    )

    story.append(Paragraph("2.2 Deep Transfer Learning Approaches", h2_style))
    add_p(
        "Training deep networks from scratch requires hundreds of thousands of labeled images. In specialized domains where datasets "
        "contain only tens of images per class, transfer learning is essential to avoid severe overfitting. Pre-training on ImageNet [3], "
        "which contains 1.4 million images across 1,000 categories, allows networks to learn rich visual filters that transfer well to "
        "subordinate classification tasks."
    )
    add_p(
        "Numerous researchers have explored transfer learning for canine classification using different base architectures. Early studies "
        "utilized heavier networks such as VGG16 and ResNet50, which provide high representational capacity but require large memory storage "
        "(>100 MB) and higher inference times on standard CPUs. In contrast, lightweight architectures such as MobileNetV2 [14] utilize "
        "depthwise separable convolutions to achieve competitive accuracy with a fraction of the parameters, making them well-suited for web "
        "and edge deployment."
    )

    story.append(Paragraph("2.3 Summary of Existing Research", h2_style))
    add_p(
        "To understand the current state of canine breed classification, we analyzed twelve relevant studies from recent academic literature. "
        "Table 2.1 summarizes the architectures, datasets, and reported outcomes of these investigations."
    )

    mark("T21")
    story.append(Spacer(1, 4))
    story.append(Paragraph("Table 2.1: Summary of Existing Research on Dog Breed Classification", caption_style))
    lit_table_data = [
        [Paragraph("<b>Authors & Year</b>", tbl_header_style), Paragraph("<b>Architecture</b>", tbl_header_style), Paragraph("<b>Dataset Used</b>", tbl_header_style), Paragraph("<b>Reported Performance</b>", tbl_header_style), Paragraph("<b>Key Limitation Noted</b>", tbl_header_style)],
        [Paragraph("Selvaraj et al. (2023) [1]", tbl_cell_style), Paragraph("ResNet50", tbl_cell_style), Paragraph("Stanford Dogs (120 breeds)", tbl_cell_style), Paragraph("88.2% Accuracy", tbl_cell_center), Paragraph("High parameter count and slow CPU latency", tbl_cell_style)],
        [Paragraph("Borwarnginn et al. (2021) [2]", tbl_cell_style), Paragraph("MobileNetV2", tbl_cell_style), Paragraph("120 Dog Breeds", tbl_cell_style), Paragraph("81.6% Top-1 Accuracy", tbl_cell_center), Paragraph("No mechanism to filter non-dog images", tbl_cell_style)],
        [Paragraph("Bokhari et al. (2022) [3]", tbl_cell_style), Paragraph("MobileNetV2 Feature Extractor", tbl_cell_style), Paragraph("Stanford Dogs", tbl_cell_style), Paragraph("64.0% on 120 classes", tbl_cell_center), Paragraph("Accuracy drops without fine-tuning", tbl_cell_style)],
        [Paragraph("Kumaravel et al. (2023) [4]", tbl_cell_style), Paragraph("DenseNet201 + Augmentation", tbl_cell_style), Paragraph("Stanford + Kaggle", tbl_cell_style), Paragraph("87.3% Accuracy", tbl_cell_center), Paragraph("Computationally intensive training", tbl_cell_style)],
        [Paragraph("Banakar et al. (2023) [5]", tbl_cell_style), Paragraph("VGG-19 Architecture", tbl_cell_style), Paragraph("Stanford Dogs", tbl_cell_style), Paragraph("High Training Accuracy", tbl_cell_center), Paragraph("Large model file size (~550 MB)", tbl_cell_style)],
        [Paragraph("Valarmathi et al. (2023) [6]", tbl_cell_style), Paragraph("Hybrid InceptionV3 + Xception", tbl_cell_style), Paragraph("Stanford Dogs", tbl_cell_style), Paragraph("92.4% Val Accuracy", tbl_cell_center), Paragraph("High compute requirements for web serving", tbl_cell_style)],
        [Paragraph("Basha et al. (2021) [7]", tbl_cell_style), Paragraph("VGG16 in PyTorch", tbl_cell_style), Paragraph("Canine Image Corpus", tbl_cell_style), Paragraph("82.5% Accuracy", tbl_cell_center), Paragraph("Sensitive to lighting and pose changes", tbl_cell_style)],
        [Paragraph("Hussain et al. (2025) [8]", tbl_cell_style), Paragraph("InceptionV3 + Background Rem.", tbl_cell_style), Paragraph("Stanford Dogs", tbl_cell_style), Paragraph("91.2% Accuracy", tbl_cell_center), Paragraph("Background removal clips ears and tails", tbl_cell_style)],
        [Paragraph("Ghotra et al. (2023) [9]", tbl_cell_style), Paragraph("MobileNetV2 + Flask", tbl_cell_style), Paragraph("Kaggle Dog Breeds", tbl_cell_style), Paragraph("High Train Accuracy", tbl_cell_center), Paragraph("Overfitting on small sample subsets", tbl_cell_style)],
        [Paragraph("Bankar et al. (2025) [10]", tbl_cell_style), Paragraph("CNN + Facial Hub", tbl_cell_style), Paragraph("Online Dog Images", tbl_cell_style), Paragraph("70.0% Test Accuracy", tbl_cell_center), Paragraph("20% generalization gap between train/test", tbl_cell_style)],
        [Paragraph("Zou et al. (2020) [11]", tbl_cell_style), Paragraph("WS-DAN & TBMSL-Net", tbl_cell_style), Paragraph("Tsinghua Dogs", tbl_cell_style), Paragraph("86.4% Accuracy", tbl_cell_center), Paragraph("Complex multi-stage attention networks", tbl_cell_style)],
        [Paragraph("Perera & Patel (2019) [12]", tbl_cell_style), Paragraph("Deep Novelty Detection", tbl_cell_style), Paragraph("Stanford Dogs", tbl_cell_style), Paragraph("80.1% Accuracy", tbl_cell_center), Paragraph("Sensitive to detection threshold tuning", tbl_cell_style)],
    ]
    t_lit_pdf = Table(lit_table_data, colWidths=[105, 95, 95, 80, 140])
    t_lit_pdf.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_header_bg),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_alt_row]),
    ]))
    story.append(t_lit_pdf)
    story.append(Spacer(1, 6))

    story.append(Paragraph("2.4 Research Gaps", h2_style))
    add_p("Our survey of previous work highlighted four recurring shortcomings:")
    add_numbered("1", "Absence of Input Validation: Nearly all surveyed systems assume users will only submit valid dog images. Uploading a non-dog image results in an erroneous breed prediction with false high confidence.")
    add_numbered("2", "Heavy Hardware Footprints: Several high-performing models rely on large architectures (VGG-19, DenseNet201) that require dedicated GPUs and exhibit high latency on standard web hosts.")
    add_numbered("3", "Single Prediction Outputs: Most tools output only a single breed label without indicating confidence or showing alternative candidate breeds.")
    add_numbered("4", "Lack of Practical Web Deployment: Many existing studies stop at model evaluation in notebooks, lacking user accounts, prediction history, database persistence, and downloadable documentation.")

    story.append(Paragraph("2.5 Selection of MobileNetV2", h2_style))
    add_p(
        "To resolve these shortcomings, our team selected MobileNetV2 as our core neural backbone. MobileNetV2 was designed "
        "specifically for efficient vision applications by introducing inverted residuals and linear bottlenecks. Instead of applying "
        "expensive full convolutions across all channels, it splits convolution into depthwise separable layers. This reduces the total "
        "parameter count to approximately 3.4 million parameters, resulting in a lightweight model file of around 14 MB. On a standard "
        "CPU, MobileNetV2 completes a forward pass in 120–160 milliseconds, making it ideal for interactive web deployment."
    )
    story.append(PageBreak())

    # =========================================================================
    # CHAPTER 3 – DATASET DESCRIPTION AND PREPROCESSING
    # =========================================================================
    mark("CH3")
    story.append(Paragraph("Chapter 3 – Dataset Description and Preprocessing", h1_style))
    
    story.append(Paragraph("3.1 Stanford Dogs Dataset Overview", h2_style))
    add_p(
        "Our project utilizes the Stanford Dogs dataset, a benchmark fine-grained visual corpus originally prepared by Khosla et al. [13]. "
        "The dataset contains photographic images of 120 purebred domestic dog varieties from around the world. We utilized the standardized "
        "Kaggle distribution, which contains exactly 10,222 labeled JPEG photographs."
    )

    story.append(Paragraph("3.2 Dataset Distribution and Partitioning", h2_style))
    add_p(
        "To ensure rigorous evaluation and prevent data leakage, we split the 10,222 images into stratified training, validation, "
        "and testing subsets using a 70% / 15% / 15% division ratio with a fixed pseudorandom seed. Stratification ensures that each breed "
        "maintains the same relative representation across all three partitions."
    )

    mark("T31")
    story.append(Spacer(1, 4))
    story.append(Paragraph("Table 3.1: Dataset Split and Partitioning Strategy", caption_style))
    split_table_data = [
        [Paragraph("<b>Dataset Partition</b>", tbl_header_style), Paragraph("<b>Number of Images</b>", tbl_header_style), Paragraph("<b>Percentage</b>", tbl_header_style), Paragraph("<b>Operational Purpose</b>", tbl_header_style)],
        [Paragraph("Training Subset", tbl_cell_style), Paragraph("7,155", tbl_cell_center), Paragraph("70.0%", tbl_cell_center), Paragraph("Feature extraction and backpropagation weight optimization", tbl_cell_style)],
        [Paragraph("Validation Subset", tbl_cell_style), Paragraph("1,533", tbl_cell_center), Paragraph("15.0%", tbl_cell_center), Paragraph("Hyperparameter tuning, early stopping, and checkpointing", tbl_cell_style)],
        [Paragraph("Testing Subset", tbl_cell_style), Paragraph("1,534", tbl_cell_center), Paragraph("15.0%", tbl_cell_center), Paragraph("Strictly held-out unbiased final performance evaluation", tbl_cell_style)],
        [Paragraph("<b>Total Dataset</b>", tbl_cell_style), Paragraph("<b>10,222</b>", tbl_cell_center), Paragraph("<b>100.0%</b>", tbl_cell_center), Paragraph("Complete Stanford Dogs benchmark image corpus", tbl_cell_style)],
    ]
    t_split_pdf = Table(split_table_data, colWidths=[110, 80, 65, 260])
    t_split_pdf.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_header_bg),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('ROWBACKGROUNDS', (0,1), (-1,-2), [colors.white, c_alt_row]),
        ('BACKGROUND', (0,-1), (-1,-1), c_header_bg),
    ]))
    story.append(t_split_pdf)
    story.append(Spacer(1, 6))

    add_p(
        "Across all 120 breeds, the average image count is 85.18 images per class, with a median of 82 images. The dataset exhibits "
        "mild class variation: Scottish Deerhound has the highest count with 126 images, while Briard and Eskimo Dog have the lowest count "
        "with 66 images each. The majority of breeds have between 75 and 95 images, providing a relatively balanced distribution."
    )

    story.append(Paragraph("3.3 Data Preprocessing Steps", h2_style))
    add_p("Raw user photographs arrive in various resolutions, aspect ratios, and color formats. Preprocessing standardizes the inputs:")
    add_numbered("1", "RGB Format Standardization: Images are verified to ensure standard 3-channel RGB format, discarding alpha transparency channels or converting single-channel grayscale images.")
    add_numbered("2", "Spatial Resizing: Each input image is resized to uniform dimensions of 224 x 224 pixels using bilinear interpolation.")
    add_numbered("3", "Pixel Normalization: Pixel values in [0, 255] are rescaled to [-1.0, +1.0] using MobileNetV2's standard normalization formula: x_norm = (x / 127.5) - 1.0.")
    add_numbered("4", "Batch Dimension Expansion: The preprocessed array is expanded into a 4-dimensional tensor of shape (1, 224, 224, 3) for model execution.")

    story.append(Paragraph("3.4 Data Augmentation Techniques", h2_style))
    add_p(
        "With an average of ~60 training samples per breed, training a deep network without augmentation increases the risk of overfitting. "
        "To increase sample variety during training, we applied real-time data augmentations:"
    )
    add_bullet("Random Horizontal Flipping (p = 0.5): Teaches the model that canine orientation does not change breed identity.")
    add_bullet("Random Rotation (up to ±15 degrees): Accommodates slight camera tilting in user photographs.")
    add_bullet("Random Zoom (up to ±10%): Simulates variations in subject distance from the camera.")
    add_bullet("Random Horizontal and Vertical Shifts (up to ±10%): Prevents the network from relying on dogs being perfectly centered.")

    story.append(Paragraph("3.5 Visual Challenges in Canine Images", h2_style))
    add_p("Exploratory analysis of the dataset revealed three primary visual challenges:")
    add_bullet("High Intra-Class Variation: Dogs of the same breed appear in different coat colors (e.g., black, yellow, and chocolate Labradors), diverse postures (sitting, running, lying down), and varying ages.")
    add_bullet("Low Inter-Class Differences: Closely related breeds possess nearly identical head shapes and body proportions (e.g., Siberian Husky vs. Alaskan Malamute), requiring the model to capture subtle cues.")
    add_bullet("Background Noise: Many images contain complex outdoor backgrounds such as grass, snow, furniture, or human handlers that can mislead the classifier if not regularized.")
    story.append(PageBreak())

    # =========================================================================
    # CHAPTER 4 – METHODOLOGY
    # =========================================================================
    mark("CH4")
    story.append(Paragraph("Chapter 4 – Methodology", h1_style))
    
    story.append(Paragraph("4.1 System Overview", h2_style))
    add_p(
        "The Dog Breed Identification system is an end-to-end web application that takes an uploaded image, processes it through "
        "a trained deep learning model, and returns the predicted breed along with confidence scores. The complete system consists "
        "of a client-side user interface, a Flask web server, a trained MobileNetV2 neural network, and a MySQL relational database. "
        "When a user selects an image and submits it, the application validates the file, prepares the image tensor, runs inference, "
        "and presents the Top-3 most likely breeds on the results page."
    )

    story.append(Paragraph("4.2 Dataset and Image Input", h2_style))
    add_p(
        "The system accepts common image formats including JPEG and PNG. On the client side, JavaScript checks that the file is not empty "
        "and does not exceed 10 MB. Once the file is submitted, the Flask backend sanitizes the filename using Werkzeug's secure_filename() "
        "utility to prevent directory traversal vulnerabilities and temporarily saves the image in the upload folder for processing."
    )

    story.append(Paragraph("4.3 Image Preprocessing", h2_style))
    add_p("Before an image can be evaluated by the neural network, it passes through four standard preprocessing steps:")
    add_numbered("1", "Image Validation: The server verifies that the uploaded file is a valid, readable image using PIL. If the file is corrupt, an error message is returned.")
    add_numbered("2", "RGB Conversion: Single-channel grayscale images or four-channel CMYK/RGBA images are converted into standard 3-channel RGB format.")
    add_numbered("3", "Resizing: The image is resized to 224 x 224 pixels using bilinear interpolation to match MobileNetV2's expected input dimensions.")
    add_numbered("4", "Pixel Normalization: Pixel values ranging from 0 to 255 are normalized into the [-1.0, +1.0] range required by MobileNetV2.")

    story.append(Paragraph("4.4 MobileNetV2 Model", h2_style))
    add_p(
        "MobileNetV2 is a convolutional neural network developed by Google, optimized for high performance on resource-constrained devices. "
        "Unlike standard CNNs that apply heavy convolution operations across all channels simultaneously, MobileNetV2 uses depthwise separable "
        "convolutions. This splits the operation into two smaller steps: a depthwise convolution that applies a single filter per input channel, "
        "followed by a pointwise convolution that combines channel outputs linearly."
    )
    add_p(
        "MobileNetV2 also introduces inverted residual blocks, where the network temporarily expands feature channels, applies filtering, "
        "and projects them back to a compact representation with linear bottlenecks. These architectural innovations reduce the model size to "
        "only 3.4 million parameters (~14 MB file size) while preserving high accuracy, making it ideal for our web application."
    )

    story.append(Paragraph("4.5 Transfer Learning and Model Training", h2_style))
    add_p(
        "Transfer learning allows us to utilize patterns learned from a massive dataset (ImageNet) and apply them to our 120 dog breeds. "
        "Because ImageNet already includes many animal categories, the pre-trained weights provide excellent initial feature extractors. "
        "Our model was trained in two sequential phases:"
    )
    add_p(
        "Phase 1 – Feature Extraction (Frozen Base): In the first phase, all 155 layers of the pre-trained MobileNetV2 base were frozen. "
        "A custom classification head comprising GlobalAveragePooling2D, a Dropout layer (rate = 0.3), and a Dense Softmax layer with 120 "
        "outputs was added. We trained this classification head for 10 epochs using the Adam optimizer with a learning rate of 1e-3. "
        "This allowed the new output weights to stabilize without disrupting the pre-trained feature filters."
    )
    add_p(
        "Phase 2 – Fine-Tuning (Top 30 Layers Unfrozen): In the second phase, we unfroze the top 30 convolutional layers of the base model "
        "while keeping the earlier layers frozen. We continued training for 5 epochs using Adam with a much lower learning rate (1e-5). "
        "This allowed higher-level filters to adapt to fine canine facial contours and coat textures without causing catastrophic forgetting."
    )

    mark("T41")
    story.append(Spacer(1, 4))
    story.append(Paragraph("Table 4.1: Neural Network Layer Progression and Parameter Distribution", caption_style))
    layer_table_data = [
        [Paragraph("<b>Layer Component</b>", tbl_header_style), Paragraph("<b>Output Shape</b>", tbl_header_style), Paragraph("<b>Parameters</b>", tbl_header_style), Paragraph("<b>Function in Architecture</b>", tbl_header_style)],
        [Paragraph("InputLayer", tbl_cell_style), Paragraph("(None, 224, 224, 3)", tbl_cell_center), Paragraph("0", tbl_cell_center), Paragraph("Accepts normalized RGB image tensors", tbl_cell_style)],
        [Paragraph("MobileNetV2 Base (155 layers)", tbl_cell_style), Paragraph("(None, 7, 7, 1280)", tbl_cell_center), Paragraph("2,257,984", tbl_cell_center), Paragraph("Depthwise separable feature extraction", tbl_cell_style)],
        [Paragraph("GlobalAveragePooling2D", tbl_cell_style), Paragraph("(None, 1280)", tbl_cell_center), Paragraph("0", tbl_cell_center), Paragraph("Spatial pooling to 1D feature vector", tbl_cell_style)],
        [Paragraph("Dropout (0.3 rate)", tbl_cell_style), Paragraph("(None, 1280)", tbl_cell_center), Paragraph("0", tbl_cell_center), Paragraph("Regularization preventing overfitting", tbl_cell_style)],
        [Paragraph("Dense (Softmax)", tbl_cell_style), Paragraph("(None, 120)", tbl_cell_center), Paragraph("153,720", tbl_cell_center), Paragraph("Class probability output across 120 breeds", tbl_cell_style)],
    ]
    t_layer_pdf = Table(layer_table_data, colWidths=[125, 95, 65, 230])
    t_layer_pdf.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_header_bg),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_alt_row]),
    ]))
    story.append(t_layer_pdf)
    story.append(Spacer(1, 6))

    story.append(Paragraph("4.6 Breed Prediction", h2_style))
    add_p(
        "When an image tensor is passed through the trained network, the final Dense layer with Softmax activation produces an array of 120 "
        "probabilities summing to 1.0. Rather than displaying only the single highest probability, our application sorts the outputs to "
        "identify the Top-3 predictions with their confidence percentages. Displaying Top-3 candidates provides transparency and helps "
        "users when evaluating similar breeds or mixed-breed dogs."
    )

    story.append(Paragraph("4.7 Web Application and Database Integration", h2_style))
    add_p(
        "The web application is built with Python Flask 3.0, which coordinates between the user interface, the deep learning model, and "
        "the MySQL database. When a user submits an image, Flask handles the multipart form request, calls the preprocessing and prediction "
        "functions, saves prediction details into the database, and renders the result template. For authenticated users, past predictions "
        "are linked to their account and displayed in their personal history log."
    )

    story.append(Paragraph("4.8 Overall Working Procedure", h2_style))
    add_p("The complete operational workflow of the application follows eight clear sequential steps:")
    add_numbered("1", "User opens the web application in a browser and navigates to the identification page.")
    add_numbered("2", "User uploads a dog photograph via the drag-and-drop or file picker interface.")
    add_numbered("3", "The application validates the file format (.jpg, .jpeg, .png) and confirms the file size is under 10 MB.")
    add_numbered("4", "The image is preprocessed by converting to RGB, resizing to 224 x 224 pixels, and normalizing pixel values to [-1, +1].")
    add_numbered("5", "The system performs canine verification using ImageNet synsets to ensure the image contains a dog.")
    add_numbered("6", "The fine-tuned MobileNetV2 classifier processes the normalized tensor and computes breed probabilities.")
    add_numbered("7", "The application formats and displays the Top-3 predicted breeds with confidence percentages.")
    add_numbered("8", "The prediction details, image path, and timestamp are saved into the MySQL database.")
    story.append(PageBreak())

    # =========================================================================
    # CHAPTER 5 – SYSTEM IMPLEMENTATION AND WEB APPLICATION
    # =========================================================================
    mark("CH5")
    story.append(Paragraph("Chapter 5 – System Implementation and Web Application", h1_style))
    
    story.append(Paragraph("5.1 Technology Stack", h2_style))
    add_p("The project implementation utilizes an integrated open-source software stack:")
    add_bullet("Python 3.13: Primary backend programming language used for machine learning and web logic.")
    add_bullet("TensorFlow 2.18 / Keras: Deep learning framework used for model training, transfer learning, and tensor inference.")
    add_bullet("Flask 3.0: Lightweight Python WSGI web framework managing HTTP routing and template rendering.")
    add_bullet("MySQL 8.0: Relational database management system persisting user accounts, prediction logs, favorites, and feedback.")
    add_bullet("ReportLab 5.1: PDF generation library used to build downloadable prediction certificates.")
    add_bullet("Frontend Technologies: Semantic HTML5, CSS3 with a cream-and-brown palette, and JavaScript for client-side interactions.")

    story.append(Paragraph("5.2 Application Architecture and Routes", h2_style))
    add_p("The Flask application organizes functionality into several core routes:")
    add_bullet("GET / : Homepage with project overview and image upload portal.")
    add_bullet("POST /predict : Accepts uploaded photographs, runs preprocessing and model inference, and returns prediction results.")
    add_bullet("GET /breed_info : Interactive directory displaying traits, history, and characteristics for all 120 breeds.")
    add_bullet("GET /compare : Side-by-side comparison interface allowing users to evaluate physical traits across any two breeds.")
    add_bullet("GET/POST /login and /signup : User authentication routes managing registration and session cookies.")
    add_bullet("GET /history : Displays past prediction history for logged-in users with saved image thumbnails.")
    add_bullet("POST /feedback : Collects user ratings (1 to 5 stars) and comments stored directly in MySQL.")
    add_bullet("GET /download_report/<prediction_id> : Dynamically generates and downloads an official PDF prediction report.")

    story.append(Paragraph("5.3 MySQL Relational Database Schema", h2_style))
    add_p("The database architecture consists of four normalized relational tables designed to ensure data consistency:")

    mark("T51")
    story.append(Spacer(1, 4))
    story.append(Paragraph("Table 5.1: MySQL Relational Database Schema and Entity Relationships", caption_style))
    db_table_data = [
        [Paragraph("<b>Table Name</b>", tbl_header_style), Paragraph("<b>Primary Key</b>", tbl_header_style), Paragraph("<b>Foreign Keys</b>", tbl_header_style), Paragraph("<b>Key Attributes Stored</b>", tbl_header_style)],
        [Paragraph("users", tbl_cell_style), Paragraph("user_id (INT)", tbl_cell_center), Paragraph("None", tbl_cell_center), Paragraph("username, email, password_hash, is_admin, created_at", tbl_cell_style)],
        [Paragraph("prediction_history", tbl_cell_style), Paragraph("prediction_id (INT)", tbl_cell_center), Paragraph("user_id -> users(user_id)", tbl_cell_center), Paragraph("image_path, predicted_breed, confidence, top3_results (JSON), model_version, created_at", tbl_cell_style)],
        [Paragraph("favorite_breeds", tbl_cell_style), Paragraph("favorite_id (INT)", tbl_cell_center), Paragraph("user_id -> users(user_id)", tbl_cell_center), Paragraph("breed_name, created_at (Unique: user_id, breed_name)", tbl_cell_style)],
        [Paragraph("feedback", tbl_cell_style), Paragraph("feedback_id (INT)", tbl_cell_center), Paragraph("user_id -> users(user_id)", tbl_cell_center), Paragraph("rating (1–5), message (TEXT), created_at", tbl_cell_style)],
    ]
    t_db_pdf = Table(db_table_data, colWidths=[90, 85, 110, 230])
    t_db_pdf.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_header_bg),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_alt_row]),
    ]))
    story.append(t_db_pdf)
    story.append(Spacer(1, 6))

    story.append(Paragraph("5.4 Dynamic PDF Prediction Certificate Engine", h2_style))
    add_p(
        "To provide users with a permanent record of their prediction, we integrated Python ReportLab 5.1. When a user requests "
        "a report, the application fetches the record from MySQL, loads the uploaded image thumbnail, and compiles a clean PDF "
        "certificate. The certificate contains the institution details, prediction date and time, uploaded image thumbnail, primary "
        "predicted breed, percentage confidence, Top-3 alternative candidates, model version, and an academic disclaimer."
    )

    story.append(Paragraph("5.5 User Authentication and Security", h2_style))
    add_p(
        "Security is handled using industry-standard practices: user passwords are encrypted using PBKDF2 with SHA-256 via Werkzeug; "
        "session cookies are configured with HttpOnly flags to mitigate cross-site scripting risks; and all database interactions use "
        "parameterized SQL queries to eliminate SQL injection vulnerabilities. The administrative dashboard is restricted to users with "
        "verified admin status."
    )
    story.append(PageBreak())

    # =========================================================================
    # CHAPTER 6 – EXPERIMENTAL RESULTS
    # =========================================================================
    mark("CH6")
    story.append(Paragraph("Chapter 6 – Experimental Results", h1_style))
    
    story.append(Paragraph("6.1 Model Training Progress", h2_style))
    add_p(
        "Model training was performed across 15 total epochs using our two-phase protocol. In Phase 1 (Epochs 1 to 10), the pre-trained "
        "MobileNetV2 base remained frozen while only the newly initialized classification layers were trained. During this phase, training "
        "accuracy increased steadily from 31.2% in Epoch 1 to 86.4% in Epoch 10, while validation accuracy reached 79.8%. The validation "
        "loss decreased smoothly from 2.124 to 0.742, confirming that the new classification weights stabilized quickly."
    )
    add_p(
        "In Phase 2 (Epochs 11 to 15), the top 30 convolutional layers of MobileNetV2 were unfrozen for fine-tuning with a lower learning "
        "rate of 1e-5. This enabled high-level spatial filters to adapt to fine canine facial features and coat patterns without causing "
        "gradient instability. By Epoch 15, training accuracy reached 92.3%, validation accuracy reached 82.4%, and validation loss decreased "
        "to 0.661. The steady decline in validation loss across both phases demonstrated that our dropout rate (0.3) and learning rate "
        "schedule prevented severe overfitting on the training data."
    )

    story.append(Paragraph("6.2 Quantitative Evaluation Metrics", h2_style))
    add_p(
        "The finalized model was evaluated on the held-out test split of 1,534 images that were never seen during training or validation. "
        "Table 6.1 presents the quantitative performance metrics calculated directly from model evaluation."
    )

    mark("T61")
    story.append(Spacer(1, 4))
    story.append(Paragraph("Table 6.1: Overall Quantitative Evaluation Metrics on Held-Out Test Set (1,534 Images)", caption_style))
    met_table_data = [
        [Paragraph("<b>Evaluation Metric</b>", tbl_header_style), Paragraph("<b>Measured Value</b>", tbl_header_style), Paragraph("<b>Operational Interpretation</b>", tbl_header_style)],
        [Paragraph("<b>Top-1 Test Accuracy</b>", tbl_cell_style), Paragraph("<b>77.64%</b>", tbl_cell_center), Paragraph("Exact ground-truth breed match on held-out test images", tbl_cell_style)],
        [Paragraph("<b>Top-5 Test Accuracy</b>", tbl_cell_style), Paragraph("<b>96.87%</b>", tbl_cell_center), Paragraph("Correct breed present within model's top 5 candidates", tbl_cell_style)],
        [Paragraph("Test Categorical Cross-Entropy Loss", tbl_cell_style), Paragraph("0.7036", tbl_cell_center), Paragraph("Cross-entropy loss on unaugmented test images", tbl_cell_style)],
        [Paragraph("Macro Average F1-Score", tbl_cell_style), Paragraph("76.91%", tbl_cell_center), Paragraph("Unweighted harmonic mean across all 120 categories", tbl_cell_style)],
        [Paragraph("Weighted Average F1-Score", tbl_cell_style), Paragraph("77.35%", tbl_cell_center), Paragraph("Support-weighted harmonic mean across all test samples", tbl_cell_style)],
    ]
    t_met_pdf = Table(met_table_data, colWidths=[150, 85, 280])
    t_met_pdf.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_header_bg),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('BACKGROUND', (0,1), (-1,2), colors.HexColor("#FEF9E7")),
        ('ROWBACKGROUNDS', (0,3), (-1,-1), [colors.white, c_alt_row]),
    ]))
    story.append(t_met_pdf)
    story.append(Spacer(1, 6))

    add_p(
        "The Top-1 accuracy of 77.64% indicates solid performance across a complex 120-class biological dataset. More importantly, "
        "the Top-5 accuracy of 96.87% confirms that in almost 97 out of 100 cases, the true breed is among the top 5 candidates identified "
        "by the model. This high Top-5 accuracy supports our decision to present Top-3 predictions in the user interface, ensuring that users "
        "receive relevant candidates even when photographs are taken from challenging angles."
    )
    story.append(PageBreak())

    # =========================================================================
    # CHAPTER 7 – CONCLUSION AND FUTURE ENHANCEMENTS
    # =========================================================================
    mark("CH7")
    story.append(Paragraph("Chapter 7 – Conclusion and Future Enhancements", h1_style))
    
    story.append(Paragraph("7.1 Conclusion", h2_style))
    add_p(
        "In this project, our team designed, built, and evaluated a complete dog breed identification system capable of classifying "
        "120 recognized breeds from photographic images. Fine-grained canine classification is a difficult task because different breeds "
        "often share similar silhouettes and coat patterns, while dogs of the same breed can vary widely in appearance. By addressing "
        "these challenges through modern machine learning and web development practices, we successfully developed a working application "
        "that delivers reliable predictions."
    )
    add_p(
        "We used the Stanford Dogs dataset of 10,222 images partitioned into stratified training (7,155 images), validation (1,533 images), "
        "and testing (1,534 images) subsets. To overcome the limitation of having only about 60 training images per breed, we implemented "
        "transfer learning using MobileNetV2 pre-trained on ImageNet. Training the model in two phases—first training the classification "
        "head on frozen features and then fine-tuning the top 30 layers with a lower learning rate—enabled the model to converge smoothly "
        "without overfitting."
    )
    add_p(
        "On the held-out test split, the model achieved a Top-1 accuracy of 77.64% and a Top-5 accuracy of 96.87%, with a categorical loss "
        "of 0.7036 and a Weighted F1-score of 77.35%. To prevent non-dog images from producing misleading predictions, we incorporated an "
        "upstream canine verification filter based on ImageNet synsets. The application presents Top-3 predictions with confidence scores, "
        "providing a transparent and practical experience for end users."
    )
    add_p(
        "We integrated the trained model into a full-stack Flask web application backed by MySQL. The application supports user accounts, "
        "prediction history logging, breed trait exploration, side-by-side breed comparisons, user feedback, and downloadable PDF certificates. "
        "Through completing this project, our team gained valuable practical experience in the full data science workflow, including dataset "
        "preparation, transfer learning, model evaluation, database integration, and web deployment."
    )

    story.append(Paragraph("7.2 Limitations", h2_style))
    add_p("While the system functions effectively, it possesses several recognized limitations:")
    add_numbered("1", "Single Dog Assumption: The system is designed for images containing a single dog; when multiple dogs are present, it evaluates only the most visually prominent animal.")
    add_numbered("2", "Purebred Bias: The training data consists exclusively of 120 purebred varieties, meaning that mixed-breed dogs are classified into their closest ancestral purebred matches.")
    add_numbered("3", "Sensitivity to Extreme Lighting: Photographs with heavy shadows, severe backlighting, or low resolution can degrade classification confidence.")
    add_numbered("4", "Visual Similarity Between Related Breeds: Certain closely related breeds, such as Welsh Corgi varieties or Whippets and Italian Greyhounds, share very similar features that can lead to reciprocal misclassifications.")

    story.append(Paragraph("7.3 Future Enhancements", h2_style))
    add_p("Based on our findings, we suggest the following realistic enhancements for future iterations:")
    add_numbered("1", "Multi-Dog Detection: Incorporating an object detection model (such as YOLO) to detect, crop, and classify multiple dogs in a single image independently.")
    add_numbered("2", "Mixed-Breed Ancestry Estimation: Extending the output layer to multi-label regression to estimate percentage ancestry for crossbreed dogs.")
    add_numbered("3", "Mobile Application Deployment: Exporting the model to TensorFlow Lite (TFLite) for on-device offline inference on Android and iOS smartphones.")
    add_numbered("4", "Expanded Breed Catalog: Adding more international and indigenous dog breeds to broaden the applicability of the system.")
    story.append(PageBreak())

    # =========================================================================
    # REFERENCES
    # =========================================================================
    mark("REFS")
    story.append(Paragraph("REFERENCES", h1_style))
    story.append(Spacer(1, 6))

    references = [
        "[1] S. Selvaraj, R. Thangarajan, S. Anbukkarasi, and S. Yuvan Prasad, \"ResNet50 Architecture Based Dog Breed Identification Using Deep Learning,\" in Proc. Int. Conf. on Computational Intelligence and Knowledge Economy, 2023.",
        "[2] P. Borwarnginn, W. Kusakunniran, S. Karnjanapreechakorn, and K. Thongkanchorn, \"Knowing Your Dog Breed: Identifying a Dog Breed with Deep Learning,\" in Proc. Int. Conf. on Information Technology, 2021.",
        "[3] S. A. Bokhari, P. Mukherjee, A. S. Singh, S. Shaik, and J. K. Mathew, \"Convolutional Neural Network Based Dog Breed Classification,\" in Proc. Int. Conf. on Innovative Computing and Communication, 2022.",
        "[4] T. Kumaravel, P. Natesan, V. E. Sathishkumar, S. S. N, S. G, and U. V, \"Automatic Dog Breed Classification Using Deep Learning,\" in Proc. Int. Conf. on Smart Systems and Inventive Technology, 2023.",
        "[5] N. Banakar, Raghavendra B. U., S. G. S., T. K. Vani, and V. M. Vishnu, \"Dog Breed Identification Using Deep Learning,\" International Journal of Advanced Research in Computer Science and Software Engineering, vol. 13, no. 5, 2023.",
        "[6] B. Valarmathi, N. S. Gupta, G. Prakash, R. H. Reddy, S. Saravanan, and P. Shanmugasundaram, \"Hybrid Deep Learning Algorithms for Dog Breed Identification—A Comparative Analysis,\" IEEE Access, vol. 11, pp. 45120–45132, 2023.",
        "[7] S. R. Basha, I. Ganesh, G. R. Reddy, and A. Hans, \"Dogs Breed Classification Using Deep Learning,\" in Proc. Int. Conf. on Artificial Intelligence and Smart Systems, 2021.",
        "[8] S. S. Hussain, K. S. R. Murthy, C. S. Rani, T. Nanuvala, C. R. Kumar, and G. Sathar, \"Automated Dog Breed Recognition Using CNN-Based Transfer Learning,\" in Proc. Int. Conf. on Advances in Computer Engineering & Communication Systems, 2025.",
        "[9] A. S. Ghotra, H. Kour, A. Hasan, and A. Khan, \"Dog Breed Identification,\" in Proc. Int. Conf. on Data Science and Machine Learning, 2023.",
        "[10] J. Bankar, A. Nalawade, S. Wali, A. Rane, and H. Matlani, \"AI Based Dog Breed Prediction Model and Virtual Canine Hub,\" International Journal of Computer Applications, vol. 186, no. 14, 2025.",
        "[11] D.-N. Zou, S.-H. Zhang, T.-J. Mu, and M. Zhang, \"A New Dataset of Dog Breed Images and a Benchmark for Fine-Grained Classification,\" Computational Visual Media, vol. 6, no. 4, pp. 477–487, 2020.",
        "[12] P. Perera and V. M. Patel, \"Deep Transfer Learning for Multiple Class Novelty Detection,\" in Proc. IEEE/CVF Conf. on Computer Vision and Pattern Recognition (CVPR), 2019, pp. 1154–1162.",
        "[13] A. Khosla, N. Jayadevaprakash, B. Yao, and L. Fei-Fei, \"Novel Dataset for Fine-Grained Image Categorization: Stanford Dogs,\" in Proc. CVPR Workshop on Fine-Grained Visual Categorization, Colorado Springs, CO, USA, 2011.",
        "[14] M. Sandler, A. Howard, M. Zhu, A. Zhmoginov, and L.-C. Chen, \"MobileNetV2: Inverted Residuals and Linear Bottlenecks,\" in Proc. IEEE/CVF Conf. on Computer Vision and Pattern Recognition (CVPR), Salt Lake City, UT, USA, 2018, pp. 4510–4520."
    ]
    for ref in references:
        add_p(ref, space_after=6)
    story.append(PageBreak())

    # =========================================================================
    # PROJECT TEAM CONTRIBUTION DETAILS
    # =========================================================================
    mark("TEAM")
    story.append(Paragraph("PROJECT TEAM CONTRIBUTION DETAILS", h1_style))
    story.append(Spacer(1, 6))

    add_p(
        "This project was collaboratively designed, developed, and evaluated by the four team members listed below. "
        "Each member assumed primary ownership of specific modules while collaborating closely on overall system integration:"
    )
    story.append(Spacer(1, 6))

    story.append(Paragraph("Table 8.1: Project Team Contribution Details", caption_style))
    contrib_data = [
        [Paragraph("<b>Member Name</b>", tbl_header_style), Paragraph("<b>Roll Number</b>", tbl_header_style), Paragraph("<b>Primary Module</b>", tbl_header_style), Paragraph("<b>Core Contributions</b>", tbl_header_style)],
        [Paragraph("K Goutham Nayak", tbl_cell_style), Paragraph("CS24B1081", tbl_cell_center), Paragraph("Backend Architecture & Reporting", tbl_cell_style), Paragraph("Flask routing, MySQL schema design, ReportLab PDF certificate engine, and authentication security.", tbl_cell_style)],
        [Paragraph("K Adithya", tbl_cell_style), Paragraph("CS24B1091", tbl_cell_center), Paragraph("Deep Learning & Model Training", tbl_cell_style), Paragraph("MobileNetV2 transfer learning, two-phase training strategy, hyperparameter tuning, and metric evaluation.", tbl_cell_style)],
        [Paragraph("R Mahesh Rathod", tbl_cell_style), Paragraph("CS24B1071", tbl_cell_center), Paragraph("Two-Stage Pipeline & Preprocessing", tbl_cell_style), Paragraph("Stage 1 canine presence filter, ImageNet synset mapping, data augmentation, and input validation.", tbl_cell_style)],
        [Paragraph("G Vishnu Vardhan", tbl_cell_style), Paragraph("CS24B1028", tbl_cell_center), Paragraph("Frontend UI/UX & Breed Directory", tbl_cell_style), Paragraph("Responsive interface design, Chart.js dashboard integration, breed directory, and side-by-side comparison.", tbl_cell_style)],
    ]
    t_contrib_pdf = Table(contrib_data, colWidths=[105, 75, 115, 220])
    t_contrib_pdf.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_header_bg),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_alt_row]),
    ]))
    story.append(t_contrib_pdf)

    return story


def generate_pdf_two_pass(output_path):
    # Pass 1: measure exact page positions
    page_dict = {}
    doc1 = SimpleDocTemplate(
        "temp_pass1.pdf",
        pagesize=A4, leftMargin=40, rightMargin=40, topMargin=46, bottomMargin=46
    )
    story1 = build_story(page_dict=None, collect_pages_dict=page_dict)
    doc1.build(story1, canvasmaker=AcademicCanvas)
    if os.path.exists("temp_pass1.pdf"):
        os.remove("temp_pass1.pdf")
    
    print(f"Pass 1 detected page mapping: {page_dict}")

    # Pass 2: generate with exact page numbers in TOC and LOT
    doc2 = SimpleDocTemplate(
        output_path,
        pagesize=A4, leftMargin=40, rightMargin=40, topMargin=46, bottomMargin=46
    )
    story2 = build_story(page_dict=page_dict, collect_pages_dict=None)
    doc2.build(story2, canvasmaker=AcademicCanvas)
    print(f"Pass 2 clean PDF successfully created at: {output_path}")

    return page_dict

# =========================================================================
# 3. REVISION SUMMARY GENERATOR
# =========================================================================

def generate_revision_summary(output_path):
    summary_text = """# REVISION SUMMARY: DOG BREED IDENTIFICATION PROJECT REPORT

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
"""
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(summary_text)
    print(f"Revision summary successfully written to: {output_path}")

# =========================================================================
# MAIN EXECUTION
# =========================================================================

if __name__ == "__main__":
    out_dir = "FINAL_REVISED_DOG_BREED_REPORT"
    os.makedirs(out_dir, exist_ok=True)
    
    docx_file = os.path.join(out_dir, "Dog_Breed_Identification_Final_Report.docx")
    pdf_file = os.path.join(out_dir, "Dog_Breed_Identification_Final_Report.pdf")
    summary_file = os.path.join(out_dir, "Revision_Summary.md")
    
    # 1. Run two-pass PDF generation to capture exact page numbers
    page_dict = generate_pdf_two_pass(pdf_file)
    
    # 2. Run DOCX generation with exact matching page numbers
    generate_docx(docx_file, page_map=page_dict)
    
    # 3. Generate Revision Summary
    generate_revision_summary(summary_file)
    
    print("All tasks completed successfully!")
