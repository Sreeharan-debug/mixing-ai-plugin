from analysis import analyze_mix
from audio_loader import load_audio


user = "user.wav"
ref = "ref.wav"

y1, sr1 = load_audio(user)
y2, sr2 = load_audio(ref)

results, scores, plot = analyze_mix(y1, sr1, y2, sr2)

print("Scores:", scores)
print("Issues:", results["issues"])