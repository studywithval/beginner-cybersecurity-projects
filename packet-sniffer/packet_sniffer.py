#!/usr/bin/env python3
"""
Basic packet sniffer built on Scapy.

Requires root/admin privileges and must only be run on networks you own
or are explicitly authorized to monitor - capturing traffic you don't
own is illegal in most jurisdictions.
"""

import argparse

try:
    from scapy.all import IP, TCP, UDP, sniff
except ImportError as exc:
    raise SystemExit(
        "Scapy is required for this tool. Install it with: pip install scapy"
    ) from exc


def describe_packet(packet):
    if IP not in packet:
        return None

    proto = "OTHER"
    sport = dport = None
    if TCP in packet:
        proto = "TCP"
        sport, dport = packet[TCP].sport, packet[TCP].dport
    elif UDP in packet:
        proto = "UDP"
        sport, dport = packet[UDP].sport, packet[UDP].dport

    src, dst = packet[IP].src, packet[IP].dst
    port_info = f"{sport} -> {dport}" if sport else ""
    return f"{proto:5} {src:>15} -> {dst:<15} {port_info}"


def handle_packet(packet):
    line = describe_packet(packet)
    if line:
        print(line)


def main():
    parser = argparse.ArgumentParser(description="Sniff and summarize network packets.")
    parser.add_argument("-c", "--count", type=int, default=20, help="Number of packets to capture (0 = infinite)")
    parser.add_argument("-i", "--iface", help="Interface to sniff on (default: scapy's default)")
    parser.add_argument("-f", "--filter", default="ip", help="BPF filter, e.g. 'tcp port 443' (default: ip)")
    args = parser.parse_args()

    print("Sniffing... press Ctrl+C to stop.\n")
    sniff(count=args.count, iface=args.iface, filter=args.filter, prn=handle_packet)


if __name__ == "__main__":
    main()
