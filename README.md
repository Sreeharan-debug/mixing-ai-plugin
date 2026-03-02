# 🎧 AI Mixing Assistant

An intelligent audio analysis tool that helps producers improve their mixes using perceptual analysis, reference comparison, and explainable insights.

---

## 🚀 Features

### 🎧 Perceptual Audio Analysis
- Frequency analysis aligned with human hearing
- Smoothed spectrum for stable results

### 📊 Multi-Band Scoring
- Sub (20–60 Hz)
- Low (60–120 Hz)
- Low-Mid (120–400 Hz)
- Mid (400–2k Hz)
- Presence (2k–5k Hz)
- Air (5k–10k Hz)

### 🧠 Intelligent Feedback
- Detects:
  - Muddiness
  - Low-end imbalance
  - Low presence
- Provides:
  - Explanation (WHY)
  - Actionable fix (HOW)

### ⚡ Masking Detection
Identifies frequency clashes where instruments overlap and lose clarity.

### 🔊 Loudness Analysis (LUFS)
Compares perceived loudness with reference tracks.

### 🎯 Priority Engine
Ranks issues based on severity and confidence to guide workflow.

### 📉 Spectrum Visualization
- Log-scale spectrum
- Difference highlighting

---

## 🖥️ Demo (Local)

```bash
pip install -r requirements.txt
streamlit run src/app.py

📂 Project Structure

plugin/
│
├── src/
│   ├── app.py
│   ├── analysis.py
│   ├── audio_loader.py
│
├── outputs/
├── requirements.txt
└── README.md


⚠️ Status

🚧 Pre-release (V2.6)

Core engine is stable, but still evolving.

🧠 Vision

To build an intelligent mixing assistant that:
Analyzes mixes like an engineer
Explains problems clearly
Helps users learn, not just fix

🚀 Roadmap

V3
AI Chat Assistant
Interactive explanations
V4
Stereo + Phase Analysis
Dynamic range detection
Future
DAW Plugin (VST)
Cloud-based analysis

👨‍💻 Author

Sreeharan M Anilkumar