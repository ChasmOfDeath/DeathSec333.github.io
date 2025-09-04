#!/bin/bash
cd ~/DeathSec333
echo "🔥 Starting DeathSec333 Python Server on port 1337..."
nohup python3 secure_server.py > server.log 2>&1 &
echo "✅ Server started in background"
echo "🌐 Access: http://localhost:1337"
echo "📊 Log: tail -f ~/DeathSec333/server.log"
