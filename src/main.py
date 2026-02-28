import os
from audio_loader import load_audio
from analysis import analyze_mix

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

INPUT_DIR = os.path.join(BASE_DIR, "data", "input")
OUTPUT_DIR = os.path.join(BASE_DIR, "data", "output")

USER_FILE = os.path.join(INPUT_DIR, "user.wav")
REF_FILE = os.path.join(INPUT_DIR, "ref.wav")


def main():
    y1, sr1 = load_audio(USER_FILE)
    y2, sr2 = load_audio(REF_FILE)

    results, scores, plot_path = analyze_mix(y1, sr1, y2, sr2, OUTPUT_DIR)

    print("\n🎧 MIX ANALYSIS REPORT:\n")

    if results["priority"]:
        p = results["priority"]
        print(f"🎯 Priority Issue: {p['type']} ({p['range']})")
        print(f"Why: {p['why']}")
        print(f"Fix: {p['fix']}\n")
    else:
        print("✅ No major issues detected\n")

    print("--- MIX SCORES ---")
    print(f"Low-End: {scores['low']}")
    print(f"Low-Mid: {scores['mid']}")
    print(f"Presence: {scores['high']}")
    print(f"\nOverall: {scores['overall']}")
    print(f"Reference Match: {scores['match']}%")

    print(f"\n📊 Spectrum saved at: {plot_path}")


if __name__ == "__main__":
    main()