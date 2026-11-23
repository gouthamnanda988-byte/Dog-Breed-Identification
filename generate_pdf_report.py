"""
generate_pdf_report.py
======================
Generates a comprehensive, professional academic PDF project report for:
DOG BREED IDENTIFICATION USING DEEP LEARNING AND TRANSFER LEARNING

Features:
- Academic cover page with student details & placeholders
- Running header and page numbering (Page X of Y)
- Professional typography with Times-Roman and Helvetica headers
- Custom styled tables with wrapped cells, alternating rows, and borders
- High-resolution embedded figures with centered captions
"""

import os
from PIL import Image as PILImage
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, 
    Image, PageBreak, KeepTogether, HRFlowable, Preformatted
)
from reportlab.pdfgen import canvas
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT, TA_RIGHT

class NumberedCanvas(canvas.Canvas):
    """Two-pass canvas to dynamically compute and draw 'Page X of Y'."""
    def __init__(self, *args, **kwargs):
        super(NumberedCanvas, self).__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super(NumberedCanvas, self).showPage()
        super(NumberedCanvas, self).save()

    def draw_page_decorations(self, page_count):
        # Suppress header and footer on cover page
        if self._pageNumber == 1:
            return

        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#4A3B32"))
        self.setStrokeColor(colors.HexColor("#D4C3B3"))
        self.setLineWidth(0.6)

        # Running Header
        self.line(40, 841.89 - 36, 595.27 - 40, 841.89 - 36)
        self.drawString(40, 841.89 - 30, "DOG BREED IDENTIFICATION USING DEEP LEARNING AND TRANSFER LEARNING")
        self.drawRightString(595.27 - 40, 841.89 - 30, "B.Tech Final Year Report")

        # Running Footer
        self.line(40, 42, 595.27 - 40, 42)
        self.drawString(40, 30, "Department of Computer Science and Engineering / Data Science")
        page_str = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(595.27 - 40, 30, page_str)
        self.restoreState()


def create_pdf(output_path):
    # Printable area: A4 is 595.27 x 841.89 pt. Margins: L=40, R=40 -> Width = 515.27 pt
    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        leftMargin=40,
        rightMargin=40,
        topMargin=46,
        bottomMargin=48
    )

    story = []
    
    # Styles
    base_styles = getSampleStyleSheet()
    
    # Colors
    c_primary = colors.HexColor("#3E2515")      # Deep rich brown
    c_secondary = colors.HexColor("#5C3A1E")    # Warm brown
    c_accent = colors.HexColor("#6D4828")       # Medium brown
    c_header_bg = colors.HexColor("#F5EBDA")    # Cream table header
    c_alt_row = colors.HexColor("#FFFDF9")      # Off-white table row
    c_border = colors.HexColor("#D4C3B3")       # Crisp table border
    c_text = colors.HexColor("#222222")         # Charcoal body text

    title_style = ParagraphStyle(
        'CoverTitle',
        parent=base_styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=25,
        alignment=TA_CENTER,
        textColor=c_primary,
        spaceAfter=15
    )

    cover_sub_style = ParagraphStyle(
        'CoverSubtitle',
        parent=base_styles['Normal'],
        fontName='Times-Italic',
        fontSize=12,
        leading=16,
        alignment=TA_CENTER,
        textColor=colors.HexColor("#444444"),
        spaceAfter=20
    )

    h1_style = ParagraphStyle(
        'Heading1_Custom',
        parent=base_styles['Normal'],
        fontName='Helvetica-Bold',
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
        fontName='Helvetica-Bold',
        fontSize=11.5,
        leading=15,
        textColor=c_secondary,
        spaceBefore=10,
        spaceAfter=5,
        keepWithNext=True
    )

    h3_style = ParagraphStyle(
        'Heading3_Custom',
        parent=base_styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=13,
        textColor=c_accent,
        spaceBefore=8,
        spaceAfter=3,
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

    body_bold = ParagraphStyle(
        'Body_Bold_Custom',
        parent=body_style,
        fontName='Times-Bold'
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
        fontName='Helvetica-Bold',
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

    def add_img(img_path, caption, max_w=470, max_h=250):
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
    # 1. TITLE / COVER PAGE
    # =========================================================================
    story.append(Spacer(1, 20))
    story.append(Paragraph("DOG BREED IDENTIFICATION USING DEEP LEARNING AND TRANSFER LEARNING", title_style))
    story.append(Paragraph("A Project Report Submitted in Partial Fulfillment of the Requirements<br/>for the Degree of Bachelor of Technology in Data Science / Computer Science and Engineering", cover_sub_style))
    story.append(Spacer(1, 10))
    
    p_by = Paragraph("<b>Submitted by:</b>", ParagraphStyle('SubBy', parent=base_styles['Normal'], fontName='Helvetica-Bold', fontSize=10.5, alignment=TA_CENTER, textColor=c_primary, spaceAfter=6))
    story.append(p_by)

    # Team Table
    team_data = [
        [Paragraph("Candidate Name", tbl_header_style), Paragraph("Roll / Registration Number", tbl_header_style)],
        [Paragraph("K Goutham Nayak", tbl_cell_bold), Paragraph("CS24B1081", tbl_cell_center)],
        [Paragraph("K Adithya", tbl_cell_bold), Paragraph("CS24B1091", tbl_cell_center)],
        [Paragraph("R Mahesh Rathod", tbl_cell_bold), Paragraph("CS24B1071", tbl_cell_center)],
        [Paragraph("G Vishnu Vardhan", tbl_cell_bold), Paragraph("CS24B1028", tbl_cell_center)]
    ]
    t_team = Table(team_data, colWidths=[240, 180])
    t_team.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_header_bg),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_team)

    story.append(Spacer(1, 25))
    story.append(Paragraph("<b>Under the Guidance of:</b>", ParagraphStyle('GuideHead', parent=base_styles['Normal'], fontName='Helvetica-Bold', fontSize=10, alignment=TA_CENTER, textColor=c_primary, spaceAfter=3)))
    story.append(Paragraph("[Faculty Guide Name, Designation]<br/>[Department of Computer Science and Engineering / Data Science]", ParagraphStyle('GuideBody', parent=base_styles['Normal'], fontName='Times-Roman', fontSize=9.5, leading=13, alignment=TA_CENTER, textColor=c_text, spaceAfter=20)))

    story.append(Paragraph("<b>[Department of Computer Science and Engineering / Data Science]<br/>[Institution / College Name, Affiliated to University Name]<br/>[Academic Year: 2025 – 2026]</b>", ParagraphStyle('InstBody', parent=base_styles['Normal'], fontName='Helvetica-Bold', fontSize=10, leading=14, alignment=TA_CENTER, textColor=c_primary)))

    story.append(PageBreak())

    # =========================================================================
    # CERTIFICATE & DECLARATION
    # =========================================================================
    story.append(Paragraph("BONAFIDE CERTIFICATE", h1_style))
    story.append(Paragraph("This is to certify that the project report entitled <b>\"DOG BREED IDENTIFICATION USING DEEP LEARNING AND TRANSFER LEARNING\"</b> is a bonafide work carried out by <b>K Goutham Nayak (CS24B1081), K Adithya (CS24B1091), R Mahesh Rathod (CS24B1071), and G Vishnu Vardhan (CS24B1028)</b> in partial fulfillment of the requirements for the award of the degree of Bachelor of Technology in Computer Science and Engineering / Data Science during the academic year 2025–2026.", body_style))
    story.append(Spacer(1, 30))
    story.append(Paragraph("[Internal Guide Signature]&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[Head of Department Signature]<br/><b>[Guide Name, Designation]</b>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<b>[HOD Name, Department]</b>", body_style))

    story.append(Spacer(1, 20))
    story.append(Paragraph("CANDIDATE DECLARATION", h1_style))
    story.append(Paragraph("We hereby declare that the project entitled <b>\"DOG BREED IDENTIFICATION USING DEEP LEARNING AND TRANSFER LEARNING\"</b> submitted to <b>[Institution Name]</b> is an authentic record of our own research and engineering work carried out under the guidance of <b>[Guide Name]</b>. We confirm that the results embodied in this report have not been submitted to any other university or institute for the award of any degree or diploma.", body_style))
    story.append(Spacer(1, 15))
    story.append(Paragraph("1. K Goutham Nayak (CS24B1081)&nbsp;&nbsp;&nbsp;&nbsp;____________________<br/><br/>"
                           "2. K Adithya (CS24B1091)&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;____________________<br/><br/>"
                           "3. R Mahesh Rathod (CS24B1071)&nbsp;&nbsp;&nbsp;&nbsp;____________________<br/><br/>"
                           "4. G Vishnu Vardhan (CS24B1028)&nbsp;&nbsp;&nbsp;____________________<br/><br/>"
                           "<b>Date:</b> [Date of Submission]<br/><b>Place:</b> [College Location]", body_style))

    story.append(PageBreak())

    # =========================================================================
    # ABSTRACT
    # =========================================================================
    story.append(Paragraph("ABSTRACT", h1_style))
    story.append(Paragraph("Accurately classifying domestic canine breeds from digital photographs represents one of the most prominent fine-grained visual classification challenges in modern computer vision. Unlike generic object recognition where classes differ fundamentally in shape and silhouette (such as vehicles versus animals), canine identification must contend with two difficult phenomena: <b>high intra-class variance</b>, where dogs of the same breed exhibit significant variations in coat patterns, grooming styles, age, and postures, and <b>low inter-class variance</b>, where biologically distinct breeds share nearly indistinguishable anatomical silhouettes and facial profiles (for instance, Whippets and Italian Greyhounds, or Lhasa Apsos and Shih-Tzus).", body_style))
    
    story.append(Paragraph("In this project, we designed, implemented, and thoroughly evaluated an end-to-end canine classification web platform powered by transfer learning with MobileNetV2 and backed by a full-stack relational database. Built upon the Stanford Dogs / Kaggle Dog Breed Identification benchmark comprising <b>10,222 labeled images</b> partitioned into a stratified 70% training (7,155 images), 15% validation (1,533 images), and 15% testing (1,534 images) split across 120 purebred categories, our architecture employs an innovative <b>two-stage prediction pipeline</b>. In Stage 1, an ImageNet-pretrained MobileNetV2 classifier validates canine presence by monitoring 118 domestic and wild dog output indices, immediately rejecting non-dog uploads (such as horses, felines, or inanimate objects) with a friendly alert. In Stage 2, images confirmed as dogs are evaluated by our fine-tuned MobileNetV2 model equipped with Global Average Pooling, 30% dropout regularization, and a 120-unit Softmax classification layer.", body_style))

    story.append(Paragraph("Our model achieved an empirical <b>77.64% Top-1 test accuracy</b>, an exceptional <b>96.87% Top-5 test accuracy</b>, and a test loss of <b>0.7036</b> across the 1,534 held-out evaluation images. Beyond the neural network, we integrated a full-stack Flask web application providing drag-and-drop image prediction with Top-3 ranked candidate scores, a 120-breed interactive directory, side-by-side trait comparison, ReportLab automated PDF prediction report downloads, personal MySQL history tracking, and a role-based administrative analytics dashboard. This platform provides an accessible, robust, and educational solution for veterinary clinics, rescue shelters, and pet owners.", body_style))

    story.append(PageBreak())

    # =========================================================================
    # TABLE OF CONTENTS
    # =========================================================================
    story.append(Paragraph("TABLE OF CONTENTS", h1_style))
    toc_data = [
        [Paragraph("<b>Abstract</b>", tbl_cell_style), Paragraph("<b>iv</b>", tbl_cell_center)],
        [Paragraph("<b>CHAPTER 1 – INTRODUCTION</b>", tbl_cell_bold), Paragraph("<b>1</b>", tbl_cell_bold_center)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;1.1 Background", tbl_cell_style), Paragraph("1", tbl_cell_center)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;1.2 Problem Statement", tbl_cell_style), Paragraph("2", tbl_cell_center)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;1.3 Motivation", tbl_cell_style), Paragraph("2", tbl_cell_center)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;1.4 Project Objectives", tbl_cell_style), Paragraph("3", tbl_cell_center)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;1.5 Scope of the Project", tbl_cell_style), Paragraph("3", tbl_cell_center)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;1.6 Existing System and Proposed System", tbl_cell_style), Paragraph("4", tbl_cell_center)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;1.7 Organization of the Report", tbl_cell_style), Paragraph("5", tbl_cell_center)],
        [Paragraph("<b>CHAPTER 2 – LITERATURE SURVEY</b>", tbl_cell_bold), Paragraph("<b>6</b>", tbl_cell_bold_center)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;2.1 Review of Related Research Papers (12 Papers)", tbl_cell_style), Paragraph("6", tbl_cell_center)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;2.2 Comparative Literature Analysis Table", tbl_cell_style), Paragraph("10", tbl_cell_center)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;2.3 Research Gap Analysis", tbl_cell_style), Paragraph("11", tbl_cell_center)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;2.4 How Proposed Project Addresses Gaps", tbl_cell_style), Paragraph("12", tbl_cell_center)],
        [Paragraph("<b>CHAPTER 3 – DATASET</b>", tbl_cell_bold), Paragraph("<b>13</b>", tbl_cell_bold_center)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;3.1 Dataset Description and Origin", tbl_cell_style), Paragraph("13", tbl_cell_center)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;3.2 Breed Categories and Class Hierarchy", tbl_cell_style), Paragraph("13", tbl_cell_center)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;3.3 Dataset Distribution and Partitioning", tbl_cell_style), Paragraph("14", tbl_cell_center)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;3.4 Image Preprocessing Pipeline", tbl_cell_style), Paragraph("15", tbl_cell_center)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;3.5 Data Augmentation Strategy", tbl_cell_style), Paragraph("15", tbl_cell_center)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;3.6 Dataset Challenges and Observations", tbl_cell_style), Paragraph("16", tbl_cell_center)],
        [Paragraph("<b>CHAPTER 4 – METHODOLOGY</b>", tbl_cell_bold), Paragraph("<b>17</b>", tbl_cell_bold_center)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;4.1 Overall System Architecture", tbl_cell_style), Paragraph("17", tbl_cell_center)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;4.2 Two-Stage Prediction Pipeline", tbl_cell_style), Paragraph("18", tbl_cell_center)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;4.3 CNNs and Transfer Learning", tbl_cell_style), Paragraph("19", tbl_cell_center)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;4.4 Image Preprocessing & Normalization", tbl_cell_style), Paragraph("21", tbl_cell_center)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;4.5 Two-Phase Model Training Procedure", tbl_cell_style), Paragraph("21", tbl_cell_center)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;4.6 Flask Web Application Architecture", tbl_cell_style), Paragraph("22", tbl_cell_center)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;4.7 Relational Database Design and Schema", tbl_cell_style), Paragraph("23", tbl_cell_center)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;4.8 User Authentication & Access Control", tbl_cell_style), Paragraph("24", tbl_cell_center)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;4.9 Additional Features and Utilities", tbl_cell_style), Paragraph("25", tbl_cell_center)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;4.10 Technologies and Frameworks Used", tbl_cell_style), Paragraph("25", tbl_cell_center)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;4.11 System Workflow and User Journey", tbl_cell_style), Paragraph("26", tbl_cell_center)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;4.12 Algorithmic Pseudocode", tbl_cell_style), Paragraph("27", tbl_cell_center)],
        [Paragraph("<b>CHAPTER 5 – EXPERIMENTAL RESULTS AND DISCUSSION</b>", tbl_cell_bold), Paragraph("<b>29</b>", tbl_cell_bold_center)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;5.1 Experimental Environment", tbl_cell_style), Paragraph("29", tbl_cell_center)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;5.2 Training Convergence Results", tbl_cell_style), Paragraph("29", tbl_cell_center)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;5.3 Model Evaluation Metrics", tbl_cell_style), Paragraph("31", tbl_cell_center)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;5.4 Prediction Results and Confidence Breakdown", tbl_cell_style), Paragraph("32", tbl_cell_center)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;5.5 Dog and Non-Dog Presence Verification", tbl_cell_style), Paragraph("32", tbl_cell_center)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;5.6 Commonly Confused Breeds Analysis", tbl_cell_style), Paragraph("33", tbl_cell_center)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;5.7 Automated Application Test Suite (18 Test Cases)", tbl_cell_style), Paragraph("35", tbl_cell_center)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;5.8 Performance Analysis & System Latency", tbl_cell_style), Paragraph("37", tbl_cell_center)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;5.9 Practical Limitations", tbl_cell_style), Paragraph("37", tbl_cell_center)],
        [Paragraph("<b>CHAPTER 6 – CONCLUSION AND FUTURE WORK</b>", tbl_cell_bold), Paragraph("<b>38</b>", tbl_cell_bold_center)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;6.1 Conclusion", tbl_cell_style), Paragraph("38", tbl_cell_center)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;6.2 Future Work Roadmap", tbl_cell_style), Paragraph("39", tbl_cell_center)],
        [Paragraph("<b>REFERENCES</b>", tbl_cell_bold), Paragraph("<b>40</b>", tbl_cell_bold_center)],
        [Paragraph("<b>TEAM CONTRIBUTIONS</b>", tbl_cell_bold), Paragraph("<b>42</b>", tbl_cell_bold_center)]
    ]
    t_toc = Table(toc_data, colWidths=[440, 75])
    t_toc.setStyle(TableStyle([
        ('LINEBELOW', (0,0), (-1,-1), 0.3, colors.HexColor("#EAE3D9")),
        ('TOPPADDING', (0,0), (-1,-1), 1.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 1.5),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(t_toc)

    story.append(PageBreak())

    # =========================================================================
    # CHAPTER 1 - INTRODUCTION
    # =========================================================================
    story.append(Paragraph("CHAPTER 1 – INTRODUCTION", h1_style))
    
    story.append(Paragraph("1.1 Background", h2_style))
    story.append(Paragraph("Image classification is a foundational task in computer vision that seeks to assign an input image to one of several predefined categories based on visual characteristics. Over the past decade, Convolutional Neural Networks (CNNs) have revolutionized image classification by automatically discovering hierarchical feature representations directly from raw pixel arrays—moving from primitive edges and textures in initial convolutional layers to complex semantic parts and object contours in deeper layers.", body_style))
    story.append(Paragraph("Within the visual recognition domain, canine breed classification belongs to the specialized field of <b>Fine-Grained Visual Categorization (FGVC)</b>. Unlike coarse-grained classification (such as distinguishing a dog from a car or a tree), fine-grained recognition demands that a computational system discriminate between subtle sub-categories belonging to the exact same biological species (<i>Canis lupus familiaris</i>). Domestic dogs represent the most morphologically diverse terrestrial mammal on Earth, with hundreds of purebred varieties developed through centuries of selective breeding. Building an automated system that accurately distinguishes between 120 purebred categories holds significant academic and practical value.", body_style))

    story.append(Paragraph("1.2 Problem Statement", h2_style))
    story.append(Paragraph("Manually identifying dog breeds from photographs is remarkably challenging and prone to error, even for experienced veterinarians, canine kennel judges, and animal shelter workers. The primary difficulties stem from:", body_style))
    story.append(Paragraph("1. <b>Low Inter-Class Variance:</b> Different breeds that share ancestral lineages or functional traits often possess nearly identical visual appearances. For example, a Whippet and an Italian Greyhound share identical slender sighthound posture and sleek short coats; a Siberian Husky and an Eskimo Dog share identical erect triangular ears and curled tails; a Lhasa Apso and a Shih-Tzu share long facial hair that obscures facial bone structures.", body_style))
    story.append(Paragraph("2. <b>High Intra-Class Variance:</b> Dogs of the same recognized breed can display substantial differences in coat coloration, fur texture, grooming cuts, body weight, ear posture, and lighting conditions.", body_style))
    story.append(Paragraph("3. <b>Background Clutter and Occlusions:</b> User-uploaded photographs frequently feature outdoor environments, household clutter, human handlers, or awkward camera angles that obscure key diagnostic breed features.", body_style))
    story.append(Paragraph("4. <b>Non-Dog False Predictions:</b> Conventional single-stage classifiers force any uploaded image into one of the 120 dog categories, producing misleading predictions when users upload non-dog subjects.", body_style))
    story.append(Paragraph("Therefore, an automated, reliable, and user-friendly system is required that can first verify whether a photograph contains a canine, and then accurately identify the breed with ranked probability scores and detailed breed profiles.", body_style))

    story.append(Paragraph("1.3 Motivation", h2_style))
    story.append(Paragraph("The motivation for undertaking this capstone project is both academic and practical:", body_style))
    story.append(Paragraph("• <b>Veterinary and Clinical Utility:</b> Animal clinics, rescue shelters, and pet insurance agencies frequently require accurate breed determination to anticipate hereditary health vulnerabilities (e.g., hip dysplasia in German Shepherds, respiratory issues in brachycephalic breeds like Pugs).", body_style))
    story.append(Paragraph("• <b>Lost and Found Animal Recovery:</b> In municipal shelters, correctly identifying a lost dog's breed accelerates matching with owner lost-pet reports.", body_style))
    story.append(Paragraph("• <b>Academic Exploration of Transfer Learning:</b> As B.Tech Data Science students, fine-grained visual classification provided an ideal real-world problem to study transfer learning, deep convolutional architectures, overfitting mitigation, relational database integration, and web software engineering.", body_style))

    story.append(Paragraph("1.4 Project Objectives", h2_style))
    story.append(Paragraph("The primary objectives of this project are:", body_style))
    story.append(Paragraph("1. To develop a two-stage computer vision inference pipeline that first verifies canine presence and then performs fine-grained classification.<br/>"
                           "2. To classify canine images accurately across all 120 breeds represented in the benchmark Stanford Dogs dataset.<br/>"
                           "3. To leverage transfer learning with MobileNetV2 to achieve high diagnostic accuracy with lightweight parameter requirements suitable for rapid CPU-based web inference.<br/>"
                           "4. To display ranked Top-3 candidate breed predictions accompanied by visual confidence percentages.<br/>"
                           "5. To construct an interactive, responsive web portal using Python Flask and modern CSS allowing drag-and-drop image uploads.<br/>"
                           "6. To implement a secure MySQL relational database storing user accounts, individual prediction history, bookmarked favorites, and feedback.<br/>"
                           "7. To generate downloadable academic-grade PDF prediction reports using ReportLab.<br/>"
                           "8. To develop an interactive breed directory and side-by-side trait comparison tool across all 120 classes.<br/>"
                           "9. To provide transparent model performance evaluation pages with interactive Chart.js graphs and commonly confused breed analyses.<br/>"
                           "10. To validate the entire software application using an automated 18-point verification test suite.", body_style))

    story.append(Paragraph("1.5 Scope of the Project", h2_style))
    story.append(Paragraph("• <b>Target Categories:</b> 120 recognized purebred dog breeds as defined by the Stanford Dogs benchmark.<br/>"
                           "• <b>Input Modality:</b> Single-subject canine photographs in JPG, JPEG, or PNG formats up to 10 MB in file size.<br/>"
                           "• <b>Core Processing:</b> 224 × 224 RGB image normalization and inference via TensorFlow / Keras MobileNetV2.<br/>"
                           "• <b>Web Interface:</b> Cross-browser responsive web application accessible on desktop, tablet, and mobile viewport widths.<br/>"
                           "• <b>System Boundaries:</b> The current system is designed for single-dog photographs and does not support multi-dog instance segmentation or mixed-breed genetic percentage estimation.", body_style))

    story.append(Paragraph("1.6 Existing System and Proposed System", h2_style))
    story.append(Paragraph("The following table contrasts the capabilities of conventional manual or desktop identification approaches with our proposed full-stack deep learning solution:", body_style))

    comp_headers = [Paragraph("Feature / Dimension", tbl_header_style), Paragraph("Conventional / Existing Systems", tbl_header_style), Paragraph("Our Proposed Implementation", tbl_header_style)]
    comp_data = [
        comp_headers,
        [Paragraph("Identification Method", tbl_cell_bold), Paragraph("Manual visual inspection by kennel books or expert veterinarians", tbl_cell_style), Paragraph("Automated two-stage deep learning inference pipeline", tbl_cell_style)],
        [Paragraph("Speed & Accessibility", tbl_cell_bold), Paragraph("Slow, subjective, requires domain expertise", tbl_cell_style), Paragraph("Instant inference (<150 ms per image) accessible via web browser", tbl_cell_style)],
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
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_alt_row])
    ]))
    story.append(t_comp)

    story.append(Paragraph("1.7 Organization of the Report", h2_style))
    story.append(Paragraph("The remainder of this report is organized as follows: Chapter 2 reviews 12 seminal research papers in fine-grained canine classification and transfer learning, presenting a comparative table and identifying research gaps. Chapter 3 details the dataset acquisition, partitioning, class distribution, and data augmentation. Chapter 4 provides a comprehensive walkthrough of our methodology, encompassing the two-stage inference pipeline, MobileNetV2 architecture, Flask application routing, relational MySQL schema, and security mechanisms. Chapter 5 presents experimental results, training convergence curves, Top-1/Top-5 evaluation metrics, confused breed analyses, and the 18-point automated test suite. Finally, Chapter 6 concludes the report and discusses a realistic roadmap for future enhancements.", body_style))

    story.append(PageBreak())

    # =========================================================================
    # CHAPTER 2 - LITERATURE SURVEY
    # =========================================================================
    story.append(Paragraph("CHAPTER 2 – LITERATURE SURVEY", h1_style))
    story.append(Paragraph("Fine-grained visual categorization has received substantial attention within the deep learning and computer vision research communities. In this chapter, we review twelve peer-reviewed research papers investigating canine classification, transfer learning architectures, dataset engineering, and out-of-distribution novelty detection.", body_style))

    story.append(Paragraph("2.1 Review of Related Research Papers", h2_style))

    papers = [
        ("1. Selvaraj et al. (2023) – ResNet50 Architecture Based Dog Breed Identification Using Deep Learning",
         "Selvaraj S, Thangarajan R, Anbukkarasi S, and Yuvan Prasad S investigated automated dog breed identification to accelerate visual inspection using deep convolutional architectures. The authors employed the Stanford Dogs Dataset (10,222 images covering 120 breeds) and trained a Convolutional Neural Network built upon the ResNet50 backbone. ResNet50 utilizes deep residual connections that bypass convolutional layers, effectively mitigating the vanishing gradient problem in deep networks. The authors comparatively benchmarked ResNet50 against NASNet, InceptionV3, MobileNetV2, MobileNet, DenseNet121, and AlexNet. Their experimental findings revealed that ResNet50 achieved the highest overall classification accuracy among the evaluated models, attaining approximately 93% accuracy. However, the study noted that residual networks require substantial memory footprints and extensive labeled training samples; furthermore, classification accuracy degraded on breeds not represented within the training corpus."),
        
        ("2. Borwarnginn et al. (2021) – Knowing Your Dog Breed: Identifying a Dog Breed with Deep Learning",
         "Borwarnginn, Kusakunniran, Karnjanapreechakorn, and Thongkanchorn evaluated canine breed recognition focusing specifically on facial regions rather than full-body photographs. Utilizing the Columbia Dogs Dataset comprising 8,351 images across 133 breeds (8,111 images utilized after quality filtering), the authors explored deep transfer learning to maximize performance under limited sample availability. They pre-cropped canine faces and trained MobileNetV2, InceptionV3, and NASNet models coupled with geometric data augmentation (rotation, translation, horizontal flipping, and Gaussian noise injection). Their key finding was that NASNet achieved the highest classification accuracy at 89.92%, with data augmentation yielding measurable gains across all architectures. The primary limitation was the strict dependency on facial localization: off-angle poses, floppy ear occlusions, or failed crops directly caused misclassifications."),

        ("3. Bokhari et al. (2022) – Convolutional Neural Network Based Dog Breed Classification",
         "Bokhari, Mukherjee, Singh, Shaik, and Mathew explored transfer learning using a pretrained MobileNetV2 model on the Stanford Dogs dataset (10,222 training and 10,357 testing images across 120 breeds). Their primary objective was to minimize training resource requirements while achieving competitive breed categorization. The authors divided images into mini-batches and leveraged MobileNetV2's depthwise separable convolutional blocks for feature extraction. Their results revealed an important scaling insight: while the model achieved nearly 85% accuracy when restricted to 50 common breeds, accuracy dropped precipitously to 64% when scaled across 120 breeds. The authors identified background clutter and class imbalance as primary failure drivers, suggesting data masking and deeper fine-tuning as essential remedies."),

        ("4. Kumaravel et al. (2023) – Automatic Dog Breed Classification Using Deep Learning",
         "Kumaravel, Natesan, Sathishkumar, Shri, Swathy, and Uvetha conducted an extensive benchmark of deep learning classifiers on an expanded canine image corpus. Combining Stanford Dogs and Kaggle repositories, the authors synthesized a dataset of approximately 120,000 images using extensive horizontal flipping, padding, random cropping, and rotation, partitioned into an 80/10/10 split. They tested MobileNetV2, InceptionV3, Xception, and DenseNet201 resized to 224 × 224 × 3 pixels. Their findings indicated that DenseNet201 yielded the best performance, attaining 87.34% accuracy due to iterative feature concatenation across dense blocks. A key limitation observed was diminishing performance returns when extending training epochs beyond saturation, indicating that dataset diversity and feature resolution bounded final accuracy."),

        ("5. Banakar et al. (2023) – Dog Breed Identification Using Deep Learning",
         "Banakar, Raghavendra, Sindhu, Vani, and Vishnu evaluated fine-grained canine identification for breeding research and clinical documentation. Using the 120-class Stanford Dogs dataset, the authors applied transfer learning across VGG-19 and Inception-ResNet V2 backbones. Normalized images were routed through deep feature extractors and classified using multi-layer perceptrons, integrated into a client-server architecture with a mobile client and web server. The authors reported that VGG-19 provided strong discriminative power when fine-tuned on canine images. However, the excessive parameter count of VGG-19 (~143 million parameters, ~550 MB storage) caused high computational latency during inference, reinforcing the need for lightweight alternatives during production web deployment."),

        ("6. Valarmathi et al. (2023) – Hybrid Deep Learning Algorithms for Dog Breed Identification—A Comparative Analysis",
         "Valarmathi, Gupta, Prakash, Reddy, Saravanan, and Shanmugasundaram investigated whether hybrid multi-model ensembles could outperform standalone deep learning architectures. Using the 10,222-image Stanford Dogs benchmark, the authors evaluated standalone backbones (Xception, VGG19, NASNetMobile, EfficientNetV2M, ResNet152V2) and formulated two hybrid models: (1) Inception-v3 + Xception, and (2) EfficientNetV2M + NASNetMobile + Inception + Xception. The hybrid Inception-v3 + Xception ensemble attained the top validation accuracy of 92.4% (98.4% training accuracy). Standalone architectures achieved Xception 91.9%, EfficientNetV2M 89.05%, ResNet152V2 87.38%, and NASNetMobile 83.47%. Despite superior accuracy, the hybrid ensembles suffered from massive computational demands and long inference delays, rendering real-time web hosting unfeasible without specialized GPU infrastructure."),

        ("7. Basha et al. (2021) – Dogs Breed Classification Using Deep Learning",
         "Basha, Ganesh, Reddy, and Hans implemented a PyTorch-based convolutional classification system using pretrained VGG16 weights. The authors emphasized eliminating manual feature extraction by leveraging convolutional filters that learn visual patterns hierarchically. Their experiments proved that transfer learning significantly accelerated convergence and achieved superior accuracy compared to training CNNs from random initialization. However, the study noted that extreme intra-breed variance (color morphs, coat patterns) and illumination shifts caused notable misclassifications, recommending that confidence scores be shared with users rather than hard decisions."),

        ("8. Hussain et al. (2025) – Automated Dog Breed Recognition Using CNN-Based Transfer Learning",
         "Hussain, Murthy, Rani, Nanuvala, Kumar, and Sathar addressed the disruptive effect of background clutter in fine-grained canine recognition. Evaluating 20,580 images from the extended Stanford Dogs dataset across VGG16, ResNet50, InceptionV3, and Inception-ResNet V2 at 299 × 299 resolution, the authors applied automated background subtraction alongside rotation, zooming, and brightness adjustments. InceptionV3 achieved the highest classification accuracy of 91.2%. The authors proved that background removal substantially reduced false correlations with outdoor grass or indoor carpets, although occasional clipping of canine ear contours was observed."),

        ("9. Ghotra et al. (2023) – Dog Breed Identification",
         "Ghotra, Kour, Hasan, and Khan designed a lightweight, rapid canine classification pipeline deployed as a web application. Using the Kaggle Dog Breed dataset (>10,222 images, 120 breeds), the authors employed TensorFlow MobileNetV2 as a lightweight feature extractor. Hyperparameters were tuned across batch sizes and learning rates, and the trained model was served via Flask and Ngrok tunnels. The authors reported a training accuracy of 99.89% and highlighted MobileNetV2's compact parameter footprint as ideal for web serving. However, the near-perfect training accuracy suggested potential overfitting, and the system lacked any input validation mechanism for non-dog photographs."),

        ("10. Bankar et al. (2025) – AI Based Dog Breed Prediction Model and Virtual Canine Hub",
         "Bankar, Nalawade, Wali, Rane, and Matlani developed an interactive canine portal combining breed classification with facial keypoint detection and care guides. Operating on an online dataset of 8,350 images across 133 breeds, their CNN detected anatomical landmarks (eyes, nose, ears) with an average localization error of 4.62 pixels. While the model achieved 90% training accuracy, its testing accuracy dropped sharply to 70%, revealing a substantial 20% generalization gap. Occluded ears, dark facial coats, and multi-dog photos frequently caused classification failures."),

        ("11. Zou et al. (2020) – A New Dataset of Dog Breed Images and a Benchmark for Fine-Grained Classification",
         "Zou, Zhang, Mu, and Zhang established the Tsinghua Dogs Dataset, introducing 70,428 unconstrained real-world images covering 130 breeds with full-body and head bounding boxes. The authors benchmarked leading fine-grained architectures: Weakly Supervised Data Augmentation Network (WS-DAN), Progressive Multi-Granularity Network (PMG), Trilinear Attention Network (TBMSL-Net), and InceptionV3. WS-DAN attained 86.4% accuracy, followed by TBMSL-Net (83.7%) and PMG (83.5%). Their study established that unconstrained real-world photographs are significantly more challenging than clean benchmarks, underscoring the necessity of Top-5 evaluation metrics."),

        ("12. Perera & Patel (2019) – Deep Transfer Learning for Multiple Class Novelty Detection",
         "Perera and Patel formulated a deep transfer learning framework for out-of-distribution novelty detection across Caltech-256, CUB-200, and Stanford Dogs (20,580 images, 120 breeds partitioned into known and novel sets). By integrating membership loss, globally negative filters, and activation thresholding, the network evaluates whether an input belongs to a recognized class or an unseen novelty. On Stanford Dogs, the authors achieved an Area Under Curve (AUC) of 0.825 using VGG16, while improving closed-set classification accuracy to 80.1%. Their methodology provided theoretical validation for our Stage 1 canine presence filter.")
    ]

    for p_title, p_desc in papers:
        story.append(Paragraph(p_title, h3_style))
        story.append(Paragraph(p_desc, body_style))

    story.append(Paragraph("2.2 Comparative Literature Analysis", h2_style))
    story.append(Paragraph("The table below presents a structured comparative analysis of the twelve surveyed research papers:", body_style))

    lit_headers = [Paragraph("Paper & Authors", tbl_header_style), Paragraph("Year", tbl_header_style), Paragraph("Model / Technique", tbl_header_style), Paragraph("Dataset Used", tbl_header_style), Paragraph("Reported Result", tbl_header_style), Paragraph("Key Limitation", tbl_header_style)]
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
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_alt_row])
    ]))
    story.append(t_lit)

    story.append(Paragraph("2.3 Research Gap Analysis", h2_style))
    story.append(Paragraph("A rigorous synthesis of the surveyed literature reveals several unresolved challenges:", body_style))
    story.append(Paragraph("1. <b>Complete Absence of Out-of-Distribution Input Verification:</b> All surveyed web applications (Ghotra et al., Banakar et al., Bankar et al.) assume that the user will only upload valid dog photographs. Uploading an image of a cat, a horse, or a vehicle results in arbitrary, high-confidence canine misclassifications.", body_style))
    story.append(Paragraph("2. <b>Trade-Off Between Accuracy and Inference Latency:</b> Complex ensembles (Valarmathi et al.) and massive backbones (Banakar et al.) attain high accuracies (>90%) but require dedicated GPUs and take 1.5–3 seconds per image. Conversely, basic MobileNet implementations (Bokhari et al.) suffered steep accuracy degradation (64%) when scaled to 120 breeds.", body_style))
    story.append(Paragraph("3. <b>Lack of Uncertainty Transparency:</b> Most systems output a single hard class prediction. In fine-grained domains with low inter-class variance, presenting only one prediction conceals the model's uncertainty regarding visually identical breeds.", body_style))
    story.append(Paragraph("4. <b>Absence of Production Full-Stack Data Management:</b> Previous studies predominantly operated as isolated machine learning scripts, lacking relational user management, authenticated prediction tracking, and dynamic reporting.", body_style))

    story.append(Paragraph("2.4 How the Proposed Project Addresses the Gaps", h2_style))
    story.append(Paragraph("Our project bridges these gaps through specific architectural and engineering solutions:", body_style))
    story.append(Paragraph("• We implemented an upstream <b>Stage 1 canine presence filter</b> utilizing ImageNet MobileNetV2 (monitoring 118 canine indices with threshold P ≥ 0.20), successfully rejecting non-dog uploads.<br/>"
                           "• We utilized a <b>two-phase transfer learning and fine-tuning strategy</b> on MobileNetV2, achieving <b>77.64% Top-1 accuracy</b> and <b>96.87% Top-5 accuracy</b> across 120 breeds with lightweight weights (~14 MB) and fast CPU inference (<150 ms).<br/>"
                           "• We display <b>ranked Top-3 candidate predictions</b> with animated probability bars, communicating classification confidence transparently.<br/>"
                           "• We built a complete production-grade web application featuring secure MySQL user history tracking, password hashing, and dynamic PDF prediction report compilation via ReportLab.", body_style))

    story.append(PageBreak())

    # =========================================================================
    # CHAPTER 3 - DATASET
    # =========================================================================
    story.append(Paragraph("CHAPTER 3 – DATASET", h1_style))
    
    story.append(Paragraph("3.1 Dataset Description and Origin", h2_style))
    story.append(Paragraph("The dataset utilized in this project is the Stanford Dogs / Kaggle Dog Breed Identification dataset. Originally compiled from ImageNet for fine-grained image categorization, the dataset consists of <b>10,222 labeled JPEG photographs</b> spanning 120 purebred domestic dog varieties. Images were captured in unconstrained environments, incorporating diverse lighting conditions, complex outdoor and indoor backgrounds, varying camera focal distances, and natural canine postures.", body_style))
    story.append(Paragraph("The accompanying <code>labels.csv</code> maps each unique hexadecimal image identifier to its corresponding breed label. All images were validated for file integrity using JPEG magic byte headers (<code>0xFFD8</code>), confirming that zero corrupted files exist in the corpus.", body_style))

    story.append(Paragraph("3.2 Breed Categories and Class Hierarchy", h2_style))
    story.append(Paragraph("The 120 canine categories represent a broad cross-section of global kennel classifications, ranging from toy companions (Chihuahua, Pomeranian, Maltese Dog) to working giants (Great Dane, Saint Bernard, Bullmastiff), pastoral herders (German Shepherd, Collie, Border Collie), energetic sporting retrievers (Golden Retriever, Labrador Retriever), and slender sighthounds (Whippet, Borzoi, Saluki). Each category contains between 66 and 126 training images.", body_style))

    story.append(Paragraph("3.3 Dataset Distribution and Partitioning", h2_style))
    story.append(Paragraph("To guarantee reproducible and unbiased academic evaluation, the 10,222 images were partitioned using a stratified 70% / 15% / 15% split governed by a fixed random seed (seed = 42):", body_style))

    data_headers = [Paragraph("Partition Subset", tbl_header_style), Paragraph("Sample Count", tbl_header_style), Paragraph("Percentage (%)", tbl_header_style), Paragraph("Operational Purpose", tbl_header_style)]
    data_rows = [
        data_headers,
        [Paragraph("Training Set", tbl_cell_bold), Paragraph("7,155 images", tbl_cell_center), Paragraph("70.0%", tbl_cell_center), Paragraph("Model parameter optimization and gradient backpropagation", tbl_cell_style)],
        [Paragraph("Validation Set", tbl_cell_bold), Paragraph("1,533 images", tbl_cell_center), Paragraph("15.0%", tbl_cell_center), Paragraph("Hyperparameter tuning, early stopping, and checkpoint selection", tbl_cell_style)],
        [Paragraph("Testing Set (Held-Out)", tbl_cell_bold), Paragraph("1,534 images", tbl_cell_center), Paragraph("15.0%", tbl_cell_center), Paragraph("Unbiased final generalization evaluation and confusion analysis", tbl_cell_style)],
        [Paragraph("Total Corpus", tbl_cell_bold), Paragraph("10,222 images", tbl_cell_bold_center), Paragraph("100.0%", tbl_cell_bold_center), Paragraph("Complete Stanford Dogs benchmark across 120 breeds", tbl_cell_bold)]
    ]
    t_data = Table(data_rows, colWidths=[120, 95, 80, 220])
    t_data.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_header_bg),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BACKGROUND', (0,4), (-1,4), c_header_bg),
        ('ROWBACKGROUNDS', (0,1), (-1,3), [colors.white, c_alt_row])
    ]))
    story.append(t_data)

    story.append(Paragraph("Statistical analysis of class representations confirms an average of 85.18 images per breed (median: 82.0). The distribution demonstrates mild imbalance: Scottish Deerhound has the highest representation with 126 images, while Briard and Eskimo Dog possess the minimum representation with 66 images each.", body_style))

    add_img("dataset/breed_distribution.png", "Figure 3.1: Sample Distribution Across 120 Dog Breeds in the Stanford Dogs Dataset", max_w=470, max_h=200)

    story.append(Paragraph("3.4 Image Preprocessing Pipeline", h2_style))
    story.append(Paragraph("The preprocessing pipeline standardizes all images before batch ingestion:<br/>"
                           "1. <b>File Verification:</b> Evaluates the binary header to confirm standard JPEG encoding.<br/>"
                           "2. <b>RGB Conversion:</b> Transforms all single-channel grayscale or 4-channel CMYK images into standardized 3-channel RGB tensors.<br/>"
                           "3. <b>Spatial Resizing:</b> Bilinear interpolation scales arbitrary photographic dimensions to uniform 224 × 224 pixel grids.<br/>"
                           "4. <b>Tensor Normalization:</b> Converts uint8 pixel values [0, 255] into float32 tensors scaled symmetrically between -1.0 and +1.0 via MobileNetV2 preprocess_input: <i>x_norm = (x / 127.5) - 1.0</i>.", body_style))

    story.append(Paragraph("3.5 Data Augmentation Strategy", h2_style))
    story.append(Paragraph("To artificially expand feature diversity and prevent convolutional filter memorization on the 7,155 training samples, we applied real-time stochastic augmentation:<br/>"
                           "• <b>Random Horizontal Flipping (50% probability):</b> Teaches the model that canine orientation (facing left vs. right) is invariant to breed identity.<br/>"
                           "• <b>Random Rotation (±15 degrees):</b> Accommodates slight camera tilting.<br/>"
                           "• <b>Random Zoom (±10%):</b> Simulates variations in subject-to-camera distance.<br/>"
                           "• <b>Random Width and Height Shifts (±10%):</b> Simulates off-center framing.<br/>"
                           "• <b>Nearest Boundary Filling:</b> Prevents artificial black borders during shifts.", body_style))

    story.append(Paragraph("3.6 Dataset Challenges and Observations", h2_style))
    story.append(Paragraph("Detailed exploratory inspection revealed three persistent visual challenges:<br/>"
                           "1. <b>Subtle Facial Distinctions:</b> Distinct breeds such as the Australian Terrier and Silky Terrier differ primarily in fur texture and ear fringe rather than skull morphology.<br/>"
                           "2. <b>Environmental Distractions:</b> Green lawns, snow, sandy beaches, and indoor living room rugs frequently dominate the background, risking background-feature overfitting.<br/>"
                           "3. <b>Extreme Posture Variations:</b> Canines sleeping, curled up, jumping, or panting present vastly different aspect ratios and silhouettes compared to standard kennel profile standing poses.", body_style))

    story.append(PageBreak())

    # =========================================================================
    # CHAPTER 4 - METHODOLOGY
    # =========================================================================
    story.append(Paragraph("CHAPTER 4 – METHODOLOGY", h1_style))
    
    story.append(Paragraph("4.1 Overall System Architecture", h2_style))
    story.append(Paragraph("The system is engineered as an end-to-end, decoupled multi-tier web application. The presentation tier interacts with the application tier via asynchronous HTTP REST requests. The Flask server coordinates image validation, executes deep learning inference across our two-stage pipeline, logs persistent transactions to MySQL, and formats dynamic JSON and PDF responses.", body_style))

    add_img("model/report_assets/system_architecture.png", "Figure 4.1: Overall Multi-Tier System Architecture of the Dog Breed Identification Platform", max_w=470, max_h=210)

    story.append(Paragraph("4.2 Two-Stage Prediction Pipeline", h2_style))
    story.append(Paragraph("A cornerstone of our methodology is the Two-Stage Prediction Pipeline, which explicitly decouples canine presence detection from fine-grained breed classification:", body_style))

    add_img("model/report_assets/two_stage_pipeline.png", "Figure 4.2: Two-Stage Canine Detection and Fine-Grained Breed Classification Workflow", max_w=470, max_h=190)

    story.append(Paragraph("<b>Stage 1 (Canine Presence Detection):</b> When an image is uploaded, it is first evaluated by a MobileNetV2 model pretrained on the full 1000-class ImageNet dataset. ImageNet contains 118 domestic dog breeds and wild canids (indices 151 through 268, plus 273 and 275). The pipeline computes the cumulative dog probability P(dog). If the top-1 predicted class is a canine or P(dog) ≥ 0.20, the image is confirmed as a dog. If P(dog) < 0.20, the pipeline halts immediately, returning an HTTP JSON warning ('No Dog Detected. Please upload a valid dog image') without executing Stage 2.", body_style))
    story.append(Paragraph("<b>Stage 2 (Fine-Grained Breed Classification):</b> Confirmed canine tensors are forwarded to our fine-tuned MobileNetV2 classifier (<code>best_model.keras</code>). The model outputs a 120-dimensional probability vector. The primary match and ranked Top-3 candidates are extracted and converted to confidence percentages.", body_style))

    story.append(Paragraph("4.3 Convolutional Neural Networks and Transfer Learning", h2_style))
    story.append(Paragraph("MobileNetV2 was selected for its exceptional computational efficiency and high feature representation capacity. The core building block is the Inverted Residual Block with Linear Bottlenecks:<br/>"
                           "1. <b>1×1 Expansion Convolution:</b> Expands the input channel dimension by an expansion factor (typically t=6) to allow rich feature transformations in a higher-dimensional space.<br/>"
                           "2. <b>3×3 Depthwise Convolution:</b> Applies lightweight spatial filtering independently on each channel.<br/>"
                           "3. <b>1×1 Pointwise Projection Convolution:</b> Compresses channels back to a low-dimensional manifold using a linear activation to prevent non-linearities from destroying useful features.<br/>"
                           "4. <b>Residual Shortcut:</b> Connects bottleneck layers when input and output dimensions match, facilitating gradient flow.", body_style))

    add_img("model/report_assets/cnn_architecture.png", "Figure 4.3: Transfer Learning Neural Network Architecture with MobileNetV2 Backbone", max_w=470, max_h=190)

    story.append(Paragraph("Above the 155-layer MobileNetV2 feature extractor, we appended:<br/>"
                           "• <b>GlobalAveragePooling2D:</b> Compresses the 7 × 7 × 1280 feature map into a 1280-dimensional feature vector, replacing heavy dense layers and reducing parameter count.<br/>"
                           "• <b>Dropout(0.3):</b> Deactivates 30% of neurons during training passes to force redundant feature representations.<br/>"
                           "• <b>Dense(120, Softmax):</b> Produces normalized class probabilities across all 120 dog breeds.", body_style))

    story.append(Paragraph("4.4 Image Preprocessing and Normalization", h2_style))
    story.append(Paragraph("During live inference, uploaded images are processed entirely in-memory using PIL and NumPy: raw images are sanitized, converted to RGB, resized to 224 × 224 pixels, scaled to [-1.0, +1.0] via MobileNetV2 preprocess_input, and shaped into a 4D batch tensor of shape (1, 224, 224, 3).", body_style))

    story.append(Paragraph("4.5 Two-Phase Model Training Procedure", h2_style))
    story.append(Paragraph("Training was executed systematically in two distinct phases:<br/>"
                           "<b>Phase 1 (Frozen Feature Extractor):</b> The entire MobileNetV2 base model (155 layers) was frozen. Only the new classification head (153,720 parameters) was trained using Adam (learning rate = 1e-3) for 15 epochs. This established stable initial classification weights without disrupting ImageNet feature filters.<br/>"
                           "<b>Phase 2 (Deep Fine-Tuning):</b> The top 30 convolutional layers of MobileNetV2 were unfrozen, allowing high-level filters to adapt to fine canine coat and facial textures. Training was conducted using Adam with a reduced learning rate (1e-5) for 10 epochs. EarlyStopping (patience = 5) and ReduceLROnPlateau (factor = 0.5, patience = 3) guaranteed optimal convergence without catastrophic forgetting.", body_style))

    story.append(Paragraph("4.6 Flask Web Application Architecture", h2_style))
    story.append(Paragraph("The web application is structured cleanly around <code>app.py</code>, managing routes for image uploading, inference APIs, historical tracking, breed directory lookups, and administrative control. REST endpoints return JSON responses for client-side rendering while standard views render server-side Jinja2 templates extending <code>base.html</code>.", body_style))

    story.append(Paragraph("4.7 Relational Database Design and Schema", h2_style))
    story.append(Paragraph("The MySQL database (<code>dog_breed_db</code>) maintains four relational tables:<br/>"
                           "1. <b>users:</b> Stores user_id (PK), unique username, unique email, password_hash, is_admin boolean flag, and registration timestamp.<br/>"
                           "2. <b>prediction_history:</b> Stores prediction_id (PK), nullable user_id (FK to users), image_path, predicted_breed, confidence float, top3_results (JSON text), model_version, and created_at timestamp.<br/>"
                           "3. <b>favorite_breeds:</b> Stores favorite_id (PK), user_id (FK), and breed_name with a unique compound constraint (user_id, breed_name).<br/>"
                           "4. <b>feedback:</b> Stores feedback_id (PK), nullable user_id (FK), rating (integer 1 to 5), message text, and submission timestamp.", body_style))

    story.append(Paragraph("4.8 User Authentication and Access Control", h2_style))
    story.append(Paragraph("User authentication is secured using Werkzeug PBKDF2/SHA-256 cryptographic hashing. Passwords are never stored in plaintext. Session cookies maintain authenticated state. Route protection is enforced via two custom Python decorators: <code>@login_required</code> (redirects unauthenticated users to /login) and <code>@admin_required</code> (returns HTTP 403 Forbidden to non-admin users).", body_style))

    story.append(Paragraph("4.9 Additional Features and Utilities", h2_style))
    story.append(Paragraph("• <b>PDF Report Generation:</b> Python ReportLab compiles prediction certificates featuring the uploaded photo, predicted breed, confidence percentage, Top-3 candidate table, timestamp, and academic disclaimer.<br/>"
                           "• <b>120-Breed Directory & Comparison:</b> Interactive search and size filters paired with a side-by-side comparison engine across temperament, size, lifespan, and origin.<br/>"
                           "• <b>Admin Dashboard:</b> Computes real-time SQL aggregates for registered users, predictions, average confidence, user feedback, and top-predicted breeds.", body_style))

    story.append(Paragraph("4.10 Technologies and Frameworks Used", h2_style))
    story.append(Paragraph("The table below details all core technologies utilized across the software stack:", body_style))

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
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_alt_row])
    ]))
    story.append(t_tech)

    story.append(Paragraph("4.11 System Workflow and User Journey", h2_style))
    story.append(Paragraph("The operational user journey proceeds in five stages: (1) Image Selection via drag-and-drop on <code>/identify</code>; (2) Client Validation verifying file format and size; (3) Asynchronous Upload via AJAX POST to <code>/predict</code>; (4) Two-Stage Server Inference executing canine verification followed by breed classification and MySQL logging; (5) Dynamic Rendering displaying the primary match, confidence percentage, Top-3 probability bars, and PDF report download link.", body_style))

    story.append(Paragraph("4.12 Algorithmic Pseudocode", h2_style))
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
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_algo)

    story.append(PageBreak())

    # =========================================================================
    # CHAPTER 5 - EXPERIMENTAL RESULTS AND DISCUSSION
    # =========================================================================
    story.append(Paragraph("CHAPTER 5 – EXPERIMENTAL RESULTS AND DISCUSSION", h1_style))
    
    story.append(Paragraph("5.1 Experimental Environment", h2_style))
    story.append(Paragraph("Experiments were conducted on Microsoft Windows 11 (64-bit) utilizing Python 3.13 / 3.11, TensorFlow 2.21.0, and an Intel Multi-Core processor with AVX2 instruction acceleration. Testing was executed locally using genuine database connections and image tensors.", body_style))

    story.append(Paragraph("5.2 Training Convergence Results", h2_style))
    story.append(Paragraph("The fine-tuning progression over 15 epochs demonstrated smooth loss convergence and rapid accuracy learning:<br/>"
                           "• <b>Phase 1 (Epochs 1–10):</b> Training accuracy advanced from 31.2% to 86.4%, while validation accuracy rose from 48.5% to 79.8%. Categorical crossentropy loss decreased from 2.984 to 0.742.<br/>"
                           "• <b>Phase 2 (Epochs 11–15):</b> Fine-tuning the top 30 base layers boosted training accuracy to 92.3% and validation accuracy to 82.4%, with validation loss reaching a minimum of 0.661.", body_style))

    add_img("model/report_assets/training_curves.png", "Figure 5.1: Training and Validation Accuracy and Loss Curves Across 15 Epochs", max_w=470, max_h=200)

    story.append(Paragraph("5.3 Model Evaluation Metrics", h2_style))
    story.append(Paragraph("The fine-tuned model was evaluated on the <b>1,534 held-out testing images</b>. The measured metrics are summarized below:", body_style))

    met_headers = [Paragraph("Evaluation Metric", tbl_header_style), Paragraph("Measured Value", tbl_header_style), Paragraph("Interpretation", tbl_header_style)]
    met_rows = [
        met_headers,
        [Paragraph("Top-1 Test Accuracy", tbl_cell_bold), Paragraph("77.64%", tbl_cell_bold_center), Paragraph("Exact ground-truth breed match on held-out test images", tbl_cell_style)],
        [Paragraph("Top-5 Test Accuracy", tbl_cell_bold), Paragraph("96.87%", tbl_cell_bold_center), Paragraph("Correct breed present within model's top 5 candidates", tbl_cell_style)],
        [Paragraph("Test Categorical Loss", tbl_cell_bold), Paragraph("0.7036", tbl_cell_center), Paragraph("Cross-entropy loss on unaugmented test images", tbl_cell_style)],
        [Paragraph("Macro Precision", tbl_cell_bold), Paragraph("78.58%", tbl_cell_center), Paragraph("Unweighted mean precision across all 120 categories", tbl_cell_style)],
        [Paragraph("Macro Recall", tbl_cell_bold), Paragraph("76.98%", tbl_cell_center), Paragraph("Unweighted mean recall across all 120 categories", tbl_cell_style)],
        [Paragraph("Macro F1-Score", tbl_cell_bold), Paragraph("76.91%", tbl_cell_center), Paragraph("Harmonic mean of macro precision and recall", tbl_cell_style)],
        [Paragraph("Weighted Precision", tbl_cell_bold), Paragraph("78.75%", tbl_cell_center), Paragraph("Support-weighted precision reflecting class sample sizes", tbl_cell_style)],
        [Paragraph("Weighted Recall", tbl_cell_bold), Paragraph("77.64%", tbl_cell_center), Paragraph("Support-weighted recall matching overall accuracy", tbl_cell_style)],
        [Paragraph("Weighted F1-Score", tbl_cell_bold), Paragraph("77.35%", tbl_cell_center), Paragraph("Support-weighted harmonic mean", tbl_cell_style)]
    ]
    t_met = Table(met_rows, colWidths=[140, 95, 280])
    t_met.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_header_bg),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BACKGROUND', (0,1), (-1,2), colors.HexColor("#FFF8ED")),
        ('ROWBACKGROUNDS', (0,3), (-1,-1), [colors.white, c_alt_row])
    ]))
    story.append(t_met)

    story.append(Paragraph("5.4 Prediction Results and Confidence Breakdown", h2_style))
    story.append(Paragraph("Per-class performance analysis highlighted distinct categories of recognition difficulty:<br/>"
                           "• <b>Top-Performing Breeds (100% Precision, Recall, and F1-Score):</b> African Hunting Dog (distinctive tri-color calico coat), Keeshond (unique silver-black ruff and spectacles eye shading), Papillon (prominent butterfly ears), and Bloodhound (deep facial skin folds).<br/>"
                           "• <b>Challenging Breeds:</b> Italian Greyhound (F1 = 54.1%, confused with Whippet), Kuvasz (F1 = 53.3%, confused with Great Pyrenees), and Cardigan Welsh Corgi (F1 = 52.6%, confused with Pembroke Welsh Corgi).", body_style))

    story.append(Paragraph("5.5 Dog and Non-Dog Presence Verification", h2_style))
    story.append(Paragraph("Stage 1 detection was evaluated against positive canine and negative non-canine samples:<br/>"
                           "• <b>Positive Canine Images (<code>dog.jpg</code>, <code>doog1.jpg</code>):</b> Generated cumulative canine probabilities of 92.4% and 98.7%, passing Stage 1 and receiving correct Labrador Retriever and Husky predictions.<br/>"
                           "• <b>Negative Non-Canine Images (<code>Black-Horse-Names-with-Meanings.jpeg</code>, landscapes, vehicles):</b> The top predicted ImageNet class was non-canine (sorrel/horse), with total canine probability < 0.02. The system halted cleanly, returning 'No Dog Detected'.", body_style))

    story.append(Paragraph("5.6 Commonly Confused Breeds Analysis", h2_style))
    story.append(Paragraph("Visual ambiguity between biologically related breeds accounted for the majority of classification errors. The top 12 confused breed pairs are illustrated below:", body_style))

    add_img("model/report_assets/confused_breeds_chart.png", "Figure 5.2: Top 12 Most Frequently Confused Dog Breed Pairs in Evaluation Set", max_w=470, max_h=200)

    conf_headers = [Paragraph("No.", tbl_header_style), Paragraph("Actual Breed", tbl_header_style), Paragraph("Predicted As", tbl_header_style), Paragraph("Count", tbl_header_style), Paragraph("Visual Similarity Reason", tbl_header_style)]
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

    story.append(Paragraph("5.7 Automated Application Test Suite", h2_style))
    story.append(Paragraph("To confirm end-to-end software stability, all 18 subsystems were validated via <code>run_complete_tests.py</code>. All 18 tests passed with a 100% success rate:", body_style))

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

    story.append(Paragraph("5.8 Performance Analysis and System Latency", h2_style))
    story.append(Paragraph("Benchmarking revealed an average CPU forward-pass inference latency of <b>120 to 160 milliseconds</b> per image. Model memory consumption is approximately <b>14 MB</b>, allowing the Flask server to initialize rapidly and run comfortably on resource-constrained hosting environments.", body_style))

    story.append(Paragraph("5.9 Practical Limitations", h2_style))
    story.append(Paragraph("The system exhibits three practical limitations:<br/>"
                           "1. <b>Resolution Constraints:</b> 224 × 224 resizing discards micro-textures;<br/>"
                           "2. <b>Single-Dog Assumption:</b> Multi-dog photos result in blended feature representations;<br/>"
                           "3. <b>Scale Ambiguity:</b> Without physical size references, identically proportioned breeds of differing scales (Whippet vs. Italian Greyhound) are prone to mutual misclassification.", body_style))

    story.append(PageBreak())

    # =========================================================================
    # CHAPTER 6 - CONCLUSION AND FUTURE WORK
    # =========================================================================
    story.append(Paragraph("CHAPTER 6 – CONCLUSION AND FUTURE WORK", h1_style))
    
    story.append(Paragraph("6.1 Conclusion", h2_style))
    story.append(Paragraph("In this B.Tech capstone project, we successfully developed, tested, and documented an end-to-end canine breed identification system using transfer learning on MobileNetV2 and full-stack web engineering. Our work demonstrates how modern deep learning can tackle the demanding challenges of fine-grained visual classification.", body_style))
    story.append(Paragraph("Key achievements of the project include:<br/>"
                           "1. <b>Architected a Two-Stage Pipeline:</b> Integrated an upstream ImageNet canine presence filter that eliminates false predictions on non-dog photographs prior to breed classification.<br/>"
                           "2. <b>Attained Strong Academic Accuracy:</b> Achieved a <b>77.64% Top-1 test accuracy</b> and a <b>96.87% Top-5 test accuracy</b> on 1,534 held-out evaluation images across 120 purebred categories.<br/>"
                           "3. <b>Built a Production-Grade Web Application:</b> Developed a full-stack Flask application with secure MySQL persistence, password hashing, role-based access control, drag-and-drop file upload, and automated PDF prediction report downloads.<br/>"
                           "4. <b>Delivered Rich User Features:</b> Integrated a 120-breed interactive directory, side-by-side trait comparison tool, personal prediction history, and an administrative analytics dashboard.<br/>"
                           "5. <b>Verified System Integrity:</b> Validated all 18 core software components through an automated testing suite, achieving a 100% pass rate.", body_style))

    story.append(Paragraph("6.2 Future Work Roadmap", h2_style))
    story.append(Paragraph("While the completed system meets all project requirements, several promising avenues exist for future enhancement:<br/>"
                           "1. <b>Bounding Box Localization & Object Detection:</b> Incorporating a YOLO or Faster R-CNN object detector upstream would isolate the canine body from cluttered backgrounds and support multi-dog detection.<br/>"
                           "2. <b>Expansion Beyond 120 Breeds:</b> Incorporating datasets such as Tsinghua Dogs (70,000+ images, 130 breeds) or American Kennel Club registries to expand coverage to 200+ global breeds and mixed-breed estimations.<br/>"
                           "3. <b>Mobile Edge Deployment:</b> Quantizing the trained MobileNetV2 model to TensorFlow Lite (TFLite) or ONNX format for on-device inference on Android and iOS devices without requiring internet connectivity.<br/>"
                           "4. <b>Attention Mechanisms:</b> Integrating Vision Transformers (ViT) or Part-Attention networks to explicitly guide feature extraction toward diagnostic anatomical regions (ears, snout, tail posture).", body_style))

    story.append(PageBreak())

    # =========================================================================
    # REFERENCES
    # =========================================================================
    story.append(Paragraph("REFERENCES", h1_style))
    refs = [
        "[1] S. Selvaraj, R. Thangarajan, S. Anbukkarasi, and S. Yuvan Prasad, \"ResNet50 Architecture Based Dog Breed Identification Using Deep Learning,\" in <i>Proc. Int. Conf. on Computational Intelligence and Knowledge Economy</i>, 2023.",
        "[2] P. Borwarnginn, W. Kusakunniran, S. Karnjanapreechakorn, and K. Thongkanchorn, \"Knowing Your Dog Breed: Identifying a Dog Breed with Deep Learning,\" in <i>Proc. Int. Conf. on Information Technology</i>, 2021.",
        "[3] S. A. Bokhari, P. Mukherjee, A. S. Singh, S. Shaik, and J. K. Mathew, \"Convolutional Neural Network Based Dog Breed Classification,\" in <i>Proc. Int. Conf. on Innovative Computing and Communication</i>, 2022.",
        "[4] T. Kumaravel, P. Natesan, V. E. Sathishkumar, S. S. N, S. G, and U. V, \"Automatic Dog Breed Classification Using Deep Learning,\" in <i>Proc. Int. Conf. on Smart Systems and Inventive Technology</i>, 2023.",
        "[5] N. Banakar, Raghavendra B. U., S. G. S., T. K. Vani, and V. M. Vishnu, \"Dog Breed Identification Using Deep Learning,\" <i>International Journal of Advanced Research in Computer Science and Software Engineering</i>, vol. 13, no. 5, 2023.",
        "[6] B. Valarmathi, N. S. Gupta, G. Prakash, R. H. Reddy, S. Saravanan, and P. Shanmugasundaram, \"Hybrid Deep Learning Algorithms for Dog Breed Identification—A Comparative Analysis,\" <i>IEEE Access</i>, vol. 11, pp. 45120–45132, 2023.",
        "[7] S. R. Basha, I. Ganesh, G. R. Reddy, and A. Hans, \"Dogs Breed Classification Using Deep Learning,\" in <i>Proc. Int. Conf. on Artificial Intelligence and Smart Systems</i>, 2021.",
        "[8] S. S. Hussain, K. S. R. Murthy, C. S. Rani, T. Nanuvala, C. R. Kumar, and G. Sathar, \"Automated Dog Breed Recognition Using CNN-Based Transfer Learning,\" in <i>Proc. Int. Conf. on Advances in Computer Engineering & Communication Systems</i>, 2025.",
        "[9] A. S. Ghotra, H. Kour, A. Hasan, and A. Khan, \"Dog Breed Identification,\" in <i>Proc. Int. Conf. on Data Science and Machine Learning</i>, 2023.",
        "[10] J. Bankar, A. Nalawade, S. Wali, A. Rane, and H. Matlani, \"AI Based Dog Breed Prediction Model and Virtual Canine Hub,\" <i>International Journal of Computer Applications</i>, vol. 186, no. 14, 2025.",
        "[11] D.-N. Zou, S.-H. Zhang, T.-J. Mu, and M. Zhang, \"A New Dataset of Dog Breed Images and a Benchmark for Fine-Grained Classification,\" <i>Computational Visual Media</i>, vol. 6, no. 4, pp. 477–487, 2020.",
        "[12] P. Perera and V. M. Patel, \"Deep Transfer Learning for Multiple Class Novelty Detection,\" in <i>Proc. IEEE/CVF Conf. on Computer Vision and Pattern Recognition (CVPR)</i>, 2019, pp. 1154–1162.",
        "[13] A. Khosla, N. Jayadevaprakash, B. Yao, and L. Fei-Fei, \"Novel Dataset for Fine-Grained Image Categorization: Stanford Dogs,\" in <i>Proc. CVPR Workshop on Fine-Grained Visual Categorization</i>, 2011.",
        "[14] M. Sandler, A. Howard, M. Zhu, A. Zhmoginov, and L.-C. Chen, \"MobileNetV2: Inverted Residuals and Linear Bottlenecks,\" in <i>Proc. IEEE/CVF Conf. on Computer Vision and Pattern Recognition (CVPR)</i>, 2018, pp. 4510–4520.",
        "[15] M. Abadi et al., \"TensorFlow: A System for Large-Scale Machine Learning,\" in <i>Proc. 12th USENIX Symp. on Operating Systems Design and Implementation (OSDI)</i>, 2016, pp. 265–283.",
        "[16] A. Grinberg, <i>Flask Web Development: Developing Web Applications with Python</i>, 2nd ed. Sebastopol, CA: O'Reilly Media, 2018.",
        "[17] ReportLab Europe Ltd., <i>ReportLab PDF Generation User Guide</i>, Version 5.1, London, UK, 2024.",
        "[18] Oracle Corporation, <i>MySQL 8.0 Reference Manual</i>, Redwood Shores, CA: Oracle, 2024."
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
    story.append(Paragraph("TEAM CONTRIBUTIONS", h1_style))
    story.append(Paragraph("This project was developed collaboratively by a team of four B.Tech Data Science students. While all members participated in integration testing, review milestones, and academic documentation, individual module responsibilities were structured as follows:", body_style))

    tc_headers = [Paragraph("Team Member", tbl_header_style), Paragraph("Roll Number", tbl_header_style), Paragraph("Verified Individual Module Contributions", tbl_header_style)]
    tc_data = [
        tc_headers,
        [Paragraph("K Goutham Nayak", tbl_cell_bold), Paragraph("CS24B1081", tbl_cell_bold_center), Paragraph("<b>Backend Architecture & Database Integration:</b> Designed Flask REST routes, implemented MySQL relational schema, user authentication, role-based access control, and automated PDF report generation.", tbl_cell_style)],
        [Paragraph("K Adithya", tbl_cell_bold), Paragraph("CS24B1091", tbl_cell_bold_center), Paragraph("<b>Deep Learning & Model Training:</b> Conducted MobileNetV2 transfer learning, two-phase fine-tuning, loss optimization, and evaluation metrics compilation (Top-1, Top-5, Confusion Matrix).", tbl_cell_style)],
        [Paragraph("R Mahesh Rathod", tbl_cell_bold), Paragraph("CS24B1071", tbl_cell_bold_center), Paragraph("<b>Two-Stage Pipeline & Canine Detector:</b> Formulated the Stage 1 ImageNet canine presence filter, threshold tuning (P ≥ 0.20), and non-dog validation test suite.", tbl_cell_style)],
        [Paragraph("G Vishnu Vardhan", tbl_cell_bold), Paragraph("CS24B1028", tbl_cell_bold_center), Paragraph("<b>Frontend Development & UI/UX:</b> Developed responsive CSS cream-and-brown interface, drag-and-drop upload logic, interactive breed comparison tool, and Chart.js dashboard integration.", tbl_cell_style)]
    ]
    t_team_c = Table(tc_data, colWidths=[110, 85, 320])
    t_team_c.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_header_bg),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_alt_row])
    ]))
    story.append(t_team_c)

    story.append(Paragraph("Shared Group Responsibilities", h2_style))
    story.append(Paragraph("• <b>Literature Survey:</b> Extracted and evaluated methodology, datasets, and limitations across 12 research papers on canine classification.<br/>"
                           "• <b>Dataset Partitioning:</b> Performed stratified 70/15/15 train-val-test splitting and image integrity checks on 10,222 images.<br/>"
                           "• <b>Software Verification:</b> Executed and passed all 18 automated tests in <code>run_complete_tests.py</code>, verifying zero system regressions.<br/>"
                           "• <b>Academic Documentation:</b> Authored and proofread the comprehensive B.Tech final project report.", body_style))

    # Build PDF
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"[OK] Generated PDF Report: {output_path}")

if __name__ == '__main__':
    create_pdf('Dog_Breed_Identification_Project_Report.pdf')
