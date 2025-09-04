#!/usr/bin/env python3
import subprocess
import os
import signal
import sys

def start_server():
    print("🚀 Starting DeathSec333 Python Server on port 1337...")
    subprocess.Popen(['nohup', 'python3', 'secure_server.py'], 
                    stdout=open('server.log', 'w'), 
                    stderr=subprocess.STDOUT)
    print("✅ Server started in background")
    print("🌐 Access: http://localhost:1337")

def stop_server():
    print("🛑 Stopping Python server...")
    os.system("pkill -f 'python3 secure_server.py'")
    print("✅ Server stopped")

def status_server():
    result = subprocess.run(['pgrep', '-f', 'python3 secure_server.py'], 
                          capture_output=True, text=True)
    if result.returncode == 0:
        print("✅ Server is running on port 1337")
        print(f"🆔 PID: {result.stdout.strip()}")
    else:
        print("❌ Server is not running")

def restart_server():
    stop_server()
    import time
    time.sleep(2)
    start_server()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("""
🔥 DeathSec333 Server Manager
Usage: python3 manage_python_server.py [command]

Commands:
  start   - Start server in background
  stop    - Stop server
  status  - Check server status
  restart - Restart server
  log     - Show server log
        """)
    else:
        cmd = sys.argv[1].lower()
        if cmd == 'start':
            start_server()
        elif cmd == 'stop':
            stop_server()
        elif cmd == 'status':
            status_server()
        elif cmd == 'restart':
            restart_server()
        elif cmd == 'log':
            os.system('tail -f server.log')
        else:
            print("❌ Unknown command")
