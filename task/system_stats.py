import psutil
import platform
import socket
import datetime
import time
import os

def get_cpu_usage(interval=0.1, delay=0.1):
    """
    Get CPU usage percentage
    
    Parameters:
    - interval: Time interval for CPU measurement
    - delay: Optional delay before measurement
    
    Returns:
    - CPU usage percentage as a float
    """
    if delay > 0:
        time.sleep(delay)
    return psutil.cpu_percent(interval=interval)

def get_detailed_cpu_info():
    """
    Get detailed CPU information
    
    Returns:
    - Dictionary with CPU details
    """
    cpu_info = {
        "Physical Cores": psutil.cpu_count(logical=False),
        "Total Cores": psutil.cpu_count(logical=True),
        "Max Frequency": f"{psutil.cpu_freq().max:.2f}MHz" if psutil.cpu_freq() and psutil.cpu_freq().max else "N/A",
        "Current Frequency": f"{psutil.cpu_freq().current:.2f}MHz" if psutil.cpu_freq() and psutil.cpu_freq().current else "N/A",
        "CPU Usage Per Core": psutil.cpu_percent(percpu=True),
        "Total CPU Usage": psutil.cpu_percent(),
    }
    
    # Add architecture and processor model
    cpu_info["Architecture"] = platform.architecture()[0]
    cpu_info["Processor"] = platform.processor()
    
    return cpu_info

def get_memory_info():
    """
    Get system memory information
    
    Returns:
    - Dictionary with memory usage details
    """
    virtual_mem = psutil.virtual_memory()
    swap = psutil.swap_memory()
    
    return {
        "total": virtual_mem.total,
        "available": virtual_mem.available,
        "used": virtual_mem.used,
        "free": virtual_mem.free,
        "percent": virtual_mem.percent,
        "swap_total": swap.total,
        "swap_used": swap.used,
        "swap_free": swap.free,
        "swap_percent": swap.percent
    }

def get_disk_info(path='/'):
    """
    Get disk usage information
    
    Parameters:
    - path: Path to check disk usage, defaults to root directory
    
    Returns:
    - Dictionary with disk usage details
    """
    disk = psutil.disk_usage(path)
    
    return {
        "total": disk.total,
        "used": disk.used,
        "free": disk.free,
        "percent": disk.percent
    }

def get_disk_io_stats():
    """
    Get disk I/O statistics
    
    Returns:
    - Dictionary with disk I/O details per disk
    """
    io_stats = {}
    disk_io = psutil.disk_io_counters(perdisk=True)
    
    for disk_name, disk_stats in disk_io.items():
        io_stats[disk_name] = {
            "read_count": disk_stats.read_count,
            "write_count": disk_stats.write_count,
            "read_bytes": disk_stats.read_bytes,
            "write_bytes": disk_stats.write_bytes,
            "read_time": disk_stats.read_time,
            "write_time": disk_stats.write_time
        }
    
    return io_stats

def get_network_info():
    """
    Get network I/O statistics
    
    Returns:
    - Dictionary with network I/O details
    """
    net_io = psutil.net_io_counters()
    
    return {
        "bytes_sent": net_io.bytes_sent,
        "bytes_recv": net_io.bytes_recv,
        "packets_sent": net_io.packets_sent,
        "packets_recv": net_io.packets_recv,
        "errin": net_io.errin,
        "errout": net_io.errout,
        "dropin": net_io.dropin,
        "dropout": net_io.dropout
    }

def get_network_connections():
    """
    Get current network connections
    
    Returns:
    - List of dictionaries with connection details
    """
    connections = []
    
    for conn in psutil.net_connections(kind='inet'):
        connection = {
            'fd': conn.fd,
            'family': str(conn.family),
            'type': str(conn.type),
            'laddr': f"{conn.laddr.ip}:{conn.laddr.port}" if conn.laddr else "N/A",
            'raddr': f"{conn.raddr.ip}:{conn.raddr.port}" if conn.raddr else "N/A",
            'status': conn.status,
            'pid': conn.pid if conn.pid else "N/A"
        }
        connections.append(connection)
    
    return connections

def get_network_interfaces():
    """
    Get network interfaces information
    
    Returns:
    - Dictionary with interface details
    """
    interfaces = {}
    addrs = psutil.net_if_addrs()
    stats = psutil.net_if_stats()
    
    for interface_name, addr_list in addrs.items():
        # Initialize interface if not present
        if interface_name not in interfaces:
            interfaces[interface_name] = {
                'addresses': {}
            }
        
        # Add interface stats if available
        if interface_name in stats:
            stat = stats[interface_name]
            interfaces[interface_name].update({
                'isup': stat.isup,
                'duplex': str(stat.duplex),
                'speed': stat.speed,
                'mtu': stat.mtu
            })
        
        # Process addresses
        for addr in addr_list:
            family_name = str(addr.family).replace('AddressFamily.', '')
            
            if family_name not in interfaces[interface_name]['addresses']:
                interfaces[interface_name]['addresses'][family_name] = []
            
            addr_info = {
                'address': addr.address,
                'netmask': addr.netmask,
                'broadcast': addr.broadcast,
                'ptp': addr.ptp
            }
            
            # Filter out None values
            addr_info = {k: v for k, v in addr_info.items() if v is not None}
            
            interfaces[interface_name]['addresses'][family_name].append(addr_info)
    
    return interfaces

def get_system_info():
    """
    Get general system information
    
    Returns:
    - Dictionary with system details
    """
    # Get system information
    uname = platform.uname()
    
    return {
        "System": uname.system,
        "Node Name": uname.node,
        "Release": uname.release,
        "Version": uname.version,
        "Machine": uname.machine,
        "Processor": uname.processor,
        "Python Version": platform.python_version(),
        "Hostname": socket.gethostname(),
        "IP Address": socket.gethostbyname(socket.gethostname()),
        "Boot Time": datetime.datetime.fromtimestamp(psutil.boot_time()).strftime("%Y-%m-%d %H:%M:%S")
    }

def get_battery_info():
    """
    Get battery information if available
    
    Returns:
    - Dictionary with battery details or None if not available
    """
    battery = psutil.sensors_battery()
    
    if battery:
        return {
            "percent": battery.percent,
            "power_plugged": battery.power_plugged,
            "secsleft": battery.secsleft if battery.secsleft != psutil.POWER_TIME_UNLIMITED else "Unlimited",
            "status": "Charging" if battery.power_plugged else "Discharging"
        }
    else:
        return None

def get_users_info():
    """
    Get information about logged in users
    
    Returns:
    - List of dictionaries with user details
    """
    users_list = []
    
    for user in psutil.users():
        user_info = {
            "name": user.name,
            "terminal": user.terminal,
            "host": user.host,
            "started": datetime.datetime.fromtimestamp(user.started).strftime("%Y-%m-%d %H:%M:%S"),
            "pid": user.pid if hasattr(user, 'pid') else None
        }
        users_list.append(user_info)
    
    return users_list