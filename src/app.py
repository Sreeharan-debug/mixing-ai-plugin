import streamlit as st
import os
from audio_loader import load_audio
from analysis import analyze_mix

st.set_page_config(page_title="AI Mixing Assistant", layout="wide")

st.title("🎧 AI Mixing Assistant")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_DIR = os.path.join(BASE_DIR, "data", "output")

# Upload files
user_file = st.file_uploader("Upload Your Mix (user.wav)", type=["wav"])
ref_file = st.file_uploader("Upload Reference Track (ref.wav)", type=["wav"])

if user_file and ref_file:

    # Save uploaded files temporarily
    user_path = os.path.join(BASE_DIR, "data", "input", "temp_user.wav")
    ref_path = os.path.join(BASE_DIR, "data", "input", "temp_ref.wav")

    with open(user_path, "wb") as f:
        f.write(user_file.read())

    with open(ref_path, "wb") as f:
        f.write(ref_file.read())

    if st.button("Analyze Mix"):

        y1, sr1 = load_audio(user_path)
        y2, sr2 = load_audio(ref_path)

        results = analyze_mix(y1, sr1, y2, sr2, OUTPUT_DIR)

        st.subheader("🧠 Analysis Report")

        for r in results:
            r = r.strip()

            if (
                r.startswith("---")
                or "Overall Mix Score" in r
                or "Reference Match" in r
            ):
                st.markdown(f"**{r}**")
            else:
                st.write("• " + r)

        # Show graph
        graph_path = os.path.join(OUTPUT_DIR, "spectrum.png")

        if os.path.exists(graph_path):
            st.subheader("📊 Spectrum Analysis")
            st.image(graph_path, use_column_width=True)