import psutil

def get_running_processes():
    process_list = []
    for proc in psutil.process_iter(attrs=['pid', 'name', 'memory_info', 'cpu_percent']):
        try:
            open_ports = proc.connections(kind='inet')
            ports = [conn.laddr.port for conn in open_ports]
            process_list.append({
                'pid': proc.info['pid'],
                'name': proc.info['name'],
                'memory_usage': proc.info['memory_info'].rss,
                'cpu_usage': proc.info['cpu_percent'],
                'ports': ports
            })
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    return process_list

def terminate_process(pid):
    try:
        p = psutil.Process(pid)
        p.terminate()
    except psutil.NoSuchProcess:
        pass
    except psutil.AccessDenied:
        pass