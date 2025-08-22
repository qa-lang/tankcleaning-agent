
# main.py (snippet)



Python
# Diagnostics (remove after you fix things)
import os, sys, platform, importlib, time
from pathlib import Path

with st.expander("🔎 Debug panel (temporary)", expanded=False):
    st.write({
        "python": sys.version,
        "platform": platform.platform(),
        "cwd": str(Path.cwd()),
        "streamlit": st.__version__,
        "has_OPENAI_API_KEY": bool(os.getenv("OPENAI_API_KEY") or st.secrets.get("OPENAI_API_KEY")),
        "time": time.strftime("%Y-%m-%d %H:%M:%S"),
    })
    for pkg in ["langchain","openai","faiss-cpu","chromadb","pandas","pydantic"]:
        try:
            m = importlib.import_module(pkg.replace("-", "_"))
            st.write(pkg, getattr(m, "__version__", "installed"))
        except Exception as e:
            st.write(pkg, "NOT INSTALLED:", e)


Visa mindre

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
