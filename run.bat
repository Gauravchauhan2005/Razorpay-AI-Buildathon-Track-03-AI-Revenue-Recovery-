@echo off
echo ======================================================================
echo  Razorpay AI Revenue Recovery Agent — 1-Click Launch (Track 03)
echo ======================================================================
echo.

if not exist ".venv\Scripts\python.exe" (
    echo [*] Virtual environment not found. Creating .venv...
    python -m venv .venv
    echo [*] Installing dependencies...
    .venv\Scripts\pip.exe install -r requirements.txt
    echo [*] Seeding database...
    .venv\Scripts\python.exe scripts/load_data.py
    echo [*] Training ML model...
    .venv\Scripts\python.exe -m app.ml.train
)

echo [*] Starting FastAPI Backend on http://127.0.0.1:8000 ...
start "Razorpay Agent - FastAPI Backend" .venv\Scripts\python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 8000

timeout /t 3 /nobreak >nul

echo [*] Starting Streamlit Dashboard on http://localhost:8501 ...
start "Razorpay Agent - Streamlit Dashboard" .venv\Scripts\python.exe -m streamlit run frontend/streamlit_app.py --server.port 8501

echo.
echo ======================================================================
echo  [+] Services are starting!
echo  [+] FastAPI Docs:       http://127.0.0.1:8000/docs
echo  [+] Streamlit UI:       http://localhost:8501
echo  [+] Run Benchmark:      .venv\Scripts\python.exe scripts/batch_benchmark.py 100
echo ======================================================================
echo.
pause
