import streamlit as st
from pathlib import Path
import os
from google.cloud import firestore
from google.oauth2 import service_account
from ui.blower_properties import blower_dimensions_input
from ui.sim_properties import sim_parameters
from ui.measurement_points import measurement_points_input
from ui.plot import run_animation
from ui.load_session import sim_explorer_ui
from models.session import SessionModel

from google.oauth2 import service_account
from google.cloud import firestore
import streamlit as st

ICON_PATH = (Path(__file__).parent / "assets" / "sound-wave-svgrepo-com.svg").resolve()
st.set_page_config(
    layout="wide",
    page_title="Vibe Check",
    page_icon=str(ICON_PATH)
)

svg_markup = Path(ICON_PATH).read_text(encoding="utf-8")
col1, col2 = st.columns([1, 12])
with col1:
    st.image(str(ICON_PATH), width=100)
with col2:
    st.markdown("<h1 style='margin:0;'>Vibe Check</h1>", unsafe_allow_html=True)

session = st.session_state.get("session")
if session is None:
    session = SessionModel()
    st.session_state["session"] = session

with st.sidebar:
    st.header("Simulation Explorer")
    sim_explorer_ui()
    
    st.divider()
    st.header("Simulation Setup")
    blower_dimensions_input(session)
    measurement_points_input(session)

animation_tab, model_tab = st.tabs(["📊 Animation", "🖼️ 3D Model Viewer"])
with animation_tab:
    animation_col, info_col = st.columns([3,1])
    with animation_col:
        run_animation(session)

    with info_col:
        sim_parameters(session)

if st.secrets["FLAGS"]["show_render_tab"]:
    with model_tab:
        from ui.model_tab import render_model_tab
        render_model_tab(session)
else:
    with model_tab:
        st.info("3D Model Viewer coming soon.")