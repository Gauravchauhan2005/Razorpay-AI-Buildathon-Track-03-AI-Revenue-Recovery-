# 💳 Razorpay AI Revenue Recovery Agent
### 🏆 Built for Razorpay AI Buildathon — Track 03: AI Revenue Recovery

## 🌟 Key Highlights & Buildathon Criteria Met

| Buildathon Requirement | How We Solved It | Verification |
|---|---|---|
| **Measured Money Recovered Across a Batch** | Autonomous batch recovery benchmark engine evaluates 100+ failed transactions, recovering **₹6.24 Lakh** out of **₹9.19 Lakh** at risk (**67.9% yield**). | Run `python scripts/batch_benchmark.py` or use UI Tab 3 |
| **Compliant Escalation** | VIP Concierge routing for transactions ≥ ₹15,000 or high-value accounts; TRAI/RBI quiet hours (9 PM–9 AM IST outreach rescheduling). | `ComplianceGuard` policy engine |
| **Strict Stopping Rules** | 3-attempt lifetime cap, low-probability floor (< 20% halts intervention), immediate cancellation when payment is captured (`payment.captured`), DND opt-outs. | Automated policy tests & stopping logs |
| **Immutable Audit Trail** | Every single action, model confidence score, guardrail check, and notification is recorded in an immutable ledger with full explainability. | `GET /api/v1/analytics/audit-trail` & UI Tab 4 |
| **Indian FinTech Localization (Hinglish)** | Native English, **Hinglish**, and Hindi recovery messaging specifically optimized for Indian UPI and card drop-offs. | UI Tab 2 & `MessageAgent` |
| **Promise-to-Pay (PTP) Tracker** | Customer payment commitments recorded to pause aggressive retries and trigger punctual, polite nudges. | `PTPService` & UI Tab 5 |

---

## 🏗️ End-to-End System Architecture

```text
               RAZORPAY PAYMENT DEGRADATION / FAILURE
                                │
                                ▼
                   POST /webhooks/razorpay
             (HMAC-SHA256 Signature Verification & Idempotency)
                                │
                                ▼
                     COMPLIANCE & AUDIT GUARD
     ┌──────────────────────────┴──────────────────────────┐
     ▼                                                     ▼
[STOPPING RULES]                                  [POLICY CHECKS]
• Attempt Count ≥ 3 → HALT                        • TRAI Quiet Hours (9PM-9AM IST)
• Already Recovered → CANCEL                      • Minimum 30-min Cooldown Cap
• Probability < 20% → STOP                        • High-Value (≥ ₹15k) → ESCALATE
                                │
                                ▼
                       AI RECOVERY PIPELINE
    ┌───────────────────────────┼───────────────────────────┐
    ▼                           ▼                           ▼
Failure Analyzer         ML Risk Predictor           Customer Profiler
(Error Classification    (GradientBoosting Model     (Segment, Success Rate,
 & Recovery Potential)    P(Recovered) [0.0 - 1.0])   Preferred Channel)
    └───────────────────────────┬───────────────────────────┘
                                ▼
                         STRATEGY ENGINE
      (RETRY_NOW · RETRY_LATER · SEND_PAYMENT_LINK · SEND_REMINDER)
                                │
                                ▼
                       AI MESSAGE PERSONALIZER
          (English · Hinglish · Hindi with Security Guardrails)
                                │
                                ▼
                        ACTION DISPATCHER
             (WhatsApp · SMS · Email · Push · PTP Nudges)
                                │
                                ▼
                CUSTOMER PAYS VIA RECOVERY LINK
                                │
                                ▼
               WEBHOOK EVENT: payment.captured
                                │
                                ▼
        REVENUE ACCOUNTED · PENDING ATTEMPTS CANCELLED · AUDITED
```

---

## 🚀 Live Demo & Quick Start

### 1. Prerequisites
- Python 3.11+ (Tested on Python 3.13.3)
- Git

### 2. Setup
```bash
# Clone the repository
git clone <your-repo-url>
cd razorpay

# Create & activate virtual environment
python -m venv .venv
.venv\Scripts\activate   # Windows
# source .venv/bin/activate  # Linux/macOS

# Install dependencies
pip install -r requirements.txt
```

### 3. Generate Data & Train Model
```bash
# Generate 1,000 synthetic transactions with failure cases
python generator/event_generator.py --count 1000 --seed 42 --output generator/data/batch_001.jsonl

# Seed the database
python scripts/load_data.py

# Train the ML Prediction Model (GradientBoosting)
python -m app.ml.train
```

### 4. Run Live Services
```bash
# Terminal 1: Start FastAPI Backend (Port 8000)
uvicorn app.main:app --host 127.0.0.1 --port 8000

# Terminal 2: Start Interactive Streamlit Dashboard (Port 8501)
streamlit run frontend/streamlit_app.py --server.port 8501
```

- **Streamlit Dashboard**: [http://localhost:8501](http://localhost:8501)
- **FastAPI Backend**: [http://127.0.0.1:8000](http://127.0.0.1:8000)
- **Interactive Swagger Docs**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## 🏆 Run the Buildathon Benchmark Evaluation

To directly verify **The Bar** (measured money recovered across a held-out batch):

```bash
python scripts/batch_benchmark.py 100
```

### Sample Benchmark Scorecard
```text
================================================================================
 🏆 FINAL BUILDATHON BENCHMARK SCORECARD
================================================================================
 • Total Transactions Evaluated:       100
 • Total Revenue at Risk:              ₹918,843.00 (₹9.19 Lakh)
 • Measured Money Recovered:           ₹623,804.00 (₹6.24 Lakh)
 • Net Revenue Recovery Rate:          67.9%
 • Transactions Recovered:             41 of 100
 • Bounded Interventions Dispatched:   62
 • Ineligible Interventions Stopped:   34 (Prevented spam/unrecoverable loss)
 • High-Value VIP Cases Escalated:     4
 • Immutable Audit Trail Events:       79 records logged
================================================================================
```

---

## 🧪 Automated Test Suite

Run the full pytest suite (100% pass rate across 21 unit & integration tests):

```bash
pytest tests/ -v
```

Tests cover:
- Compliance stopping rules (max attempts, low-probability floor, captured payment halt).
- Multi-lingual & Hinglish message generation with financial guardrails.
- Immutable audit trail ledger append & filter operations.
- ML feature extraction & probability bounded ranges.
- Webhook signature validation (HMAC-SHA256) & idempotent replay protection.

---

## 📂 Project Structure

```text
razorpay/
├── app/
│   ├── main.py                      # FastAPI app entrypoint
│   ├── api/
│   │   ├── webhook.py               # Webhook receiver with HMAC & deduplication
│   │   ├── payments.py              # Payment inquiry & listing
│   │   ├── recovery.py              # Recovery orchestrator, PTP & manual triggers
│   │   └── dashboard.py             # Analytics, Audit Trail, and Benchmark endpoints
│   ├── agents/
│   │   ├── failure_analyzer.py      # Failure categorization & recoverability
│   │   ├── compliance_guard.py      # TRAI quiet hours, frequency caps & stopping rules
│   │   ├── strategy_agent.py        # Rule & ML-based action routing
│   │   ├── message_agent.py         # Hinglish, English, Hindi guardrailed messages
│   │   └── recovery_agent.py        # Pipeline orchestrator
│   ├── ml/
│   │   ├── features.py              # Vectorization engine
│   │   ├── train.py                 # Multi-classifier training pipeline
│   │   ├── predict.py               # Real-time inference & heuristic fallback
│   │   └── model.pkl                # Serialized GradientBoosting model
│   ├── models/                      # SQLAlchemy entities (Payment, Customer, AuditLog, PTP)
│   ├── services/                    # Razorpay, Notification, Payment, Audit, PTP services
│   ├── core/                        # Config, logging, security
│   └── utils/                       # Pydantic schemas & helpers
├── frontend/
│   └── streamlit_app.py             # 5-tab interactive Streamlit dashboard
├── generator/                       # Synthetic transaction & persona generators
├── scripts/
│   ├── load_data.py                 # Database seeder
│   └── batch_benchmark.py           # Buildathon benchmark evaluation CLI
├── tests/                           # 21 unit & integration tests
├── Dockerfile & docker-compose.yml  # Production deployment
└── README.md
```

---

## 🛡️ Financial Safety & Guardrails
- **Zero Hallucination of Credentials**: Never requests OTPs, card PINs, CVVs, or passwords.
- **Strict Money Bounds**: Cannot alter transaction amounts or invent unauthorized discounts.
- **Idempotent by Design**: Webhooks deduplicated using unique event IDs.
- **Immediate Cancellation**: The moment a payment is captured, all pending reminders are cancelled instantly.

---

## 📜 License
MIT License
