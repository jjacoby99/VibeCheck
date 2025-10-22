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
                value=getattr(session.blower, 'length', 1.0),
                key="blower_length_x"
            )
        with c2:
            width = st.number_input(
                "Width - y (m)", 
                min_value=0.0, 
                value=getattr(session.blower, 'width', 1.0),
                key="blower_width_y"
            )
        with c3:
            height = st.number_input(
                "Height - z (m)", 
                min_value=0.0, 
                value=getattr(session.blower, 'height', 1.0),
                key="blower_height_z"
            )

        if not height or not width or not length:
            st.info("Please enter valid blower dimensions.")
            return

        session.blower = Cuboid(
            length=length, 
            width=width, 
            height=height
        )