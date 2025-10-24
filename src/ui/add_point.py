import streamlit as st
import numpy as np
from models.session import SessionModel
from models.point import VibrationPoint

@st.dialog("Add Measurement Point")
def add_measurement_point(session: SessionModel):
    with st.container():
        point_index = len(session.measurement_points)

        name = st.text_input("Point Name", value=f"Point {len(session.measurement_points) + 1}", key="add_point_name")
        c1, c2, c3 = st.columns(3)
        with c1:
            x = st.number_input("X Coordinate", value=0.0, key=f"x_input_{point_index}")
        with c2:
            y = st.number_input("Y Coordinate", value=0.0, key=f"y_input_{point_index}")
        with c3:
            z = st.number_input("Z Coordinate", value=0.0, key=f"z_input_{point_index}")

        with st.container(border=True):
            st.caption("Vibration Properties")
            c1, c2, c3 = st.columns(3)
            with c1:
                st.subheader("Frequency (Hz)")
                horiz_frequency = st.number_input(
                    "Horizontal", 
                    value=0.0, 
                    format="%.6f",
                    key=f"horizontal_frequency_input_{point_index}",
                    min_value=0.0
                )
                vert_frequency = st.number_input(
                    "Vertical", 
                    value=0.0, 
                    format="%.6f",
                    key=f"vertical_frequency_input_{point_index}",
                    min_value=0.0
                )
            with c2:
                st.subheader("Amplitude (m)")
                horiz_amplitude = st.number_input(
                    "Horizontal", 
                    value=0.0, 
                    format="%.6f",
                    key=f"horizontal_amplitude_input_{point_index}",
                    min_value=0.0
                )
                vert_amplitude = st.number_input(
                    "Vertical", 
                    value=0.0, 
                    format="%.6f",
                    key=f"vertical_amplitude_input_{point_index}",
                    min_value=0.0
                )
            with c3:
                st.subheader("Phase (°)")
                horiz_phase = st.number_input(
                    "Horizontal", 
                    value=0.0, 
                    key=f"horizontal_phase_input_{point_index}"
                )
                vert_phase = st.number_input(
                    "Vertical", 
                    value=0.0, 
                    key=f"vertical_phase_input_{point_index}"
                )

        if st.button("Add Point"):
            new_point = VibrationPoint(
                x=x, 
                y=y, 
                z=z, 
                name=name,
                frequency_h=horiz_frequency,
                amplitude_h=horiz_amplitude,    
                phase_h=horiz_phase,
                frequency_v=vert_frequency,
                amplitude_v=vert_amplitude,
                phase_v=vert_phase
            )
            session.measurement_points.append(new_point)
            st.success(f"Measurement Point {name} added.")
            st.rerun()