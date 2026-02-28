import numpy as np
import matplotlib.pyplot as plt
import os

# 🔥 Normalize audio (fix loudness bias)
def normalize_audio(y):
    max_val = np.max(np.abs(y))
    return y / max_val if max_val != 0 else y


def get_frequency_energy(y, sr):
    fft = np.abs(np.fft.rfft(y))
    freqs = np.fft.rfftfreq(len(y), 1/sr)
    return freqs, fft


def band_energy(freqs, fft, low, high):
    idx = np.where((freqs >= low) & (freqs <= high))
    return np.mean(fft[idx]) if len(idx[0]) > 0 else 0


def get_severity(confidence):
    if confidence < 30:
        return "Mild"
    elif confidence < 60:
        return "Moderate"
    else:
        return "Severe"


# 📊 Graph function
def plot_spectrum(freqs1, fft1, freqs2, fft2, output_path):
    plt.figure(figsize=(10, 6))

    plt.plot(freqs1, fft1, label="User Mix", alpha=0.7)
    plt.plot(freqs2, fft2, label="Reference", alpha=0.7)

    plt.xlim(20, 10000)
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Amplitude")
    plt.title("Frequency Spectrum Comparison")

    plt.legend()
    plt.grid()

    plt.savefig(output_path)
    plt.close()


def analyze_mix(y1, sr1, y2, sr2, output_dir):

    # 🔥 Normalize both signals
    y1 = normalize_audio(y1)
    y2 = normalize_audio(y2)

    freqs1, fft1 = get_frequency_energy(y1, sr1)
    freqs2, fft2 = get_frequency_energy(y2, sr2)

    report = []

    # 🎯 LOW-MID (Mud: 200–500 Hz)
    user_mud = band_energy(freqs1, fft1, 200, 500)
    ref_mud = band_energy(freqs2, fft2, 200, 500)

    mud_ratio = user_mud / ref_mud if ref_mud != 0 else 0

    if mud_ratio > 1.2:
        confidence = min((mud_ratio - 1.2) * 100, 100)
        severity = get_severity(confidence)

        report.append(
            f"Your mix has excessive low-mid energy (200–500 Hz), which may cause muddiness. "
            f"Try reducing 250–400 Hz on instruments like guitars, pads, or vocals. "
            f"(Confidence: {confidence:.1f}% | Severity: {severity})"
        )

    # 🎯 PRESENCE (2k–5k Hz)
    user_presence = band_energy(freqs1, fft1, 2000, 5000)
    ref_presence = band_energy(freqs2, fft2, 2000, 5000)

    presence_ratio = user_presence / ref_presence if ref_presence != 0 else 1

    if presence_ratio < 0.8:
        confidence = min((0.8 - presence_ratio) * 100, 100)
        severity = get_severity(confidence)

        report.append(
            f"Your mix has weaker presence (2k–5k Hz) than the reference, which may cause vocals or leads to feel less forward. "
            f"Try boosting around 2k–4k Hz slightly or reducing competing instruments. "
            f"(Confidence: {confidence:.1f}% | Severity: {severity})"
        )

    # 🎯 LOW END (20–120 Hz)
    user_low = band_energy(freqs1, fft1, 20, 120)
    ref_low = band_energy(freqs2, fft2, 20, 120)

    low_ratio = user_low / ref_low if ref_low != 0 else 0

    if low_ratio > 1.3:
        confidence = min((low_ratio - 1.3) * 100, 100)
        severity = get_severity(confidence)

        report.append(
            f"Your mix has excessive low-end (20–120 Hz), which may make it sound boomy or uncontrolled. "
            f"Try tightening the bass or using sidechain compression with the kick. "
            f"(Confidence: {confidence:.1f}% | Severity: {severity})"
        )

    # ✅ No issues fallback
    if not report:
        report.append("Your mix is well-balanced compared to the reference. No major issues detected.")

    # 📊 Generate graph
    graph_path = os.path.join(output_dir, "spectrum.png")
    plot_spectrum(freqs1, fft1, freqs2, fft2, graph_path)

    return report