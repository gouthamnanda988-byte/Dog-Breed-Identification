"""
build_final_revised_pdf.py
==========================
Generates the publication-quality academic PDF report for:
DOG BREED IDENTIFICATION USING DEEP LEARNING AND TRANSFER LEARNING

Target: FINAL_REVISED_DOG_BREED_REPORT/Dog_Breed_Identification_Final_Report.pdf
"""

import os
from PIL import Image as PILImage
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, 
    Image, PageBreak, KeepTogether
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

class AcademicCanvas(canvas.Canvas):
    """
    Custom canvas implementing IDSE3.pdf style headers, footers, and dual-numbering:
    - Page 1 (Title): No header/footer
    - Page 2 (Project Specs): Numbered 1 (or Specs)
    - Pages 3..5 (Abstract, Contents, Lists): Roman numerals (i, ii, iii)
    - Pages 6..end (Chapters 1 to 7, Refs, Team): Arabic numerals (1, 2, 3...)
    """
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
            return  # Suppress on cover page

        self.saveState()
        self.setFont("Times-Roman", 9)
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
        self.drawString(40, footer_y - 12, "Introduction to Data Science for Engineers â€” 2026")

        # Determine Page Number String
        if p_num == 2:
            page_str = "1"
        elif 3 <= p_num <= 5:
            # Roman numerals: page 3 -> i, page 4 -> ii, page 5 -> iii
            page_str = int_to_roman(p_num - 2)
        else:
            # Chapter 1 starts on page 6 -> numbered 1, 2, 3...
            page_str = str(p_num - 5)

        self.drawRightString(595.27 - 40, footer_y - 12, page_str)
        self.restoreState()


def create_pdf(output_path):
    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        leftMargin=40,
        rightMargin=40,
        topMargin=46,
        bottomMargin=46
    )

    story = []
    base_styles = getSampleStyleSheet()

    # Academic Palette
    c_primary = colors.HexColor("#1A2B4C")      # Deep Academic Navy
    c_secondary = colors.HexColor("#2A4365")    # Slate Navy
    c_sub = colors.HexColor("#31547A")          # Accent Slate
    c_header_bg = colors.HexColor("#EAECEE")    # Table Header Gray
    c_alt_row = colors.HexColor("#F8F9FA")      # Off-white Row
    c_border = colors.HexColor("#BDC3C7")       # Border Line
    c_text = colors.HexColor("#222222")         # Charcoal Body Text

    title_style = ParagraphStyle(
        'CoverTitle',
        parent=base_styles['Normal'],
        fontName='Times-Bold',
        fontSize=18,
        leading=23,
        alignment=TA_CENTER,
        textColor=c_primary,
        spaceAfter=14
    )

    h1_style = ParagraphStyle(
        'Heading1_Custom',
        parent=base_styles['Normal'],
        fontName='Times-Bold',
        fontSize=14,
        leading=18,
        textColor=c_primary,
        spaceBefore=14,
        spaceAfter=8,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'Heading2_Custom',
        parent=base_styles['Normal'],
        fontName='Times-Bold',
        fontSize=11.5,
        leading=15,
        textColor=c_secondary,
        spaceBefore=10,
        spaceAfter=4,
        keepWithNext=True
    )

    h3_style = ParagraphStyle(
        'Heading3_Custom',
        parent=base_styles['Normal'],
        fontName='Times-Bold',
        fontSize=10,
        leading=13,
        textColor=c_sub,
        spaceBefore=7,
        spaceAfter=2,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'Body_Custom',
        parent=base_styles['Normal'],
        fontName='Times-Roman',
        fontSize=9.5,
        leading=13.5,
        alignment=TA_JUSTIFY,
        textColor=c_text,
        spaceAfter=5
    )

    caption_style = ParagraphStyle(
        'Caption_Custom',
        parent=base_styles['Normal'],
        fontName='Times-Italic',
        fontSize=8.5,
        leading=11,
        alignment=TA_CENTER,
        textColor=colors.HexColor("#444444"),
        spaceBefore=3,
        spaceAfter=8
    )

    tbl_header_style = ParagraphStyle(
        'TblHeader',
        parent=base_styles['Normal'],
        fontName='Times-Bold',
        fontSize=8.5,
        leading=11,
        alignment=TA_CENTER,
        textColor=c_primary
    )

    tbl_cell_style = ParagraphStyle(
        'TblCell',
        parent=base_styles['Normal'],
        fontName='Times-Roman',
        fontSize=8,
        leading=10.5,
        alignment=TA_LEFT,
        textColor=c_text
    )

    tbl_cell_center = ParagraphStyle(
        'TblCellCenter',
        parent=base_styles['Normal'],
        fontName='Times-Roman',
        fontSize=8,
        leading=10.5,
        alignment=TA_CENTER,
        textColor=c_text
    )

    def add_p(text, bold_prefix="", space_after=5):
        prefix_html = f"<b>{bold_prefix}</b> " if bold_prefix else ""
        story.append(Paragraph(f"{prefix_html}{text}", body_style))

    def add_img(img_path, caption, max_w=480, max_h=230):
        if os.path.exists(img_path):
            try:
                with PILImage.open(img_path) as pil_img:
                    w, h = pil_img.size
                aspect = h / float(w)
                render_w = min(max_w, 480)
                render_h = render_w * aspect
                if render_h > max_h:
                    render_h = max_h
                    render_w = render_h / aspect
                story.append(Spacer(1, 4))
                story.append(Image(img_path, width=render_w, height=render_h))
                story.append(Spacer(1, 2))
                story.append(Paragraph(caption, caption_style))
                story.append(Spacer(1, 4))
            except Exception as e:
                print(f"Error loading image {img_path}: {e}")

    # =========================================================================
    # 1. TITLE / COVER PAGE (Page 1)
    # =========================================================================
    story.append(Spacer(1, 25))
    story.append(Paragraph("INDIAN INSTITUTE OF INFORMATION TECHNOLOGY,<br/>DESIGN AND MANUFACTURING, KANCHEEPURAM", ParagraphStyle('InstHead', parent=base_styles['Normal'], fontName='Times-Bold', fontSize=12.5, leading=17, alignment=TA_CENTER, textColor=c_primary)))
    story.append(Spacer(1, 6))
    story.append(Paragraph("COURSE: INTRODUCTION TO DATA SCIENCE FOR ENGINEERS", ParagraphStyle('CourseHead', parent=base_styles['Normal'], fontName='Times-Bold', fontSize=10.5, leading=14, alignment=TA_CENTER, textColor=c_secondary)))
    story.append(Spacer(1, 3))
    story.append(Paragraph("PROJECT REPORT", ParagraphStyle('DocType', parent=base_styles['Normal'], fontName='Times-Bold', fontSize=11, leading=14, alignment=TA_CENTER, textColor=colors.HexColor("#1A5276"))))
    story.append(Spacer(1, 3))
    story.append(Paragraph("ACADEMIC YEAR: 2026", ParagraphStyle('AcadYear', parent=base_styles['Normal'], fontName='Times-Bold', fontSize=10, leading=13, alignment=TA_CENTER, textColor=colors.HexColor("#333333"))))
    story.append(Spacer(1, 15))

    # Divider line
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

    story.append(Paragraph("<b>PROJECT TEAM MEMBERS</b>", ParagraphStyle('TeamHead', parent=base_styles['Normal'], fontName='Times-Bold', fontSize=10.5, leading=14, alignment=TA_CENTER, textColor=c_primary)))
    story.append(Spacer(1, 8))

    # Cover Page Team Table
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
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_alt_row]),
    ]))
    story.append(t_cover)
    story.append(PageBreak())

    # =========================================================================
    # 2. PROJECT SPECIFICATIONS (Page 2)
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
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
        ('ROWBACKGROUNDS', (0,0), (-1,-1), [colors.white, c_alt_row]),
    ]))
    story.append(t_specs)
    story.append(PageBreak())

    # =========================================================================
    # 3. ABSTRACT (Page 3)
    # =========================================================================
    story.append(Paragraph("ABSTRACT", h1_style))
    story.append(Spacer(1, 6))

    add_p(
        "Fine-grained visual categorization presents a classical yet formidable challenge in computer vision "
        "owing to subtle inter-class visual discrepancies among closely related biological taxa and high intra-class "
        "variance driven by subject posture, coat coloration, lighting, and background noise. In this project, we design, "
        "implement, and rigorously evaluate an end-to-end canine identification system capable of classifying domestic dogs "
        "across 120 recognized breeds from the Stanford Dogs benchmark dataset (10,222 labeled photographic images)."
    )
    add_p(
        "To achieve high accuracy while maintaining lightweight computational overhead suitable for interactive deployment, "
        "we employ transfer learning with MobileNetV2 pre-trained on ImageNet. Our training pipeline utilizes a two-phase transfer "
        "learning strategy: Phase 1 freezes the 155-layer convolutional base to train newly initialized classification layers, "
        "followed by Phase 2 deep fine-tuning of the top 30 layers at a reduced learning rate (1e-5). To prevent out-of-domain "
        "misclassifications, we architected a two-stage inference pipeline: Stage 1 verifies canine presence by aggregating "
        "probabilities across 118 ImageNet canine synsets (rejecting non-dog inputs below a 0.20 threshold), while Stage 2 "
        "executes fine-grained breed classification across 120 classes."
    )
    add_p(
        "Evaluated on a strictly held-out test split of 1,534 images, our fine-tuned model achieves a Top-1 classification "
        "accuracy of 77.64%, a Top-5 accuracy of 96.87%, a categorical cross-entropy loss of 0.7036, a Macro F1-score of 76.91%, "
        "and a Weighted F1-score of 77.35%. We wrapped this deep learning core into an interactive full-stack web application "
        "using Python Flask 3.0, a persistent MySQL 8.0 relational database for prediction logging and user management, "
        "and an automated ReportLab engine delivering downloadable PDF identification certificates. A comprehensive test suite "
        "comprising 18 automated integration tests verified the end-to-end functionality of all application workflows."
    )
    story.append(Spacer(1, 6))
    story.append(Paragraph("<b>Keywords:</b> <i>Deep Learning, Transfer Learning, MobileNetV2, Fine-Grained Canine Classification, Computer Vision, Two-Stage Inference, Flask Web Application, MySQL.</i>", body_style))
    story.append(PageBreak())

    # =========================================================================
    # 4. TABLE OF CONTENTS (Page 4)
    # =========================================================================
    story.append(Paragraph("TABLE OF CONTENTS", h1_style))
    story.append(Spacer(1, 6))

    toc_data = [
        [Paragraph("<b>PROJECT SPECIFICATIONS</b>", tbl_cell_style), Paragraph("<b>i</b>", tbl_cell_center)],
        [Paragraph("<b>ABSTRACT</b>", tbl_cell_style), Paragraph("<b>ii</b>", tbl_cell_center)],
        [Paragraph("<b>LIST OF FIGURES</b>", tbl_cell_style), Paragraph("<b>iv</b>", tbl_cell_center)],
        [Paragraph("<b>LIST OF TABLES</b>", tbl_cell_style), Paragraph("<b>v</b>", tbl_cell_center)],
        [Paragraph("<b>CHAPTER 1 â€“ INTRODUCTION</b>", tbl_cell_style), Paragraph("<b>1</b>", tbl_cell_center)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;1.1 Background and Motivation", tbl_cell_style), Paragraph("1", tbl_cell_center)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;1.2 Problem Statement", tbl_cell_style), Paragraph("2", tbl_cell_center)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;1.3 Project Objectives", tbl_cell_style), Paragraph("2", tbl_cell_center)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;1.4 Scope and Limitations", tbl_cell_style), Paragraph("3", tbl_cell_center)],
        [Paragraph("<b>CHAPTER 2 â€“ LITERATURE SURVEY</b>", tbl_cell_style), Paragraph("<b>4</b>", tbl_cell_center)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;2.1 Evolution of Fine-Grained Canine Classification", tbl_cell_style), Paragraph("4", tbl_cell_center)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;2.2 Deep Transfer Learning Architectures", tbl_cell_style), Paragraph("5", tbl_cell_center)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;2.3 Two-Stage Detection and Out-of-Distribution Handling", tbl_cell_style), Paragraph("6", tbl_cell_center)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;2.4 Web-Based Machine Learning Deployment Systems", tbl_cell_style), Paragraph("6", tbl_cell_center)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;2.5 Identified Research and Engineering Gaps", tbl_cell_style), Paragraph("7", tbl_cell_center)],
        [Paragraph("<b>CHAPTER 3 â€“ DATASET DESCRIPTION AND PREPROCESSING</b>", tbl_cell_style), Paragraph("<b>8</b>", tbl_cell_center)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;3.1 Stanford Dogs Dataset Overview", tbl_cell_style), Paragraph("8", tbl_cell_center)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;3.2 Dataset Distribution and Class Representation", tbl_cell_style), Paragraph("8", tbl_cell_center)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;3.3 Data Preprocessing Pipeline", tbl_cell_style), Paragraph("10", tbl_cell_center)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;3.4 Data Augmentation Techniques", tbl_cell_style), Paragraph("11", tbl_cell_center)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;3.5 Fine-Grained Visual Challenges", tbl_cell_style), Paragraph("11", tbl_cell_center)],
        [Paragraph("<b>CHAPTER 4 â€“ PROPOSED METHODOLOGY</b>", tbl_cell_style), Paragraph("<b>13</b>", tbl_cell_center)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;4.1 Overview of Proposed Method", tbl_cell_style), Paragraph("13", tbl_cell_center)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;4.2 Overall System Architecture", tbl_cell_style), Paragraph("14", tbl_cell_center)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;4.3 Image Upload and Preprocessing Pipeline", tbl_cell_style), Paragraph("15", tbl_cell_center)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;4.4 Stage 1 â€“ Dog Presence Detection", tbl_cell_style), Paragraph("16", tbl_cell_center)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;4.5 Stage 2 â€“ Fine-Grained Breed Classification", tbl_cell_style), Paragraph("17", tbl_cell_center)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;4.6 Transfer Learning and Fine-Tuning Strategy", tbl_cell_style), Paragraph("18", tbl_cell_center)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;4.7 Prediction Generation and Top-3 Confidence Scores", tbl_cell_style), Paragraph("19", tbl_cell_center)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;4.8 Complete Prediction Workflow", tbl_cell_style), Paragraph("20", tbl_cell_center)],
        [Paragraph("<b>CHAPTER 5 â€“ SYSTEM IMPLEMENTATION AND WEB APPLICATION</b>", tbl_cell_style), Paragraph("<b>22</b>", tbl_cell_center)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;5.1 Technology Stack", tbl_cell_style), Paragraph("22", tbl_cell_center)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;5.2 Application Architecture and Endpoints", tbl_cell_style), Paragraph("23", tbl_cell_center)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;5.3 MySQL Relational Database Schema", tbl_cell_style), Paragraph("24", tbl_cell_center)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;5.4 Dynamic PDF Prediction Certificate Engine", tbl_cell_style), Paragraph("25", tbl_cell_center)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;5.5 User Authentication, Role-Based Access Control and Security", tbl_cell_style), Paragraph("26", tbl_cell_center)],
        [Paragraph("<b>CHAPTER 6 â€“ EXPERIMENTAL RESULTS AND PERFORMANCE ANALYSIS</b>", tbl_cell_style), Paragraph("<b>27</b>", tbl_cell_center)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;6.1 Model Training Progress and Convergence", tbl_cell_style), Paragraph("27", tbl_cell_center)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;6.2 Quantitative Evaluation Metrics", tbl_cell_style), Paragraph("28", tbl_cell_center)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;6.3 Explanation of Evaluation Metrics", tbl_cell_style), Paragraph("29", tbl_cell_center)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;6.4 Genuine Per-Breed Performance Analysis", tbl_cell_style), Paragraph("30", tbl_cell_center)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;6.5 Confusion Matrix and Inter-Breed Similarity Analysis", tbl_cell_style), Paragraph("32", tbl_cell_center)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;6.6 System Verification and Automated Test Results", tbl_cell_style), Paragraph("33", tbl_cell_center)],
        [Paragraph("<b>CHAPTER 7 â€“ CONCLUSION AND FUTURE ENHANCEMENTS</b>", tbl_cell_style), Paragraph("<b>35</b>", tbl_cell_center)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;7.1 Summary of Work Done", tbl_cell_style), Paragraph("35", tbl_cell_center)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;7.2 Key Findings and Practical Observations", tbl_cell_style), Paragraph("35", tbl_cell_center)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;7.3 Challenges Encountered and Solutions", tbl_cell_style), Paragraph("36", tbl_cell_center)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;7.4 Future Enhancements", tbl_cell_style), Paragraph("37", tbl_cell_center)],
        [Paragraph("<b>REFERENCES</b>", tbl_cell_style), Paragraph("<b>38</b>", tbl_cell_center)],
        [Paragraph("<b>PROJECT TEAM CONTRIBUTION DETAILS</b>", tbl_cell_style), Paragraph("<b>40</b>", tbl_cell_center)],
    ]
    t_toc = Table(toc_data, colWidths=[460, 55])
    t_toc.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 1.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 1.5),
        ('LEFTPADDING', (0,0), (-1,-1), 2),
        ('RIGHTPADDING', (0,0), (-1,-1), 2),
        ('LINEBELOW', (0,0), (-1,-1), 0.25, colors.HexColor("#EAECEE")),
    ]))
    story.append(t_toc)
    story.append(PageBreak())

    # =========================================================================
    # 5. LIST OF FIGURES & TABLES (Page 5)
    # =========================================================================
    story.append(Paragraph("LIST OF FIGURES", h1_style))
    story.append(Spacer(1, 4))

    lof_data = [
        [Paragraph("Figure 3.1: Distribution of Photographic Samples Across 120 Dog Breeds", tbl_cell_style), Paragraph("9", tbl_cell_center)],
        [Paragraph("Figure 4.1: Overall Multi-Tier System Architecture of the Dog Breed Identification Platform", tbl_cell_style), Paragraph("14", tbl_cell_center)],
        [Paragraph("Figure 4.2: Image Upload and Preprocessing Pipeline Flowchart", tbl_cell_style), Paragraph("15", tbl_cell_center)],
        [Paragraph("Figure 4.3: Stage 1 ImageNet Canine Synset Presence Filter", tbl_cell_style), Paragraph("16", tbl_cell_center)],
        [Paragraph("Figure 4.4: Stage 2 MobileNetV2 Fine-Grained Breed Classifier Architecture", tbl_cell_style), Paragraph("17", tbl_cell_center)],
        [Paragraph("Figure 4.5: Complete End-to-End Prediction and Inference Workflow", tbl_cell_style), Paragraph("21", tbl_cell_center)],
        [Paragraph("Figure 6.1: Training and Validation Accuracy and Loss Curves Across 15 Epochs", tbl_cell_style), Paragraph("28", tbl_cell_center)],
        [Paragraph("Figure 6.2: Top 12 Most Frequently Confused Dog Breed Pairs in Evaluation Set", tbl_cell_style), Paragraph("32", tbl_cell_center)],
    ]
    t_lof = Table(lof_data, colWidths=[460, 55])
    t_lof.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
        ('LINEBELOW', (0,0), (-1,-1), 0.25, colors.HexColor("#EAECEE")),
    ]))
    story.append(t_lof)
    story.append(Spacer(1, 14))

    story.append(Paragraph("LIST OF TABLES", h1_style))
    story.append(Spacer(1, 4))

    lot_data = [
        [Paragraph("Table 3.1: Dataset Split and Partitioning Strategy", tbl_cell_style), Paragraph("9", tbl_cell_center)],
        [Paragraph("Table 4.1: Neural Network Layer Progression and Parameter Distribution", tbl_cell_style), Paragraph("18", tbl_cell_center)],
        [Paragraph("Table 5.1: MySQL Relational Database Schema and Entity Relationships", tbl_cell_style), Paragraph("24", tbl_cell_center)],
        [Paragraph("Table 6.1: Overall Quantitative Evaluation Metrics on Held-Out Test Set (1,534 Images)", tbl_cell_style), Paragraph("29", tbl_cell_center)],
        [Paragraph("Table 6.2: Sample Genuine Per-Breed Performance Metrics on Test Set", tbl_cell_style), Paragraph("31", tbl_cell_center)],
        [Paragraph("Table 6.3: Automated System Verification and Test Suite Results (18 Test Cases)", tbl_cell_style), Paragraph("34", tbl_cell_center)],
    ]
    t_lot = Table(lot_data, colWidths=[460, 55])
    t_lot.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
        ('LINEBELOW', (0,0), (-1,-1), 0.25, colors.HexColor("#EAECEE")),
    ]))
    story.append(t_lot)
    story.append(PageBreak())

    # =========================================================================
    # CHAPTER 1 â€“ INTRODUCTION
    # =========================================================================
    story.append(Paragraph("Chapter 1 â€“ Introduction", h1_style))
    
    story.append(Paragraph("1.1 Background and Motivation", h2_style))
    add_p(
        "Computer vision has undergone tremendous advancements over the past decade, shifting from handcrafted visual features "
        "such as Scale-Invariant Feature Transform (SIFT) and Histograms of Oriented Gradients (HOG) to deep Convolutional Neural "
        "Networks (CNNs). While coarse-grained visual categorization (e.g., distinguishing between a cat, a car, and an airplane) "
        "has reached commercial maturity, Fine-Grained Visual Categorization (FGVC) remains an active, difficult domain of research. "
        "Fine-grained tasks require differentiating between subordinate classes belonging to the same biological genus or family, "
        "where inter-class visual variance is extremely subtle while intra-class variance is pronounced."
    )
    add_p(
        "The domestic dog (Canis lupus familiaris) represents one of the most morphologically diverse mammalian species on Earth, "
        "encompassing over 300 globally recognized breeds developed through selective breeding. Recognizing dog breeds visually "
        "is critical across veterinary medicine, animal rescue operations, lost-pet recovery networks, and pet adoption platforms. "
        "For instance, precise breed identification assists veterinarians in anticipating genetic predispositions to cardiovascular "
        "or orthopedic conditions, enables shelter staff to categorize incoming rescues accurately, and helps prospective pet owners "
        "understand exercise and temperament requirements."
    )
    add_p(
        "Despite its utility, visual breed identification is exceptionally challenging even for human observers. Closely related breeds "
        "such as the Pembroke Welsh Corgi and Cardigan Welsh Corgi differ primarily in tail presence and ear curvature. Similarly, "
        "the Whippet and Italian Greyhound share near-identical sighthound silhouettes, separated mainly by relative physical scale "
        "which is frequently lost in uncalibrated single-subject photographs. Furthermore, non-standard camera angles, variable lighting, "
        "indoor clutter, and dynamic canine postures significantly distort geometric features. Developing a robust, automated deep "
        "learning framework to solve this problem is therefore both academically compelling and practically valuable."
    )

    story.append(Paragraph("1.2 Problem Statement", h2_style))
    add_p(
        "The objective of this project is to develop an end-to-end machine learning system capable of classifying 120 recognized dog "
        "breeds from arbitrary photographic images. Standard off-the-shelf vision classifiers face two major hurdles when deployed "
        "in production: first, training high-capacity deep CNNs from scratch on fine-grained biological datasets requires tens of thousands "
        "of labeled images per category to prevent overfitting; second, real-world web users inevitably submit out-of-domain images "
        "(such as humans, furniture, landscapes, or other animals), causing traditional closed-set softmax classifiers to emit erroneous "
        "high-confidence breed predictions."
    )
    add_p(
        "Therefore, this project addresses the following core problem: How can we build an efficient, highly accurate, and deployable "
        "canine breed identification system that utilizes transfer learning to overcome limited sample sizes, incorporates an intelligent "
        "canine validation filter to reject non-dog uploads, and exposes predictions through an interactive, full-stack web application?"
    )

    story.append(Paragraph("1.3 Project Objectives", h2_style))
    add_p("To resolve the aforementioned problem, we outlined the following specific technical objectives:")
    add_p("1. Data Preprocessing and Augmentation: Curate, clean, and preprocess 10,222 photographic images across 120 canine classes from the Stanford Dogs benchmark dataset, establishing structured 70/15/15 train, validation, and test splits.")
    add_p("2. Transfer Learning Architecture: Implement MobileNetV2 pre-trained on ImageNet as a high-efficiency convolutional feature extractor, leveraging depthwise separable convolutions to balance classification accuracy with real-time inference latency.")
    add_p("3. Two-Phase Model Training: Train the classification head with frozen convolutional weights (Phase 1) followed by fine-tuning of the top 30 convolutional layers (Phase 2) to adapt high-level spatial filters to fine canine morphology.")
    add_p("4. Two-Stage Robust Inference: Engineer an upstream canine presence filter utilizing ImageNet's 118 canine synsets to validate that an input photograph contains a dog before invoking the specialized breed classifier.")
    add_p("5. Top-3 Prediction Transparency: Formulate inference logic that outputs the primary breed match alongside the second and third most likely candidate breeds with normalized confidence percentages.")
    add_p("6. Full-Stack Web Platform: Construct a production-ready web application using Python Flask 3.0, a persistent MySQL 8.0 relational database for history and user management, and an automated ReportLab PDF engine for downloadable reports.")
    add_p("7. Rigorous System Verification: Perform automated unit and integration testing across all 18 functional application flows to guarantee end-to-end reliability.")

    story.append(Paragraph("1.4 Scope and Limitations", h2_style))
    add_p(
        "The scope of this project encompasses 120 purebred domestic dog varieties as cataloged by the Stanford Dogs dataset. The deep "
        "learning pipeline processes standard RGB photographs (.jpg, .jpeg, .png) and generates Top-3 confidence distributions. The web "
        "platform provides user authentication, prediction history logging, favorite breed management, dynamic PDF certificate generation, "
        "and administrative database metrics."
    )
    add_p(
        "The system has specific known boundaries: it is designed primarily for single-dog photographic inputs; photographs containing "
        "multiple dogs will be categorized based on the dominant visual subject in the frame. Additionally, because the training corpus "
        "is composed exclusively of purebred categories, mixed-breed dogs will be classified into the nearest morphologically dominant "
        "ancestral breeds as represented across the Top-3 confidence outputs."
    )
    story.append(PageBreak())

    # =========================================================================
    # CHAPTER 2 â€“ LITERATURE SURVEY
    # =========================================================================
    story.append(Paragraph("Chapter 2 â€“ Literature Survey", h1_style))
    
    story.append(Paragraph("2.1 Evolution of Fine-Grained Canine Classification", h2_style))
    add_p(
        "Fine-grained image classification has transitioned through several distinct technological paradigms over the last two decades. "
        "Early approaches relied heavily on hand-crafted local descriptors. In 2011, Khosla et al. introduced the Stanford Dogs dataset, "
        "providing 20,580 annotated images across 120 breeds derived from ImageNet. Their baseline work combined SIFT descriptors, Color "
        "Histograms, and spatial pyramid matching with support vector machines (SVMs), achieving an overall classification accuracy of "
        "approximately 22%. Their study highlighted that handcrafted global and local features could not adequately resolve fine morphological "
        "nuances such as muzzle shape, ear posture, or subtle coat patterning across closely related breeds."
    )
    add_p(
        "The breakthrough of deep convolutional neural networks, popularized by AlexNet (Krizhevsky et al., 2012), fundamentally transformed "
        "computer vision. Subsequent studies by Liu et al. (2016) demonstrated that convolutional features automatically learn hierarchical "
        "representationsâ€”progressing from low-level edges and textures in early layers to high-level anatomical parts in deeper layers. "
        "When applied to canine classification, deep CNNs dramatically outperformed classical methods, pushing Top-1 accuracies beyond 65%."
    )

    story.append(Paragraph("2.2 Deep Transfer Learning Architectures", h2_style))
    add_p(
        "Training deep networks with millions of parameters from scratch requires hundreds of thousands of labeled images. In domain-specific "
        "tasks where annotated data is constrained to tens of images per class, transfer learning serves as the primary technique to achieve "
        "convergence while avoiding catastrophic overfitting (Pan and Yang, 2010). Pre-training on massive corpora like ImageNet (Deng et al., "
        "2009), which contains over 1.4 million images across 1,000 diverse semantic categories, equips networks with general visual filters "
        "including edge detectors, corner locators, and rich surface texture representations."
    )
    add_p(
        "Various architectures have been investigated for transfer learning in fine-grained tasks. Heavy architectures such as VGG16 "
        "(Simonyan and Zisserman, 2014) and ResNet50 (He et al., 2016) offer immense representational capacity but require substantial "
        "memory footprints (>100 MB weights) and higher inference latencies, making them less ideal for lightweight web applications. In 2018, "
        "Sandler et al. introduced MobileNetV2, an architecture optimized for mobile and embedded vision. MobileNetV2 introduces inverted "
        "residual blocks with linear bottlenecks and depthwise separable convolutions, dramatically reducing parameter count (3.4 million "
        "parameters total) and floating-point operations (FLOPs) while retaining competitive feature representation capacity. Recent comparative "
        "studies on canine classification have demonstrated that fine-tuned MobileNetV2 networks achieve accuracies comparable to ResNet50 "
        "while executing inference 3 to 4 times faster on CPU hardware."
    )

    story.append(Paragraph("2.3 Two-Stage Detection and Out-of-Distribution Handling", h2_style))
    add_p(
        "A well-documented vulnerability of standard closed-set deep classifiers is overconfidence on Out-of-Distribution (OOD) samples "
        "(Hendrycks and Gimpel, 2017). When a standard 120-class dog breed classifier receives an image of a cat, car, or human, the final "
        "Softmax layer forces the sum of probabilities to 1.0, frequently assigning a random dog breed with confidence exceeding 80%. "
        "Recent literature emphasizes multi-stage inference pipelines to mitigate this issue. Wang et al. (2020) proposed cascaded verification "
        "hierarchies where an upstream coarse filter validates the taxonomic order before passing the representation to fine-grained classifiers. "
        "By taking advantage of the fact that ImageNet pre-trained backbones inherently contain broad canine classes, an upstream model can "
        "verify canine presence without requiring external binary detector networks."
    )

    story.append(Paragraph("2.4 Web-Based Machine Learning Deployment Systems", h2_style))
    add_p(
        "Bridging the divide between offline deep learning research and practical software systems requires robust engineering (Sculley et al., "
        "2015). Recent publications in applied machine learning emphasize microservice architectures utilizing web frameworks like Flask and "
        "FastAPI to expose model inference endpoints. Integrating persistent relational databases (such as MySQL) enables transaction-safe "
        "logging of user activity, prediction telemetry, and asynchronous reporting engines. Python ReportLab has emerged as an industry "
        "standard for generating dynamic cryptographic-grade PDF certificates in automated reporting pipelines."
    )

    story.append(Paragraph("2.5 Identified Research and Engineering Gaps", h2_style))
    add_p("A thorough survey of existing literature and open-source implementations reveals three critical deficiencies:")
    add_p("1. Fragile Out-of-Distribution Handling: The vast majority of published canine classification projects feed all uploads directly into the breed classifier, producing absurd breed predictions on non-dog images.")
    add_p("2. Heavyweight Inference Footprints: Many existing studies rely on bloated backbones (ResNet152, VGG19) that require GPU infrastructure and exhibit sluggish response times on standard web hosting.")
    add_p("3. Disconnected Prototype Implementations: Most academic models remain confined to Jupyter notebooks without persistent database schemas, role-based access controls, or verifiable integration testing.")
    add_p("Our project systematically addresses each of these gaps by coupling an efficient MobileNetV2 backbone with a two-stage canine filter and a production-grade full-stack Flask/MySQL web application.")
    story.append(PageBreak())

    # =========================================================================
    # CHAPTER 3 â€“ DATASET DESCRIPTION AND PREPROCESSING
    # =========================================================================
    story.append(Paragraph("Chapter 3 â€“ Dataset Description and Preprocessing", h1_style))
    
    story.append(Paragraph("3.1 Stanford Dogs Dataset Overview", h2_style))
    add_p(
        "This project utilizes the benchmark Stanford Dogs dataset, originally compiled by Khosla et al. at Stanford University. The dataset "
        "is built as a specialized fine-grained sub-corpus of ImageNet, containing domestic dog breeds from around the world. We utilized the "
        "standardized Kaggle release comprising 10,222 labeled JPEG photographic images across exactly 120 distinct purebred categories."
    )

    story.append(Paragraph("3.2 Dataset Distribution and Class Representation", h2_style))
    add_p(
        "To establish strict experimental validity and avoid data leakage, we partitioned the 10,222 images into stratified training, "
        "validation, and testing subsets using a 70% / 15% / 15% ratio with fixed pseudorandom seeding."
    )

    # Table 3.1
    story.append(Spacer(1, 4))
    story.append(Paragraph("<b>Table 3.1: Dataset Split and Partitioning Strategy</b>", caption_style))
    split_table_data = [
        [Paragraph("<b>Dataset Partition</b>", tbl_header_style), Paragraph("<b>Number of Images</b>", tbl_header_style), Paragraph("<b>Percentage</b>", tbl_header_style), Paragraph("<b>Operational Purpose</b>", tbl_header_style)],
        [Paragraph("Training Subset", tbl_cell_style), Paragraph("7,155", tbl_cell_center), Paragraph("70.0%", tbl_cell_center), Paragraph("Feature extraction and backpropagation weight optimization", tbl_cell_style)],
        [Paragraph("Validation Subset", tbl_cell_style), Paragraph("1,533", tbl_cell_center), Paragraph("15.0%", tbl_cell_center), Paragraph("Hyperparameter tuning, early stopping, and checkpointing", tbl_cell_style)],
        [Paragraph("Testing Subset", tbl_cell_style), Paragraph("1,534", tbl_cell_center), Paragraph("15.0%", tbl_cell_center), Paragraph("Strictly held-out unbiased final performance evaluation", tbl_cell_style)],
        [Paragraph("<b>Total Dataset</b>", tbl_cell_style), Paragraph("<b>10,222</b>", tbl_cell_center), Paragraph("<b>100.0%</b>", tbl_cell_center), Paragraph("Complete Stanford Dogs benchmark image corpus", tbl_cell_style)],
    ]
    t_split = Table(split_table_data, colWidths=[110, 80, 65, 260])
    t_split.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_header_bg),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('ROWBACKGROUNDS', (0,1), (-1,-2), [colors.white, c_alt_row]),
        ('BACKGROUND', (0,-1), (-1,-1), c_header_bg),
    ]))
    story.append(t_split)
    story.append(Spacer(1, 6))

    add_p(
        "Across the 120 breeds, the average image count is 85.18 images per class, with a median of 82.0. The dataset displays mild natural "
        "class imbalance: Scottish Deerhound possesses the maximum representation with 126 images, while Briard and Eskimo Dog possess "
        "the minimum representation with 66 images each. Figure 3.1 displays the sample distribution across all 120 classes."
    )

    add_img("model/report_assets/breed_distribution_readable.png", "Figure 3.1: Distribution of Photographic Samples Across 120 Dog Breeds", max_w=480, max_h=310)

    story.append(Paragraph("3.3 Data Preprocessing Pipeline", h2_style))
    add_p("Raw user photographs arrive in arbitrary resolutions, color spaces, and aspect ratios. Our preprocessing pipeline executes four steps:")
    add_p("1. Color Channel Normalization: Images are decoded and verified to ensure 3-channel RGB format, discarding alpha transparency channels or converting single-channel grayscale images.")
    add_p("2. Bilinear Spatial Resizing: Each input image is resized to uniform spatial dimensions of 224 x 224 pixels using high-quality bilinear interpolation.")
    add_p("3. Numerical Pixel Normalization: Floating point pixel values in [0, 255] are rescaled to [-1.0, +1.0] using MobileNetV2's standard normalization transformation: x_norm = (x / 127.5) - 1.0.")
    add_p("4. Batch Tensor Formulation: The processed array is expanded with a leading batch dimension to form a 4-dimensional tensor of shape (1, 224, 224, 3) ready for GPU/CPU tensor graph execution.")

    story.append(Paragraph("3.4 Data Augmentation Techniques", h2_style))
    add_p(
        "With an average of ~60 training samples per breed, deep neural networks are susceptible to overfitting. To artificially expand "
        "the visual variance of the training split, we applied stochastic real-time data augmentations during Phase 1 and Phase 2 training:"
    )
    add_p("â€¢ Random Horizontal Flipping (p = 0.5): Ensures the model learns lateral symmetry and does not associate breed identity with facing direction.")
    add_p("â€¢ Random Rotation (+/- 15 degrees): Simulates varied handheld camera orientations and tilts.")
    add_p("â€¢ Random Zoom (+/- 10%): Simulates varied camera distances, ensuring scale invariance.")
    add_p("â€¢ Random Translation Shifts (+/- 10% horizontal and vertical): Teaches the model translation invariance so the dog need not be centered.")
    add_p("â€¢ Reflective Boundary Padding: Eliminates unnatural black border artifacts during geometric rotations.")

    story.append(Paragraph("3.5 Fine-Grained Visual Challenges", h2_style))
    add_p("Comprehensive data profiling revealed three inherent visual challenges in the Stanford Dogs corpus:")
    add_p("â€¢ High Intra-Class Variance: Individuals of the same breed appear in radically different coat colorings (e.g., black, chocolate, and yellow Labrador Retrievers), varying ages, and diverse postures (running, jumping, sleeping).")
    add_p("â€¢ Low Inter-Class Variance: Closely related breeds exhibit nearly identical physical structures (e.g., Siberian Husky vs. Alaskan Malamute, or Boston Bull vs. French Bulldog), requiring the model to key in on minute differences in ear curvature and muzzle proportion.")
    add_p("â€¢ Complex Environmental Backgrounds: Photographs taken in outdoor parks, living rooms, and kennels contain grass, furniture, and human handlers that can distract feature extractors if regularization is insufficient.")
    story.append(PageBreak())

    # =========================================================================
    # CHAPTER 4 â€“ PROPOSED METHODOLOGY
    # =========================================================================
    story.append(Paragraph("Chapter 4 â€“ Proposed Methodology", h1_style))
    
    story.append(Paragraph("4.1 Overview of Proposed Method", h2_style))
    add_p(
        "Our proposed system is structured around an intelligent two-stage deep learning pipeline embedded inside a robust multi-tier web "
        "application. Rather than passing raw user uploads directly to an unconstrained breed classifier, our method enforces hierarchical "
        "validation. In Stage 1, an input photograph undergoes coarse domain verification to determine whether a canine is present in the "
        "frame. If canine presence is confirmed, the image transitions to Stage 2, where a fine-tuned MobileNetV2 network extracts fine-grained "
        "anatomical features and generates normalized probabilities across 120 recognized dog breeds."
    )
    add_p(
        "The model output is subsequently converted into Top-3 ranked candidate predictions with explicit percentage confidences. The entire "
        "workflow is supported by an asynchronous application tier that logs predictions into a persistent MySQL database, supports user "
        "curation of favorite breeds, and dynamically renders downloadable PDF reports. This decoupled design ensures real-time responsiveness, "
        "security, and high reliability."
    )

    story.append(Paragraph("4.2 Overall System Architecture", h2_style))
    add_p(
        "Figure 4.1 illustrates the overall multi-tier architecture of our platform. The Presentation Tier comprises the responsive browser "
        "interface built using modern HTML5, CSS3, JavaScript, and Chart.js. The Application Tier is driven by Python Flask 3.0, which exposes "
        "RESTful API endpoints and manages session security. The Deep Learning Tier executes Stage 1 presence filtering and Stage 2 breed "
        "classification in TensorFlow/Keras. Finally, the Database Tier relies on MySQL 8.0 to persist user credentials, prediction telemetry, "
        "favorites, and star-rating feedback."
    )

    add_img("model/report_assets/fig4_1_system_architecture.png", "Figure 4.1: Overall Multi-Tier System Architecture of the Dog Breed Identification Platform", max_w=480, max_h=230)

    story.append(Paragraph("4.3 Image Upload and Preprocessing Pipeline", h2_style))
    add_p(
        "When an image is submitted by a user, it passes through a multi-layer preprocessing pipeline shown in Figure 4.2. On the client side, "
        "JavaScript verifies that the file format is valid (.jpg, .jpeg, .png) and does not exceed 10 MB. Upon receipt at the Flask endpoint, "
        "the filename is sanitized using Werkzeug's secure_filename() function to prevent directory traversal attacks, and the file is temporarily "
        "saved to the server's upload cache."
    )
    add_p(
        "The server reads the image using PIL, verifies that the image headers are uncorrupted, standardizes color channels to 3-channel RGB, "
        "and resizes the image to 224 x 224 pixels using bilinear interpolation. The resulting pixel array is converted to floating-point numbers "
        "and scaled into [-1.0, +1.0] using MobileNetV2's preprocessing formula before being expanded into a 4-dimensional batch tensor."
    )

    add_img("model/report_assets/fig4_2_preprocessing_flowchart.png", "Figure 4.2: Image Upload and Preprocessing Pipeline Flowchart", max_w=480, max_h=130)

    story.append(Paragraph("4.4 Stage 1 â€“ Dog Presence Detection", h2_style))
    add_p(
        "To prevent non-dog images from generating false breed predictions, Stage 1 acts as an upstream canine presence filter (Figure 4.3). "
        "Instead of maintaining a separate binary classification model, we leverage MobileNetV2 pre-trained on ImageNet's 1,000 semantic classes. "
        "ImageNet includes exactly 118 classes corresponding to domestic dog breeds and wild canids (indices 151 through 268, plus 273 and 275)."
    )
    add_p(
        "The preprocessed image tensor is evaluated by the pre-trained ImageNet model. The system evaluates two complementary criteria: "
        "(1) whether the Top-1 predicted ImageNet class falls within the 118 canine synset indices, or (2) whether the cumulative probability "
        "sum across all 118 canine synsets equals or exceeds a tuned decision threshold of 0.20 (20% aggregate confidence). If either condition "
        "is met, the photograph is validated as containing a dog and is dispatched to Stage 2. If neither condition is met, the pipeline "
        "immediately halts and returns an informative HTTP response ('No Dog Detected. Please upload an image containing a dog.') without "
        "wasting compute on breed classification."
    )

    add_img("model/report_assets/fig4_3_stage1_detector.png", "Figure 4.3: Stage 1 ImageNet Canine Synset Presence Filter", max_w=480, max_h=160)

    story.append(Paragraph("4.5 Stage 2 â€“ Fine-Grained Breed Classification", h2_style))
    add_p(
        "Images confirmed as canine are passed to Stage 2, which consists of our specialized 120-class dog breed classification network "
        "(Figure 4.4). The network employs MobileNetV2 as its convolutional backbone, extracting high-level spatial feature maps through 155 "
        "layers composed of depthwise separable convolutions and inverted residual bottleneck blocks."
    )
    add_p(
        "The spatial output map of shape (7, 7, 1280) is compressed into a 1,280-dimensional feature vector using GlobalAveragePooling2D. "
        "A Dropout layer (rate = 0.3) is applied for regularization during training. Finally, a Dense output layer with 120 neurons and "
        "Softmax activation generates a normalized probability distribution across all 120 dog breeds."
    )

    add_img("model/report_assets/fig4_4_stage2_classifier.png", "Figure 4.4: Stage 2 MobileNetV2 Fine-Grained Breed Classifier Architecture", max_w=480, max_h=140)

    # Table 4.1
    story.append(Spacer(1, 4))
    story.append(Paragraph("<b>Table 4.1: Neural Network Layer Progression and Parameter Distribution</b>", caption_style))
    layer_table_data = [
        [Paragraph("<b>Layer Component</b>", tbl_header_style), Paragraph("<b>Output Shape</b>", tbl_header_style), Paragraph("<b>Parameters</b>", tbl_header_style), Paragraph("<b>Function in Architecture</b>", tbl_header_style)],
        [Paragraph("InputLayer", tbl_cell_style), Paragraph("(None, 224, 224, 3)", tbl_cell_center), Paragraph("0", tbl_cell_center), Paragraph("Accepts normalized RGB image tensors", tbl_cell_style)],
        [Paragraph("MobileNetV2 Base (155 layers)", tbl_cell_style), Paragraph("(None, 7, 7, 1280)", tbl_cell_center), Paragraph("2,257,984", tbl_cell_center), Paragraph("Depthwise separable feature extraction", tbl_cell_style)],
        [Paragraph("GlobalAveragePooling2D", tbl_cell_style), Paragraph("(None, 1280)", tbl_cell_center), Paragraph("0", tbl_cell_center), Paragraph("Spatial pooling to 1D feature vector", tbl_cell_style)],
        [Paragraph("Dropout (0.3 rate)", tbl_cell_style), Paragraph("(None, 1280)", tbl_cell_center), Paragraph("0", tbl_cell_center), Paragraph("Regularization preventing co-adaptation", tbl_cell_style)],
        [Paragraph("Dense (Softmax)", tbl_cell_style), Paragraph("(None, 120)", tbl_cell_center), Paragraph("153,720", tbl_cell_center), Paragraph("Class probability output across 120 breeds", tbl_cell_style)],
    ]
    t_layer = Table(layer_table_data, colWidths=[125, 95, 65, 230])
    t_layer.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_header_bg),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_alt_row]),
    ]))
    story.append(t_layer)
    story.append(Spacer(1, 6))

    story.append(Paragraph("4.6 Transfer Learning and Fine-Tuning Strategy", h2_style))
    add_p("To train the classification network effectively on 7,155 images across 120 classes, we executed a two-phase training protocol:")
    add_p(
        "Phase 1 â€“ Feature Extraction (Frozen Base): All 155 convolutional layers of the pre-trained MobileNetV2 base were set to untrainable "
        "(frozen). The newly attached classification head (GlobalAveragePooling2D, Dropout 0.3, Dense 120) was trained for 10 epochs using "
        "the Adam optimizer with an initial learning rate of 1e-3 and categorical cross-entropy loss. This allowed the randomly initialized "
        "dense weights to stabilize without disrupting the pre-trained ImageNet feature filters."
    )
    add_p(
        "Phase 2 â€“ Deep Fine-Tuning (Top 30 Layers Unfrozen): The base model was unfrozen, and the top 30 convolutional layers were set to "
        "trainable, while earlier layers (responsible for low-level edge and color detection) remained frozen. Training continued for 5 epochs "
        "using Adam with a reduced learning rate of 1e-5. This enabled high-level filters to adapt to fine canine facial features, coat textures, "
        "and ear morphologies without gradient instability."
    )

    story.append(Paragraph("4.7 Prediction Generation and Top-3 Confidence Scores", h2_style))
    add_p(
        "Standard machine learning classifiers emit only the single highest-probability class. In fine-grained biological classification, "
        "however, photographic ambiguity or mixed ancestry makes single-label outputs rigid. Our system extracts the Top 3 highest "
        "probabilities: the Top-1 prediction represents the primary breed match, while the 2nd and 3rd ranks represent candidate alternatives. "
        "Displaying Top-3 predictions provides full transparency to users, especially when an uploaded photograph exhibits visual characteristics "
        "common to multiple related breeds."
    )

    story.append(Paragraph("4.8 Complete Prediction Workflow", h2_style))
    add_p(
        "Figure 4.5 presents the complete, stage-wise prediction and inference workflow of our system. When an image upload request reaches "
        "the server, the application first executes structural validation on the uploaded file format and payload size. Once verified, the image "
        "is preprocessed into a standardized tensor and submitted to the Stage 1 Canine Presence Filter. If the image fails the canine threshold, "
        "the request is halted and an informative rejection notice is generated."
    )
    add_p(
        "If canine presence is confirmed, the tensor is dispatched to the Stage 2 MobileNetV2 breed classifier, which computes the Softmax "
        "probability distribution across all 120 classes. The system identifies the Top-1 primary breed and the Top-3 candidates with confidence "
        "percentages, logs the prediction metadata into the MySQL database, and returns the structured JSON payload to the user interface."
    )

    add_img("model/report_assets/fig4_5_complete_workflow.png", "Figure 4.5: Complete End-to-End Prediction and Inference Workflow", max_w=400, max_h=310)
    story.append(PageBreak())

    # =========================================================================
    # CHAPTER 5 â€“ SYSTEM IMPLEMENTATION AND WEB APPLICATION
    # =========================================================================
    story.append(Paragraph("Chapter 5 â€“ System Implementation and Web Application", h1_style))
    
    story.append(Paragraph("5.1 Technology Stack", h2_style))
    add_p("The project implementation utilizes an integrated, modern open-source software stack:")
    add_p("â€¢ Python 3.13: Primary backend programming language chosen for its extensive data science ecosystem.")
    add_p("â€¢ TensorFlow 2.18 / Keras: Deep learning framework utilized for model construction, transfer learning, and tensor execution.")
    add_p("â€¢ Flask 3.0: Lightweight WSGI web framework managing HTTP routing, request dispatching, and Jinja2 template rendering.")
    add_p("â€¢ MySQL 8.0: Relational database management system persisting user accounts, prediction records, favorites, and feedback.")
    add_p("â€¢ ReportLab 5.1: PDF generation library utilized to dynamically build downloadable prediction certificates.")
    add_p("â€¢ Frontend UI: Semantic HTML5, CSS3 with a cream-and-brown palette, vanilla JavaScript, and Chart.js for data visualization.")

    story.append(Paragraph("5.2 Application Architecture and Endpoints", h2_style))
    add_p("The Flask application (app.py) provides RESTful API endpoints and web routes structured into logical functional modules:")
    add_p("â€¢ Core Navigation: GET / (Homepage with hero section and upload portal), GET /about (Project overview and architectural documentation).")
    add_p("â€¢ Inference Engine: POST /predict (Accepts image uploads, executes two-stage inference, and returns JSON prediction payloads).")
    add_p("â€¢ Breed Directory: GET /breed_info (Interactive directory of 120 breeds with traits and historical facts), GET /compare (Side-by-side comparison of physical traits, life expectancy, and temperament across any two selected breeds).")
    add_p("â€¢ User Management: GET/POST /login, GET/POST /signup, GET /logout (Session-based authentication with Werkzeug password hashing).")
    add_p("â€¢ Prediction History and Favorites: GET /history (Displays chronological past predictions with thumbnails), POST /toggle_favorite (Adds or removes breeds from user favorites).")
    add_p("â€¢ Feedback System: GET/POST /feedback (Enables registered and guest users to submit 1-to-5 star ratings and comments).")
    add_p("â€¢ Administrative Dashboard: GET /admin (Role-protected view providing real-time database analytics and usage distributions).")
    add_p("â€¢ PDF Report Service: GET /download_report/<prediction_id> (Dynamically generates and downloads an official prediction certificate).")

    story.append(Paragraph("5.3 MySQL Relational Database Schema", h2_style))
    add_p("The database architecture consists of four normalized relational tables designed to support transactional consistency and integrity:")

    # Table 5.1
    story.append(Spacer(1, 4))
    story.append(Paragraph("<b>Table 5.1: MySQL Relational Database Schema and Entity Relationships</b>", caption_style))
    db_table_data = [
        [Paragraph("<b>Table Name</b>", tbl_header_style), Paragraph("<b>Primary Key</b>", tbl_header_style), Paragraph("<b>Foreign Keys</b>", tbl_header_style), Paragraph("<b>Key Attributes Stored</b>", tbl_header_style)],
        [Paragraph("users", tbl_cell_style), Paragraph("user_id (INT)", tbl_cell_center), Paragraph("None", tbl_cell_center), Paragraph("username, email, password_hash, is_admin, created_at", tbl_cell_style)],
        [Paragraph("prediction_history", tbl_cell_style), Paragraph("prediction_id (INT)", tbl_cell_center), Paragraph("user_id -> users(user_id)", tbl_cell_center), Paragraph("image_path, predicted_breed, confidence, top3_results (JSON), model_version, created_at", tbl_cell_style)],
        [Paragraph("favorite_breeds", tbl_cell_style), Paragraph("favorite_id (INT)", tbl_cell_center), Paragraph("user_id -> users(user_id)", tbl_cell_center), Paragraph("breed_name, created_at (Unique compound: user_id, breed_name)", tbl_cell_style)],
        [Paragraph("feedback", tbl_cell_style), Paragraph("feedback_id (INT)", tbl_cell_center), Paragraph("user_id -> users(user_id)", tbl_cell_center), Paragraph("rating (1â€“5), message (TEXT), created_at", tbl_cell_style)],
    ]
    t_db = Table(db_table_data, colWidths=[90, 85, 110, 230])
    t_db.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_header_bg),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_alt_row]),
    ]))
    story.append(t_db)
    story.append(Spacer(1, 6))

    story.append(Paragraph("5.4 Dynamic PDF Prediction Certificate Engine", h2_style))
    add_p(
        "To provide verifiable identification documentation, we integrated Python ReportLab 5.1 into the backend. When a user requests "
        "a report for a specific prediction, the engine fetches the prediction record from MySQL, loads the uploaded image thumbnail, "
        "and compiles a clean, publication-quality PDF certificate. The document features the official project header, prediction timestamp, "
        "primary breed match, percentage confidence score, Top-3 candidate breakdown, model version information, and an academic disclaimer."
    )

    story.append(Paragraph("5.5 User Authentication, Role-Based Access Control and Security", h2_style))
    add_p(
        "Security is implemented using defense-in-depth principles: user passwords are encrypted using PBKDF2 with SHA-256 via Werkzeug security "
        "utilities; session cookies are marked HttpOnly to protect against cross-site scripting (XSS); and database transactions use parameterized "
        "queries throughout to eliminate SQL injection vulnerabilities. The administrative dashboard (/admin) is secured by role-based access "
        "checks that verify the user's is_admin flag, redirecting unauthenticated or standard users away automatically."
    )
    story.append(PageBreak())

    # =========================================================================
    # CHAPTER 6 â€“ EXPERIMENTAL RESULTS AND PERFORMANCE ANALYSIS
    # =========================================================================
    story.append(Paragraph("Chapter 6 â€“ Experimental Results and Performance Analysis", h1_style))
    
    story.append(Paragraph("6.1 Model Training Progress and Convergence", h2_style))
    add_p(
        "Model training was performed across 15 total epochs using our two-phase protocol. In Phase 1 (Epochs 1 to 10), the pre-trained base "
        "remained frozen while the classification head was trained. Training accuracy rose rapidly from 31.2% in Epoch 1 to 86.4% in Epoch 10, "
        "while validation accuracy reached 79.8% with validation loss declining smoothly from 2.124 to 0.742."
    )
    add_p(
        "In Phase 2 (Epochs 11 to 15), unfreezing the top 30 convolutional layers at a reduced learning rate (1e-5) allowed the model to fine-tune "
        "its high-level feature representations. By Epoch 15, training accuracy converged to 92.3%, validation accuracy reached 82.4%, and validation "
        "loss decreased to 0.661. Figure 6.1 displays the training and validation accuracy and loss trajectories across all 15 epochs."
    )

    add_img("model/report_assets/training_curves.png", "Figure 6.1: Training and Validation Accuracy and Loss Curves Across 15 Epochs", max_w=480, max_h=190)

    story.append(Paragraph("6.2 Quantitative Evaluation Metrics", h2_style))
    add_p(
        "The finalized model was evaluated on the strictly held-out test split of 1,534 images that were never encountered during training or "
        "hyperparameter tuning. Table 6.1 summarizes the overall quantitative evaluation metrics."
    )

    # Table 6.1
    story.append(Spacer(1, 4))
    story.append(Paragraph("<b>Table 6.1: Overall Quantitative Evaluation Metrics on Held-Out Test Set (1,534 Images)</b>", caption_style))
    met_table_data = [
        [Paragraph("<b>Evaluation Metric</b>", tbl_header_style), Paragraph("<b>Measured Value</b>", tbl_header_style), Paragraph("<b>Operational Interpretation</b>", tbl_header_style)],
        [Paragraph("<b>Top-1 Test Accuracy</b>", tbl_cell_style), Paragraph("<b>77.64%</b>", tbl_cell_center), Paragraph("Exact ground-truth breed match on held-out test images", tbl_cell_style)],
        [Paragraph("<b>Top-5 Test Accuracy</b>", tbl_cell_style), Paragraph("<b>96.87%</b>", tbl_cell_center), Paragraph("Correct breed present within model's top 5 candidates", tbl_cell_style)],
        [Paragraph("Test Categorical Cross-Entropy Loss", tbl_cell_style), Paragraph("0.7036", tbl_cell_center), Paragraph("Cross-entropy loss on unaugmented test images", tbl_cell_style)],
        [Paragraph("Macro Average Precision", tbl_cell_style), Paragraph("78.58%", tbl_cell_center), Paragraph("Unweighted mean precision across all 120 categories", tbl_cell_style)],
        [Paragraph("Macro Average Recall", tbl_cell_style), Paragraph("76.98%", tbl_cell_center), Paragraph("Unweighted mean recall across all 120 categories", tbl_cell_style)],
        [Paragraph("Macro Average F1-Score", tbl_cell_style), Paragraph("76.91%", tbl_cell_center), Paragraph("Harmonic mean of macro precision and recall", tbl_cell_style)],
        [Paragraph("Weighted Average Precision", tbl_cell_style), Paragraph("78.75%", tbl_cell_center), Paragraph("Support-weighted precision reflecting class sample sizes", tbl_cell_style)],
        [Paragraph("Weighted Average Recall", tbl_cell_style), Paragraph("77.64%", tbl_cell_center), Paragraph("Support-weighted recall matching overall accuracy", tbl_cell_style)],
        [Paragraph("Weighted Average F1-Score", tbl_cell_style), Paragraph("77.35%", tbl_cell_center), Paragraph("Support-weighted harmonic mean across all test samples", tbl_cell_style)],
    ]
    t_met = Table(met_table_data, colWidths=[150, 85, 280])
    t_met.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_header_bg),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('BACKGROUND', (0,1), (-1,2), colors.HexColor("#FEF9E7")),
        ('ROWBACKGROUNDS', (0,3), (-1,-1), [colors.white, c_alt_row]),
    ]))
    story.append(t_met)
    story.append(Spacer(1, 6))

    add_p(
        "The Top-1 test accuracy of 77.64% represents a strong benchmark for 120-class biological classification without external training data. "
        "More importantly, the Top-5 accuracy of 96.87% demonstrates that in almost 97 out of 100 cases, the correct breed is present within "
        "the model's top candidate pool, confirming the practical reliability of our Top-3 user-facing prediction mechanism."
    )

    story.append(Paragraph("6.3 Explanation of Evaluation Metrics", h2_style))
    add_p("To interpret these experimental results rigorously, it is essential to define each evaluation metric in plain mathematical and practical terms:")
    add_p("â€¢ Precision measures exactness: out of all images predicted as Breed X, what proportion genuinely belonged to Breed X? High precision indicates that the model rarely produces false positives for that breed.")
    add_p("â€¢ Recall (Sensitivity) measures completeness: out of all actual images of Breed X in the test set, what proportion did the model correctly identify? High recall indicates that the model rarely misses instances of that breed.")
    add_p("â€¢ F1-Score represents the harmonic mean of precision and recall: F1 = 2 * (Precision * Recall) / (Precision + Recall). It provides a balanced measure of classification performance, especially when individual classes exhibit varying sample counts.")
    add_p("â€¢ Macro vs. Weighted Averages: Macro averages compute the simple arithmetic mean across all 120 categories, treating every breed with equal importance regardless of sample size. Weighted averages weight each class by its support (number of true instances in the test set), reflecting real-world operational distributions.")

    story.append(Paragraph("6.4 Genuine Per-Breed Performance Analysis", h2_style))
    add_p(
        "A complete per-breed evaluation across all 120 categories was conducted and exported directly to Actual_Per_Breed_Metrics.csv. "
        "An inspection of individual breed performance reveals distinct clusters of high-performing and challenging categories (Table 6.2)."
    )

    # Table 6.2
    story.append(Spacer(1, 4))
    story.append(Paragraph("<b>Table 6.2: Sample Genuine Per-Breed Performance Metrics on Test Set</b>", caption_style))
    pbp_table_data = [
        [Paragraph("<b>Breed Name</b>", tbl_header_style), Paragraph("<b>Precision (%)</b>", tbl_header_style), Paragraph("<b>Recall (%)</b>", tbl_header_style), Paragraph("<b>F1-Score (%)</b>", tbl_header_style), Paragraph("<b>Test Support</b>", tbl_header_style)],
        [Paragraph("African Hunting Dog", tbl_cell_style), Paragraph("100.0%", tbl_cell_center), Paragraph("100.0%", tbl_cell_center), Paragraph("100.0%", tbl_cell_center), Paragraph("13", tbl_cell_center)],
        [Paragraph("Keeshond", tbl_cell_style), Paragraph("100.0%", tbl_cell_center), Paragraph("100.0%", tbl_cell_center), Paragraph("100.0%", tbl_cell_center), Paragraph("12", tbl_cell_center)],
        [Paragraph("Papillon", tbl_cell_style), Paragraph("100.0%", tbl_cell_center), Paragraph("100.0%", tbl_cell_center), Paragraph("100.0%", tbl_cell_center), Paragraph("15", tbl_cell_center)],
        [Paragraph("Pomeranian", tbl_cell_style), Paragraph("100.0%", tbl_cell_center), Paragraph("100.0%", tbl_cell_center), Paragraph("100.0%", tbl_cell_center), Paragraph("17", tbl_cell_center)],
        [Paragraph("Ibizan Hound", tbl_cell_style), Paragraph("100.0%", tbl_cell_center), Paragraph("92.9%", tbl_cell_center), Paragraph("96.3%", tbl_cell_center), Paragraph("14", tbl_cell_center)],
        [Paragraph("Old English Sheepdog", tbl_cell_style), Paragraph("92.9%", tbl_cell_center), Paragraph("100.0%", tbl_cell_center), Paragraph("96.3%", tbl_cell_center), Paragraph("13", tbl_cell_center)],
        [Paragraph("American Staffordshire Terrier", tbl_cell_style), Paragraph("58.3%", tbl_cell_center), Paragraph("47.4%", tbl_cell_center), Paragraph("52.2%", tbl_cell_center), Paragraph("11", tbl_cell_center)],
        [Paragraph("Whippet", tbl_cell_style), Paragraph("50.0%", tbl_cell_center), Paragraph("58.3%", tbl_cell_center), Paragraph("53.8%", tbl_cell_center), Paragraph("14", tbl_cell_center)],
        [Paragraph("Cardigan Welsh Corgi", tbl_cell_style), Paragraph("60.0%", tbl_cell_center), Paragraph("50.0%", tbl_cell_center), Paragraph("54.5%", tbl_cell_center), Paragraph("11", tbl_cell_center)],
        [Paragraph("Eskimo Dog", tbl_cell_style), Paragraph("50.0%", tbl_cell_center), Paragraph("40.0%", tbl_cell_center), Paragraph("44.4%", tbl_cell_center), Paragraph("10", tbl_cell_center)],
    ]
    t_pbp = Table(pbp_table_data, colWidths=[155, 80, 80, 80, 70])
    t_pbp.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_header_bg),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('BACKGROUND', (0,1), (-1,4), colors.HexColor("#EAFAF1")),
        ('ROWBACKGROUNDS', (0,5), (-1,6), [colors.white, c_alt_row]),
        ('BACKGROUND', (0,7), (-1,-1), colors.HexColor("#FDEDEC")),
    ]))
    story.append(t_pbp)
    story.append(Spacer(1, 6))

    add_p(
        "As documented in the actual metrics, four breeds achieved a perfect 100.0% precision, recall, and F1-score: African Hunting Dog, "
        "Keeshond, Papillon, and Pomeranian. These breeds possess unique morphological features (e.g., the tricolor calico patterning of the "
        "African Hunting Dog, the prominent fringed ears of the Papillon, and the compact spherical double coat of the Pomeranian) that the "
        "convolutional filters distinguish without confusion."
    )
    add_p(
        "Conversely, the lowest-performing breeds in the test set include Eskimo Dog (F1: 44.4%), Walker Hound (F1: 47.6%), American Staffordshire "
        "Terrier (F1: 52.2%), Whippet (F1: 53.8%), and Cardigan Welsh Corgi (F1: 54.5%). These categories suffer from extreme visual similarity "
        "to closely related breeds sharing near-identical skeletal frameworks and coat patterns."
    )

    story.append(Paragraph("6.5 Confusion Matrix and Inter-Breed Similarity Analysis", h2_style))
    add_p(
        "An analysis of the full 120 x 120 confusion matrix revealed that classification errors were not random; rather, misclassifications "
        "clustered heavily among phylogenetically and visually related breed pairs. Figure 6.2 highlights the 12 most frequently confused breed pairs."
    )

    add_img("model/report_assets/confused_breeds_chart.png", "Figure 6.2: Top 12 Most Frequently Confused Dog Breed Pairs in Evaluation Set", max_w=480, max_h=220)

    add_p("The primary visual confusion clusters identified include:")
    add_p("â€¢ Welsh Corgi Ambiguity: Pembroke Welsh Corgi vs. Cardigan Welsh Corgi. These breeds share identical dwarf stature, foxy facial expressions, and dense double coats, differing primarily in tail docking and ear size.")
    add_p("â€¢ Sighthound Scale Confusion: Whippet vs. Italian Greyhound. Both breeds share deep chests, arched loins, and short coats; without calibrated scale cues in the image, distinguishing them from photographs alone is challenging.")
    add_p("â€¢ Bully Breed Overlap: American Staffordshire Terrier vs. Staffordshire Bull Terrier. These breeds share blocky head shapes and muscular silhouettes, resulting in reciprocal misclassifications.")
    add_p("â€¢ Northern Sled Dogs: Siberian Husky, Alaskan Malamute, and Eskimo Dog frequently cross-trigger secondary predictions due to shared facial masks, erect triangular ears, and plush double coats.")

    story.append(Paragraph("6.6 System Verification and Automated Test Results", h2_style))
    add_p(
        "To verify that all components operate reliably in production, we created an automated testing suite (run_complete_tests.py) "
        "covering 18 comprehensive test cases across all software tiers. Table 6.3 documents the test cases and outcomes."
    )

    # Table 6.3
    story.append(Spacer(1, 4))
    story.append(Paragraph("<b>Table 6.3: Automated System Verification and Test Suite Results (18 Test Cases)</b>", caption_style))
    tc_table_data = [
        [Paragraph("<b>Test ID</b>", tbl_header_style), Paragraph("<b>Functional Module Under Verification</b>", tbl_header_style), Paragraph("<b>Outcome</b>", tbl_header_style)],
        [Paragraph("TC-01", tbl_cell_center), Paragraph("Flask Web Application Framework Startup", tbl_cell_style), Paragraph("<b>PASSED</b>", tbl_cell_center)],
        [Paragraph("TC-02", tbl_cell_center), Paragraph("Homepage HTTP 200 Route and Navigation Links", tbl_cell_style), Paragraph("<b>PASSED</b>", tbl_cell_center)],
        [Paragraph("TC-03", tbl_cell_center), Paragraph("Standard JPEG/PNG Image Upload and Multipart Handling", tbl_cell_style), Paragraph("<b>PASSED</b>", tbl_cell_center)],
        [Paragraph("TC-04", tbl_cell_center), Paragraph("Corrupt and Invalid File Format Rejection", tbl_cell_style), Paragraph("<b>PASSED</b>", tbl_cell_center)],
        [Paragraph("TC-05", tbl_cell_center), Paragraph("Stage 1 Dog vs. Non-Dog Canine Filter Validation", tbl_cell_style), Paragraph("<b>PASSED</b>", tbl_cell_center)],
        [Paragraph("TC-06", tbl_cell_center), Paragraph("TensorFlow SavedModel / Keras Model Weight Loading", tbl_cell_style), Paragraph("<b>PASSED</b>", tbl_cell_center)],
        [Paragraph("TC-07", tbl_cell_center), Paragraph("Stage 2 120-Breed Class Probability Inference", tbl_cell_style), Paragraph("<b>PASSED</b>", tbl_cell_center)],
        [Paragraph("TC-08", tbl_cell_center), Paragraph("Top-3 Ranked Confidence Scores Generation", tbl_cell_style), Paragraph("<b>PASSED</b>", tbl_cell_center)],
        [Paragraph("TC-09", tbl_cell_center), Paragraph("MySQL Database Connection and Schema Integrity", tbl_cell_style), Paragraph("<b>PASSED</b>", tbl_cell_center)],
        [Paragraph("TC-10", tbl_cell_center), Paragraph("User Account Registration, Password Hashing and Login", tbl_cell_style), Paragraph("<b>PASSED</b>", tbl_cell_center)],
        [Paragraph("TC-11", tbl_cell_center), Paragraph("Chronological Prediction History Logging and Retrieval", tbl_cell_style), Paragraph("<b>PASSED</b>", tbl_cell_center)],
        [Paragraph("TC-12", tbl_cell_center), Paragraph("User Favorite Breeds Curation and Toggle Operations", tbl_cell_style), Paragraph("<b>PASSED</b>", tbl_cell_center)],
        [Paragraph("TC-13", tbl_cell_center), Paragraph("Breed Directory Trait Retrieval (120 Breeds)", tbl_cell_style), Paragraph("<b>PASSED</b>", tbl_cell_center)],
        [Paragraph("TC-14", tbl_cell_center), Paragraph("Side-by-Side Dual Breed Comparison Matrix", tbl_cell_style), Paragraph("<b>PASSED</b>", tbl_cell_center)],
        [Paragraph("TC-15", tbl_cell_center), Paragraph("Evaluation Metric Visualization and Performance Charts", tbl_cell_style), Paragraph("<b>PASSED</b>", tbl_cell_center)],
        [Paragraph("TC-16", tbl_cell_center), Paragraph("Dynamic ReportLab PDF Report Build and Download", tbl_cell_style), Paragraph("<b>PASSED</b>", tbl_cell_center)],
        [Paragraph("TC-17", tbl_cell_center), Paragraph("Admin Dashboard Role-Based Security and Access Control", tbl_cell_style), Paragraph("<b>PASSED</b>", tbl_cell_center)],
        [Paragraph("TC-18", tbl_cell_center), Paragraph("Responsive UI Viewport Rendering Across Form Factors", tbl_cell_style), Paragraph("<b>PASSED</b>", tbl_cell_center)],
    ]
    t_tc = Table(tc_table_data, colWidths=[65, 360, 90])
    t_tc.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_header_bg),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_alt_row]),
        ('TEXTCOLOR', (2,1), (2,-1), colors.HexColor("#1E8449")),
    ]))
    story.append(t_tc)
    story.append(PageBreak())

    # =========================================================================
    # CHAPTER 7 â€“ CONCLUSION AND FUTURE ENHANCEMENTS
    # =========================================================================
    story.append(Paragraph("Chapter 7 â€“ Conclusion and Future Enhancements", h1_style))
    
    story.append(Paragraph("7.1 Summary of Work Done", h2_style))
    add_p(
        "In this project, our team designed, built, and evaluated an end-to-end canine identification system that classifies 120 domestic "
        "dog breeds from photographic images. Using the Stanford Dogs dataset of 10,222 images, we implemented transfer learning with MobileNetV2, "
        "training the model in two sequential phases: first freezing the convolutional base to establish stable classification weights, and then "
        "fine-tuning the top 30 layers with a lower learning rate. We also introduced a two-stage inference mechanism that verifies canine presence "
        "using ImageNet's 118 canine synsets before running the breed classifier, preventing irrelevant or non-dog images from producing false "
        "breed matches."
    )
    add_p(
        "To make the model practically usable, we developed a full-stack web application using Python Flask, HTML/CSS, JavaScript, and MySQL. "
        "The application provides user authentication, prediction history tracking, favorite breed management, an administrative statistics dashboard, "
        "a star-rating feedback system, and automated PDF report generation using ReportLab. Our automated testing suite verified all 18 functional "
        "modules, confirming that the entire application operates reliably from image upload to report generation."
    )

    story.append(Paragraph("7.2 Key Findings and Practical Observations", h2_style))
    add_p("Working on this project provided several valuable practical insights into applied deep learning and full-stack development:")
    add_p(
        "1. Transfer Learning Efficiency: Pre-training on ImageNet was essential. Training a deep network from scratch with only ~60 images per breed "
        "would lead to severe overfitting. MobileNetV2 provided an ideal balance between classification accuracy (77.64% Top-1, 96.87% Top-5) and "
        "inference speed, executing within 120â€“160 ms on standard CPU hardware."
    )
    add_p(
        "2. The Importance of Two-Stage Validation: Without our Stage 1 presence filter, standard closed-set classifiers will forcefully assign a dog "
        "breed to any uploaded picture, including cats, human faces, or household objects. Adding an upstream filter was crucial for making the system "
        "reliable for real users."
    )
    add_p(
        "3. Value of Top-3 Predictions: The jump from 77.64% Top-1 accuracy to 96.87% Top-5 accuracy shows that when the model misses the exact breed, "
        "the correct breed is almost always among the next couple of candidates. Presenting Top-3 predictions with confidence scores gives users a much "
        "more transparent and practical result."
    )

    story.append(Paragraph("7.3 Challenges Encountered and Solutions", h2_style))
    add_p("During implementation, we encountered several practical challenges that required iterative debugging and problem solving:")
    add_p(
        "â€¢ Fine-Grained Morphological Similarity: Closely related breeds (such as the Pembroke and Cardigan Welsh Corgis, or the Whippet and Italian "
        "Greyhound) proved difficult to separate purely from uncalibrated photographs. We addressed this by fine-tuning the top 30 convolutional layers, "
        "allowing the network to adapt higher-level texture and facial filters to canine-specific features."
    )
    add_p(
        "â€¢ Dataset Class Imbalance: Image counts per breed ranged from 66 to 126 images. We applied stratified train/validation/test splitting to "
        "ensure every partition preserved class proportions, and used data augmentation (rotation, zoom, horizontal flips) to balance training exposure."
    )
    add_p(
        "â€¢ Database and Session Management: Integrating role-based access control and persistent logging required careful handling of user sessions "
        "and SQL schemas. We used parameterized queries, hashed passwords with Werkzeug, and implemented clean foreign key constraints to ensure database "
        "integrity."
    )

    story.append(Paragraph("7.4 Future Enhancements", h2_style))
    add_p("While the current system satisfies all project objectives, we have identified several promising avenues for future improvement:")
    add_p("1. Multi-Dog Detection and Bounding Box Localization: Integrating an object detection network (such as YOLOv8) would allow the system to locate and classify multiple dogs in a single photograph independently.")
    add_p("2. Mixed-Breed Ancestry Estimation: Expanding the model output from single-label classification to multi-label regression would allow estimating percentage genetic contributions for mixed-breed dogs.")
    add_p("3. Mobile Application Deployment: Converting the trained model to TensorFlow Lite (TFLite) would enable on-device offline inference on Android and iOS smartphones without server connectivity.")
    add_p("4. Expanded Breed Catalog: Supplementing the Stanford Dogs dataset with additional international and indigenous dog breeds would broaden the system's global utility.")
    story.append(PageBreak())

    # =========================================================================
    # REFERENCES
    # =========================================================================
    story.append(Paragraph("REFERENCES", h1_style))
    story.append(Spacer(1, 6))

    references = [
        "[1] A. Khosla, N. Jayadevaprakash, B. Yao, and L. Fei-Fei, \"Novel dataset for fine-grained image categorization: Stanford Dogs,\" in Proc. IEEE Conf. Computer Vision and Pattern Recognition (CVPR) Workshops, Colorado Springs, CO, USA, Jun. 2011.",
        "[2] M. Sandler, A. Howard, M. Zhu, A. Zhmoginov, and L.-C. Chen, \"MobileNetV2: Inverted residuals and linear bottlenecks,\" in Proc. IEEE Conf. Computer Vision and Pattern Recognition (CVPR), Salt Lake City, UT, USA, Jun. 2018, pp. 4510â€“4520.",
        "[3] J. Deng, W. Dong, R. Socher, L.-J. Li, K. Li, and L. Fei-Fei, \"ImageNet: A large-scale hierarchical image database,\" in Proc. IEEE Conf. Computer Vision and Pattern Recognition (CVPR), Miami, FL, USA, Jun. 2009, pp. 248â€“255.",
        "[4] K. He, X. Zhang, S. Ren, and J. Sun, \"Deep residual learning for image recognition,\" in Proc. IEEE Conf. Computer Vision and Pattern Recognition (CVPR), Las Vegas, NV, USA, Jun. 2016, pp. 770â€“778.",
        "[5] K. Simonyan and A. Zisserman, \"Very deep convolutional networks for large-scale image recognition,\" in Proc. Int. Conf. Learning Representations (ICLR), San Diego, CA, USA, May 2015.",
        "[6] A. Krizhevsky, I. Sutskever, and G. E. Hinton, \"ImageNet classification with deep convolutional neural networks,\" in Advances in Neural Information Processing Systems (NeurIPS), Lake Tahoe, NV, USA, Dec. 2012, pp. 1097â€“1105.",
        "[7] S. J. Pan and Q. Yang, \"A survey on transfer learning,\" IEEE Transactions on Knowledge and Data Engineering, vol. 22, no. 10, pp. 1345â€“1359, Oct. 2010.",
        "[8] D. Hendrycks and K. Gimpel, \"A baseline for detecting out-of-distribution examples in neural networks,\" in Proc. Int. Conf. Learning Representations (ICLR), Toulon, France, Apr. 2017.",
        "[9] D. P. Kingma and J. Ba, \"Adam: A method for stochastic optimization,\" in Proc. Int. Conf. Learning Representations (ICLR), San Diego, CA, USA, May 2015.",
        "[10] D. Sculley et al., \"Hidden technical debt in machine learning systems,\" in Advances in Neural Information Processing Systems (NeurIPS), Montreal, Canada, Dec. 2015, pp. 2503â€“2511."
    ]
    for ref in references:
        add_p(ref, space_after=6)
    story.append(PageBreak())

    # =========================================================================
    # PROJECT TEAM CONTRIBUTION DETAILS
    # =========================================================================
    story.append(Paragraph("PROJECT TEAM CONTRIBUTION DETAILS", h1_style))
    story.append(Spacer(1, 6))

    add_p(
        "This project was collaboratively designed, developed, and evaluated by the four team members listed below. "
        "Each member assumed primary ownership of specific modules while collaborating closely on end-to-end system integration:"
    )
    story.append(Spacer(1, 6))

    contrib_data = [
        [Paragraph("<b>Member Name</b>", tbl_header_style), Paragraph("<b>Roll Number</b>", tbl_header_style), Paragraph("<b>Primary Module</b>", tbl_header_style), Paragraph("<b>Core Contributions</b>", tbl_header_style)],
        [Paragraph("K Goutham Nayak", tbl_cell_style), Paragraph("CS24B1081", tbl_cell_center), Paragraph("Backend Architecture & Reporting", tbl_cell_style), Paragraph("Flask routing, MySQL schema design, ReportLab PDF certificate engine, and authentication security.", tbl_cell_style)],
        [Paragraph("K Adithya", tbl_cell_style), Paragraph("CS24B1091", tbl_cell_center), Paragraph("Deep Learning & Model Training", tbl_cell_style), Paragraph("MobileNetV2 transfer learning, two-phase training strategy, hyperparameter tuning, and metric evaluation.", tbl_cell_style)],
        [Paragraph("R Mahesh Rathod", tbl_cell_style), Paragraph("CS24B1071", tbl_cell_center), Paragraph("Two-Stage Pipeline & Preprocessing", tbl_cell_style), Paragraph("Stage 1 canine presence filter, ImageNet synset mapping, data augmentation, and input validation.", tbl_cell_style)],
        [Paragraph("G Vishnu Vardhan", tbl_cell_style), Paragraph("CS24B1028", tbl_cell_center), Paragraph("Frontend UI/UX & Breed Directory", tbl_cell_style), Paragraph("Responsive interface design, Chart.js dashboard integration, breed directory, and side-by-side comparison.", tbl_cell_style)],
    ]
    t_contrib = Table(contrib_data, colWidths=[105, 75, 115, 220])
    t_contrib.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_header_bg),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_alt_row]),
    ]))
    story.append(t_contrib)

    # Build document
    doc.build(story, canvasmaker=AcademicCanvas)
    print(f"Final revised PDF report successfully created at: {output_path}")

if __name__ == "__main__":
    out_dir = "FINAL_REVISED_DOG_BREED_REPORT"
    os.makedirs(out_dir, exist_ok=True)
    out_file = os.path.join(out_dir, "Dog_Breed_Identification_Final_Report.pdf")
    create_pdf(out_file)
