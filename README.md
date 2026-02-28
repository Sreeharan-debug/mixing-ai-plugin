# 🎧 AI Mixing Assistant (V1.9)

## 🧠 Overview

AI-powered tool that analyzes your mix by comparing it with a reference track and provides intelligent, human-readable feedback.

This project focuses on **explainable mix diagnostics** — not auto-mixing — helping producers understand *why* their mix sounds off and *how to fix it*.

---

## 🚀 Features

* 🎚️ Mix vs Reference comparison
* 📊 Frequency-based issue detection
* 📉 Confidence & severity scoring
* 💡 Actionable suggestions (what to fix)
* 🎛️ Smoothed + log-scale spectrum visualization (plugin-style)
* 🎯 Smart problem zone highlighting (context-aware)
* 📊 Multi-band scoring system
* 🧠 Overall mix quality score
* 🔥 Reference match percentage
* 🎧 Masking detection (kick/bass & vocal regions)

---

## 🧠 How It Works

1. Loads user mix and reference track
2. Normalizes audio for fair comparison
3. Performs frequency analysis (FFT)
4. Detects imbalances in key frequency bands
5. Identifies masking between elements
6. Generates human-readable insights
7. Assigns scores to each frequency band
8. Calculates overall mix quality score
9. Computes similarity to reference (match %)
10. Visualizes spectrum with intelligent highlighting

---

## 📊 Sample Output

### 🎧 Analysis Report

* Low-Mid issue: Muddiness (200–500 Hz)
  *(Confidence: 18.8% | Severity: Mild)*

---

### 📊 Mix Scores

* Low-End Score: 91.0/100
* Low-Mid Score: 61.2/100
* Presence Score: 99.4/100

**Overall Mix Score: 83.9/100**
**Reference Match: 83.9%**

---

### 📈 Spectrum Graph

![Spectrum](data/output/spectrum.png)

---

## 🛠️ Tech Stack

* Python
* Librosa
* NumPy
* Matplotlib

---

## ▶️ How to Run

```bash
python src/main.py
```

---

## 📁 Output

* `data/output/report.txt` → Analysis report
* `data/output/spectrum.png` → Spectrum visualization with smart highlighting

---

## 📌 Version

**V1.9 — Masking Detection + Intelligent Mix Evaluation**

---

## 🎯 Vision

To build an **AI-powered mix mentor** that helps producers understand their mixes through clear, contextual, and actionable feedback — raising the overall quality of music production.

---
