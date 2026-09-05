# 🎥 5-Minute Video Pitch Script & Demo Guide
### Razorpay AI Buildathon — Track 03: AI Revenue Recovery

Use this exact timing and script structure to record your 5-minute video presentation.

---

## ⏱️ Video Breakdown

| Timestamp | Section | Visual on Screen | Key Talking Points |
|---|---|---|---|
| **0:00 – 0:45** | **The Problem** | Slide or Razorpay checkout screen with failed payment | How merchants lose 18–22% of revenue to failed payments & checkout abandonment; why traditional blind retries destroy customer trust and fail. |
| **0:45 – 1:45** | **The Architecture** | Architecture diagram from README | The autonomous agent loop: Webhook Ingestion -> Failure Analysis -> ML Probability Predictor -> Compliance Stopping Guard -> Hinglish Message Generator. |
| **1:45 – 3:00** | **Live Interactive Demo** | Streamlit UI (`http://localhost:8501`) Tab 2 | Select a failed payment (`pay_439902`). Show AI analysis, Hinglish WhatsApp draft, and dispatch. Then trigger `payment.captured` and show real-time recovery. |
| **3:00 – 4:00** | **The Proof: Batch Benchmark** | Streamlit UI Tab 3 & Terminal (`python scripts/batch_benchmark.py`) | Run the live benchmark across 100 failed transactions: show **₹6.24 Lakh recovered out of ₹9.19 Lakh at risk (67.9% net yield)**, and explain stopping rules. |
| **4:00 – 4:45** | **What Broke at 2 AM** | Streamlit Tab 4 (Audit Trail) & Code Snippet | Share the TRAI quiet hours incident at 2 AM and how `ComplianceGuard` was engineered; explain the prevention of fake discount hallucinations. |
| **4:45 – 5:00** | **Closing & Impact** | Executive KPI Overview (Tab 1) | Reiterate the value: measurable recovered revenue, regulatory compliance, zero spam, and high conversion through localized Hinglish messaging. |

---

## 🗣️ Second-by-Second Script

### [0:00 - 0:45] The Hook & The Problem
> *"Hi, I'm presenting our project for the Razorpay AI Buildathon Track 03: AI Revenue Recovery.*  
> *Every single day, Indian merchants lose between 15 to 25 percent of their revenue to failed transactions—from UPI server timeouts and insufficient balances to authentication drops.*  
> *Traditional systems treat all failures identically: either they do nothing, or they bombard customers with blind SMS retries that feel like spam and have less than a 5 percent conversion rate.*  
> *We asked: What if an AI agent understood why the payment failed, predicted whether it’s recoverable, respected Indian compliance quiet hours, and spoke to the customer in natural Hinglish?"*

### [0:45 - 1:45] The Architecture & System Design
> *(Switch screen to Architecture Diagram)*  
> *"Here is how our autonomous recovery agent works.*  
> *When a transaction degrades, our FastAPI webhook receiver ingests the Razorpay event with full HMAC-SHA256 signature verification and idempotency.*  
> *The event is parsed by our Failure Analyzer, which classifies the root cause—such as network failure, bank decline, or insufficient funds.*  
> *Our Feature Engineering pipeline extracts 11 behavioral features, and our trained GradientBoosting model predicts the exact recovery probability.*  
> *Next, our Compliance Guard evaluates strict business rules: Is it between 9 PM and 9 AM IST? If so, TRAI quiet hours apply, and outreach is held until 9:15 AM next morning.*  
> *If cleared, our Message Agent generates localized, empathetic outreach in English, Hinglish, or Hindi with zero hallucination guardrails."*

### [1:45 - 3:00] Live Interactive Demo
> *(Switch screen to Streamlit UI: `http://localhost:8501` - Tab 2)*  
> *"Let's see this live in our Streamlit dashboard.*  
> *In Tab 2, I can pick a real failed transaction from our database. Let’s pick `pay_439902`, an authentication failure.*  
> *I select 'Hinglish' outreach and click 'Analyze with AI Agent'.*  
> *Instantly, the agent inspects the customer segment, transaction history, and failure context.*  
> *Look at the rationale: it recognizes the temporary failure, predicts a 62.9% recovery score, and drafts a polite, conversational Hinglish message with a secure payment link.*  
> *Now I click 'Dispatch Recovery Action'. The notification is sent via WhatsApp, attempt number 1 is logged, and the state becomes 'contacted'.*  
> *If the customer says 'I’ll pay after office hours', we can log a Promise-to-Pay for 6 hours, pausing retries.*  
> *And the moment the customer completes payment, Razorpay’s `payment.captured` webhook halts all future retries and credits the recovered revenue in real-time."*

### [3:00 - 4:00] The Proof: Batch Recovery Benchmark
> *(Switch screen to Tab 3 or Terminal)*  
> *"The Buildathon bar states: Don't just identify the problem. Show measured money recovered across a batch.*  
> *Here in Tab 3—and via our CLI benchmark script—we evaluate a held-out test batch of 100 failed transactions.*  
> *Watch this: across ₹9.19 Lakh of revenue at risk, our agent dispatched 62 bounded interventions, safely stopped 34 unrecoverable cases to prevent merchant fee waste, and successfully recovered ₹6.24 Lakh—achieving a 67.9% net revenue recovery rate.*  
> *Every single action, confidence score, and policy check is permanently recorded in our immutable audit trail in Tab 4."*

### [4:00 - 4:45] What Broke at 2 AM
> *(Switch screen to Tab 4 or `docs/WHAT_BROKE_AT_2AM.md`)*  
> *"Now, what broke at 2 AM during development?*  
> *At 2:14 AM during overnight testing, an insufficient balance failure occurred. The unconstrained agent immediately fired off an outreach message at 2:15 AM.*  
> *That’s a direct violation of TRAI quiet hours in India, which prohibit commercial communication between 9 PM and 9 AM IST.*  
> *We engineered our way out by building `ComplianceGuard`, which calculates IST time and enforces an automated quiet-hours hold until 9:15 AM next morning.*  
> *Similarly, when early LLM prompts hallucinated fake 20% discount coupons to bribe customers, we decoupled financial logic into a deterministic state engine with strict negative guardrails."*

### [4:45 - 5:00] Conclusion
> *"In summary, our AI Revenue Recovery Agent is bounded, compliant, localized for Indian FinTech, and backed by measurable batch proof. Thank you!"*
