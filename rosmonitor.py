#!/usr/bin/env python
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


def get_ports_by_pid(pid):
    stdout = run_command(
        ['lsof', '-Pa', '-p', str(pid), '-i'])[:-1].split('\n')

    connections = []
    for line in stdout[1:]:
        parts = line.split(' ')
        parts = [part for part in parts if len(part) > 1]
        parts = parts[7:]
        proto = parts[0]
        connection = parts[1]
        connections.append([proto, connection])
    return connections


def get_process_file(pid):
    stdout = run_command(
        ['ps', '-p', str(pid), '-o', 'cmd'])[:-1].split('\n')[1]
    return stdout


def get_rosmaster_pid():
    stdout = run_command(['pgrep', '-f', 'rosmaster'])[:-1].split('\n')
    return int(stdout[0])


def generate_ros_table():
    table = []
    processes = [['/rosmaster', [get_rosmaster_pid()]]]
    processes.extend([[node, get_node_pid(node)] for node in get_nodes()])
    sum_cpu = 0
    sum_mem = 0
    max_pid_len = 0
    max_name_len = 0
    for name, pid in processes:
        performances = get_process_performance(pid[0])
        connections = get_ports_by_pid(pid[0])
        connections = [connection[1]
                       for connection in connections if connection[0] == 'UDP']
        connections = " ".join(connections)
        max_pid_len = max(max_pid_len, len(str(pid[0])))
        max_name_len = max(max_name_len, len(name))
        table.append([
            name,
            pid[0],
            str(performances[0]) + "%",
            str(performances[1]) + "%",
            connections,
        ])
        sum_cpu += performances[0]
        sum_mem += performances[1]
    table.append([
        "-" * max_name_len,
        "-" * max_pid_len,
        str(sum_cpu) + "%",
        str(sum_mem) + "%",
        "",
    ])
    return table


def main():
    from tabulate import tabulate
    import os

    while True:
        try:
            table = generate_ros_table()
            os.system('clear')
            table_items = table[:-1]
            table_items.sort(key=lambda x: x[2], reverse=True)
            table[:-1] = table_items
            print tabulate(table, headers=(
                'name',
                'pid',
                'cpu',
                'mem',
                'UDP connections',
            ))
            print 'press ctrl+c to exit'
        except KeyboardInterrupt:
            break
        except ValueError as e:
            print '[ERR] ' + e
            continue


if __name__ == "__main__":
    try:
        get_rosmaster_pid()
    except ValueError:
        print '[ERR] Cannot detect rosmaster in your ROS system.'
        exit(1)
    main()
