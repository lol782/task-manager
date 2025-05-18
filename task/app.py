import streamlit as st
import pandas as pd
import psutil
import time
import os
import platform
from datetime import datetime

import process_utils as pu
import system_stats as ss

# Set page configuration
st.set_page_config(
    page_title="System Task Manager",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply custom CSS
with open("assets/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Page title
st.title("📊 System Task Manager")

# Sidebar
st.sidebar.title("Controls")

# Refresh rate
refresh_rate = st.sidebar.slider(
    "Refresh Rate (seconds)",
    min_value=1,
    max_value=60,
    value=3
)

# View options
view = st.sidebar.radio(
    "View",
    ["Dashboard", "Processes", "System Information", "Disk Usage", "Network Statistics"]
)

# Add kill process option in sidebar when in Processes view
if view == "Processes":
    sort_option = st.sidebar.selectbox(
        "Sort processes by:",
        ["CPU Usage (%)", "Memory Usage (%)", "PID", "Name"]
    )
    
    filter_option = st.sidebar.text_input("Filter processes (name contains):")
    
    show_count = st.sidebar.slider(
        "Number of processes to display",
        min_value=10,
        max_value=100,
        value=25
    )
    
    with st.sidebar.expander("Process Actions"):
        pid_to_kill = st.number_input("Enter PID to terminate:", min_value=0, step=1)
        if st.button("Terminate Process"):
            if pid_to_kill > 0:
                success = pu.kill_process(pid_to_kill)
                if success:
                    st.sidebar.success(f"Process with PID {pid_to_kill} terminated successfully!")
                else:
                    st.sidebar.error(f"Failed to terminate process with PID {pid_to_kill}")

# Main content area
if view == "Dashboard":
    # Create 4 columns for the main system metrics
    col1, col2, col3, col4 = st.columns(4)
    
    # Function to format size in human-readable format
    def format_size(bytes):
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if bytes < 1024:
                return f"{bytes:.2f} {unit}"
            bytes /= 1024
        return f"{bytes:.2f} PB"

    # Placeholder for metrics that will be updated
    cpu_metric = col1.metric("CPU Usage", "0%")
    mem_metric = col2.metric("Memory Usage", "0%")
    disk_metric = col3.metric("Disk Usage", "0%")
    net_metric = col4.metric("Network Usage", "0 KB/s")
    
    # Create tabs for additional info
    tab1, tab2 = st.tabs(["Top Processes", "System Overview"])
    
    with tab1:
        processes_placeholder = st.empty()
    
    with tab2:
        sys_info_col1, sys_info_col2 = st.columns(2)
        
        with sys_info_col1:
            st.subheader("System Information")
            system_info = {
                "Operating System": platform.system(),
                "OS Version": platform.version(),
                "Machine": platform.machine(),
                "Processor": platform.processor(),
                "Python Version": platform.python_version(),
                "Hostname": platform.node()
            }
            st.table(pd.DataFrame(list(system_info.items()), columns=["Property", "Value"]))
        
        with sys_info_col2:
            st.subheader("Memory Details")
            memory_placeholder = st.empty()
    
    # Main dashboard refresh loop
    while view == "Dashboard":
        # CPU Usage
        cpu_percent = ss.get_cpu_usage()
        col1.metric("CPU Usage", f"{cpu_percent:.1f}%", delta=f"{cpu_percent - ss.get_cpu_usage(delay=0):.1f}%")
        
        # Memory usage
        mem_info = ss.get_memory_info()
        mem_percent = mem_info['percent']
        mem_used = format_size(mem_info['used'])
        mem_total = format_size(mem_info['total'])
        col2.metric("Memory Usage", f"{mem_percent:.1f}%", delta=None, help=f"Used: {mem_used} / Total: {mem_total}")
        
        # Disk usage
        disk_info = ss.get_disk_info()
        disk_percent = disk_info['percent']
        disk_used = format_size(disk_info['used'])
        disk_total = format_size(disk_info['total'])
        col3.metric("Disk Usage", f"{disk_percent:.1f}%", delta=None, help=f"Used: {disk_used} / Total: {disk_total}")
        
        # Network stats
        net_info = ss.get_network_info()
        net_speed = format_size(net_info['bytes_sent'] + net_info['bytes_recv'])
        col4.metric("Network Traffic", f"{net_speed}/s", delta=None)
        
        # Update top processes
        processes = pu.get_processes_info(sort_by="cpu", limit=10)
        processes_placeholder.dataframe(processes, use_container_width=True)
        
        # Update memory details
        memory_df = pd.DataFrame({
            "Type": ["Total", "Available", "Used", "Free", "Swap Used", "Swap Free"],
            "Value": [
                format_size(mem_info['total']),
                format_size(mem_info['available']),
                format_size(mem_info['used']),
                format_size(mem_info['free']),
                format_size(mem_info['swap_used']),
                format_size(mem_info['swap_free'])
            ]
        })
        memory_placeholder.table(memory_df)
        
        # Wait before refreshing
        time.sleep(refresh_rate)
        st.rerun()

elif view == "Processes":
    # Process listing with search and sort capabilities
    st.subheader("Running Processes")
    
    # Sort mapping
    sort_mapping = {
        "CPU Usage (%)": "cpu",
        "Memory Usage (%)": "memory",
        "PID": "pid",
        "Name": "name"
    }
    
    # Get process data
    processes = pu.get_processes_info(
        sort_by=sort_mapping[sort_option],
        limit=show_count,
        filter_name=filter_option
    )
    
    # Display process table
    st.dataframe(processes, use_container_width=True)
    
    # Process actions (inline)
    st.subheader("Process Actions")
    cols = st.columns([2, 1, 1])
    with cols[0]:
        pid_input = st.number_input("Process ID (PID):", min_value=0, step=1)
    with cols[1]:
        if st.button("Terminate Process", key="term_proc"):
            if pid_input > 0:
                success = pu.kill_process(pid_input)
                if success:
                    st.success(f"Process with PID {pid_input} terminated successfully!")
                else:
                    st.error(f"Failed to terminate process with PID {pid_input}")
    with cols[2]:
        if st.button("Refresh Processes"):
            pass  # The page will refresh automatically
    
    # Add auto-refresh
    time.sleep(refresh_rate)
    st.rerun()

elif view == "System Information":
    st.header("System Information")
    
    # Get system info
    cpu_info = ss.get_detailed_cpu_info()
    mem_info = ss.get_memory_info()
    sys_info = ss.get_system_info()
    
    # Format sizes
    def format_size(bytes):
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if bytes < 1024:
                return f"{bytes:.2f} {unit}"
            bytes /= 1024
        return f"{bytes:.2f} PB"
    
    # Create tabs for different information categories
    tabs = st.tabs(["CPU", "Memory", "System", "Boot Time"])
    
    with tabs[0]:
        st.subheader("CPU Information")
        cpu_usage = ss.get_cpu_usage()
        st.progress(cpu_usage/100)
        st.write(f"Current CPU Usage: {cpu_usage:.1f}%")
        
        # Create CPU info table
        cpu_df = pd.DataFrame({
            "Property": list(cpu_info.keys()),
            "Value": list(cpu_info.values())
        })
        st.table(cpu_df)
        
        # CPU usage per core
        st.subheader("CPU Usage Per Core")
        cpu_count = psutil.cpu_count(logical=True)
        cpu_percent_per_core = psutil.cpu_percent(percpu=True)
        
        for i, percent in enumerate(cpu_percent_per_core):
            st.write(f"Core {i}: {percent}%")
            st.progress(percent/100)
    
    with tabs[1]:
        st.subheader("Memory Information")
        
        # Memory usage diagram
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("RAM Usage")
            st.progress(mem_info['percent']/100)
            st.write(f"{mem_info['percent']:.1f}% Used")
            
            memory_df = pd.DataFrame({
                "Type": ["Total", "Available", "Used", "Free"],
                "Value": [
                    format_size(mem_info['total']),
                    format_size(mem_info['available']),
                    format_size(mem_info['used']),
                    format_size(mem_info['free'])
                ]
            })
            st.table(memory_df)
        
        with col2:
            st.write("Swap Usage")
            swap_percent = mem_info['swap_percent']
            st.progress(swap_percent/100 if swap_percent is not None else 0)
            st.write(f"{swap_percent:.1f}% Used" if swap_percent is not None else "No swap configured")
            
            swap_df = pd.DataFrame({
                "Type": ["Total Swap", "Used Swap", "Free Swap"],
                "Value": [
                    format_size(mem_info['swap_total']),
                    format_size(mem_info['swap_used']),
                    format_size(mem_info['swap_free'])
                ]
            })
            st.table(swap_df)
    
    with tabs[2]:
        st.subheader("System Information")
        
        system_df = pd.DataFrame({
            "Property": list(sys_info.keys()),
            "Value": list(sys_info.values())
        })
        st.table(system_df)
        
        # Display logged in users
        st.subheader("Logged In Users")
        users = psutil.users()
        if users:
            users_data = []
            for user in users:
                users_data.append({
                    "Username": user.name,
                    "Terminal": user.terminal or "N/A",
                    "Host": user.host or "localhost",
                    "Started": datetime.fromtimestamp(user.started).strftime("%Y-%m-%d %H:%M:%S")
                })
            st.table(pd.DataFrame(users_data))
        else:
            st.write("No users currently logged in")
    
    with tabs[3]:
        st.subheader("Boot Time")
        boot_time = datetime.fromtimestamp(psutil.boot_time())
        st.write(f"System booted at: {boot_time.strftime('%Y-%m-%d %H:%M:%S')}")
        
        uptime_seconds = time.time() - psutil.boot_time()
        days = int(uptime_seconds // (24 * 3600))
        hours = int((uptime_seconds % (24 * 3600)) // 3600)
        minutes = int((uptime_seconds % 3600) // 60)
        seconds = int(uptime_seconds % 60)
        
        st.write(f"System uptime: {days} days, {hours} hours, {minutes} minutes, {seconds} seconds")
    
    # Auto-refresh
    time.sleep(refresh_rate)
    st.rerun()

elif view == "Disk Usage":
    st.header("Disk Usage")
    
    # Get disk partitions
    partitions = psutil.disk_partitions()
    
    # Format size
    def format_size(bytes):
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if bytes < 1024:
                return f"{bytes:.2f} {unit}"
            bytes /= 1024
        return f"{bytes:.2f} PB"
    
    # Display disk usage for each partition
    for partition in partitions:
        try:
            usage = psutil.disk_usage(partition.mountpoint)
            
            st.subheader(f"Partition: {partition.mountpoint}")
            st.write(f"Device: {partition.device}")
            st.write(f"File System: {partition.fstype}")
            
            # Progress bar for disk usage
            st.progress(usage.percent/100)
            st.write(f"Usage: {usage.percent}%")
            
            # Create a table with disk details
            disk_data = pd.DataFrame({
                "Property": ["Total Size", "Used Space", "Free Space"],
                "Value": [
                    format_size(usage.total),
                    format_size(usage.used),
                    format_size(usage.free)
                ]
            })
            st.table(disk_data)
        except PermissionError:
            st.write(f"Cannot access {partition.mountpoint} (Permission denied)")
        except Exception as e:
            st.write(f"Error accessing {partition.mountpoint}: {str(e)}")
    
    # Display disk I/O statistics
    st.subheader("Disk I/O Statistics")
    
    io_stats = ss.get_disk_io_stats()
    
    if io_stats:
        # Create main IO stats dataframe
        io_df = pd.DataFrame({
            "Device": list(io_stats.keys()),
            "Read Count": [stats['read_count'] for stats in io_stats.values()],
            "Write Count": [stats['write_count'] for stats in io_stats.values()],
            "Read Bytes": [format_size(stats['read_bytes']) for stats in io_stats.values()],
            "Write Bytes": [format_size(stats['write_bytes']) for stats in io_stats.values()]
        })
        st.dataframe(io_df, use_container_width=True)
    else:
        st.write("No disk I/O statistics available")
    
    # Auto-refresh
    time.sleep(refresh_rate)
    st.rerun()

elif view == "Network Statistics":
    st.header("Network Statistics")
    
    # Get network information
    net_io = ss.get_network_info()
    net_connections = ss.get_network_connections()
    net_interfaces = ss.get_network_interfaces()
    
    # Format size
    def format_size(bytes, rate=False):
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if bytes < 1024:
                return f"{bytes:.2f} {unit}" + ("/s" if rate else "")
            bytes /= 1024
        return f"{bytes:.2f} PB" + ("/s" if rate else "")
    
    # Create tabs for different network information
    tabs = st.tabs(["Overview", "Connections", "Interfaces"])
    
    with tabs[0]:
        st.subheader("Network I/O")
        
        # Create traffic metrics
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Bytes Sent", format_size(net_io["bytes_sent"]))
            st.metric("Packets Sent", f"{net_io['packets_sent']:,}")
        with col2:
            st.metric("Bytes Received", format_size(net_io["bytes_recv"]))
            st.metric("Packets Received", f"{net_io['packets_recv']:,}")
        
        # Network traffic over time
        st.subheader("Network Traffic Rate")
        
        # Store previous values for rate calculation
        if 'prev_net_io' not in st.session_state:
            st.session_state.prev_net_io = net_io
            st.session_state.prev_time = time.time()
        
        # Calculate rates
        time_diff = time.time() - st.session_state.prev_time
        sent_rate = (net_io['bytes_sent'] - st.session_state.prev_net_io['bytes_sent']) / time_diff
        recv_rate = (net_io['bytes_recv'] - st.session_state.prev_net_io['bytes_recv']) / time_diff
        
        # Update previous values
        st.session_state.prev_net_io = net_io
        st.session_state.prev_time = time.time()
        
        # Display current rates
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Upload Rate", format_size(sent_rate, rate=True))
        with col2:
            st.metric("Download Rate", format_size(recv_rate, rate=True))
    
    with tabs[1]:
        st.subheader("Network Connections")
        
        # Filter options
        filter_options = ["All", "ESTABLISHED", "LISTEN", "CLOSE_WAIT", "TIME_WAIT", "SYN_SENT"]
        selected_status = st.selectbox("Filter by status:", filter_options)
        
        # Apply filter
        if selected_status != "All":
            filtered_connections = [conn for conn in net_connections if conn['status'] == selected_status]
        else:
            filtered_connections = net_connections
        
        # Convert to dataframe for display
        if filtered_connections:
            connections_df = pd.DataFrame(filtered_connections)
            st.dataframe(connections_df, use_container_width=True)
        else:
            st.write("No connections matching the selected filter")
    
    with tabs[2]:
        st.subheader("Network Interfaces")
        
        for name, data in net_interfaces.items():
            st.write(f"### {name}")
            
            # Create a table for interface details
            interface_data = []
            for key, value in data.items():
                if key in ['addresses']:
                    continue  # Handle addresses separately
                interface_data.append({"Property": key, "Value": str(value)})
            
            st.table(pd.DataFrame(interface_data))
            
            # Display addresses if available
            if 'addresses' in data and data['addresses']:
                st.write("#### Addresses")
                addresses_data = []
                for addr_family, addresses in data['addresses'].items():
                    for addr in addresses:
                        addr_info = {"Family": addr_family}
                        addr_info.update(addr)
                        addresses_data.append(addr_info)
                
                if addresses_data:
                    st.table(pd.DataFrame(addresses_data))
    
    # Auto-refresh
    time.sleep(refresh_rate)
    st.rerun()  # Changed from st.experimental_rerun()

# Add footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center;'>System Task Manager | Created with Streamlit</div>",
    unsafe_allow_html=True
)