import re
import subprocess
import psutil


def run_command(command):
    out = subprocess.Popen(command,
                           stdout=subprocess.PIPE,
                           stderr=subprocess.STDOUT)
    stdout, _ = out.communicate()
    return stdout


def get_nodes():
    stdout = run_command(['rosnode', 'list'])
    nodes = stdout[:-1].split('\n')
    return nodes


def get_node_pid(node_name):
    stdout = run_command(['rosnode', 'info', node_name])
    r = re.findall(r'Pid: \d*', stdout)
    items = []
    for item in r:
        pid = [int(s) for s in item.split() if s.isdigit()][0]
        items.append(pid)
    return items


def get_process_performance(pid):
    stdout = run_command(
        ['ps', '-p', str(pid), '-o', '%cpu,%mem'])[:-1].split('\n')
    items = [float(s) for s in stdout[-1].strip().split(" ") if s != ""]
    return items


def bytes2human(n):
    symbols = ('K', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y')
    prefix = {}
    for i, s in enumerate(symbols):
        prefix[s] = 1 << (i + 1) * 10
    for s in reversed(symbols):
        if n >= prefix[s]:
            value = float(n) / prefix[s]
            return '%.1f%s' % (value, s)
    return "%sB" % n


def get_process_netstat(pid):
    stdout = run_command(['cat', "/proc/"+str(pid)+"/net/dev"])[:-1]
    lines = stdout.split('\n')
    interfaces = {}
    for line in lines[2:]:
        index = line.find(':')
        name = line[:index].strip()
        items = [int(item)
                 for item in line[index+1:].split(' ') if item.isdigit()]
        interfaces[name] = {
            'receive': {
                'bytes': items[0],
                'packets': items[1],
            },
            'transmit': {
                'bytes': items[8],
                'packets': items[9],
            }
        }
    return interfaces


def get_process_file(pid):
    stdout = run_command(
        ['ps', '-p', str(pid), '-o', 'cmd'])[:-1].split('\n')[1]
    return stdout


def get_rosmaster_pid():
    stdout = run_command(['pgrep', '-f', 'rosmaster'])[:-1].split('\n')
    return int(stdout[0])


if __name__ == "__main__":
    from tabulate import tabulate
    ifname = 'enp3s0'

    table = []
    processes = [['/rosmaster', [get_rosmaster_pid()]]]
    processes.extend([[node, get_node_pid(node)] for node in get_nodes()])
    for name, pid in processes:
        performances = get_process_performance(pid[0])
        table.append([
            name,
            pid[0],
            str(performances[0]) + "%",
            str(performances[1]) + "%",
            get_process_netstat(pid[0])['lo']['transmit']['bytes'],
            get_process_netstat(pid[0])['lo']['receive']['bytes'],
            get_process_netstat(pid[0])[ifname]['transmit']['bytes'],
            get_process_netstat(pid[0])[ifname]['receive']['bytes'],
            # get_process_file(pid[0])
        ])

    print tabulate(table, headers=(
        'name',
        'pid',
        'cpu',
        'mem',
        'lo_tx_bytes',
        'lo_rx_bytes',
        ifname + '_tx_bytes',
        ifname + '_rx_bytes',
        # 'command'
    ))
