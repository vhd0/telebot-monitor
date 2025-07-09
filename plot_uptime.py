import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import re
import sys

# Khởi tạo lists trước khi đọc file
times = []
statuses = []

try:
    with open('log_for_chart.txt', encoding='utf-8') as f:
        lines = f.readlines()
        
        # Xử lý từng dòng để lấy thời gian và trạng thái
        for line in lines:
            match = re.match(r'\|\s*(.*?)\s*\|\s*(.*?)\s*\|', line)
            if match:
                times.append(match.group(1))
                # Chỉ quan tâm đến trạng thái ✅/❌, không quan tâm số lần retry
                statuses.append(1 if '✅' in match.group(2) else 0)
    # Chỉ vẽ chart nếu có dữ liệu
    if len(times) > 0:
        x = np.arange(len(times))
        y = np.array(statuses)

        plt.style.use('seaborn-v0_8-darkgrid')
        
        # Tạo figure với kích thước nhỏ gọn
        fig, ax = plt.subplots(figsize=(10, 3))

        # Vẽ bars
        colors = ['#2ecc40' if s == 1 else '#ff4136' for s in y]
        bars = ax.bar(x, y, color=colors, edgecolor='#222', width=0.7, zorder=3)

        # Vẽ markers
        for i in range(len(x)):
            marker = '*' if i == len(x)-1 else 'o'
            size = 120 if i == len(x)-1 else 80
            ax.scatter(i, y[i], s=size, color=colors[i], 
                      edgecolor='#222', linewidth=1.5, zorder=4,
                      marker=marker)

        # Tìm và đánh dấu các đợt downtime
        streaks = []
        start = None
        for i, s in enumerate(y):
            if s == 0 and start is None:
                start = i
            if s == 1 and start is not None:
                streaks.append((start, i - 1))
                start = None
        if start is not None:
            streaks.append((start, len(y) - 1))

        # Annotation cho downtime
        for s, e in streaks:
            count = e - s + 1
            if count > 0:
                downtime_mins = count * 30
                x_mid = (s + e) / 2
                ax.annotate(
                    f"{count}x ({downtime_mins}m)",
                    xy=(x_mid, 0.1), xycoords='data',
                    xytext=(0, 20), textcoords='offset points',
                    ha='center', va='bottom',
                    fontsize=8, color='#b22222',
                    bbox=dict(boxstyle='round,pad=0.2',
                             fc='#fff0f0', ec='#ff4136',
                             lw=1, alpha=0.88)
                )
                ax.axvspan(s-0.35, e+0.35, ymin=0, ymax=0.16,
                          color='#ff4136', alpha=0.13, zorder=1)

        # Thiết lập style
        ax.set_facecolor('#f6fafd')
        fig.patch.set_facecolor('#f6fafd')
        ax.grid(axis='y', linestyle=':', alpha=0.15, zorder=1)

        # Thiết lập axes
        ax.set_ylim(-0.1, 1.1)
        ax.set_yticks([0, 1])
        ax.set_yticklabels(['DOWN', 'UP'], fontsize=9)
        
        # Thiết lập ticks
        num_ticks = min(5, len(x))
        tick_positions = np.linspace(0, len(x)-1, num_ticks, dtype=int)
        ax.set_xticks(tick_positions)
        tick_labels = [times[i].split()[1] for i in tick_positions]
        ax.set_xticklabels(tick_labels, fontsize=8, rotation=0)

        # Legend
        green_patch = mpatches.Patch(color='#2ecc40', label='Up', alpha=0.7)
        red_patch = mpatches.Patch(color='#ff4136', label='Down', alpha=0.7)
        star = plt.Line2D([], [], color='black', marker='*',
                         linestyle='None', markersize=8,
                         label='Latest', markerfacecolor='grey')
        ax.legend(handles=[green_patch, red_patch, star],
                 loc='upper left', fontsize=8, frameon=True,
                 ncol=3)

        # Title
        ax.set_title('Uptime Monitor (30m)',
                    fontsize=10, pad=8, color='#222')

        # Layout
        plt.tight_layout(pad=1.0)
        
        # Lưu chart
        plt.savefig('uptime_chart.png',
                    dpi=120,
                    bbox_inches='tight',
                    transparent=False)
        plt.close()
    else:
        print("Không có dữ liệu để vẽ chart")

except Exception as e:
    print(f"Lỗi khi tạo chart: {str(e)}")
    sys.exit(1)
