# AI-Based Payment Recovery Agent
## Complete End-to-End Project Build Document

**Project Type:** AI/Agentic FinTech System  
**Platform:** Razorpay  
**Primary Goal:** Recover failed or abandoned payments using intelligent, personalized, and automated recovery strategies.

---

# 1. Project Overview

## 1.1 Problem Statement

Online payments frequently fail because of:

- Insufficient balance
- Bank/network failures
- Incorrect payment details
- UPI failures
- Card declines
- Authentication failures
- Temporary technical problems
- Customer abandonment
- Payment timeouts
- Expired payment links

A conventional payment system generally reports the failure but does not intelligently determine:

1. Why the payment failed.
2. Whether the customer is likely to complete payment.
3. When the customer should be contacted.
4. Which communication channel should be used.
5. What message should be sent.
6. Whether the customer should receive another payment link.
7. When the recovery attempt should stop.

The proposed system solves this problem using an **AI-powered Payment Recovery Agent**.

---

# 2. Proposed Solution

The system receives payment events and customer/payment information.

It then performs:

```text
Payment Event
      ↓
Event Ingestion
      ↓
Data Validation
      ↓
Payment Failure Analysis
      ↓
Feature Extraction
      ↓
Recovery Probability Prediction
      ↓
Recovery Strategy Selection
      ↓
AI Message Generation
      ↓
Action Execution
      ↓
Customer Response
      ↓
Payment Retry
      ↓
Outcome Tracking
      ↓
Model/Strategy Improvement
```

The system should not blindly retry every payment.

Instead, it should determine the **best next action**.

Example:

```text
Payment Failed
     ↓
Reason = Insufficient Balance
     ↓
Recovery Probability = 82%
     ↓
Recommended Action = Retry after 6 hours
     ↓
Preferred Channel = WhatsApp/SMS
     ↓
AI generates personalized message
     ↓
Payment Link sent
     ↓
Customer pays
     ↓
Recovery Successful
```

---

# 3. Project Objectives

The system should achieve the following:

### Objective 1 — Detect failed payments

Identify failed, pending, abandoned, or incomplete transactions.

### Objective 2 — Understand failure reasons

Classify failures into categories such as:

- Insufficient funds
- Bank decline
- Network failure
- Authentication failure
- Incorrect details
- UPI failure
- Timeout
- Customer abandonment
- Unknown/technical failure

### Objective 3 — Predict recovery probability

Estimate the probability that a customer will successfully recover the payment.

Example:

```text
Customer A → 91%
Customer B → 64%
Customer C → 12%
```

### Objective 4 — Select recovery action

Possible actions:

```text
NO_ACTION
RETRY_NOW
RETRY_LATER
SEND_REMINDER
SEND_PAYMENT_LINK
CHANGE_CHANNEL
OFFER_ASSISTANCE
ESCALATE_TO_HUMAN
```

### Objective 5 — Generate personalized communication

Instead of sending the same message to everyone, the AI generates context-aware messages.

### Objective 6 — Track recovery

Measure:

- Recovery rate
- Revenue recovered
- Number of attempts
- Time to recovery
- Channel effectiveness
- Failure reason effectiveness

---

# 4. Recommended Technology Stack

## Backend

Use:

```text
Python
FastAPI
Pydantic
SQLAlchemy
```

## Database

For development:

```text
SQLite
```

For production:

```text
PostgreSQL
```

## AI / Machine Learning

Start with:

```text
scikit-learn
pandas
numpy
```

Optional advanced model:

```text
XGBoost
LightGBM
PyTorch
TensorFlow
```

For the LLM layer:

```text
OpenAI API
```

or another compatible LLM provider.

## Workflow

For a simple project:

```text
Python services
```

For an advanced agentic architecture:

```text
LangGraph
```

## Frontend

Recommended:

```text
React
```

or, for a faster hackathon implementation:

```text
Streamlit
```

## Infrastructure

Development:

```text
Docker
Docker Compose
```

Production:

```text
AWS / Azure / GCP
```

## Payment Integration

```text
Razorpay APIs
Razorpay Webhooks
```

Razorpay officially supports webhook events including `payment.failed`, `payment.authorized`, `payment.captured`, and `order.paid`. Webhooks are asynchronous and are recommended for automation, while API verification can supplement them for critical user-facing status checks.

---

# 5. System Architecture

The recommended architecture is:

```text
                       ┌─────────────────────┐
                       │      Razorpay       │
                       │ Payments / Events   │
                       └──────────┬──────────┘
                                  │
                                  ▼
                       ┌─────────────────────┐
                       │  Webhook Receiver   │
                       │     FastAPI         │
                       └──────────┬──────────┘
                                  │
                                  ▼
                       ┌─────────────────────┐
                       │ Event Normalizer    │
                       └──────────┬──────────┘
                                  │
                                  ▼
                       ┌─────────────────────┐
                       │ Payment Database    │
                       └──────────┬──────────┘
                                  │
                                  ▼
                    ┌──────────────────────────┐
                    │ Payment Recovery Agent   │
                    └────────────┬─────────────┘
                                 │
             ┌───────────────────┼───────────────────┐
             │                   │                   │
             ▼                   ▼                   ▼
      ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
      │ Failure     │    │ Recovery    │    │ Customer    │
      │ Analyzer    │    │ Predictor   │    │ Profiler    │
      └──────┬──────┘    └──────┬──────┘    └──────┬──────┘
             │                   │                   │
             └───────────────────┼───────────────────┘
                                 ▼
                       ┌─────────────────────┐
                       │ Strategy Engine     │
                       └──────────┬──────────┘
                                  │
                                  ▼
                       ┌─────────────────────┐
                       │ LLM Message Agent   │
                       └──────────┬──────────┘
                                  │
                                  ▼
                       ┌─────────────────────┐
                       │ Action Dispatcher   │
                       └──────────┬──────────┘
                                  │
                    ┌─────────────┼─────────────┐
                    ▼             ▼             ▼
                  SMS         WhatsApp       Email
                    │             │             │
                    └─────────────┼─────────────┘
                                  ▼
                         Customer Payment
                                  │
                                  ▼
                       ┌─────────────────────┐
                       │ Recovery Tracking   │
                       └─────────────────────┘
```

---

# 6. Project Folder Structure

Your current project already has a `generator` directory.

Build the project into this structure:

```text
payment-recovery-agent/
│
├── README.md
├── requirements.txt
├── .env
├── .env.example
├── docker-compose.yml
├── Dockerfile
│
├── generator/
│   ├── event_generator.py
│   ├── customer_generator.py
│   ├── payment_generator.py
│   └── data/
│       ├── batch_001.jsonl
│       └── batch_002.jsonl
│
├── app/
│   ├── main.py
│   │
│   ├── api/
│   │   ├── webhook.py
│   │   ├── payments.py
│   │   ├── recovery.py
│   │   └── dashboard.py
│   │
│   ├── agents/
│   │   ├── recovery_agent.py
│   │   ├── failure_analyzer.py
│   │   ├── strategy_agent.py
│   │   └── message_agent.py
│   │
│   ├── ml/
│   │   ├── features.py
│   │   ├── train.py
│   │   ├── predict.py
│   │   └── model.pkl
│   │
│   ├── services/
│   │   ├── razorpay_service.py
│   │   ├── notification_service.py
│   │   ├── payment_service.py
│   │   └── recovery_service.py
│   │
│   ├── models/
│   │   ├── payment.py
│   │   ├── customer.py
│   │   ├── recovery.py
│   │   └── event.py
│   │
│   ├── database/
│   │   ├── database.py
│   │   └── migrations/
│   │
│   ├── core/
│   │   ├── config.py
│   │   ├── security.py
│   │   └── logging.py
│   │
│   └── utils/
│       ├── validators.py
│       └── helpers.py
│
├── frontend/
│   ├── src/
│   └── package.json
│
├── tests/
│   ├── test_webhook.py
│   ├── test_recovery.py
│   ├── test_predictor.py
│   └── test_strategy.py
│
└── docs/
    ├── architecture.md
    ├── api.md
    └── demo.md
```

---

# 7. Step 1 — Fix Python on Windows

Your current command:

```text
python3 event_generator.py
```

produces:

```text
Python was not found
```

On Windows, first check:

```cmd
python --version
```

If that works:

```cmd
python event_generator.py --count 1000 --seed 42 --output data/batch_001.jsonl
```

Alternatively:

```cmd
py --version
```

and:

```cmd
py event_generator.py --count 1000 --seed 42 --output data/batch_001.jsonl
```

---

# 8. Step 2 — Create Virtual Environment

From:

```text
payment-recovery-agent\
```

run:

```cmd
python -m venv .venv
```

Activate it:

```cmd
.venv\Scripts\activate
```

You should see:

```text
(.venv)
```

in the terminal.

Upgrade pip:

```cmd
python -m pip install --upgrade pip
```

---

# 9. Step 3 — Install Dependencies

Create:

```text
requirements.txt
```

Add:

```text
fastapi
uvicorn[standard]
pydantic
pydantic-settings
python-dotenv
sqlalchemy
requests
httpx
pandas
numpy
scikit-learn
joblib
razorpay
python-multipart
```

Then:

```cmd
pip install -r requirements.txt
```

For the optional LLM layer:

```cmd
pip install openai
```

For advanced agent orchestration:

```cmd
pip install langgraph
```

---

# 10. Step 4 — Configure Environment Variables

Create:

```text
.env
```

Example:

```env
RAZORPAY_KEY_ID=your_test_key_id
RAZORPAY_KEY_SECRET=your_test_key_secret
RAZORPAY_WEBHOOK_SECRET=your_webhook_secret

DATABASE_URL=sqlite:///./payment_recovery.db

OPENAI_API_KEY=your_api_key

SMS_PROVIDER_API_KEY=
WHATSAPP_PROVIDER_API_KEY=
EMAIL_PROVIDER_API_KEY=
```

Never commit `.env` to GitHub.

Create:

```text
.gitignore
```

with:

```text
.venv/
.env
__pycache__/
*.pyc
*.db
model.pkl
node_modules/
```

---

# 11. Step 5 — Generate Synthetic Payment Data

Your existing command is:

```cmd
python event_generator.py --count 1000 --seed 42 --output data/batch_001.jsonl
```

The generated dataset should contain events similar to:

```json
{
  "event_id": "evt_000001",
  "customer_id": "cust_1001",
  "payment_id": "pay_100001",
  "order_id": "order_100001",
  "amount": 2499,
  "currency": "INR",
  "payment_method": "upi",
  "status": "failed",
  "failure_reason": "insufficient_funds",
  "timestamp": "2026-09-05T10:30:00",
  "customer_age_days": 180,
  "previous_attempts": 2,
  "previous_success_rate": 0.75
}
```

---

# 12. Recommended Dataset Fields

Your generator should produce:

### Customer

```text
customer_id
customer_age_days
customer_segment
previous_transactions
successful_transactions
failed_transactions
average_transaction_value
```

### Payment

```text
payment_id
order_id
amount
currency
payment_method
status
failure_reason
timestamp
```

### Behaviour

```text
previous_attempts
time_since_last_payment
number_of_failed_attempts
number_of_successful_payments
```

### Context

```text
hour
day_of_week
device_type
location
```

### Recovery

```text
previous_recovery_attempts
previous_recovery_success
preferred_channel
```

---

# 13. Step 6 — Database Design

Create four major tables.

## Customer

```text
customers
---------
id
customer_id
email
phone
segment
created_at
preferred_channel
```

## Payment

```text
payments
--------
id
payment_id
order_id
customer_id
amount
currency
method
status
failure_reason
created_at
updated_at
```

## Recovery Attempt

```text
recovery_attempts
-----------------
id
payment_id
customer_id
attempt_number
channel
strategy
message
scheduled_at
executed_at
status
result
```

## Event

```text
events
------
id
event_id
event_type
payment_id
payload
received_at
processed_at
```

---

# 14. Step 7 — Event Ingestion

The system must accept Razorpay webhook events.

Important events include:

```text
payment.authorized
payment.captured
payment.failed
order.paid
```

Razorpay's documentation specifically describes `payment.failed` as the event used to receive notifications when a customer's payment attempt fails.

Create:

```text
app/api/webhook.py
```

Conceptually:

```text
POST /webhooks/razorpay
        ↓
Receive raw body
        ↓
Verify signature
        ↓
Parse event
        ↓
Store event
        ↓
Process event
        ↓
Return HTTP 2xx
```

---

# 15. Step 8 — Webhook Security

Never trust an incoming webhook automatically.

The system should:

```text
Incoming webhook
      ↓
Read raw request body
      ↓
Read Razorpay signature
      ↓
Generate HMAC signature
      ↓
Compare signatures
      ↓
Valid?
  ├── No → Reject
  └── Yes → Process
```

Razorpay recommends validating webhook signatures using the **raw webhook request body**, rather than a reconstructed JSON representation.

Also make webhook processing idempotent.

If the same event arrives twice:

```text
event_id = evt_123
```

the system should process it only once.

---

# 16. Step 9 — Failure Analyzer

Create:

```text
failure_analyzer.py
```

The analyzer converts raw payment errors into meaningful categories.

Example:

```text
Raw error:
"Transaction declined due to insufficient balance"

↓

Category:
INSUFFICIENT_FUNDS

↓

Severity:
MEDIUM

↓

Recoverability:
HIGH
```

Recommended categories:

```text
INSUFFICIENT_FUNDS
BANK_DECLINE
NETWORK_FAILURE
AUTHENTICATION_FAILURE
INVALID_DETAILS
UPI_FAILURE
TIMEOUT
CUSTOMER_ABANDONED
LIMIT_EXCEEDED
UNKNOWN
```

---

# 17. Step 10 — Feature Engineering

Create features for the prediction model.

Example:

```text
amount
payment_method
failure_reason
previous_attempts
previous_success_rate
customer_age_days
hour
day_of_week
previous_recovery_success
time_since_previous_attempt
```

Example feature vector:

```text
[
  2499,
  UPI,
  INSUFFICIENT_FUNDS,
  2,
  0.75,
  180,
  14,
  5,
  0.60,
  360
]
```

---

# 18. Step 11 — Recovery Prediction Model

The ML model predicts:

```text
P(payment will be recovered)
```

Example:

```text
Input
 ↓
Payment + Customer Features
 ↓
ML Model
 ↓
0.87
```

Interpretation:

```text
87% recovery probability
```

Start with:

```text
LogisticRegression
```

Then compare with:

```text
RandomForestClassifier
GradientBoostingClassifier
XGBoost
```

---

# 19. Step 12 — Training Dataset

Create a target variable:

```text
recovered
```

where:

```text
1 = payment eventually recovered
0 = payment not recovered
```

Example:

| Amount | Method | Attempts | Previous Success | Failure | Recovered |
|---:|---|---:|---:|---|---:|
| 500 | UPI | 1 | 0.9 | network | 1 |
| 2500 | Card | 3 | 0.2 | decline | 0 |
| 1000 | UPI | 1 | 0.8 | balance | 1 |

---

# 20. Step 13 — Train the Model

Pipeline:

```text
JSONL Dataset
     ↓
Pandas DataFrame
     ↓
Data Cleaning
     ↓
Feature Engineering
     ↓
Train/Test Split
     ↓
Model Training
     ↓
Evaluation
     ↓
Save Model
```

Save the model:

```text
app/ml/model.pkl
```

Use:

```text
joblib.dump()
```

---

# 21. Step 14 — Model Evaluation

Do not only measure accuracy.

Measure:

```text
Accuracy
Precision
Recall
F1 Score
ROC-AUC
```

For a recovery system, pay special attention to:

```text
Recall
Precision
ROC-AUC
```

Also measure business metrics:

```text
Recovered Revenue
Recovery Rate
Cost per Recovery
False Recovery Attempts
```

---

# 22. Step 15 — Customer Segmentation

Divide customers into groups.

Example:

### High Value

```text
High transaction value
High historical success
```

### Loyal

```text
Many successful transactions
```

### At Risk

```text
Multiple recent failures
```

### New Customer

```text
Little/no historical data
```

### Low Probability

```text
Repeated failures
Low engagement
```

This helps the strategy engine make better decisions.

---

# 23. Step 16 — Recovery Strategy Engine

The strategy engine is the brain of the system.

Input:

```text
Payment data
+
Customer data
+
Failure reason
+
Recovery probability
+
Previous attempts
```

Output:

```text
Recommended action
```

Example rules:

```text
IF recovery_probability >= 0.80
AND attempts == 0
→ RETRY_NOW

IF failure_reason == INSUFFICIENT_FUNDS
→ RETRY_LATER

IF failure_reason == NETWORK_FAILURE
→ RETRY_NOW

IF attempts >= 3
→ STOP_AUTOMATIC_RETRY

IF recovery_probability < 0.20
→ NO_ACTION

IF high_value_customer
AND probability >= 0.60
→ HUMAN_ASSISTANCE
```

---

# 24. Step 17 — Recovery Policy

A simple policy:

```text
Attempt 1
   ↓
Wait 15 minutes
   ↓
Attempt 2
   ↓
Wait 6 hours
   ↓
Attempt 3
   ↓
Wait 24 hours
   ↓
Final reminder
   ↓
Stop
```

Never create infinite retries.

Use:

```text
MAX_RECOVERY_ATTEMPTS = 3
```

---

# 25. Step 18 — Channel Selection

Possible channels:

```text
SMS
Email
WhatsApp
Push Notification
```

The agent should choose the best channel.

Example:

```text
Customer preferred channel = WhatsApp
       ↓
WhatsApp available?
       ↓
YES
       ↓
Send WhatsApp message
```

Fallback:

```text
WhatsApp
 ↓
SMS
 ↓
Email
```

---

# 26. Step 19 — AI Message Generator

The LLM should not make payment decisions directly.

Instead:

```text
ML + Rules
      ↓
Determine strategy
      ↓
LLM
      ↓
Generate message
```

Example input:

```text
Customer:
Returning customer

Failure:
Temporary bank/network failure

Amount:
₹2,499

Recommended action:
Retry now

Tone:
Professional and helpful
```

Generated message:

```text
Hi! Your recent payment of ₹2,499 could not be completed due to a temporary payment issue. You can safely try again using the payment option below. If you continue to face an issue, we're happy to help.
```

---

# 27. Step 20 — LLM Guardrails

The LLM must NOT:

- Invent payment details.
- Invent discounts.
- Invent refunds.
- Change payment amount.
- Claim payment success without verification.
- Ask for passwords.
- Ask for OTPs.
- Ask for card PINs.
- Expose sensitive information.

The LLM should only generate communication from trusted structured data.

Use a structured prompt:

```text
Customer name: {name}
Amount: {amount}
Failure reason: {safe_failure_reason}
Recommended action: {action}
Payment link: {payment_link}

Generate a concise customer recovery message.

Do not:
- request OTP
- request PIN
- invent discounts
- claim successful payment
- expose internal system information
```

---

# 28. Step 21 — Agent Architecture

The recovery agent can be implemented as:

```text
                    Recovery Agent
                          │
        ┌─────────────────┼──────────────────┐
        │                 │                  │
        ▼                 ▼                  ▼
 Failure Analyzer   Risk Predictor    Customer Profiler
        │                 │                  │
        └─────────────────┼──────────────────┘
                          ▼
                  Strategy Agent
                          │
                          ▼
                  Message Agent
                          │
                          ▼
                  Action Dispatcher
                          │
                          ▼
                   Recovery Result
```

---

# 29. Step 22 — Agent Decision Object

Use a structured output such as:

```json
{
  "payment_id": "pay_123",
  "recovery_probability": 0.82,
  "failure_category": "network_failure",
  "recommended_action": "retry_now",
  "channel": "whatsapp",
  "priority": "high",
  "attempt_number": 1,
  "reason": "High recovery probability and temporary failure type"
}
```

This makes the system explainable.

---

# 30. Step 23 — Explainability

Every decision should have a reason.

Example:

```text
Recovery Probability: 82%

Recommended Action:
Retry after 15 minutes

Reason:
• Customer has 8 previous successful payments
• Failure was classified as temporary network failure
• Only one recovery attempt has been made
• Historical recovery probability is high
```

This is important for demonstrating that the AI is not a black box.

---

# 31. Step 24 — Notification Service

Create:

```text
notification_service.py
```

Interface:

```text
send_sms()
send_email()
send_whatsapp()
send_push()
```

During development, use mock services.

Example:

```text
MOCK SMS

To: +91XXXXXXXXXX

Message:
Your payment could not be completed...
```

Later replace the mock provider with an actual communication provider.

---

# 32. Step 25 — Razorpay Integration

Use Razorpay's Test Mode while developing.

Razorpay Payment Links can also be created and shared with customers through APIs, email, SMS, or social channels.

Recommended flow:

```text
Failed Payment
      ↓
Recovery Agent
      ↓
Decision
      ↓
Generate/Reuse Payment Link
      ↓
Send Link
      ↓
Customer Opens Link
      ↓
Payment
      ↓
Razorpay
      ↓
Webhook
      ↓
payment.captured
      ↓
Recovery = SUCCESS
```

---

# 33. Step 26 — Webhook Processing Logic

For:

```text
payment.failed
```

execute:

```text
Store Event
     ↓
Find Payment
     ↓
Analyze Failure
     ↓
Generate Features
     ↓
Predict Recovery
     ↓
Select Strategy
     ↓
Generate Message
     ↓
Schedule Action
```

For:

```text
payment.captured
```

execute:

```text
Find Recovery Attempts
        ↓
Mark Payment Recovered
        ↓
Calculate Recovered Revenue
        ↓
Stop Future Recovery Attempts
        ↓
Update Customer History
```

This is extremely important.

If a payment succeeds, the agent must stop sending recovery reminders.

---

# 34. Step 27 — Dashboard

Build a dashboard with:

## KPI Cards

```text
Total Payments
Failed Payments
Recovery Attempts
Recovered Payments
Recovery Rate
Revenue Recovered
```

Example:

```text
Total Payments       10,000
Failed Payments       1,840
Recovery Attempts     1,620
Recovered Payments      782
Recovery Rate          42.7%
Revenue Recovered   ₹8.42L
```

---

# 35. Dashboard — Recovery Funnel

Show:

```text
Failed Payments
      ↓
Eligible for Recovery
      ↓
Recovery Attempt
      ↓
Customer Engaged
      ↓
Payment Completed
```

Example:

```text
1840
 ↓
1620
 ↓
1400
 ↓
782
```

---

# 36. Dashboard — Failure Analysis

Display:

```text
Failure Reason
-----------------------
Insufficient Funds   31%
Network Failure      24%
Bank Decline         18%
UPI Failure          14%
Timeout               8%
Other                 5%
```

---

# 37. Dashboard — Recovery by Channel

Display:

```text
WhatsApp    51%
SMS         38%
Email       27%
Push        19%
```

Do not hard-code these values in the final system; calculate them from actual data.

---

# 38. Dashboard — AI Decisions

Show:

```text
Payment ID
Failure
Probability
Action
Channel
Status
```

Example:

| Payment | Failure | Probability | Action | Status |
|---|---|---:|---|---|
| pay_101 | Network | 89% | Retry | Recovered |
| pay_102 | Balance | 76% | Retry later | Pending |
| pay_103 | Decline | 21% | Stop | Closed |

---

# 39. Step 28 — API Endpoints

Recommended APIs:

```text
GET  /health
GET  /payments
GET  /payments/{id}
POST /webhooks/razorpay

GET  /recovery
GET  /recovery/{id}
POST /recovery/{id}/retry

GET  /analytics/overview
GET  /analytics/failures
GET  /analytics/channels
GET  /analytics/revenue

POST /agent/analyze/{payment_id}
POST /agent/recover/{payment_id}
```

---

# 40. Step 29 — Example API Flow

Request:

```text
POST /agent/analyze/pay_123
```

Response:

```json
{
  "payment_id": "pay_123",
  "status": "failed",
  "failure_reason": "network_failure",
  "recovery_probability": 0.87,
  "recommended_action": "retry_later",
  "retry_after_minutes": 15,
  "channel": "whatsapp",
  "priority": "high"
}
```

---

# 41. Step 30 — Testing Strategy

Test each component independently.

## Unit Tests

Test:

```text
Failure classification
Feature generation
Prediction
Strategy selection
Message generation
Webhook verification
Retry limits
```

## Integration Tests

Test:

```text
Webhook
 ↓
Database
 ↓
Agent
 ↓
Strategy
 ↓
Notification
```

## End-to-End Test

Simulate:

```text
Payment Failed
 ↓
Webhook received
 ↓
Agent analyzes
 ↓
Recovery strategy created
 ↓
Message sent
 ↓
Payment succeeds
 ↓
Captured webhook
 ↓
Recovery marked successful
```

---

# 42. Step 31 — Synthetic Demo

Your demo should contain multiple scenarios.

### Scenario A — High Probability

```text
Failure:
Network

Customer:
Returning customer

Probability:
91%

Action:
Retry

Result:
Recovered
```

### Scenario B — Insufficient Funds

```text
Failure:
Insufficient balance

Probability:
78%

Action:
Retry after 6 hours
```

### Scenario C — Repeated Failure

```text
Failures:
4

Probability:
14%

Action:
Stop automatic recovery
```

### Scenario D — High Value Customer

```text
Amount:
₹25,000

Probability:
67%

Action:
Human assistance
```

---

# 43. Step 32 — Logging

Every agent decision should be logged.

Example:

```text
2026-09-05 12:30:22
PAYMENT: pay_123

Failure:
network_failure

Probability:
0.87

Strategy:
retry_later

Channel:
whatsapp

Attempt:
1
```

Use structured logging where possible.

---

# 44. Step 33 — Monitoring

Monitor:

```text
Webhook failures
Agent errors
Prediction latency
Notification failures
Recovery rate
API latency
```

Important alerts:

```text
Webhook processing failure
Notification provider failure
Database failure
High prediction error
Abnormally low recovery rate
```

Razorpay states that webhook endpoints should return a 2XX response within 5 seconds; unsuccessful deliveries are retried with exponential backoff for up to 24 hours. Your webhook handler should therefore acknowledge quickly and move heavier processing to asynchronous/background processing where appropriate.

---

# 45. Step 34 — Idempotency

This is a critical production feature.

Suppose:

```text
payment.failed
```

is delivered twice.

Bad system:

```text
Attempt 1
Attempt 2
```

Correct system:

```text
Event ID already processed
        ↓
Ignore duplicate
```

Database:

```text
event_id UNIQUE
```

---

# 46. Step 35 — Recovery State Machine

Use states:

```text
FAILED
   ↓
ELIGIBLE
   ↓
ANALYZING
   ↓
STRATEGY_SELECTED
   ↓
SCHEDULED
   ↓
CONTACTED
   ↓
RETRY_PENDING
   ↓
RECOVERED
```

Failure path:

```text
FAILED
 ↓
ANALYZING
 ↓
NOT_RECOVERABLE
 ↓
CLOSED
```

---

# 47. Step 36 — Important Business Rules

Implement:

```text
MAX_ATTEMPTS = 3
```

Never repeatedly contact the customer.

Stop recovery when:

```text
payment captured
```

Stop when:

```text
maximum attempts reached
```

Stop when:

```text
customer opts out
```

Stop when:

```text
payment expires
```

Do not automatically retry failures where retrying is inappropriate.

---

# 48. Step 37 — AI + Rules Architecture

Do not allow the LLM to control the complete payment workflow.

Recommended:

```text
                Payment
                   ↓
              Rules Layer
                   ↓
            ML Prediction
                   ↓
          Strategy Engine
                   ↓
             LLM Layer
                   ↓
        Human-readable message
```

This is safer than:

```text
Payment
  ↓
LLM
  ↓
Do whatever LLM says
```

The LLM should primarily handle language and contextual reasoning.

The deterministic strategy engine should enforce business constraints.

---

# 49. Step 38 — Security

Implement:

```text
HTTPS
Webhook signature validation
Environment variables
Database access control
Input validation
Rate limiting
Authentication
Authorization
Structured logging
PII minimization
```

Never store:

```text
Card PIN
CVV
OTP
Passwords
Full sensitive payment credentials
```

---

# 50. Step 39 — Docker

Create:

```text
Dockerfile
```

The application should run with:

```text
docker build -t payment-recovery-agent .
```

Then:

```text
docker run -p 8000:8000 payment-recovery-agent
```

For local development:

```text
docker-compose up
```

Recommended services:

```text
API
Database
Worker
Redis
Frontend
```

---

# 51. Step 40 — Background Worker

Recovery actions should not block the webhook.

Architecture:

```text
Webhook
   ↓
Validate
   ↓
Save Event
   ↓
Queue Job
   ↓
Return 200
   ↓
Worker
   ↓
AI Agent
   ↓
Recovery Action
```

Possible tools:

```text
Celery
Redis
RQ
```

For a hackathon MVP, FastAPI background tasks can be enough.

---

# 52. Step 41 — Complete Runtime Flow

The final system should operate like this:

```text
                 CUSTOMER
                    │
                    ▼
              RAZORPAY PAYMENT
                    │
              ┌─────┴─────┐
              │           │
           SUCCESS      FAILURE
              │           │
              ▼           ▼
          Captured     Webhook
                          │
                          ▼
                    Event Processor
                          │
                          ▼
                    Failure Analyzer
                          │
                          ▼
                    Feature Engine
                          │
                          ▼
                   ML Prediction
                          │
                          ▼
                  Strategy Engine
                          │
                          ▼
                   Recovery Agent
                          │
                          ▼
                 Channel Selection
                          │
            ┌─────────────┼─────────────┐
            ▼             ▼             ▼
          SMS         WhatsApp        Email
            │             │             │
            └─────────────┼─────────────┘
                          ▼
                       CUSTOMER
                          │
                          ▼
                    PAYMENT RETRY
                          │
                          ▼
                       RAZORPAY
                          │
                          ▼
                  payment.captured
                          │
                          ▼
                  RECOVERY SUCCESS
                          │
                          ▼
                 Analytics Dashboard
```

---

# 53. Step 42 — Complete Build Order

Do NOT try to build everything simultaneously.

Follow this exact order.

## Phase 1 — Environment

```text
1. Install Python
2. Create virtual environment
3. Install dependencies
4. Create .env
```

## Phase 2 — Dataset

```text
5. Fix event_generator.py
6. Generate 1,000 events
7. Inspect JSONL
8. Validate fields
```

Command:

```cmd
python event_generator.py --count 1000 --seed 42 --output data/batch_001.jsonl
```

## Phase 3 — Database

```text
9. Create SQLAlchemy models
10. Create database
11. Import generated events
```

## Phase 4 — Backend

```text
12. Create FastAPI app
13. Add health endpoint
14. Add payment endpoints
15. Add webhook endpoint
```

## Phase 5 — Recovery Engine

```text
16. Failure analyzer
17. Feature engine
18. ML model
19. Strategy engine
```

## Phase 6 — AI

```text
20. Message generation
21. Agent orchestration
22. Guardrails
```

## Phase 7 — Notifications

```text
23. Mock SMS
24. Mock WhatsApp
25. Mock Email
```

## Phase 8 — Razorpay

```text
26. Test API integration
27. Configure Test Mode
28. Configure webhook
29. Test payment events
```

## Phase 9 — Dashboard

```text
30. Build analytics API
31. Build frontend
32. Add charts
33. Add payment detail page
34. Add agent decision page
```

## Phase 10 — Deployment

```text
35. Dockerize
36. Deploy backend
37. Deploy frontend
38. Configure HTTPS
39. Configure webhook
```

## Phase 11 — Testing

```text
40. Unit tests
41. Integration tests
42. End-to-end test
43. Failure scenarios
```

---

# 54. Minimum Viable Product

If you have limited time, build these features first:

```text
✓ Synthetic payment generator
✓ FastAPI backend
✓ SQLite database
✓ Payment failure webhook
✓ Failure classifier
✓ Recovery probability model
✓ Rule-based strategy engine
✓ AI message generator
✓ Mock notification service
✓ Recovery dashboard
✓ Recovery analytics
```

This is enough for a strong functional demo.

---

# 55. Advanced Version

After the MVP works, add:

```text
✓ LangGraph agent
✓ PostgreSQL
✓ Redis
✓ Celery
✓ Real notification provider
✓ Razorpay Payment Links
✓ Customer segmentation
✓ A/B testing
✓ Reinforcement learning
✓ Real-time dashboard
✓ Model monitoring
✓ Human-in-the-loop
```

---

# 56. Evaluation Metrics

Your final presentation should report:

## Technical Metrics

```text
Webhook processing latency
Prediction latency
API latency
System uptime
```

## ML Metrics

```text
Precision
Recall
F1
ROC-AUC
```

## Business Metrics

```text
Recovery Rate
Recovered Revenue
Average Recovery Time
Cost per Recovery
Attempts per Recovery
```

---

# 57. Key Success Metric

The most important metric is:

```text
Recovery Rate
```

Formula:

```text
Recovery Rate =
Recovered Failed Payments
--------------------------
Eligible Failed Payments
× 100
```

Revenue metric:

```text
Recovered Revenue =
Σ value of recovered payments
```

---

# 58. Example Final Results

After running the complete synthetic experiment, your dashboard could show:

```text
Total Transactions        10,000
Failed Transactions        1,850
Eligible Recoveries        1,600
Recovered Payments           720

Recovery Rate                45%
Recovered Revenue        ₹8.7 Lakh

Average Attempts              1.8
Average Recovery Time      5.4 hrs
```

Use your actual experimental results rather than these example numbers.

---

# 59. Demo Script

Your final demonstration should follow this story.

### Step 1

Show dashboard:

```text
10,000 transactions
1,850 failed
```

### Step 2

Select a failed payment:

```text
Payment:
pay_123

Amount:
₹2,499

Failure:
Network failure
```

### Step 3

Click:

```text
Analyze with AI
```

Show:

```text
Recovery Probability: 87%
```

### Step 4

Show reasoning:

```text
Returning customer
High historical success
Temporary failure type
Only one previous attempt
```

### Step 5

Show recommendation:

```text
Retry after 15 minutes
Channel: WhatsApp
Priority: High
```

### Step 6

Show AI-generated message.

### Step 7

Simulate payment success.

### Step 8

Send:

```text
payment.captured
```

### Step 9

Dashboard updates:

```text
Recovered Payments +1
Recovered Revenue +₹2,499
```

This creates a complete end-to-end story.

---

# 60. What Makes This an AI Agent?

Do not describe the project merely as:

> "An AI model that predicts failed payments."

The stronger description is:

> **An autonomous payment recovery agent that observes payment failures, understands the failure context, predicts recovery likelihood, chooses an appropriate recovery strategy, generates personalized communication, executes recovery actions, and learns from the resulting outcomes.**

The architecture contains:

```text
Observe
   ↓
Reason
   ↓
Decide
   ↓
Act
   ↓
Observe Outcome
   ↓
Improve
```

That is the agentic loop.

---

# 61. Final Architecture for Presentation

Use this simplified architecture in your PPT:

```text
              RAZORPAY
                  │
                  ▼
             WEBHOOKS
                  │
                  ▼
        ┌──────────────────┐
        │ EVENT PROCESSOR   │
        └────────┬─────────┘
                 │
                 ▼
        ┌──────────────────┐
        │ PAYMENT ANALYZER │
        └────────┬─────────┘
                 │
                 ▼
        ┌──────────────────┐
        │  ML PREDICTOR    │
        │ Recovery Score   │
        └────────┬─────────┘
                 │
                 ▼
        ┌──────────────────┐
        │ STRATEGY AGENT   │
        └────────┬─────────┘
                 │
                 ▼
        ┌──────────────────┐
        │  LLM AGENT       │
        │ Message Creation │
        └────────┬─────────┘
                 │
                 ▼
        ┌──────────────────┐
        │ NOTIFICATIONS    │
        └────────┬─────────┘
                 │
                 ▼
             CUSTOMER
                 │
                 ▼
             PAYMENT
                 │
                 ▼
             RAZORPAY
                 │
                 ▼
          RECOVERY RESULT
                 │
                 ▼
             ANALYTICS
```

---

# 62. Final Project Modules

Your finished project should contain these modules:

```text
1. Event Generator
2. Webhook Receiver
3. Event Processor
4. Payment Database
5. Failure Analyzer
6. Feature Engineering
7. Recovery Prediction Model
8. Customer Segmentation
9. Strategy Engine
10. AI Message Generator
11. Recovery Agent
12. Notification Service
13. Razorpay Integration
14. Recovery Scheduler
15. Analytics Engine
16. Dashboard
17. Monitoring
18. Security Layer
19. Testing Layer
```

---

# 63. Final Deliverables

At project completion, prepare:

```text
Source Code
│
├── Backend
├── Frontend
├── ML Model
├── Agent
├── Dataset Generator
├── Tests
└── Deployment Files
```

Documentation:

```text
README.md
Architecture Diagram
API Documentation
Database Schema
ML Documentation
Agent Documentation
Testing Report
Deployment Guide
```

Presentation:

```text
1. Problem
2. Existing Gap
3. Proposed Solution
4. Architecture
5. AI Agent
6. ML Prediction
7. Recovery Workflow
8. Dashboard
9. Results
10. Future Scope
```

---

# 64. Recommended Development Strategy

Build the project in **three milestones**.

## Milestone 1 — Working Backend

Target:

```text
Generator
+
Database
+
FastAPI
+
Webhook
+
Failure Analyzer
```

At this point you should be able to run:

```text
payment.failed
```

and see it stored and classified.

---

## Milestone 2 — Intelligent Recovery

Add:

```text
ML Predictor
+
Strategy Engine
+
AI Message Generator
+
Mock Notifications
```

At this point:

```text
payment.failed
       ↓
AI analysis
       ↓
Recovery decision
       ↓
Message
```

should work automatically.

---

## Milestone 3 — Production-Style Demo

Add:

```text
Razorpay Test Mode
+
Payment Links
+
Dashboard
+
Analytics
+
Docker
+
Webhook Security
```

Then demonstrate:

```text
FAILED PAYMENT
       ↓
AI RECOVERY
       ↓
CUSTOMER RETRIES
       ↓
PAYMENT SUCCESS
       ↓
RECOVERY DASHBOARD UPDATED
```

---

# 65. Final Definition of Done

The project is complete when the following scenario works automatically:

```text
1. Payment fails.

2. Razorpay webhook/event is received.

3. Event signature is validated.

4. Event is stored.

5. Failure reason is classified.

6. Customer/payment features are generated.

7. Recovery probability is predicted.

8. Recovery strategy is selected.

9. Appropriate channel is selected.

10. Personalized recovery message is generated.

11. Recovery action is scheduled/executed.

12. Customer retries payment.

13. Razorpay sends successful payment event.

14. System detects successful payment.

15. Future recovery attempts are cancelled.

16. Recovery attempt is marked successful.

17. Recovered revenue is calculated.

18. Dashboard updates.

19. Outcome is stored for future model improvement.
```

---

# 66. Final One-Line Project Description

> **An AI-powered autonomous payment recovery agent that transforms failed Razorpay transactions into intelligent, personalized, and measurable recovery opportunities.**

---

# 67. Official Razorpay References

For implementation, use Razorpay's official documentation for:

- Webhooks and event handling
- Payment events
- Payment Links
- Payment APIs
- Test Mode

Razorpay recommends webhooks as the primary mechanism for asynchronous automation and API verification as a supplement for critical immediate status checks.

[Razorpay Webhooks Documentation](https://razorpay.com/docs/webhooks/?utm_source=chatgpt.com)

[Razorpay Payment Webhook Events](https://razorpay.com/docs/webhooks/payments/?utm_source=chatgpt.com)

[Razorpay Payment Links API](https://razorpay.com/docs/api/payments/payment-links/?utm_source=chatgpt.com)

---

# 68. Immediate Next Step

From your current directory:

```text
D:\projects\razorpay\payment-recovery-agent\payment-recovery-agent\generator>
```

first run:

```cmd
python --version
```

Then:

```cmd
py --version
```

Then generate your first dataset with whichever Python command works:

```cmd
python event_generator.py --count 1000 --seed 42 --output data/batch_001.jsonl
```

or:

```cmd
py event_generator.py --count 1000 --seed 42 --output data/batch_001.jsonl
```

**Do not move to the ML/agent/dashboard stages until this generator successfully creates `batch_001.jsonl`.**

Once that works, the correct build sequence is:

```text
DATA GENERATOR
      ↓
DATABASE
      ↓
FASTAPI
      ↓
WEBHOOK
      ↓
FAILURE ANALYZER
      ↓
ML PREDICTOR
      ↓
STRATEGY ENGINE
      ↓
AI AGENT
      ↓
NOTIFICATIONS
      ↓
RAZORPAY TEST MODE
      ↓
DASHBOARD
      ↓
DOCKER
      ↓
DEPLOYMENT
```