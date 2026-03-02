import numpy as np
import librosa
import matplotlib.pyplot as plt
import os
import pyloudnorm as pyln


def analyze_mix(y1, sr1, y2, sr2, output_dir="outputs"):
    os.makedirs(output_dir, exist_ok=True)

    # ---------- NORMALIZE ----------
    y1 = y1 / np.max(np.abs(y1))
    y2 = y2 / np.max(np.abs(y2))

    # ---------- SPECTRUM ----------
    def get_spectrum(y, sr):
        n_fft = 4096

        S = np.abs(librosa.stft(y, n_fft=n_fft))
        S_db = librosa.amplitude_to_db(S, ref=np.max)

        avg = np.mean(S_db, axis=1)
        avg = np.convolve(avg, np.ones(20)/20, mode='same')

        freqs = librosa.fft_frequencies(sr=sr, n_fft=n_fft)
        return freqs, avg

    f1, s1 = get_spectrum(y1, sr1)
    f2, s2 = get_spectrum(y2, sr2)

    # ---------- ALIGN ----------
    min_len = min(len(s1), len(s2))
    s1, s2 = s1[:min_len], s2[:min_len]
    f1 = f1[:min_len]

    # ---------- PERCEPTUAL ----------
    w = 1 / (1 + (f1 / 1000)**2)
    s1 *= w
    s2 *= w

    # ---------- BAND ENERGY ----------
    def band_energy(freqs, spec, low, high):
        mask = (freqs >= low) & (freqs <= high)
        if np.sum(mask) == 0:
            return 0
        return np.median(spec[mask])

    bands = {
        "sub": (20, 60),
        "low": (60, 120),
        "lowmid": (120, 400),
        "mid": (400, 2000),
        "presence": (2000, 5000),
        "air": (5000, 10000)
    }

    user_vals = {b: band_energy(f1, s1, *bands[b]) for b in bands}
    ref_vals = {b: band_energy(f1, s2, *bands[b]) for b in bands}

    # ---------- SCORE ----------
    def score(u, r):
        return max(0, 100 * np.exp(-abs(u - r) / 10))

    scores = {b: round(score(user_vals[b], ref_vals[b]), 1) for b in bands}
    scores["overall"] = round(np.mean(list(scores.values())), 1)
    scores["match"] = scores["overall"]

    # ---------- NORMALIZED DIFF ----------
    def norm_diff(u, r):
        return (u - r) / (abs(r) + 1e-6)

    diffs = {b: norm_diff(user_vals[b], ref_vals[b]) for b in bands}

    issues = []

    # ---------- CORE ISSUES ----------
    if diffs["lowmid"] > 0.15:
        issues.append({
            "type": "Muddiness",
            "range": "120–400 Hz",
            "severity": "High",
            "confidence": round(abs(diffs["lowmid"]) * 100, 1),
            "why": "Excess low-mid energy reduces clarity.",
            "fix": "Cut 200–350 Hz."
        })

    if abs(diffs["low"]) > 0.15:
        issues.append({
            "type": "Low-End Imbalance",
            "range": "60–120 Hz",
            "severity": "Medium",
            "confidence": round(abs(diffs["low"]) * 100, 1),
            "why": "Kick and bass are unbalanced.",
            "fix": "Use EQ or sidechain."
        })

    if diffs["presence"] < -0.15:
        issues.append({
            "type": "Low Presence",
            "range": "2k–5k Hz",
            "severity": "Medium",
            "confidence": round(abs(diffs["presence"]) * 100, 1),
            "why": "Mix lacks clarity.",
            "fix": "Boost 3–5 kHz."
        })

    # ---------- MASKING ----------
    def detect_masking(freqs, u, r):
        res = []
        diff = u - r

        regions = {
            "Low-Mid Masking": (120, 400),
            "Mid Masking": (400, 2000),
            "Presence Masking": (2000, 5000)
        }

        for name, (l, h) in regions.items():
            mask = (freqs >= l) & (freqs <= h)
            if np.sum(mask) == 0:
                continue

            d = np.mean(diff[mask])

            if d > 3:
                res.append({
                    "type": name,
                    "range": f"{l}–{h} Hz",
                    "severity": "High" if d > 6 else "Medium",
                    "confidence": round(d * 10, 1),
                    "why": "Frequency overlap causing masking.",
                    "fix": "Use EQ separation."
                })
        return res

    issues.extend(detect_masking(f1, s1, s2))

    # ---------- LUFS ----------
    meter = pyln.Meter(sr1)
    user_lufs = meter.integrated_loudness(y1)
    ref_lufs = meter.integrated_loudness(y2)

    if abs(user_lufs - ref_lufs) > 2:
        issues.append({
            "type": "Loudness Mismatch",
            "range": "Full",
            "severity": "High",
            "confidence": round(abs(user_lufs - ref_lufs) * 10, 1),
            "why": "Loudness differs from reference.",
            "fix": "Adjust limiter.",
            "value": f"{user_lufs:.1f} vs {ref_lufs:.1f} LUFS"
        })

    # ---------- PRIORITY ----------
    def rank(i):
        return (50 if i["severity"] == "High" else 30) + i["confidence"]

    issues = sorted(issues, key=rank, reverse=True)
    priority = issues[0] if issues else None

    # ---------- PLOT ----------
    diff_curve = s1 - s2

    plt.figure(figsize=(10, 5))
    plt.semilogx(f1, s1, label="User")
    plt.semilogx(f1, s2, label="Reference")
    plt.fill_between(f1, diff_curve, alpha=0.2)
    plt.legend()

    plot_path = os.path.join(output_dir, "spectrum.png")
    plt.savefig(plot_path)
    plt.close()

    return {"issues": issues, "priority": priority}, scores, plot_path