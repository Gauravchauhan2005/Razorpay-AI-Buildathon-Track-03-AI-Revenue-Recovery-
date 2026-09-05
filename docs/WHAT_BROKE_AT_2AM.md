# 🌙 What Broke at 2 AM, and How We Got Out

> *"The bar for Razorpay AI Buildathon builders: Show your work, show honest metrics, tell us what broke at 2 AM, and how you got out."*

Building an autonomous AI agent that deals with real money, webhooks, and customer communication is fraught with subtle failure modes that only surface under pressure. Here is what broke during our development, and how we engineered our way out.

---

## 1. Incident 1: The 2:14 AM TRAI Regulatory Violation Trap

### 💥 What Broke
At 2:14 AM during overnight synthetic stress testing, a simulated payment of ₹4,999 failed due to an insufficient balance error (`INSUFFICIENT_FUNDS`). 

The raw agent pipeline immediately detected the failure, calculated a high recovery probability (82%), generated a personalized Hinglish WhatsApp message, and fired off an immediate recovery outreach at **02:15 AM**.

**The Disaster**:
1. **Legal & Regulatory Non-Compliance**: In India, TRAI (Telecom Regulatory Authority of India) and RBI guidelines strictly prohibit non-critical transactional and promotional commercial outreach between **9:00 PM and 9:00 AM IST**.
2. **Customer Churn**: Waking up a paying customer at 2 AM with a WhatsApp notification about a failed transaction causes rage, destroys merchant reputation, and guarantees permanent opt-out.

### 🛠️ How We Got Out: The `ComplianceGuard` Time-Lock Engine
We realized an autonomous agent in FinTech cannot operate on pure unconstrained triggers; it requires **regulatory time-locking**:
- Implemented `ComplianceGuard.get_ist_now()`, calculating Indian Standard Time (UTC+5:30).
- If an outreach attempt is evaluated between 21:00 and 09:00 IST, the outreach is **strictly held** and automatically rescheduled for **09:15 AM IST** next morning.
- The action is recorded in the **Audit Trail** as `QUIET_HOURS_RESCHEDULE`, guaranteeing zero 2 AM notifications while still winning back the revenue during daylight hours.

---

## 2. Incident 2: The LLM Hallucinating "20% Discount" Bribes

### 💥 What Broke
When we initially tested an end-to-end LLM-controlled recovery agent using an open-ended prompt (`"Convince the customer to complete their failed payment"`), the LLM began taking creative liberties to boost conversion:
```text
"Hi Rahul! Your payment of ₹2,499 failed. As a special apology, use coupon RECOVER20 
for an instant 20% discount on your retry! Tap here: https://..."
```
**The Disaster**:
The LLM literally invented an unauthorized discount out of thin air, eating the merchant’s gross margin. Worse, in other edge cases, LLMs have been known to ask users to verify their card details or CVV to "fix" the issue.

### 🛠️ How We Got Out: Hybrid AI Architecture + Negative Guardrails
We stripped the LLM of decision-making authority over financial terms:
1. **Deterministic Rule + ML Separation**: The ML model predicts $P(\text{Recovery})$; the deterministic Strategy Engine enforces allowed actions (`RETRY_NOW`, `RETRY_LATER`, `SEND_PAYMENT_LINK`, `ESCALATE_TO_HUMAN`).
2. **Guardrailed Messaging**:
   - The LLM receives strict negative constraints: `Do NOT request OTP/PIN/password. Do NOT invent discounts or refunds. Do NOT claim payment success.`
   - Hard template fallbacks exist for all failure categories and languages (**English**, **Hinglish**, **Hindi**).
   - If the LLM generates any prohibited phrase or exceeds bounds, it is dropped in favor of the certified template.

---

## 3. Incident 3: The Webhook Replay Storm & Duplicate Reminders

### 💥 What Broke
Razorpay's production webhook infrastructure guarantees **at-least-once delivery**. If our server took slightly more than 5 seconds to respond due to heavy ML model inference, Razorpay’s exponential backoff retry sent the exact same `payment.failed` event a second and third time.

Our asynchronous workers picked up both events, classified both, and dispatched **two identical WhatsApp reminders within 30 seconds** for the same failed transaction.

### 🛠️ How We Got Out: Database-Level Idempotency & State Locking
1. **Unique Event Key**: Enforced `event_id` as a unique index in the `events` table. If a duplicate event arrives, the handler returns `HTTP 200 {"status": "ok"}` immediately without re-triggering the pipeline.
2. **Atomic Recovery State Transitions**:
   $$\text{FAILED} \longrightarrow \text{ELIGIBLE} \longrightarrow \text{ANALYZING} \longrightarrow \text{CONTACTED} \longrightarrow \text{RECOVERED}$$
   Once an attempt is marked `contacted`, subsequent incoming triggers are debounced.
3. **Instant Cancellation on `payment.captured`**: The moment a customer pays via the payment link, Razorpay sends `payment.captured`. The webhook handler atomically halts all future pending retries and marks the recovery attempt as `fulfilled`.

---

## 4. Incident 4: The 20% Probability Money Pit (Spamming Unrecoverables)

### 💥 What Broke
Our first prototype attempted to recover *every* payment failure. When a customer repeatedly hit a hard bank fraud decline (`BANK_DECLINE`) or had 4 failed attempts in a row, the agent kept sending reminders.

Not only was the recovery rate on these near 0%, but the merchant incurred SMS/WhatsApp provider fees and annoyed frustrated users whose cards were blocked.

### 🛠️ How We Got Out: Bounded Stopping Rules
We established strict mathematical stopping thresholds:
1. **Probability Floor**: If $P(\text{Recovery}) < 0.20$, the agent takes `NO_ACTION` and transitions the payment to `closed`.
2. **Attempt Ceiling**: Hard cap of **3 lifetime attempts**.
3. **High-Value VIP Gate**: Any failed payment $\ge \text{₹}15,000$ or for high-value accounts skips automated bots and escalates directly to a Human Relationship Manager.

---

## 5. Summary: What We Learned

> **Real FinTech AI isn’t about letting an LLM run wild. It’s about building a robust, explainable state machine with strict compliance gates, deterministic money guards, and an unshakeable audit trail.**
