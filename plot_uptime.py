import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import re

with open('log_for_chart.txt', encoding='utf-8') as f:
    lines = f.readlines()

if times:
    x = np.arange(len(times))
    y = np.array(statuses)

    plt.style.use('seaborn-v0_8-darkgrid')
    
    # Giảm kích thước chart
    fig, ax = plt.subplots(figsize=(10, 3))  # Thu nhỏ kích thước

    colors = ['#2ecc40' if s == 1 else '#ff4136' for s in y]
    bars = ax.bar(x, y, color=colors, edgecolor='#222', width=0.7, zorder=3)

    # Thu nhỏ điểm đánh dấu
    for i in range(len(x)):
        marker = '*' if i == len(x)-1 else 'o'  # Dấu sao cho điểm cuối
        size = 120 if i == len(x)-1 else 80     # Điểm cuối lớn hơn
        ax.scatter(i, y[i], s=size, color=colors[i], 
                  edgecolor='#222', linewidth=1.5, zorder=4,
                  marker=marker)

    # Thu gọn annotation cho các đợt downtime
    for s, e in streaks:
        count = e - s + 1
        if count > 0:
            downtime_mins = count * 30
            x_mid = (s + e) / 2
            # Thu gọn text và giảm kích thước
            ax.annotate(
                f"{count}x ({downtime_mins}m)",  # Thu gọn text
                xy=(x_mid, 0.1), xycoords='data',
                xytext=(0, 20), textcoords='offset points',  # Giảm offset
                ha='center', va='bottom',
                fontsize=8, color='#b22222',  # Giảm font size
                bbox=dict(boxstyle='round,pad=0.2', 
                         fc='#fff0f0', ec='#ff4136', 
                         lw=1, alpha=0.88)
            )
            ax.axvspan(s-0.35, e+0.35, ymin=0, ymax=0.16, 
                      color='#ff4136', alpha=0.13, zorder=1)

    # Tối ưu hiển thị grid và background
    ax.set_facecolor('#f6fafd')
    fig.patch.set_facecolor('#f6fafd')
    ax.grid(axis='y', linestyle=':', alpha=0.15, zorder=1)

    # Tối ưu các label
    ax.set_ylim(-0.1, 1.1)
    ax.set_yticks([0, 1])
    ax.set_yticklabels(['DOWN', 'UP'], fontsize=9)
    
    # Hiển thị ít nhãn thời gian hơn
    num_ticks = min(5, len(x))  # Giảm số lượng nhãn
    tick_positions = np.linspace(0, len(x)-1, num_ticks, dtype=int)
    ax.set_xticks(tick_positions)
    tick_labels = [times[i].split()[1] for i in tick_positions]  # Chỉ hiển thị giờ:phút
    ax.set_xticklabels(tick_labels, fontsize=8, rotation=0)  # Bỏ rotation

    # Thu gọn legend
    green_patch = mpatches.Patch(color='#2ecc40', label='Up', alpha=0.7)
    red_patch = mpatches.Patch(color='#ff4136', label='Down', alpha=0.7)
    star = plt.Line2D([], [], color='black', marker='*', 
                      linestyle='None', markersize=8, 
                      label='Latest', markerfacecolor='grey')
    ax.legend(handles=[green_patch, red_patch, star], 
             loc='upper left', fontsize=8, frameon=True,
             ncol=3)  # Hiển thị legend trên một hàng

    # Thu gọn title
    ax.set_title('Uptime Monitor (30m)', 
                fontsize=10, pad=8, color='#222')

    # Tối ưu spacing
    plt.tight_layout(pad=1.0)
    
    # Lưu với DPI phù hợp
    plt.savefig('uptime_chart.png', 
                dpi=120,  # Giảm DPI
                bbox_inches='tight',
                transparent=False)
    plt.close()
