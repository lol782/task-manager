# main.py
import streamlit as st
import time
import random
import os
import json
import pandas as pd
import matplotlib.pyplot as plt
from core.process_manager import ProcessManager, Process
from core.scheduler import Scheduler
from core.resource_analyzer import ResourceAnalyzer
from core.network import Network
from ui.dashboard import show_dashboard
from ui.process_table import show_process_table
from ui.control_panel import show_control_panel
from utils.visualizer import get_gantt_chart_figure

# Page configuration
st.set_page_config(
    page_title="Custom Task Manager",
    page_icon="🖥️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Function to load dummy processes from JSON
def load_dummy_processes():
    try:
        if os.path.exists('data/dummy_processes.json'):
            with open('data/dummy_processes.json', 'r') as file:
                data = json.load(file)
                processes = []
                for proc_data in data['processes']:
                    process = Process(
                        proc_data['pid'],
                        proc_data['name'],
                        proc_data['status'],
                        proc_data['cpu_usage'],
                        proc_data['memory_usage'],
                        proc_data['priority'],
                        proc_data.get('start_time', time.time())
                    )
                    processes.append(process)
                return processes
        return None
    except Exception as e:
        st.error(f"Error loading dummy processes: {e}")
        return None

# Initialize session state for persistence
if 'process_manager' not in st.session_state:
    st.session_state.process_manager = ProcessManager()
    
    # Try to load dummy processes from JSON file
    dummy_processes = load_dummy_processes()
    
    if dummy_processes:
        for process in dummy_processes:
            st.session_state.process_manager.add_process(process)
    else:
        # If loading fails, add some hardcoded dummy processes
        st.session_state.process_manager.add_process(Process(1001, "System", "Running", 25, 40, 10))
        st.session_state.process_manager.add_process(Process(1002, "Browser", "Running", 35, 60, 7))
        st.session_state.process_manager.add_process(Process(1003, "IDE", "Waiting", 5, 30, 5))
        st.session_state.process_manager.add_process(Process(1004, "Background Service", "Stopped", 0, 15, 3))

if 'scheduler' not in st.session_state:
    st.session_state.scheduler = Scheduler()

if 'resource_analyzer' not in st.session_state:
    st.session_state.resource_analyzer = ResourceAnalyzer()

if 'network' not in st.session_state:
    st.session_state.network = Network()

# Update resource data with current scheduling algorithm
st.session_state.resource_analyzer.update(
    st.session_state.process_manager.get_processes(),
    st.session_state.scheduler.algorithm
)
st.session_state.network.update()

# App title
st.title("🖥️ Custom Task Manager")

# Add a sidebar to show current system state
st.sidebar.header("System Status")
st.sidebar.info(f"Current Scheduling Algorithm: {st.session_state.scheduler.algorithm}")
st.sidebar.metric("Total Processes", len(st.session_state.process_manager.get_processes()))
running_count = len([p for p in st.session_state.process_manager.get_processes() if p.status == "Running"])
st.sidebar.metric("Running Processes", running_count)

# Create tabs for different sections
tab1, tab2, tab3, tab4 = st.tabs(["Dashboard", "Processes", "Control Panel", "Network Details"])

with tab1:
    show_dashboard(st.session_state.resource_analyzer, st.session_state.network)
    
    # Display Gantt chart as a separate section with clear heading
    st.header("Process Allocation (Gantt Chart)")
    fig = get_gantt_chart_figure(st.session_state.process_manager.get_processes())
    st.pyplot(fig)
    
    # Add process-specific metrics based on the scheduling algorithm
    st.subheader("Process CPU Allocation")
    processes = st.session_state.process_manager.get_processes()
    if processes:
        # Create a dataframe showing how CPU is allocated based on the algorithm
        cpu_data = []
        for p in processes:
            if p.status == "Running":
                cpu_data.append({
                    "Process": f"{p.name} (PID: {p.pid})",
                    "CPU Share (%)": p.current_cpu if hasattr(p, 'current_cpu') else p.cpu_usage,
                    "Priority": p.priority
                })
        
        if cpu_data:
            cpu_df = pd.DataFrame(cpu_data)
            st.bar_chart(cpu_df.set_index("Process")["CPU Share (%)"])
        else:
            st.info("No running processes to show CPU allocation.")
    
    # Add performance metrics section
    st.subheader("Scheduling Performance Metrics")
    col1, col2 = st.columns(2)

    with col1:
        # Calculate and display average waiting time
        waiting_processes = [p for p in processes if p.status == "Waiting"]
        if waiting_processes:
            avg_waiting_time = sum([(time.time() - p.start_time) for p in waiting_processes]) / len(waiting_processes)
            st.metric("Avg. Waiting Time", f"{avg_waiting_time:.2f}s")
        else:
            st.metric("Avg. Waiting Time", "0.00s")

    with col2:
        # Calculate and display throughput (completed processes)
        # For simulation, we'll just show running processes as throughput
        st.metric("Throughput", f"{running_count} processes")

with tab2:
    show_process_table(st.session_state.process_manager, st.session_state.scheduler)

with tab3:
    show_control_panel(st.session_state.process_manager, st.session_state.scheduler)

with tab4:
    st.header("Network Details")
    
    # Show network graph
    st.subheader("Network Usage Over Time")
    network_data = st.session_state.network.get_network_usage()
    if network_data:
        st.line_chart(pd.DataFrame({'Network Usage (KB/s)': network_data}))
    else:
        st.info("No network data available.")
    
    # Add network connections table
    st.subheader("Network Connections")
    
    # Generate some dummy network connection data
    connections = []
    protocols = ["TCP", "UDP", "HTTP", "HTTPS"]
    statuses = ["ESTABLISHED", "LISTENING", "CLOSED", "TIME_WAIT"]
    
    # Associate network connections with actual processes
    processes = st.session_state.process_manager.get_processes()
    for i in range(min(5, len(processes))):
        p = processes[i]
        connections.append({
            "Process": f"{p.name} (PID: {p.pid})",
            "Local Address": f"192.168.1.{random.randint(1, 255)}:{random.randint(1000, 65000)}",
            "Remote Address": f"172.16.{random.randint(1, 255)}.{random.randint(1, 255)}:{random.randint(1, 65000)}",
            "Protocol": random.choice(protocols),
            "Status": random.choice(statuses),
            "Bytes Sent": random.randint(100, 10000),
            "Bytes Received": random.randint(100, 10000)
        })
    
    # Display the network connections table
    st.table(pd.DataFrame(connections))

# Add a footer
st.markdown("---")
st.markdown("Custom Task Manager Simulation - v1.0")

# Update process statuses based on scheduler
scheduled_processes = st.session_state.scheduler.schedule(
    st.session_state.process_manager.get_processes()
)
st.session_state.process_manager.processes = scheduled_processes

# Auto-refresh the app every 5 seconds to simulate real-time updates
time.sleep(1)
st.rerun()
