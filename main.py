
import streamlit as st

from data_loader import load_transitions
from logic import find_transition
from utils import format_transition_row


st.title("Tank Cleaning Guidance Agent")

transitions = load_transitions()
prev_cargo = st.text_input("Previous Cargo", "Base Oil")
next_cargo = st.text_input("Next Cargo", "Jet Fuel")

if st.button("Get Cleaning Guidance"):
    row = find_transition(transitions, prev_cargo, next_cargo)
    st.markdown(format_transition_row(row))
