# -*- coding: utf-8 -*-
"""
Created on Fri Nov 21 15:32:21 2025

@author: clemr
"""

import streamlit as st
import hashlib
import requests

# Load API URL from info.txt
with open('info.txt', 'r') as f:
    API_URL = f.read().strip()

st.title("Commit & Reveal Application")

# --- Commit Phase ---
st.header("1. Commit Phase")

uni_id_commit = st.text_input("NEOMA ID (Commit Phase)")
number_commit = st.number_input("Number (0–100)", min_value=0, max_value=100, step=1)
nonce_commit = st.text_input("Nonce (password)", type="password")

if st.button("Commit"):
    preimage = f"{uni_id_commit}|{number_commit}|{nonce_commit}"
    commit_hash = hashlib.sha256(preimage.encode()).hexdigest()

    st.write("### Preimage:")
    st.code(preimage)
    st.write("### SHA-256 Hash:")
    st.code(commit_hash)

    payload = {"uni_id": uni_id_commit, "commit": commit_hash}
    try:
        response = requests.post(API_URL, json=payload)
        st.success(f"Commit sent! Server response: {response.text}")
    except Exception as e:
        st.error(f"Error sending commit: {e}")

# --- Reveal Phase ---
st.header("2. Reveal Phase")

uni_id_reveal = st.text_input("NEOMA ID (Reveal Phase)")
number_reveal = st.number_input("Number (0–100) (Reveal Phase)", min_value=0, max_value=100, step=1)
nonce_reveal = st.text_input("Nonce (Reveal Phase)", type="password")

if st.button("Reveal"):
    payload = {
        "uni_id": uni_id_reveal,
        "number": int(number_reveal),
        "nonce": nonce_reveal,
    }
    try:
        response = requests.post(API_URL, json=payload)
        st.success(f"Reveal sent! Server response: {response.text}")
    except Exception as e:
        st.error(f"Error sending reveal: {e}")
