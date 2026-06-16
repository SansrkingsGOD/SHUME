#!/bin/bash
echo "Starting AI Resume & Portfolio Builder..."
echo "API: http://localhost:8000"
echo "Open frontend/index.html in your browser"
echo ""
cd "$(dirname "$0")/backend"
python3 run.py
