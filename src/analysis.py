import numpy as np
import librosa
import matplotlib.pyplot as plt
import pyloudnorm as pyln


# ---------- UTILITIES ----------

def to_mono(y):
    return np.mean(y, axis=0)


def smooth_spectrum(spec, window=15):

    kernel = np.ones(window) / window
    return np.convolve(spec, kernel, mode="same")


# ---------- PERCEPTUAL WEIGHTING ----------

def perceptual_weight(freqs):

    weights = np.ones_like(freqs)

    for i, f in enumerate(freqs):

        if f < 100:
            weights[i] = 0.6
        elif f < 400:
            weights[i] = 0.8
        elif f < 4000:
            weights[i] = 1.2
        elif f < 10000:
            weights[i] = 1.0
        else:
            weights[i] = 0.8

    return weights


# ---------- SPECTRUM ----------

def compute_spectrum(y, sr):

    S = np.abs(librosa.stft(y, n_fft=4096))

    S = np.mean(S, axis=1)

    S = librosa.amplitude_to_db(S)

    freqs = librosa.fft_frequencies(sr=sr, n_fft=4096)

    S = smooth_spectrum(S)

    return freqs, S


# ---------- MULTIBAND ----------

def band_energy(freqs, spec, low, high):

    mask = (freqs >= low) & (freqs <= high)

    return np.mean(spec[mask])


def multiband_analysis(freqs, user_spec, ref_spec):

    bands = {
        "sub": (20, 60),
        "low": (60, 120),
        "low_mid": (120, 400),
        "mid": (400, 2000),
        "presence": (2000, 6000),
        "air": (6000, 16000)
    }

    scores = {}

    for name, (lo, hi) in bands.items():

        u = band_energy(freqs, user_spec, lo, hi)
        r = band_energy(freqs, ref_spec, lo, hi)

        diff = abs(u - r)

        score = max(0, 100 - diff * 3)

        scores[name] = round(score, 1)

    return scores


# ---------- WEIGHTED OVERALL SCORE ----------

def weighted_score(scores):

    weights = {
        "sub": 0.15,
        "low": 0.2,
        "low_mid": 0.2,
        "mid": 0.2,
        "presence": 0.15,
        "air": 0.1
    }

    total = 0

    for band in weights:

        total += scores[band] * weights[band]

    return round(total, 1)


# ---------- MASKING DETECTION ----------

def masking_detection(freqs, user_spec):

    mask_regions = []

    low_mid_energy = band_energy(freqs, user_spec, 200, 400)

    mid_energy = band_energy(freqs, user_spec, 1000, 3000)

    if low_mid_energy > mid_energy + 6:

        mask_regions.append({
            "type": "Low-Mid Masking",
            "fix": "Reduce 200-400Hz congestion"
        })

    high_energy = band_energy(freqs, user_spec, 4000, 7000)

    if high_energy > 0:

        if high_energy > mid_energy + 10:

            mask_regions.append({
                "type": "Harsh Presence",
                "fix": "Reduce 4-6kHz"
            })

    return mask_regions


# ---------- DYNAMICS ----------

def dynamic_analysis(y, sr):

    meter = pyln.Meter(sr)

    loudness = meter.integrated_loudness(y)

    rms = np.sqrt(np.mean(y**2))
    peak = np.max(np.abs(y))

    crest = peak / (rms + 1e-8)

    return {
        "crest_factor": round(crest, 2),
        "lufs": round(loudness, 2)
    }


# ---------- STEREO ----------

def stereo_analysis(y):

    L = y[0]
    R = y[1]

    mid = (L + R) / 2
    side = (L - R) / 2

    width = np.mean(side**2) / (np.mean(mid**2) + 1e-8)

    phase = np.corrcoef(L, R)[0, 1]

    mono = 100 - np.mean(np.abs(side)) * 100

    return {
        "stereo_width": round(width, 3),
        "phase_corr": round(phase, 3),
        "mono_compatibility": round(mono, 2)
    }


# ---------- SEGMENTATION ----------

def segmentation(y, sr):

    onset_env = librosa.onset.onset_strength(y=y, sr=sr)

    frames = librosa.onset.onset_detect(onset_envelope=onset_env, sr=sr)

    times = librosa.frames_to_time(frames, sr=sr)

    return times[:10]


# ---------- SPECTRUM PLOT ----------

def plot_spectrum(freqs, user_spec, ref_spec):

    plt.figure(figsize=(10, 5))

    plt.semilogx(freqs, user_spec, label="User")
    plt.semilogx(freqs, ref_spec, label="Reference")

    plt.xlabel("Frequency (Hz)")
    plt.ylabel("dB")

    plt.title("Spectrum Comparison")

    plt.legend()

    path = "spectrum.png"

    plt.savefig(path)

    plt.close()

    return path


# ---------- MAIN ENGINE ----------

def analyze_mix(y1, sr1, y2, sr2):

    user = to_mono(y1)
    ref = to_mono(y2)

    freqs, user_spec = compute_spectrum(user, sr1)
    _, ref_spec = compute_spectrum(ref, sr2)

    scores = multiband_analysis(freqs, user_spec, ref_spec)

    overall = weighted_score(scores)

    scores["overall"] = overall
    scores["match"] = overall

    dynamics = dynamic_analysis(user, sr1)

    spatial = stereo_analysis(y1)

    segments = segmentation(user, sr1)

    masking = masking_detection(freqs, user_spec)

    issues = masking

    priority = issues[0] if issues else None

    plot = plot_spectrum(freqs, user_spec, ref_spec)

    results = {
        "dynamics": dynamics,
        "spatial": spatial,
        "segments": segments,
        "issues": issues,
        "priority": priority
    }

    return results, scores, plot