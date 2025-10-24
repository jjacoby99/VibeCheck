# src/ui/load_session.py
import streamlit as st
from logic.repo import save_config, load_config, list_configs, search_configs, delete_config
from logic.adapters import domain_to_dto, dto_to_domain

def sim_explorer_ui():
    with st.expander("Simulation Project Explorer", expanded=True):
        st.subheader("Save simulation setup")
        # --- One-time hydration from ?cfg= param ---
        cfg_id = st.query_params.get("cfg", None)
        if "loaded_cfg_id" not in st.session_state:
            st.session_state.loaded_cfg_id = None

        if cfg_id and st.session_state.loaded_cfg_id != cfg_id:
            dto = load_config(cfg_id)
            if dto:
                st.session_state.session = dto_to_domain(dto)
                st.session_state.loaded_cfg_id = cfg_id
                st.toast(f"Loaded config: {dto.name}")
            else:
                st.warning("Config ID not found.")

        # --- Save current ---
        current_name = getattr(st.session_state.session, "name", "My Setup")
        with st.form("save_form", clear_on_submit=False):
            new_name = st.text_input("Name", value=current_name)
            save_clicked = st.form_submit_button("💾 Save configuration", use_container_width=True)
        if save_clicked:
            dto = domain_to_dto(st.session_state.session)
            dto.name = new_name
            new_id = save_config(dto)
            # refresh domain (to carry id) and guard against immediate re-load
            st.session_state.session = dto_to_domain(dto)
            st.session_state.loaded_cfg_id = new_id
            st.query_params["cfg"] = new_id
            st.success("Saved. The page URL now restores this setup.")

        st.divider()
        st.subheader("Load simulation setup")
        # --- Search + list ---
        #c1, c2 = st.columns([2, 1])
        #with c1:
        #    q = st.text_input("Search projects by name", placeholder="Type to filter…")
        #with c2:
        #    refresh = st.button("↻ Refresh list", use_container_width=True)

        #if refresh:
        #    st.rerun()

        items = list_configs()

        # Present as a selectable list
        names = [f"{i.name}  —  {i.id}" for i in items]
        selected_idx = st.selectbox(
            "Available projects",
            options=range(len(items)) if items else [],
            format_func=lambda i: names[i].split("  —  ")[0],
            index=0 if items else None,
            placeholder="No projects found" if not items else None,
        )

        #colA, colB, colC = st.columns([1,1,1])
        load_clicked = st.button("📥 Load selected", use_container_width=True, disabled=not items)
        #with colB:
        #    del_clicked = st.button("🗑️ Delete selected", use_container_width=True, disabled=not items)
        #with colC:
        #    copy_clicked = st.button("📋 Copy link", use_container_width=True, disabled=not items)

        if items and selected_idx is not None:
            chosen = items[selected_idx]

            if load_clicked:
                st.session_state.session = dto_to_domain(chosen)
                st.session_state.loaded_cfg_id = chosen.id
                st.query_params["cfg"] = chosen.id
                st.success(f"Loaded: {chosen.name}")
                st.rerun()

            #if del_clicked:
            #    delete_config(chosen.id)
            #    st.success(f"Deleted: {chosen.name}")
            #    st.rerun()

            #if copy_clicked:
            #    # Streamlit doesn’t copy to clipboard natively here; show the URL for manual copy.
            #    base = st.experimental_get_query_params()
            #    st.query_params["cfg"] = chosen.id  # ensure URL reflects the chosen id
            #    st.info("Copy the current page URL from your browser; it now includes the selected config ID.")
