# 🎧 AI Mixing Assistant

> **Reference-based mix analysis with intelligent audio insights**
> Not just analysis — this helps you *fix your mix like a pro.*

---

## 🚀 What is this?

**AI Mixing Assistant** is a smart audio analysis tool that compares your mix against a reference track and tells you:

* 🎯 What’s wrong
* 🧠 Why it’s wrong
* 🔧 How to fix it

This is not auto-mixing.
This is **learning + decision support for producers.**

---

## ✨ Features

### 🎚️ Spectrum Analysis

* Log-scale frequency comparison
* User vs Reference visualization
* Highlighted problem regions

### 🧠 AI Mix Insights (Core Feature)

* Detects:

  * Low-end imbalance (20–120 Hz)
  * Muddiness (200–500 Hz)
  * Presence issues (2k–5k Hz)
* Gives:

  * Severity
  * Confidence
  * Explanation
  * Fix suggestions

### 📊 Mix Scoring System

* Low-End Score
* Low-Mid Score
* Presence Score
* Overall Score
* Reference Match %

### 🎯 Priority Fix System

* Highlights the **most important issue first**
* Helps producers focus on what matters

---

## 🖥️ Demo UI

* Upload your mix + reference
* Click **Analyze**
* Get:

  * Mix scores
  * Visual spectrum
  * AI insights

---

## 🛠️ Tech Stack

* Python 🐍
* Streamlit ⚡
* Librosa 🎵
* NumPy
* Matplotlib

---

## 📂 Project Structure

```
mixing-ai-plugin/
│
├── src/
│   ├── app.py              # Streamlit UI
│   ├── analysis.py         # Core intelligence engine
│   ├── audio_loader.py     # Audio processing
│
├── outputs/                # Generated spectrum plots
├── README.md
└── requirements.txt
```

---

## ⚙️ Installation

```bash
git clone https://github.com/YOUR_USERNAME/mixing-ai-plugin.git
cd mixing-ai-plugin

python -m venv venv
venv\Scripts\activate   # Windows

pip install -r requirements.txt
```

---

## ▶️ Run the App

```bash
streamlit run src/app.py
```

Open in browser:

```
http://localhost:8501
```

---

## 🧠 How it Works

1. Convert audio → frequency spectrum (FFT)
2. Split into perceptual bands:

   * Low (20–120 Hz)
   * Low-Mid (200–500 Hz)
   * Presence (2k–5k Hz)
3. Compare with reference track
4. Generate:

   * Scores
   * Differences
   * AI-based insights

---

## 📈 Current Version

**v2.2 — Intelligence Layer**

✅ Spectrum analysis
✅ Reference matching
✅ Smart scoring
✅ AI insights (WHY + FIX)

---

## 🔮 Roadmap

### 🔜 v3 (Next Phase)

* Chat-based assistant (“Why is my mix bad?”)
* Better masking detection
* Genre-aware analysis

### 🚀 Future Vision

* DAW Plugin (VST)
* Real-time mix feedback
* ML-based perception modeling

---

## 💡 Why this matters

Most tools show you data.

This tool tells you:

> **what to do with that data**

---

## 🤝 Contributing

Open to collaborations, especially in:

* Audio engineering
* Machine learning
* Plugin development

---

## 📬 Contact

**Sreeharan M Anilkumar**
🎵 Audio + AI Builder

---

## ⭐ If you like this project

Give it a star — it helps a lot 🚀

---
