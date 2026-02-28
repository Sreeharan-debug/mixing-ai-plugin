import streamlit as st
import tempfile
import os

# ✅ Correct imports (same folder)
from analysis import analyze_mix
from audio_loader import load_audio

# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="AI Mixing Assistant",
    layout="wide"
)

st.title("🎧 AI Mixing Assistant")

# ---------- FILE UPLOAD ----------
col1, col2 = st.columns(2)

with col1:
    user_file = st.file_uploader("Upload Your Mix (WAV)", type=["wav"])

with col2:
    ref_file = st.file_uploader("Upload Reference Track (WAV)", type=["wav"])

# ---------- ANALYZE BUTTON ----------
if st.button("Analyze Mix"):

    if user_file and ref_file:

        # Save temp files
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as f1:
            f1.write(user_file.read())
            user_path = f1.name

        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as f2:
            f2.write(ref_file.read())
            ref_path = f2.name

        # Load audio
        y1, sr1 = load_audio(user_path)
        y2, sr2 = load_audio(ref_path)

        # ---------- ANALYSIS ----------
        results, scores, plot_path = analyze_mix(y1, sr1, y2, sr2)

        # ---------- PRIORITY ----------
        st.subheader("🎯 What to Fix First")

        if results["priority"]:
            p = results["priority"]

            st.error(
                f"Priority Issue: {p['type']} ({p['range']})"
            )

            st.write(f"**Why:** {p['why']}")
            st.write(f"**Fix:** {p['fix']}")

        else:
            st.success("No major issues detected 🎉")

        # ---------- SCORES ----------
        st.subheader("📊 Mix Scores")

        st.progress(scores["low"] / 100)
        st.write(f"Low-End: {scores['low']}")

        st.progress(scores["mid"] / 100)
        st.write(f"Low-Mid: {scores['mid']}")

        st.progress(scores["high"] / 100)
        st.write(f"Presence: {scores['high']}")

        st.progress(scores["overall"] / 100)
        st.write(f"Overall: {scores['overall']}")

        st.write(f"🎯 Reference Match: {scores['match']}%")

        # ---------- SPECTRUM ----------
        st.subheader("📉 Spectrum Analysis")
        st.image(plot_path)

        # ---------- ALL INSIGHTS ----------
        st.subheader("🧠 AI Mix Insights")

        if results["issues"]:
            for issue in results["issues"]:
                st.warning(
                    f"{issue['type']} ({issue['range']}) | "
                    f"Confidence: {issue['confidence']}% | "
                    f"Severity: {issue['severity']}"
                )
        else:
            st.info("Mix looks clean — no major problems detected.")

    else:
        st.warning("Please upload both files.")