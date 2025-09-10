#!/usr/bin/env python3
"""
DeathSec333 CLI Port Scanner
Terminal-based network reconnaissance tool
"""

import socket
import threading
import time
from datetime import datetime

class CLIPortScanner:
    def __init__(self):
        self.open_ports = []
        self.scanning = True
    
    def scan_port(self, target, port):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex((target, port))
            sock.close()
            
            if result == 0:
                service = self.get_service_name(port)
                self.open_ports.append((port, service))
                print(f"[\033[92m+\033[0m] Port {port}/tcp OPEN - {service}")
                return True
        except:
            pass
        return False
    
    def get_service_name(self, port):
        services = {
            21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP", 53: "DNS",
            80: "HTTP", 110: "POP3", 143: "IMAP", 443: "HTTPS", 993: "IMAPS",
            995: "POP3S", 3389: "RDP", 5432: "PostgreSQL", 3306: "MySQL",
            1433: "MSSQL", 6379: "Redis", 27017: "MongoDB", 8080: "HTTP-Proxy"
        }
        return services.get(port, "Unknown")
    
    def scan_range(self, target, start_port, end_port):
        print(f"\n\033[91m╔══════════════════════════════════════╗\033[0m")
        print(f"\033[91m║        DeathSec333 Port Scanner     ║\033[0m")
        print(f"\033[91m╚══════════════════════════════════════╝\033[0m")
        print(f"\033[92mTarget: {target}\033[0m")
        print(f"\033[92mPort Range: {start_port}-{end_port}\033[0m")
        print(f"\033[92mStarting scan at {datetime.now().strftime('%H:%M:%S')}\033[0m")
        print("=" * 50)
        
        threads = []
        for port in range(start_port, end_port + 1):
            if not self.scanning:
                break
            thread = threading.Thread(target=self.scan_port, args=(target, port))
            threads.append(thread)
            thread.start()
            
            # Limit concurrent threads
            if len(threads) >= 100:
                for t in threads:
                    t.join()
                threads = []
        
        # Wait for remaining threads
        for t in threads:
            t.join()
        
        print("=" * 50)
        print(f"\033[92mScan completed! Found {len(self.open_ports)} open ports\033[0m")
        if self.open_ports:
            print(f"\033[93mOpen ports: {', '.join([str(p[0]) for p in self.open_ports])}\033[0m")

def main():
    scanner = CLIPortScanner()
    
    try:
        target = input("\033[96mEnter target IP/hostname (default: 127.0.0.1): \033[0m").strip()
        if not target:
            target = "127.0.0.1"
        
        start_port = input("\033[96mStart port (default: 1): \033[0m").strip()
        start_port = int(start_port) if start_port else 1
        
        end_port = input("\033[96mEnd port (default: 1000): \033[0m").strip()
        end_port = int(end_port) if end_port else 1000
        
        scanner.scan_range(target, start_port, end_port)
        
    except KeyboardInterrupt:
        print("\n\033[91m[!] Scan interrupted by user\033[0m")
        scanner.scanning = False
    except Exception as e:
        print(f"\033[91m[!] Error: {str(e)}\033[0m")

if __name__ == "__main__":
    main()
