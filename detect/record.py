import sounddevice as sd


def record():
    fs = 22050
    duration = 4

    recording = sd.rec(duration * fs, samplerate=fs, channels=1, dtype='float64').ravel()
    sd.wait()
    return {'data': recording, 'rate': fs}
