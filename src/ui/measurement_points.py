import streamlit as st
from models.session import SessionModel
from ui.edit_point import edit_measurement_point
from ui.add_point import add_measurement_point

def measurement_points_input(session: SessionModel):
    with st.container(border=True):
        st.subheader("Measurement Points")
        if not session.measurement_points:
            st.info("No measurement points added yet.")
            

        for i, point in enumerate(session.measurement_points):
            c1, c2 = st.columns([3,1])
            with c1:
                st.write(f"**{point.name}**: ({point.x}, {point.y}, {point.z})")
            with c2:
                if st.button("✏️", key=f"edit_point_{i}"):
                    edit_measurement_point(session, i)

        if st.button("Add Measurement Point"):
            add_measurement_point(session)