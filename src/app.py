import streamlit as st
from ui.blower_properties import blower_dimensions_input
from ui.sim_properties import sim_parameters
from ui.measurement_points import measurement_points_input
from ui.plot import run_animation
from models.session import SessionModel

st.set_page_config(layout="wide", page_title="VibeCheck - Vibration Simulator")
session = st.session_state.get("session")
if session is None:
    session = SessionModel()
    st.session_state["session"] = session

with st.sidebar:
    st.header("Simulation Setup")
    blower_dimensions_input(session)
    sim_parameters(session)
    measurement_points_input(session)


run_animation(session)