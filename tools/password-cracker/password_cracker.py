#!/usr/bin/env python3
"""
DeathSec333 Advanced Password Cracker
Dictionary and Brute Force Attack Tool
"""

import hashlib
import itertools
import string
import threading
import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog
import time
from datetime import datetime

class PasswordCracker:
    def __init__(self, root):
        self.root = root
        self.root.title("DeathSec333 - Password Cracker")
        self.root.geometry("900x700")
        self.root.configure(bg='black')
        
        self.cracking = False
        self.found_password = None
        self.attempts = 0
        
        self.create_gui()
    
    def create_gui(self):
        # Title
        title = tk.Label(self.root, text="DeathSec333 Password Cracker", 
                        fg='#ff0040', bg='black', font=('Courier', 16, 'bold'))
        title.pack(pady=10)
        
        # Hash Input Frame
        hash_frame = tk.Frame(self.root, bg='black')
        hash_frame.pack(pady=10, fill='x', padx=20)
        
        tk.Label(hash_frame, text="Target Hash:", fg='#00ff00', bg='black',
                font=('Courier', 12, 'bold')).pack(anchor='w')
        self.hash_entry = tk.Entry(hash_frame, width=80, font=('Courier', 10))
        self.hash_entry.pack(fill='x', pady=5)
        
        # Hash Type Frame
        type_frame = tk.Frame(self.root, bg='black')
        type_frame.pack(pady=5)
        
        tk.Label(type_frame, text="Hash Type:", fg='#00ff00', bg='black',
                font=('Courier', 12)).pack(side='left', padx=5)
        
        self.hash_type = tk.StringVar(value="md5")
        hash_types = ["md5", "sha1", "sha256", "sha512"]
        for ht in hash_types:
            tk.Radiobutton(type_frame, text=ht.upper(), variable=self.hash_type,
                          value=ht, fg='#00ff00', bg='black', 
                          selectcolor='#333333', font=('Courier', 10)).pack(side='left', padx=5)
        
        # Attack Method Frame
        method_frame = tk.Frame(self.root, bg='black')
        method_frame.pack(pady=10)
        
        tk.Label(method_frame, text="Attack Method:", fg='#00ff00', bg='black',
                font=('Courier', 12, 'bold')).pack(anchor='w')
        
        self.attack_method = tk.StringVar(value="dictionary")
        
        dict_frame = tk.Frame(method_frame, bg='black')
        dict_frame.pack(fill='x', pady=5)
        
        tk.Radiobutton(dict_frame, text="Dictionary Attack", 
                      variable=self.attack_method, value="dictionary",
                      fg='#00ff00', bg='black', selectcolor='#333333',
                      font=('Courier', 10)).pack(side='left')
        
        self.dict_file = tk.Entry(dict_frame, width=40, font=('Courier', 10))
        self.dict_file.pack(side='left', padx=10)
        self.dict_file.insert(0, "rockyou.txt")
        
        tk.Button(dict_frame, text="Browse", command=self.browse_dictionary,
                 bg='#333333', fg='white', font=('Courier', 8)).pack(side='left', padx=5)
        
        brute_frame = tk.Frame(method_frame, bg='black')
        brute_frame.pack(fill='x', pady=5)
        
        tk.Radiobutton(brute_frame, text="Brute Force Attack",
                      variable=self.attack_method, value="bruteforce",
                      fg='#00ff00', bg='black', selectcolor='#333333',
                      font=('Courier', 10)).pack(side='left')
        
        tk.Label(brute_frame, text="Max Length:", fg='#00ff00', bg='black',
                font=('Courier', 10)).pack(side='left', padx=10)
        self.max_length = tk.Entry(brute_frame, width=5, font=('Courier', 10))
        self.max_length.pack(side='left', padx=5)
        self.max_length.insert(0, "4")
        
        # Character Set Frame
        charset_frame = tk.Frame(self.root, bg='black')
        charset_frame.pack(pady=5)
        
        tk.Label(charset_frame, text="Character Set:", fg='#00ff00', bg='black',
                font=('Courier', 10)).pack(side='left', padx=5)
        
        self.use_lowercase = tk.BooleanVar(value=True)
        self.use_uppercase = tk.BooleanVar(value=True)
        self.use_digits = tk.BooleanVar(value=True)
        self.use_special = tk.BooleanVar(value=False)
        
        tk.Checkbutton(charset_frame, text="a-z", variable=self.use_lowercase,
                      fg='#00ff00', bg='black', selectcolor='#333333',
                      font=('Courier', 9)).pack(side='left', padx=2)
        tk.Checkbutton(charset_frame, text="A-Z", variable=self.use_uppercase,
                      fg='#00ff00', bg='black', selectcolor='#333333',
                      font=('Courier', 9)).pack(side='left', padx=2)
        tk.Checkbutton(charset_frame, text="0-9", variable=self.use_digits,
                      fg='#00ff00', bg='black', selectcolor='#333333',
                      font=('Courier', 9)).pack(side='left', padx=2)
        tk.Checkbutton(charset_frame, text="!@#$", variable=self.use_special,
                      fg='#00ff00', bg='black', selectcolor='#333333',
                      font=('Courier', 9)).pack(side='left', padx=2)
        
        # Control Buttons
        button_frame = tk.Frame(self.root, bg='black')
        button_frame.pack(pady=15)
        
        self.start_btn = tk.Button(button_frame, text="Start Cracking",
                                  command=self.start_cracking, bg='#ff0040', fg='white',
                                  font=('Courier', 12, 'bold'))
        self.start_btn.pack(side='left', padx=10)
        
        self.stop_btn = tk.Button(button_frame, text="Stop",
                                 command=self.stop_cracking, bg='#666666', fg='white',
                                 font=('Courier', 12, 'bold'), state='disabled')
        self.stop_btn.pack(side='left', padx=10)
        
        self.clear_btn = tk.Button(button_frame, text="Clear",
                                  command=self.clear_results, bg='#333333', fg='white',
                                  font=('Courier', 12, 'bold'))
        self.clear_btn.pack(side='left', padx=10)
        
        # Progress Frame
        progress_frame = tk.Frame(self.root, bg='black')
        progress_frame.pack(fill='x', padx=20, pady=10)
        
        tk.Label(progress_frame, text="Progress:", fg='#00ff00', bg='black',
                font=('Courier', 10)).pack(anchor='w')
        
        self.progress = ttk.Progressbar(progress_frame, length=400, mode='indeterminate')
        self.progress.pack(fill='x', pady=5)
        
        self.status_label = tk.Label(progress_frame, text="Ready", fg='#00ff00', bg='black',
                                    font=('Courier', 10))
        self.status_label.pack(anchor='w')
        
        # Results Area
        results_frame = tk.Frame(self.root, bg='black')
        results_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        tk.Label(results_frame, text="Results:", fg='#00ff00', bg='black',
                font=('Courier', 12, 'bold')).pack(anchor='w')
        
        self.results_text = scrolledtext.ScrolledText(results_frame,
                                                     bg='black', fg='#00ff00',
                                                     font=('Courier', 10),
                                                     height=15)
        self.results_text.pack(fill='both', expand=True)
    
    def log_result(self, message):
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.results_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.results_text.see(tk.END)
        self.root.update()
    
    def hash_password(self, password, hash_type):
        if hash_type == "md5":
            return hashlib.md5(password.encode()).hexdigest()
        elif hash_type == "sha1":
            return hashlib.sha1(password.encode()).hexdigest()
        elif hash_type == "sha256":
            return hashlib.sha256(password.encode()).hexdigest()
        elif hash_type == "sha512":
            return hashlib.sha512(password.encode()).hexdigest()
    
    def browse_dictionary(self):
        filename = filedialog.askopenfilename(
            title="Select Dictionary File",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if filename:
            self.dict_file.delete(0, tk.END)
            self.dict_file.insert(0, filename)
    
    def get_charset(self):
        charset = ""
        if self.use_lowercase.get():
            charset += string.ascii_lowercase
        if self.use_uppercase.get():
            charset += string.ascii_uppercase
        if self.use_digits.get():
            charset += string.digits
        if self.use_special.get():
            charset += "!@#$%^&*()_+-=[]{}|;:,.<>?"
        return charset
    
    def dictionary_attack(self, target_hash, hash_type, dict_file):
        try:
            with open(dict_file, 'r', encoding='utf-8', errors='ignore') as f:
                for line_num, password in enumerate(f, 1):
                    if not self.cracking:
                        break
                    
                    password = password.strip()
                    if not password:
                        continue
                    
                    self.attempts += 1
                    hashed = self.hash_password(password, hash_type)
                    
                    if self.attempts % 1000 == 0:
                        self.status_label.config(text=f"Tried {self.attempts} passwords...")
                        self.root.update()
                    
                    if hashed == target_hash:
                        self.found_password = password
                        self.log_result(f"PASSWORD FOUND: {password}")
                        self.log_result(f"Attempts: {self.attempts}")
                        return True
                        
        except FileNotFoundError:
            self.log_result(f"ERROR: Dictionary file '{dict_file}' not found!")
            return False
        except Exception as e:
            self.log_result(f"ERROR: {str(e)}")
            return False
        
        return False
    
    def bruteforce_attack(self, target_hash, hash_type, max_length, charset):
        for length in range(1, max_length + 1):
            if not self.cracking:
                break
                
            self.log_result(f"Trying passwords of length {length}...")
            
            for password_tuple in itertools.product(charset, repeat=length):
                if not self.cracking:
                    break
                
                password = ''.join(password_tuple)
                self.attempts += 1
                hashed = self.hash_password(password, hash_type)
                
                if self.attempts % 10000 == 0:
                    self.status_label.config(text=f"Tried {self.attempts} passwords...")
                    self.root.update()
                
                if hashed == target_hash:
                    self.found_password = password
                    self.log_result(f"PASSWORD FOUND: {password}")
                    self.log_result(f"Attempts: {self.attempts}")
                    return True
        
        return False
    
    def start_cracking(self):
        target_hash = self.hash_entry.get().strip().lower()
        if not target_hash:
            self.log_result("ERROR: Please enter a target hash!")
            return
        
        hash_type = self.hash_type.get()
        attack_method = self.attack_method.get()
        
        self.cracking = True
        self.found_password = None
        self.attempts = 0
        
        self.start_btn.config(state='disabled')
        self.stop_btn.config(state='normal')
        self.progress.start()
        
        self.log_result("=" * 60)
        self.log_result(f"Starting {attack_method} attack")
        self.log_result(f"Target hash: {target_hash}")
        self.log_result(f"Hash type: {hash_type.upper()}")
        self.log_result("=" * 60)
        
        # Start cracking in separate thread
        crack_thread = threading.Thread(target=self.perform_crack, 
                                       args=(target_hash, hash_type, attack_method))
        crack_thread.daemon = True
        crack_thread.start()
    
    def perform_crack(self, target_hash, hash_type, attack_method):
        start_time = time.time()
        success = False
        
        try:
            if attack_method == "dictionary":
                dict_file = self.dict_file.get().strip()
                if not dict_file:
                    self.log_result("ERROR: Please specify a dictionary file!")
                    return
                success = self.dictionary_attack(target_hash, hash_type, dict_file)
            
            elif attack_method == "bruteforce":
                try:
                    max_length = int(self.max_length.get())
                except ValueError:
                    self.log_result("ERROR: Invalid max length!")
                    return
                
                charset = self.get_charset()
                if not charset:
                    self.log_result("ERROR: Please select at least one character set!")
                    return
                
                self.log_result(f"Character set: {charset}")
                self.log_result(f"Max length: {max_length}")
                success = self.bruteforce_attack(target_hash, hash_type, max_length, charset)
        
        except Exception as e:
            self.log_result(f"ERROR: {str(e)}")
        
        end_time = time.time()
        elapsed = end_time - start_time
        
        self.log_result("=" * 60)
        if success:
            self.log_result(f"SUCCESS! Password cracked in {elapsed:.2f} seconds")
            self.status_label.config(text=f"SUCCESS! Password: {self.found_password}")
        else:
            if self.cracking:
                self.log_result(f"FAILED! Password not found after {self.attempts} attempts")
                self.log_result(f"Time elapsed: {elapsed:.2f} seconds")
                self.status_label.config(text="Failed - Password not found")
            else:
                self.log_result("Attack stopped by user")
                self.status_label.config(text="Stopped by user")
        
        self.cracking = False
        self.start_btn.config(state='normal')
        self.stop_btn.config(state='disabled')
        self.progress.stop()
    
    def stop_cracking(self):
        self.cracking = False
        self.log_result("Stopping attack...")
    
    def clear_results(self):
        self.results_text.delete(1.0, tk.END)
        self.status_label.config(text="Ready")
        self.attempts = 0
        self.found_password = None

if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordCracker(root)
    root.mainloop()
