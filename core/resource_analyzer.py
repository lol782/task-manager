# core/resource_analyzer.py
class ResourceAnalyzer:
    def __init__(self):
        self.cpu_history = []
        self.memory_history = []
        self.process_cpu_usage = {}  # Track CPU usage per process
        
    def update(self, processes, scheduler_algorithm):
        # Calculate CPU usage based on running processes and scheduling algorithm
        total_cpu = 0
        active_processes = [p for p in processes if p.status == "Running"]
        
        # Reset process CPU allocation
        for p in processes:
            if p.pid not in self.process_cpu_usage:
                self.process_cpu_usage[p.pid] = 0
        
        # Allocate CPU based on scheduling algorithm
        if active_processes:
            if scheduler_algorithm == "Round Robin":
                # Distribute CPU evenly among running processes
                cpu_per_process = 100 / len(active_processes)
                for p in active_processes:
                    p.current_cpu = min(p.cpu_usage, cpu_per_process)
                    total_cpu += p.current_cpu
                    self.process_cpu_usage[p.pid] = p.current_cpu
                    
            elif scheduler_algorithm == "Priority":
                # Allocate CPU based on priority
                total_priority = sum(p.priority for p in active_processes)
                for p in active_processes:
                    priority_share = p.priority / total_priority if total_priority > 0 else 0
                    p.current_cpu = min(p.cpu_usage, 100 * priority_share)
                    total_cpu += p.current_cpu
                    self.process_cpu_usage[p.pid] = p.current_cpu
                    
            elif scheduler_algorithm == "First Come First Served":
                # Give all CPU to the first process in the queue
                if active_processes:
                    first_process = min(active_processes, key=lambda p: p.start_time)
                    first_process.current_cpu = first_process.cpu_usage
                    total_cpu = first_process.current_cpu
                    self.process_cpu_usage[first_process.pid] = first_process.current_cpu
        
        # Calculate memory usage (sum of all process memory)
        total_memory = sum(p.memory_usage for p in active_processes)
        
        self.cpu_history.append(total_cpu)
        self.memory_history.append(total_memory)
        
        # Keep only the last 20 data points
        if len(self.cpu_history) > 20:
            self.cpu_history.pop(0)
        if len(self.memory_history) > 20:
            self.memory_history.pop(0)
    
    def get_cpu_usage(self):
        return self.cpu_history
        
    def get_memory_usage(self):
        return self.memory_history
        
    def get_process_cpu_usage(self):
        return self.process_cpu_usage
