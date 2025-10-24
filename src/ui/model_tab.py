from __future__ import annotations
import numpy as np
import streamlit as st
import plotly.graph_objects as go
from pathlib import Path

# Prefer numpy-stl; fall back to trimesh if needed
def _load_mesh(stl_path: Path):
    try:
        from stl import mesh as stlmesh
        m = stlmesh.Mesh.from_file(str(stl_path))
        verts = m.vectors.reshape(-1, 3)
        # Deduplicate vertices for Plotly Mesh3d
        uniq, idx = np.unique(verts.round(6), axis=0, return_inverse=True)
        faces = idx.reshape(-1, 3).astype(np.int32)
        return uniq, faces
    except Exception:
        # Trimesh fallback (works for stl/obj/ply)
        import trimesh
        tm = trimesh.load_mesh(stl_path, process=False)
        if not isinstance(tm, trimesh.Trimesh):
            tm = tm.dump(concatenate=True)
        uniq = tm.vertices.view(np.ndarray)
        faces = tm.faces.view(np.ndarray).astype(np.int32)
        return uniq, faces

@st.cache_data(show_spinner=False)
def load_model(stl_path_str: str):
    stl_path = Path(stl_path_str)
    if not stl_path.exists():
        raise FileNotFoundError(f"Mesh not found: {stl_path}")
    return _load_mesh(stl_path)

def _edges_from_faces(faces: np.ndarray) -> np.ndarray:
    edges = np.vstack([faces[:, [0,1]], faces[:, [1,2]], faces[:, [2,0]]])
    edges = np.unique(np.sort(edges, axis=1), axis=0)
    return edges

def _measurement_points_from_session(session) -> np.ndarray:
    """
    Accepts your current SessionModel.
    Expects session.measurement_points to be a list of objects with x,y,z (or .coords()).
    Returns (N,3) ndarray. Safe if missing/empty.
    """
    pts = []
    mps = getattr(session, "measurement_points", []) or []
    for p in mps:
        # adapt to your class shape
        if hasattr(p, "x") and hasattr(p, "y") and hasattr(p, "z"):
            pts.append([float(p.x), float(p.y), float(p.z)])
        elif hasattr(p, "coords"):
            x, y, z = p.coords()
            pts.append([float(x), float(y), float(z)])
    if not pts:
        return np.empty((0, 3))
    return np.asarray(pts, dtype=float)

def render_model_tab(session=None):
    st.subheader("3D Blower Model (mesh viewer)")
    colA, colB, colC = st.columns([2,1,1], vertical_alignment="bottom")

    with colA:
        # Path relative to this file: src/ui/model_tab.py -> ../assets/blower.stl
        uploaded = st.file_uploader("Upload mesh (STL/OBJ)", type=["stl", "obj"])
        if not uploaded:
            st.info("Upload a mesh to view.")
            return
        
        # Streamlit’s UploadedFile acts like a BytesIO
        tmp = Path("temp_mesh.stl")
        tmp.write_bytes(uploaded.getvalue())
        uniq, faces = load_model(tmp)
        
    with colB:
        show_wire = st.checkbox("Wireframe overlay", value=True)
    with colC:
        opacity = st.slider("Opacity", 0.1, 1.0, 0.5)

    # Build Plotly figure
    fig = go.Figure()
    fig.add_trace(go.Mesh3d(
        x=uniq[:,0], y=uniq[:,1], z=uniq[:,2],
        i=faces[:,0], j=faces[:,1], k=faces[:,2],
        opacity=opacity,
        flatshading=True,
        lighting=dict(ambient=0.5, diffuse=0.5, specular=0.1, roughness=0.9),
        showscale=False,
        name="Blower Mesh",
    ))

    if show_wire:
        edges = _edges_from_faces(faces)
        # Build a single Scatter3d with None breaks for segments
        xs = np.r_[uniq[edges[:,0],0], None, uniq[edges[:,1],0]]
        ys = np.r_[uniq[edges[:,0],1], None, uniq[edges[:,1],1]]
        zs = np.r_[uniq[edges[:,0],2], None, uniq[edges[:,1],2]]
        fig.add_trace(go.Scatter3d(
            x=xs, y=ys, z=zs,
            mode="lines",
            line=dict(width=1),
            hoverinfo="none",
            name="Wireframe"
        ))

    # Measurement points overlay (from your session)
    mp = _measurement_points_from_session(session)
    if mp.size > 0:
        fig.add_trace(go.Scatter3d(
            x=mp[:,0], y=mp[:,1], z=mp[:,2],
            mode="markers",
            marker=dict(size=5, symbol="circle-open"),
            name="Measurement Points"
        ))

    fig.update_layout(
        scene=dict(
            aspectmode="data",
            xaxis=dict(visible=False),
            yaxis=dict(visible=False),
            zaxis=dict(visible=False),
            # Initial camera a bit backed off; adjust if your model is very large
            camera=dict(eye=dict(x=1.6, y=1.6, z=1.2))
        ),
        margin=dict(l=0, r=0, t=0, b=0),
        height=700,  # keep it within most screens
    )

    st.plotly_chart(fig, use_container_width=True)
