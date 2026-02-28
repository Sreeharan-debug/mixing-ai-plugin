# 🎧 AI Mixing Assistant (V1.5)

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
* 🎯 Visual problem zone highlighting (low-end & mud regions)

---

## 🧠 How It Works

1. Loads user mix and reference track
2. Normalizes audio for fair comparison
3. Performs frequency analysis (FFT)
4. Detects imbalances in key frequency bands
5. Generates human-readable insights
6. Visualizes spectrum with highlighted problem zones

---

## 📊 Sample Output

### 🎧 Analysis Report

* Your mix has excessive low-mid energy (200–500 Hz), which may cause muddiness.
  Try reducing 250–400 Hz on instruments like guitars, pads, or vocals.
  *(Confidence: 18.8% | Severity: Mild)*

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
* `data/output/spectrum.png` → Spectrum visualization with highlighted zones

---

## 📌 Version

**V1.5 — Visual Intelligence + Problem Zone Highlighting**

---

## 🎯 Vision

To build an **AI-powered mix mentor** that helps producers understand their mixes through clear, contextual, and actionable feedback — raising the overall quality of music production.

---
