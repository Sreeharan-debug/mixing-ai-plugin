import streamlit as st
import tempfile
import os

from analysis import analyze_mix
from audio_loader import load_audio

st.set_page_config(page_title="AI Mixing Assistant", layout="wide")
st.title("🎧 AI Mixing Assistant")

col1, col2 = st.columns(2)

with col1:
    user_file = st.file_uploader("Your Mix", type=["wav"])

with col2:
    ref_file = st.file_uploader("Reference", type=["wav"])

if st.button("Analyze Mix"):

    if user_file and ref_file:

        with tempfile.NamedTemporaryFile(delete=False) as f1:
            f1.write(user_file.read())
            p1 = f1.name

        with tempfile.NamedTemporaryFile(delete=False) as f2:
            f2.write(ref_file.read())
            p2 = f2.name

        y1, sr1 = load_audio(p1)
        y2, sr2 = load_audio(p2)

        results, scores, plot = analyze_mix(y1, sr1, y2, sr2)

        st.header("🎯 Priority")

        if results["priority"]:
            p = results["priority"]
            st.error(f"{p['type']} ({p['range']})")
            st.write(p["why"])
            st.write(p["fix"])
        else:
            st.success("Clean mix")

        st.header("📊 Scores")

        for k in ["sub","low","lowmid","mid","presence","air"]:
            st.write(f"{k}: {scores[k]}")
            st.progress(scores[k]/100)

        st.write(f"Overall: {scores['overall']}")
        st.progress(scores["overall"]/100)

        st.write(f"Match: {scores['match']}%")

        st.header("📉 Spectrum")
        st.image(plot)

        st.header("🧠 Issues")
        for i in results["issues"]:
            st.warning(f"{i['type']} | {i['confidence']}%")

    else:
        st.warning("Upload both files")