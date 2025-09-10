#!/usr/bin/env python3
"""
DeathSec333 Network Packet Sniffer
Advanced Traffic Analysis and Monitoring Tool
"""

import socket
import struct
import threading
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import time
from datetime import datetime
import json
import sys

class PacketSniffer:
    def __init__(self, root):
        self.root = root
        self.root.title("DeathSec333 - Network Packet Sniffer")
        self.root.geometry("1200x900")
        self.root.configure(bg='black')
        
        self.sniffing = False
        self.packets = []
        self.packet_count = 0
        self.protocols = {'TCP': 0, 'UDP': 0, 'ICMP': 0, 'Other': 0}
        
        self.create_gui()
    
    def create_gui(self):
        # Title
        title = tk.Label(self.root, text="DeathSec333 Network Packet Sniffer", 
                        fg='#ff0040', bg='black', font=('Courier', 16, 'bold'))
        title.pack(pady=10)
        
        # Control Frame
        control_frame = tk.Frame(self.root, bg='black')
        control_frame.pack(pady=10, fill='x', padx=20)
        
        # Interface Selection
        tk.Label(control_frame, text="Interface:", fg='#00ff00', bg='black',
                font=('Courier', 12, 'bold')).pack(side='left', padx=5)
        
        self.interface_var = tk.StringVar(value="eth0")
        interface_combo = ttk.Combobox(control_frame, textvariable=self.interface_var,
                                      values=['eth0', 'wlan0', 'lo', 'any'], width=10)
        interface_combo.pack(side='left', padx=5)
        
        # Filter Options
        tk.Label(control_frame, text="Filter:", fg='#00ff00', bg='black',
                font=('Courier', 12)).pack(side='left', padx=10)
        
        self.filter_var = tk.StringVar(value="all")
        filter_combo = ttk.Combobox(control_frame, textvariable=self.filter_var,
                                   values=['all', 'tcp', 'udp', 'icmp', 'http'], width=8)
        filter_combo.pack(side='left', padx=5)
        
        # Port Filter
        tk.Label(control_frame, text="Port:", fg='#00ff00', bg='black',
                font=('Courier', 12)).pack(side='left', padx=10)
        self.port_entry = tk.Entry(control_frame, width=8, font=('Courier', 10))
        self.port_entry.pack(side='left', padx=5)
        
        # Control Buttons
        button_frame = tk.Frame(self.root, bg='black')
        button_frame.pack(pady=15)
        
        self.start_btn = tk.Button(button_frame, text="Start Sniffing",
                                  command=self.start_sniffing, bg='#ff0040', fg='white',
                                  font=('Courier', 12, 'bold'))
        self.start_btn.pack(side='left', padx=10)
        
        self.stop_btn = tk.Button(button_frame, text="Stop Sniffing",
                                 command=self.stop_sniffing, bg='#666666', fg='white',
                                 font=('Courier', 12, 'bold'), state='disabled')
        self.stop_btn.pack(side='left', padx=10)
        
        self.clear_btn = tk.Button(button_frame, text="Clear Packets",
                                  command=self.clear_packets, bg='#333333', fg='white',
                                  font=('Courier', 12, 'bold'))
        self.clear_btn.pack(side='left', padx=10)
        
        self.save_btn = tk.Button(button_frame, text="Save Capture",
                                 command=self.save_capture, bg='#006600', fg='white',
                                 font=('Courier', 12, 'bold'))
        self.save_btn.pack(side='left', padx=10)
        
        # Statistics Frame
        stats_frame = tk.Frame(self.root, bg='black')
        stats_frame.pack(fill='x', padx=20, pady=10)
        
        tk.Label(stats_frame, text="Statistics:", fg='#00ff00', bg='black',
                font=('Courier', 12, 'bold')).pack(anchor='w')
        
        stats_info_frame = tk.Frame(stats_frame, bg='black')
        stats_info_frame.pack(fill='x', pady=5)
        
        self.packet_count_label = tk.Label(stats_info_frame, text="Packets: 0", 
                                          fg='#00ff00', bg='black', font=('Courier', 10))
        self.packet_count_label.pack(side='left', padx=10)
        
        self.tcp_count_label = tk.Label(stats_info_frame, text="TCP: 0", 
                                       fg='#00ff00', bg='black', font=('Courier', 10))
        self.tcp_count_label.pack(side='left', padx=10)
        
        self.udp_count_label = tk.Label(stats_info_frame, text="UDP: 0", 
                                       fg='#00ff00', bg='black', font=('Courier', 10))
        self.udp_count_label.pack(side='left', padx=10)
        
        self.icmp_count_label = tk.Label(stats_info_frame, text="ICMP: 0", 
                                        fg='#00ff00', bg='black', font=('Courier', 10))
        self.icmp_count_label.pack(side='left', padx=10)
        
        self.status_label = tk.Label(stats_info_frame, text="Status: Ready", 
                                    fg='#ff0040', bg='black', font=('Courier', 10))
        self.status_label.pack(side='right', padx=10)
        
        # Notebook for different views
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Packet List Tab
        packet_frame = tk.Frame(notebook, bg='black')
        notebook.add(packet_frame, text='Packet List')
        
        # Packet List
        self.packet_listbox = tk.Listbox(packet_frame, bg='black', fg='#00ff00',
                                        font=('Courier', 9), height=20,
                                        selectbackground='#333333')
        self.packet_listbox.pack(fill='both', expand=True, pady=5)
        self.packet_listbox.bind('<Double-Button-1>', self.show_packet_details)
        
        # Packet Details Tab
        details_frame = tk.Frame(notebook, bg='black')
        notebook.add(details_frame, text='Packet Details')
        
        tk.Label(details_frame, text="Packet Details:", fg='#00ff00', bg='black',
                font=('Courier', 12, 'bold')).pack(anchor='w', pady=5)
        
        self.details_text = scrolledtext.ScrolledText(details_frame,
                                                     bg='black', fg='#00ff00',
                                                     font=('Courier', 10),
                                                     height=25)
        self.details_text.pack(fill='both', expand=True)
        
        # Raw Data Tab
        raw_frame = tk.Frame(notebook, bg='black')
        notebook.add(raw_frame, text='Raw Data')
        
        tk.Label(raw_frame, text="Raw Packet Data (Hex):", fg='#00ff00', bg='black',
                font=('Courier', 12, 'bold')).pack(anchor='w', pady=5)
        
        self.raw_text = scrolledtext.ScrolledText(raw_frame,
                                                 bg='black', fg='#00ff00',
                                                 font=('Courier', 10),
                                                 height=25)
        self.raw_text.pack(fill='both', expand=True)
    
    def simulate_packet_capture(self):
        """Simulate packet capture for demonstration"""
        import random
        
        sample_ips = ['192.168.1.1', '192.168.1.100', '8.8.8.8', '1.1.1.1', '192.168.1.50']
        protocols = ['TCP', 'UDP', 'ICMP']
        ports = [80, 443, 53, 22, 21, 25, 110, 143, 993, 995]
        
        while self.sniffing:
            # Generate fake packet data
            timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
            protocol = random.choice(protocols)
            src_ip = random.choice(sample_ips)
            dest_ip = random.choice(sample_ips)
            
            if protocol in ['TCP', 'UDP']:
                src_port = random.choice(ports)
                dest_port = random.choice(ports)
                src_info = f"{src_ip}:{src_port}"
                dest_info = f"{dest_ip}:{dest_port}"
                
                if protocol == 'TCP':
                    flags = random.choice(['SYN', 'ACK', 'FIN', 'PSH,ACK', 'SYN,ACK'])
                    info = f"Flags: {flags} Seq: {random.randint(1000, 9999)}"
                    if src_port == 80 or dest_port == 80:
                        info += " [HTTP]"
                    elif src_port == 443 or dest_port == 443:
                        info += " [HTTPS]"
                else:  # UDP
                    info = f"Length: {random.randint(50, 1500)}"
                    if src_port == 53 or dest_port == 53:
                        info += " [DNS]"
            else:  # ICMP
                src_info = src_ip
                dest_info = dest_ip
                info = "ICMP Echo Request/Reply"
            
            # Apply filters
            filter_type = self.filter_var.get().lower()
            port_filter = self.port_entry.get().strip()
            
            if filter_type != "all" and protocol.lower() != filter_type:
                if not (filter_type == "http" and "HTTP" in info):
                    time.sleep(0.1)
                    continue
            
            if port_filter and port_filter.isdigit():
                port_num = int(port_filter)
                if protocol in ["TCP", "UDP"]:
                    if f":{port_num}" not in src_info and f":{port_num}" not in dest_info:
                        time.sleep(0.1)
                        continue
            
            packet_info = {
                'timestamp': timestamp,
                'protocol': protocol,
                'src': src_info,
                'dest': dest_info,
                'length': random.randint(64, 1500),
                'info': info,
                'raw_data': b'Simulated packet data...',
                'details': f"Simulated {protocol} packet from {src_info} to {dest_info}"
            }
            
            self.packets.append(packet_info)
            self.packet_count += 1
            self.protocols[protocol] += 1
            
            # Update GUI
            self.update_packet_list(packet_info)
            self.update_statistics()
            
            time.sleep(random.uniform(0.1, 0.5))  # Random delay between packets
    
    def update_packet_list(self, packet_info):
        """Update packet list display"""
        packet_line = f"{packet_info['timestamp']:<12} {packet_info['protocol']:<8} {packet_info['src']:<20} {packet_info['dest']:<20} {packet_info['length']:<8} {packet_info['info']}"
        
        self.packet_listbox.insert(tk.END, packet_line)
        self.packet_listbox.see(tk.END)
        
        # Limit display to last 1000 packets for performance
        if self.packet_listbox.size() > 1000:
            self.packet_listbox.delete(0)
    
    def update_statistics(self):
        """Update statistics display"""
        self.packet_count_label.config(text=f"Packets: {self.packet_count}")
        self.tcp_count_label.config(text=f"TCP: {self.protocols['TCP']}")
        self.udp_count_label.config(text=f"UDP: {self.protocols['UDP']}")
        self.icmp_count_label.config(text=f"ICMP: {self.protocols['ICMP']}")
    
    def show_packet_details(self, event):
        """Show detailed packet information"""
        selection = self.packet_listbox.curselection()
        if selection:
            index = selection[0]
            if index < len(self.packets):
                packet = self.packets[index]
                
                # Show packet details
                details = f"""Packet Details:
================
Timestamp: {packet['timestamp']}
Protocol: {packet['protocol']}
Source: {packet['src']}
Destination: {packet['dest']}
Length: {packet['length']} bytes
Info: {packet['info']}

Additional Details:
{packet.get('details', 'No additional details available')}
"""
                
                self.details_text.delete(1.0, tk.END)
                self.details_text.insert(tk.END, details)
                
                # Show raw data (hex dump simulation)
                raw_data = packet['raw_data']
                if isinstance(raw_data, bytes):
                    hex_dump = ' '.join(f'{b:02x}' for b in raw_data[:100])  # First 100 bytes
                else:
                    hex_dump = "Simulated hex data: 45 00 00 3c 1c 46 40 00 40 06 b1 e6 ac 10 00 01 ac 10 00 02"
                
                self.raw_text.delete(1.0, tk.END)
                self.raw_text.insert(tk.END, f"Raw Packet Data (Hex):\n{hex_dump}")
    
    def start_sniffing(self):
        """Start packet sniffing"""
        if self.sniffing:
            return
        
        self.sniffing = True
        self.start_btn.config(state='disabled')
        self.stop_btn.config(state='normal')
        self.status_label.config(text="Status: Sniffing...")
        
        # Start sniffing thread (using simulation for demo)
        self.sniffer_thread = threading.Thread(target=self.simulate_packet_capture)
        self.sniffer_thread.daemon = True
        self.sniffer_thread.start()
        
        # Note: In a real implementation, you would need root privileges
        # and would use actual socket programming to capture packets
        messagebox.showinfo("Info", "Packet sniffing started (simulation mode)\nNote: Real packet capture requires root privileges")
    
    def stop_sniffing(self):
        """Stop packet sniffing"""
        self.sniffing = False
        self.start_btn.config(state='normal')
        self.stop_btn.config(state='disabled')
        self.status_label.config(text="Status: Stopped")
    
    def clear_packets(self):
        """Clear all captured packets"""
        self.packets = []
        self.packet_count = 0
        self.protocols = {'TCP': 0, 'UDP': 0, 'ICMP': 0, 'Other': 0}
        
        self.packet_listbox.delete(0, tk.END)
        self.details_text.delete(1.0, tk.END)
        self.raw_text.delete(1.0, tk.END)
        
        self.update_statistics()
    
    def save_capture(self):
        """Save captured packets to file"""
        if not self.packets:
            messagebox.showwarning("Warning", "No packets to save!")
            return
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("Text files", "*.txt"), ("All files", "*.*")]
        )
        
        if filename:
            try:
                if filename.endswith('.json'):
                    with open(filename, 'w') as f:
                        json.dump(self.packets, f, indent=2, default=str)
                else:
                    with open(filename, 'w') as f:
                        f.write("DeathSec333 Packet Capture Report\n")
                        f.write("=" * 50 + "\n\n")
                        f.write(f"Total Packets: {self.packet_count}\n")
                        f.write(f"TCP: {self.protocols['TCP']}\n")
                        f.write(f"UDP: {self.protocols['UDP']}\n")
                        f.write(f"ICMP: {self.protocols['ICMP']}\n")
                        f.write(f"Other: {self.protocols['Other']}\n\n")
                        
                        f.write("Packet Details:\n")
                        f.write("-" * 50 + "\n")
                        
                        for i, packet in enumerate(self.packets, 1):
                            f.write(f"Packet {i}:\n")
                            f.write(f"  Time: {packet['timestamp']}\n")
                            f.write(f"  Protocol: {packet['protocol']}\n")
                            f.write(f"  Source: {packet['src']}\n")
                            f.write(f"  Destination: {packet['dest']}\n")
                            f.write(f"  Length: {packet['length']}\n")
                            f.write(f"  Info: {packet['info']}\n\n")
                
                messagebox.showinfo("Success", f"Capture saved to {filename}")
            
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save capture: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = PacketSniffer(root)
    root.mainloop()
