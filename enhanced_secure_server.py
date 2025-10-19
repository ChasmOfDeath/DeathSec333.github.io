#!/usr/bin/env python3
import http.server
import socketserver
import os
import json
import datetime
import urllib.parse

class SecurityHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        # Enhanced security headers
        self.send_header('X-Frame-Options', 'DENY')
        self.send_header('X-Content-Type-Options', 'nosniff')
        self.send_header('X-XSS-Protection', '1; mode=block')
        self.send_header('Referrer-Policy', 'no-referrer')
        self.send_header('Server', 'DeathSec333-Protected')
        self.send_header('X-Powered-By', 'DeathSec333-Security-System')
        self.send_header('Strict-Transport-Security', 'max-age=31536000')
        super().end_headers()
    
    def log_security_event(self, event_type, details):
        timestamp = datetime.datetime.now().isoformat()
        client_ip = self.client_address[0]
        
        security_log = {
            'timestamp': timestamp,
            'ip': client_ip,
            'event_type': event_type,
            'details': details,
            'user_agent': self.headers.get('User-Agent', 'Unknown')
        }
        
        # Log to file
        with open('security_events.log', 'a') as f:
            f.write(json.dumps(security_log) + '\n')
        
        print(f"🚨 SECURITY EVENT: {event_type} from {client_ip}")
    
    def do_GET(self):
        # Check for suspicious patterns in URL
        suspicious_patterns = [
            '../', '..\\', 'etc/passwd', 'cmd.exe', 'script',
            'eval', 'alert', 'javascript:', 'vbscript:'
        ]
        
        url_decoded = urllib.parse.unquote(self.path)
        
        for pattern in suspicious_patterns:
            if pattern in url_decoded.lower():
                self.log_security_event('suspicious_url', {
                    'url': self.path,
                    'pattern': pattern
                })
                self.send_error(403, "Access Denied - Security Violation Logged")
                return
        
        # Log all requests
        self.log_message(f"🔍 Access: {self.client_address[0]} - {self.path}")
        
        super().do_GET()

PORT = 1337
Handler = SecurityHTTPRequestHandler

print(f"🛡️ DeathSec333 Enhanced Security Server Starting on Port {PORT}")
print(f"🌐 Local: http://localhost:{PORT}")
print(f"🔒 Advanced security monitoring enabled")
print(f"📊 Security events logged to: security_events.log")

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print(f"✅ Protected server running on port {PORT}")
    httpd.serve_forever()
