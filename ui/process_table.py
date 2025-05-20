# ui/process_table.py
import streamlit as st
import pandas as pd

def show_process_table(process_manager, scheduler=None):
    st.header("Process List")
    
    processes = process_manager.get_processes()
    
    if not processes or len(processes) == 0:
        st.warning("No processes available. Add processes from the Control Panel.")
        return
    
    # Debug information
    st.write(f"Number of processes loaded: {len(processes)}")
    
    # Create a dataframe for display
    data = []
    for p in processes:
        data.append({
            "PID": p.pid,
            "Name": p.name,
            "Status": p.status,
            "CPU Usage (%)": p.cpu_usage,
            "Memory Usage (%)": p.memory_usage,
            "Priority": p.priority
        })
    
    # Display as a dataframe
    st.dataframe(data, use_container_width=True)
    
    # Process actions section
    st.subheader("Process Actions")
    
    # Create columns for different actions
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if processes:
            running_processes = [p for p in processes if p.status == "Running"]
            if running_processes:
                pid_to_stop = st.selectbox(
                    "Select process to stop:", 
                    [f"{p.pid} - {p.name}" for p in running_processes],
                    key="stop_process"
                )
                if st.button("Stop Process"):
                    if pid_to_stop:
                        pid = int(pid_to_stop.split(" - ")[0])
                        process_manager.update_process_status(pid, "Stopped")
                        st.success(f"Process {pid_to_stop} stopped.")
                        st.rerun()
            else:
                st.info("No running processes to stop")
    
    with col2:
        if processes:
            stopped_processes = [p for p in processes if p.status != "Running"]
            if stopped_processes:
                pid_to_start = st.selectbox(
                    "Select process to start:", 
                    [f"{p.pid} - {p.name}" for p in stopped_processes],
                    key="start_process"
                )
                if st.button("Start Process"):
                    if pid_to_start:
                        pid = int(pid_to_start.split(" - ")[0])
                        process_manager.update_process_status(pid, "Running")
                        st.success(f"Process {pid_to_start} started.")
                        st.rerun()
            else:
                st.info("No stopped processes to start")
                
    with col3:
        if processes:
            pid_to_kill = st.selectbox(
                "Select process to kill:", 
                [f"{p.pid} - {p.name}" for p in processes],
                key="kill_process"
            )
            if st.button("Kill Process"):
                if pid_to_kill:
                    pid = int(pid_to_kill.split(" - ")[0])
                    process_manager.remove_process(pid)
                    st.success(f"Process {pid_to_kill} killed.")
                    st.rerun()
