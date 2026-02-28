# 🎧 AI Mixing Assistant

> AI-powered mix analysis tool that helps producers identify tonal issues, compare with reference tracks, and improve mix quality through intelligent feedback.

---

## 🚀 Live Concept

Upload your mix → Compare with reference → Get actionable insights in seconds.

---

## 🧠 Why This Exists

Most producers struggle with:
- ❌ Muddy mixes  
- ❌ Poor low-end balance  
- ❌ Weak presence  
- ❌ No clear feedback  

This tool solves that by acting like a **virtual mix engineer** — analyzing your track and pointing out what needs fixing.

---

## ✨ Core Features

### 🎯 Intelligent Mix Diagnostics
- Detects:
  - Low-end imbalance (20–120 Hz)
  - Low-mid muddiness (200–500 Hz)
  - Presence clarity (2k–5k Hz)

---

### 📊 Multi-Band Scoring Engine
- Low-End Score  
- Low-Mid Score  
- Presence Score  
- **Overall Mix Score**

---

### 🎧 Reference Track Matching
- Compare your mix with professional tracks  
- Get a **Reference Match %**

---

### 📈 Spectrum Visualization
- Log-scale frequency analysis  
- Smoothed curves (human-perception based)  
- Highlighted problem zones  

---

### ⚡ Instant Feedback UI
- Upload `.wav` files  
- One-click analysis  
- Clean, real-time dashboard  

---

## ⚡ Quick Start (Plug & Play)

### 1. Clone Repo
```bash
git clone https://github.com/Sreeharan-debug/mixing-ai-plugin.git
cd mixing-ai-plugin
2. Setup Environment
python -m venv venv

Activate:

Windows (CMD):

venv\Scripts\activate
3. Install Dependencies
pip install librosa numpy matplotlib streamlit soundfile
4. Run App
streamlit run src/app.py
5. Open in Browser
http://localhost:8501
🧪 Example Output
🎧 MIX ANALYSIS REPORT:

- Low-Mid issue: Muddiness (200–500 Hz)

--- MIX SCORES ---
Low-End: 91.0
Low-Mid: 61.2
Presence: 99.4

Overall: 83.9
Reference Match: 83.9%
📁 Project Structure
mixing-ai-plugin/
│
├── src/
│   ├── app.py              # Streamlit UI
│   ├── analysis.py         # Core analysis engine
│   ├── audio_loader.py     # Audio processing
│   └── main.py             # CLI version
│
├── outputs/                # Generated files (ignored)
├── temp/                   # Temp files (ignored)
│
├── .gitignore
├── README.md
🛠️ Tech Stack

Python

Librosa

NumPy

Matplotlib

Streamlit

🚀 Current Version

V2.2 — Accuracy Upgrade

Fixed spectrum scaling (true dB)

Improved frequency smoothing

More reliable scoring system

Clean architecture (UI vs analysis separation)

🧭 Roadmap
🔜 V2.3

Perceptual weighting (human hearing model)

Advanced masking detection

Smarter issue prioritization

🔥 Future Vision

AI Chat Mixing Assistant

ML-based mix evaluation

Cloud-based mix analysis

VST / DAW Plugin

🎯 Vision

To build an AI-powered mixing assistant that:

Teaches producers why their mix sounds wrong

Provides real-time feedback

Bridges the gap between beginners and professional engineers

👨‍💻 Author

Sreeharan M Anilkumar

Audio Engineer

AI Developer

Building tools for the next generation of producers

⭐ Contributing

Open to ideas, feedback, and collaboration.

📌 License

MIT License