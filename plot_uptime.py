import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import re
import sys

try:
    # Đọc dữ liệu từ ping_log.md
    with open('ping_log.md', 'r', encoding='utf-8') as f:
        lines = f.readlines()[2:]  # Bỏ qua header
        
    times = []
    statuses = []
    
    # Chỉ lấy 30 dòng cuối
    for line in lines[-30:]:
        match = re.match(r'\|\s*(.*?)\s*\|\s*(.*?)\s*\|', line)
        if match:
            times.append(match.group(1))
            statuses.append(1 if '✅' in match.group(2) else 0)
    
    if times:
        x = np.arange(len(times))
        y = np.array(statuses)
        
        plt.style.use('seaborn-v0_8-darkgrid')
        fig, ax = plt.subplots(figsize=(10, 3))
        
        # Vẽ bars
        colors = ['#2ecc40' if s == 1 else '#ff4136' for s in y]
        ax.bar(x, y, color=colors, width=0.7, alpha=0.7)
        
        # Đánh dấu điểm
        for i, (status, color) in enumerate(zip(y, colors)):
            marker = '*' if i == len(x)-1 else 'o'
            size = 120 if i == len(x)-1 else 80
            ax.scatter(i, status, s=size, color=color, 
                      edgecolor='#222', linewidth=1.5, zorder=3,
                      marker=marker)
        
        # Style
        ax.set_facecolor('#f8f9fa')
        fig.patch.set_facecolor('#f8f9fa')
        
        # Axes
        ax.set_ylim(-0.1, 1.1)
        ax.set_yticks([0, 1])
        ax.set_yticklabels(['DOWN', 'UP'])
        
        # X ticks
        num_ticks = min(5, len(x))
        tick_positions = np.linspace(0, len(x)-1, num_ticks, dtype=int)
        ax.set_xticks(tick_positions)
        tick_labels = [times[i].split()[1] for i in tick_positions]  # Chỉ hiển thị giờ:phút
        ax.set_xticklabels(tick_labels, rotation=0)
        
        # Legend
        handles = [
            mpatches.Patch(color='#2ecc40', alpha=0.7, label='Up'),
            mpatches.Patch(color='#ff4136', alpha=0.7, label='Down'),
            plt.Line2D([], [], color='black', marker='*', 
                      linestyle='None', label='Latest')
        ]
        ax.legend(handles=handles, loc='upper left', ncol=3)
        
        plt.title('Uptime Monitor (30m)', pad=10)
        plt.tight_layout()
        
        plt.savefig('uptime_chart.png', dpi=100, bbox_inches='tight')
        plt.close()

except Exception as e:
    print(f"Lỗi khi tạo chart: {str(e)}", file=sys.stderr)
    sys.exit(1)
