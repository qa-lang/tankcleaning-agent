
# main.py (snippet)

import streamlit as st
from data_loader import load_transitions
from logic import find_transition
from utils import format_transition_row

st.title("Tank Cleaning Guidance Agent")

transitions = load_transitions()


# main.py (add after loading transitions)
prev_options = sorted(set(transitions["Previous_Cargo"].dropna().unique()))
next_options = sorted(set(transitions["Next_Cargo"].dropna().unique()))

col1, col2 = st.columns(2)
with col1:
    prev_cargo = st.selectbox("Previous Cargo", options=prev_options, index=0 if prev_options else None)
with col2:
    next_cargo = st.selectbox("Next Cargo", options=next_options, index=0 if next_options else None)


# Debug/visibility (optional – remove later)
with st.expander("Preview loaded transitions (first 10)"):
    st.dataframe(transitions.head(10))

prev_cargo = st.text_input("Previous Cargo", "Base Oil")
next_cargo = st.text_input("Next Cargo", "Jet Fuel")
...

import os, streamlit as st
OPENAI_KEY = os.getenv("OPENAI_API_KEY") or st.secrets.get("OPENAI_API_KEY")
if not OPENAI_KEY:
    st.error("Missing OPENAI_API_KEY in Secrets or env. Go to Manage app → Settings → Secrets.")
    st.stop()




Python
# app/main.py
from pathlib import Path
import os
import streamlit as st

# 🧭 Page config (kept minimal; adjust as you like)
st.set_page_config(page_title="Tank Cleaning Guidance Agent", layout="wide")

# 🔧 Diagnostics (temporary)
from app.components.debug_panel import render_debug_panel
render_debug_panel(expanded=False)

# 🔐 Secrets sanity check (OpenAI or Azure OpenAI)
OPENAI_KEY = os.getenv("OPENAI_API_KEY") or st.secrets.get("OPENAI_API_KEY")
AZURE_KEY  = os.getenv("AZURE_OPENAI_API_KEY") or st.secrets.get("AZURE_OPENAI_API_KEY")
if not (OPENAI_KEY or AZURE_KEY):
    st.info(
        "No OpenAI/Azure OpenAI key found. "
        "On Streamlit Cloud, set secrets via **Manage app → Settings → Secrets**.\n\n"
        "Expected keys: `OPENAI_API_KEY` or `AZURE_OPENAI_API_KEY` (+ endpoint/deployment)."
    )

st.title("Tank Cleaning Guidance Agent")

# ── UI ──────────────────────────────────────────────────────────────────────────
with st.form("transition_form", clear_on_submit=False):
    prev_cargo = st.selectbox(
        "Previous Cargo",
        ["Base", "AGO, GO, GTL", "MS", "ULSD", "Jet Fuel"],
        index=1,
    )
    next_cargo = st.selectbox(
        "Next Cargo",
        ["Jet Fuel", "Aut, Gsoln, DMA", "ULSD", "MS", "Base"],
        index=0,
    )
    # ✅ CRITICAL: forms submit only via a submit button inside the form
    generate = st.form_submit_button("Generate cleaning plan")

# ── ACTION ─────────────────────────────────────────────────────────────────────
def _run_agent(prev: str, nxt: str):
    """Call your existing agent/chain here; raise on error."""
    # TODO: replace this import/adapter with your actual agent call.
    # Example:
    # from app.agent import generate_cleaning_plan
    # return generate_cleaning_plan(prev, nxt)
    from app.agent import generate_cleaning_plan  # adjust if module differs
    return generate_cleaning_plan(prev, nxt)

if generate:
    with st.status("Working…", expanded=True) as status:
        st.write({"previous": prev_cargo, "next": next_cargo})
        try:
            plan = _run_agent(prev_cargo, next_cargo)
        except Exception as e:
            st.exception(e)  # 👈 show real error instead of failing silently
            status.update(state="error", label="Failed")
            st.stop()
        status.update(state="complete", label="Done")

    if plan:
        st.markdown(plan)
    else:
        st.warning("No plan returned by the agent. Check logs and inputs.")



