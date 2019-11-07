import record
import numpy as np
import scipy.io.wavfile as wav
from audio.processor import WavProcessor, format_predictions
from mic_array import MicArray

RESPEAKER_INDEX = 2  # refer to input device id
RESPEAKER_RATE = 16000
RESPEAKER_CHANNELS = 4

with WavProcessor() as proc:
    while True:
        smartsoundwave = record.record()
        (rate, sig) =  wav.read(smartsoundwave)
        if sig.dtype != np.int16:
            raise TypeError('Bad sample type: %r' % sig.dtype)

        predictions = proc.get_predictions(rate, sig)

        print(predictions)
        print(format_predictions(predictions))
