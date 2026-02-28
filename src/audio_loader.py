import librosa

def load_audio(file_path):
    y, sr = librosa.load(file_path, sr=None, mono=True)
    return y, sr