#!/usr/bin/env python3
import http.server
import socketserver
import os

PORT = 4444

class SecureHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        # Add security headers
        self.send_header('X-Content-Type-Options', 'nosniff')
        self.send_header('X-Frame-Options', 'DENY')
        self.send_header('X-XSS-Protection', '1; mode=block')
        self.send_header('Strict-Transport-Security', 'max-age=31536000; includeSubDomains')
        self.send_header('Content-Security-Policy', "default-src 'self'")
        super().end_headers()

class ReuseAddrTCPServer(socketserver.TCPServer):
    allow_reuse_address = True

if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    Handler = SecureHandler
    
    try:
        with ReuseAddrTCPServer(("", PORT), Handler) as httpd:
            print(f"🔥 DeathSec333 Secure Server Starting on Port {PORT}")
            print(f"🌐 Access: http://localhost:{PORT}")
            print("🔒 Security headers enabled")
            httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Server stopped")
    except Exception as e:
        print(f"❌ Error: {e}")

