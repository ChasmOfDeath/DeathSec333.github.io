#!/usr/bin/env python3
"""
DeathSec333 Advanced Port Scanner
Professional network reconnaissance tool
"""

import socket
import threading
import tkinter as tk
from tkinter import ttk, scrolledtext
import subprocess
import time
from datetime import datetime

class AdvancedPortScanner:
    def __init__(self, root):
        self.root = root
        self.root.title("DeathSec333 - Advanced Port Scanner")
        self.root.geometry("800x600")
        self.root.configure(bg='black')
        
        # Variables
        self.scanning = False
        self.open_ports = []
        
        self.create_gui()
    
    def create_gui(self):
        # Title
        title = tk.Label(self.root, text="DeathSec333 Advanced Port Scanner", 
                        fg='#ff0040', bg='black', font=('Courier', 16, 'bold'))
        title.pack(pady=10)
        
        # Input Frame
        input_frame = tk.Frame(self.root, bg='black')
        input_frame.pack(pady=10)
        
        tk.Label(input_frame, text="Target:", fg='#00ff00', bg='black', 
                font=('Courier', 12)).grid(row=0, column=0, padx=5)
        self.target_entry = tk.Entry(input_frame, width=20, font=('Courier', 10))
        self.target_entry.grid(row=0, column=1, padx=5)
        self.target_entry.insert(0, "127.0.0.1")
        
        tk.Label(input_frame, text="Port Range:", fg='#00ff00', bg='black',
                font=('Courier', 12)).grid(row=0, column=2, padx=5)
        self.port_start = tk.Entry(input_frame, width=8, font=('Courier', 10))
        self.port_start.grid(row=0, column=3, padx=2)
        self.port_start.insert(0, "1")
        
        tk.Label(input_frame, text="to", fg='#00ff00', bg='black',
                font=('Courier', 12)).grid(row=0, column=4, padx=2)
        self.port_end = tk.Entry(input_frame, width=8, font=('Courier', 10))
        self.port_end.grid(row=0, column=5, padx=2)
        self.port_end.insert(0, "1000")
        
        # Buttons
        button_frame = tk.Frame(self.root, bg='black')
        button_frame.pack(pady=10)
        
        self.scan_btn = tk.Button(button_frame, text="Start Scan", 
                                 command=self.start_scan, bg='#ff0040', fg='white',
                                 font=('Courier', 10, 'bold'))
        self.scan_btn.pack(side=tk.LEFT, padx=5)
        
        self.stop_btn = tk.Button(button_frame, text="Stop Scan", 
                                 command=self.stop_scan, bg='#666666', fg='white',
                                 font=('Courier', 10, 'bold'), state='disabled')
        self.stop_btn.pack(side=tk.LEFT, padx=5)
        
        self.clear_btn = tk.Button(button_frame, text="Clear Results", 
                                  command=self.clear_results, bg='#333333', fg='white',
                                  font=('Courier', 10, 'bold'))
        self.clear_btn.pack(side=tk.LEFT, padx=5)
        
        # Progress Bar
        self.progress = ttk.Progressbar(self.root, length=400, mode='determinate')
        self.progress.pack(pady=10)
        
        # Results Area
        results_frame = tk.Frame(self.root, bg='black')
        results_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        tk.Label(results_frame, text="Scan Results:", fg='#00ff00', bg='black',
                font=('Courier', 12, 'bold')).pack(anchor='w')
        
        self.results_text = scrolledtext.ScrolledText(results_frame, 
                                                     bg='black', fg='#00ff00',
                                                     font=('Courier', 10),
                                                     height=20)
        self.results_text.pack(fill=tk.BOTH, expand=True)
    
    def log_result(self, message):
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.results_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.results_text.see(tk.END)
        self.root.update()
    
    def scan_port(self, target, port):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex((target, port))
            sock.close()
            
            if result == 0:
                service = self.get_service_name(port)
                self.open_ports.append(port)
                self.log_result(f"Port {port}/tcp OPEN - {service}")
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
    
    def start_scan(self):
        if self.scanning:
            return
            
        target = self.target_entry.get().strip()
        try:
            start_port = int(self.port_start.get())
            end_port = int(self.port_end.get())
        except ValueError:
            self.log_result("ERROR: Invalid port range!")
            return
        
        if not target:
            self.log_result("ERROR: Please enter a target!")
            return
        
        self.scanning = True
        self.scan_btn.config(state='disabled')
        self.stop_btn.config(state='normal')
        self.open_ports = []
        
        self.log_result(f"Starting scan on {target}")
        self.log_result(f"Port range: {start_port}-{end_port}")
        self.log_result("=" * 50)
        
        # Start scanning in separate thread
        scan_thread = threading.Thread(target=self.perform_scan, 
                                      args=(target, start_port, end_port))
        scan_thread.daemon = True
        scan_thread.start()
    
    def perform_scan(self, target, start_port, end_port):
        total_ports = end_port - start_port + 1
        self.progress['maximum'] = total_ports
        
        for port in range(start_port, end_port + 1):
            if not self.scanning:
                break
                
            self.scan_port(target, port)
            self.progress['value'] = port - start_port + 1
            self.root.update()
        
        if self.scanning:
            self.log_result("=" * 50)
            self.log_result(f"Scan completed! Found {len(self.open_ports)} open ports")
            if self.open_ports:
                self.log_result(f"Open ports: {', '.join(map(str, self.open_ports))}")
        
        self.scanning = False
        self.scan_btn.config(state='normal')
        self.stop_btn.config(state='disabled')
    
    def stop_scan(self):
        self.scanning = False
        self.log_result("Scan stopped by user")
    
    def clear_results(self):
        self.results_text.delete(1.0, tk.END)
        self.progress['value'] = 0

if __name__ == "__main__":
    root = tk.Tk()
    app = AdvancedPortScanner(root)
    root.mainloop()
