# components/visualizer.py
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
from mpl_toolkits.mplot3d.art3d import Line3DCollection, Poly3DCollection

# If your SessionModel imports changed, adjust these imports accordingly
from models.session import SessionModel
from models.point import VibrationPoint  

def _box_edges_from_vertices(verts_xyz):
    """Return line segments for a cuboid given 8 vertices in the order from your Cuboid.vertices."""
    # verts_xyz: list of 8 (x,y,z) in this order:
    # 0:(0,0,0), 1:(L,0,0), 2:(L,W,0), 3:(0,W,0),
    # 4:(0,0,H), 5:(L,0,H), 6:(L,W,H), 7:(0,W,H)
    idx_edges = [
        (0,1),(1,2),(2,3),(3,0),  # bottom
        (4,5),(5,6),(6,7),(7,4),  # top
        (0,4),(1,5),(2,6),(3,7),  # verticals
    ]
    V = np.array(verts_xyz, dtype=float)
    return [(V[i], V[j]) for (i,j) in idx_edges]

def _box_faces_from_LWH(L, W, H):
    """Return faces (quads) for a cuboid of size LxWxH with min corner at (0,0,0)."""
    return [
        # bottom (z=0)
        [(0,0,0), (L,0,0), (L,W,0), (0,W,0)],
        # top (z=H)
        [(0,0,H), (L,0,H), (L,W,H), (0,W,H)],
        # sides
        [(0,0,0), (L,0,0), (L,0,H), (0,0,H)],       # y=0
        [(0,W,0), (L,W,0), (L,W,H), (0,W,H)],       # y=W
        [(0,0,0), (0,W,0), (0,W,H), (0,0,H)],       # x=0
        [(L,0,0), (L,W,0), (L,W,H), (L,0,H)],       # x=L
    ]

def _compute_positions(base_positions, points, t, exaggerate, h_axis='y', v_axis='z'):
    """Compute animated positions at time t (seconds) for all points."""
    pos = base_positions.copy()
    axis_idx = {'x':0, 'y':1, 'z':2}
    h_i = axis_idx[h_axis]
    v_i = axis_idx[v_axis]

    for i, p in enumerate(points):
        # Per-point angular frequencies
        omega_h = 2.0 * np.pi * float(p.frequency_h)
        omega_v = 2.0 * np.pi * float(p.frequency_v)
        pos[i, h_i] += exaggerate * float(p.amplitude_h) * np.sin(omega_h * t + float(p.phase_h))
        pos[i, v_i] += exaggerate * float(p.amplitude_v) * np.sin(omega_v * t + float(p.phase_v))
    return pos

def run_animation(session: SessionModel, h_axis='y', v_axis='z'):
    """Render a simple 3D vibration animation in Streamlit using the session model."""
    if session.blower is None or session.sim_props is None:
        st.warning("Please define the blower dimensions and simulation settings first.")
        return
    if not session.measurement_points:
        st.info("No measurement points yet — add a few points to see them animate.")
        return

    # Pull from your models
    L, W, H = float(session.blower.length), float(session.blower.width), float(session.blower.height)
    sim = session.sim_props
    fps = int(sim.FPS)
    exaggerate = float(sim.exaggeration)
    time_scale = float(sim.time_scale)
    total_time = float(sim.total_time)
    n_frames = max(1, int(total_time * fps))

    # Base point array
    points: list[VibrationPoint] = session.measurement_points  # type: ignore
    base_positions = np.array([[p.x, p.y, p.z] for p in points], dtype=float)

    # --- Matplotlib figure setup ---
    fig = plt.figure(figsize=(25, 15))
    ax = fig.add_subplot(111, projection="3d")
    ax.set_xlabel("X (m)")
    ax.set_ylabel("Y (m)")
    ax.set_zlabel("Z (m)")
    ax.set_title("Blower Vibration")

    # Draw cuboid: edges + translucent faces
    verts = [(v.x, v.y, v.z) for v in session.blower.vertices]
    edge_segs = _box_edges_from_vertices(verts)
    lc = Line3DCollection(edge_segs, colors='k', linewidths=1.0, alpha=0.9, zorder=5)
    ax.add_collection3d(lc)

    faces = _box_faces_from_LWH(L, W, H)
    face_poly = Poly3DCollection(faces, facecolors=(0.8, 0.85, 0.95, 0.20), edgecolors='none', zorder=1)
    ax.add_collection3d(face_poly)

    # Scatter + stems + labels
    scat = ax.scatter(base_positions[:,0], base_positions[:,1], base_positions[:,2], s=50, depthshade=True, zorder=10)

    stems = []
    for p in base_positions:
        line, = ax.plot([p[0], p[0]], [p[1], p[1]], [p[2], p[2]], alpha=0.45, linewidth=1.2, zorder=2)
        stems.append(line)

    labels = []
    for i, p in enumerate(points):
        name = p.name or f"P{i+1}"
        txt = ax.text(base_positions[i,0], base_positions[i,1], base_positions[i,2] + 0.02*H, name,
                      fontsize=9, ha='center', va='bottom', zorder=20)
        labels.append(txt)

    # Nice margins so the box isn’t edge-to-edge
    margin = 0.2
    ax.set_xlim(-margin * L, (1 + margin) * L)
    ax.set_ylim(-margin * W, (1 + margin) * W)
    ax.set_zlim(-margin * H, (1 + margin) * H)
    # ax.set_box_aspect((L, W, H))  # optional

    placeholder = st.empty()
    start = st.button("▶ Run animation", type="primary")

    if not start:
        # Draw a static first frame
        placeholder.pyplot(fig, clear_figure=False)
        return

    # Animate
    for frame in range(n_frames):
        t = (frame / fps) * time_scale
        P = _compute_positions(base_positions, points, t, exaggerate, h_axis=h_axis, v_axis=v_axis)

        # Update scatter
        scat._offsets3d = (P[:,0], P[:,1], P[:,2])

        # Update stems and labels
        for i, line in enumerate(stems):
            x = [base_positions[i,0], P[i,0]]
            y = [base_positions[i,1], P[i,1]]
            z = [base_positions[i,2], P[i,2]]
            line.set_data(x, y)
            line.set_3d_properties(z)

        for i, txt in enumerate(labels):
            txt.set_position((P[i,0], P[i,1]))
            txt.set_3d_properties(P[i,2] + 0.02*H, zdir='z')

        placeholder.pyplot(fig, clear_figure=False)
