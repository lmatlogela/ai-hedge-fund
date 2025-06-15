import streamlit as st
from datetime import datetime
from main import run_hedge_fund, ANALYST_ORDER, LLM_ORDER  # Adjust if needed

# --- Glassmorphism background & styles ---
def add_bg_from_url():
    st.markdown(
        f"""
        <style>
        .stApp {{
            background: linear-gradient(120deg, #0a1429cc 0%, #203568cc 100%),
                        url("https://images.unsplash.com/photo-1506744038136-46273834b3fb?auto=format&fit=crop&w=1350&q=80");
            background-size: cover;
            background-attachment: fixed;
        }}
        .block-container {{
            background: rgba(24, 27, 48, 0.7);
            border-radius: 22px;
            box-shadow: 0 8px 32px 0 #181b30cc;
            backdrop-filter: blur(14px);
        }}
        </style>
        """,
        unsafe_allow_html=True
    )
add_bg_from_url()

# --- Header ---
st.markdown("""
<div style='text-align: center;'>
    <h1 style='font-size: 3.2rem; letter-spacing: 2px; background: linear-gradient(90deg,#0fffc1,#7e48ff 70%,#ffa9f9); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-weight:900; margin-bottom:0;'>
        AI Hedge Fund <span style="font-size:1.8rem;">2025</span>
    </h1>
    <span style="font-size:1.2rem; color:#b3b8ff;">
        Next-gen AI-powered investment simulation platform
    </span>
</div>
""", unsafe_allow_html=True)
st.markdown("---")

with st.container():
    col1, col2 = st.columns([2, 1])
    with col1:
        tickers = st.text_input(
            "Enter Stock Tickers (comma-separated)",
            value="AAPL,GOOG,MSFT,NVDA,TSLA",
            help="e.g. AAPL,MSFT,NVDA"
        )
    with col2:
        initial_cash = st.number_input(
            "Initial Cash ($)",
            value=100_000,
            min_value=1_000,
            step=1_000,
            format="%i"
        )

    date1, date2 = st.columns(2)
    with date1:
        start_date = st.date_input("Start Date", datetime(2024, 1, 1))
    with date2:
        end_date = st.date_input("End Date", datetime.today())

    st.markdown("---")
    # --- Analysts Section ---
    st.subheader("Select Your Virtual Investment Team 👨‍💼👩‍💼")
    analyst_options = [display for display, value in ANALYST_ORDER]
    default_analysts = analyst_options[:2] if len(analyst_options) >= 2 else analyst_options
    selected_analysts = st.multiselect(
        "AI Analysts",
        analyst_options,
        default=default_analysts
    )

    st.markdown("---")
    # --- LLM Model Selection ---
    st.subheader("Choose Your LLM Engine 🤖")
    llm_models = [f"{name} ({provider})" for display, name, provider in LLM_ORDER]
    model_name = st.selectbox("Select LLM Model", llm_models, index=0)

    # --- Margin, Reasoning, and Graph Toggles ---
    margin, reasoning, show_graph = st.columns(3)
    with margin:
        margin_requirement = st.number_input(
            "Margin Requirement (%)", value=0, min_value=0, max_value=100, step=1
        )
    with reasoning:
        show_reasoning = st.toggle("Show Reasoning", value=True)
    with show_graph:
        show_agent_graph = st.toggle("Show Agent Graph", value=False)

    st.markdown("---")
    # --- Run Button ---
    run_btn = st.button("🚀 Run AI Hedge Fund", use_container_width=True)
    st.markdown("## Results")
    results_placeholder = st.empty()

    # --- Run hedge fund simulation ---
    if run_btn:
        with st.spinner("Simulating trading decisions with your AI team..."):
            tickers_list = [t.strip() for t in tickers.split(",") if t.strip()]
            # Setup portfolio structure (match your backend's requirements)
            portfolio = {
                "cash": initial_cash,
                "margin_requirement": margin_requirement,
                "margin_used": 0,
                "positions": {t: {
                    "long": 0, "short": 0, "long_cost_basis": 0.0,
                    "short_cost_basis": 0.0, "short_margin_used": 0.0
                } for t in tickers_list},
                "realized_gains": {t: {"long": 0.0, "short": 0.0} for t in tickers_list}
            }
            try:
                # Parse model choice
                model_name_only, model_provider = model_name.split(" (")
                model_provider = model_provider.replace(")", "")
                # Call your actual logic
                result = run_hedge_fund(
                    tickers=tickers_list,
                    start_date=start_date.strftime("%Y-%m-%d"),
                    end_date=end_date.strftime("%Y-%m-%d"),
                    portfolio=portfolio,
                    show_reasoning=show_reasoning,
                    selected_analysts=selected_analysts,
                    model_name=model_name_only,
                    model_provider=model_provider,
                )
                st.success("Simulation complete!")
                results_placeholder.write(result)
            except Exception as e:
                st.error(f"Error running AI Hedge Fund: {e}")

st.markdown("""
<style>
/* Futuristic field and button styling */
input, select, button, textarea, .stButton > button {
    border-radius: 18px !important;
    border: 1.5px solid #7e48ff !important;
    background: rgba(12, 19, 36, 0.86) !important;
    color: #c7f7f4 !important;
    font-weight: 600 !important;
    font-size: 1.05rem !important;
    box-shadow: 0 4px 24px #1d1835c2 !important;
}
.stButton > button {
    font-size: 1.18rem !important;
    background: linear-gradient(92deg,#7e48ff 0%,#0fffc1 100%) !important;
    color: #232646 !important;
    font-weight: 700 !important;
    transition: all 0.2s;
}
.stButton > button:hover {
    transform: translateY(-2px) scale(1.04);
    background: linear-gradient(92deg,#0fffc1 0%,#7e48ff 100%) !important;
    color: #1a213a !important;
}
</style>
""", unsafe_allow_html=True)
