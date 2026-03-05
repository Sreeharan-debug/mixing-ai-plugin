import librosa
import numpy as np

def load_audio(path, sr=44100):

    y, sr = librosa.load(path, sr=sr, mono=False)

    if y.ndim == 1:
        y = np.expand_dims(y, axis=0)

    return y, sr