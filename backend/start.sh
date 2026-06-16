#!/bin/bash
cd "$(dirname "$0")"
echo "Starting AI Resume Builder API on http://localhost:8000"
python3 -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
