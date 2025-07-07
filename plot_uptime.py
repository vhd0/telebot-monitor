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

    fig, ax = plt.subplots(figsize=(14, 4))

    # Bar colors
    colors = ['#2ecc40' if s == 1 else '#ff4136' for s in y]
    bars = ax.bar(x, y, color=colors, edgecolor='#222', width=0.7, zorder=3)

    # Markers
    for i in range(len(x)):
        ax.scatter(x[i], y[i], s=150, color=colors[i], edgecolor='#222', linewidth=1.8, zorder=4)

    # Find and annotate downtime streaks
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
            downtime_mins = count * 30  # 30 phút một lần ping
            x_mid = (s + e) / 2
            ax.annotate(
                f"{downtime_mins} phút downtime\n({count}x fail)",
                xy=(x_mid, 0.1), xycoords='data',
                xytext=(0, 28), textcoords='offset points',
                ha='center', va='bottom',
                fontsize=10, color='#b22222', weight='bold',
                bbox=dict(boxstyle='round,pad=0.32', fc='#fff0f0', ec='#ff4136', lw=1.2, alpha=0.88)
            )
            ax.axvspan(s-0.35, e+0.35, ymin=0, ymax=0.16, color='#ff4136', alpha=0.13, zorder=1)

    # Background and grid
    ax.set_facecolor('#f6fafd')
    fig.patch.set_facecolor('#f6fafd')
    ax.axhspan(-0.1, 0.5, facecolor='#ffe8e8', alpha=0.09, zorder=0)
    ax.axhspan(0.5, 1.1, facecolor='#e8ffe9', alpha=0.06, zorder=0)
    ax.grid(axis='y', linestyle=':', alpha=0.19, zorder=1)

    # Axes and ticks
    ax.set_ylim(-0.1, 1.1)
    ax.set_yticks([0, 1])
    ax.set_yticklabels(['❌ Down', '✅ Up'], fontsize=12, weight='bold')
    xtickstep = max(1, len(x)//10)
    ax.set_xticks(x[::xtickstep])
    ax.set_xticklabels([times[i] for i in range(0, len(times), xtickstep)], 
                       fontsize=9, rotation=38, ha='right')

    # Legend
    green_patch = mpatches.Patch(color='#2ecc40', label='Uptime', alpha=0.7)
    red_patch = mpatches.Patch(color='#ff4136', label='Downtime', alpha=0.7)
    ax.legend(handles=[green_patch, red_patch], loc='upper left', fontsize=11, frameon=True)

    # Title
    ax.set_title('⏱️ Uptime/Downtime Monitor (30 min/ping)', 
                fontsize=16, weight='bold', pad=14, color='#222')

    # Optimize UI
    for spine in ['top', 'right']:
        ax.spines[spine].set_visible(False)
    ax.spines['left'].set_linewidth(1.1)
    ax.spines['bottom'].set_linewidth(1.1)

    plt.tight_layout(pad=1.5)
    plt.savefig('uptime_chart.png', dpi=140, bbox_inches='tight', transparent=False)
    plt.close()
