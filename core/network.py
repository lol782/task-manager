# core/network.py
import random

class Network:
    def __init__(self):
        self.network_history = []
        
    def update(self):
        # Generate dummy network usage data
        network = random.randint(0, 100)
        self.network_history.append(network)
        
        # Keep only the last 20 data points
        if len(self.network_history) > 20:
            self.network_history.pop(0)
    
    def get_network_usage(self):
        return self.network_history
