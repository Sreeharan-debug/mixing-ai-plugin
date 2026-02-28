import numpy as np
import librosa
import matplotlib.pyplot as plt
import os


def analyze_mix(y1, sr1, y2, sr2, output_dir="outputs"):
    os.makedirs(output_dir, exist_ok=True)

    # ---------- FFT ----------
    def get_spectrum(y, sr):
        S = np.abs(librosa.stft(y, n_fft=2048))
        S_db = librosa.amplitude_to_db(S, ref=np.max)
        freqs = librosa.fft_frequencies(sr=sr)
        avg = np.mean(S_db, axis=1)
        return freqs, avg

    f1, s1 = get_spectrum(y1, sr1)
    f2, s2 = get_spectrum(y2, sr2)

    # ---------- Bands (SAFE) ----------
    def band_energy(freqs, spec, low, high):
        mask = (freqs >= low) & (freqs <= high)
        if np.sum(mask) == 0:
            return 0
        return np.mean(spec[mask])

    user_low = band_energy(f1, s1, 20, 120)
    user_mid = band_energy(f1, s1, 200, 500)
    user_high = band_energy(f1, s1, 2000, 5000)

    ref_low = band_energy(f2, s2, 20, 120)
    ref_mid = band_energy(f2, s2, 200, 500)
    ref_high = band_energy(f2, s2, 2000, 5000)

    # ---------- Scores ----------
    def score(user, ref):
        diff = abs(user - ref)
        return max(0, 100 - diff * 2)

    low_score = score(user_low, ref_low)
    mid_score = score(user_mid, ref_mid)
    high_score = score(user_high, ref_high)

    overall = (low_score + mid_score + high_score) / 3

    scores = {
        "low": round(low_score, 1),
        "mid": round(mid_score, 1),
        "high": round(high_score, 1),
        "overall": round(overall, 1),
        "match": round(overall, 1)
    }

    # ---------- INTELLIGENCE ----------
    issues = []

    mid_diff = user_mid - ref_mid
    if mid_diff > 2:
        confidence = min(100, abs(mid_diff) * 10)
        issues.append({
            "type": "Muddiness",
            "range": "200–500 Hz",
            "severity": "High" if confidence > 60 else "Medium",
            "confidence": round(confidence, 1),
            "why": "Too much energy in low-mids causes instruments to overlap.",
            "fix": "Reduce 250–400 Hz by 2–4 dB."
        })

    high_diff = ref_high - user_high
    if high_diff > 2:
        issues.append({
            "type": "Low Presence",
            "range": "2k–5k Hz",
            "severity": "Medium",
            "confidence": round(high_diff * 10, 1),
            "why": "Mix lacks clarity.",
            "fix": "Boost 3–5 kHz slightly."
        })

    low_diff = user_low - ref_low
    if abs(low_diff) > 3:
        issues.append({
            "type": "Low-End Imbalance",
            "range": "20–120 Hz",
            "severity": "Medium",
            "confidence": round(abs(low_diff) * 10, 1),
            "why": "Kick & bass conflict.",
            "fix": "Use sidechain or EQ separation."
        })

    priority = issues[0] if issues else None

    # ---------- PLOT ----------
    plt.figure(figsize=(10, 5))
    plt.semilogx(f1, s1, label="User Mix")
    plt.semilogx(f2, s2, label="Reference")

    plt.axvspan(20, 120, color='blue', alpha=0.1)
    plt.axvspan(200, 500, color='red', alpha=0.1)

    plt.title("Frequency Spectrum (Log Scale)")
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Amplitude (dB)")
    plt.legend()

    plot_path = os.path.join(output_dir, "spectrum.png")
    plt.savefig(plot_path)
    plt.close()

    return {
        "issues": issues,
        "priority": priority
    }, scores, plot_path