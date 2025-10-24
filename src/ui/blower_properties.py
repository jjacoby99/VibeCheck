import streamlit as st
from models.cuboid import Cuboid
from models.session import SessionModel

def blower_dimensions_input(session: SessionModel):
    with st.container(border=True):
        st.subheader(f"Blower Dimensions")
        c1, c2, c3 = st.columns(3)
        with c1:
            length = st.number_input(
                "Length - x (m)", 
                min_value=0.0, 
                value=session.blower.length if session.blower else 1.0,
                key=f"blower_length_x_{str(session.blower.length)}"
            )
            session.blower.length = length

        with c2:
            width = st.number_input(
                "Width - y (m)", 
                min_value=0.0, 
                value=session.blower.width if session.blower else 1.0,
                key=f"blower_width_y_{str(session.blower.width)}"
            )
            session.blower.width = width

        with c3:
            height = st.number_input(
                "Height - z (m)", 
                min_value=0.0, 
                value=session.blower.height if session.blower else 1.0,
                key=f"blower_height_z_{str(session.blower.height)}"
            )
            session.blower.height = height

        if not height or not width or not length:
            st.info("Please enter valid blower dimensions.")
            return