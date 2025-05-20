# ui/control_panel.py
import streamlit as st
import random
import time
from utils.helpers import generate_id

def show_control_panel(process_manager, scheduler):
    st.header("Control Panel")
    
    # Process creation form
    with st.form("new_process_form"):
        st.subheader("Create New Process")
        name = st.text_input("Process Name", value=f"Process-{random.randint(100, 999)}")
        
        col1, col2 = st.columns(2)
        with col1:
            status = st.selectbox("Initial Status", ["Running", "Waiting", "Stopped"])
        with col2:
            priority = st.slider("Priority", 1, 10, 5)
        
        # Generate random resource usage for the dummy process
        cpu_usage = random.randint(1, 50)
        memory_usage = random.randint(10, 70)
        
        submit = st.form_submit_button("Add Process")
        
        if submit:
            pid = generate_id()
            # Create a new process with current time as start_time
            new_process = Process(pid, name, status, cpu_usage, memory_usage, priority, time.time())
            process_manager.add_process(new_process)
            st.success(f"Process {name} (PID: {pid}) added successfully!")
    
    # Scheduler settings
    st.subheader("Scheduler Settings")
    algorithm = st.selectbox("Scheduling Algorithm", 
                           ["Round Robin", "Priority", "First Come First Served"])
    
    if algorithm == "Round Robin":
        quantum = st.slider("Time Quantum (seconds)", 1, 10, 2)
        scheduler.quantum = quantum
    
    if st.button("Apply Scheduling Algorithm"):
        scheduler.set_algorithm(algorithm)
        st.success(f"Scheduling algorithm changed to {algorithm}")
    
    # Global actions
    st.subheader("Global Actions")
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Start All Processes"):
            processes = process_manager.get_processes()
            for process in processes:
                process.status = "Running"
            st.success("All processes started")
    
    with col2:
        if st.button("Stop All Processes"):
            processes = process_manager.get_processes()
            for process in processes:
                process.status = "Stopped"
            st.success("All processes stopped")

# Make sure to import Process class
from core.process_manager import Process
