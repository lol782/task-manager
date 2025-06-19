---

# 🖥️ System Task Manager

A powerful and interactive task manager built with **Streamlit**, offering real-time system monitoring, process management, and hardware insights in a sleek web-based UI.

![System Task Manager Screenshot](https://via.placeholder.com/800x450?text=System+Task+Manager+Screenshot)

---

## 🚀 Features

### 🔧 Real-time System Monitoring

* **CPU usage** – Total and per-core usage.
* **Memory** – RAM and swap utilization.
* **Network** – Traffic, interfaces, and active connections.

### 📋 Process Management

* View all running processes.
* Sort, search, and filter.
* Terminate selected processes.
* cutomised process sheduling algorithms,vizulaise also

### 🖥️ System Information

* Hardware specifications.
* OS details and version.
* Network interface information.
* Current user sessions and logins.

### 🧩 Interactive UI

* Tab-based navigation.
* Customizable refresh rate.
* Clean and responsive layout.

---

## 🛠️ Installation

### 🔍 Prerequisites

* Python 3.7+
* `pip` package manager

### ⚙️ Setup

1. **Clone the repository**:

   ```bash
   git clone https://github.com/lol782/task-manager-streamlit.git
   cd task-manager
   ```

2. **Create a virtual environment** (optional but recommended):

   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

---

## ▶️ Usage

1. **Run the application**:

   ```bash
   streamlit run main.py
   ```

2. **Open in browser**:

   ```
   http://localhost:8501
   ```

---

## 🧭 Application Views

| View              | Description                                      |
| ----------------- | ------------------------------------------------ |
| **Dashboard**     | Overview of system performance and top processes |
| **Processes**     | View, filter, and manage running processes with  |
|                     customise process sheduling algorithm            |
| **System Info**   | Detailed OS and hardware information             |
| **Network Stats** | Live interface traffic and network connections   |

---

## 🔐 Permissions

Some features require elevated privileges:

* **Linux/macOS**: Use `sudo` for full access to all processes.
* **Windows**: Run as **Administrator** for complete process control.

---

## 🎨 Customization

Modify the UI appearance via:

```
assets/style.css
```

---

## 📦 Dependencies

* [Streamlit](https://streamlit.io/) – UI framework
* [pandas](https://pandas.pydata.org/) – Data wrangling
* [matplotlib](https://matplotlib.org/) – Visualization (optional)
* [plotly](https://plotly.com/python/) – Interactive charts (optional)

---

## 📁 Project Structure

```
task_manager_sim/
│
├── main.py                        # Streamlit app entry point
├── requirements.txt
│
├── core/
│   ├── __init__.py
│   ├── process_manager.py         # CRUD for processes
│   ├── scheduler.py               # Scheduling algorithms
│   ├── resource_analyzer.py       # CPU/Memory usage calculations
│   └── network.py                 # Network usage simulation or stats
│
├── data/
│   └── dummy_processes.json       # Predefined dummy process set
│
├── ui/
│   ├── __init__.py
│   ├── dashboard.py               # Gantt chart, memory, CPU, network
│   ├── process_table.py           # Process list
│   └── control_panel.py           # Add/start/stop process
│
└── utils/
    ├── __init__.py
    ├── visualizer.py              # Gantt, memory, CPU, network graphs
    └── helpers.py                 # ID generator, time, format utils

```

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

## 🤝 Contributing

Contributions, bug reports, and feature requests are welcome.
Feel free to fork the repo and submit a Pull Request!

---

Let me know if you'd like a version with badges (e.g., Python version, license, etc.) or markdown enhancements like collapsible sections.
