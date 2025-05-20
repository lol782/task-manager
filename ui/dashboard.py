# ui/dashboard.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import time

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import time

def show_dashboard(resource_analyzer, network):
    st.header("System Dashboard")
    
    # Create three columns for the metrics
    col1, col2, col3 = st.columns(3)
    
    # Get the latest values
    cpu = resource_analyzer.get_cpu_usage()[-1] if resource_analyzer.get_cpu_usage() else 0
    memory = resource_analyzer.get_memory_usage()[-1] if resource_analyzer.get_memory_usage() else 0
    network_usage = network.get_network_usage()[-1] if network.get_network_usage() else 0
    
    # Display metrics
    col1.metric("CPU Usage", f"{cpu}%", f"{cpu-50:.1f}%" if cpu > 50 else f"{cpu-50:.1f}%")
    col2.metric("Memory Usage", f"{memory}%", f"{memory-60:.1f}%" if memory > 60 else f"{memory-60:.1f}%")
    col3.metric("Network", f"{network_usage} KB/s", f"{network_usage-30:.1f}" if network_usage > 30 else f"{network_usage-30:.1f}")
    
    # Add titles for the graphs
    st.subheader("CPU Usage Over Time")
    cpu_data = resource_analyzer.get_cpu_usage()
    if cpu_data:
        st.line_chart(pd.DataFrame({'CPU Usage (%)': cpu_data}))
    
    st.subheader("Memory Usage Over Time")
    memory_data = resource_analyzer.get_memory_usage()
    if memory_data:
        st.line_chart(pd.DataFrame({'Memory Usage (%)': memory_data}))
    
    st.subheader("Network Usage Over Time")
    network_data = network.get_network_usage()
    if network_data:
        st.line_chart(pd.DataFrame({'Network (KB/s)': network_data}))

