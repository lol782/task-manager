import psutil
import pandas as pd
import os
import datetime

def get_processes_info(sort_by='cpu', limit=None, filter_name=None):
    """
    Get information about running processes
    
    Parameters:
    - sort_by: Sort criteria ('cpu', 'memory', 'pid', 'name')
    - limit: Number of processes to return
    - filter_name: Filter processes by name (case-insensitive substring)
    
    Returns:
    - DataFrame with process information
    """
    processes = []
    
    # Iterate through all processes
    for proc in psutil.process_iter(['pid', 'name', 'username', 'status', 'create_time']):
        try:
            # Get process info as a dictionary
            proc_info = proc.info
            
            # Get CPU and memory usage
            with proc.oneshot():
                # Get CPU usage (might be None for some processes)
                try:
                    cpu_percent = proc.cpu_percent(interval=0.1)
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    cpu_percent = 0.0
                
                # Get memory info (might be None for some processes)
                try:
                    mem_info = proc.memory_info()
                    mem_percent = proc.memory_percent()
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    mem_info = None
                    mem_percent = 0.0
                
                # Get command line (might be None for some processes)
                try:
                    cmdline = " ".join(proc.cmdline())
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    cmdline = "N/A"
                
                # Get executable path (might be None for some processes)
                try:
                    exe = proc.exe()
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    exe = "N/A"
            
            # Create a process information dictionary
            process_dict = {
                'pid': proc_info['pid'],
                'name': proc_info['name'],
                'username': proc_info['username'] or "N/A",
                'status': proc_info['status'],
                'cpu_percent': cpu_percent,
                'memory_percent': mem_percent,
                'create_time': datetime.datetime.fromtimestamp(proc_info['create_time']).strftime("%Y-%m-%d %H:%M:%S") if proc_info['create_time'] else "N/A",
                'command': cmdline,
                'executable': exe
            }
            
            # Filter by name if specified
            if filter_name and filter_name.lower() not in process_dict['name'].lower():
                continue
            
            processes.append(process_dict)
        
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    
    # Sort processes
    sort_mapping = {
        'cpu': 'cpu_percent',
        'memory': 'memory_percent',
        'pid': 'pid',
        'name': 'name'
    }
    
    sort_key = sort_mapping.get(sort_by, 'cpu_percent')
    
    # Apply sorting
    if sort_key in ['name']:
        processes.sort(key=lambda x: str(x.get(sort_key, '')).lower())
    else:
        processes.sort(key=lambda x: x.get(sort_key, 0), reverse=True)
    
    # Apply limit
    if limit:
        processes = processes[:limit]
    
    # Convert to DataFrame
    df = pd.DataFrame(processes)
    
    # Format percentage columns
    if 'cpu_percent' in df.columns:
        df['cpu_percent'] = df['cpu_percent'].round(1)
    if 'memory_percent' in df.columns:
        df['memory_percent'] = df['memory_percent'].round(1)
    
    return df

def kill_process(pid):
    """
    Kill a process by its PID
    
    Parameters:
    - pid: Process ID to kill
    
    Returns:
    - True if successful, False otherwise
    """
    try:
        process = psutil.Process(pid)
        process.terminate()  # Try to terminate it gracefully first
        
        # Wait for process to terminate
        gone, alive = psutil.wait_procs([process], timeout=3)
        
        # If still alive, kill it
        if process in alive:
            process.kill()
        
        return True
    except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess) as e:
        print(f"Error killing process {pid}: {e}")
        return False

def suspend_process(pid):
    """
    Suspend a process by its PID
    
    Parameters:
    - pid: Process ID to suspend
    
    Returns:
    - True if successful, False otherwise
    """
    try:
        process = psutil.Process(pid)
        process.suspend()
        return True
    except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess) as e:
        print(f"Error suspending process {pid}: {e}")
        return False

def resume_process(pid):
    """
    Resume a suspended process by its PID
    
    Parameters:
    - pid: Process ID to resume
    
    Returns:
    - True if successful, False otherwise
    """
    try:
        process = psutil.Process(pid)
        process.resume()
        return True
    except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess) as e:
        print(f"Error resuming process {pid}: {e}")
        return False

def get_process_details(pid):
    """
    Get detailed information about a specific process
    
    Parameters:
    - pid: Process ID
    
    Returns:
    - Dictionary with process details or None if not found
    """
    try:
        process = psutil.Process(pid)
        with process.oneshot():
            # Get basic info
            name = process.name()
            status = process.status()
            create_time = datetime.datetime.fromtimestamp(process.create_time()).strftime("%Y-%m-%d %H:%M:%S")
            
            # Get CPU info
            cpu_percent = process.cpu_percent(interval=0.1)
            cpu_times = process.cpu_times()
            
            # Get memory info
            memory_info = process.memory_info()
            memory_percent = process.memory_percent()
            
            # Get IO counters
            try:
                io_counters = process.io_counters()
                io_data = {
                    'read_count': io_counters.read_count,
                    'write_count': io_counters.write_count,
                    'read_bytes': io_counters.read_bytes,
                    'write_bytes': io_counters.write_bytes
                }
            except (psutil.AccessDenied, AttributeError):
                io_data = {
                    'read_count': 'N/A',
                    'write_count': 'N/A',
                    'read_bytes': 'N/A',
                    'write_bytes': 'N/A'
                }
            
            # Get other details
            try:
                cmdline = process.cmdline()
                exe = process.exe()
                cwd = process.cwd()
            except (psutil.AccessDenied, AttributeError):
                cmdline = ['N/A']
                exe = 'N/A'
                cwd = 'N/A'
            
            # Get connections
            try:
                connections = process.connections()
                conn_data = []
                for conn in connections:
                    conn_data.append({
                        'fd': conn.fd,
                        'family': str(conn.family),
                        'type': str(conn.type),
                        'local_addr': f"{conn.laddr.ip}:{conn.laddr.port}" if hasattr(conn, 'laddr') and conn.laddr else 'N/A',
                        'remote_addr': f"{conn.raddr.ip}:{conn.raddr.port}" if hasattr(conn, 'raddr') and conn.raddr else 'N/A',
                        'status': conn.status
                    })
            except (psutil.AccessDenied, AttributeError):
                conn_data = []
            
            # Get open files
            try:
                open_files = process.open_files()
                files_data = [f.path for f in open_files]
            except (psutil.AccessDenied, AttributeError):
                files_data = []
            
            # Return all data
            return {
                'pid': pid,
                'name': name,
                'status': status,
                'create_time': create_time,
                'cpu_percent': cpu_percent,
                'cpu_user_time': cpu_times.user,
                'cpu_system_time': cpu_times.system,
                'memory_rss': memory_info.rss,
                'memory_vms': memory_info.vms,
                'memory_percent': memory_percent,
                'io': io_data,
                'command': ' '.join(cmdline),
                'executable': exe,
                'cwd': cwd,
                'connections': conn_data,
                'open_files': files_data
            }
    
    except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess) as e:
        print(f"Error getting details for process {pid}: {e}")
        return None