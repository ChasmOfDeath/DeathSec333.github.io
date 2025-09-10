#!/usr/bin/env python3
"""
DeathSec333 CLI Web Vulnerability Scanner
Terminal-based web security testing tool
"""

import requests
import urllib.parse
import re
from datetime import datetime

class CLIWebScanner:
    def __init__(self):
        self.vulnerabilities = []
        try:
            self.session = requests.Session()
            self.session.headers.update({'User-Agent': 'DeathSec333-Scanner/1.0'})
        except:
            print("\033[91m[!] requests module not found. Install with: pip install requests\033[0m")
            exit(1)
    
    def test_security_headers(self, url):
        print(f"\033[93m[*] Testing security headers...\033[0m")
        
        try:
            response = self.session.get(url, timeout=10)
            headers = response.headers
            
            security_headers = {
                'X-Frame-Options': 'Missing X-Frame-Options header',
                'X-XSS-Protection': 'Missing X-XSS-Protection header',
                'X-Content-Type-Options': 'Missing X-Content-Type-Options header',
                'Strict-Transport-Security': 'Missing HSTS header'
            }
            
            for header, description in security_headers.items():
                if header not in headers:
                    print(f"\033[91m[!] {description}\033[0m")
                    self.vulnerabilities.append(description)
            
            if 'Server' in headers:
                server_info = headers['Server']
                print(f"\033[91m[!] Server information disclosed: {server_info}\033[0m")
                self.vulnerabilities.append(f"Server disclosure: {server_info}")
        
        except Exception as e:
            print(f"\033[91m[!] Error testing headers: {str(e)}\033[0m")

def main():
    print(f"\033[91m╔══════════════════════════════════════╗\033[0m")
    print(f"\033[91m║    DeathSec333 Web Vuln Scanner     ║\033[0m")
    print(f"\033[91m╚══════════════════════════════════════╝\033[0m")
    
    scanner = CLIWebScanner()
    
    try:
        target_url = input("\033[96mEnter target URL: \033[0m").strip()
        if not target_url:
            print("\033[91m[!] No URL provided!\033[0m")
            return
        
        if not target_url.startswith(('http://', 'https://')):
            target_url = 'http://' + target_url
        
        print(f"\033[92m[+] Starting scan on: {target_url}\033[0m")
        print("=" * 50)
        
        scanner.test_security_headers(target_url)
        
        print("=" * 50)
        print(f"\033[92m[+] Scan completed! Found {len(scanner.vulnerabilities)} issues\033[0m")
        
        if scanner.vulnerabilities:
            print(f"\033[93m[*] Summary of findings:\033[0m")
            for i, vuln in enumerate(scanner.vulnerabilities, 1):
                print(f"\033[91m    {i}. {vuln}\033[0m")
        
    except KeyboardInterrupt:
        print(f"\n\033[91m[!] Scan interrupted by user\033[0m")
    except Exception as e:
        print(f"\033[91m[!] Error: {str(e)}\033[0m")

if __name__ == "__main__":
    main()
