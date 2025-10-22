import streamlit as st
from models.session import SessionModel
from models.sim import Sim

def sim_parameters(session: SessionModel):
    with st.container(border=True):
        st.subheader("Simulation Parameters")
        FPS = st.number_input(
            "Frame rate (FPS)", 
            min_value=1, 
            value=getattr(session.sim_props, 'FPS', 60),
            key="sim_time_step"
        )

        exaggeration = st.number_input(
            "Exaggeration Factor",
            min_value=1.0,
            value=getattr(session.sim_props, 'exaggeration', 400.0),
            max_value=1_000_000.0,
            key="sim_exaggeration",
            help="Factor by which to exaggerate the displacement. Useful for visualizing small displacements."
        )

        time_scale = st.number_input(
            "Time Scale",
            min_value=0.00001,
            value=getattr(session.sim_props, 'time_scale', 1.0),
            max_value=100.0,
            key="sim_time_scale",
            help="Scale factor for simulation time. Values > 1 speed up the simulation, values < 1 slow it down."
        )

        total_time = st.number_input(
            "Total Simulation Time (s)", 
            min_value=0.1,
            value=getattr(session.sim_props, 'total_time', 10.0),
            key="sim_total_time"
        )

    if not FPS or not exaggeration or not time_scale or not total_time:
        st.info("Please enter valid simulation parameters.")
        return
    
    session.sim_props = Sim(
        FPS=FPS,
        exaggeration=exaggeration,
        time_scale=time_scale,
        total_time=total_time
    )