#!/usr/bin/env bash
set -e

echo "======================================================================"
echo " Razorpay AI Revenue Recovery Agent — 1-Click Launch (Track 03)"
echo "======================================================================"

if [ ! -d ".venv" ]; then
    echo "[*] Creating virtual environment..."
    python3 -m venv .venv
    source .venv/bin/activate
    echo "[*] Installing dependencies..."
    pip install -r requirements.txt
    echo "[*] Seeding database..."
    python scripts/load_data.py
    echo "[*] Training ML model..."
    python -m app.ml.train
else
    source .venv/bin/activate
fi

echo "[*] Starting FastAPI Backend on http://127.0.0.1:8000 ..."
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 &
BACKEND_PID=$!

sleep 3

echo "[*] Starting Streamlit Dashboard on http://localhost:8501 ..."
python -m streamlit run frontend/streamlit_app.py --server.port 8501 &
FRONTEND_PID=$!

echo ""
echo "======================================================================"
echo " [+] Services are running!"
echo " [+] FastAPI Docs:       http://127.0.0.1:8000/docs"
echo " [+] Streamlit UI:       http://localhost:8501"
echo " [+] Run Benchmark:      python scripts/batch_benchmark.py 100"
echo "======================================================================"

trap "kill $BACKEND_PID $FRONTEND_PID" EXIT
wait
