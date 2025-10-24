import json
import streamlit as st
from google.oauth2 import service_account
from google.cloud import firestore

def get_db() -> firestore.Client:
    # Option A: FIREBASE block with keys
    if "FIREBASE" in st.secrets:
        fb = st.secrets["FIREBASE"]
        creds_info = {
            "type": "service_account",
            "project_id": fb["project_id"],
            "client_email": fb["client_email"],
            "private_key": fb["private_key"],
            "token_uri": fb.get("token_uri", "https://oauth2.googleapis.com/token"),
            "auth_uri": fb.get("auth_uri", "https://accounts.google.com/o/oauth2/auth"),
        }

    credentials = service_account.Credentials.from_service_account_info(creds_info)
    return firestore.Client(project=creds_info["project_id"], credentials=credentials)
