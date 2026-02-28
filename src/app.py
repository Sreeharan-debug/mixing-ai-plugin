import streamlit as st
import librosa
import numpy as np
import matplotlib.pyplot as plt

from analysis import analyze_mix

st.set_page_config(page_title="AI Mixing Assistant", layout="wide")

st.title("🎧 AI Mixing Assistant")

col1, col2 = st.columns(2)

with col1:
    user_file = st.file_uploader("Upload Your Mix (WAV)", type=["wav"])

with col2:
    ref_file = st.file_uploader("Upload Reference Track (WAV)", type=["wav"])

if user_file and ref_file:
    if st.button("Analyze Mix"):

        y1, sr1 = librosa.load(user_file, sr=None)
        y2, sr2 = librosa.load(ref_file, sr=None)

        results, scores = analyze_mix(y1, sr1, y2, sr2)

        # 🎯 WHAT TO FIX
        st.subheader("🎯 What to Fix First")

        if results["issues"]:
            st.error(results["issues"][0])
        else:
            st.success("No major issues detected 🎉")

        # 📊 SCORES
        st.subheader("📊 Mix Scores")

        st.progress(scores["low"] / 100)
        st.write(f"Low-End: {scores['low']}")

        st.progress(scores["lowmid"] / 100)
        st.write(f"Low-Mid: {scores['lowmid']}")

        st.progress(scores["presence"] / 100)
        st.write(f"Presence: {scores['presence']}")

        st.progress(scores["overall"] / 100)
        st.write(f"Overall: {scores['overall']}")

        st.write(f"🎯 Reference Match: {results['reference_match']}%")

        # 📈 SPECTRUM
        st.subheader("📈 Spectrum Analysis")

        def plot_spectrum(y, sr, label):
            S = np.abs(librosa.stft(y))
            S_db = librosa.amplitude_to_db(S, ref=np.max)
            freqs = librosa.fft_frequencies(sr=sr)
            avg = np.mean(S_db, axis=1)
            return freqs, avg

        f1, s1 = plot_spectrum(y1, sr1, "User")
        f2, s2 = plot_spectrum(y2, sr2, "Ref")

        fig, ax = plt.subplots()
        ax.plot(f1, s1, label="User Mix")
        ax.plot(f2, s2, label="Reference")

        ax.set_xscale("log")
        ax.set_xlabel("Frequency (Hz)")
        ax.set_ylabel("Amplitude (dB)")
        ax.set_title("Frequency Spectrum (Log Scale)")
        ax.legend()

        # Highlight regions
        ax.axvspan(20, 120, alpha=0.1)
        ax.axvspan(200, 500, alpha=0.1, color='red')

        st.pyplot(fig)