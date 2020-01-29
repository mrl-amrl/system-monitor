#!/usr/bin/env python 
import subprocess as sub
from collections import namedtuple


def parse_name_port(name_port):
    port_index = name_port.rfind('.')
    if port_index == -1:
        raise ValueError("could'nt find port index")
    try:
        port = int(name_port[port_index+1:])
    except ValueError:
        raise ValueError("invalid port integer")
    return name_port[:port_index].strip(), port


def parse_packet(data):
    packet_raw = []
    space_index = data.index(' ')
    packet_raw.append(data[:space_index].strip())
    data = data[space_index + 4:]
    arrow_index = data.index('>')
    packet_raw.extend(parse_name_port(data[:arrow_index].strip()))
    data = data[arrow_index+2:]
    colon_index = data.index(':')
    packet_raw.extend(parse_name_port(data[:colon_index].strip()))
    data = data[colon_index+2:]
    comma_index = data.find(',')
    packet_raw.append(data[:comma_index].strip())
    data = data[comma_index+9:]
    packet_raw.append(int(data.strip()))
    Packet = namedtuple('Packet', [
                        'time', 'src_name', 'src_port', 'dest_name', 'dest_port', 'proto', 'length'])
    return Packet(*packet_raw)


def listen(ifname, proto, direction):
    command = ['tcpdump', '-i', ifname, proto, '-l', '-Q', direction]
    p = sub.Popen(command, stdout=sub.PIPE)
    for row in iter(p.stdout.readline, b''):
        try:
            packet = parse_packet(row)
        except ValueError:
            continue
        yield packet


def filter_packet(packet, src_name=None, src_port=None, dest_name=None, dest_port=None, proto=None):
    if proto is not None:
        if proto != packet.proto:
            return False

    if src_name is not None:
        if src_name != packet.src_name:
            return False

    if src_port is not None:
        if src_port != packet.src_port:
            return False

    if dest_name is not None:
        if dest_name != packet.dest_name:
            return False

    if dest_port is not None:
        if dest_port != packet.dest_port:
            return False
    return True


def sizeof_fmt(num, suffix='B'):
    for unit in ['', 'Ki', 'Mi', 'Gi', 'Ti', 'Pi', 'Ei', 'Zi']:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Yi', suffix)


if __name__ == "__main__":
    ifname = 'enp3s0'
    proto = 'udp'
    direction = ['in', 'out', 'inout'][1]

    total_size = 0
    for packet in listen(ifname, proto, direction):
        # if not filter_packet(packet, src_name='192.168.10.170'):
        #     continue
        print(packet)