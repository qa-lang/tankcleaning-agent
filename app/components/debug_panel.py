
# app/components/debug_panel.py
import os, sys, platform, importlib, time
from pathlib import Path
import streamlit as st

def render_debug_panel(expanded: bool = False):
    """Temporary diagnostics panel. Remove once the app is stable."""
    with st.expander("🔎 Debug panel (temporary)", expanded=expanded):
        st.write({
            "python": sys.version,
            "platform": platform.platform(),
            "cwd": str(Path.cwd()),
            "streamlit": st.__version__,
            "has_OPENAI_API_KEY": bool(os.getenv("OPENAI_API_KEY") or st.secrets.get("OPENAI_API_KEY")),
            "has_AZURE_OPENAI_API_KEY": bool(os.getenv("AZURE_OPENAI_API_KEY") or st.secrets.get("AZURE_OPENAI_API_KEY")),
            "time": time.strftime("%Y-%m-%d %H:%M:%S"),
        })
        for pkg in ["langchain","openai","faiss-cpu","chromadb","pandas","pydantic"]:
            try:
                m = importlib.import_module(pkg.replace("-", "_"))
                st.write(pkg, getattr(m, "__version__", "installed"))
            except Exception as e:
                st.write(pkg, "NOT INSTALLED:", e)
