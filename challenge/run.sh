#!/bin/bash
cd "$(dirname "$0")"
echo "Starting Learnify platform..."

# Delete old DB to apply fresh schema
rm -f data/platform.db

if ! python -c "import fastapi" 2>/dev/null; then
    echo "Installing dependencies..."
    pip install -r requirements.txt -q
fi

echo "Backend → http://localhost:8000"
uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload &
BACKEND_PID=$!

sleep 2

echo "Frontend → http://localhost:8501"
streamlit run frontend/app.py --server.port 8501 --server.address 0.0.0.0

kill $BACKEND_PID 2>/dev/null