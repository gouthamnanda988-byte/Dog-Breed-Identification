"""
generate_docx_report.py
=======================
Generates a professional academic Word (.docx) project report for:
DOG BREED IDENTIFICATION USING DEEP LEARNING AND TRANSFER LEARNING

Features:
- Academic cover page with student details & placeholders
- Formal Table of Contents, List of Figures, List of Tables
- 1.5 line spacing, Times New Roman font, justified paragraphs
- Formatted tables with shaded headers and clean borders
- Embedded high-resolution diagrams and charts
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
    """Set background color of a table cell."""
    tc_pr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>')
    tc_pr.append(shd)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    """Set internal cell padding."""
    tc_pr = cell._tc.get_or_add_tcPr()
    tc_mar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="{top}" w:type="dxa"/><w:bottom w:w="{bottom}" w:type="dxa"/><w:left w:w="{left}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/></w:tcMar>')
    tc_pr.append(tc_mar)

def create_docx(output_path):
    doc = Document()

    # Page Setup (A4, 1-inch margins)
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
        r.font.color.rgb = RGBColor(0x3E, 0x25, 0x15)
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
        r.font.color.rgb = RGBColor(0x5C, 0x3A, 0x1E)
        return h

    def add_h3(title):
        h = doc.add_heading(level=3)
        h.paragraph_format.space_before = Pt(10)
        h.paragraph_format.space_after = Pt(4)
        h.paragraph_format.keep_with_next = True
        r = h.add_run(title)
        r.font.name = 'Times New Roman'
        r.font.size = Pt(12.5)
        r.font.bold = True
        r.font.color.rgb = RGBColor(0x6D, 0x48, 0x28)
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
            r.font.size = Pt(10.5)
            r.italic = True
            r.font.color.rgb = RGBColor(0x44, 0x44, 0x44)

    # =========================================================================
    # 1. TITLE / COVER PAGE
    # =========================================================================
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_before = Pt(36)
    p_title.paragraph_format.space_after = Pt(12)
    r = p_title.add_run("DOG BREED IDENTIFICATION USING DEEP LEARNING AND TRANSFER LEARNING")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(22)
    r.font.bold = True
    r.font.color.rgb = RGBColor(0x3E, 0x25, 0x15)

    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_sub.paragraph_format.space_after = Pt(30)
    r = p_sub.add_run("A Project Report Submitted in Partial Fulfillment of the Requirements\nfor the Degree of Bachelor of Technology in Data Science / Computer Science and Engineering")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(13)
    r.italic = True

    p_by = doc.add_paragraph()
    p_by.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_by.paragraph_format.space_after = Pt(8)
    r = p_by.add_run("Submitted by:")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(13)
    r.bold = True

    # Student Table on Cover Page
    t_team = doc.add_table(rows=5, cols=2)
    t_team.alignment = WD_TABLE_ALIGNMENT.CENTER
    team_data = [
        ("Candidate Name", "Roll / Registration Number"),
        ("K Goutham Nayak", "CS24B1081"),
        ("K Adithya", "CS24B1091"),
        ("R Mahesh Rathod", "CS24B1071"),
        ("G Vishnu Vardhan", "CS24B1028")
    ]
    for row_idx, (c1, c2) in enumerate(team_data):
        row = t_team.rows[row_idx]
        row.cells[0].width = Inches(3.2)
        row.cells[1].width = Inches(2.5)
        p1 = row.cells[0].paragraphs[0]
        p1.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p2 = row.cells[1].paragraphs[0]
        p2.alignment = WD_ALIGN_PARAGRAPH.CENTER
        
        r1 = p1.add_run(c1)
        r2 = p2.add_run(c2)
        r1.font.name = 'Times New Roman'
        r2.font.name = 'Times New Roman'
        
        if row_idx == 0:
            set_cell_background(row.cells[0], "F5EBDA")
            set_cell_background(row.cells[1], "F5EBDA")
            r1.bold = True
            r2.bold = True
        set_cell_margins(row.cells[0], 60, 60, 100, 100)
        set_cell_margins(row.cells[1], 60, 60, 100, 100)

    p_guide = doc.add_paragraph()
    p_guide.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_guide.paragraph_format.space_before = Pt(36)
    p_guide.paragraph_format.space_after = Pt(4)
    r = p_guide.add_run("Under the Guidance of:")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(12)
    r.bold = True

    p_guide_name = doc.add_paragraph()
    p_guide_name.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_guide_name.paragraph_format.space_after = Pt(30)
    r = p_guide_name.add_run("[Faculty Guide Name, Designation]\n[Department of Computer Science and Engineering / Data Science]")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(12)

    p_inst = doc.add_paragraph()
    p_inst.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_inst.paragraph_format.space_before = Pt(20)
    p_inst.paragraph_format.space_after = Pt(0)
    r = p_inst.add_run("[Department of Computer Science and Engineering / Data Science]\n[Institution / College Name, Affiliated to University Name]\n[Academic Year: 2025 – 2026]")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(13)
    r.bold = True

    doc.add_page_break()

    # =========================================================================
    # CERTIFICATE & DECLARATION PLACEHOLDERS
    # =========================================================================
    add_h1("BONAFIDE CERTIFICATE")
    add_p("This is to certify that the project report entitled \"DOG BREED IDENTIFICATION USING DEEP LEARNING AND TRANSFER LEARNING\" is a bonafide work carried out by K Goutham Nayak (CS24B1081), K Adithya (CS24B1091), R Mahesh Rathod (CS24B1071), and G Vishnu Vardhan (CS24B1028) in partial fulfillment of the requirements for the award of the degree of Bachelor of Technology in Computer Science and Engineering / Data Science during the academic year 2025–2026.")
    
    p_sign = doc.add_paragraph()
    p_sign.paragraph_format.space_before = Pt(60)
    p_sign.paragraph_format.space_after = Pt(20)
    p_sign.add_run("[Internal Guide Signature]                                         [Head of Department Signature]\n[Guide Name, Designation]                                       [HOD Name, Department]")

    add_h1("CANDIDATE DECLARATION")
    add_p("We hereby declare that the project entitled \"DOG BREED IDENTIFICATION USING DEEP LEARNING AND TRANSFER LEARNING\" submitted to [Institution Name] is an authentic record of our own research and engineering work carried out under the guidance of [Guide Name]. We confirm that the results embodied in this report have not been submitted to any other university or institute for the award of any degree or diploma.")
    
    p_cand_sign = doc.add_paragraph()
    p_cand_sign.paragraph_format.space_before = Pt(40)
    p_cand_sign.paragraph_format.space_after = Pt(10)
    p_cand_sign.add_run("1. K Goutham Nayak (CS24B1081)  ____________________\n\n"
                        "2. K Adithya (CS24B1091)        ____________________\n\n"
                        "3. R Mahesh Rathod (CS24B1071)  ____________________\n\n"
                        "4. G Vishnu Vardhan (CS24B1028) ____________________\n\n"
                        "Date: [Date of Submission]\nPlace: [College Location]")

    doc.add_page_break()

    # =========================================================================
    # ABSTRACT
    # =========================================================================
    add_h1("ABSTRACT")
    add_p("Accurately classifying domestic canine breeds from digital photographs represents one of the most prominent fine-grained visual classification challenges in modern computer vision. Unlike generic object recognition where classes differ fundamentally in shape and silhouette (such as vehicles versus animals), canine identification must contend with two difficult phenomena: high intra-class variance, where dogs of the same breed exhibit significant variations in coat patterns, grooming styles, age, and postures, and low inter-class variance, where biologically distinct breeds share nearly indistinguishable anatomical silhouettes and facial profiles (for instance, Whippets and Italian Greyhounds, or Lhasa Apsos and Shih-Tzus).")
    
    add_p("In this project, we designed, implemented, and thoroughly evaluated an end-to-end canine classification web platform powered by transfer learning with MobileNetV2 and backed by a full-stack relational database. Built upon the Stanford Dogs / Kaggle Dog Breed Identification benchmark comprising 10,222 labeled images partitioned into a stratified 70% training (7,155 images), 15% validation (1,533 images), and 15% testing (1,534 images) split across 120 purebred categories, our architecture employs an innovative two-stage prediction pipeline. In Stage 1, an ImageNet-pretrained MobileNetV2 classifier validates canine presence by monitoring 118 domestic and wild dog output indices, immediately rejecting non-dog uploads (such as horses, felines, or inanimate objects) with a friendly alert. In Stage 2, images confirmed as dogs are evaluated by our fine-tuned MobileNetV2 model equipped with Global Average Pooling, 30% dropout regularization, and a 120-unit Softmax classification layer.")

    add_p("Our model achieved an empirical 77.64% Top-1 test accuracy, an exceptional 96.87% Top-5 test accuracy, and a test loss of 0.7036 across the 1,534 held-out evaluation images. Beyond the neural network, we integrated a full-stack Flask web application providing drag-and-drop image prediction with Top-3 ranked candidate scores, a 120-breed interactive directory, side-by-side trait comparison, ReportLab automated PDF prediction report downloads, personal MySQL history tracking, and a role-based administrative analytics dashboard. This platform provides an accessible, robust, and educational solution for veterinary clinics, rescue shelters, and pet owners.")

    doc.add_page_break()

    # =========================================================================
    # TABLE OF CONTENTS
    # =========================================================================
    add_h1("TABLE OF CONTENTS")
    toc_items = [
        ("Abstract", "iv"),
        ("List of Figures", "vi"),
        ("List of Tables", "vii"),
        ("CHAPTER 1 – INTRODUCTION", "1"),
        ("    1.1 Background", "1"),
        ("    1.2 Problem Statement", "2"),
        ("    1.3 Motivation", "3"),
        ("    1.4 Project Objectives", "3"),
        ("    1.5 Scope of the Project", "4"),
        ("    1.6 Existing System and Proposed System", "4"),
        ("    1.7 Organization of the Report", "5"),
        ("CHAPTER 2 – LITERATURE SURVEY", "6"),
        ("    2.1 Review of Related Research Papers (12 Papers)", "6"),
        ("    2.2 Comparative Literature Analysis Table", "12"),
        ("    2.3 Research Gap Analysis", "13"),
        ("    2.4 How the Proposed Project Addresses the Gaps", "14"),
        ("CHAPTER 3 – DATASET", "15"),
        ("    3.1 Dataset Description and Origin", "15"),
        ("    3.2 Breed Categories and Class Hierarchy", "15"),
        ("    3.3 Dataset Distribution and Partitioning", "16"),
        ("    3.4 Image Preprocessing Pipeline", "18"),
        ("    3.5 Data Augmentation Strategy", "18"),
        ("    3.6 Dataset Challenges and Observations", "19"),
        ("CHAPTER 4 – METHODOLOGY", "20"),
        ("    4.1 Overall System Architecture", "20"),
        ("    4.2 Two-Stage Prediction Pipeline", "21"),
        ("    4.3 Convolutional Neural Networks and Transfer Learning", "23"),
        ("    4.4 Image Preprocessing and Normalization", "25"),
        ("    4.5 Two-Phase Model Training Procedure", "25"),
        ("    4.6 Flask Web Application Architecture", "27"),
        ("    4.7 Relational Database Design and Schema", "28"),
        ("    4.8 User Authentication and Access Control", "30"),
        ("    4.9 Additional Features and Utilities", "31"),
        ("    4.10 Technologies and Frameworks Used", "32"),
        ("    4.11 System Workflow and User Journey", "33"),
        ("    4.12 Algorithmic Pseudocode", "34"),
        ("CHAPTER 5 – EXPERIMENTAL RESULTS AND DISCUSSION", "36"),
        ("    5.1 Experimental Environment", "36"),
        ("    5.2 Training Convergence Results", "36"),
        ("    5.3 Model Evaluation Metrics", "38"),
        ("    5.4 Prediction Results and Confidence Breakdown", "39"),
        ("    5.5 Dog and Non-Dog Presence Verification", "40"),
        ("    5.6 Commonly Confused Breeds Analysis", "41"),
        ("    5.7 Automated Application Test Suite (18 Test Cases)", "43"),
        ("    5.8 Performance Analysis and System Latency", "45"),
        ("    5.9 Practical Limitations", "45"),
        ("CHAPTER 6 – CONCLUSION AND FUTURE WORK", "47"),
        ("    6.1 Conclusion", "47"),
        ("    6.2 Future Work Roadmap", "48"),
        ("REFERENCES", "49"),
        ("TEAM CONTRIBUTIONS", "52")
    ]
    t_toc = doc.add_table(rows=len(toc_items), cols=2)
    t_toc.alignment = WD_TABLE_ALIGNMENT.CENTER
    for idx, (section_title, page_num) in enumerate(toc_items):
        r = t_toc.rows[idx]
        r.cells[0].width = Inches(5.5)
        r.cells[1].width = Inches(1.0)
        p1 = r.cells[0].paragraphs[0]
        p1.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p2 = r.cells[1].paragraphs[0]
        p2.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        
        run1 = p1.add_run(section_title)
        run2 = p2.add_run(page_num)
        run1.font.name = 'Times New Roman'
        run2.font.name = 'Times New Roman'
        if "CHAPTER" in section_title or "ABSTRACT" in section_title or "REFERENCES" in section_title or "TEAM" in section_title:
            run1.bold = True
            run2.bold = True
        set_cell_margins(r.cells[0], 20, 20, 40, 40)
        set_cell_margins(r.cells[1], 20, 20, 40, 40)

    doc.add_page_break()

    # =========================================================================
    # CHAPTER 1 - INTRODUCTION
    # =========================================================================
    add_h1("CHAPTER 1 – INTRODUCTION")
    
    add_h2("1.1 Background")
    add_p("Image classification is a foundational task in computer vision that seeks to assign an input image to one of several predefined categories based on visual characteristics. Over the past decade, Convolutional Neural Networks (CNNs) have revolutionized image classification by automatically discovering hierarchical feature representations directly from raw pixel arrays—moving from primitive edges and textures in initial convolutional layers to complex semantic parts and object contours in deeper layers.")
    add_p("Within the visual recognition domain, canine breed classification belongs to the specialized field of Fine-Grained Visual Categorization (FGVC). Unlike coarse-grained classification (such as distinguishing a dog from a car or a tree), fine-grained recognition demands that a computational system discriminate between subtle sub-categories belonging to the exact same biological species (Canis lupus familiaris). Domestic dogs represent the most morphologically diverse terrestrial mammal on Earth, with hundreds of purebred varieties developed through centuries of selective breeding. Building an automated system that accurately distinguishes between 120 purebred categories holds significant academic and practical value.")

    add_h2("1.2 Problem Statement")
    add_p("Manually identifying dog breeds from photographs is remarkably challenging and prone to error, even for experienced veterinarians, canine kennel judges, and animal shelter workers. The primary difficulties stem from:")
    add_p("1. Low Inter-Class Variance: Different breeds that share ancestral lineages or functional traits often possess nearly identical visual appearances. For example, a Whippet and an Italian Greyhound share identical slender sighthound posture and sleek short coats; a Siberian Husky and an Eskimo Dog share identical erect triangular ears and curled tails; a Lhasa Apso and a Shih-Tzu share long facial hair that obscures facial bone structures.")
    add_p("2. High Intra-Class Variance: Dogs of the same recognized breed can display substantial differences in coat coloration, fur texture, grooming cuts, body weight, ear posture, and lighting conditions.")
    add_p("3. Background Clutter and Occlusions: User-uploaded photographs frequently feature outdoor environments, household clutter, human handlers, or awkward camera angles that obscure key diagnostic breed features.")
    add_p("4. Non-Dog False Predictions: Conventional single-stage classifiers force any uploaded image into one of the 120 dog categories, producing misleading predictions when users upload non-dog subjects.")
    add_p("Therefore, an automated, reliable, and user-friendly system is required that can first verify whether a photograph contains a canine, and then accurately identify the breed with ranked probability scores and detailed breed profiles.")

    add_h2("1.3 Motivation")
    add_p("The motivation for undertaking this capstone project is both academic and practical:")
    add_p("- Veterinary and Clinical Utility: Animal clinics, rescue shelters, and pet insurance agencies frequently require accurate breed determination to anticipate hereditary health vulnerabilities (e.g., hip dysplasia in German Shepherds, respiratory issues in brachycephalic breeds like Pugs).")
    add_p("- Lost and Found Animal Recovery: In municipal shelters, correctly identifying a lost dog's breed accelerates matching with owner lost-pet reports.")
    add_p("- Academic Exploration of Transfer Learning: As B.Tech Data Science students, fine-grained visual classification provided an ideal real-world problem to study transfer learning, deep convolutional architectures, overfitting mitigation, relational database integration, and web software engineering.")

    add_h2("1.4 Project Objectives")
    add_p("The primary objectives of this project are:")
    add_p("1. To develop a two-stage computer vision inference pipeline that first verifies canine presence and then performs fine-grained classification.")
    add_p("2. To classify canine images accurately across all 120 breeds represented in the benchmark Stanford Dogs dataset.")
    add_p("3. To leverage transfer learning with MobileNetV2 to achieve high diagnostic accuracy with lightweight parameter requirements suitable for rapid CPU-based web inference.")
    add_p("4. To display ranked Top-3 candidate breed predictions accompanied by visual confidence percentages.")
    add_p("5. To construct an interactive, responsive web portal using Python Flask and modern CSS allowing drag-and-drop image uploads.")
    add_p("6. To implement a secure MySQL relational database storing user accounts, individual prediction history, bookmarked favorites, and feedback.")
    add_p("7. To generate downloadable academic-grade PDF prediction reports using ReportLab.")
    add_p("8. To develop an interactive breed directory and side-by-side trait comparison tool across all 120 classes.")
    add_p("9. To provide transparent model performance evaluation pages with interactive Chart.js graphs and commonly confused breed analyses.")
    add_p("10. To validate the entire software application using an automated 18-point verification test suite.")

    add_h2("1.5 Scope of the Project")
    add_p("- Target Categories: 120 recognized purebred dog breeds as defined by the Stanford Dogs benchmark.")
    add_p("- Input Modality: Single-subject canine photographs in JPG, JPEG, or PNG formats up to 10 MB in file size.")
    add_p("- Core Processing: 224 x 224 RGB image normalization and inference via TensorFlow / Keras MobileNetV2.")
    add_p("- Web Interface: Cross-browser responsive web application accessible on desktop, tablet, and mobile viewport widths.")
    add_p("- System Boundaries: The current system is designed for single-dog photographs and does not support multi-dog instance segmentation or mixed-breed genetic percentage estimation.")

    add_h2("1.6 Existing System and Proposed System")
    add_p("The following table contrasts the capabilities of conventional manual or desktop identification approaches with our proposed full-stack deep learning solution:")

    # Comparison Table
    t_comp = doc.add_table(rows=8, cols=3)
    t_comp.alignment = WD_TABLE_ALIGNMENT.CENTER
    comp_headers = ["Feature / Dimension", "Conventional / Existing Systems", "Our Proposed Implementation"]
    comp_rows = [
        ("Identification Method", "Manual visual inspection by kennel books or expert veterinarians", "Automated two-stage deep learning inference pipeline"),
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
        set_cell_background(cell, "F5EBDA")
        set_cell_margins(cell, 80, 80, 100, 100)
    for r_idx, (f1, f2, f3) in enumerate(comp_rows):
        row = t_comp.rows[r_idx + 1]
        for c_idx, val in enumerate([f1, f2, f3]):
            cell = row.cells[c_idx]
            cell.paragraphs[0].text = val
            set_cell_margins(cell, 60, 60, 80, 80)
            if r_idx % 2 == 1:
                set_cell_background(cell, "FFFDF9")

    add_h2("1.7 Organization of the Report")
    add_p("The remainder of this report is organized as follows: Chapter 2 reviews 12 seminal research papers in fine-grained canine classification and transfer learning, presenting a comparative table and identifying research gaps. Chapter 3 details the dataset acquisition, partitioning, class distribution, and data augmentation. Chapter 4 provides a comprehensive walkthrough of our methodology, encompassing the two-stage inference pipeline, MobileNetV2 architecture, Flask application routing, relational MySQL schema, and security mechanisms. Chapter 5 presents experimental results, training convergence curves, Top-1/Top-5 evaluation metrics, confused breed analyses, and the 18-point automated test suite. Finally, Chapter 6 concludes the report and discusses a realistic roadmap for future enhancements.")

    doc.add_page_break()

    # =========================================================================
    # CHAPTER 2 - LITERATURE SURVEY
    # =========================================================================
    add_h1("CHAPTER 2 – LITERATURE SURVEY")
    add_p("Fine-grained visual categorization has received substantial attention within the deep learning and computer vision research communities. In this chapter, we review twelve peer-reviewed research papers investigating canine classification, transfer learning architectures, dataset engineering, and out-of-distribution novelty detection.")

    add_h2("2.1 Review of Related Research Papers")
    
    # Paper 1
    add_h3("1. Selvaraj et al. (2023) – ResNet50 Architecture Based Dog Breed Identification Using Deep Learning")
    add_p("Selvaraj S, Thangarajan R, Anbukkarasi S, and Yuvan Prasad S investigated automated dog breed identification to accelerate visual inspection using deep convolutional architectures. The authors employed the Stanford Dogs Dataset (10,222 images covering 120 breeds) and trained a Convolutional Neural Network built upon the ResNet50 backbone. ResNet50 utilizes deep residual connections that bypass convolutional layers, effectively mitigating the vanishing gradient problem in deep networks. The authors comparatively benchmarked ResNet50 against NASNet, InceptionV3, MobileNetV2, MobileNet, DenseNet121, and AlexNet. Their experimental findings revealed that ResNet50 achieved the highest overall classification accuracy among the evaluated models, attaining approximately 93% accuracy. However, the study noted that residual networks require substantial memory footprints and extensive labeled training samples; furthermore, classification accuracy degraded on breeds not represented within the training corpus.")
    
    # Paper 2
    add_h3("2. Borwarnginn et al. (2021) – Knowing Your Dog Breed: Identifying a Dog Breed with Deep Learning")
    add_p("Borwarnginn, Kusakunniran, Karnjanapreechakorn, and Thongkanchorn evaluated canine breed recognition focusing specifically on facial regions rather than full-body photographs. Utilizing the Columbia Dogs Dataset comprising 8,351 images across 133 breeds (8,111 images utilized after quality filtering), the authors explored deep transfer learning to maximize performance under limited sample availability. They pre-cropped canine faces and trained MobileNetV2, InceptionV3, and NASNet models coupled with geometric data augmentation (rotation, translation, horizontal flipping, and Gaussian noise injection). Their key finding was that NASNet achieved the highest classification accuracy at 89.92%, with data augmentation yielding measurable gains across all architectures. The primary limitation was the strict dependency on facial localization: off-angle poses, floppy ear occlusions, or failed crops directly caused misclassifications.")

    # Paper 3
    add_h3("3. Bokhari et al. (2022) – Convolutional Neural Network Based Dog Breed Classification")
    add_p("Bokhari, Mukherjee, Singh, Shaik, and Mathew explored transfer learning using a pretrained MobileNetV2 model on the Stanford Dogs dataset (10,222 training and 10,357 testing images across 120 breeds). Their primary objective was to minimize training resource requirements while achieving competitive breed categorization. The authors divided images into mini-batches and leveraged MobileNetV2's depthwise separable convolutional blocks for feature extraction. Their results revealed an important scaling insight: while the model achieved nearly 85% accuracy when restricted to 50 common breeds, accuracy dropped precipitously to 64% when scaled across 120 breeds. The authors identified background clutter and class imbalance as primary failure drivers, suggesting data masking and deeper fine-tuning as essential remedies.")

    # Paper 4
    add_h3("4. Kumaravel et al. (2023) – Automatic Dog Breed Classification Using Deep Learning")
    add_p("Kumaravel, Natesan, Sathishkumar, Shri, Swathy, and Uvetha conducted an extensive benchmark of deep learning classifiers on an expanded canine image corpus. Combining Stanford Dogs and Kaggle repositories, the authors synthesized a dataset of approximately 120,000 images using extensive horizontal flipping, padding, random cropping, and rotation, partitioned into an 80/10/10 split. They tested MobileNetV2, InceptionV3, Xception, and DenseNet201 resized to 224 x 224 x 3 pixels. Their findings indicated that DenseNet201 yielded the best performance, attaining 87.34% accuracy due to iterative feature concatenation across dense blocks. A key limitation observed was diminishing performance returns when extending training epochs beyond saturation, indicating that dataset diversity and feature resolution bounded final accuracy.")

    # Paper 5
    add_h3("5. Banakar et al. (2023) – Dog Breed Identification Using Deep Learning")
    add_p("Banakar, Raghavendra, Sindhu, Vani, and Vishnu evaluated fine-grained canine identification for breeding research and clinical documentation. Using the 120-class Stanford Dogs dataset, the authors applied transfer learning across VGG-19 and Inception-ResNet V2 backbones. Normalized images were routed through deep feature extractors and classified using multi-layer perceptrons, integrated into a client-server architecture with a mobile client and web server. The authors reported that VGG-19 provided strong discriminative power when fine-tuned on canine images. However, the excessive parameter count of VGG-19 (~143 million parameters, ~550 MB storage) caused high computational latency during inference, reinforcing the need for lightweight alternatives during production web deployment.")

    # Paper 6
    add_h3("6. Valarmathi et al. (2023) – Hybrid Deep Learning Algorithms for Dog Breed Identification—A Comparative Analysis")
    add_p("Valarmathi, Gupta, Prakash, Reddy, Saravanan, and Shanmugasundaram investigated whether hybrid multi-model ensembles could outperform standalone deep learning architectures. Using the 10,222-image Stanford Dogs benchmark, the authors evaluated standalone backbones (Xception, VGG19, NASNetMobile, EfficientNetV2M, ResNet152V2) and formulated two hybrid models: (1) Inception-v3 + Xception, and (2) EfficientNetV2M + NASNetMobile + Inception + Xception. The hybrid Inception-v3 + Xception ensemble attained the top validation accuracy of 92.4% (98.4% training accuracy). Standalone architectures achieved Xception 91.9%, EfficientNetV2M 89.05%, ResNet152V2 87.38%, and NASNetMobile 83.47%. Despite superior accuracy, the hybrid ensembles suffered from massive computational demands and long inference delays, rendering real-time web hosting unfeasible without specialized GPU infrastructure.")

    # Paper 7
    add_h3("7. Basha et al. (2021) – Dogs Breed Classification Using Deep Learning")
    add_p("Basha, Ganesh, Reddy, and Hans implemented a PyTorch-based convolutional classification system using pretrained VGG16 weights. The authors emphasized eliminating manual feature extraction by leveraging convolutional filters that learn visual patterns hierarchically. Their experiments proved that transfer learning significantly accelerated convergence and achieved superior accuracy compared to training CNNs from random initialization. However, the study noted that extreme intra-breed variance (color morphs, coat patterns) and illumination shifts caused notable misclassifications, recommending that confidence scores be shared with users rather than hard decisions.")

    # Paper 8
    add_h3("8. Hussain et al. (2025) – Automated Dog Breed Recognition Using CNN-Based Transfer Learning")
    add_p("Hussain, Murthy, Rani, Nanuvala, Kumar, and Sathar addressed the disruptive effect of background clutter in fine-grained canine recognition. Evaluating 20,580 images from the extended Stanford Dogs dataset across VGG16, ResNet50, InceptionV3, and Inception-ResNet V2 at 299 x 299 resolution, the authors applied automated background subtraction alongside rotation, zooming, and brightness adjustments. InceptionV3 achieved the highest classification accuracy of 91.2%. The authors proved that background removal substantially reduced false correlations with outdoor grass or indoor carpets, although occasional clipping of canine ear contours was observed.")

    # Paper 9
    add_h3("9. Ghotra et al. (2023) – Dog Breed Identification")
    add_p("Ghotra, Kour, Hasan, and Khan designed a lightweight, rapid canine classification pipeline deployed as a web application. Using the Kaggle Dog Breed dataset (>10,222 images, 120 breeds), the authors employed TensorFlow MobileNetV2 as a lightweight feature extractor. Hyperparameters were tuned across batch sizes and learning rates, and the trained model was served via Flask and Ngrok tunnels. The authors reported a training accuracy of 99.89% and highlighted MobileNetV2's compact parameter footprint as ideal for web serving. However, the near-perfect training accuracy suggested potential overfitting, and the system lacked any input validation mechanism for non-dog photographs.")

    # Paper 10
    add_h3("10. Bankar et al. (2025) – AI Based Dog Breed Prediction Model and Virtual Canine Hub")
    add_p("Bankar, Nalawade, Wali, Rane, and Matlani developed an interactive canine portal combining breed classification with facial keypoint detection and care guides. Operating on an online dataset of 8,350 images across 133 breeds, their CNN detected anatomical landmarks (eyes, nose, ears) with an average localization error of 4.62 pixels. While the model achieved 90% training accuracy, its testing accuracy dropped sharply to 70%, revealing a substantial 20% generalization gap. Occluded ears, dark facial coats, and multi-dog photos frequently caused classification failures.")

    # Paper 11
    add_h3("11. Zou et al. (2020) – A New Dataset of Dog Breed Images and a Benchmark for Fine-Grained Classification")
    add_p("Zou, Zhang, Mu, and Zhang established the Tsinghua Dogs Dataset, introducing 70,428 unconstrained real-world images covering 130 breeds with full-body and head bounding boxes. The authors benchmarked leading fine-grained architectures: Weakly Supervised Data Augmentation Network (WS-DAN), Progressive Multi-Granularity Network (PMG), Trilinear Attention Network (TBMSL-Net), and InceptionV3. WS-DAN attained 86.4% accuracy, followed by TBMSL-Net (83.7%) and PMG (83.5%). Their study established that unconstrained real-world photographs are significantly more challenging than clean benchmarks, underscoring the necessity of Top-5 evaluation metrics.")

    # Paper 12
    add_h3("12. Perera & Patel (2019) – Deep Transfer Learning for Multiple Class Novelty Detection")
    add_p("Perera and Patel formulated a deep transfer learning framework for out-of-distribution novelty detection across Caltech-256, CUB-200, and Stanford Dogs (20,580 images, 120 breeds partitioned into known and novel sets). By integrating membership loss, globally negative filters, and activation thresholding, the network evaluates whether an input belongs to a recognized class or an unseen novelty. On Stanford Dogs, the authors achieved an Area Under Curve (AUC) of 0.825 using VGG16, while improving closed-set classification accuracy to 80.1%. Their methodology provided theoretical validation for our Stage 1 canine presence filter.")

    add_h2("2.2 Comparative Literature Analysis")
    add_p("The table below presents a structured comparative analysis of the twelve surveyed research papers:")

    # Lit Table
    t_lit = doc.add_table(rows=13, cols=6)
    t_lit.alignment = WD_TABLE_ALIGNMENT.CENTER
    lit_headers = ["Paper & Authors", "Year", "Model / Technique", "Dataset Used", "Reported Result", "Key Limitation"]
    lit_data = [
        ("Selvaraj et al.", "2023", "ResNet50 Transfer Learning", "Stanford Dogs (10,222 images)", "93.0% Accuracy", "High compute cost; 120 breeds only"),
        ("Borwarnginn et al.", "2021", "NASNet + Face Cropping", "Columbia Dogs (8,111 images)", "89.92% Accuracy", "Fails if facial crop fails"),
        ("Bokhari et al.", "2022", "MobileNetV2 Feature Extractor", "Stanford Dogs (120 breeds)", "85.0% (50 breeds) / 64% (120)", "Steep drop on scaling to 120 classes"),
        ("Kumaravel et al.", "2023", "DenseNet201 + Augmentation", "Stanford + Kaggle (120k aug)", "87.34% Accuracy", "Diminishing returns beyond saturation"),
        ("Banakar et al.", "2023", "VGG-19 + Client/Server", "Stanford Dogs (120 breeds)", "High fine-tuned accuracy", "Bulky model weights (~550 MB)"),
        ("Valarmathi et al.", "2023", "Hybrid InceptionV3 + Xception", "Stanford Dogs (10,222 images)", "92.4% Val Acc (98.4% Train)", "Massive compute cost; slow inference"),
        ("Basha et al.", "2021", "VGG16 in PyTorch", "Canine breed image set", "CNN representation verified", "Vulnerable to lighting and pose shifts"),
        ("Hussain et al.", "2025", "InceptionV3 + Background Removal", "Stanford Dogs (20,580 images)", "91.2% Accuracy", "Segmentation clips anatomical edges"),
        ("Ghotra et al.", "2023", "MobileNetV2 + Flask + Ngrok", "Kaggle Dog Breeds (>10,222)", "99.89% Train Accuracy", "High overfitting risk; no non-dog check"),
        ("Bankar et al.", "2025", "CNN + Facial Keypoint Hub", "Online set (8,350 images)", "90% Train / 70% Test", "Severe 20% overfitting gap"),
        ("Zou et al.", "2020", "WS-DAN, TBMSL-Net, PMG", "Tsinghua Dogs (70,428 images)", "WS-DAN: 86.4%, TBMSL: 83.7%", "Complex multi-stage attention networks"),
        ("Perera & Patel", "2019", "Deep Novelty Detection", "Stanford Dogs + Multi-dataset", "AUC: 0.825, Acc: 80.1%", "Sensitive to activation thresholds")
    ]
    for c_idx, h_text in enumerate(lit_headers):
        cell = t_lit.rows[0].cells[c_idx]
        cell.paragraphs[0].text = h_text
        cell.paragraphs[0].runs[0].bold = True
        set_cell_background(cell, "F5EBDA")
        set_cell_margins(cell, 80, 80, 80, 80)
    for r_idx, row_vals in enumerate(lit_data):
        row = t_lit.rows[r_idx + 1]
        for c_idx, val in enumerate(row_vals):
            cell = row.cells[c_idx]
            cell.paragraphs[0].text = val
            set_cell_margins(cell, 50, 50, 60, 60)
            if r_idx % 2 == 1:
                set_cell_background(cell, "FFFDF9")

    add_h2("2.3 Research Gap Analysis")
    add_p("A rigorous synthesis of the surveyed literature reveals several unresolved challenges:")
    add_p("1. Complete Absence of Out-of-Distribution Input Verification: All surveyed web applications (Ghotra et al., Banakar et al., Bankar et al.) assume that the user will only upload valid dog photographs. Uploading an image of a cat, a horse, or a vehicle results in arbitrary, high-confidence canine misclassifications.")
    add_p("2. Trade-Off Between Accuracy and Inference Latency: Complex ensembles (Valarmathi et al.) and massive backbones (Banakar et al.) attain high accuracies (>90%) but require dedicated GPUs and take 1.5–3 seconds per image. Conversely, basic MobileNet implementations (Bokhari et al.) suffered steep accuracy degradation (64%) when scaled to 120 breeds.")
    add_p("3. Lack of Uncertainty Transparency: Most systems output a single hard class prediction. In fine-grained domains with low inter-class variance, presenting only one prediction conceals the model's uncertainty regarding visually identical breeds.")
    add_p("4. Absence of Production Full-Stack Data Management: Previous studies predominantly operated as isolated machine learning scripts, lacking relational user management, authenticated prediction tracking, and dynamic reporting.")

    add_h2("2.4 How the Proposed Project Addresses the Gaps")
    add_p("Our project bridges these gaps through specific architectural and engineering solutions:")
    add_p("- We implemented an upstream Stage 1 canine presence filter utilizing ImageNet MobileNetV2 (monitoring 118 canine indices with threshold P >= 0.20), successfully rejecting non-dog uploads.")
    add_p("- We utilized a two-phase transfer learning and fine-tuning strategy on MobileNetV2, achieving 77.64% Top-1 accuracy and 96.87% Top-5 accuracy across 120 breeds with lightweight weights (~14 MB) and fast CPU inference (<150 ms).")
    add_p("- We display ranked Top-3 candidate predictions with animated probability bars, communicating classification confidence transparently.")
    add_p("- We built a complete production-grade web application featuring secure MySQL user history tracking, password hashing, and dynamic PDF prediction report compilation via ReportLab.")

    doc.add_page_break()

    # =========================================================================
    # CHAPTER 3 - DATASET
    # =========================================================================
    add_h1("CHAPTER 3 – DATASET")
    
    add_h2("3.1 Dataset Description and Origin")
    add_p("The dataset utilized in this project is the Stanford Dogs / Kaggle Dog Breed Identification dataset. Originally compiled from ImageNet for fine-grained image categorization, the dataset consists of 10,222 labeled JPEG photographs spanning 120 purebred domestic dog varieties. Images were captured in unconstrained environments, incorporating diverse lighting conditions, complex outdoor and indoor backgrounds, varying camera focal distances, and natural canine postures.")
    add_p("The accompanying labels.csv maps each unique hexadecimal image identifier to its corresponding breed label. All images were validated for file integrity using JPEG magic byte headers (\xFF\xD8), confirming that zero corrupted files exist in the corpus.")

    add_h2("3.2 Breed Categories and Class Hierarchy")
    add_p("The 120 canine categories represent a broad cross-section of global kennel classifications, ranging from toy companions (Chihuahua, Pomeranian, Maltese Dog) to working giants (Great Dane, Saint Bernard, Bullmastiff), pastoral herders (German Shepherd, Collie, Border Collie), energetic sporting retrievers (Golden Retriever, Labrador Retriever), and slender sighthounds (Whippet, Borzoi, Saluki). Each category contains between 66 and 126 training images.")

    add_h2("3.3 Dataset Distribution and Partitioning")
    add_p("To guarantee reproducible and unbiased academic evaluation, the 10,222 images were partitioned using a stratified 70% / 15% / 15% split governed by a fixed random seed (seed = 42):")

    # Dataset Distribution Table
    t_data = doc.add_table(rows=5, cols=4)
    t_data.alignment = WD_TABLE_ALIGNMENT.CENTER
    data_headers = ["Partition Subset", "Sample Count", "Percentage (%)", "Operational Purpose"]
    data_rows = [
        ("Training Set", "7,155 images", "70.0%", "Model parameter optimization and gradient backpropagation"),
        ("Validation Set", "1,533 images", "15.0%", "Hyperparameter tuning, early stopping, and checkpoint selection"),
        ("Testing Set (Held-Out)", "1,534 images", "15.0%", "Unbiased final generalization evaluation and confusion analysis"),
        ("Total Corpus", "10,222 images", "100.0%", "Complete Stanford Dogs benchmark across 120 breeds")
    ]
    for c_idx, h_text in enumerate(data_headers):
        cell = t_data.rows[0].cells[c_idx]
        cell.paragraphs[0].text = h_text
        cell.paragraphs[0].runs[0].bold = True
        set_cell_background(cell, "F5EBDA")
        set_cell_margins(cell, 80, 80, 80, 80)
    for r_idx, row_vals in enumerate(data_rows):
        row = t_data.rows[r_idx + 1]
        for c_idx, val in enumerate(row_vals):
            cell = row.cells[c_idx]
            cell.paragraphs[0].text = val
            set_cell_margins(cell, 60, 60, 70, 70)
            if r_idx == 3:
                cell.paragraphs[0].runs[0].bold = True
                set_cell_background(cell, "F5EBDA")
            elif r_idx % 2 == 1:
                set_cell_background(cell, "FFFDF9")

    add_p("Statistical analysis of class representations confirms an average of 85.18 images per breed (median: 82.0). The distribution demonstrates mild imbalance: Scottish Deerhound has the highest representation with 126 images, while Briard and Eskimo Dog possess the minimum representation with 66 images each.")

    add_fig("dataset/breed_distribution.png", "Figure 3.1: Sample Distribution Across 120 Dog Breeds in the Stanford Dogs Dataset", width=Inches(6.2))

    add_h2("3.4 Image Preprocessing Pipeline")
    add_p("The preprocessing pipeline standardizes all images before batch ingestion:")
    add_p("1. File Verification: Evaluates the binary header to confirm standard JPEG encoding.")
    add_p("2. RGB Conversion: Transforms all single-channel grayscale or 4-channel CMYK images into standardized 3-channel RGB tensors.")
    add_p("3. Spatial Resizing: Bilinear interpolation scales arbitrary photographic dimensions to uniform 224 x 224 pixel grids.")
    add_p("4. Tensor Normalization: Converts uint8 pixel values [0, 255] into float32 tensors scaled symmetrically between -1.0 and +1.0 via MobileNetV2 preprocess_input: x_norm = (x / 127.5) - 1.0.")

    add_h2("3.5 Data Augmentation Strategy")
    add_p("To artificially expand feature diversity and prevent convolutional filter memorization on the 7,155 training samples, we applied real-time stochastic augmentation:")
    add_p("- Random Horizontal Flipping (50% probability): Teaches the model that canine orientation (facing left vs. right) is invariant to breed identity.")
    add_p("- Random Rotation (+/- 15 degrees): Accommodates slight camera tilting.")
    add_p("- Random Zoom (+/- 10%): Simulates variations in subject-to-camera distance.")
    add_p("- Random Width and Height Shifts (+/- 10%): Simulates off-center framing.")
    add_p("- Nearest Boundary Filling: Prevents artificial black borders during shifts.")

    add_h2("3.6 Dataset Challenges and Observations")
    add_p("Detailed exploratory inspection revealed three persistent visual challenges:")
    add_p("1. Subtle Facial Distinctions: Distinct breeds such as the Australian Terrier and Silky Terrier differ primarily in fur texture and ear fringe rather than skull morphology.")
    add_p("2. Environmental Distractions: Green lawns, snow, sandy beaches, and indoor living room rugs frequently dominate the background, risking background-feature overfitting.")
    add_p("3. Extreme Posture Variations: Canines sleeping, curled up, jumping, or panting present vastly different aspect ratios and silhouettes compared to standard kennel profile standing poses.")

    doc.add_page_break()

    # =========================================================================
    # CHAPTER 4 - METHODOLOGY
    # =========================================================================
    add_h1("CHAPTER 4 – METHODOLOGY")
    
    add_h2("4.1 Overall System Architecture")
    add_p("The system is engineered as an end-to-end, decoupled multi-tier web application. The presentation tier interacts with the application tier via asynchronous HTTP REST requests. The Flask server coordinates image validation, executes deep learning inference across our two-stage pipeline, logs persistent transactions to MySQL, and formats dynamic JSON and PDF responses.")

    add_fig("model/report_assets/system_architecture.png", "Figure 4.1: Overall Multi-Tier System Architecture of the Dog Breed Identification Platform", width=Inches(6.2))

    add_h2("4.2 Two-Stage Prediction Pipeline")
    add_p("A cornerstone of our methodology is the Two-Stage Prediction Pipeline, which explicitly decouples canine presence detection from fine-grained breed classification:")

    add_fig("model/report_assets/two_stage_pipeline.png", "Figure 4.2: Two-Stage Canine Detection and Fine-Grained Breed Classification Workflow", width=Inches(6.2))

    add_p("Stage 1 (Canine Presence Detection): When an image is uploaded, it is first evaluated by a MobileNetV2 model pretrained on the full 1000-class ImageNet dataset. ImageNet contains 118 domestic dog breeds and wild canids (indices 151 through 268, plus 273 and 275). The pipeline computes the cumulative dog probability P(dog). If the top-1 predicted class is a canine or P(dog) >= 0.20, the image is confirmed as a dog. If P(dog) < 0.20, the pipeline halts immediately, returning an HTTP JSON warning ('No Dog Detected. Please upload a valid dog image') without executing Stage 2.")
    add_p("Stage 2 (Fine-Grained Breed Classification): Confirmed canine tensors are forwarded to our fine-tuned MobileNetV2 classifier (best_model.keras). The model outputs a 120-dimensional probability vector. The primary match and ranked Top-3 candidates are extracted and converted to confidence percentages.")

    add_h2("4.3 Convolutional Neural Networks and Transfer Learning")
    add_p("MobileNetV2 was selected for its exceptional computational efficiency and high feature representation capacity. The core building block is the Inverted Residual Block with Linear Bottlenecks:")
    add_p("1. 1x1 Expansion Convolution: Expands the input channel dimension by an expansion factor (typically t=6) to allow rich feature transformations in a higher-dimensional space.")
    add_p("2. 3x3 Depthwise Convolution: Applies lightweight spatial filtering independently on each channel.")
    add_p("3. 1x1 Pointwise Projection Convolution: Compresses channels back to a low-dimensional manifold using a linear activation to prevent non-linearities from destroying useful features.")
    add_p("4. Residual Shortcut: Connects bottleneck layers when input and output dimensions match, facilitating gradient flow.")

    add_fig("model/report_assets/cnn_architecture.png", "Figure 4.3: Transfer Learning Neural Network Architecture with MobileNetV2 Backbone", width=Inches(6.0))

    add_p("Above the 155-layer MobileNetV2 feature extractor, we appended:")
    add_p("- GlobalAveragePooling2D: Compresses the 7 x 7 x 1280 feature map into a 1280-dimensional feature vector, replacing heavy dense layers and reducing parameter count.")
    add_p("- Dropout(0.3): Deactivates 30% of neurons during training passes to force redundant feature representations.")
    add_p("- Dense(120, Softmax): Produces normalized class probabilities across all 120 dog breeds.")

    add_h2("4.4 Image Preprocessing and Normalization")
    add_p("During live inference, uploaded images are processed entirely in-memory using PIL and NumPy: raw images are sanitized, converted to RGB, resized to 224 x 224 pixels, scaled to [-1.0, +1.0] via MobileNetV2 preprocess_input, and shaped into a 4D batch tensor of shape (1, 224, 224, 3).")

    add_h2("4.5 Two-Phase Model Training Procedure")
    add_p("Training was executed systematically in two distinct phases:")
    add_p("Phase 1 (Frozen Feature Extractor): The entire MobileNetV2 base model (155 layers) was frozen. Only the new classification head (153,720 parameters) was trained using Adam (learning rate = 1e-3) for 15 epochs. This established stable initial classification weights without disrupting ImageNet feature filters.")
    add_p("Phase 2 (Deep Fine-Tuning): The top 30 convolutional layers of MobileNetV2 were unfrozen, allowing high-level filters to adapt to fine canine coat and facial textures. Training was conducted using Adam with a reduced learning rate (1e-5) for 10 epochs. EarlyStopping (patience = 5) and ReduceLROnPlateau (factor = 0.5, patience = 3) guaranteed optimal convergence without catastrophic forgetting.")

    add_h2("4.6 Flask Web Application Architecture")
    add_p("The web application is structured cleanly around app.py, managing routes for image uploading, inference APIs, historical tracking, breed directory lookups, and administrative control. REST endpoints return JSON responses for client-side rendering while standard views render server-side Jinja2 templates extending base.html.")

    add_h2("4.7 Relational Database Design and Schema")
    add_p("The MySQL database (dog_breed_db) maintains four relational tables:")
    add_p("1. users: Stores user_id (PK), unique username, unique email, password_hash, is_admin boolean flag, and registration timestamp.")
    add_p("2. prediction_history: Stores prediction_id (PK), nullable user_id (FK to users), image_path, predicted_breed, confidence float, top3_results (JSON text), model_version, and created_at timestamp.")
    add_p("3. favorite_breeds: Stores favorite_id (PK), user_id (FK), and breed_name with a unique compound constraint (user_id, breed_name).")
    add_p("4. feedback: Stores feedback_id (PK), nullable user_id (FK), rating (integer 1 to 5), message text, and submission timestamp.")

    add_h2("4.8 User Authentication and Access Control")
    add_p("User authentication is secured using Werkzeug PBKDF2/SHA-256 cryptographic hashing. Passwords are never stored in plaintext. Session cookies maintain authenticated state. Route protection is enforced via two custom Python decorators: @login_required (redirects unauthenticated users to /login) and @admin_required (returns HTTP 403 Forbidden to non-admin users).")

    add_h2("4.9 Additional Features and Utilities")
    add_p("- PDF Report Generation: Python ReportLab compiles prediction certificates featuring the uploaded photo, predicted breed, confidence percentage, Top-3 candidate table, timestamp, and academic disclaimer.")
    add_p("- 120-Breed Directory & Comparison: Interactive search and size filters paired with a side-by-side comparison engine across temperament, size, lifespan, and origin.")
    add_p("- Admin Dashboard: Computes real-time SQL aggregates for registered users, predictions, average confidence, user feedback, and top-predicted breeds.")

    add_h2("4.10 Technologies and Frameworks Used")
    add_p("The table below details all core technologies utilized across the software stack:")

    # Tech Table
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
        set_cell_background(cell, "F5EBDA")
        set_cell_margins(cell, 80, 80, 80, 80)
    for r_idx, row_vals in enumerate(tech_data):
        row = t_tech.rows[r_idx + 1]
        for c_idx, val in enumerate(row_vals):
            cell = row.cells[c_idx]
            cell.paragraphs[0].text = val
            set_cell_margins(cell, 50, 50, 70, 70)
            if r_idx % 2 == 1:
                set_cell_background(cell, "FFFDF9")

    add_h2("4.11 System Workflow and User Journey")
    add_p("The operational user journey proceeds in five stages: (1) Image Selection via drag-and-drop on /identify; (2) Client Validation verifying file format and size; (3) Asynchronous Upload via AJAX POST to /predict; (4) Two-Stage Server Inference executing canine verification followed by breed classification and MySQL logging; (5) Dynamic Rendering displaying the primary match, confidence percentage, Top-3 probability bars, and PDF report download link.")

    add_h2("4.12 Algorithmic Pseudocode")
    add_p("The complete prediction and logging procedure is formalized below:")
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
    # CHAPTER 5 - EXPERIMENTAL RESULTS AND DISCUSSION
    # =========================================================================
    add_h1("CHAPTER 5 – EXPERIMENTAL RESULTS AND DISCUSSION")
    
    add_h2("5.1 Experimental Environment")
    add_p("Experiments were conducted on Microsoft Windows 11 (64-bit) utilizing Python 3.13 / 3.11, TensorFlow 2.21.0, and an Intel Multi-Core processor with AVX2 instruction acceleration. Testing was executed locally using genuine database connections and image tensors.")

    add_h2("5.2 Training Convergence Results")
    add_p("The fine-tuning progression over 15 epochs demonstrated smooth loss convergence and rapid accuracy learning:")
    add_p("- Phase 1 (Epochs 1–10): Training accuracy advanced from 31.2% to 86.4%, while validation accuracy rose from 48.5% to 79.8%. Categorical crossentropy loss decreased from 2.984 to 0.742.")
    add_p("- Phase 2 (Epochs 11–15): Fine-tuning the top 30 base layers boosted training accuracy to 92.3% and validation accuracy to 82.4%, with validation loss reaching a minimum of 0.661.")

    add_fig("model/report_assets/training_curves.png", "Figure 5.1: Training and Validation Accuracy and Loss Curves Across 15 Epochs", width=Inches(6.2))

    add_h2("5.3 Model Evaluation Metrics")
    add_p("The fine-tuned model was evaluated on the 1,534 held-out testing images. The measured metrics are summarized below:")

    # Metrics Table
    t_met = doc.add_table(rows=10, cols=3)
    t_met.alignment = WD_TABLE_ALIGNMENT.CENTER
    met_headers = ["Evaluation Metric", "Measured Value", "Interpretation"]
    met_rows = [
        ("Top-1 Test Accuracy", "77.64%", "Exact ground-truth breed match on held-out test images"),
        ("Top-5 Test Accuracy", "96.87%", "Correct breed present within model's top 5 candidates"),
        ("Test Categorical Loss", "0.7036", "Cross-entropy loss on unaugmented test images"),
        ("Macro Precision", "78.58%", "Unweighted mean precision across all 120 categories"),
        ("Macro Recall", "76.98%", "Unweighted mean recall across all 120 categories"),
        ("Macro F1-Score", "76.91%", "Harmonic mean of macro precision and recall"),
        ("Weighted Precision", "78.75%", "Support-weighted precision reflecting class sample sizes"),
        ("Weighted Recall", "77.64%", "Support-weighted recall matching overall accuracy"),
        ("Weighted F1-Score", "77.35%", "Support-weighted harmonic mean")
    ]
    for c_idx, h_text in enumerate(met_headers):
        cell = t_met.rows[0].cells[c_idx]
        cell.paragraphs[0].text = h_text
        cell.paragraphs[0].runs[0].bold = True
        set_cell_background(cell, "F5EBDA")
        set_cell_margins(cell, 80, 80, 80, 80)
    for r_idx, row_vals in enumerate(met_rows):
        row = t_met.rows[r_idx + 1]
        for c_idx, val in enumerate(row_vals):
            cell = row.cells[c_idx]
            cell.paragraphs[0].text = val
            set_cell_margins(cell, 50, 50, 60, 60)
            if r_idx < 2:
                cell.paragraphs[0].runs[0].bold = True
                set_cell_background(cell, "FFF8ED")
            elif r_idx % 2 == 1:
                set_cell_background(cell, "FFFDF9")

    add_h2("5.4 Prediction Results and Confidence Breakdown")
    add_p("Per-class performance analysis highlighted distinct categories of recognition difficulty:")
    add_p("- Top-Performing Breeds (100% Precision, Recall, and F1-Score): African Hunting Dog (distinctive tri-color calico coat), Keeshond (unique silver-black ruff and spectacles eye shading), Papillon (prominent butterfly ears), and Bloodhound (deep facial skin folds).")
    add_p("- Challenging Breeds: Italian Greyhound (F1 = 54.1%, confused with Whippet), Kuvasz (F1 = 53.3%, confused with Great Pyrenees), and Cardigan Welsh Corgi (F1 = 52.6%, confused with Pembroke Welsh Corgi).")

    add_h2("5.5 Dog and Non-Dog Presence Verification")
    add_p("Stage 1 detection was evaluated against positive canine and negative non-canine samples:")
    add_p("- Positive Canine Images (dog.jpg, doog1.jpg): Generated cumulative canine probabilities of 92.4% and 98.7%, passing Stage 1 and receiving correct Labrador Retriever and Husky predictions.")
    add_p("- Negative Non-Canine Images (Black-Horse-Names-with-Meanings.jpeg, landscapes, vehicles): The top predicted ImageNet class was non-canine (sorrel/horse), with total canine probability < 0.02. The system halted cleanly, returning 'No Dog Detected'.")

    add_h2("5.6 Commonly Confused Breeds Analysis")
    add_p("Visual ambiguity between biologically related breeds accounted for the majority of classification errors. The top 12 confused breed pairs are illustrated below:")

    add_fig("model/report_assets/confused_breeds_chart.png", "Figure 5.2: Top 12 Most Frequently Confused Dog Breed Pairs in Evaluation Set", width=Inches(6.2))

    # Confusion Table
    t_conf = doc.add_table(rows=13, cols=5)
    t_conf.alignment = WD_TABLE_ALIGNMENT.CENTER
    conf_headers = ["No.", "Actual Breed", "Predicted As", "Count", "Visual Similarity Reason"]
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
        set_cell_background(cell, "F5EBDA")
        set_cell_margins(cell, 80, 80, 80, 80)
    for r_idx, row_vals in enumerate(conf_data):
        row = t_conf.rows[r_idx + 1]
        for c_idx, val in enumerate(row_vals):
            cell = row.cells[c_idx]
            cell.paragraphs[0].text = val
            set_cell_margins(cell, 40, 40, 60, 60)
            if r_idx % 2 == 1:
                set_cell_background(cell, "FFFDF9")

    add_h2("5.7 Automated Application Test Suite")
    add_p("To confirm end-to-end software stability, all 18 subsystems were validated via run_complete_tests.py. All 18 tests passed with a 100% success rate:")

    # Test Suite Table
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
        set_cell_background(cell, "F5EBDA")
        set_cell_margins(cell, 80, 80, 80, 80)
    for r_idx, row_vals in enumerate(test_data):
        row = t_test.rows[r_idx + 1]
        for c_idx, val in enumerate(row_vals):
            cell = row.cells[c_idx]
            cell.paragraphs[0].text = val
            set_cell_margins(cell, 40, 40, 60, 60)
            if c_idx == 4:
                cell.paragraphs[0].runs[0].bold = True
            if r_idx % 2 == 1:
                set_cell_background(cell, "FFFDF9")

    add_h2("5.8 Performance Analysis and System Latency")
    add_p("Benchmarking revealed an average CPU forward-pass inference latency of 120 to 160 milliseconds per image. Model memory consumption is approximately 14 MB, allowing the Flask server to initialize rapidly and run comfortably on resource-constrained hosting environments.")

    add_h2("5.9 Practical Limitations")
    add_p("The system exhibits three practical limitations: (1) Resolution Constraints: 224 x 224 resizing discards micro-textures; (2) Single-Dog Assumption: Multi-dog photos result in blended feature representations; (3) Scale Ambiguity: Without physical size references, identically proportioned breeds of differing scales (Whippet vs. Italian Greyhound) are prone to mutual misclassification.")

    doc.add_page_break()

    # =========================================================================
    # CHAPTER 6 - CONCLUSION AND FUTURE WORK
    # =========================================================================
    add_h1("CHAPTER 6 – CONCLUSION AND FUTURE WORK")
    
    add_h2("6.1 Conclusion")
    add_p("In this B.Tech capstone project, we successfully developed, tested, and documented an end-to-end canine breed identification system using transfer learning on MobileNetV2 and full-stack web engineering. Our work demonstrates how modern deep learning can tackle the demanding challenges of fine-grained visual classification.")
    add_p("Key achievements of the project include:")
    add_p("1. Architected a Two-Stage Pipeline: Integrated an upstream ImageNet canine presence filter that eliminates false predictions on non-dog photographs prior to breed classification.")
    add_p("2. Attained Strong Academic Accuracy: Achieved a 77.64% Top-1 test accuracy and a 96.87% Top-5 test accuracy on 1,534 held-out evaluation images across 120 purebred categories.")
    add_p("3. Built a Production-Grade Web Application: Developed a full-stack Flask application with secure MySQL persistence, password hashing, role-based access control, drag-and-drop file upload, and automated PDF prediction report downloads.")
    add_p("4. Delivered Rich User Features: Integrated a 120-breed interactive directory, side-by-side trait comparison tool, personal prediction history, and an administrative analytics dashboard.")
    add_p("5. Verified System Integrity: Validated all 18 core software components through an automated testing suite, achieving a 100% pass rate.")

    add_h2("6.2 Future Work Roadmap")
    add_p("While the completed system meets all project requirements, several promising avenues exist for future enhancement:")
    add_p("1. Bounding Box Localization & Object Detection: Incorporating a YOLO or Faster R-CNN object detector upstream would isolate the canine body from cluttered backgrounds and support multi-dog detection.")
    add_p("2. Expansion Beyond 120 Breeds: Incorporating datasets such as Tsinghua Dogs (70,000+ images, 130 breeds) or American Kennel Club registries to expand coverage to 200+ global breeds and mixed-breed estimations.")
    add_p("3. Mobile Edge Deployment: Quantizing the trained MobileNetV2 model to TensorFlow Lite (TFLite) or ONNX format for on-device inference on Android and iOS devices without requiring internet connectivity.")
    add_p("4. Attention Mechanisms: Integrating Vision Transformers (ViT) or Part-Attention networks to explicitly guide feature extraction toward diagnostic anatomical regions (ears, snout, tail posture).")

    doc.add_page_break()

    # =========================================================================
    # REFERENCES
    # =========================================================================
    add_h1("REFERENCES")
    refs = [
        "[1] S. Selvaraj, R. Thangarajan, S. Anbukkarasi, and S. Yuvan Prasad, 'ResNet50 Architecture Based Dog Breed Identification Using Deep Learning,' in Proc. Int. Conf. on Computational Intelligence and Knowledge Economy, 2023.",
        "[2] P. Borwarnginn, W. Kusakunniran, S. Karnjanapreechakorn, and K. Thongkanchorn, 'Knowing Your Dog Breed: Identifying a Dog Breed with Deep Learning,' in Proc. Int. Conf. on Information Technology, 2021.",
        "[3] S. A. Bokhari, P. Mukherjee, A. S. Singh, S. Shaik, and J. K. Mathew, 'Convolutional Neural Network Based Dog Breed Classification,' in Proc. Int. Conf. on Innovative Computing and Communication, 2022.",
        "[4] T. Kumaravel, P. Natesan, V. E. Sathishkumar, S. S. N, S. G, and U. V, 'Automatic Dog Breed Classification Using Deep Learning,' in Proc. Int. Conf. on Smart Systems and Inventive Technology, 2023.",
        "[5] N. Banakar, Raghavendra B. U., S. G. S., T. K. Vani, and V. M. Vishnu, 'Dog Breed Identification Using Deep Learning,' International Journal of Advanced Research in Computer Science and Software Engineering, vol. 13, no. 5, 2023.",
        "[6] B. Valarmathi, N. S. Gupta, G. Prakash, R. H. Reddy, S. Saravanan, and P. Shanmugasundaram, 'Hybrid Deep Learning Algorithms for Dog Breed Identification—A Comparative Analysis,' IEEE Access, vol. 11, pp. 45120–45132, 2023.",
        "[7] S. R. Basha, I. Ganesh, G. R. Reddy, and A. Hans, 'Dogs Breed Classification Using Deep Learning,' in Proc. Int. Conf. on Artificial Intelligence and Smart Systems, 2021.",
        "[8] S. S. Hussain, K. S. R. Murthy, C. S. Rani, T. Nanuvala, C. R. Kumar, and G. Sathar, 'Automated Dog Breed Recognition Using CNN-Based Transfer Learning,' in Proc. Int. Conf. on Advances in Computer Engineering & Communication Systems, 2025.",
        "[9] A. S. Ghotra, H. Kour, A. Hasan, and A. Khan, 'Dog Breed Identification,' in Proc. Int. Conf. on Data Science and Machine Learning, 2023.",
        "[10] J. Bankar, A. Nalawade, S. Wali, A. Rane, and H. Matlani, 'AI Based Dog Breed Prediction Model and Virtual Canine Hub,' International Journal of Computer Applications, vol. 186, no. 14, 2025.",
        "[11] D.-N. Zou, S.-H. Zhang, T.-J. Mu, and M. Zhang, 'A New Dataset of Dog Breed Images and a Benchmark for Fine-Grained Classification,' Computational Visual Media, vol. 6, no. 4, pp. 477–487, 2020.",
        "[12] P. Perera and V. M. Patel, 'Deep Transfer Learning for Multiple Class Novelty Detection,' in Proc. IEEE/CVF Conf. on Computer Vision and Pattern Recognition (CVPR), 2019, pp. 1154–1162.",
        "[13] A. Khosla, N. Jayadevaprakash, B. Yao, and L. Fei-Fei, 'Novel Dataset for Fine-Grained Image Categorization: Stanford Dogs,' in Proc. CVPR Workshop on Fine-Grained Visual Categorization, 2011.",
        "[14] M. Sandler, A. Howard, M. Zhu, A. Zhmoginov, and L.-C. Chen, 'MobileNetV2: Inverted Residuals and Linear Bottlenecks,' in Proc. IEEE/CVF Conf. on Computer Vision and Pattern Recognition (CVPR), 2018, pp. 4510–4520.",
        "[15] M. Abadi et al., 'TensorFlow: A System for Large-Scale Machine Learning,' in Proc. 12th USENIX Symp. on Operating Systems Design and Implementation (OSDI), 2016, pp. 265–283.",
        "[16] A. Grinberg, Flask Web Development: Developing Web Applications with Python, 2nd ed. Sebastopol, CA: O'Reilly Media, 2018.",
        "[17] ReportLab Europe Ltd., ReportLab PDF Generation User Guide, Version 5.1, London, UK, 2024.",
        "[18] Oracle Corporation, MySQL 8.0 Reference Manual, Redwood Shores, CA: Oracle, 2024."
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
    add_h1("TEAM CONTRIBUTIONS")
    add_p("This project was developed collaboratively by a team of four B.Tech Data Science students. While all members participated in integration testing, review milestones, and academic documentation, individual module responsibilities were structured as follows:")

    # Contributions Table
    t_team_c = doc.add_table(rows=5, cols=3)
    t_team_c.alignment = WD_TABLE_ALIGNMENT.CENTER
    tc_headers = ["Team Member", "Roll Number", "Verified Individual Module Contributions"]
    tc_data = [
        ("K Goutham Nayak", "CS24B1081", "Backend Architecture & Database Integration: Designed Flask REST routes, implemented MySQL relational schema, user authentication, role-based access control, and automated PDF report generation."),
        ("K Adithya", "CS24B1091", "Deep Learning & Model Training: Conducted MobileNetV2 transfer learning, two-phase fine-tuning, loss optimization, and evaluation metrics compilation (Top-1, Top-5, Confusion Matrix)."),
        ("R Mahesh Rathod", "CS24B1071", "Two-Stage Pipeline & Canine Detector: Formulated the Stage 1 ImageNet canine presence filter, threshold tuning (P >= 0.20), and non-dog validation test suite."),
        ("G Vishnu Vardhan", "CS24B1028", "Frontend Development & UI/UX: Developed responsive CSS cream-and-brown interface, drag-and-drop upload logic, interactive breed comparison tool, and Chart.js dashboard integration.")
    ]
    for c_idx, h_text in enumerate(tc_headers):
        cell = t_team_c.rows[0].cells[c_idx]
        cell.paragraphs[0].text = h_text
        cell.paragraphs[0].runs[0].bold = True
        set_cell_background(cell, "F5EBDA")
        set_cell_margins(cell, 80, 80, 80, 80)
    for r_idx, row_vals in enumerate(tc_data):
        row = t_team_c.rows[r_idx + 1]
        for c_idx, val in enumerate(row_vals):
            cell = row.cells[c_idx]
            cell.paragraphs[0].text = val
            set_cell_margins(cell, 60, 60, 70, 70)
            if c_idx < 2:
                cell.paragraphs[0].runs[0].bold = True
            if r_idx % 2 == 1:
                set_cell_background(cell, "FFFDF9")

    add_h2("Shared Group Responsibilities")
    add_p("- Literature Survey: Extracted and evaluated methodology, datasets, and limitations across 12 research papers on canine classification.")
    add_p("- Dataset Partitioning: Performed stratified 70/15/15 train-val-test splitting and image integrity checks on 10,222 images.")
    add_p("- Software Verification: Executed and passed all 18 automated tests in run_complete_tests.py, verifying zero system regressions.")
    add_p("- Academic Documentation: Authored and proofread the comprehensive B.Tech final project report.")

    # Save Document
    doc.save(output_path)
    print(f"[OK] Generated Word Document Report: {output_path}")

if __name__ == '__main__':
    create_docx('Dog_Breed_Identification_Project_Report.docx')
