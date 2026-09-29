"""S1: minimal Streamlit dashboard.

Shows the gateway health (API_URL/health) so the wiring can be verified
before the real pages (metrics charts, contracts, logs) are built.

Run locally:  streamlit run services/dashboard/app.py
Owner: S1.
"""

from __future__ import annotations

import os

import requests
import streamlit as st

API_URL = os.getenv("API_URL", "http://localhost:8000")

st.set_page_config(page_title="Smart Healthcare Data Space")
st.title("Smart Healthcare Data Space")
st.caption(f"Gateway: {API_URL} (S4)")

try:
    response = requests.get(f"{API_URL}/health", timeout=3)
    st.subheader("API health")
    st.json(response.json())
except requests.RequestException as exc:
    st.error(f"API unreachable at {API_URL}: {exc}")

st.info("TODO S1: training metrics charts, contract table, connector logs.")
