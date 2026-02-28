import os
from audio_loader import load_audio
from analysis import analyze_mix

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

INPUT_DIR = os.path.join(BASE_DIR, "data", "input")
OUTPUT_DIR = os.path.join(BASE_DIR, "data", "output")

USER_FILE = os.path.join(INPUT_DIR, "user.wav")
REF_FILE = os.path.join(INPUT_DIR, "ref.wav")
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "report.txt")


def main():
    y1, sr1 = load_audio(USER_FILE)
    y2, sr2 = load_audio(REF_FILE)

    results = analyze_mix(y1, sr1, y2, sr2, OUTPUT_DIR)

    print("\n🎧 MIX ANALYSIS REPORT:\n")

    # 🔥 Clean formatted output
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        for r in results:
            if r.startswith("---") or r.startswith("\n---"):
                print(r.strip())
                f.write(r.strip() + "\n")
            elif r.strip() == "":
                continue
            else:
                print("- " + r)
                f.write("- " + r + "\n")


if __name__ == "__main__":
    main()