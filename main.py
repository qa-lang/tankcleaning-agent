
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
