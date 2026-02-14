#!/usr/bin/env python3
"""
Super Simple Port Scanner (Ports 1-100)

What it does:
- Asks the user for a website or IP address.
- Tries ports 1 to 100 one by one.
- Shows if a port is OPEN, CLOSED, or FILTERED.
- Prints progress while scanning (like 10%, 20%, ...).
- Only works with TCP (not UDP).
"""

import socket
import sys
import time

COMMON_PORTS = {
    20: "FTP-Data",
    21: "FTP",
    22: "SSH",
    23: "Telnet",
    25: "SMTP Mail",
    53: "DNS",
    80: "HTTP Web",
    110: "POP3 Mail",
    143: "IMAP Mail",
    443: "HTTPS Web",
}

def get_ip(target: str) -> str:
    """Turn a website name into an IP address."""
    try:
        return socket.gethostbyname(target)
    except socket.gaierror:
        print("[!] Cannot find that host. Check the spelling.")
        sys.exit(1)

def scan_port(ip: str, port: int, timeout: float = 0.8) -> str:
    """Check if a port is open, closed, or filtered."""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(timeout)
    try:
        result = s.connect_ex((ip, port))
        if result == 0:
            return "open"
        else:
            return "closed"
    except socket.timeout:
        return "filtered"
    except Exception:
        return "closed"
    finally:
        s.close()

def main():
    print(" Simple TCP Port Scanner ")
    target = input("Enter website or IP: ").strip()
    if not target:
        print("Please type ip like 127.0.0.1 or Doman name like example.com")
        sys.exit(1)

    ip = get_ip(target)
    print(f"Target: {target} ({ip})")
    print("Scanning ports 1-100... Please wait.\n")

    start = time.time()
    open_ports = []

    total_ports = 100
    checked = 0

    for port in range(1, 101):
        status = scan_port(ip, port)
        if status == "open":
            service = COMMON_PORTS.get(port, "Unknown service")
            print(f"[OPEN] Port {port:<3} {service}")
            open_ports.append(port)

        # update progress every 10%
        checked += 1
        progress = int((checked / total_ports) * 100)
        if progress % 10 == 0:
            print(f" {progress}% done...")

    duration = time.time() - start

    print("\nScan Finished ")
    if open_ports:
        print("Open ports:", ", ".join(map(str, open_ports)))
    else:
        print("No open ports found in 1-100.")
    print(f"Took {duration:.1f} seconds")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[!] Scan stopped by user.")
        sys.exit(0)

"""Made by: Keneni Bekele"""
