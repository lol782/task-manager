System Task Manager
A comprehensive task manager built with Streamlit that provides detailed system monitoring and process management capabilities.

Show Image

Features
Real-time system monitoring:
CPU usage (overall and per-core)
Memory usage (RAM and swap)
Disk usage and I/O statistics
Network traffic and connections
Process management:
View all running processes
Sort and filter processes
Terminate processes
Detailed process information
System information:
Detailed hardware specifications
Operating system details
Network interfaces
Users and login information
Interactive UI:
Customizable refresh rate
Different views for specific monitoring needs
Easy navigation through tabs
Responsive design
Installation
Prerequisites
Python 3.7 or higher
pip (Python package installer)
Setup
Clone this repository:
bash
git clone https://github.com/yourusername/task-manager-streamlit.git
cd task-manager-streamlit
Create a virtual environment (optional but recommended):
bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
Install dependencies:
bash
pip install -r requirements.txt
Usage
Start the Streamlit application:
bash
streamlit run app.py
Open your browser and navigate to:
http://localhost:8501
Views
Dashboard: Overview of system resources and top processes
Processes: Complete list of running processes with management options
System Information: Detailed information about your hardware and OS
Disk Usage: Storage utilization and I/O statistics
Network Statistics: Network interfaces, connections, and traffic
Note on Permissions
Some system monitoring features require elevated permissions:

Linux/macOS: You may need to run the application with sudo for full functionality
Windows: Run as Administrator for complete access to all processes
Customization
You can customize the appearance by modifying the assets/style.css file.

Dependencies
Streamlit - Web application framework
psutil - Process and system utilities
pandas - Data manipulation and analysis
matplotlib - Data visualization (optional)
plotly - Interactive visualizations (optional)
Project Structure
task_manager_streamlit/
├── app.py                        # Main Streamlit app
├── process_utils.py              # Utility functions for process handling
├── system_stats.py               # Functions for CPU, RAM, Disk, Network info
├── requirements.txt              # Python dependencies
├── assets/
│   └── style.css                 # Custom CSS styling
└── README.md                     # Project overview
License
This project is licensed under the MIT License - see the LICENSE file for details.

Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

