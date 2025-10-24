# app_stl_points.py
# pip install streamlit plotly numpy-stl trimesh shapely==2.0.4 (trimesh dep)

import streamlit as st
import numpy as np
import plotly.graph_objects as go
from models.session import SessionModel
def render_model_tab(session: SessionModel):

    # Choose either numpy-stl OR trimesh
    USE_TRIMESH = True

    if USE_TRIMESH:
        import trimesh
    else:
        from stl import mesh as npstl

    st.set_page_config(layout="wide", page_title="STL + Moving Points")

    st.title("STL viewer with animated measurement points")

    uploaded = st.file_uploader("Upload an STL", type=["stl"])
    colA, colB = st.columns([1,1])
    with colA:
        decimate_target = st.slider("Decimate to ~N faces (trimesh only)", 1000, 100_000, 20_000, step=1000)
    with colB:
        n_frames = st.slider("Animation frames", 20, 300, 120, step=10)

    # Example measurement points and motion settings
    # Base positions (x,y,z) in STL coordinates. Replace with your real points.
    base_points = np.array([
        [0.0, 0.0, 0.0],
        [0.3, 0.2, 0.1],
        [-0.2, 0.25, 0.05],
        [0.15, -0.1, 0.2],
    ])

    # Per-point vibration parameters (amplitudes in model units; phases in rad)
    amp_h = np.array([0.02, 0.01, 0.015, 0.01])   # horizontal (x) amplitude
    amp_v = np.array([0.01, 0.015, 0.01, 0.02])   # vertical (z) amplitude
    phase_h = np.array([0.0, 0.7, 1.3, 2.0])
    phase_v = np.array([0.0, 1.1, 2.2, 2.9])
    freq_hz = 2.0  # animation frequency (visual only)

    @st.cache_data(show_spinner=False)
    def load_mesh(file_bytes, decimate_to_faces: int):
        if USE_TRIMESH:
            m = trimesh.load(file_bytes, file_type='stl')
            # Ensure triangular mesh
            if not isinstance(m, trimesh.Trimesh) and hasattr(m, 'dump'):
                # if a Scene, merge geometry
                combined = trimesh.util.concatenate(tuple(g for g in m.geometry.values()))
                m = combined

            m.remove_unreferenced_vertices()
            # Decimate if heavy
            if len(m.faces) > decimate_to_faces:
                try:
                    m = m.simplify_quadratic_decimation(decimate_to_faces)
                except Exception:
                    pass  # fall back to original if QEM not available
            vertices = m.vertices
            faces = m.faces  # (n,3) indices
            # Also get unique edges for a wireframe overlay
            edges = m.edges_unique
            return vertices, faces, edges
        else:
            m = npstl.Mesh.from_file(file_bytes)
            # numpy-stl stores triangles directly; build vertices list & faces
            v = np.vstack([m.v0, m.v1, m.v2])
            # Make vertices unique
            verts, inv = np.unique(v, axis=0, return_inverse=True)
            faces = inv.reshape(-1, 3)
            # No easy decimate here; edges optional
            return verts, faces, None

    def mesh3d_trace(vertices, faces, color="lightgray", opacity=0.9):
        i, j, k = faces[:,0], faces[:,1], faces[:,2]
        return go.Mesh3d(
            x=vertices[:,0], y=vertices[:,1], z=vertices[:,2],
            i=i, j=j, k=k,
            color=color,
            opacity=opacity,
            flatshading=True,
            lighting=dict(ambient=0.6, diffuse=0.8, roughness=0.9),
            lightposition=dict(x=100, y=200, z=100),
            name="Mesh"
        )

    def wireframe_trace(vertices, edges, line_width=1):
        if edges is None:
            return None
        # Build a single trace with segments separated by None
        pts = []
        for e0, e1 in edges:
            pts.append(vertices[e0])
            pts.append(vertices[e1])
            pts.append([None, None, None])
        pts = np.array(pts, dtype=object)
        return go.Scatter3d(
            x=pts[:,0], y=pts[:,1], z=pts[:,2],
            mode="lines",
            line=dict(width=line_width),
            name="Wireframe",
            hoverinfo="skip",
            showlegend=False
        )

    def point_positions(t):
        # t in seconds; sinusoidal motion around base_points
        x = base_points[:,0] + amp_h * np.sin(2*np.pi*freq_hz*t + np.deg2rad(phase_h))
        y = base_points[:,1]  # keep y fixed for this demo; change if needed
        z = base_points[:,2] + amp_v * np.sin(2*np.pi*freq_hz*t + np.deg2rad(phase_v))
        return np.column_stack([x,y,z])

    def make_figure(vertices, faces, edges, n_frames=120):
        # Static mesh
        mesh = mesh3d_trace(vertices, faces)
        wire = wireframe_trace(vertices, edges)

        # Initial point positions (t=0)
        p0 = point_positions(0.0)
        points0 = go.Scatter3d(
            x=p0[:,0], y=p0[:,1], z=p0[:,2],
            mode="markers+text",
            marker=dict(size=6),
            text=[f"P{i}" for i in range(len(p0))],
            textposition="top center",
            name="Points",
        )

        data = [mesh, points0] if wire is None else [mesh, wire, points0]

        # --- FIX: build frames that update ONLY the points trace ---
        point_trace_index = 1 if wire is None else 2  # mesh=0, (wire=1), points=1/2
        frames = []
        ts = np.linspace(0, 1.0, n_frames, endpoint=False)  # 1s loop visually
        for i, t in enumerate(ts):
            p = point_positions(t)
            frames.append(
                go.Frame(
                    name=str(i),  # give each frame a name so slider can target it
                    data=[
                        go.Scatter3d(
                            x=p[:,0], y=p[:,1], z=p[:,2],
                            mode="markers+text",
                            marker=dict(size=6),
                        )
                    ],
                    traces=[point_trace_index],  # <— tell Plotly which trace to update
                )
            )

        fig = go.Figure(data=data, frames=frames)

        # Layout & controls (slider targets frame names)
        fig.update_layout(
            scene=dict(
                aspectmode="data",
                xaxis=dict(visible=False),
                yaxis=dict(visible=False),
                zaxis=dict(visible=False),
            ),
            margin=dict(l=0, r=0, t=0, b=0),
            showlegend=False,
            updatemenus=[
                dict(
                    type="buttons",
                    buttons=[
                        dict(label="▶ Play", method="animate",
                            args=[None, {"frame": {"duration": 33, "redraw": True},
                                        "fromcurrent": True,
                                        "transition": {"duration": 0}}]),
                        dict(label="⏸ Pause", method="animate",
                            args=[[None], {"frame": {"duration": 0, "redraw": False},
                                            "mode": "immediate"}]),
                    ],
                    direction="left",
                    x=0.0, y=1.05, xanchor="left", yanchor="bottom",
                    pad={"t": 0, "r": 10}
                )
            ],
            sliders=[dict(
                steps=[dict(
                    method="animate",
                    args=[[str(i)], {"mode": "immediate",
                                    "frame": {"duration": 0, "redraw": True},
                                    "transition": {"duration": 0}}],
                    label=str(i)
                ) for i in range(len(frames))],
                x=0.0, y=1.02, currentvalue={"prefix": "Frame: "}, len=1.0
            )]
        )
        return fig


    if uploaded is None:
        st.info("Upload an STL to view the mesh and animated points.")
    else:
        vertices, faces, edges = load_mesh(uploaded, decimate_target)
        fig = make_figure(vertices, faces, edges, n_frames=n_frames)
        st.plotly_chart(fig, use_container_width=True, config={"displaylogo": False})
        session.run_simulation = False
