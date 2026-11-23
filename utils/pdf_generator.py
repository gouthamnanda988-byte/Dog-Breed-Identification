"""
PDF Report Generator for Dog Breed Identification
Generates a professional single-page PDF prediction report using ReportLab.
"""

import os
import io
from datetime import datetime
from PIL import Image as PILImage

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    Image as RLImage,
    HRFlowable,
    KeepTogether
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY

import config


# Brand color palette (Warm Cream & Brown theme)
BROWN_DARK = colors.HexColor('#5C3A1E')
BROWN_PRIMARY = colors.HexColor('#8B5E3C')
BROWN_LIGHT = colors.HexColor('#A97B5A')
AMBER_ACCENT = colors.HexColor('#D4A574')
CREAM_BG = colors.HexColor('#FFF8ED')
CREAM_CARD = colors.HexColor('#FFF3E2')
TEXT_DARK = colors.HexColor('#3E2515')
TEXT_MUTED = colors.HexColor('#7A5C43')
BORDER_COLOR = colors.HexColor('#E0CDB8')
WHITE = colors.HexColor('#FFFFFF')
GREEN_ACCENT = colors.HexColor('#2E7D32')


def _get_scaled_image(image_path, max_width=210, max_height=190):
    """
    Scale uploaded image preserving aspect ratio for ReportLab.
    Falls back gracefully if image file cannot be read.
    """
    if not image_path:
        return None

    # Check if absolute path or filename in upload folder
    full_path = image_path
    if not os.path.isabs(full_path):
        full_path = os.path.join(config.UPLOAD_FOLDER, image_path)

    if not os.path.exists(full_path):
        return None

    try:
        with PILImage.open(full_path) as pil_im:
            orig_w, orig_h = pil_im.size
            if orig_w == 0 or orig_h == 0:
                return None
            aspect = orig_h / float(orig_w)

        # Scale within max bounding box
        target_w = max_width
        target_h = target_w * aspect
        if target_h > max_height:
            target_h = max_height
            target_w = target_h / aspect

        return RLImage(full_path, width=target_w, height=target_h)
    except Exception as e:
        print(f"[!] Warning: Could not process image for PDF report: {e}")
        return None


def generate_prediction_pdf(prediction_data):
    """
    Generate an in-memory PDF prediction report as a BytesIO buffer.
    
    Expected prediction_data keys:
      - predicted_breed (str)
      - confidence (float or int)
      - top3 (list of dicts: [{'breed': ..., 'confidence': ...}, ...])
      - image_path (str)
      - prediction_date / created_at (str or datetime)
      - model_version (str, optional, defaults to 'MobileNetV2-v1')
    """
    buffer = io.BytesIO()

    # Document setup: Letter size with 0.5 inch (36pt) margins
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=36,
        leftMargin=36,
        topMargin=32,
        bottomMargin=32
    )

    # Styles
    base_styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        'DocTitle',
        parent=base_styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        textColor=BROWN_DARK,
        alignment=TA_LEFT
    )

    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=base_styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=13,
        textColor=TEXT_MUTED,
        alignment=TA_LEFT
    )

    section_header_style = ParagraphStyle(
        'SectionHeader',
        parent=base_styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=BROWN_DARK,
        spaceBefore=8,
        spaceAfter=4
    )

    label_style = ParagraphStyle(
        'FieldLabel',
        parent=base_styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=12,
        textColor=TEXT_MUTED
    )

    value_style = ParagraphStyle(
        'FieldValue',
        parent=base_styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=13,
        textColor=TEXT_DARK
    )

    breed_highlight_style = ParagraphStyle(
        'BreedHighlight',
        parent=base_styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=16,
        leading=20,
        textColor=BROWN_DARK
    )

    confidence_badge_style = ParagraphStyle(
        'ConfBadge',
        parent=base_styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=15,
        textColor=GREEN_ACCENT
    )

    disclaimer_style = ParagraphStyle(
        'DisclaimerText',
        parent=base_styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=7.8,
        leading=11,
        textColor=TEXT_MUTED,
        alignment=TA_JUSTIFY
    )

    table_header_style = ParagraphStyle(
        'TableHeader',
        parent=base_styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=11,
        textColor=WHITE,
        alignment=TA_CENTER
    )

    table_cell_style = ParagraphStyle(
        'TableCell',
        parent=base_styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=12,
        textColor=TEXT_DARK
    )

    table_cell_bold = ParagraphStyle(
        'TableCellBold',
        parent=base_styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=12,
        textColor=BROWN_DARK
    )

    table_cell_center = ParagraphStyle(
        'TableCellCenter',
        parent=base_styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=12,
        textColor=BROWN_PRIMARY,
        alignment=TA_CENTER
    )

    story = []

    # 1. Header Banner
    header_table_data = [
        [
            Paragraph("🐾 <b>Dog Breed Identification</b>", title_style),
            Paragraph("<b>PROJECT REPORT</b><br/><font color='#7A5C43'>B.Tech Data Science</font>", ParagraphStyle('RightMeta', parent=subtitle_style, alignment=TA_RIGHT))
        ],
        [
            Paragraph("Official Deep Learning Prediction & Classification Summary", subtitle_style),
            Paragraph(f"Generated: {datetime.now().strftime('%B %d, %Y')}", ParagraphStyle('RightDate', parent=subtitle_style, alignment=TA_RIGHT, fontSize=8.5))
        ]
    ]
    header_table = Table(header_table_data, colWidths=[360, 180])
    header_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
        ('TOPPADDING', (0, 0), (-1, -1), 0),
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('RIGHTPADDING', (0, 0), (-1, -1), 0),
    ]))
    story.append(header_table)
    story.append(Spacer(1, 6))
    story.append(HRFlowable(width="100%", thickness=2, color=BROWN_PRIMARY, spaceBefore=2, spaceAfter=10))

    # Parse prediction fields
    predicted_breed = prediction_data.get('predicted_breed', 'Unknown Breed')
    confidence_val = prediction_data.get('confidence', 0.0)
    try:
        conf_float = float(confidence_val)
    except (ValueError, TypeError):
        conf_float = 0.0

    model_version = prediction_data.get('model_version', 'MobileNetV2-v1')
    image_filename = prediction_data.get('image_path') or prediction_data.get('filename') or ''

    # Format date & time
    raw_date = prediction_data.get('created_at') or prediction_data.get('prediction_date')
    if isinstance(raw_date, datetime):
        date_str = raw_date.strftime('%B %d, %Y at %I:%M %p')
    elif isinstance(raw_date, str) and raw_date.strip():
        date_str = raw_date
    else:
        date_str = datetime.now().strftime('%B %d, %Y at %I:%M %p')

    # Top 3 candidates
    top3_list = prediction_data.get('top3', [])
    if not top3_list:
        # Fallback if only single prediction available
        top3_list = [{'breed': predicted_breed, 'confidence': conf_float}]

    # 2. Main Prediction Results Card (Image + Details)
    rl_img = _get_scaled_image(image_filename, max_width=200, max_height=170)
    if rl_img is None:
        img_cell = Paragraph("<font color='#8C7260'><i>[Uploaded Dog Image]</i></font>", ParagraphStyle('NoImg', alignment=TA_CENTER))
    else:
        img_cell = rl_img

    details_table_data = [
        [Paragraph("PRIMARY PREDICTED BREED", label_style)],
        [Paragraph(f"<b>{predicted_breed}</b>", breed_highlight_style)],
        [Spacer(1, 4)],
        [Paragraph("CONFIDENCE SCORE", label_style)],
        [Paragraph(f"<b>{conf_float:.2f}% Match</b>", confidence_badge_style)],
        [Spacer(1, 4)],
        [Paragraph("MODEL VERSION", label_style)],
        [Paragraph(f"{model_version} (120 Stanford Dogs Classes)", value_style)],
        [Spacer(1, 4)],
        [Paragraph("PREDICTION TIMESTAMP", label_style)],
        [Paragraph(f"{date_str}", value_style)],
        [Spacer(1, 4)],
        [Paragraph("INPUT IMAGE FILE", label_style)],
        [Paragraph(f"{os.path.basename(image_filename) if image_filename else 'dog_upload.jpg'}", value_style)],
    ]
    details_subtable = Table(details_table_data, colWidths=[290])
    details_subtable.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 0),
        ('TOPPADDING', (0, 0), (-1, -1), 1),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 1),
    ]))

    card_table_data = [[img_cell, details_subtable]]
    card_table = Table(card_table_data, colWidths=[220, 320])
    card_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), CREAM_CARD),
        ('BOX', (0, 0), (-1, -1), 1, BORDER_COLOR),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('ALIGN', (0, 0), (0, 0), 'CENTER'),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
    ]))
    story.append(card_table)
    story.append(Spacer(1, 14))

    # 3. Top 3 Breed Predictions Table
    story.append(Paragraph("🏆 Top 3 Candidate Breed Predictions", section_header_style))
    story.append(Spacer(1, 4))

    top3_rows = [
        [
            Paragraph("Rank", table_header_style),
            Paragraph("Candidate Breed Name", ParagraphStyle('THL', parent=table_header_style, alignment=TA_LEFT)),
            Paragraph("Confidence (%)", table_header_style),
            Paragraph("Classification Status", table_header_style)
        ]
    ]

    for i, item in enumerate(top3_list[:3]):
        rank_num = i + 1
        b_name = item.get('breed', 'Unknown')
        c_val = float(item.get('confidence', 0.0))
        status_text = "Primary Prediction" if rank_num == 1 else "Alternative Candidate"
        status_color = "#2E7D32" if rank_num == 1 else "#5A3E2B"

        top3_rows.append([
            Paragraph(f"<b>#{rank_num}</b>", table_cell_center),
            Paragraph(f"{b_name}", table_cell_bold if rank_num == 1 else table_cell_style),
            Paragraph(f"<b>{c_val:.2f}%</b>", table_cell_center),
            Paragraph(f"<font color='{status_color}'><b>{status_text}</b></font>", table_cell_center)
        ])

    top3_table = Table(top3_rows, colWidths=[50, 240, 110, 140])
    top3_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), BROWN_PRIMARY),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 0.5, BORDER_COLOR),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [WHITE, CREAM_BG]),
    ]))
    story.append(top3_table)
    story.append(Spacer(1, 14))

    # 4. Model Architecture & Pipeline Technical Specifications
    story.append(Paragraph("⚙️ Technical Architecture Specifications", section_header_style))
    story.append(Spacer(1, 4))

    specs_data = [
        [
            Paragraph("<b>Base Architecture:</b>", label_style),
            Paragraph("MobileNetV2 (Transfer Learning via ImageNet weights)", value_style),
            Paragraph("<b>Input Resolution:</b>", label_style),
            Paragraph("224 × 224 RGB (3 Channels)", value_style)
        ],
        [
            Paragraph("<b>Output Layer:</b>", label_style),
            Paragraph("120-Way Softmax Activation", value_style),
            Paragraph("<b>Pretrained Weights:</b>", label_style),
            Paragraph("Kaggle Dog Breed / Stanford Dogs", value_style)
        ],
        [
            Paragraph("<b>Validation Stage:</b>", label_style),
            Paragraph("ImageNet Dog / Non-Dog Canine Verification", value_style),
            Paragraph("<b>Framework:</b>", label_style),
            Paragraph("TensorFlow / Keras 2.x & Flask Backend", value_style)
        ]
    ]
    specs_table = Table(specs_data, colWidths=[120, 160, 110, 150])
    specs_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), CREAM_BG),
        ('BOX', (0, 0), (-1, -1), 0.5, BORDER_COLOR),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(specs_table)
    story.append(Spacer(1, 14))

    # 5. Academic & Technical Disclaimer (Required)
    disclaimer_box_data = [
        [
            Paragraph(
                "<b>📌 Technical & Academic Disclaimer:</b><br/>"
                "This prediction report was automatically generated by the Dog Breed Identification deep learning application as part of a B.Tech Data Science project. "
                "The predicted breed and associated confidence metrics represent probabilistic estimates computed by a convolutional neural network (MobileNetV2) trained on 120 canine classes. "
                "Predictions are intended strictly for educational, research, and technical demonstration purposes, and should not be used as an official pedigree, veterinary diagnostic, or certified kennel club documentation.",
                disclaimer_style
            )
        ]
    ]
    disclaimer_table = Table(disclaimer_box_data, colWidths=[540])
    disclaimer_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#FDF7E7')),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#E5D3A1')),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
    ]))
    story.append(disclaimer_table)
    story.append(Spacer(1, 8))

    # 6. Footer Note
    footer_text = Paragraph(
        "<font color='#8C7260'>🐾 Dog Breed Identification • B.Tech Data Science Project • Generated via ReportLab</font>",
        ParagraphStyle('Footer', parent=base_styles['Normal'], fontName='Helvetica', fontSize=7.5, alignment=TA_CENTER)
    )
    story.append(footer_text)

    # Build PDF
    doc.build(story)
    buffer.seek(0)
    return buffer
