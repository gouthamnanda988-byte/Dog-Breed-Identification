"""
generate_academic_diagrams.py
==============================
Generates publication-quality academic architecture diagrams for the B.Tech project report.
"""
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches

os.makedirs('model/report_assets', exist_ok=True)

# -------------------------------------------------------------------------
# 1. Overall System Architecture
# -------------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(12, 6.5))
ax.set_xlim(0, 12)
ax.set_ylim(0, 7)
ax.axis('off')

# Colors
c_client = '#E8C9A4'
c_flask  = '#D4A574'
c_ml     = '#8B5E3C'
c_db     = '#5C3A1E'
c_box    = '#FFF8ED'

# User / Client Tier
r1 = patches.FancyBboxPatch((0.5, 2.2), 2.2, 3.0, boxstyle="round,pad=0.2", facecolor=c_client, edgecolor='#8B5E3C', linewidth=2)
ax.add_patch(r1)
ax.text(1.6, 4.8, 'CLIENT TIER', fontsize=11, fontweight='bold', ha='center', color='#3E2515')
ax.text(1.6, 4.2, 'Web Browser', fontsize=10, ha='center', fontweight='bold', color='#3E2515')
ax.text(1.6, 3.6, '- Drag & Drop Upload\n- Real-Time Results\n- Breed Comparison\n- PDF Report View\n- Admin Dashboard', fontsize=8.5, ha='center', color='#3E2515')

# Arrow 1
ax.annotate('', xy=(3.4, 3.7), xytext=(2.7, 3.7), arrowprops=dict(arrowstyle="->", lw=2.5, color='#8B5E3C'))
ax.text(3.05, 4.0, 'HTTP / REST', fontsize=8, ha='center', color='#5C3A1E', fontweight='bold')

# Web Application Tier (Flask)
r2 = patches.FancyBboxPatch((3.5, 1.8), 2.6, 3.8, boxstyle="round,pad=0.2", facecolor=c_flask, edgecolor='#8B5E3C', linewidth=2)
ax.add_patch(r2)
ax.text(4.8, 5.2, 'APPLICATION TIER', fontsize=11, fontweight='bold', ha='center', color='#FFFFFF')
ax.text(4.8, 4.6, 'Flask Web Framework', fontsize=10, ha='center', fontweight='bold', color='#FFFFFF')
ax.text(4.8, 3.7, '- app.py & config.py\n- Input Validation\n- Session Auth & RBAC\n- REST API Endpoints\n- PDF Report Generator\n  (ReportLab 5.1.0)', fontsize=8.5, ha='center', color='#3E2515')

# Arrow 2 (to ML)
ax.annotate('', xy=(6.9, 4.6), xytext=(6.1, 4.6), arrowprops=dict(arrowstyle="->", lw=2.5, color='#8B5E3C'))
ax.text(6.5, 4.9, 'Preprocessed\nTensor', fontsize=8, ha='center', color='#5C3A1E', fontweight='bold')

# Arrow 3 (to DB)
ax.annotate('', xy=(6.9, 2.6), xytext=(6.1, 2.6), arrowprops=dict(arrowstyle="<->", lw=2.5, color='#5C3A1E'))
ax.text(6.5, 2.1, 'Parameterized\nSQL Queries', fontsize=8, ha='center', color='#5C3A1E', fontweight='bold')

# ML Engine Tier
r3 = patches.FancyBboxPatch((7.0, 3.6), 4.5, 2.6, boxstyle="round,pad=0.2", facecolor=c_ml, edgecolor='#3E2515', linewidth=2)
ax.add_patch(r3)
ax.text(9.25, 5.8, 'DEEP LEARNING TIER (TensorFlow / Keras)', fontsize=10.5, fontweight='bold', ha='center', color='#FFFFFF')
ax.text(9.25, 5.15, 'Stage 1: Pretrained ImageNet MobileNetV2 (Dog Presence Filter)', fontsize=8.5, ha='center', color='#FFF8ED')
ax.text(9.25, 4.55, 'Stage 2: Fine-Tuned MobileNetV2 (120 Dog Breeds)', fontsize=8.5, ha='center', color='#FFF8ED', fontweight='bold')
ax.text(9.25, 3.95, '- Input: 224x224x3 | Dropout(0.3) | Softmax 120\n- Top-1 Match + Top-3 Confidence Distributions', fontsize=8, ha='center', color='#FFF8ED')

# Database Tier
r4 = patches.FancyBboxPatch((7.0, 1.0), 4.5, 2.2, boxstyle="round,pad=0.2", facecolor=c_db, edgecolor='#3E2515', linewidth=2)
ax.add_patch(r4)
ax.text(9.25, 2.8, 'DATABASE TIER (MySQL - dog_breed_db)', fontsize=10.5, fontweight='bold', ha='center', color='#FFFFFF')
ax.text(9.25, 2.2, '- users (user_id, username, email, password_hash, is_admin)\n- prediction_history (prediction_id, breed, conf, top3, timestamp)\n- favorite_breeds (favorite_id, user_id, breed_name)\n- feedback (feedback_id, user_id, message, rating 1-5)', fontsize=8, ha='center', color='#E8C9A4')

plt.title('Complete End-to-End System Architecture of Dog Breed Identification Platform', fontsize=13, fontweight='bold', pad=15, color='#3E2515')
plt.tight_layout()
plt.savefig('model/report_assets/system_architecture.png', dpi=200)
plt.close()
print('[OK] Generated model/report_assets/system_architecture.png')

# -------------------------------------------------------------------------
# 2. Two-Stage Prediction Pipeline Diagram
# -------------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(12, 5.5))
ax.set_xlim(0, 12)
ax.set_ylim(0, 6)
ax.axis('off')

# Input Box
b_in = patches.FancyBboxPatch((0.4, 2.2), 1.8, 1.8, boxstyle="round,pad=0.15", facecolor='#FFF3E2', edgecolor='#8B5E3C', linewidth=2)
ax.add_patch(b_in)
ax.text(1.3, 3.3, 'USER IMAGE', fontsize=10, fontweight='bold', ha='center', color='#5C3A1E')
ax.text(1.3, 2.7, 'JPG / JPEG / PNG\nMax 10 MB', fontsize=8.5, ha='center', color='#5A3E2B')

# Arrow
ax.annotate('', xy=(2.7, 3.1), xytext=(2.2, 3.1), arrowprops=dict(arrowstyle="->", lw=2, color='#8B5E3C'))

# Preprocessing
b_prep = patches.FancyBboxPatch((2.7, 2.0), 2.0, 2.2, boxstyle="round,pad=0.15", facecolor='#F5EBDA', edgecolor='#8B5E3C', linewidth=2)
ax.add_patch(b_prep)
ax.text(3.7, 3.7, 'PREPROCESSING', fontsize=9.5, fontweight='bold', ha='center', color='#5C3A1E')
ax.text(3.7, 2.9, '- RGB Conversion\n- Resize to 224x224\n- MobileNetV2 Scale\n  [-1, +1]', fontsize=8, ha='center', color='#5A3E2B')

# Arrow
ax.annotate('', xy=(5.2, 3.1), xytext=(4.7, 3.1), arrowprops=dict(arrowstyle="->", lw=2, color='#8B5E3C'))

# Stage 1 Detector
b_st1 = patches.FancyBboxPatch((5.2, 2.0), 2.5, 2.2, boxstyle="round,pad=0.15", facecolor='#E8C9A4', edgecolor='#8B5E3C', linewidth=2)
ax.add_patch(b_st1)
ax.text(6.45, 3.8, 'STAGE 1: DETECTOR', fontsize=9.5, fontweight='bold', ha='center', color='#3E2515')
ax.text(6.45, 3.3, 'Pretrained MobileNetV2', fontsize=8.5, ha='center', color='#3E2515', fontweight='bold')
ax.text(6.45, 2.6, 'Checks 118 Dog Classes\nin ImageNet\nThreshold: P(dog) >= 0.20', fontsize=8, ha='center', color='#3E2515')

# Reject Branch (Downward)
ax.annotate('', xy=(6.45, 0.7), xytext=(6.45, 2.0), arrowprops=dict(arrowstyle="->", lw=2, color='#C0392B'))
ax.text(6.55, 1.35, 'No Dog Detected\n(P < 0.20)', fontsize=8, ha='left', color='#C0392B', fontweight='bold')
b_rej = patches.FancyBboxPatch((5.2, 0.1), 2.5, 0.6, boxstyle="round,pad=0.1", facecolor='#FDEDEC', edgecolor='#C0392B', linewidth=1.5)
ax.add_patch(b_rej)
ax.text(6.45, 0.4, 'Reject: "No Dog Detected"', fontsize=8.5, fontweight='bold', ha='center', color='#C0392B')

# Accept Branch (Forward)
ax.annotate('', xy=(8.3, 3.1), xytext=(7.7, 3.1), arrowprops=dict(arrowstyle="->", lw=2.5, color='#27AE60'))
ax.text(8.0, 3.4, 'Dog Validated', fontsize=8, ha='center', color='#27AE60', fontweight='bold')

# Stage 2 Classifier
b_st2 = patches.FancyBboxPatch((8.3, 2.0), 3.3, 2.2, boxstyle="round,pad=0.15", facecolor='#8B5E3C', edgecolor='#3E2515', linewidth=2)
ax.add_patch(b_st2)
ax.text(9.95, 3.8, 'STAGE 2: BREED CLASSIFIER', fontsize=9.5, fontweight='bold', ha='center', color='#FFFFFF')
ax.text(9.95, 3.3, 'Fine-Tuned MobileNetV2', fontsize=8.5, ha='center', color='#FFF8ED', fontweight='bold')
ax.text(9.95, 2.5, '120 Breed Softmax Vector\nTop-1 Match + Confidence %\nTop-3 Ranked Alternatives', fontsize=8, ha='center', color='#FFF8ED')

# Final Arrow
ax.annotate('', xy=(9.95, 0.7), xytext=(9.95, 2.0), arrowprops=dict(arrowstyle="->", lw=2, color='#8B5E3C'))
b_out = patches.FancyBboxPatch((8.3, 0.1), 3.3, 0.6, boxstyle="round,pad=0.1", facecolor='#E8F8F5', edgecolor='#27AE60', linewidth=1.5)
ax.add_patch(b_out)
ax.text(9.95, 0.4, 'Results Display & MySQL History Insert', fontsize=8.5, fontweight='bold', ha='center', color='#1E8449')

plt.title('Two-Stage Canine Detection and Classification Inference Workflow', fontsize=13, fontweight='bold', pad=15, color='#3E2515')
plt.tight_layout()
plt.savefig('model/report_assets/two_stage_pipeline.png', dpi=200)
plt.close()
print('[OK] Generated model/report_assets/two_stage_pipeline.png')

# -------------------------------------------------------------------------
# 3. Model Neural Network Architecture Layer Diagram
# -------------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(11, 4.5))
ax.set_xlim(0, 11)
ax.set_ylim(0, 4)
ax.axis('off')

boxes = [
    ('Input Image\n(224 x 224 x 3)', '#FFF3E2', 0.8),
    ('MobileNetV2 Base\n(155 Layers)\nPretrained ImageNet\n[Frozen early, 30 fine-tuned]', '#D4A574', 2.3),
    ('GlobalAverage\nPooling2D\nShape: (1280,)', '#A97B5A', 5.3),
    ('Dropout (0.3)\nRegularization\n(30% rate)', '#E8C9A4', 7.3),
    ('Dense (120)\nSoftmax\n120 Dog Breeds', '#8B5E3C', 9.2)
]

for label, col, x_pos in boxes:
    w = 1.5 if 'Dense' in label or 'Dropout' in label or 'Global' in label or 'Input' in label else 2.4
    patch = patches.FancyBboxPatch((x_pos, 1.2), w, 1.8, boxstyle="round,pad=0.15", facecolor=col, edgecolor='#3E2515', linewidth=1.8)
    ax.add_patch(patch)
    text_col = '#FFFFFF' if col in ['#8B5E3C', '#A97B5A'] else '#3E2515'
    ax.text(x_pos + w/2, 2.1, label, ha='center', va='center', fontsize=8.5, fontweight='bold', color=text_col)

# Arrows between boxes
arrows = [
    (0.8 + 1.5, 2.3),
    (2.3 + 2.4, 5.3),
    (5.3 + 1.5, 7.3),
    (7.3 + 1.5, 9.2)
]
for x1, x2 in arrows:
    ax.annotate('', xy=(x2, 2.1), xytext=(x1, 2.1), arrowprops=dict(arrowstyle="->", lw=2, color='#5C3A1E'))

plt.title('Layered Transfer Learning Architecture of MobileNetV2 for 120-Breed Classification', fontsize=12, fontweight='bold', pad=15, color='#3E2515')
plt.tight_layout()
plt.savefig('model/report_assets/cnn_architecture.png', dpi=200)
plt.close()
print('[OK] Generated model/report_assets/cnn_architecture.png')
