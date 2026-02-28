import numpy as np
import matplotlib.pyplot as plt
import os

# 🔥 Normalize audio
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


def smooth(data, window_size=100):
    return np.convolve(data, np.ones(window_size)/window_size, mode='same')


def get_severity(confidence):
    if confidence < 30:
        return "Mild"
    elif confidence < 60:
        return "Moderate"
    else:
        return "Severe"


# 🔥 Convert ratio → score
def get_score(ratio, ideal=1.0):
    diff = abs(ratio - ideal)
    score = max(0, 100 - diff * 100)
    return min(score, 100)


# 📊 Smart graph (V1.6+)
def plot_spectrum(freqs1, fft1, freqs2, fft2, output_path,
                  show_low=False, low_intensity=0.1,
                  show_mud=False, mud_intensity=0.1):

    fft1 = smooth(fft1)
    fft2 = smooth(fft2)

    plt.figure(figsize=(10, 6))

    plt.plot(freqs1, fft1, label="User Mix", alpha=0.8)
    plt.plot(freqs2, fft2, label="Reference", alpha=0.8)

    plt.xscale("log")
    plt.xlim(20, 10000)

    if show_low:
        plt.axvspan(20, 120, alpha=low_intensity, label="Low-End Issue")

    if show_mud:
        plt.axvspan(200, 500, alpha=mud_intensity, label="Mud Issue")

    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Amplitude")
    plt.title("Smart Frequency Spectrum Analysis")

    plt.legend()
    plt.grid(True, which="both", linestyle="--", linewidth=0.5)

    plt.savefig(output_path)
    plt.close()


def analyze_mix(y1, sr1, y2, sr2, output_dir):

    y1 = normalize_audio(y1)
    y2 = normalize_audio(y2)

    freqs1, fft1 = get_frequency_energy(y1, sr1)
    freqs2, fft2 = get_frequency_energy(y2, sr2)

    report = []

    show_low = False
    show_mud = False
    low_intensity = 0.1
    mud_intensity = 0.1

    # 🎯 LOW-END
    user_low = band_energy(freqs1, fft1, 20, 120)
    ref_low = band_energy(freqs2, fft2, 20, 120)
    low_ratio = user_low / ref_low if ref_low != 0 else 0

    low_score = get_score(low_ratio)

    if low_ratio > 1.3:
        confidence = min((low_ratio - 1.3) * 100, 100)
        severity = get_severity(confidence)

        show_low = True
        low_intensity = min(0.1 + confidence / 200, 0.5)

        report.append(
            f"Low-End issue: Excess energy (20–120 Hz). "
            f"(Confidence: {confidence:.1f}% | Severity: {severity})"
        )

    # 🎯 LOW-MID (Mud)
    user_mud = band_energy(freqs1, fft1, 200, 500)
    ref_mud = band_energy(freqs2, fft2, 200, 500)
    mud_ratio = user_mud / ref_mud if ref_mud != 0 else 0

    mud_score = get_score(mud_ratio)

    if mud_ratio > 1.2:
        confidence = min((mud_ratio - 1.2) * 100, 100)
        severity = get_severity(confidence)

        show_mud = True
        mud_intensity = min(0.1 + confidence / 200, 0.5)

        report.append(
            f"Low-Mid issue: Muddiness (200–500 Hz). "
            f"(Confidence: {confidence:.1f}% | Severity: {severity})"
        )

    # 🎯 PRESENCE
    user_presence = band_energy(freqs1, fft1, 2000, 5000)
    ref_presence = band_energy(freqs2, fft2, 2000, 5000)
    presence_ratio = user_presence / ref_presence if ref_presence != 0 else 1

    presence_score = get_score(presence_ratio)

    if presence_ratio < 0.8:
        confidence = min((0.8 - presence_ratio) * 100, 100)
        severity = get_severity(confidence)

        report.append(
            f"Presence issue: Weak vocals/leads (2k–5k Hz). "
            f"(Confidence: {confidence:.1f}% | Severity: {severity})"
        )

    # 🔥 SCORES
    report.append("\n--- MIX SCORES ---")
    report.append(f"Low-End Score: {low_score:.1f}/100")
    report.append(f"Low-Mid Score: {mud_score:.1f}/100")
    report.append(f"Presence Score: {presence_score:.1f}/100")

    overall_score = (low_score + mud_score + presence_score) / 3
    report.append(f"\nOverall Mix Score: {overall_score:.1f}/100")

    # 🔥 V1.8 FEATURE
    match_percent = overall_score
    report.append(f"Reference Match: {match_percent:.1f}%")

    # 📊 GRAPH
    graph_path = os.path.join(output_dir, "spectrum.png")

    plot_spectrum(
        freqs1, fft1, freqs2, fft2, graph_path,
        show_low=show_low,
        low_intensity=low_intensity,
        show_mud=show_mud,
        mud_intensity=mud_intensity
    )

    return report