"""
generate_report_charts.py
=========================
Generates high-resolution academic charts from real experimental metrics in performance_metrics.json.
Used directly in the B.Tech project report.
"""
import os
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

os.makedirs('model/report_assets', exist_ok=True)

with open('model/performance_metrics.json', 'r', encoding='utf-8') as f:
    m = json.load(f)

# 1. Training & Validation Curves
hist = m.get('history', {})
epochs = range(1, len(hist['train_accuracy']) + 1)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5))
fig.suptitle('MobileNetV2 Fine-Tuning Performance Across 15 Epochs', fontsize=14, fontweight='bold', color='#3E2515')

ax1.plot(epochs, [a * 100 for a in hist['train_accuracy']], marker='o', color='#8B5E3C', linewidth=2, label='Training Accuracy')
ax1.plot(epochs, [a * 100 for a in hist['val_accuracy']], marker='s', color='#D4A574', linewidth=2, linestyle='--', label='Validation Accuracy')
ax1.set_title('Accuracy Progression (%)', fontsize=12, fontweight='bold', color='#5C3A1E')
ax1.set_xlabel('Epoch', fontsize=10)
ax1.set_ylabel('Accuracy (%)', fontsize=10)
ax1.set_ylim(20, 100)
ax1.grid(True, alpha=0.3)
ax1.legend(loc='lower right')
ax1.set_facecolor('#FFFDF9')

ax2.plot(epochs, hist['train_loss'], marker='o', color='#8B5E3C', linewidth=2, label='Training Loss')
ax2.plot(epochs, hist['val_loss'], marker='s', color='#D4A574', linewidth=2, linestyle='--', label='Validation Loss')
ax2.set_title('Loss Convergence (Categorical Crossentropy)', fontsize=12, fontweight='bold', color='#5C3A1E')
ax2.set_xlabel('Epoch', fontsize=10)
ax2.set_ylabel('Loss', fontsize=10)
ax2.grid(True, alpha=0.3)
ax2.legend(loc='upper right')
ax2.set_facecolor('#FFFDF9')

plt.tight_layout()
plt.savefig('model/report_assets/training_curves.png', dpi=200)
plt.close()
print('[OK] Generated model/report_assets/training_curves.png')

# 2. Confused Breeds Horizontal Bar Chart
conf = m.get('commonly_confused_breeds', m.get('top_confusions', []))
if conf:
    labels = [f"{c['actual_breed']} -> {c['predicted_breed']}" for c in conf[:12]][::-1]
    counts = [c['count'] for c in conf[:12]][::-1]

    plt.figure(figsize=(11, 6.5))
    bars = plt.barh(labels, counts, color='#8B5E3C', edgecolor='#5C3A1E')
    plt.title('Top 12 Most Frequently Confused Dog Breed Pairs in Evaluation Set', fontsize=13, fontweight='bold', color='#3E2515')
    plt.xlabel('Number of Misclassified Images (Validation & Test Sets)', fontsize=11)
    plt.xlim(0, max(counts) + 2)
    for bar in bars:
        w = bar.get_width()
        plt.text(w + 0.15, bar.get_y() + bar.get_height()/2, f'{int(w)} images', va='center', ha='left', fontsize=9, color='#3E2515', fontweight='bold')
    plt.grid(axis='x', alpha=0.3)
    plt.tight_layout()
    plt.savefig('model/report_assets/confused_breeds_chart.png', dpi=200)
    plt.close()
    print('[OK] Generated model/report_assets/confused_breeds_chart.png')
