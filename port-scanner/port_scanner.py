#!/usr/bin/env python3
"""
Simple TCP port scanner.

Only scan hosts you own or have explicit written authorization to test.
Unauthorized scanning may violate the Computer Fraud and Abuse Act (US)
or equivalent laws elsewhere.
"""

import argparse
import socket
from concurrent.futures import ThreadPoolExecutor, as_completed


def scan_port(host: str, port: int, timeout: float = 0.5):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(timeout)
    try:
        if sock.connect_ex((host, port)) == 0:
            try:
                service = socket.getservbyport(port)
            except OSError:
                service = "unknown"
            return port, service
    finally:
        sock.close()
    return None


def scan(host: str, start_port: int, end_port: int, workers: int = 100, timeout: float = 0.5):
    open_ports = []
    with ThreadPoolExecutor(max_workers=workers) as executor:
        futures = [
            executor.submit(scan_port, host, port, timeout)
            for port in range(start_port, end_port + 1)
        ]
        for future in as_completed(futures):
            result = future.result()
            if result:
                open_ports.append(result)
    return sorted(open_ports)


def main():
    parser = argparse.ArgumentParser(description="Scan a host for open TCP ports.")
    parser.add_argument("host", nargs="?", default="127.0.0.1", help="Target host (default: 127.0.0.1)")
    parser.add_argument("-p", "--ports", default="1-1024", help="Port range, e.g. 1-1024 (default)")
    parser.add_argument("-t", "--timeout", type=float, default=0.5, help="Per-port connect timeout in seconds")
    args = parser.parse_args()

    start, end = (int(x) for x in args.ports.split("-"))
    print(f"Scanning {args.host} ports {start}-{end}...\n")

    results = scan(args.host, start, end, timeout=args.timeout)
    if not results:
        print("No open ports found.")
    else:
        for port, service in results:
            print(f"  {port:>5}/tcp  open  {service}")


if __name__ == "__main__":
    main()
