#!/usr/bin/env python3
"""
DeathSec333 CLI Password Cracker
Terminal-based password cracking tool
"""

import hashlib
import itertools
import string
import time
from datetime import datetime

class CLIPasswordCracker:
    def __init__(self):
        self.attempts = 0
        self.found = False
    
    def hash_password(self, password, hash_type):
        if hash_type == "md5":
            return hashlib.md5(password.encode()).hexdigest()
        elif hash_type == "sha1":
            return hashlib.sha1(password.encode()).hexdigest()
        elif hash_type == "sha256":
            return hashlib.sha256(password.encode()).hexdigest()
        elif hash_type == "sha512":
            return hashlib.sha512(password.encode()).hexdigest()
    
    def dictionary_attack(self, target_hash, hash_type, dict_file):
        print(f"\033[93m[*] Starting dictionary attack...\033[0m")
        
        try:
            with open(dict_file, 'r', encoding='utf-8', errors='ignore') as f:
                for line_num, password in enumerate(f, 1):
                    password = password.strip()
                    if not password:
                        continue
                    
                    self.attempts += 1
                    hashed = self.hash_password(password, hash_type)
                    
                    if self.attempts % 1000 == 0:
                        print(f"\033[94m[*] Tried {self.attempts} passwords...\033[0m")
                    
                    if hashed == target_hash:
                        print(f"\033[92m[+] PASSWORD FOUND: {password}\033[0m")
                        print(f"\033[92m[+] Attempts: {self.attempts}\033[0m")
                        return password
                        
        except FileNotFoundError:
            print(f"\033[91m[!] Dictionary file '{dict_file}' not found!\033[0m")
            return None
        except Exception as e:
            print(f"\033[91m[!] Error: {str(e)}\033[0m")
            return None
        
        return None
    
    def brute_force_attack(self, target_hash, hash_type, max_length, charset):
        print(f"\033[93m[*] Starting brute force attack...\033[0m")
        print(f"\033[93m[*] Character set: {charset}\033[0m")
        print(f"\033[93m[*] Max length: {max_length}\033[0m")
        
        for length in range(1, max_length + 1):
            print(f"\033[94m[*] Trying passwords of length {length}...\033[0m")
            
            for password_tuple in itertools.product(charset, repeat=length):
                password = ''.join(password_tuple)
                self.attempts += 1
                hashed = self.hash_password(password, hash_type)
                
                if self.attempts % 10000 == 0:
                    print(f"\033[94m[*] Tried {self.attempts} passwords...\033[0m")
                
                if hashed == target_hash:
                    print(f"\033[92m[+] PASSWORD FOUND: {password}\033[0m")
                    print(f"\033[92m[+] Attempts: {self.attempts}\033[0m")
                    return password
        
        return None

def main():
    print(f"\033[91m╔══════════════════════════════════════╗\033[0m")
    print(f"\033[91m║      DeathSec333 Password Cracker   ║\033[0m")
    print(f"\033[91m╚══════════════════════════════════════╝\033[0m")
    
    cracker = CLIPasswordCracker()
    
    try:
        target_hash = input("\033[96mEnter target hash: \033[0m").strip().lower()
        if not target_hash:
            print("\033[91m[!] No hash provided!\033[0m")
            return
        
        print("\033[96mHash types: 1) MD5  2) SHA1  3) SHA256  4) SHA512\033[0m")
        hash_choice = input("\033[96mSelect hash type (1-4): \033[0m").strip()
        
        hash_types = {"1": "md5", "2": "sha1", "3": "sha256", "4": "sha512"}
        hash_type = hash_types.get(hash_choice, "md5")
        
        print("\033[96mAttack methods: 1) Dictionary  2) Brute Force\033[0m")
        attack_choice = input("\033[96mSelect attack method (1-2): \033[0m").strip()
        
        start_time = time.time()
        result = None
        
        if attack_choice == "1":
            dict_file = input("\033[96mDictionary file (default: password-cracker/rockyou.txt): \033[0m").strip()
            if not dict_file:
                dict_file = "password-cracker/rockyou.txt"
            result = cracker.dictionary_attack(target_hash, hash_type, dict_file)
        
        elif attack_choice == "2":
            max_length = input("\033[96mMax password length (default: 4): \033[0m").strip()
            max_length = int(max_length) if max_length else 4
            
            charset = string.ascii_lowercase + string.ascii_uppercase + string.digits
            result = cracker.brute_force_attack(target_hash, hash_type, max_length, charset)
        
        end_time = time.time()
        elapsed = end_time - start_time
        
        print("=" * 50)
        if result:
            print(f"\033[92m[+] SUCCESS! Password cracked in {elapsed:.2f} seconds\033[0m")
        else:
            print(f"\033[91m[!] FAILED! Password not found after {cracker.attempts} attempts\033[0m")
            print(f"\033[91m[!] Time elapsed: {elapsed:.2f} seconds\033[0m")
        
    except KeyboardInterrupt:
        print(f"\n\033[91m[!] Attack stopped by user\033[0m")
    except Exception as e:
        print(f"\033[91m[!] Error: {str(e)}\033[0m")

if __name__ == "__main__":
    main()
