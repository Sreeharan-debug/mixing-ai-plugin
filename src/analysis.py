import numpy as np
import librosa

def compute_spectrum(y, sr):
    S = np.abs(librosa.stft(y, n_fft=2048))
    S_db = librosa.amplitude_to_db(S, ref=np.max)
    freqs = librosa.fft_frequencies(sr=sr)
    avg_spectrum = np.mean(S_db, axis=1)
    return freqs, avg_spectrum


def band_energy(freqs, spectrum, low, high):
    mask = (freqs >= low) & (freqs <= high)
    return np.mean(spectrum[mask]) if np.any(mask) else -100


def score_band(user_val, ref_val):
    diff = abs(user_val - ref_val)
    score = max(0, 100 - diff * 2)
    return round(score, 1)


def analyze_mix(y1, sr1, y2, sr2):
    freqs1, spec1 = compute_spectrum(y1, sr1)
    freqs2, spec2 = compute_spectrum(y2, sr2)

    # Bands
    low_user = band_energy(freqs1, spec1, 20, 120)
    low_ref = band_energy(freqs2, spec2, 20, 120)

    lowmid_user = band_energy(freqs1, spec1, 200, 500)
    lowmid_ref = band_energy(freqs2, spec2, 200, 500)

    presence_user = band_energy(freqs1, spec1, 2000, 5000)
    presence_ref = band_energy(freqs2, spec2, 2000, 5000)

    # Scores
    low_score = score_band(low_user, low_ref)
    lowmid_score = score_band(lowmid_user, lowmid_ref)
    presence_score = score_band(presence_user, presence_ref)

    overall = round((low_score + lowmid_score + presence_score) / 3, 1)

    # Reference match (clean)
    ref_match = overall

    # Issues
    issues = []

    if lowmid_score < 70:
        issues.append("Low-Mid Muddiness (200–500 Hz)")

    if low_score < 70:
        issues.append("Weak or Boomy Low-End (20–120 Hz)")

    if presence_score < 70:
        issues.append("Lack of Presence (2k–5k Hz)")

    results = {
        "issues": issues,
        "reference_match": ref_match
    }

    scores = {
        "low": low_score,
        "lowmid": lowmid_score,
        "presence": presence_score,
        "overall": overall
    }

    return results, scores