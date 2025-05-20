# core/process_manager.py
# core/process_manager.py (additional class)
import time
import json
import os
class ProcessManager:
    def __init__(self):
        self.processes = []

    def add_process(self, process):
        self.processes.append(process)
        
    def remove_process(self, pid):
        self.processes = [p for p in self.processes if p.pid != pid]
        
    def get_process(self, pid):
        for process in self.processes:
            if process.pid == pid:
                return process
        return None
        
    def get_processes(self):
        return self.processes
        
    def update_process_status(self, pid, status):
        process = self.get_process(pid)
        if process:
            process.status = status
    # Add to core/process_manager.py
def load_dummy_processes(self):
    try:
        if os.path.exists('data/dummy_processes.json'):
            with open('data/dummy_processes.json', 'r') as file:
                data = json.load(file)
                for proc_data in data['processes']:
                    process = Process(
                        proc_data['pid'],
                        proc_data['name'],
                        proc_data['status'],
                        proc_data['cpu_usage'],
                        proc_data['memory_usage'],
                        proc_data['priority']
                    )
                    self.add_process(process)
            return True
        return False
    except Exception as e:
        print(f"Error loading dummy processes: {e}")
        return False
# core/process_manager.py (update to Process class)

class Process:
    def __init__(self, pid, name, status, cpu_usage=0, memory_usage=0, priority=5, start_time=None):
        self.pid = pid
        self.name = name
        self.status = status
        self.cpu_usage = cpu_usage
        self.memory_usage = memory_usage
        self.priority = priority
        self.start_time = start_time if start_time is not None else time.time()
