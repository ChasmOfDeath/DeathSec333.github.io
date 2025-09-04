#!/usr/bin/env python3
import http.server
import socketserver
import ssl
import os

class SecureHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        # Add security headers
        self.send_header('X-Frame-Options', 'DENY')
        self.send_header('X-Content-Type-Options', 'nosniff')
        self.send_header('X-XSS-Protection', '1; mode=block')
        self.send_header('Referrer-Policy', 'strict-origin-when-cross-origin')
        super().end_headers()
    
    def log_message(self, format, *args):
        print(f"🔒 DeathSec333 Server: {format % args}")

PORT = 1337
Handler = SecureHTTPRequestHandler

print(f"🔥 DeathSec333 Secure Server Starting on Port {PORT}")
print(f"🌐 Access: http://localhost:{PORT}")
print(f"🔒 Security headers enabled")

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print(f"✅ Server running on port {PORT}")
    httpd.serve_forever()
