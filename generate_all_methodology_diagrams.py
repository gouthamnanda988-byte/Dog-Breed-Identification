"""
generate_all_methodology_diagrams.py
====================================
Generates spacious, clean, professional diagrams for Chapter 4 (Methodology):
1. fig4_1_system_architecture.png (Clean multi-tier architecture)
2. fig4_2_preprocessing_flowchart.png (Image upload & preprocessing pipeline)
3. fig4_3_stage1_detector.png (Stage 1 dog presence verification)
4. fig4_4_stage2_classifier.png (Stage 2 fine-grained breed classification)
5. fig4_5_complete_workflow.png (Complete prediction workflow flowchart)
"""

import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches

os.makedirs('model/report_assets', exist_ok=True)

# Common styling
FONT_FAMILY = 'sans-serif'
C_BOX_BG = '#F0F4F8'
C_BOX_EDGE = '#2B4C7E'
C_TEXT = '#1A202C'
C_ACCENT = '#2B4C7E'
C_DECISION_BG = '#FFF8E7'
C_DECISION_EDGE = '#D97706'
C_REJECT_BG = '#FEE2E2'
C_REJECT_EDGE = '#DC2626'
C_PASS_BG = '#DCFCE7'
C_PASS_EDGE = '#16A34A'

# -----------------------------------------------------------------------------
# 1. FIG 4.1: OVERALL SYSTEM ARCHITECTURE
# -----------------------------------------------------------------------------
def make_fig4_1():
    fig, ax = plt.subplots(figsize=(12, 7.5), dpi=300)
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 8)
    ax.axis('off')

    # Draw 4 Tier Frames
    tiers = [
        ("Presentation Tier (Client)", 0.5, 0.5, 2.5, 6.8, '#F8FAFC', '#94A3B8'),
        ("Application Tier (Flask)", 3.4, 0.5, 2.6, 6.8, '#F1F5F9', '#64748B'),
        ("Deep Learning Tier (TensorFlow)", 6.4, 0.5, 2.6, 6.8, '#F8FAFC', '#94A3B8'),
        ("Data Tier (MySQL)", 9.4, 0.5, 2.2, 6.8, '#F1F5F9', '#64748B')
    ]
    for name, x, y, w, h, bg, border in tiers:
        rect = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.1", fc=bg, ec=border, lw=1.2, ls='--')
        ax.add_patch(rect)
        ax.text(x + w/2, y + h - 0.35, name, ha='center', va='center', fontsize=9.5, fontweight='bold', color='#334155', fontfamily=FONT_FAMILY)

    # Blocks inside Presentation Tier
    b_user = patches.FancyBboxPatch((0.7, 5.2), 2.1, 1.2, boxstyle="round,pad=0.08", fc='#E2E8F0', ec='#475569', lw=1.2)
    ax.add_patch(b_user)
    ax.text(1.75, 5.8, "User\n(Web Browser)", ha='center', va='center', fontsize=9.5, fontweight='bold', color=C_TEXT, fontfamily=FONT_FAMILY)

    b_ui = patches.FancyBboxPatch((0.7, 2.2), 2.1, 1.8, boxstyle="round,pad=0.08", fc='#FFFFFF', ec='#2B4C7E', lw=1.2)
    ax.add_patch(b_ui)
    ax.text(1.75, 3.1, "Web Interface\n• Drag-and-Drop\n• Breed Directory\n• Trait Comparison\n• Admin Dashboard", ha='center', va='center', fontsize=8.5, color=C_TEXT, fontfamily=FONT_FAMILY)

    # Blocks inside Application Tier (Flask)
    b_flask = patches.FancyBboxPatch((3.6, 4.4), 2.2, 2.0, boxstyle="round,pad=0.08", fc='#FFFFFF', ec='#2B4C7E', lw=1.2)
    ax.add_patch(b_flask)
    ax.text(4.7, 5.4, "Flask Backend\n(app.py)\n• Route Handling\n• Session & Auth\n• PDF Generator", ha='center', va='center', fontsize=9, fontweight='bold', color=C_TEXT, fontfamily=FONT_FAMILY)

    b_prep = patches.FancyBboxPatch((3.6, 1.5), 2.2, 1.8, boxstyle="round,pad=0.08", fc='#FFFFFF', ec='#2B4C7E', lw=1.2)
    ax.add_patch(b_prep)
    ax.text(4.7, 2.4, "Image Preparation\n• Validation\n• RGB Conversion\n• 224×224 Scaling\n• Normalization", ha='center', va='center', fontsize=8.5, color=C_TEXT, fontfamily=FONT_FAMILY)

    # Blocks inside Deep Learning Tier
    b_stage1 = patches.FancyBboxPatch((6.6, 4.2), 2.2, 2.2, boxstyle="round,pad=0.08", fc='#EFF6FF', ec='#1D4ED8', lw=1.2)
    ax.add_patch(b_stage1)
    ax.text(7.7, 5.3, "Stage 1: Dog Filter\n(ImageNet MobileNetV2)\n• 118 Dog Classes\n• Canine Threshold\n  P(dog) ≥ 0.20", ha='center', va='center', fontsize=8.5, fontweight='bold', color='#1E3A8A', fontfamily=FONT_FAMILY)

    b_stage2 = patches.FancyBboxPatch((6.6, 1.2), 2.2, 2.2, boxstyle="round,pad=0.08", fc='#EFF6FF', ec='#1D4ED8', lw=1.2)
    ax.add_patch(b_stage2)
    ax.text(7.7, 2.3, "Stage 2: Classifier\n(Fine-Tuned Model)\n• MobileNetV2 Base\n• Pooling & Dropout\n• 120-Breed Softmax", ha='center', va='center', fontsize=8.5, fontweight='bold', color='#1E3A8A', fontfamily=FONT_FAMILY)

    # Blocks inside Database Tier
    b_mysql = patches.FancyBboxPatch((9.6, 2.0), 1.8, 4.4, boxstyle="round,pad=0.08", fc='#FFFFFF', ec='#0D9488', lw=1.2)
    ax.add_patch(b_mysql)
    ax.text(10.5, 4.2, "MySQL Database\n(dog_breed_db)\n\n• users\n• prediction_history\n• favorite_breeds\n• feedback", ha='center', va='center', fontsize=9, fontweight='bold', color='#0F766E', fontfamily=FONT_FAMILY)

    # Straight Arrows
    arrow_props = dict(facecolor='#475569', edgecolor='#475569', arrowstyle="->", lw=1.4)
    double_arrow = dict(facecolor='#475569', edgecolor='#475569', arrowstyle="<->", lw=1.4)

    # User <-> UI
    ax.annotate("", xy=(1.75, 4.0), xytext=(1.75, 5.2), arrowprops=double_arrow)
    # UI -> Flask
    ax.annotate("", xy=(3.6, 5.4), xytext=(2.8, 5.4), arrowprops=double_arrow)
    # Flask <-> Image Prep
    ax.annotate("", xy=(4.7, 3.3), xytext=(4.7, 4.4), arrowprops=double_arrow)
    # Image Prep -> Stage 1
    ax.annotate("", xy=(6.6, 5.3), xytext=(5.8, 5.3), arrowprops=arrow_props)
    # Stage 1 -> Stage 2
    ax.annotate("", xy=(7.7, 3.4), xytext=(7.7, 4.2), arrowprops=arrow_props)
    # Flask <-> MySQL
    ax.annotate("", xy=(9.6, 5.4), xytext=(5.8, 5.4), arrowprops=double_arrow)

    plt.tight_layout()
    plt.savefig('model/report_assets/fig4_1_system_architecture.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("Created fig4_1_system_architecture.png")

# -----------------------------------------------------------------------------
# 2. FIG 4.2: IMAGE PREPROCESSING FLOWCHART
# -----------------------------------------------------------------------------
def make_fig4_2():
    fig, ax = plt.subplots(figsize=(11, 3.2), dpi=300)
    ax.set_xlim(0, 11)
    ax.set_ylim(0, 3)
    ax.axis('off')

    steps = [
        ("1. Image Upload\n(.jpg, .jpeg, .png)", 0.4, 0.7, 1.4, 1.5),
        ("2. File Validation\n(Size ≤ 10 MB)", 2.2, 0.7, 1.4, 1.5),
        ("3. RGB Conversion\n(3 Channels)", 4.0, 0.7, 1.4, 1.5),
        ("4. Spatial Resizing\n(224 × 224 pixels)", 5.8, 0.7, 1.4, 1.5),
        ("5. Normalization\n([-1.0, +1.0])", 7.6, 0.7, 1.4, 1.5),
        ("6. Input Tensor\n(1, 224, 224, 3)", 9.4, 0.7, 1.4, 1.5)
    ]

    for label, x, y, w, h in steps:
        rect = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.08", fc='#F8FAFC', ec='#2B4C7E', lw=1.2)
        ax.add_patch(rect)
        ax.text(x + w/2, y + h/2, label, ha='center', va='center', fontsize=8.5, fontweight='bold', color=C_TEXT, fontfamily=FONT_FAMILY)

    # Arrows between steps
    arrow_props = dict(facecolor='#2B4C7E', edgecolor='#2B4C7E', arrowstyle="-|>", lw=1.5, mutation_scale=12)
    for i in range(len(steps) - 1):
        x_start = steps[i][1] + steps[i][3]
        x_end = steps[i+1][1]
        y_mid = 0.7 + 0.75
        ax.annotate("", xy=(x_end, y_mid), xytext=(x_start, y_mid), arrowprops=arrow_props)

    plt.tight_layout()
    plt.savefig('model/report_assets/fig4_2_preprocessing_flowchart.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("Created fig4_2_preprocessing_flowchart.png")

# -----------------------------------------------------------------------------
# 3. FIG 4.3: STAGE 1 DOG DETECTOR
# -----------------------------------------------------------------------------
def make_fig4_3():
    fig, ax = plt.subplots(figsize=(10, 4.5), dpi=300)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 5)
    ax.axis('off')

    # Blocks
    # Input
    b1 = patches.FancyBboxPatch((0.5, 2.0), 1.8, 1.2, boxstyle="round,pad=0.08", fc='#F8FAFC', ec='#2B4C7E', lw=1.2)
    ax.add_patch(b1)
    ax.text(1.4, 2.6, "Input Tensor\n(1, 224, 224, 3)", ha='center', va='center', fontsize=9, fontweight='bold', color=C_TEXT)

    # Pretrained MobileNetV2
    b2 = patches.FancyBboxPatch((3.0, 1.8), 2.2, 1.6, boxstyle="round,pad=0.08", fc='#EFF6FF', ec='#1D4ED8', lw=1.3)
    ax.add_patch(b2)
    ax.text(4.1, 2.6, "Pretrained\nMobileNetV2\n(1,000 ImageNet Classes)", ha='center', va='center', fontsize=9, fontweight='bold', color='#1E3A8A')

    # Canine Filter Logic
    b3 = patches.FancyBboxPatch((5.9, 1.7), 2.2, 1.8, boxstyle="round,pad=0.08", fc=C_DECISION_BG, ec=C_DECISION_EDGE, lw=1.3)
    ax.add_patch(b3)
    ax.text(7.0, 2.6, "Canine Validation\nCheck 118 dog classes\nThreshold:\nP(dog) ≥ 0.20", ha='center', va='center', fontsize=8.5, fontweight='bold', color='#92400E')

    # Output decisions
    b_pass = patches.FancyBboxPatch((8.7, 3.2), 1.2, 1.0, boxstyle="round,pad=0.08", fc=C_PASS_BG, ec=C_PASS_EDGE, lw=1.3)
    ax.add_patch(b_pass)
    ax.text(9.3, 3.7, "Dog Confirmed\n(Proceed to\nStage 2)", ha='center', va='center', fontsize=7.5, fontweight='bold', color='#166534')

    b_reject = patches.FancyBboxPatch((8.7, 1.0), 1.2, 1.0, boxstyle="round,pad=0.08", fc=C_REJECT_BG, ec=C_REJECT_EDGE, lw=1.3)
    ax.add_patch(b_reject)
    ax.text(9.3, 1.5, "Non-Dog\n('No Dog\nDetected')", ha='center', va='center', fontsize=7.5, fontweight='bold', color='#991B1B')

    # Arrows
    arr = dict(facecolor='#2B4C7E', edgecolor='#2B4C7E', arrowstyle="-|>", lw=1.4, mutation_scale=12)
    ax.annotate("", xy=(3.0, 2.6), xytext=(2.3, 2.6), arrowprops=arr)
    ax.annotate("", xy=(5.9, 2.6), xytext=(5.2, 2.6), arrowprops=arr)

    arr_pass = dict(facecolor=C_PASS_EDGE, edgecolor=C_PASS_EDGE, arrowstyle="-|>", lw=1.4, mutation_scale=12)
    arr_reject = dict(facecolor=C_REJECT_EDGE, edgecolor=C_REJECT_EDGE, arrowstyle="-|>", lw=1.4, mutation_scale=12)

    ax.annotate("If Yes (≥ 0.20)", xy=(8.7, 3.7), xytext=(8.1, 2.9), arrowprops=arr_pass, fontsize=8, color='#166534', fontweight='bold')
    ax.annotate("If No (< 0.20)", xy=(8.7, 1.5), xytext=(8.1, 2.3), arrowprops=arr_reject, fontsize=8, color='#991B1B', fontweight='bold')

    plt.tight_layout()
    plt.savefig('model/report_assets/fig4_3_stage1_detector.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("Created fig4_3_stage1_detector.png")

# -----------------------------------------------------------------------------
# 4. FIG 4.4: STAGE 2 BREED CLASSIFIER
# -----------------------------------------------------------------------------
def make_fig4_4():
    fig, ax = plt.subplots(figsize=(11, 3.4), dpi=300)
    ax.set_xlim(0, 11)
    ax.set_ylim(0, 3.4)
    ax.axis('off')

    layers = [
        ("Confirmed Canine\nImage Tensor\n(224 × 224 × 3)", 0.4, 0.8, 1.6, 1.8, '#F8FAFC', '#2B4C7E'),
        ("MobileNetV2 Base\n(155 layers, top 30\nfine-tuned, 7×7×1280)", 2.5, 0.8, 2.2, 1.8, '#EFF6FF', '#1D4ED8'),
        ("Global Average\nPooling (GAP)\n(1,280 features)", 5.2, 0.8, 1.6, 1.8, '#F0FDF4', '#16A34A'),
        ("Dropout Layer\n(Rate = 0.30,\nprevents overfit)", 7.2, 0.8, 1.5, 1.8, '#FEF3C7', '#D97706'),
        ("Dense Softmax\n(120 units,\nbreed probabilities)", 9.1, 0.8, 1.6, 1.8, '#FDF2F8', '#DB2777')
    ]

    for label, x, y, w, h, bg, border in layers:
        rect = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.08", fc=bg, ec=border, lw=1.2)
        ax.add_patch(rect)
        ax.text(x + w/2, y + h/2, label, ha='center', va='center', fontsize=8, fontweight='bold', color=C_TEXT)

    arr = dict(facecolor='#2B4C7E', edgecolor='#2B4C7E', arrowstyle="-|>", lw=1.4, mutation_scale=12)
    for i in range(len(layers) - 1):
        x_start = layers[i][1] + layers[i][3]
        x_end = layers[i+1][1]
        y_mid = 0.8 + 0.9
        ax.annotate("", xy=(x_end, y_mid), xytext=(x_start, y_mid), arrowprops=arr)

    plt.tight_layout()
    plt.savefig('model/report_assets/fig4_4_stage2_classifier.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("Created fig4_4_stage2_classifier.png")

# -----------------------------------------------------------------------------
# 5. FIG 4.5: COMPLETE PREDICTION WORKFLOW (FLOWCHART)
# -----------------------------------------------------------------------------
def make_fig4_5():
    fig, ax = plt.subplots(figsize=(8.5, 12), dpi=300)
    ax.set_xlim(0, 8.5)
    ax.set_ylim(0, 12)
    ax.axis('off')

    # Vertically arranged flowchart boxes
    # Center x = 4.25
    y_coords = [
        (11.2, 0.7, "Uploaded Image (User File)", '#F8FAFC', '#2B4C7E'),
        (10.1, 0.7, "Image Validation (Format & Size Check)", '#F8FAFC', '#2B4C7E'),
        (9.0, 0.7, "Image Preprocessing (RGB, 224×224, Normalized)", '#F8FAFC', '#2B4C7E'),
        (7.9, 0.7, "Stage 1: Dog Presence Detection (ImageNet MobileNetV2)", '#EFF6FF', '#1D4ED8'),
        # Decision diamond at y=6.6
        (5.1, 0.7, "Stage 2: Dog Breed Classification (Fine-Tuned Model)", '#EFF6FF', '#1D4ED8'),
        (4.0, 0.7, "Generate 120-Breed Softmax Probabilities", '#F0FDF4', '#16A34A'),
        (2.9, 0.7, "Select Top-1 Primary Breed & Ranked Top-3 Candidates", '#F0FDF4', '#16A34A'),
        (1.8, 0.7, "Display Breed Match, Confidence % & Probability Bars", '#FDF2F8', '#DB2777'),
        (0.7, 0.7, "Store Prediction in MySQL & Enable PDF Report Download", '#F8FAFC', '#0D9488')
    ]

    arr = dict(facecolor='#334155', edgecolor='#334155', arrowstyle="-|>", lw=1.4, mutation_scale=12)

    # Draw boxes
    for y, h, text, bg, border in y_coords:
        rect = patches.FancyBboxPatch((1.5, y), 5.5, h, boxstyle="round,pad=0.08", fc=bg, ec=border, lw=1.2)
        ax.add_patch(rect)
        ax.text(4.25, y + h/2, text, ha='center', va='center', fontsize=9, fontweight='bold', color=C_TEXT)

    # Decision Diamond at y=6.4 to 7.0
    diamond_pts = [(4.25, 7.3), (6.3, 6.6), (4.25, 5.9), (2.2, 6.6)]
    diamond = patches.Polygon(diamond_pts, closed=True, fc=C_DECISION_BG, ec=C_DECISION_EDGE, lw=1.3)
    ax.add_patch(diamond)
    ax.text(4.25, 6.6, "Is a Dog\nDetected?\n(P(dog) ≥ 0.20)", ha='center', va='center', fontsize=8.5, fontweight='bold', color='#92400E')

    # Rejection Box on Right
    rect_rej = patches.FancyBboxPatch((6.8, 6.2), 1.5, 0.8, boxstyle="round,pad=0.08", fc=C_REJECT_BG, ec=C_REJECT_EDGE, lw=1.2)
    ax.add_patch(rect_rej)
    ax.text(7.55, 6.6, "Display Alert:\n'No Dog\nDetected'", ha='center', va='center', fontsize=7.5, fontweight='bold', color='#991B1B')

    # Connecting arrows
    # 1 -> 2
    ax.annotate("", xy=(4.25, 10.8), xytext=(4.25, 11.2), arrowprops=arr)
    # 2 -> 3
    ax.annotate("", xy=(4.25, 9.7), xytext=(4.25, 10.1), arrowprops=arr)
    # 3 -> 4
    ax.annotate("", xy=(4.25, 8.6), xytext=(4.25, 9.0), arrowprops=arr)
    # 4 -> Decision
    ax.annotate("", xy=(4.25, 7.3), xytext=(4.25, 7.9), arrowprops=arr)

    # Decision -> Rejection (No)
    arr_no = dict(facecolor=C_REJECT_EDGE, edgecolor=C_REJECT_EDGE, arrowstyle="-|>", lw=1.4, mutation_scale=12)
    ax.annotate("", xy=(6.8, 6.6), xytext=(6.3, 6.6), arrowprops=arr_no)
    ax.text(6.5, 6.8, "No", ha='center', va='bottom', fontsize=8.5, fontweight='bold', color='#991B1B')

    # Decision -> Stage 2 (Yes)
    arr_yes = dict(facecolor=C_PASS_EDGE, edgecolor=C_PASS_EDGE, arrowstyle="-|>", lw=1.4, mutation_scale=12)
    ax.annotate("", xy=(4.25, 5.8), xytext=(4.25, 5.9), arrowprops=arr_yes)
    ax.text(4.45, 5.85, "Yes", ha='left', va='center', fontsize=8.5, fontweight='bold', color='#16A34A')

    # Stage 2 -> Probabilities
    ax.annotate("", xy=(4.25, 4.7), xytext=(4.25, 5.1), arrowprops=arr)
    # Probabilities -> Top-3
    ax.annotate("", xy=(4.25, 3.6), xytext=(4.25, 4.0), arrowprops=arr)
    # Top-3 -> Display
    ax.annotate("", xy=(4.25, 2.5), xytext=(4.25, 2.9), arrowprops=arr)
    # Display -> Database & Report
    ax.annotate("", xy=(4.25, 1.4), xytext=(4.25, 1.8), arrowprops=arr)

    plt.tight_layout()
    plt.savefig('model/report_assets/fig4_5_complete_workflow.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("Created fig4_5_complete_workflow.png")

if __name__ == '__main__':
    make_fig4_1()
    make_fig4_2()
    make_fig4_3()
    make_fig4_4()
    make_fig4_5()
    print("All methodology diagrams created successfully!")
