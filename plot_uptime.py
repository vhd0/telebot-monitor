import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import re

with open('log_for_chart.txt', encoding='utf-8') as f:
    lines = f.readlines()

times = []
statuses = []

for line in lines:
    match = re.match(r'\|\s*(.*?)\s*\|\s*(.*?)\s*\|', line)
    if match:
        times.append(match.group(1))
        statuses.append(1 if '✅' in match.group(2) else 0)

if times:
    x = np.arange(len(times))
    y = np.array(statuses)

    plt.style.use('seaborn-v0_8-darkgrid')
    
    # Điều chỉnh kích thước chart nhỏ hơn
    fig, ax = plt.subplots(figsize=(12, 4))

    colors = ['#2ecc40' if s == 1 else '#ff4136' for s in y]
    bars = ax.bar(x, y, color=colors, edgecolor='#222', width=0.7, zorder=3)

    # Đánh dấu điểm cuối cùng để dễ nhận biết
    last_x = len(x) - 1
    last_color = colors[last_x]
    ax.scatter(last_x, y[last_x], s=200, color=last_color, 
              edgecolor='#222', linewidth=2, zorder=5,
              marker='*')  # Dùng dấu sao cho điểm cuối

    # Các điểm còn lại nhỏ hơn
    for i in range(len(x)-1):
        ax.scatter(i, y[i], s=100, color=colors[i], 
                  edgecolor='#222', linewidth=1.5, zorder=4)

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

    for s, e in streaks:
        count = e - s + 1
        if count > 0:
            downtime_mins = count * 30
            x_mid = (s + e) / 2
            ax.annotate(
                f"{downtime_mins}m down\n({count} fails)",
                xy=(x_mid, 0.1), xycoords='data',
                xytext=(0, 25), textcoords='offset points',
                ha='center', va='bottom',
                fontsize=9, color='#b22222', weight='bold',
                bbox=dict(boxstyle='round,pad=0.2', fc='#fff0f0', 
                         ec='#ff4136', lw=1, alpha=0.88)
            )
            ax.axvspan(s-0.35, e+0.35, ymin=0, ymax=0.16, 
                      color='#ff4136', alpha=0.13, zorder=1)

    ax.set_facecolor('#f6fafd')
    fig.patch.set_facecolor('#f6fafd')
    ax.axhspan(-0.1, 0.5, facecolor='#ffe8e8', alpha=0.09, zorder=0)
    ax.axhspan(0.5, 1.1, facecolor='#e8ffe9', alpha=0.06, zorder=0)
    ax.grid(axis='y', linestyle=':', alpha=0.19, zorder=1)

    ax.set_ylim(-0.1, 1.1)
    ax.set_yticks([0, 1])
    ax.set_yticklabels(['DOWN', 'UP'], fontsize=10, weight='bold')
    
    # Hiển thị ít nhãn thời gian hơn, tập trung vào điểm cuối
    num_ticks = min(6, len(x))  # Tối đa 6 nhãn
    tick_positions = np.linspace(0, len(x)-1, num_ticks, dtype=int)
    ax.set_xticks(tick_positions)
    tick_labels = [times[i] for i in tick_positions]
    ax.set_xticklabels(tick_labels, fontsize=8, rotation=30, ha='right')

    green_patch = mpatches.Patch(color='#2ecc40', label='Uptime', alpha=0.7)
    red_patch = mpatches.Patch(color='#ff4136', label='Downtime', alpha=0.7)
    star_marker = plt.Line2D([], [], color='black', marker='*', 
                            linestyle='None', markersize=10, 
                            label='Latest Check', markerfacecolor='grey')
    ax.legend(handles=[green_patch, red_patch, star_marker], 
             loc='upper left', fontsize=9, frameon=True)

    ax.set_title('Uptime Monitor (30min interval)', 
                fontsize=12, weight='bold', pad=10, color='#222')

    for spine in ['top', 'right']:
        ax.spines[spine].set_visible(False)
    ax.spines['left'].set_linewidth(1)
    ax.spines['bottom'].set_linewidth(1)

    plt.tight_layout(pad=1.5)
    
    plt.rcParams['font.family'] = 'DejaVu Sans'
    plt.savefig('uptime_chart.png', 
                dpi=150,
                bbox_inches='tight',
                transparent=False,
                format='png',
                metadata={'Author': 'GitHub Actions'})
    plt.close()
