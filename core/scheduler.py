# core/scheduler.py
import time

class Scheduler:
    def __init__(self):
        self.algorithm = "Round Robin"
        self.quantum = 2  # Time quantum for Round Robin (in seconds)
        
    def set_algorithm(self, algorithm):
        self.algorithm = algorithm
        
    def schedule(self, processes):
        if not processes:
            return []
            
        # Make a copy to avoid modifying the original list
        scheduled_processes = processes.copy()
        
        if self.algorithm == "Round Robin":
            return self._round_robin(scheduled_processes)
        elif self.algorithm == "Priority":
            return self._priority_scheduling(scheduled_processes)
        elif self.algorithm == "First Come First Served":
            return self._fcfs(scheduled_processes)
        else:
            return scheduled_processes
    
    def _round_robin(self, processes):
        # Simple round robin implementation - just rotate the list
        # In a real implementation, we would manage time slices
        if processes:
            # Move first process to the end
            first = processes.pop(0)
            processes.append(first)
        return processes
    
    def _priority_scheduling(self, processes):
        # Sort processes by priority (higher priority value = higher priority)
        # Only running and waiting processes are considered for scheduling
        active_processes = [p for p in processes if p.status in ["Running", "Waiting"]]
        inactive_processes = [p for p in processes if p.status not in ["Running", "Waiting"]]
        
        # Sort by priority (descending)
        sorted_active = sorted(active_processes, key=lambda p: p.priority, reverse=True)
        
        # Update status - highest priority process gets to run if it's waiting
        if sorted_active and sorted_active[0].status == "Waiting":
            sorted_active[0].status = "Running"
        
        # Combine sorted active processes with inactive ones
        return sorted_active + inactive_processes
    
    def _fcfs(self, processes):
        # First Come First Served - sort by start time
        # Only running and waiting processes are considered for scheduling
        active_processes = [p for p in processes if p.status in ["Running", "Waiting"]]
        inactive_processes = [p for p in processes if p.status not in ["Running", "Waiting"]]
        
        # Sort by start time (ascending)
        sorted_active = sorted(active_processes, key=lambda p: p.start_time)
        
        # Update status - earliest process gets to run if it's waiting
        if sorted_active and sorted_active[0].status == "Waiting":
            sorted_active[0].status = "Running"
        
        # Combine sorted active processes with inactive ones
        return sorted_active + inactive_processes
