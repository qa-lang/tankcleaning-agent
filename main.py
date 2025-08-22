
# main.py (snippet)
import streamlit as st
from data_loader import load_transitions
from logic import find_transition
from utils import format_transition_row

st.title("Tank Cleaning Guidance Agent")

transitions = load_transitions()

# Debug/visibility (optional – remove later)
with st.expander("Preview loaded transitions (first 10)"):
    st.dataframe(transitions.head(10))

prev_cargo = st.text_input("Previous Cargo", "Base Oil")
next_cargo = st.text_input("Next Cargo", "Jet Fuel")
...
