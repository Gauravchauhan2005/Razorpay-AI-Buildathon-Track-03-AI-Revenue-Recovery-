"""
Streamlit dashboard for Razorpay AI Revenue Recovery Agent.
Track 03: AI Revenue Recovery — Razorpay AI Buildathon
"""
import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
from typing import Dict, Any, Optional
import os

API_BASE_URL = os.getenv("API_BASE_URL", "http://127.0.0.1:8000")

st.set_page_config(
    page_title="Razorpay AI Revenue Recovery Agent",
    page_icon="💳",
    layout="wide",
    initial_sidebar_state="expanded"
)

@st.cache_data(ttl=10)
def fetch_api(endpoint: str) -> Optional[Any]:
    """Fetch data from the API endpoint."""
    try:
        response = requests.get(f"{API_BASE_URL}{endpoint}", timeout=5)
        response.raise_for_status()
        return response.json()
    except Exception:
        return None

def main() -> None:
    """Main dashboard entrypoint."""
    st.title("💳 Razorpay AI Revenue Recovery Agent")
    st.markdown(
        "**Track 03: AI Revenue Recovery** · *Autonomous, compliant, and explainable payment recovery pipeline*"
    )

    overview = fetch_api("/api/v1/analytics/overview")
    if not overview:
        st.warning(f"⚠️ Backend API is unreachable at `{API_BASE_URL}`. Please start the FastAPI backend.")
        st.code("python -m uvicorn app.main:app --port 8000", language="bash")
        return

    # Top KPI Banner
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.metric("Total Payments", f"{overview.get('total_payments', 0):,}")
    with col2:
        st.metric("Failed Payments", f"{overview.get('failed_payments', 0):,}")
    with col3:
        st.metric("Recovered Payments", f"{overview.get('recovered_payments', 0):,}")
    with col4:
        rate = overview.get("recovery_rate", 0.0)
        color = "#28a745" if rate > 40 else "#fd7e14" if rate > 20 else "#dc3545"
        st.markdown(f"**Recovery Rate**<br><span style='color:{color}; font-size:26px; font-weight:bold;'>{rate:.1f}%</span>", unsafe_allow_html=True)
    with col5:
        rev = overview.get("revenue_recovered", 0)
        st.metric("Recovered Revenue", f"₹{rev/100000:.2f} Lakh" if rev >= 100000 else f"₹{rev:,.0f}")

    st.markdown("---")

    # Main Navigation Tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 Overview & Analytics",
        "⚡ Interactive AI Recovery Sandbox",
        "🏆 Batch Recovery Benchmark",
        "📋 Compliance & Audit Trail",
        "🤝 Promise-to-Pay & Escalations"
    ])

    # =========================================================================
    # TAB 1: OVERVIEW & ANALYTICS
    # =========================================================================
    with tab1:
        failures = fetch_api("/api/v1/analytics/failures")
        channels = fetch_api("/api/v1/analytics/channels")
        revenue = fetch_api("/api/v1/analytics/revenue")
        decisions = fetch_api("/api/v1/analytics/decisions")

        c1, c2 = st.columns(2)
        with c1:
            st.subheader("Payment Failure Distribution")
            if failures:
                df_fail = pd.DataFrame(failures)
                if not df_fail.empty:
                    fig = px.pie(
                        df_fail, 
                        values='count', 
                        names='reason', 
                        title='Root Causes of Payment Degradation',
                        hole=0.4,
                        color_discrete_sequence=px.colors.qualitative.Bold
                    )
                    st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No failure data available.")

        with c2:
            st.subheader("Recovery Channel Effectiveness")
            if channels:
                df_chan = pd.DataFrame(channels)
                if not df_chan.empty:
                    fig = px.bar(
                        df_chan, 
                        x='channel', 
                        y=['attempts', 'recovered'], 
                        barmode='group', 
                        title='Outreach Attempts vs Successful Recoveries', 
                        color_discrete_sequence=['#4361ee', '#2ec4b6']
                    )
                    st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No channel data available.")

        # Revenue Metrics
        st.markdown("---")
        st.subheader("Revenue Recovery Performance")
        if revenue:
            r1, r2, r3 = st.columns(3)
            failed_rev = revenue.get('total_failed_revenue', 0)
            rec_rev = revenue.get('recovered_revenue', 0)
            rec_pct = revenue.get('recovery_rate', 0)
            
            r1.metric("Total Failed Revenue at Risk", f"₹{failed_rev/100000:.2f} Lakh" if failed_rev >= 100000 else f"₹{failed_rev:,.0f}")
            r2.metric("Total Money Recovered", f"₹{rec_rev/100000:.2f} Lakh" if rec_rev >= 100000 else f"₹{rec_rev:,.0f}")
            r3.metric("Net Recovery Yield", f"{rec_pct:.1f}%")

        # Recent Decisions
        st.markdown("---")
        st.subheader("Recent Autonomous Recovery Decisions")
        if decisions:
            df_dec = pd.DataFrame(decisions)
            if not df_dec.empty:
                st.dataframe(df_dec, use_container_width=True)

    # =========================================================================
    # TAB 2: INTERACTIVE AI RECOVERY SANDBOX
    # =========================================================================
    with tab2:
        st.subheader("Interactive AI Recovery Engine")
        st.markdown(
            "Test how the agent analyzes failures, evaluates stopping rules, generates Hinglish/English communication, "
            "and dispatches compliant recovery actions."
        )

        sample_payments = fetch_api("/api/v1/payments?status=failed&limit=15") or []
        sample_ids = [p["payment_id"] for p in sample_payments] if sample_payments else []
        
        col_sel, col_lang = st.columns([3, 1])
        with col_sel:
            selected_id = st.selectbox(
                "Select a failed transaction to test:",
                ["-- Choose a payment --"] + sample_ids if sample_ids else ["-- No failed payments --"]
            )
        with col_lang:
            lang = st.selectbox("Outreach Language:", ["hinglish", "english", "hindi"], index=0)

        custom_id = st.text_input("Or enter specific Payment ID:", value="" if selected_id.startswith("--") else selected_id)

        c_eval, c_act = st.columns(2)

        with c_eval:
            st.markdown("### 1. Observe & Reason (AI Decision Engine)")
            if st.button("🔍 Run AI Failure & Policy Analysis", type="primary"):
                if custom_id:
                    with st.spinner("Analyzing failure root cause, ML probability & TRAI/RBI compliance gates..."):
                        resp = requests.post(f"{API_BASE_URL}/api/v1/recovery/agent/analyze/{custom_id}?language={lang}")
                        if resp.status_code == 200:
                            dec = resp.json()
                            st.success("✅ Analysis & Policy Check Complete!")
                            
                            prob = dec.get("recovery_probability", 0)
                            color_p = "green" if prob >= 0.7 else "orange" if prob >= 0.3 else "red"
                            st.markdown(f"#### Recovery Probability: <span style='color:{color_p}; font-size:24px;'>{prob*100:.1f}%</span>", unsafe_allow_html=True)

                            col_d1, col_d2 = st.columns(2)
                            with col_d1:
                                st.write(f"**Failure Category:** `{dec.get('failure_category')}`")
                                st.write(f"**Action Recommended:** `{dec.get('recommended_action')}`")
                                st.write(f"**Priority:** `{dec.get('priority').upper()}`")
                            with col_d2:
                                st.write(f"**Optimal Channel:** `{dec.get('channel').upper()}`")
                                st.write(f"**Delay:** `{dec.get('retry_after_minutes')} mins`")
                                st.write(f"**Language:** `{lang.upper()}`")

                            st.info(f"💡 **Policy Rationale:** {dec.get('reason')}")

                            if dec.get("message"):
                                st.markdown("##### ✉️ Guardrailed Communication Draft:")
                                st.code(dec.get("message"), language="text")
                        else:
                            st.error(f"Error {resp.status_code}: {resp.text}")

        with c_act:
            st.markdown("### 2. Act, Track & Intervene")
            col_b1, col_b2 = st.columns(2)
            with col_b1:
                if st.button("🚀 Dispatch Recovery Action", type="secondary"):
                    if custom_id:
                        with st.spinner("Dispatching bounded notification and updating audit trail..."):
                            resp = requests.post(f"{API_BASE_URL}/api/v1/recovery/agent/recover/{custom_id}?language={lang}")
                            if resp.status_code == 200:
                                res = resp.json()
                                if res.get("status") == "recovery_executed":
                                    st.success(f"🎉 Intervention Dispatched via {res.get('channel', '').upper()}!")
                                    st.write(f"**Attempt Number:** {res.get('attempt_number')}")
                                    if res.get("message"):
                                        st.code(res.get("message"), language="text")
                                else:
                                    st.warning(f"Outreach Bounded / Halted: {res.get('reason')}")
                            else:
                                st.error(f"Error {resp.status_code}: {resp.text}")
            with col_b2:
                ptp_delay = st.number_input("Customer promised delay (hours):", min_value=1, max_value=72, value=6)
                if st.button("🤝 Log Promise-to-Pay"):
                    if custom_id:
                        resp = requests.post(
                            f"{API_BASE_URL}/api/v1/recovery/{custom_id}/promise-to-pay",
                            json={"promised_hours_delay": ptp_delay}
                        )
                        if resp.status_code == 200:
                            st.success(f"Promise-to-Pay logged! Outreach paused for {ptp_delay}h.")
                        else:
                            st.error(f"Error: {resp.text}")

    # =========================================================================
    # TAB 3: BATCH RECOVERY BENCHMARK
    # =========================================================================
    with tab3:
        st.subheader("🏆 Razorpay Buildathon — Batch Recovery Evaluation Bench")
        st.markdown(
            "> *\"Don’t just identify the problem. Show measured money recovered across a batch, with compliant escalation, stopping rules, and an audit trail.\"*"
        )

        b_col1, b_col2 = st.columns([1, 2])
        with b_col1:
            batch_sz = st.slider("Select Evaluation Batch Size:", min_value=10, max_value=150, value=50, step=10)
            run_btn = st.button("▶️ Run Autonomous Batch Benchmark", type="primary")

        if run_btn:
            with st.spinner(f"Evaluating {batch_sz} failed transactions through agent pipeline..."):
                resp = requests.post(f"{API_BASE_URL}/api/v1/analytics/benchmark-batch?batch_size={batch_sz}", timeout=30)
                if resp.status_code == 200:
                    data = resp.json()
                    st.success("✅ Batch Benchmark Run Finished!")

                    # Benchmark metrics
                    m1, m2, m3, m4 = st.columns(4)
                    m1.metric("Batch Evaluated", f"{data['batch_size_evaluated']} payments")
                    m2.metric("Revenue at Risk", f"₹{data['total_revenue_at_risk']:,.0f}")
                    m3.metric("Measured Money Recovered", f"₹{data['revenue_recovered']:,.0f}")
                    m4.metric("Net Recovery Yield", f"{data['recovery_rate_percentage']}%")

                    st.markdown("---")
                    col_det1, col_det2, col_det3 = st.columns(3)
                    with col_det1:
                        st.info(f"📤 **Interventions Dispatched:** {data['interventions_dispatched']}")
                    with col_det2:
                        st.warning(f"⛔ **Ineligible Retries Stopped:** {data['stopped_by_policy']}")
                    with col_det3:
                        st.error(f"👤 **VIP Cases Escalated:** {data['escalated_to_human']}")

                    st.markdown(f"**Executive Summary:** {data['summary']}")
                else:
                    st.error(f"Benchmark error: {resp.text}")

    # =========================================================================
    # TAB 4: COMPLIANCE & AUDIT TRAIL
    # =========================================================================
    with tab4:
        st.subheader("📋 Immutable Audit Trail & Governance")
        st.markdown("Every decision, model score, policy gate, and message dispatch is recorded in an immutable audit ledger.")

        audit_data = fetch_api("/api/v1/analytics/audit-trail?limit=50")
        if audit_data and "records" in audit_data:
            st.write(f"Total Logged Events: **{audit_data.get('total_records', 0)}**")
            df_audit = pd.DataFrame(audit_data["records"])
            if not df_audit.empty:
                st.dataframe(df_audit, use_container_width=True)
            else:
                st.info("No audit logs recorded yet. Run analysis or batch benchmark to generate audit events.")
        else:
            st.info("Audit trail loading...")

    # =========================================================================
    # TAB 5: PROMISE-TO-PAY & ESCALATIONS
    # =========================================================================
    with tab5:
        st.subheader("🤝 Promise-to-Pay Commitments & VIP Escalations")
        st.markdown("Monitor customers who committed to pay at a future time, and high-value accounts routed for human assistance.")

        ptp_data = fetch_api("/api/v1/analytics/ptp") or []
        if ptp_data:
            df_ptp = pd.DataFrame(ptp_data)
            st.markdown("### Active Promise-to-Pay Tracker")
            st.dataframe(df_ptp, use_container_width=True)
        else:
            st.info("No active Promise-to-Pay records found. You can log one in Tab 2.")

        st.markdown("### High-Value Concierge Escalation Queue")
        escalated_payments = fetch_api("/api/v1/payments?status=failed&limit=50") or []
        vip_list = [p for p in escalated_payments if p.get("recovery_status") == "escalated" or float(p.get("amount", 0)) >= 15000]
        if vip_list:
            df_vip = pd.DataFrame(vip_list)[["payment_id", "customer_id", "amount", "currency", "failure_reason", "recovery_status"]]
            st.dataframe(df_vip, use_container_width=True)
        else:
            st.info("No payments currently in escalation queue.")

if __name__ == "__main__":
    main()
