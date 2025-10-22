import streamlit as st
from models.session import SessionModel
from models.point import VibrationPoint

@st.dialog("Edit Measurement Point")
def edit_measurement_point(session: SessionModel, point_index: int):
    point = session.measurement_points[point_index]
    
    with st.form(key=f"edit_point_form_{point_index}"):
        name = st.text_input("Point Name", value=point.name, key="edit_point_name")

        c1, c2, c3 = st.columns(3)
        with c1:
            x = st.number_input("X Coordinate", value=point.x, key=f"x_input_{point_index}")
        with c2:
            y = st.number_input("Y Coordinate", value=point.y, key=f"y_input_{point_index}")
        with c3:
            z = st.number_input("Z Coordinate", value=point.z, key=f"z_input_{point_index}")
        
        with st.container(border=True):
            st.caption("Vibration Properties")
            c1, c2, c3 = st.columns(3)
            with c1:
                st.subheader("Frequency (Hz)")
                horiz_frequency = st.number_input(
                    "Horizontal", 
                    value=getattr(point, 'frequency_h', 1.0), 
                    key=f"horizontal_frequency_input_{point_index}",
                    format="%.6f",
                    min_value=0.0
                )
                vert_frequency = st.number_input(
                    "Vertical", 
                    value=getattr(point, 'frequency_v', 1.0), 
                    key=f"vertical_frequency_input_{point_index}",
                    format="%.6f",
                    min_value=0.0
                )
            with c2:
                st.subheader("Amplitude (m)")
                horiz_amplitude = st.number_input(
                    "Horizontal", 
                    value=getattr(point, 'amplitude_h', 0.1), 
                    key=f"horizontal_amplitude_input_{point_index}",
                    format="%.6f",
                    min_value=0.0
                )
                vert_amplitude = st.number_input(
                    "Vertical", 
                    value=getattr(point, 'amplitude_v', 0.1), 
                    key=f"vertical_amplitude_input_{point_index}",
                    format="%.6f",
                    min_value=0.0
                )
            with c3:
                st.subheader("Phase (°)")
                horiz_phase = st.number_input(
                    "Horizontal", 
                    value=getattr(point, 'phase_h', 0.0), 
                    key=f"horizontal_phase_input_{point_index}",
                    format="%.6f",
                )
                vert_phase = st.number_input(
                    "Vertical", 
                    value=getattr(point, 'phase_v', 0.0), 
                    key=f"vertical_phase_input_{point_index}",
                    format="%.6f",
                )
        submitted = st.form_submit_button("Save Changes")

        if submitted:
            session.measurement_points[point_index] = VibrationPoint(
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
            st.success(f"Measurement Point {point_index + 1} updated.")
            st.rerun()
    
    delete = st.button("🗑", key=f"delete_point_{point_index}", help=f"Delete {session.measurement_points[point_index].name}")
    if delete:
        session.measurement_points.pop(point_index)
        st.success(f"Measurement Point {point_index + 1} deleted.")
        return