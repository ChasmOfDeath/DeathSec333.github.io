#!/usr/bin/env python3
"""
DeathSec333 Cybersecurity Toolkit Launcher
Launch all your hacking tools from one interface
"""

import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import os
import sys
from datetime import datetime

class DeathSec333Launcher:
    def __init__(self, root):
        self.root = root
        self.root.title("DeathSec333 - Cybersecurity Toolkit")
        self.root.geometry("800x600")
        self.root.configure(bg='black')
        
        # Center the window
        self.center_window()
        
        self.create_gui()
    
    def center_window(self):
        """Center the window on screen"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def create_gui(self):
        # Title Frame
        title_frame = tk.Frame(self.root, bg='black')
        title_frame.pack(pady=20)
        
        # ASCII Art Title
        ascii_title = """
╔══════════════════════════════════════════════════════════════╗
║                        DeathSec333                           ║
║                 Cybersecurity Toolkit v1.0                  ║
║                    Elite Hacking Arsenal                     ║
╚══════════════════════════════════════════════════════════════╝
        """
        
        title_label = tk.Label(title_frame, text=ascii_title, 
                              fg='#ff0040', bg='black', 
                              font=('Courier', 10, 'bold'))
        title_label.pack()
        
        # Subtitle
        subtitle = tk.Label(title_frame, 
                           text="Professional Penetration Testing & Security Analysis Tools",
                           fg='#00ff00', bg='black', 
                           font=('Courier', 12))
        subtitle.pack(pady=10)
        
        # Tools Frame
        tools_frame = tk.Frame(self.root, bg='black')
        tools_frame.pack(expand=True, fill='both', padx=40, pady=20)
        
        # Tool Cards
        self.create_tool_card(tools_frame, 
                             "🎯 Advanced Port Scanner",
                             "Professional network reconnaissance tool\n• Multi-threaded scanning\n• Service detection\n• Custom port ranges",
                             "port-scanner/advanced_port_scanner.py",
                             0, 0)
        
        self.create_tool_card(tools_frame,
                             "🔓 Password Cracker Suite", 
                             "Advanced password cracking toolkit\n• Dictionary attacks\n• Brute force attacks\n• Multiple hash types",
                             "password-cracker/password_cracker.py",
                             0, 1)
        
        self.create_tool_card(tools_frame,
                             "🕷️ Web Vulnerability Scanner",
                             "Comprehensive web application security testing\n• SQL Injection detection\n• XSS vulnerability testing\n• Security header analysis",
                             "web-scanner/web_vulnerability_scanner.py", 
                             1, 0)
        
        self.create_tool_card(tools_frame,
                             "📡 Network Packet Sniffer",
                             "Advanced network traffic analysis\n• Real-time packet capture\n• Protocol analysis\n• Traffic statistics",
                             "packet-sniffer/packet_sniffer.py",
                             1, 1)
        
        # Status Frame
        status_frame = tk.Frame(self.root, bg='black')
        status_frame.pack(fill='x', padx=20, pady=10)
        
        self.status_label = tk.Label(status_frame, 
                                    text="Ready - Select a tool to launch",
                                    fg='#00ff00', bg='black', 
                                    font=('Courier', 10))
        self.status_label.pack(side='left')
        
        # Time display
        self.time_label = tk.Label(status_frame,
                                  text="",
                                  fg='#ff0040', bg='black',
                                  font=('Courier', 10))
        self.time_label.pack(side='right')
        
        # Update time
        self.update_time()
        
        # Footer
        footer_frame = tk.Frame(self.root, bg='black')
        footer_frame.pack(fill='x', pady=10)
        
        footer_text = "DeathSec333 © 2024 | Elite Cybersecurity Solutions | Use Responsibly"
        footer_label = tk.Label(footer_frame, text=footer_text,
                               fg='#666666', bg='black',
                               font=('Courier', 8))
        footer_label.pack()
    
    def create_tool_card(self, parent, title, description, script_path, row, col):
        """Create a tool card widget"""
        card_frame = tk.Frame(parent, bg='#111111', relief='raised', bd=2)
        card_frame.grid(row=row, column=col, padx=15, pady=15, sticky='nsew')
        
        # Configure grid weights
        parent.grid_rowconfigure(row, weight=1)
        parent.grid_columnconfigure(col, weight=1)
        
        # Title
        title_label = tk.Label(card_frame, text=title,
                              fg='#ff0040', bg='#111111',
                              font=('Courier', 14, 'bold'))
        title_label.pack(pady=15)
        
        # Description
        desc_label = tk.Label(card_frame, text=description,
                             fg='#00ff00', bg='#111111',
                             font=('Courier', 10),
                             justify='left')
        desc_label.pack(pady=10, padx=20)
        
        # Launch Button
        launch_btn = tk.Button(card_frame, text="LAUNCH TOOL",
                              command=lambda: self.launch_tool(script_path, title),
                              bg='#ff0040', fg='white',
                              font=('Courier', 12, 'bold'),
                              relief='raised', bd=3,
                              cursor='hand2')
        launch_btn.pack(pady=20)
        
        # Hover effects
        def on_enter(e):
            card_frame.config(bg='#222222')
            title_label.config(bg='#222222')
            desc_label.config(bg='#222222')
            launch_btn.config(bg='#cc0033')
        
        def on_leave(e):
            card_frame.config(bg='#111111')
            title_label.config(bg='#111111')
            desc_label.config(bg='#111111')
            launch_btn.config(bg='#ff0040')
        
        card_frame.bind("<Enter>", on_enter)
        card_frame.bind("<Leave>", on_leave)
        title_label.bind("<Enter>", on_enter)
        title_label.bind("<Leave>", on_leave)
        desc_label.bind("<Enter>", on_enter)
        desc_label.bind("<Leave>", on_leave)
    
    def launch_tool(self, script_path, tool_name):
        """Launch a cybersecurity tool"""
        try:
            self.status_label.config(text=f"Launching {tool_name}...")
            self.root.update()
            
            # Check if script exists
            if not os.path.exists(script_path):
                messagebox.showerror("Error", f"Tool not found: {script_path}")
                self.status_label.config(text="Error - Tool not found")
                return
            
            # Launch the tool
            if sys.platform.startswith('win'):
                subprocess.Popen([sys.executable, script_path], 
                               creationflags=subprocess.CREATE_NEW_CONSOLE)
            else:
                subprocess.Popen([sys.executable, script_path])
            
            self.status_label.config(text=f"{tool_name} launched successfully")
            
            # Show success message
            messagebox.showinfo("Success", f"{tool_name} has been launched!")
            
        except Exception as e:
            error_msg = f"Failed to launch {tool_name}: {str(e)}"
            messagebox.showerror("Error", error_msg)
            self.status_label.config(text="Error launching tool")
    
    def update_time(self):
        """Update the time display"""
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.time_label.config(text=current_time)
        self.root.after(1000, self.update_time)

class AboutDialog:
    def __init__(self, parent):
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("About DeathSec333 Toolkit")
        self.dialog.geometry("600x400")
        self.dialog.configure(bg='black')
        self.dialog.resizable(False, False)
        
        # Center dialog
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        self.create_about_content()
    
    def create_about_content(self):
        # Title
        title = tk.Label(self.dialog, text="DeathSec333 Cybersecurity Toolkit",
                        fg='#ff0040', bg='black',
                        font=('Courier', 16, 'bold'))
        title.pack(pady=20)
        
        # Version info
        version_info = """
Version: 1.0
Release Date: 2024
Author: DeathSec333
License: Educational Use Only

DISCLAIMER:
This toolkit is designed for educational purposes and authorized 
penetration testing only. Users are responsible for complying 
with all applicable laws and regulations.

TOOLS INCLUDED:
• Advanced Port Scanner - Network reconnaissance
• Password Cracker Suite - Authentication testing  
• Web Vulnerability Scanner - Application security testing
• Network Packet Sniffer - Traffic analysis

Use these tools responsibly and only on systems you own 
or have explicit permission to test.
        """
        
        info_label = tk.Label(self.dialog, text=version_info,
                             fg='#00ff00', bg='black',
                             font=('Courier', 10),
                             justify='left')
        info_label.pack(pady=20, padx=30)
        
        # Close button
        close_btn = tk.Button(self.dialog, text="Close",
                             command=self.dialog.destroy,
                             bg='#ff0040', fg='white',
                             font=('Courier', 12, 'bold'))
        close_btn.pack(pady=20)

def main():
    root = tk.Tk()
    
    # Add menu bar
    menubar = tk.Menu(root, bg='black', fg='#00ff00')
    root.config(menu=menubar)
    
    # File menu
    file_menu = tk.Menu(menubar, tearoff=0, bg='black', fg='#00ff00')
    menubar.add_cascade(label="File", menu=file_menu)
    file_menu.add_command(label="Exit", command=root.quit)
    
    # Help menu
    help_menu = tk.Menu(menubar, tearoff=0, bg='black', fg='#00ff00')
    menubar.add_cascade(label="Help", menu=help_menu)
    help_menu.add_command(label="About", command=lambda: AboutDialog(root))
    
    app = DeathSec333Launcher(root)
    
    # Handle window closing
    def on_closing():
        if messagebox.askokcancel("Quit", "Do you want to quit DeathSec333 Toolkit?"):
            root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()

if __name__ == "__main__":
    main()
