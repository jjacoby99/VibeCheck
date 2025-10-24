import streamlit as st
from models.session import SessionModel
from models.sim import Sim

def sim_parameters(session: SessionModel):
    
    with st.container(border=True):
        if not session.sim_props:
            return
        st.subheader("Simulation Parameters")
        FPS = st.number_input(
            "Frame rate (FPS)", 
            min_value=1, 
            value=session.sim_props.FPS if session.sim_props else 30,
            key=f"sim_time_step_{str(session.sim_props.FPS)}"
        )
        session.sim_props.FPS = FPS
        exaggeration = st.number_input(
            "Exaggeration Factor",
            min_value=1.0,
            value=session.sim_props.exaggeration if session.sim_props else 10.0,
            max_value=1_000_000.0,
            key=f"sim_exaggeration_{str(session.sim_props.exaggeration)}",
            help="Factor by which to exaggerate the displacement. Useful for visualizing small displacements."
        )
        session.sim_props.exaggeration = exaggeration

        time_scale = st.number_input(
            "Time Scale",
            min_value=0.00001,
            value=session.sim_props.time_scale if session.sim_props else 1.0,
            max_value=100.0,
            key=f"sim_time_scale_{str(session.sim_props.time_scale)}",
            help="Scale factor for simulation time. Values > 1 speed up the simulation, values < 1 slow it down."
        )
        session.sim_props.time_scale = time_scale

        total_time = st.number_input(
            "Total Simulation Time (s)", 
            min_value=0.1,
            value=session.sim_props.total_time if session.sim_props else 10.0,
            key=f"sim_total_time_{str(session.sim_props.total_time)}"
        )
        session.sim_props.total_time = total_time

    if not FPS or not exaggeration or not time_scale or not total_time:
        st.info("Please enter valid simulation parameters.")
        return
    
    start = st.button("▶ Run animation", type="primary")
    stop = st.button("■ Stop animation", type="secondary")
    if start:
        session.run_simulation = True

    if stop:
        session.run_simulation = False

    session.sim_props = Sim(
        FPS=FPS,
        exaggeration=exaggeration,
        time_scale=time_scale,
        total_time=total_time
    )