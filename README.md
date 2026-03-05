# 🎧 AI Mixing Diagnostic Engine

An AI-assisted audio mixing diagnostic tool that analyzes a mix
against a reference track and identifies tonal imbalance, masking,
dynamic issues, and stereo field problems.

The system combines digital signal processing with a rule-based
intelligence layer to generate actionable mix feedback.

---

## 🚀 Features

• Multiband tonal analysis
• Reference track comparison
• Masking detection
• Dynamic analysis (LUFS + crest factor)
• Stereo field analysis
• Spectrum comparison visualization
• AI-generated mix insights

---
## ARCHITECTURE
Audio
 ↓
audio_loader.py
 ↓
analysis.py (DSP engine)
 ↓
intelligence.py (AI reasoning)
 ↓
app.py (Streamlit interface)

---

## 🖥️ Demo (Local)

```bash
pip install -r requirements.txt
streamlit run src/app.py

📂 Project Structure

project/
│
├── analysis.py        # DSP analysis engine
├── intelligence.py    # AI reasoning layer
├── audio_loader.py    # Audio IO
├── app.py             # Streamlit UI
├── main.py            # CLI test
├── requirements.txt
└── README.md


⚠️ Status

release (V3.0)

Core engine is stable, but still evolving.

🧠 Vision

To build an intelligent mixing assistant that:
Analyzes mixes like an engineer
Explains problems clearly
Helps users learn, not just fix

🚀 Roadmap

V4
Future
DAW Plugin (VST)
Cloud-based analysis

👨‍💻 Author

Sreeharan M Anilkumar