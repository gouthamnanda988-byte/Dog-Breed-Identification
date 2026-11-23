"""
generate_pdf_report_v2.py
=========================
Generates an academic, publication-quality PDF project report for:
DOG BREED IDENTIFICATION USING DEEP LEARNING AND TRANSFER LEARNING

Features:
- Academic presentation layout inspired by IDSE3.pdf
- Front matter with Roman numerals, Chapters with Arabic numerals starting at 1
- Running headers and footers with thin rule lines
- Strict exclusion of certificates, declarations, and signature pages
- Centered figures with captions and booktabs-style formatted tables
"""

import os
from PIL import Image as PILImage
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, 
    Image, PageBreak, KeepTogether, Preformatted
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
    - Page 2 (Project Specs): Page 1
    - Pages 3..6 (Abstract, Contents, Lists): Roman numerals (i, ii, iii, iv)
    - Pages 7..end (Chapters 1 to 7, Refs, Team): Arabic numerals (1, 2, 3...)
    """
    def __init__(self, *args, **kwargs):
        super(AcademicCanvas, self).__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        # We know:
        # Page 1: Cover
        # Page 2: Project Specifications (numbered 1)
        # Page 3: Abstract (numbered i)
        # Page 4: Contents (numbered ii)
        # Page 5: List of Figures & Tables (numbered iii)
        # Page 6: Chapter 1 start (numbered 1)
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
        self.setFont("Times-Roman", 9)
        self.setFillColor(colors.HexColor("#333333"))
        self.setStrokeColor(colors.HexColor("#7F8C8D"))
        self.setLineWidth(0.5)

        # Header rule & text
        header_y = 841.89 - 36
        self.line(40, header_y, 595.27 - 40, header_y)
        self.drawString(40, header_y + 5, "[Institution / College Name]")
        self.drawRightString(595.27 - 40, header_y + 5, "Dog Breed Identification Report")

        # Footer rule & text
        footer_y = 40
        self.line(40, footer_y, 595.27 - 40, footer_y)
        self.drawString(40, footer_y - 12, "Department of Computer Science and Engineering / Data Science")

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
    c_header_bg = colors.HexColor("#EAECEE")    # Neutral Crisp Table Header
    c_alt_row = colors.HexColor("#F8F9FA")      # Off-white Row
    c_border = colors.HexColor("#BDC3C7")       # Clean Border Line
    c_text = colors.HexColor("#222222")         # Charcoal Body Text

    title_style = ParagraphStyle(
        'CoverTitle',
        parent=base_styles['Normal'],
        fontName='Times-Bold',
        fontSize=18,
        leading=23,
        alignment=TA_CENTER,
        textColor=c_primary,
        spaceAfter=12
    )

    cover_sub_style = ParagraphStyle(
        'CoverSubtitle',
        parent=base_styles['Normal'],
        fontName='Times-Italic',
        fontSize=11,
        leading=15,
        alignment=TA_CENTER,
        textColor=colors.HexColor("#333333"),
        spaceAfter=24
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
        parent=tbl_cell_style,
        alignment=TA_CENTER
    )

    tbl_cell_bold = ParagraphStyle(
        'TblCellBold',
        parent=tbl_cell_style,
        fontName='Times-Bold'
    )

    tbl_cell_bold_center = ParagraphStyle(
        'TblCellBoldCenter',
        parent=tbl_cell_center,
        fontName='Times-Bold'
    )

    code_style = ParagraphStyle(
        'CodeStyle',
        parent=base_styles['Normal'],
        fontName='Courier',
        fontSize=7.5,
        leading=9.5,
        textColor=colors.HexColor("#1A202C")
    )

    def add_img(img_path, caption, max_w=470, max_h=230):
        if os.path.exists(img_path):
            try:
                with PILImage.open(img_path) as pil_img:
                    w, h = pil_img.size
                aspect = h / float(w)
                render_w = min(max_w, 470)
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
    story.append(Spacer(1, 15))
    story.append(Paragraph("[INDIAN INSTITUTE OF INFORMATION TECHNOLOGY / INSTITUTION NAME]<br/><b>[DEPARTMENT OF COMPUTER SCIENCE AND ENGINEERING / DATA SCIENCE]</b>", ParagraphStyle('InstHead', parent=base_styles['Normal'], fontName='Times-Bold', fontSize=12, leading=16, alignment=TA_CENTER, textColor=c_primary)))
    story.append(Spacer(1, 4))
    story.append(Paragraph("B.Tech 3rd Year / Final Year – Academic Year 2025–2026<br/><b>INTRODUCTION TO DATA SCIENCE FOR ENGINEERS / CAPSTONE PROJECT REPORT</b>", ParagraphStyle('AcadSub', parent=base_styles['Normal'], fontName='Times-Roman', fontSize=10, leading=14, alignment=TA_CENTER, textColor=colors.HexColor("#1A5276"))))
    story.append(Spacer(1, 10))
    story.append(Paragraph("_________________________________________________________________________________", ParagraphStyle('DivLine', parent=base_styles['Normal'], fontName='Times-Roman', fontSize=9, alignment=TA_CENTER, textColor=colors.HexColor("#7F8C8D"))))
    story.append(Spacer(1, 15))

    story.append(Paragraph("DOG BREED IDENTIFICATION USING DEEP LEARNING AND TRANSFER LEARNING", title_style))
    story.append(Paragraph("An End-to-End Fine-Grained Canine Classification System Utilizing MobileNetV2,<br/>Two-Stage Image Validation, and a Full-Stack Web Platform", cover_sub_style))
    story.append(Spacer(1, 10))

    story.append(Paragraph("<b>PROJECT TEAM MEMBERS</b>", ParagraphStyle('SubBy', parent=base_styles['Normal'], fontName='Times-Bold', fontSize=11, alignment=TA_CENTER, textColor=c_primary, spaceAfter=8)))

    # Team Table
    team_data = [
        [Paragraph("S.No.", tbl_header_style), Paragraph("Name", tbl_header_style), Paragraph("Roll Number", tbl_header_style), Paragraph("Responsibility", tbl_header_style)],
        [Paragraph("1", tbl_cell_center), Paragraph("K Goutham Nayak", tbl_cell_bold), Paragraph("CS24B1081", tbl_cell_center), Paragraph("Backend Architecture, MySQL Database and PDF Reporting", tbl_cell_style)],
        [Paragraph("2", tbl_cell_center), Paragraph("K Adithya", tbl_cell_bold), Paragraph("CS24B1091", tbl_cell_center), Paragraph("Deep Learning Model Architecture and Fine-Tuning", tbl_cell_style)],
        [Paragraph("3", tbl_cell_center), Paragraph("R Mahesh Rathod", tbl_cell_bold), Paragraph("CS24B1071", tbl_cell_center), Paragraph("Two-Stage Canine Presence Detection and Validation", tbl_cell_style)],
        [Paragraph("4", tbl_cell_center), Paragraph("G Vishnu Vardhan", tbl_cell_bold), Paragraph("CS24B1028", tbl_cell_center), Paragraph("Frontend UI/UX, Breed Directory and Trait Comparison", tbl_cell_style)]
    ]
    t_team = Table(team_data, colWidths=[35, 125, 95, 260])
    t_team.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_header_bg),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(t_team)

    story.append(Spacer(1, 25))
    story.append(Paragraph("<b>Under the Guidance of:</b> [Faculty Guide Name, Designation]<br/>[Department of Computer Science and Engineering / Data Science]<br/>[Institution / College Name, Affiliated to University Name]<br/>Academic Year: 2025 – 2026", ParagraphStyle('GuideFoot', parent=base_styles['Normal'], fontName='Times-Roman', fontSize=9.5, leading=13.5, alignment=TA_CENTER, textColor=c_text)))

    story.append(PageBreak())

    # =========================================================================
    # 2. PROJECT SPECIFICATIONS (Page 2)
    # =========================================================================
    story.append(Paragraph("PROJECT SPECIFICATIONS", h1_style))
    specs_data = [
        [Paragraph("Course", tbl_cell_bold), Paragraph("Introduction to Data Science for Engineers / Capstone Project", tbl_cell_style)],
        [Paragraph("Academic Degree", tbl_cell_bold), Paragraph("Bachelor of Technology (B.Tech) in Computer Science / Data Science", tbl_cell_style)],
        [Paragraph("Core Deep Learning Model", tbl_cell_bold), Paragraph("MobileNetV2 with Inverted Residuals and Linear Bottlenecks", tbl_cell_style)],
        [Paragraph("Transfer Learning Source", tbl_cell_bold), Paragraph("ImageNet Pretrained Weights (1.4M images, 1,000 classes)", tbl_cell_style)],
        [Paragraph("Benchmark Dataset", tbl_cell_bold), Paragraph("Stanford Dogs / Kaggle Dog Breed Identification", tbl_cell_style)],
        [Paragraph("Total Photographic Images", tbl_cell_bold), Paragraph("10,222 labeled JPEG photographs", tbl_cell_style)],
        [Paragraph("Canine Breed Classes", tbl_cell_bold), Paragraph("120 purebred domestic dog varieties", tbl_cell_style)],
        [Paragraph("Input Image Resolution", tbl_cell_bold), Paragraph("224 × 224 pixels (3-channel RGB)", tbl_cell_style)],
        [Paragraph("Inference Pipeline", tbl_cell_bold), Paragraph("Two-Stage Architecture (Stage 1: Canine Filter; Stage 2: Breed Classifier)", tbl_cell_style)],
        [Paragraph("Web Application Framework", tbl_cell_bold), Paragraph("Python Flask 3.0 (REST APIs, Session Management, Jinja2)", tbl_cell_style)],
        [Paragraph("Database Management", tbl_cell_bold), Paragraph("MySQL 8.0 Server (dog_breed_db with 4 relational tables)", tbl_cell_style)],
        [Paragraph("Reporting Engine", tbl_cell_bold), Paragraph("Python ReportLab 5.1 (Dynamic PDF prediction certificate generation)", tbl_cell_style)],
        [Paragraph("Top-1 Test Accuracy", tbl_cell_bold), Paragraph("77.64% (on 1,534 held-out evaluation test images)", tbl_cell_style)],
        [Paragraph("Top-5 Test Accuracy", tbl_cell_bold), Paragraph("96.87% (on 1,534 held-out evaluation test images)", tbl_cell_style)],
        [Paragraph("Average Inference Latency", tbl_cell_bold), Paragraph("120 to 160 milliseconds per image on standard CPU", tbl_cell_style)],
        [Paragraph("Model Weight Storage Size", tbl_cell_bold), Paragraph("~14 MB (best_model.keras)", tbl_cell_style)]
    ]
    t_specs = Table(specs_data, colWidths=[180, 335])
    t_specs.setStyle(TableStyle([
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('ROWBACKGROUNDS', (0,0), (-1,-1), [colors.white, c_alt_row])
    ]))
    story.append(t_specs)

    story.append(PageBreak())

    # =========================================================================
    # 3. ABSTRACT (Page 3)
    # =========================================================================
    story.append(Paragraph("Abstract", h1_style))
    story.append(Paragraph("Domestic canines (<i>Canis lupus familiaris</i>) represent the most morphologically diverse mammal on Earth, encompassing hundreds of purebred varieties characterized by subtle variations in cranial geometry, ear carriage, muzzle length, coat pigmentation, and grooming profiles. Automatically classifying dog breeds from digital photographs is a quintessential challenge in <b>Fine-Grained Visual Categorization (FGVC)</b>. Unlike coarse-grained object detection where classes exhibit distinct silhouettes (such as distinguishing a vehicle from a dog), fine-grained canine classification must resolve two competing computer vision difficulties: <b>low inter-class variance</b>, where biologically related breeds exhibit virtually identical physical appearances (for instance, Whippets and Italian Greyhounds, or Lhasa Apsos and Shih-Tzus), and <b>high intra-class variance</b>, where dogs of the same breed differ markedly across coat patterns, colors, age, body postures, and photographic lighting.", body_style))

    story.append(Paragraph("In this project, we designed, implemented, and thoroughly evaluated an end-to-end canine identification platform utilizing transfer learning with <b>MobileNetV2</b> and backed by a full-stack relational web architecture. Using the benchmark Stanford Dogs / Kaggle Dog Breed dataset comprising <b>10,222 labeled photographs</b> across <b>120 purebred categories</b>, we established a stratified 70% training (7,155 images), 15% validation (1,533 images), and 15% testing (1,534 images) partition.", body_style))

    story.append(Paragraph("To resolve a pervasive limitation in existing classification systems—where non-dog inputs are arbitrarily forced into canine classes—we formulated an innovative <b>two-stage prediction pipeline</b>. In Stage 1, an upstream ImageNet-pretrained MobileNetV2 network evaluates whether an uploaded photograph contains a canine by monitoring 118 domestic and wild dog output categories, rejecting non-dog uploads (such as horses, felines, or vehicles) when the cumulative canine probability falls below 0.20. In Stage 2, verified canine images are classified by our fine-tuned MobileNetV2 architecture equipped with Global Average Pooling, 30% dropout regularization, and a 120-unit Softmax output layer.", body_style))

    story.append(Paragraph("Experimental evaluation on the 1,534 held-out test images demonstrated a <b>Top-1 test accuracy of 77.64%</b>, an exceptional <b>Top-5 test accuracy of 96.87%</b>, a test categorical cross-entropy loss of <b>0.7036</b>, and a macro F1-score of <b>76.91%</b>. On consumer CPU hardware, a complete forward pass completes in <b>120 to 160 milliseconds</b> with a compact model weight footprint of <b>14 MB</b>.", body_style))

    story.append(Paragraph("Beyond model development, we engineered a complete web platform using Python Flask and MySQL. The application provides drag-and-drop image uploads, Top-3 ranked candidate scores with animated confidence bars, an interactive 120-breed directory with trait comparison, automated PDF report downloads via ReportLab, personal prediction histories, and an administrative analytics dashboard. The completed system was verified using an automated 18-point testing suite, with all tests passing successfully.", body_style))

    story.append(Spacer(1, 8))
    story.append(Paragraph("<b>Keywords:</b> Dog Breed Identification, Deep Learning, Transfer Learning, MobileNetV2, Fine-Grained Visual Categorization, Computer Vision, Flask, MySQL, ReportLab.", body_style))

    story.append(PageBreak())

    # =========================================================================
    # 4. CONTENTS (Page 4)
    # =========================================================================
    story.append(Paragraph("Contents", h1_style))
    toc_data = [
        [Paragraph("<b>Project Specifications</b>", tbl_cell_style), Paragraph("<b>1</b>", tbl_cell_center)],
        [Paragraph("<b>Abstract</b>", tbl_cell_style), Paragraph("<b>i</b>", tbl_cell_center)],
        [Paragraph("<b>List of Figures & Tables</b>", tbl_cell_style), Paragraph("<b>iii</b>", tbl_cell_center)],
        [Paragraph("<b>Chapter 1 – Introduction</b>", tbl_cell_bold), Paragraph("<b>1</b>", tbl_cell_bold_center)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;Background of Dog Breed Identification", tbl_cell_style), Paragraph("1", tbl_cell_center)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;Problem Statement", tbl_cell_style), Paragraph("1", tbl_cell_center)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;Motivation", tbl_cell_style), Paragraph("2", tbl_cell_center)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;Objectives", tbl_cell_style), Paragraph("2", tbl_cell_center)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;Scope", tbl_cell_style), Paragraph("3", tbl_cell_center)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;Proposed Approach", tbl_cell_style), Paragraph("3", tbl_cell_center)],
        [Paragraph("<b>Chapter 2 – Literature Review</b>", tbl_cell_bold), Paragraph("<b>4</b>", tbl_cell_bold_center)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;Research on Dog Breed Classification", tbl_cell_style), Paragraph("4", tbl_cell_center)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;CNN-Based Classification", tbl_cell_style), Paragraph("4", tbl_cell_center)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;Transfer Learning Approaches", tbl_cell_style), Paragraph("4", tbl_cell_center)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;Comparison of Existing Research", tbl_cell_style), Paragraph("5", tbl_cell_center)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;Research Gap", tbl_cell_style), Paragraph("6", tbl_cell_center)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;Selection of MobileNetV2", tbl_cell_style), Paragraph("7", tbl_cell_center)],
        [Paragraph("<b>Chapter 3 – Dataset and Image Preparation</b>", tbl_cell_bold), Paragraph("<b>8</b>", tbl_cell_bold_center)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;Stanford Dogs Dataset", tbl_cell_style), Paragraph("8", tbl_cell_center)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;Breed Categories", tbl_cell_style), Paragraph("8", tbl_cell_center)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;Dataset Organization", tbl_cell_style), Paragraph("8", tbl_cell_center)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;Training, Validation and Testing Split", tbl_cell_style), Paragraph("9", tbl_cell_center)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;Image Resizing and Normalization", tbl_cell_style), Paragraph("9", tbl_cell_center)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;Data Augmentation", tbl_cell_style), Paragraph("10", tbl_cell_center)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;Dataset Challenges", tbl_cell_style), Paragraph("10", tbl_cell_center)],
        [Paragraph("<b>Chapter 4 – Proposed Methodology</b>", tbl_cell_bold), Paragraph("<b>11</b>", tbl_cell_bold_center)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;Overall System Architecture", tbl_cell_style), Paragraph("11", tbl_cell_center)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;Image Input and Validation", tbl_cell_style), Paragraph("11", tbl_cell_center)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;Dog Presence Verification", tbl_cell_style), Paragraph("12", tbl_cell_center)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;MobileNetV2 Feature Extraction", tbl_cell_style), Paragraph("13", tbl_cell_center)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;Transfer Learning and Fine-Tuning", tbl_cell_style), Paragraph("13", tbl_cell_center)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;Breed Classification", tbl_cell_style), Paragraph("14", tbl_cell_center)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;Prediction Confidence and Top-3 Results", tbl_cell_style), Paragraph("14", tbl_cell_center)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;Complete Prediction Workflow", tbl_cell_style), Paragraph("15", tbl_cell_center)],
        [Paragraph("<b>Chapter 5 – Model Development and Web Application</b>", tbl_cell_bold), Paragraph("<b>16</b>", tbl_cell_bold_center)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;Development Environment", tbl_cell_style), Paragraph("16", tbl_cell_center)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;Model Training", tbl_cell_style), Paragraph("16", tbl_cell_center)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;Model Integration", tbl_cell_style), Paragraph("17", tbl_cell_center)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;Flask Application Architecture", tbl_cell_style), Paragraph("17", tbl_cell_center)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;Image Upload and Prediction", tbl_cell_style), Paragraph("18", tbl_cell_center)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;User Authentication", tbl_cell_style), Paragraph("18", tbl_cell_center)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;Breed Information and Trait Comparison", tbl_cell_style), Paragraph("18", tbl_cell_center)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;Prediction History", tbl_cell_style), Paragraph("19", tbl_cell_center)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;Database Design", tbl_cell_style), Paragraph("19", tbl_cell_center)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;Other Implemented Features", tbl_cell_style), Paragraph("20", tbl_cell_center)],
        [Paragraph("<b>Chapter 6 – Results and Discussion</b>", tbl_cell_bold), Paragraph("<b>21</b>", tbl_cell_bold_center)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;Training and Validation Performance", tbl_cell_style), Paragraph("21", tbl_cell_center)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;Accuracy and Loss", tbl_cell_style), Paragraph("21", tbl_cell_center)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;Top-1 and Top-5 Accuracy", tbl_cell_style), Paragraph("22", tbl_cell_center)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;Precision, Recall and F1-Score", tbl_cell_style), Paragraph("22", tbl_cell_center)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;Prediction Examples", tbl_cell_style), Paragraph("23", tbl_cell_center)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;Dog and Non-Dog Image Testing", tbl_cell_style), Paragraph("23", tbl_cell_center)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;Commonly Confused Breeds", tbl_cell_style), Paragraph("24", tbl_cell_center)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;Application Testing", tbl_cell_style), Paragraph("25", tbl_cell_center)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;Observations", tbl_cell_style), Paragraph("26", tbl_cell_center)],
        [Paragraph("<b>Chapter 7 – Conclusion and Future Enhancements</b>", tbl_cell_bold), Paragraph("<b>27</b>", tbl_cell_bold_center)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;Project Summary", tbl_cell_style), Paragraph("27", tbl_cell_center)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;Learning Outcomes", tbl_cell_style), Paragraph("27", tbl_cell_center)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;Limitations", tbl_cell_style), Paragraph("28", tbl_cell_center)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;Future Improvements", tbl_cell_style), Paragraph("28", tbl_cell_center)],
        [Paragraph("<b>References</b>", tbl_cell_bold), Paragraph("<b>29</b>", tbl_cell_bold_center)],
        [Paragraph("<b>Team Contributions</b>", tbl_cell_bold), Paragraph("<b>31</b>", tbl_cell_bold_center)]
    ]
    t_toc = Table(toc_data, colWidths=[440, 75])
    t_toc.setStyle(TableStyle([
        ('LINEBELOW', (0,0), (-1,-1), 0.3, colors.HexColor("#EAECEE")),
        ('TOPPADDING', (0,0), (-1,-1), 1.2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 1.2),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(t_toc)

    story.append(PageBreak())

    # =========================================================================
    # 5. LIST OF FIGURES & TABLES (Page 5)
    # =========================================================================
    story.append(Paragraph("List of Figures", h1_style))
    fig_data = [
        [Paragraph("Figure 3.1", tbl_cell_bold), Paragraph("Sample Distribution Across 120 Dog Breeds in Stanford Dogs Dataset", tbl_cell_style), Paragraph("10", tbl_cell_center)],
        [Paragraph("Figure 4.1", tbl_cell_bold), Paragraph("Overall Multi-Tier System Architecture of the Platform", tbl_cell_style), Paragraph("11", tbl_cell_center)],
        [Paragraph("Figure 4.2", tbl_cell_bold), Paragraph("Two-Stage Canine Detection and Fine-Grained Classification Workflow", tbl_cell_style), Paragraph("12", tbl_cell_center)],
        [Paragraph("Figure 4.3", tbl_cell_bold), Paragraph("Transfer Learning Neural Network Architecture with MobileNetV2 Backbone", tbl_cell_style), Paragraph("13", tbl_cell_center)],
        [Paragraph("Figure 5.1", tbl_cell_bold), Paragraph("Administrative Dashboard Displaying Real-Time Metrics and Charts", tbl_cell_style), Paragraph("20", tbl_cell_center)],
        [Paragraph("Figure 6.1", tbl_cell_bold), Paragraph("Training and Validation Accuracy and Loss Curves Across 15 Epochs", tbl_cell_style), Paragraph("21", tbl_cell_center)],
        [Paragraph("Figure 6.2", tbl_cell_bold), Paragraph("Top 12 Most Frequently Confused Dog Breed Pairs in Evaluation Set", tbl_cell_style), Paragraph("24", tbl_cell_center)]
    ]
    t_figs = Table(fig_data, colWidths=[80, 375, 60])
    t_figs.setStyle(TableStyle([
        ('LINEBELOW', (0,0), (-1,-1), 0.3, colors.HexColor("#EAECEE")),
        ('TOPPADDING', (0,0), (-1,-1), 2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
    ]))
    story.append(t_figs)

    story.append(Spacer(1, 14))
    story.append(Paragraph("List of Tables", h1_style))
    tbl_data = [
        [Paragraph("Table 1.1", tbl_cell_bold), Paragraph("Comparison Between Conventional Identification and Proposed System", tbl_cell_style), Paragraph("3", tbl_cell_center)],
        [Paragraph("Table 2.1", tbl_cell_bold), Paragraph("Structured Comparison of Existing Research on Canine Breed Classification", tbl_cell_style), Paragraph("5", tbl_cell_center)],
        [Paragraph("Table 3.1", tbl_cell_bold), Paragraph("Dataset Partitioning into Training, Validation, and Testing Sets", tbl_cell_style), Paragraph("9", tbl_cell_center)],
        [Paragraph("Table 4.1", tbl_cell_bold), Paragraph("Neural Network Layer Progression and Parameter Distribution", tbl_cell_style), Paragraph("13", tbl_cell_center)],
        [Paragraph("Table 5.1", tbl_cell_bold), Paragraph("Model Training Hyperparameter Configuration", tbl_cell_style), Paragraph("16", tbl_cell_center)],
        [Paragraph("Table 5.2", tbl_cell_bold), Paragraph("Relational Database Schema Design (dog_breed_db)", tbl_cell_style), Paragraph("19", tbl_cell_center)],
        [Paragraph("Table 5.3", tbl_cell_bold), Paragraph("Core Software Technologies and Functional Roles", tbl_cell_style), Paragraph("17", tbl_cell_center)],
        [Paragraph("Table 6.1", tbl_cell_bold), Paragraph("Model Performance Metrics on Held-Out Test Set (1,534 Images)", tbl_cell_style), Paragraph("22", tbl_cell_center)],
        [Paragraph("Table 6.2", tbl_cell_bold), Paragraph("Top 12 Most Frequently Confused Dog Breed Pairs with Visual Reasons", tbl_cell_style), Paragraph("24", tbl_cell_center)],
        [Paragraph("Table 6.3", tbl_cell_bold), Paragraph("Complete 18-Point Automated Application Test Suite Verification", tbl_cell_style), Paragraph("25", tbl_cell_center)]
    ]
    t_tbls = Table(tbl_data, colWidths=[80, 375, 60])
    t_tbls.setStyle(TableStyle([
        ('LINEBELOW', (0,0), (-1,-1), 0.3, colors.HexColor("#EAECEE")),
        ('TOPPADDING', (0,0), (-1,-1), 2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
    ]))
    story.append(t_tbls)

    story.append(PageBreak())

    # =========================================================================
    # CHAPTER 1 – INTRODUCTION (Page 6 -> Main Page 1)
    # =========================================================================
    story.append(Paragraph("Chapter 1 – Introduction", h1_style))
    
    story.append(Paragraph("Background of Dog Breed Identification", h2_style))
    story.append(Paragraph("Computer vision has experienced extraordinary progress over the past decade through the emergence of deep Convolutional Neural Networks (CNNs). In traditional object recognition tasks, models are tasked with discriminating between broad object categories that possess fundamentally distinct shapes, edges, and silhouettes—such as separating a car from an airplane, or an animal from a building.", body_style))
    story.append(Paragraph("In contrast, canine breed classification belongs to the specialized and challenging domain of <b>Fine-Grained Visual Categorization (FGVC)</b>. Canines belong to the same biological species (<i>Canis lupus familiaris</i>), yet selective breeding practiced by humans over hundreds of years has produced more than 300 globally recognized domestic breeds. These breeds display remarkable morphological diversity: they range from miniature toy lapdogs like the Chihuahua (weighing under 2 kg) to giant draft and guard dogs like the Saint Bernard and Mastiff (weighing over 80 kg).", body_style))
    story.append(Paragraph("Developing an automated system capable of recognizing 120 distinct breeds directly from user photographs requires a neural network to look beyond coarse silhouettes and learn subtle, discriminative anatomical markers—such as the curl of a tail, muzzle-to-skull proportions, ear posture, coat texture, and facial pigmentation patterns.", body_style))

    story.append(Paragraph("Problem Statement", h2_style))
    story.append(Paragraph("Accurately determining a dog's breed from an unconstrained digital photograph is notoriously difficult, even for experienced canine professionals, veterinarians, and animal shelter intake officers. The primary challenges include:", body_style))
    story.append(Paragraph("1. <b>Low Inter-Class Variance:</b> Biologically related breeds often look almost identical to the human eye. For example, a Whippet and an Italian Greyhound share an identical aerodynamic sighthound posture and sleek short coat, differing primarily in physical scale that cannot be measured from a 2D photograph lacking reference objects. Similarly, a Lhasa Apso and a Shih-Tzu both feature long, flowing facial fur that completely conceals underlying facial bone structure.", body_style))
    story.append(Paragraph("2. <b>High Intra-Class Variance:</b> Canines of the same recognized purebred breed display substantial variations in fur color morphs, coat trimming styles, age, facial expressions, and body weight.", body_style))
    story.append(Paragraph("3. <b>Unconstrained Photographic Conditions:</b> Real-world photographs submitted by users often feature poor illumination, cluttered domestic or outdoor backgrounds, partial occlusions by humans or furniture, and non-standard camera angles.", body_style))
    story.append(Paragraph("4. <b>The Non-Dog False Prediction Problem:</b> A significant flaw in existing classification systems is their closed-world assumption: if a user uploads a photograph of a horse, a cat, or a car, a single-stage 120-class classifier will forcefully output one of the 120 dog breeds with arbitrary confidence.", body_style))
    story.append(Paragraph("An automated, reliable, and user-friendly system is required that can first verify whether a photograph contains a dog, and then accurately identify the breed with ranked probability scores and detailed breed profiles.", body_style))

    story.append(Paragraph("Motivation", h2_style))
    story.append(Paragraph("The motivation behind this project is driven by both practical real-world utility and academic learning:", body_style))
    story.append(Paragraph("• <b>Veterinary Medicine and Animal Shelters:</b> Animal welfare organizations and veterinary clinics frequently need to determine a dog's breed to anticipate hereditary health vulnerabilities (such as gastric torsion in deep-chested breeds, hip dysplasia in German Shepherds, or respiratory distress in brachycephalic dogs like French Bulldogs).", body_style))
    story.append(Paragraph("• <b>Lost and Found Animal Recovery:</b> In municipal animal shelters, correctly identifying a lost pet's breed accelerates matching with owner lost-pet reports and adoption records.", body_style))
    story.append(Paragraph("• <b>Academic Exploration of Transfer Learning:</b> As B.Tech Data Science students, fine-grained canine classification provided an ideal capstone project to investigate transfer learning, mitigate overfitting on small datasets, design multi-tier web applications, and implement relational database architectures.", body_style))

    story.append(Paragraph("Objectives", h2_style))
    story.append(Paragraph("The primary objectives of this project are:<br/>"
                           "1. Prepare and preprocess the Stanford Dogs benchmark dataset across 120 breeds.<br/>"
                           "2. Build an upstream Stage 1 canine presence filter utilizing ImageNet MobileNetV2 to reject non-dog uploads.<br/>"
                           "3. Fine-tune a lightweight MobileNetV2 architecture for 120-breed classification using a two-phase training procedure.<br/>"
                           "4. Extract and present ranked Top-3 candidate predictions with animated confidence bars.<br/>"
                           "5. Construct a responsive, modern web portal using Python Flask and cream-and-brown styled CSS.<br/>"
                           "6. Implement a persistent MySQL relational database storing user accounts, prediction history, favorites, and feedback.<br/>"
                           "7. Develop dynamic PDF prediction report generation using Python ReportLab.<br/>"
                           "8. Integrate an interactive 120-breed directory and side-by-side trait comparison tool.<br/>"
                           "9. Build an administrative analytics dashboard computing real-time SQL aggregates.<br/>"
                           "10. Validate system stability through an automated 18-point testing suite.", body_style))

    story.append(Paragraph("Scope", h2_style))
    story.append(Paragraph("• <b>Target Categories:</b> 120 recognized purebred dog breeds as defined by the Stanford Dogs benchmark.<br/>"
                           "• <b>Input Modality:</b> Single-subject canine photographs in JPG, JPEG, or PNG formats up to 10 MB in file size.<br/>"
                           "• <b>Core Processing:</b> 224 × 224 RGB image normalization and inference via TensorFlow / Keras MobileNetV2.<br/>"
                           "• <b>Web Interface:</b> Cross-browser responsive web application accessible on desktop, tablet, and mobile viewport widths.<br/>"
                           "• <b>System Boundaries:</b> The current system is designed for single-dog photographs and does not support multi-dog instance segmentation or mixed-breed genetic percentage estimation.", body_style))

    story.append(Paragraph("Proposed Approach", h2_style))
    story.append(Paragraph("Our proposed approach addresses the limitations of conventional and command-line identification systems by coupling deep learning transfer learning with a multi-tier web architecture:", body_style))

    # Table 1.1
    story.append(Paragraph("<b>Table 1.1: Comparison Between Conventional Identification and Proposed System</b>", caption_style))
    comp_headers = [Paragraph("Feature / Dimension", tbl_header_style), Paragraph("Conventional / Existing Systems", tbl_header_style), Paragraph("Our Proposed Implementation", tbl_header_style)]
    comp_data = [
        comp_headers,
        [Paragraph("Identification Method", tbl_cell_bold), Paragraph("Manual visual inspection using kennel books or memory", tbl_cell_style), Paragraph("Automated two-stage deep learning inference pipeline", tbl_cell_style)],
        [Paragraph("Speed and Accessibility", tbl_cell_bold), Paragraph("Slow, subjective, requires domain expertise", tbl_cell_style), Paragraph("Instant inference (<150 ms per image) accessible via web browser", tbl_cell_style)],
        [Paragraph("Non-Dog Input Handling", tbl_cell_bold), Paragraph("Typically produces a false positive dog prediction", tbl_cell_style), Paragraph("Stage 1 ImageNet filter validates canine presence and rejects non-dogs", tbl_cell_style)],
        [Paragraph("Model Architecture", tbl_cell_bold), Paragraph("Heavy models (VGG16, ResNet50) requiring dedicated GPUs", tbl_cell_style), Paragraph("Lightweight MobileNetV2 (~3.5M parameters) optimized for CPU deployment", tbl_cell_style)],
        [Paragraph("Output Information", tbl_cell_bold), Paragraph("Single hard predicted label", tbl_cell_style), Paragraph("Primary breed match, confidence percentage, and ranked Top-3 alternatives", tbl_cell_style)],
        [Paragraph("Data Persistence", tbl_cell_bold), Paragraph("Stateless or desktop command-line scripts", tbl_cell_style), Paragraph("Persistent MySQL database tracking individual user history and feedback", tbl_cell_style)],
        [Paragraph("Reporting", tbl_cell_bold), Paragraph("Manual screenshotting or logging", tbl_cell_style), Paragraph("One-click automated PDF prediction report generation via ReportLab", tbl_cell_style)]
    ]
    t_comp = Table(comp_data, colWidths=[120, 195, 200])
    t_comp.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_header_bg),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_alt_row])
    ]))
    story.append(t_comp)

    story.append(PageBreak())

    # =========================================================================
    # CHAPTER 2 – LITERATURE REVIEW
    # =========================================================================
    story.append(Paragraph("Chapter 2 – Literature Review", h1_style))
    
    story.append(Paragraph("Research on Dog Breed Classification", h2_style))
    story.append(Paragraph("Research in automated animal identification has transitioned from classical hand-crafted feature extractors (such as SIFT, HOG, and color histograms) to deep convolutional neural networks. Early approaches struggled with canine classification because coat patterns and lighting variations caused high intra-class variance that manual mathematical descriptors could not effectively capture.", body_style))

    story.append(Paragraph("CNN-Based Classification", h2_style))
    story.append(Paragraph("Convolutional Neural Networks transformed the field by learning hierarchical feature representations directly from raw pixels. The initial convolutional layers learn low-level primitives like edges, lines, and color gradients; intermediate layers combine these into textures and ear or eye contours; and deeper layers synthesize full facial and body representations. However, training a deep CNN entirely from scratch on 120 dog breeds requires hundreds of thousands of labeled images, which are rarely available for specialized fine-grained domains.", body_style))

    story.append(Paragraph("Transfer Learning Approaches", h2_style))
    story.append(Paragraph("Transfer learning addresses data scarcity by taking a network pre-trained on a massive visual corpus—most notably ImageNet, which contains 1.4 million images across 1,000 diverse categories—and transferring its learned feature representations to a target domain. Because ImageNet already includes 118 classes of domestic dogs and wild canids, its pre-trained convolutional filters already possess specialized knowledge of fur textures, canine ear structures, and facial geometry.", body_style))

    story.append(Paragraph("Comparison of Existing Research", h2_style))
    story.append(Paragraph("We conducted a comprehensive literature survey examining twelve recent peer-reviewed research papers focusing on canine breed recognition, transfer learning, and out-of-distribution detection:", body_style))

    # Table 2.1
    story.append(Paragraph("<b>Table 2.1: Structured Comparison of Existing Research on Canine Breed Classification</b>", caption_style))
    lit_headers = [Paragraph("Paper & Authors", tbl_header_style), Paragraph("Year", tbl_header_style), Paragraph("Model / Technique", tbl_header_style), Paragraph("Dataset Used", tbl_header_style), Paragraph("Reported Result", tbl_header_style), Paragraph("Key Limitation Observed", tbl_header_style)]
    lit_data = [
        lit_headers,
        [Paragraph("Selvaraj et al.", tbl_cell_bold), Paragraph("2023", tbl_cell_center), Paragraph("ResNet50 Transfer Learning", tbl_cell_style), Paragraph("Stanford Dogs (10,222)", tbl_cell_style), Paragraph("93.0% Accuracy", tbl_cell_style), Paragraph("High compute cost; 120 breeds only", tbl_cell_style)],
        [Paragraph("Borwarnginn et al.", tbl_cell_bold), Paragraph("2021", tbl_cell_center), Paragraph("NASNet + Face Cropping", tbl_cell_style), Paragraph("Columbia Dogs (8,111)", tbl_cell_style), Paragraph("89.92% Accuracy", tbl_cell_style), Paragraph("Fails if facial crop fails", tbl_cell_style)],
        [Paragraph("Bokhari et al.", tbl_cell_bold), Paragraph("2022", tbl_cell_center), Paragraph("MobileNetV2 Feature Extractor", tbl_cell_style), Paragraph("Stanford Dogs (120 breeds)", tbl_cell_style), Paragraph("85% (50 cl.) / 64% (120 cl.)", tbl_cell_style), Paragraph("Steep drop on scaling to 120 classes", tbl_cell_style)],
        [Paragraph("Kumaravel et al.", tbl_cell_bold), Paragraph("2023", tbl_cell_center), Paragraph("DenseNet201 + Augmentation", tbl_cell_style), Paragraph("Stanford + Kaggle (120k)", tbl_cell_style), Paragraph("87.34% Accuracy", tbl_cell_style), Paragraph("Diminishing returns beyond saturation", tbl_cell_style)],
        [Paragraph("Banakar et al.", tbl_cell_bold), Paragraph("2023", tbl_cell_center), Paragraph("VGG-19 + Client/Server", tbl_cell_style), Paragraph("Stanford Dogs (120 breeds)", tbl_cell_style), Paragraph("High fine-tuned accuracy", tbl_cell_style), Paragraph("Bulky model weights (~550 MB)", tbl_cell_style)],
        [Paragraph("Valarmathi et al.", tbl_cell_bold), Paragraph("2023", tbl_cell_center), Paragraph("Hybrid InceptionV3 + Xception", tbl_cell_style), Paragraph("Stanford Dogs (10,222)", tbl_cell_style), Paragraph("92.4% Val Acc (98.4% Tr)", tbl_cell_style), Paragraph("Massive compute cost; slow inference", tbl_cell_style)],
        [Paragraph("Basha et al.", tbl_cell_bold), Paragraph("2021", tbl_cell_center), Paragraph("VGG16 in PyTorch", tbl_cell_style), Paragraph("Canine breed image set", tbl_cell_style), Paragraph("CNN representation verified", tbl_cell_style), Paragraph("Vulnerable to lighting and pose shifts", tbl_cell_style)],
        [Paragraph("Hussain et al.", tbl_cell_bold), Paragraph("2025", tbl_cell_center), Paragraph("InceptionV3 + Background Rem.", tbl_cell_style), Paragraph("Stanford Dogs (20,580)", tbl_cell_style), Paragraph("91.2% Accuracy", tbl_cell_style), Paragraph("Segmentation clips anatomical edges", tbl_cell_style)],
        [Paragraph("Ghotra et al.", tbl_cell_bold), Paragraph("2023", tbl_cell_center), Paragraph("MobileNetV2 + Flask + Ngrok", tbl_cell_style), Paragraph("Kaggle Dog Breeds (>10,222)", tbl_cell_style), Paragraph("99.89% Train Accuracy", tbl_cell_style), Paragraph("High overfitting risk; no non-dog check", tbl_cell_style)],
        [Paragraph("Bankar et al.", tbl_cell_bold), Paragraph("2025", tbl_cell_center), Paragraph("CNN + Facial Keypoint Hub", tbl_cell_style), Paragraph("Online set (8,350 images)", tbl_cell_style), Paragraph("90% Train / 70% Test", tbl_cell_style), Paragraph("Severe 20% overfitting gap", tbl_cell_style)],
        [Paragraph("Zou et al.", tbl_cell_bold), Paragraph("2020", tbl_cell_center), Paragraph("WS-DAN, TBMSL-Net, PMG", tbl_cell_style), Paragraph("Tsinghua Dogs (70,428)", tbl_cell_style), Paragraph("WS-DAN: 86.4%, TBMSL: 83.7%", tbl_cell_style), Paragraph("Complex multi-stage attention networks", tbl_cell_style)],
        [Paragraph("Perera & Patel", tbl_cell_bold), Paragraph("2019", tbl_cell_center), Paragraph("Deep Novelty Detection", tbl_cell_style), Paragraph("Stanford Dogs + Multi-dataset", tbl_cell_style), Paragraph("AUC: 0.825, Acc: 80.1%", tbl_cell_style), Paragraph("Sensitive to activation thresholds", tbl_cell_style)]
    ]
    t_lit = Table(lit_data, colWidths=[80, 32, 108, 95, 95, 105])
    t_lit.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_header_bg),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('TOPPADDING', (0,0), (-1,-1), 2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_alt_row])
    ]))
    story.append(t_lit)

    story.append(Paragraph("Research Gap", h2_style))
    story.append(Paragraph("Our comparative analysis revealed four critical shortcomings across the surveyed research:<br/>"
                           "1. <b>Absence of Out-of-Distribution Validation:</b> All surveyed web applications assume the user will only upload valid dog photographs. If a user uploads an image of a cat, horse, or car, these systems return a false canine breed prediction with high confidence.<br/>"
                           "2. <b>Computational Footprint vs. Speed Trade-Off:</b> Heavy ensemble architectures (Valarmathi et al.) and deep networks (Banakar et al.) achieve high accuracy but require dedicated GPU acceleration and take 1.5–3 seconds per image. Conversely, basic MobileNet implementations (Bokhari et al.) suffered a sharp accuracy collapse (64%) when scaled to 120 breeds without fine-tuning.<br/>"
                           "3. <b>Lack of Uncertainty Transparency:</b> Almost all implementations output a single hard class label. In fine-grained classification where breeds look nearly identical, concealing the model's alternative predictions hides important uncertainty from users.<br/>"
                           "4. <b>Lack of Full-Stack Data Management:</b> Prior works operated primarily as standalone machine learning scripts without user authentication, database persistence, or dynamic reporting.", body_style))

    story.append(Paragraph("Selection of MobileNetV2", h2_style))
    story.append(Paragraph("To overcome these gaps, we selected <b>MobileNetV2</b> as our core neural backbone. MobileNetV2 is specifically designed for high-efficiency mobile and edge vision applications through its innovative <b>Inverted Residuals and Linear Bottlenecks</b>:<br/>"
                           "• Standard convolutional layers apply spatial filtering and channel transformation simultaneously, requiring huge parameter matrices.<br/>"
                           "• MobileNetV2 splits this operation into a 1×1 expansion convolution (increasing channels by an expansion factor t=6), a 3×3 depthwise convolution (applying spatial filtering independently on each channel), and a 1×1 pointwise linear projection (compressing channels without non-linear ReLU distortion).<br/>"
                           "• This architecture requires only <b>~3.5 million parameters</b>, resulting in a trained model file of just <b>~14 MB</b>. On a standard multi-core CPU, MobileNetV2 executes a forward pass in <b>under 150 milliseconds</b>, making it ideal for interactive web serving without needing a costly dedicated GPU.", body_style))

    story.append(PageBreak())

    # =========================================================================
    # CHAPTER 3 – DATASET AND IMAGE PREPARATION
    # =========================================================================
    story.append(Paragraph("Chapter 3 – Dataset and Image Preparation", h1_style))
    
    story.append(Paragraph("Stanford Dogs Dataset", h2_style))
    story.append(Paragraph("Our project utilizes the widely respected Stanford Dogs / Kaggle Dog Breed Identification dataset. Originally compiled by Aditya Khosla et al. at Stanford University from ImageNet, the dataset consists of <b>10,222 labeled photographs</b> covering <b>120 recognized purebred dog breeds</b>. The photographs were taken under natural, unconstrained real-world conditions, encompassing varied domestic living rooms, outdoor parks, diverse focal distances, and natural canine activities.", body_style))

    story.append(Paragraph("Breed Categories", h2_style))
    story.append(Paragraph("The 120 canine categories represent a broad cross-section of global kennel classifications, including toy companions (Chihuahua, Pomeranian, Maltese Dog), working giants (Great Dane, Saint Bernard, Bullmastiff), pastoral herders (German Shepherd, Collie, Border Collie), energetic sporting retrievers (Golden Retriever, Labrador Retriever), and slender sighthounds (Whippet, Borzoi, Saluki).", body_style))

    story.append(Paragraph("Dataset Organization", h2_style))
    story.append(Paragraph("The dataset is structured around an image directory containing 10,222 JPEG files named by unique 32-character hexadecimal identifiers, paired with labels.csv mapping each ID to its ground-truth breed. File headers were verified using JPEG magic bytes (<code>0xFFD8</code>), confirming 100% data integrity across all 10,222 files.", body_style))

    story.append(Paragraph("Training, Validation and Testing Split", h2_style))
    story.append(Paragraph("To ensure unbiased academic evaluation, we partitioned the 10,222 images using a stratified 70% / 15% / 15% split governed by a fixed random seed (seed = 42):", body_style))

    # Table 3.1
    story.append(Paragraph("<b>Table 3.1: Dataset Partitioning into Training, Validation, and Testing Sets</b>", caption_style))
    split_headers = [Paragraph("Partition Subset", tbl_header_style), Paragraph("Image Count", tbl_header_style), Paragraph("Percentage (%)", tbl_header_style), Paragraph("Functional Purpose", tbl_header_style)]
    split_data = [
        split_headers,
        [Paragraph("Training Set", tbl_cell_bold), Paragraph("7,155 images", tbl_cell_center), Paragraph("70.0%", tbl_cell_center), Paragraph("Model parameter optimization and backpropagation", tbl_cell_style)],
        [Paragraph("Validation Set", tbl_cell_bold), Paragraph("1,533 images", tbl_cell_center), Paragraph("15.0%", tbl_cell_center), Paragraph("Hyperparameter tuning, early stopping, and checkpoint selection", tbl_cell_style)],
        [Paragraph("Testing Set (Held-Out)", tbl_cell_bold), Paragraph("1,534 images", tbl_cell_center), Paragraph("15.0%", tbl_cell_center), Paragraph("Unbiased final evaluation and confusion matrix computation", tbl_cell_style)],
        [Paragraph("Total Corpus", tbl_cell_bold), Paragraph("10,222 images", tbl_cell_bold_center), Paragraph("100.0%", tbl_cell_bold_center), Paragraph("Complete Stanford Dogs benchmark across 120 breeds", tbl_cell_bold)]
    ]
    t_split = Table(split_data, colWidths=[120, 95, 80, 220])
    t_split.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_header_bg),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BACKGROUND', (0,4), (-1,4), c_header_bg),
        ('ROWBACKGROUNDS', (0,1), (-1,3), [colors.white, c_alt_row])
    ]))
    story.append(t_split)

    story.append(Paragraph("The class distribution shows an average of 85.18 images per breed (median: 82.0). The dataset exhibits mild class imbalance: Scottish Deerhound has the highest representation with 126 images, while Briard and Eskimo Dog possess the minimum representation with 66 images each.", body_style))

    add_img("dataset/breed_distribution.png", "Figure 3.1: Sample Distribution Across 120 Dog Breeds in the Stanford Dogs Dataset", max_w=470, max_h=190)

    story.append(Paragraph("Image Resizing and Normalization", h2_style))
    story.append(Paragraph("Raw photographs possess varying dimensions and aspect ratios. Before batch processing, images pass through an automated preprocessing pipeline: (1) RGB format standardization, (2) bilinear spatial resizing to 224 × 224 pixels, (3) float32 normalization scaling pixels to [-1.0, +1.0] via <i>x_norm = (x / 127.5) - 1.0</i>, and (4) batch dimension expansion to shape (1, 224, 224, 3).", body_style))

    story.append(Paragraph("Data Augmentation", h2_style))
    story.append(Paragraph("To expand feature diversity on the 7,155 training samples, we applied real-time stochastic augmentation: random horizontal flipping (50% probability), random rotation (±15 degrees), random zoom (±10%), random width and height shifts (±10%), and nearest boundary filling.", body_style))

    story.append(Paragraph("Dataset Challenges", h2_style))
    story.append(Paragraph("Exploratory inspection revealed three primary visual challenges: subtle facial distinctions between related breeds, environmental background clutter (grass, snow, living room rugs), and extreme posture variations (sleeping, jumping, panting).", body_style))

    story.append(PageBreak())

    # =========================================================================
    # CHAPTER 4 – PROPOSED METHODOLOGY
    # =========================================================================
    story.append(Paragraph("Chapter 4 – Proposed Methodology", h1_style))
    
    story.append(Paragraph("Overall System Architecture", h2_style))
    story.append(Paragraph("We engineered the system as a decoupled, multi-tier web application consisting of four distinct tiers: Presentation Tier (Browser Client), Application Tier (Flask Web Framework), Deep Learning Tier (TensorFlow / Keras), and Database Tier (MySQL Server).", body_style))

    add_img("model/report_assets/system_architecture.png", "Figure 4.1: Overall Multi-Tier System Architecture of the Dog Breed Identification Platform", max_w=470, max_h=200)

    story.append(Paragraph("Image Input and Validation", h2_style))
    story.append(Paragraph("When a user uploads an image, client-side JavaScript validates file format (.jpg, .jpeg, .png) and size (<= 10 MB). On the server, app.py sanitizes the filename with secure_filename() and verifies image decodability using PIL.", body_style))

    story.append(Paragraph("Dog Presence Verification", h2_style))
    story.append(Paragraph("To prevent non-dog uploads from receiving arbitrary dog breed predictions, Stage 1 evaluates the tensor using an ImageNet MobileNetV2 network monitoring 118 canine output classes. If the Top-1 predicted ImageNet class is a canine or cumulative canine probability P(dog) >= 0.20, the image is verified as a dog. Otherwise, the pipeline halts immediately with a 'No Dog Detected' alert.", body_style))

    add_img("model/report_assets/two_stage_pipeline.png", "Figure 4.2: Two-Stage Canine Detection and Fine-Grained Breed Classification Workflow", max_w=470, max_h=180)

    story.append(Paragraph("MobileNetV2 Feature Extraction", h2_style))
    story.append(Paragraph("Confirmed canine images are processed by our customized MobileNetV2 architecture. The network extracts rich spatial features through 155 layers of depthwise separable convolutions and inverted residual bottlenecks, outputting a high-level feature map of shape (7, 7, 1280).", body_style))

    add_img("model/report_assets/cnn_architecture.png", "Figure 4.3: Transfer Learning Neural Network Architecture with MobileNetV2 Backbone", max_w=470, max_h=180)

    story.append(Paragraph("Transfer Learning and Fine-Tuning", h2_style))
    story.append(Paragraph("Training was conducted in two sequential phases: Phase 1 (Frozen Base) trained only the new classification head for 10 epochs with Adam (lr = 1e-3). Phase 2 (Fine-Tuning) unfroze the top 30 base layers for 5 epochs with a reduced learning rate (lr = 1e-5), allowing high-level filters to specialize in canine facial and coat textures.", body_style))

    story.append(Paragraph("Breed Classification", h2_style))
    story.append(Paragraph("Above the MobileNetV2 base, GlobalAveragePooling2D condenses the feature map into 1,280 features, Dropout (0.3) prevents overfitting, and a Dense Softmax layer outputs normalized probabilities across all 120 breeds.", body_style))

    # Table 4.1
    story.append(Paragraph("<b>Table 4.1: Neural Network Layer Progression and Parameter Distribution</b>", caption_style))
    layer_headers = [Paragraph("Layer Component", tbl_header_style), Paragraph("Output Shape", tbl_header_style), Paragraph("Parameters", tbl_header_style), Paragraph("Function in Architecture", tbl_header_style)]
    layer_data = [
        layer_headers,
        [Paragraph("InputLayer", tbl_cell_bold), Paragraph("(None, 224, 224, 3)", tbl_cell_center), Paragraph("0", tbl_cell_center), Paragraph("Accepts normalized RGB image tensors", tbl_cell_style)],
        [Paragraph("MobileNetV2 Base (155 layers)", tbl_cell_bold), Paragraph("(None, 7, 7, 1280)", tbl_cell_center), Paragraph("2,257,984", tbl_cell_center), Paragraph("Depthwise separable feature extraction", tbl_cell_style)],
        [Paragraph("GlobalAveragePooling2D", tbl_cell_bold), Paragraph("(None, 1280)", tbl_cell_center), Paragraph("0", tbl_cell_center), Paragraph("Spatial pooling to 1D feature vector", tbl_cell_style)],
        [Paragraph("Dropout (0.3 rate)", tbl_cell_bold), Paragraph("(None, 1280)", tbl_cell_center), Paragraph("0", tbl_cell_center), Paragraph("Regularization preventing co-adaptation", tbl_cell_style)],
        [Paragraph("Dense (Softmax)", tbl_cell_bold), Paragraph("(None, 120)", tbl_cell_center), Paragraph("153,720", tbl_cell_center), Paragraph("Class probability output across 120 breeds", tbl_cell_style)]
    ]
    t_layer = Table(layer_data, colWidths=[130, 110, 75, 200])
    t_layer.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_header_bg),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_alt_row])
    ]))
    story.append(t_layer)

    story.append(Paragraph("Prediction Confidence and Top-3 Results", h2_style))
    story.append(Paragraph("Rather than returning only a single class label, our system extracts the top 3 highest probabilities: the top-1 class is identified as the primary breed match, while the 2nd and 3rd highest probabilities are extracted as candidate alternatives. Displaying Top-3 predictions provides full transparency to users, especially when the photograph depicts a mixed breed or a breed with visual similarity to another class.", body_style))

    story.append(Paragraph("Complete Prediction Workflow", h2_style))
    algo_text = (
        "Algorithm 1: Two-Stage Canine Identification and Logging\n"
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
        "                prediction_id=prediction_id)"
    )
    t_algo = Table([[Preformatted(algo_text, code_style)]], colWidths=[515])
    t_algo.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F8F9FA")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#D1D5DB")),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_algo)

    story.append(PageBreak())

    # =========================================================================
    # CHAPTER 5 – MODEL DEVELOPMENT AND WEB APPLICATION
    # =========================================================================
    story.append(Paragraph("Chapter 5 – Model Development and Web Application", h1_style))
    
    story.append(Paragraph("Development Environment", h2_style))
    story.append(Paragraph("The software was developed and validated under Microsoft Windows 11 (64-bit), utilizing Python 3.13 / 3.11, TensorFlow 2.21.0, Flask 3.0.0, and MySQL Server 8.0.", body_style))

    story.append(Paragraph("Model Training", h2_style))
    story.append(Paragraph("Training hyperparameters across both phases are summarized below:", body_style))

    # Table 5.1
    story.append(Paragraph("<b>Table 5.1: Model Training Hyperparameter Configuration</b>", caption_style))
    cfg_headers = [Paragraph("Hyperparameter / Parameter", tbl_header_style), Paragraph("Phase 1: Feature Extraction", tbl_header_style), Paragraph("Phase 2: Fine-Tuning", tbl_header_style)]
    cfg_data = [
        cfg_headers,
        [Paragraph("Base Model Layers", tbl_cell_bold), Paragraph("155 layers (Frozen)", tbl_cell_style), Paragraph("Top 30 layers Unfrozen (125 Frozen)", tbl_cell_style)],
        [Paragraph("Trainable Parameters", tbl_cell_bold), Paragraph("153,720 parameters", tbl_cell_style), Paragraph("1,212,504 parameters", tbl_cell_style)],
        [Paragraph("Non-Trainable Parameters", tbl_cell_bold), Paragraph("2,257,984 parameters", tbl_cell_style), Paragraph("1,199,200 parameters", tbl_cell_style)],
        [Paragraph("Batch Size", tbl_cell_bold), Paragraph("32", tbl_cell_center), Paragraph("32", tbl_cell_center)],
        [Paragraph("Optimizer", tbl_cell_bold), Paragraph("Adam (beta1=0.9, beta2=0.999)", tbl_cell_style), Paragraph("Adam (beta1=0.9, beta2=0.999)", tbl_cell_style)],
        [Paragraph("Initial Learning Rate", tbl_cell_bold), Paragraph("1e-3 (0.001)", tbl_cell_center), Paragraph("1e-5 (0.00001)", tbl_cell_center)],
        [Paragraph("Loss Function", tbl_cell_bold), Paragraph("Categorical Cross-Entropy", tbl_cell_style), Paragraph("Categorical Cross-Entropy", tbl_cell_style)],
        [Paragraph("Epochs Executed", tbl_cell_bold), Paragraph("10 epochs", tbl_cell_center), Paragraph("5 epochs (EarlyStopping trigger)", tbl_cell_center)],
        [Paragraph("Regularization", tbl_cell_bold), Paragraph("Dropout (30%) + Augmentation", tbl_cell_style), Paragraph("Dropout (30%) + Augmentation", tbl_cell_style)],
        [Paragraph("Callbacks Active", tbl_cell_bold), Paragraph("ModelCheckpoint, ReduceLROnPlateau", tbl_cell_style), Paragraph("EarlyStopping, ModelCheckpoint", tbl_cell_style)]
    ]
    t_cfg = Table(cfg_data, colWidths=[150, 180, 185])
    t_cfg.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_header_bg),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('TOPPADDING', (0,0), (-1,-1), 2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_alt_row])
    ]))
    story.append(t_cfg)

    story.append(Paragraph("Model Integration", h2_style))
    story.append(Paragraph("In app.py, the trained model model/best_model.keras is loaded once during server initialization using tf.keras.models.load_model(). The model instance is cached in memory, eliminating per-request loading latency and enabling immediate inference for concurrent user requests.", body_style))

    story.append(Paragraph("Flask Application Architecture", h2_style))
    story.append(Paragraph("The backend application (app.py) follows modular WSGI design principles, serving routes for drag-and-drop image prediction, 120-breed directory lookups, user history, trait comparison, and administrative control.", body_style))

    # Table 5.3 Tech Stack
    story.append(Paragraph("<b>Table 5.3: Core Software Technologies and Functional Roles</b>", caption_style))
    tech_headers = [Paragraph("Technology", tbl_header_style), Paragraph("Version / Category", tbl_header_style), Paragraph("Functional Role in Project", tbl_header_style)]
    tech_data = [
        tech_headers,
        [Paragraph("Python", tbl_cell_bold), Paragraph("3.13 / 3.11", tbl_cell_center), Paragraph("Primary programming language across ML pipeline and backend", tbl_cell_style)],
        [Paragraph("TensorFlow / Keras", tbl_cell_bold), Paragraph("2.21.0", tbl_cell_center), Paragraph("Model training, transfer learning, fine-tuning, and inference", tbl_cell_style)],
        [Paragraph("MobileNetV2", tbl_cell_bold), Paragraph("ImageNet Backbone", tbl_cell_center), Paragraph("Convolutional feature extractor for Stage 1 and Stage 2", tbl_cell_style)],
        [Paragraph("Flask", tbl_cell_bold), Paragraph("3.0.0", tbl_cell_center), Paragraph("Backend WSGI web framework, session management, and REST APIs", tbl_cell_style)],
        [Paragraph("MySQL & Connector", tbl_cell_bold), Paragraph("8.0 Server / Connector", tbl_cell_center), Paragraph("Relational persistence for user accounts, history, and feedback", tbl_cell_style)],
        [Paragraph("ReportLab", tbl_cell_bold), Paragraph("5.1.0", tbl_cell_center), Paragraph("Academic PDF prediction report generation engine", tbl_cell_style)],
        [Paragraph("Chart.js & Matplotlib", tbl_cell_bold), Paragraph("4.4.0 / 3.9.0", tbl_cell_center), Paragraph("Interactive web analytics and static publication charts", tbl_cell_style)]
    ]
    t_tech = Table(tech_data, colWidths=[120, 115, 280])
    t_tech.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_header_bg),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('TOPPADDING', (0,0), (-1,-1), 2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_alt_row])
    ]))
    story.append(t_tech)

    story.append(Paragraph("Image Upload and Prediction", h2_style))
    story.append(Paragraph("The front-end interface provides a clean, responsive drag-and-drop drop zone. Once an image is selected, client-side JavaScript generates an immediate local preview with dimensions. Clicking Predict Breed triggers an asynchronous fetch() POST request. If Stage 1 detects a non-dog, a warning card is shown; if verified as a dog, the primary breed match, confidence percentage, and animated Top-3 probability bars appear smoothly.", body_style))

    story.append(Paragraph("User Authentication", h2_style))
    story.append(Paragraph("User security is implemented using Werkzeug's cryptographic PBKDF2/SHA-256 password hashing. Passwords are never stored in plaintext. Secure session cookies track user identity across requests. Two custom Python decorators enforce route protection: @login_required (redirects unauthenticated users to /login) and @admin_required (restricts administrative routes to users with is_admin = 1, returning HTTP 403 Forbidden to regular users).", body_style))

    story.append(Paragraph("Breed Information and Trait Comparison", h2_style))
    story.append(Paragraph("To provide educational value beyond raw predictions, we curated a comprehensive JSON database (database/breeds_data.json) covering all 120 breeds. Each breed entry includes origin, size, typical lifespan, temperament tags, and physical descriptions. Users can select any two breeds for side-by-side comparison across height, weight, activity level, and care requirements.", body_style))

    story.append(Paragraph("Prediction History", h2_style))
    story.append(Paragraph("Every successful prediction is recorded in MySQL. Authenticated users can visit /history to review their previous uploads, examine past confidence scores, and re-download prediction reports. Guests can also view recent session predictions.", body_style))

    story.append(Paragraph("Database Design", h2_style))
    story.append(Paragraph("The relational database dog_breed_db maintains four normalized tables:", body_style))

    # Table 5.2
    story.append(Paragraph("<b>Table 5.2: Relational Database Schema Design (dog_breed_db)</b>", caption_style))
    db_headers = [Paragraph("Table Name", tbl_header_style), Paragraph("Primary Key", tbl_header_style), Paragraph("Foreign Keys", tbl_header_style), Paragraph("Key Attributes Stored", tbl_header_style)]
    db_data = [
        db_headers,
        [Paragraph("users", tbl_cell_bold), Paragraph("user_id (INT)", tbl_cell_center), Paragraph("None", tbl_cell_center), Paragraph("username, email, password_hash, is_admin, created_at", tbl_cell_style)],
        [Paragraph("prediction_history", tbl_cell_bold), Paragraph("prediction_id (INT)", tbl_cell_center), Paragraph("user_id -> users(user_id)", tbl_cell_style), Paragraph("image_path, predicted_breed, confidence, top3_results (JSON), model_version, created_at", tbl_cell_style)],
        [Paragraph("favorite_breeds", tbl_cell_bold), Paragraph("favorite_id (INT)", tbl_cell_center), Paragraph("user_id -> users(user_id)", tbl_cell_style), Paragraph("breed_name, created_at (Unique compound: user_id, breed_name)", tbl_cell_style)],
        [Paragraph("feedback", tbl_cell_bold), Paragraph("feedback_id (INT)", tbl_cell_center), Paragraph("user_id -> users(user_id)", tbl_cell_style), Paragraph("rating (1–5), message (TEXT), created_at", tbl_cell_style)]
    ]
    t_db = Table(db_data, colWidths=[95, 90, 115, 215])
    t_db.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_header_bg),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('TOPPADDING', (0,0), (-1,-1), 2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_alt_row])
    ]))
    story.append(t_db)

    story.append(Paragraph("Other Implemented Features", h2_style))
    story.append(Paragraph("• ReportLab PDF Report Generation: Produces a standardized, academic prediction report containing the project title, uploaded photograph, primary match, confidence score, Top-3 candidate breakdown, model version, timestamp, and a scientific machine learning disclaimer.<br/>"
                           "• Star Rating Feedback System: Allows users to submit 1-to-5 star ratings and comments stored directly in MySQL.<br/>"
                           "• Admin Analytics Dashboard: Calculates live SQL metrics (total users, total predictions, average confidence, total feedback) and visualizes the top 10 most frequently identified breeds using a Chart.js horizontal bar chart.", body_style))

    add_img("model/report_assets/admin_dashboard.png", "Figure 5.1: Administrative Dashboard Interface Displaying Real-Time Database Metrics and Top Breeds", max_w=400, max_h=190)

    story.append(PageBreak())

    # =========================================================================
    # CHAPTER 6 – RESULTS AND DISCUSSION
    # =========================================================================
    story.append(Paragraph("Chapter 6 – Results and Discussion", h1_style))
    
    story.append(Paragraph("Training and Validation Performance", h2_style))
    story.append(Paragraph("Training proceeded smoothly across 15 epochs without gradient instability. In Phase 1 (frozen base), the newly attached classification head learned decision boundaries rapidly: Epoch 1 attained 31.2% train / 48.5% val accuracy (loss 2.124); Epoch 5 reached 72.1% train / 73.6% val accuracy (loss 0.985); Epoch 10 reached 86.4% train / 79.8% val accuracy (loss 0.742). In Phase 2, fine-tuning the top 30 layers increased training accuracy to 92.3%, validation accuracy to 82.4%, and lowered validation loss to 0.661.", body_style))

    add_img("model/report_assets/training_curves.png", "Figure 6.1: Training and Validation Accuracy and Loss Curves Across 15 Epochs", max_w=470, max_h=190)

    story.append(Paragraph("Accuracy and Loss", h2_style))
    story.append(Paragraph("The smooth decrease in validation loss across both phases confirmed that our learning rate reduction strategy (1e-3 down to 1e-5) and 30% dropout regularization successfully prevented severe memorization on the 7,155 training images.", body_style))

    story.append(Paragraph("Top-1 and Top-5 Accuracy", h2_style))
    story.append(Paragraph("The fine-tuned model was evaluated on the 1,534 held-out test images that were never seen during training or validation:", body_style))

    # Table 6.1
    story.append(Paragraph("<b>Table 6.1: Model Performance Metrics on Held-Out Test Set (1,534 Images)</b>", caption_style))
    met_headers = [Paragraph("Evaluation Metric", tbl_header_style), Paragraph("Measured Value", tbl_header_style), Paragraph("Operational Interpretation", tbl_header_style)]
    met_rows = [
        met_headers,
        [Paragraph("Top-1 Test Accuracy", tbl_cell_bold), Paragraph("77.64%", tbl_cell_bold_center), Paragraph("Exact ground-truth breed match on held-out test images", tbl_cell_style)],
        [Paragraph("Top-5 Test Accuracy", tbl_cell_bold), Paragraph("96.87%", tbl_cell_bold_center), Paragraph("Correct breed present within model's top 5 candidates", tbl_cell_style)],
        [Paragraph("Test Categorical Cross-Entropy Loss", tbl_cell_bold), Paragraph("0.7036", tbl_cell_center), Paragraph("Cross-entropy loss on unaugmented test images", tbl_cell_style)],
        [Paragraph("Macro Average Precision", tbl_cell_bold), Paragraph("78.58%", tbl_cell_center), Paragraph("Unweighted mean precision across all 120 categories", tbl_cell_style)],
        [Paragraph("Macro Average Recall", tbl_cell_bold), Paragraph("76.98%", tbl_cell_center), Paragraph("Unweighted mean recall across all 120 categories", tbl_cell_style)],
        [Paragraph("Macro Average F1-Score", tbl_cell_bold), Paragraph("76.91%", tbl_cell_center), Paragraph("Harmonic mean of macro precision and recall", tbl_cell_style)],
        [Paragraph("Weighted Average Precision", tbl_cell_bold), Paragraph("78.75%", tbl_cell_center), Paragraph("Support-weighted precision reflecting class sample sizes", tbl_cell_style)],
        [Paragraph("Weighted Average Recall", tbl_cell_bold), Paragraph("77.64%", tbl_cell_center), Paragraph("Support-weighted recall matching overall accuracy", tbl_cell_style)],
        [Paragraph("Weighted Average F1-Score", tbl_cell_bold), Paragraph("77.35%", tbl_cell_center), Paragraph("Support-weighted harmonic mean across all test samples", tbl_cell_style)]
    ]
    t_met = Table(met_rows, colWidths=[140, 95, 280])
    t_met.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_header_bg),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('TOPPADDING', (0,0), (-1,-1), 2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BACKGROUND', (0,1), (-1,2), colors.HexColor("#FEF9E7")),
        ('ROWBACKGROUNDS', (0,3), (-1,-1), [colors.white, c_alt_row])
    ]))
    story.append(t_met)

    story.append(Paragraph("The Top-5 accuracy of 96.87% is especially meaningful for practical canine identification: in almost 97 out of 100 cases, the correct breed is present among the top 5 candidates ranked by the model.", body_style))

    story.append(Paragraph("Precision, Recall and F1-Score", h2_style))
    story.append(Paragraph("Examining individual breed performance showed strong discriminative power across the majority of breeds: top-performing breeds with 100% precision, recall, and F1 included African Hunting Dog, Keeshond, Papillon, and Bloodhound. Challenging breeds with lower F1 scores included Italian Greyhound (54.1%), Kuvasz (53.3%), and Cardigan Welsh Corgi (52.6%).", body_style))

    story.append(Paragraph("Prediction Examples", h2_style))
    story.append(Paragraph("Evaluating test images showed robust inference: an input Labrador Retriever photo (dog.jpg) was classified as Labrador Retriever with 69.34% confidence (#2: Golden Retriever 9.37%, #3: Chesapeake Bay Retriever 8.08%). A Siberian Husky image (doog1.jpg) was correctly identified with 98.7% canine probability in Stage 1 and high breed confidence in Stage 2.", body_style))

    story.append(Paragraph("Dog and Non-Dog Image Testing", h2_style))
    story.append(Paragraph("Stage 1 was validated against positive dog images and negative non-canine controls. Dog photos produced canine probabilities > 88%, passing cleanly into Stage 2. Negative controls (horse photo Black-Horse-Names-with-Meanings.jpeg, vehicles, landscapes) produced canine probabilities < 0.02 and were halted with 'No Dog Detected'.", body_style))

    story.append(Paragraph("Commonly Confused Breeds", h2_style))
    story.append(Paragraph("The confusion matrix revealed 12 prominent pairs of confused dog breeds. In all cases, confusion is biologically justified by identical coat textures, ancestral lineages, or anatomical silhouettes:", body_style))

    add_img("model/report_assets/confused_breeds_chart.png", "Figure 6.2: Top 12 Most Frequently Confused Dog Breed Pairs in Evaluation Set", max_w=470, max_h=190)

    # Table 6.2
    story.append(Paragraph("<b>Table 6.2: Top 12 Most Frequently Confused Dog Breed Pairs with Visual Reasons</b>", caption_style))
    conf_headers = [Paragraph("No.", tbl_header_style), Paragraph("Actual Breed", tbl_header_style), Paragraph("Predicted Breed", tbl_header_style), Paragraph("Count", tbl_header_style), Paragraph("Visual Similarity Reason", tbl_header_style)]
    conf_data = [
        conf_headers,
        [Paragraph("1", tbl_cell_center), Paragraph("Whippet", tbl_cell_bold), Paragraph("Italian Greyhound", tbl_cell_style), Paragraph("7 images", tbl_cell_center), Paragraph("Identical slender sighthound posture and sleek coat", tbl_cell_style)],
        [Paragraph("2", tbl_cell_center), Paragraph("Lhasa Apso", tbl_cell_bold), Paragraph("Shih-Tzu", tbl_cell_style), Paragraph("6 images", tbl_cell_center), Paragraph("Closely related Tibetan companion dogs with long facial fur", tbl_cell_style)],
        [Paragraph("3", tbl_cell_center), Paragraph("Eskimo Dog", tbl_cell_bold), Paragraph("Siberian Husky", tbl_cell_style), Paragraph("5 images", tbl_cell_center), Paragraph("Arctic spitz breeds with erect ears, double coats, curled tails", tbl_cell_style)],
        [Paragraph("4", tbl_cell_center), Paragraph("Australian Terrier", tbl_cell_bold), Paragraph("Silky Terrier", tbl_cell_style), Paragraph("4 images", tbl_cell_center), Paragraph("Related terrier types sharing wiry/silky coats and silhouettes", tbl_cell_style)],
        [Paragraph("5", tbl_cell_center), Paragraph("Kuvasz", tbl_cell_bold), Paragraph("Great Pyrenees", tbl_cell_style), Paragraph("4 images", tbl_cell_center), Paragraph("Large flock-guarding breeds with solid white double coats", tbl_cell_style)],
        [Paragraph("6", tbl_cell_center), Paragraph("Maltese Dog", tbl_cell_bold), Paragraph("West Highland White Terrier", tbl_cell_style), Paragraph("4 images", tbl_cell_center), Paragraph("Similar fine-grained facial features, fur texture, and white color", tbl_cell_style)],
        [Paragraph("7", tbl_cell_center), Paragraph("Samoyed", tbl_cell_bold), Paragraph("Great Pyrenees", tbl_cell_style), Paragraph("4 images", tbl_cell_center), Paragraph("Large breeds sharing solid white, fluffy double coats", tbl_cell_style)],
        [Paragraph("8", tbl_cell_center), Paragraph("Staffordshire Bull Terrier", tbl_cell_bold), Paragraph("American Staffordshire Terrier", tbl_cell_style), Paragraph("4 images", tbl_cell_center), Paragraph("Closely related bully breeds sharing blocky heads and muscular frames", tbl_cell_style)],
        [Paragraph("9", tbl_cell_center), Paragraph("Cardigan Welsh Corgi", tbl_cell_bold), Paragraph("Pembroke Welsh Corgi", tbl_cell_style), Paragraph("3 images", tbl_cell_center), Paragraph("Both Welsh Corgi breeds, differing primarily in tail length", tbl_cell_style)],
        [Paragraph("10", tbl_cell_center), Paragraph("Collie", tbl_cell_bold), Paragraph("Shetland Sheepdog", tbl_cell_style), Paragraph("3 images", tbl_cell_center), Paragraph("Herding breeds sharing identical facial markings and long ruffs", tbl_cell_style)],
        [Paragraph("11", tbl_cell_center), Paragraph("Irish Wolfhound", tbl_cell_bold), Paragraph("Scottish Deerhound", tbl_cell_style), Paragraph("3 images", tbl_cell_center), Paragraph("Similar rough-coated wiry body structure and sighthound build", tbl_cell_style)],
        [Paragraph("12", tbl_cell_center), Paragraph("Lakeland Terrier", tbl_cell_bold), Paragraph("Soft-Coated Wheaten Terrier", tbl_cell_style), Paragraph("3 images", tbl_cell_center), Paragraph("Similar tan/wheaten coat colors and bearded facial profiles", tbl_cell_style)]
    ]
    t_conf = Table(conf_data, colWidths=[25, 120, 130, 55, 185])
    t_conf.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_header_bg),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('TOPPADDING', (0,0), (-1,-1), 2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_alt_row])
    ]))
    story.append(t_conf)

    story.append(Paragraph("Application Testing", h2_style))
    story.append(Paragraph("To confirm end-to-end software stability, all 18 subsystems were validated via run_complete_tests.py. All 18 tests passed with a 100% success rate:", body_style))

    # Table 6.3
    story.append(Paragraph("<b>Table 6.3: Complete 18-Point Automated Application Test Suite Verification</b>", caption_style))
    test_headers = [Paragraph("Test ID", tbl_header_style), Paragraph("Subsystem", tbl_header_style), Paragraph("Expected Behavior", tbl_header_style), Paragraph("Actual Measured Outcome", tbl_header_style), Paragraph("Status", tbl_header_style)]
    test_data = [
        test_headers,
        [Paragraph("TC-01", tbl_cell_bold_center), Paragraph("Flask Startup", tbl_cell_style), Paragraph("Initializes cleanly with secret key", tbl_cell_style), Paragraph("App initialized; secret key verified", tbl_cell_style), Paragraph("PASS", tbl_cell_bold_center)],
        [Paragraph("TC-02", tbl_cell_bold_center), Paragraph("Homepage Navigation", tbl_cell_style), Paragraph("HTTP 200 on /; renders navbar links", tbl_cell_style), Paragraph("Status 200; Navigation links present", tbl_cell_style), Paragraph("PASS", tbl_cell_bold_center)],
        [Paragraph("TC-03", tbl_cell_bold_center), Paragraph("Image Upload", tbl_cell_style), Paragraph("Multipart POST saves image", tbl_cell_style), Paragraph("Status 200; Saved to uploads/", tbl_cell_style), Paragraph("PASS", tbl_cell_bold_center)],
        [Paragraph("TC-04", tbl_cell_bold_center), Paragraph("Invalid Image Handling", tbl_cell_style), Paragraph("Rejects bad format & corrupted files", tbl_cell_style), Paragraph("Proper error messages returned", tbl_cell_style), Paragraph("PASS", tbl_cell_bold_center)],
        [Paragraph("TC-05", tbl_cell_bold_center), Paragraph("Canine Validation", tbl_cell_style), Paragraph("Blocks non-dogs; accepts dogs", tbl_cell_style), Paragraph("Horse rejected; Dog accepted", tbl_cell_style), Paragraph("PASS", tbl_cell_bold_center)],
        [Paragraph("TC-06", tbl_cell_bold_center), Paragraph("Model Loading", tbl_cell_style), Paragraph("MobileNetV2 loaded (224, 224, 3)", tbl_cell_style), Paragraph("Input (224, 224, 3); 120 classes", tbl_cell_style), Paragraph("PASS", tbl_cell_bold_center)],
        [Paragraph("TC-07", tbl_cell_bold_center), Paragraph("Breed Prediction", tbl_cell_style), Paragraph("Returns valid breed and confidence", tbl_cell_style), Paragraph("Predicted Labrador (69.34%)", tbl_cell_style), Paragraph("PASS", tbl_cell_bold_center)],
        [Paragraph("TC-08", tbl_cell_bold_center), Paragraph("Top-3 Ranked Scores", tbl_cell_style), Paragraph("Exactly 3 breeds sorted descending", tbl_cell_style), Paragraph("Scores: #1 69.3%, #2 9.4%, #3 8.1%", tbl_cell_style), Paragraph("PASS", tbl_cell_bold_center)],
        [Paragraph("TC-09", tbl_cell_bold_center), Paragraph("MySQL Connection", tbl_cell_style), Paragraph("Connects to dog_breed_db; 4 tables", tbl_cell_style), Paragraph("Connected; all 4 tables verified", tbl_cell_style), Paragraph("PASS", tbl_cell_bold_center)],
        [Paragraph("TC-10", tbl_cell_bold_center), Paragraph("Signup & Login", tbl_cell_style), Paragraph("Creates user, hashes password", tbl_cell_style), Paragraph("Signup OK; session created; logout OK", tbl_cell_style), Paragraph("PASS", tbl_cell_bold_center)],
        [Paragraph("TC-11", tbl_cell_bold_center), Paragraph("Prediction History", tbl_cell_style), Paragraph("Restricts unauthenticated users", tbl_cell_style), Paragraph("Guest -> 302; Authenticated -> 200", tbl_cell_style), Paragraph("PASS", tbl_cell_bold_center)],
        [Paragraph("TC-12", tbl_cell_bold_center), Paragraph("Favorite Breeds", tbl_cell_style), Paragraph("AJAX toggle bookmarks breed", tbl_cell_style), Paragraph("Bookmark added & removed correctly", tbl_cell_style), Paragraph("PASS", tbl_cell_bold_center)],
        [Paragraph("TC-13", tbl_cell_bold_center), Paragraph("Breed Directory", tbl_cell_style), Paragraph("/breeds renders 120 breeds", tbl_cell_style), Paragraph("Status 200; 120 breeds loaded", tbl_cell_style), Paragraph("PASS", tbl_cell_bold_center)],
        [Paragraph("TC-14", tbl_cell_bold_center), Paragraph("Breed Comparison", tbl_cell_style), Paragraph("Verifies comparison selectors", tbl_cell_style), Paragraph("Side-by-side attributes verified", tbl_cell_style), Paragraph("PASS", tbl_cell_bold_center)],
        [Paragraph("TC-15", tbl_cell_bold_center), Paragraph("Performance Charts", tbl_cell_style), Paragraph("Returns accuracy and confusion data", tbl_cell_style), Paragraph("Status 200; 77.64% test accuracy", tbl_cell_style), Paragraph("PASS", tbl_cell_bold_center)],
        [Paragraph("TC-16", tbl_cell_bold_center), Paragraph("PDF Report Download", tbl_cell_style), Paragraph("Streams valid PDF binary", tbl_cell_style), Paragraph("Status 200; Mime: application/pdf", tbl_cell_style), Paragraph("PASS", tbl_cell_bold_center)],
        [Paragraph("TC-17", tbl_cell_bold_center), Paragraph("Admin Access Control", tbl_cell_style), Paragraph("Enforces RBAC on /admin", tbl_cell_style), Paragraph("Guest -> 302; User -> 403; Admin -> 200", tbl_cell_style), Paragraph("PASS", tbl_cell_bold_center)],
        [Paragraph("TC-18", tbl_cell_bold_center), Paragraph("Responsive Design", tbl_cell_style), Paragraph("Viewport meta tag & media queries", tbl_cell_style), Paragraph("Breakpoints (480, 600, 768, 900px)", tbl_cell_style), Paragraph("PASS", tbl_cell_bold_center)]
    ]
    t_test = Table(test_data, colWidths=[40, 95, 140, 195, 45])
    t_test.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_header_bg),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('TOPPADDING', (0,0), (-1,-1), 2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_alt_row]),
        ('TEXTCOLOR', (4,1), (4,-1), colors.HexColor("#1E7E34")),
    ]))
    story.append(t_test)

    story.append(Paragraph("Observations", h2_style))
    story.append(Paragraph("• Inference Latency: On standard consumer CPU hardware, a single prediction forward pass (preprocessing, Stage 1 check, Stage 2 prediction, and database insertion) takes 120 to 160 milliseconds, well within the 500 ms benchmark for interactive web responsiveness.<br/>"
                           "• Memory Footprint: MobileNetV2 requires only ~14 MB of disk storage and minimal RAM, enabling rapid application startup and stable hosting on lightweight server environments.", body_style))

    story.append(PageBreak())

    # =========================================================================
    # CHAPTER 7 – CONCLUSION AND FUTURE ENHANCEMENTS
    # =========================================================================
    story.append(Paragraph("Chapter 7 – Conclusion and Future Enhancements", h1_style))
    
    story.append(Paragraph("Project Summary", h2_style))
    story.append(Paragraph("In this B.Tech capstone project, we designed, developed, and deployed an end-to-end canine breed identification platform using transfer learning with MobileNetV2 and full-stack web engineering. Our work demonstrates that lightweight convolutional networks can achieve high diagnostic performance in complex fine-grained visual classification tasks while maintaining low computational latency.", body_style))
    story.append(Paragraph("Key accomplishments of the project include:<br/>"
                           "1. <b>Architected a Two-Stage Pipeline:</b> Introduced an upstream ImageNet canine presence filter that prevents non-dog uploads from receiving false dog breed predictions.<br/>"
                           "2. <b>Attained Strong Academic Accuracy:</b> Achieved 77.64% Top-1 test accuracy and 96.87% Top-5 test accuracy across 120 breeds on 1,534 held-out evaluation images.<br/>"
                           "3. <b>Engineered a Full-Stack Web Platform:</b> Implemented a secure Flask application with MySQL database persistence, PBKDF2 password hashing, role-based access control, and dynamic PDF prediction report compilation.<br/>"
                           "4. <b>Delivered Rich User Features:</b> Integrated a 120-breed interactive directory, side-by-side trait comparison, individual prediction history tracking, user feedback, and an administrative dashboard.<br/>"
                           "5. <b>Validated Reliability:</b> Executed an automated 18-point verification testing suite with a 100% pass rate.", body_style))

    story.append(Paragraph("Learning Outcomes", h2_style))
    story.append(Paragraph("Through the development of this project, our team acquired valuable engineering experience:<br/>"
                           "• Practical understanding of deep transfer learning, inverted residual bottlenecks, and the delicate balance required during two-phase fine-tuning.<br/>"
                           "• Experience with dataset splitting strategies, data augmentation, and handling fine-grained visual classification challenges.<br/>"
                           "• Full-stack web engineering skills connecting deep learning models to Flask web applications and MySQL databases.<br/>"
                           "• Automated testing practices to ensure software stability across database transactions, session cookies, and API endpoints.", body_style))

    story.append(Paragraph("Limitations", h2_style))
    story.append(Paragraph("The system exhibits three practical limitations:<br/>"
                           "1. <b>Resolution Downscaling:</b> Resizing images to 224 × 224 pixels inevitably discards micro-level textures (such as fine fur whisker curls) that could help differentiate closely related terrier varieties.<br/>"
                           "2. <b>Single-Subject Assumption:</b> The model assumes that a single primary canine is centered in the photograph. If multiple dogs appear together, their feature maps blend, leading to lower prediction confidence.<br/>"
                           "3. <b>Absence of Physical Scale Reference:</b> In a 2D photograph lacking reference objects, an Italian Greyhound (weighing 4 kg) looks identical in proportions to a Whippet (weighing 13 kg). Without physical scale measurements, 2D CNNs cannot exploit size differences.", body_style))

    story.append(Paragraph("Future Improvements", h2_style))
    story.append(Paragraph("Several promising directions exist for future enhancement:<br/>"
                           "1. <b>Upstream Object Detection & Bounding Box Localization:</b> Incorporating a lightweight YOLOv8 detector to crop the canine body from cluttered backgrounds before classification.<br/>"
                           "2. <b>Mobile Edge Deployment:</b> Quantizing the trained MobileNetV2 model to TensorFlow Lite (TFLite) or ONNX format for on-device inference on Android and iOS devices without requiring internet connectivity.<br/>"
                           "3. <b>Vision Transformers (ViT) & Attention Mechanisms:</b> Exploring part-attention networks to explicitly focus convolutional attention on diagnostic anatomical regions (ears, snout, tail posture).<br/>"
                           "4. <b>Mixed-Breed Percentage Estimation:</b> Expanding the classification head to estimate breed composition percentages for mixed-breed dogs.", body_style))

    story.append(PageBreak())

    # =========================================================================
    # REFERENCES
    # =========================================================================
    story.append(Paragraph("References", h1_style))
    refs = [
        "1. S. Selvaraj, R. Thangarajan, S. Anbukkarasi, and S. Yuvan Prasad, \"ResNet50 Architecture Based Dog Breed Identification Using Deep Learning,\" in <i>Proc. Int. Conf. on Computational Intelligence and Knowledge Economy</i>, 2023.",
        "2. P. Borwarnginn, W. Kusakunniran, S. Karnjanapreechakorn, and K. Thongkanchorn, \"Knowing Your Dog Breed: Identifying a Dog Breed with Deep Learning,\" in <i>Proc. Int. Conf. on Information Technology</i>, 2021.",
        "3. S. A. Bokhari, P. Mukherjee, A. S. Singh, S. Shaik, and J. K. Mathew, \"Convolutional Neural Network Based Dog Breed Classification,\" in <i>Proc. Int. Conf. on Innovative Computing and Communication</i>, 2022.",
        "4. T. Kumaravel, P. Natesan, V. E. Sathishkumar, S. S. N, S. G, and U. V, \"Automatic Dog Breed Classification Using Deep Learning,\" in <i>Proc. Int. Conf. on Smart Systems and Inventive Technology</i>, 2023.",
        "5. N. Banakar, Raghavendra B. U., S. G. S., T. K. Vani, and V. M. Vishnu, \"Dog Breed Identification Using Deep Learning,\" <i>International Journal of Advanced Research in Computer Science and Software Engineering</i>, vol. 13, no. 5, 2023.",
        "6. B. Valarmathi, N. S. Gupta, G. Prakash, R. H. Reddy, S. Saravanan, and P. Shanmugasundaram, \"Hybrid Deep Learning Algorithms for Dog Breed Identification—A Comparative Analysis,\" <i>IEEE Access</i>, vol. 11, pp. 45120–45132, 2023.",
        "7. S. R. Basha, I. Ganesh, G. R. Reddy, and A. Hans, \"Dogs Breed Classification Using Deep Learning,\" in <i>Proc. Int. Conf. on Artificial Intelligence and Smart Systems</i>, 2021.",
        "8. S. S. Hussain, K. S. R. Murthy, C. S. Rani, T. Nanuvala, C. R. Kumar, and G. Sathar, \"Automated Dog Breed Recognition Using CNN-Based Transfer Learning,\" in <i>Proc. Int. Conf. on Advances in Computer Engineering & Communication Systems</i>, 2025.",
        "9. A. S. Ghotra, H. Kour, A. Hasan, and A. Khan, \"Dog Breed Identification,\" in <i>Proc. Int. Conf. on Data Science and Machine Learning</i>, 2023.",
        "10. J. Bankar, A. Nalawade, S. Wali, A. Rane, and H. Matlani, \"AI Based Dog Breed Prediction Model and Virtual Canine Hub,\" <i>International Journal of Computer Applications</i>, vol. 186, no. 14, 2025.",
        "11. D.-N. Zou, S.-H. Zhang, T.-J. Mu, and M. Zhang, \"A New Dataset of Dog Breed Images and a Benchmark for Fine-Grained Classification,\" <i>Computational Visual Media</i>, vol. 6, no. 4, pp. 477–487, 2020.",
        "12. P. Perera and V. M. Patel, \"Deep Transfer Learning for Multiple Class Novelty Detection,\" in <i>Proc. IEEE/CVF Conf. on Computer Vision and Pattern Recognition (CVPR)</i>, 2019, pp. 1154–1162.",
        "13. A. Khosla, N. Jayadevaprakash, B. Yao, and L. Fei-Fei, \"Novel Dataset for Fine-Grained Image Categorization: Stanford Dogs,\" in <i>Proc. CVPR Workshop on Fine-Grained Visual Categorization</i>, 2011.",
        "14. M. Sandler, A. Howard, M. Zhu, A. Zhmoginov, and L.-C. Chen, \"MobileNetV2: Inverted Residuals and Linear Bottlenecks,\" in <i>Proc. IEEE/CVF Conf. on Computer Vision and Pattern Recognition (CVPR)</i>, 2018, pp. 4510–4520.",
        "15. M. Abadi et al., \"TensorFlow: A System for Large-Scale Machine Learning,\" in <i>Proc. 12th USENIX Symp. on Operating Systems Design and Implementation (OSDI)</i>, 2016, pp. 265–283.",
        "16. A. Grinberg, <i>Flask Web Development: Developing Web Applications with Python</i>, 2nd ed. Sebastopol, CA: O'Reilly Media, 2018.",
        "17. ReportLab Europe Ltd., <i>ReportLab PDF Generation User Guide</i>, Version 5.1, London, UK, 2024.",
        "18. Oracle Corporation, <i>MySQL 8.0 Reference Manual</i>, Redwood Shores, CA: Oracle, 2024."
    ]
    ref_style = ParagraphStyle(
        'RefStyle',
        parent=base_styles['Normal'],
        fontName='Times-Roman',
        fontSize=8.5,
        leading=12,
        alignment=TA_LEFT,
        textColor=c_text,
        leftIndent=20,
        firstLineIndent=-20,
        spaceAfter=4
    )
    for r_text in refs:
        story.append(Paragraph(r_text, ref_style))

    story.append(PageBreak())

    # =========================================================================
    # TEAM CONTRIBUTIONS
    # =========================================================================
    story.append(Paragraph("Team Contributions", h1_style))
    story.append(Paragraph("This project was divided into four major areas to ensure that each team member contributed to a specific part of the development process.", body_style))

    story.append(Paragraph("K Goutham Nayak – CS24B1081", h2_style))
    story.append(Paragraph("Backend Architecture, MySQL Database and PDF Reporting", h3_style))
    story.append(Paragraph("• Implemented Flask application routing and asynchronous REST APIs.<br/>"
                           "• Designed the MySQL relational database schema (dog_breed_db) across 4 tables.<br/>"
                           "• Developed password hashing using Werkzeug PBKDF2/SHA-256 and role-based decorators (@login_required, @admin_required).<br/>"
                           "• Built the automated ReportLab PDF prediction report generator.<br/>"
                           "• Configured individual prediction history and favorites management.", body_style))

    story.append(Paragraph("K Adithya – CS24B1091", h2_style))
    story.append(Paragraph("Deep Learning Model Architecture and Fine-Tuning", h3_style))
    story.append(Paragraph("• Implemented MobileNetV2 transfer learning using TensorFlow / Keras.<br/>"
                           "• Configured the two-phase training strategy (Phase 1 frozen feature extraction; Phase 2 top 30 unfrozen fine-tuning).<br/>"
                           "• Applied learning rate scheduling, early stopping, and model checkpointing.<br/>"
                           "• Computed quantitative evaluation metrics (Top-1 77.64%, Top-5 96.87%, test loss 0.7036, macro/weighted F1).<br/>"
                           "• Generated training convergence curves and confusion matrix artifacts.", body_style))

    story.append(Paragraph("R Mahesh Rathod – CS24B1071", h2_style))
    story.append(Paragraph("Two-Stage Canine Presence Detection and Validation", h3_style))
    story.append(Paragraph("• Formulated and implemented the Stage 1 ImageNet canine presence filter.<br/>"
                           "• Mapped 118 domestic and wild canine ImageNet class indices.<br/>"
                           "• Calibrated the cumulative canine probability threshold (P(dog) >= 0.20).<br/>"
                           "• Validated the system against negative non-dog images (horses, vehicles, landscapes).<br/>"
                           "• Conducted error analysis on the 12 most frequently confused dog breed pairs.", body_style))

    story.append(Paragraph("G Vishnu Vardhan – CS24B1028", h2_style))
    story.append(Paragraph("Frontend UI/UX, Breed Directory and Trait Comparison", h3_style))
    story.append(Paragraph("• Designed the responsive HTML5/CSS3 cream-and-brown web interface.<br/>"
                           "• Developed the drag-and-drop file upload logic and image preview in JavaScript.<br/>"
                           "• Built the 120-breed interactive directory with search and size filtering.<br/>"
                           "• Implemented the side-by-side breed trait comparison tool.<br/>"
                           "• Integrated Chart.js for the administrative dashboard and model performance charts.", body_style))

    story.append(Paragraph("Shared Group Responsibilities", h2_style))
    story.append(Paragraph("• Extracted and evaluated methodology and limitations across 12 research papers in the literature survey.<br/>"
                           "• Partitioned the 10,222 images into stratified 70% / 15% / 15% train, validation, and test sets.<br/>"
                           "• Executed and validated all 18 test cases in the automated application test suite (run_complete_tests.py).<br/>"
                           "• Prepared and proofread the comprehensive B.Tech project report.", body_style))

    story.append(Spacer(1, 20))
    story.append(Paragraph("<b>— END OF REPORT —</b>", ParagraphStyle('EndRep', parent=base_styles['Normal'], fontName='Times-Bold', fontSize=10, alignment=TA_CENTER, textColor=c_primary)))

    # Build PDF
    doc.build(story, canvasmaker=AcademicCanvas)
    print(f"[OK] Generated PDF Report: {output_path}")

if __name__ == '__main__':
    create_pdf('Dog_Breed_Identification_Project_Report.pdf')
