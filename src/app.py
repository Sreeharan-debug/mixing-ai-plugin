import streamlit as st
import tempfile

from analysis import analyze_mix
from audio_loader import load_audio
from intelligence import analyze_mix_intelligence


st.set_page_config(page_title="AI Mixing Diagnostic", layout="wide")

st.title("AI Mixing Diagnostic")


# ---------- FILE UPLOAD ----------

mix = st.file_uploader("Upload your mix", type=["wav"])
ref = st.file_uploader("Upload reference track", type=["wav"])


# ---------- ANALYZE BUTTON ----------

if st.button("Analyze"):

    if mix and ref:

        # Save uploaded files temporarily
        with tempfile.NamedTemporaryFile(delete=False) as f:
            f.write(mix.read())
            mix_path = f.name

        with tempfile.NamedTemporaryFile(delete=False) as f:
            f.write(ref.read())
            ref_path = f.name


        # Load audio
        y1, sr1 = load_audio(mix_path)
        y2, sr2 = load_audio(ref_path)


        # ---------- DSP ANALYSIS ----------

        results, scores, plot = analyze_mix(y1, sr1, y2, sr2)


        # ---------- AI INTELLIGENCE ----------

        insights = analyze_mix_intelligence(scores, results)


        # ---------- MULTIBAND SCORES ----------

        st.header("Multiband Mix Scores")

        bands = ["sub", "low", "low_mid", "mid", "presence", "air"]

        for b in bands:

            val = scores[b]

            st.write(f"{b.upper()}: {val}/100")

            st.progress(val / 100)


        # ---------- OVERALL SCORE ----------

        st.header("Overall Mix Score")

        st.metric("Mix Score", scores["overall"])

        st.write(f"Reference Match: {scores['match']}%")


        # ---------- DYNAMIC ANALYSIS ----------

        st.header("Dynamic Analysis")

        st.write(f"Crest Factor: {results['dynamics']['crest_factor']}")
        st.write(f"LUFS: {results['dynamics']['lufs']}")


        # ---------- STEREO ANALYSIS ----------

        st.header("Stereo Analysis")

        st.write(f"Stereo Width: {results['spatial']['stereo_width']}")
        st.write(f"Phase Correlation: {results['spatial']['phase_corr']}")
        st.write(f"Mono Compatibility: {results['spatial']['mono_compatibility']}")


        # ---------- SEGMENTATION ----------

        st.header("Track Segments")

        if len(results["segments"]) > 0:

            for s in results["segments"]:
                st.write(f"{round(float(s),2)} sec")

        else:

            st.write("No segments detected.")


        # ---------- PRIORITY ISSUE ----------

        st.header("Priority Issue")

        if results["priority"]:

            st.error(results["priority"]["type"])
            st.write(results["priority"]["fix"])

        else:

            st.success("No major issues detected")


        # ---------- SPECTRUM ----------

        st.header("Spectrum Comparison")

        st.image(plot)


        # ---------- ALL ISSUES ----------

        st.header("All Issues")

        if results["issues"]:

            for i in results["issues"]:
                st.warning(i["type"])

        else:

            st.success("No issues detected")


        # ---------- AI INSIGHTS ----------

        st.header("AI Mix Insights")

        if insights:

            for insight in insights:
                st.info(insight)

        else:

            st.success("No additional AI insights detected.")


    else:

        st.warning("Please upload both mix and reference track.")