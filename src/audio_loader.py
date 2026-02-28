import librosa

def load_audio(file, sr=22050):
    y, sr = librosa.load(file, sr=sr, mono=True)
    return y, sr