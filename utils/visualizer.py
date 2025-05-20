# utils/visualizer.py
import matplotlib.pyplot as plt
import numpy as np
import io
import base64
from matplotlib.colors import LinearSegmentedColormap

def create_gantt_chart(processes):
    # Sort processes by priority
    sorted_processes = sorted(processes, key=lambda x: x.priority, reverse=True)
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Custom colors for different statuses
    colors = {
        'Running': '#4CAF50',  # Green
        'Waiting': '#FFC107',  # Yellow
        'Stopped': '#F44336'   # Red
    }
    
    y_ticks = []
    y_labels = []
    
    for i, process in enumerate(sorted_processes):
        y_pos = len(sorted_processes) - i
        y_ticks.append(y_pos)
        y_labels.append(f"{process.name} (PID: {process.pid})")
        
        # Create a bar for each process
        ax.barh(y_pos, process.cpu_usage, left=0, height=0.5, 
                color=colors.get(process.status, '#9E9E9E'),
                alpha=0.8)
        
        # Add text inside the bar
        ax.text(process.cpu_usage/2, y_pos, f"{process.status}", 
                ha='center', va='center', color='white', fontweight='bold')
    
    # Customize the chart
    ax.set_yticks(y_ticks)
    ax.set_yticklabels(y_labels)
    ax.set_xlabel('CPU Usage (%)')
    ax.set_title('Process Gantt Chart')
    ax.grid(axis='x', linestyle='--', alpha=0.7)
    
    # Add a legend
    from matplotlib.patches import Patch
    legend_elements = [Patch(facecolor=color, label=status) 
                       for status, color in colors.items()]
    ax.legend(handles=legend_elements, loc='upper right')
    
    # Convert plot to PNG image
    buf = io.BytesIO()
    plt.tight_layout()
    fig.savefig(buf, format='png')
    buf.seek(0)
    plt.close(fig)
    
    return buf

def get_gantt_chart_as_base64(processes):
    buf = create_gantt_chart(processes)
    data = base64.b64encode(buf.read()).decode('utf-8')
    return data
def get_gantt_chart_figure(processes):
    import matplotlib.pyplot as plt
    from matplotlib.patches import Patch
    # Sort processes by priority
    sorted_processes = sorted(processes, key=lambda x: x.priority, reverse=True)
    fig, ax = plt.subplots(figsize=(10, 6))
    colors = {'Running': '#4CAF50', 'Waiting': '#FFC107', 'Stopped': '#F44336'}
    y_ticks = []
    y_labels = []
    for i, process in enumerate(sorted_processes):
        y_pos = len(sorted_processes) - i
        y_ticks.append(y_pos)
        y_labels.append(f"{process.name} (PID: {process.pid})")
        ax.barh(y_pos, process.cpu_usage, left=0, height=0.5, color=colors.get(process.status, '#9E9E9E'), alpha=0.8)
        ax.text(process.cpu_usage/2, y_pos, f"{process.status}", ha='center', va='center', color='white', fontweight='bold')
    ax.set_yticks(y_ticks)
    ax.set_yticklabels(y_labels)
    ax.set_xlabel('CPU Usage (%)')
    ax.set_title('Process Gantt Chart')
    ax.grid(axis='x', linestyle='--', alpha=0.7)
    legend_elements = [Patch(facecolor=color, label=status) for status, color in colors.items()]
    ax.legend(handles=legend_elements, loc='upper right')
    plt.tight_layout()
    return fig
