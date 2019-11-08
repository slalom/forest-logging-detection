import numpy as np
import scipy.io.wavfile as wav
import time
import calendar
import wave
from audio.processor import WavProcessor, format_predictions
from mic_array import MicArray
from pixels import pixels

RATE = 16000
CHANNELS = 4
CHUNK_SIZE = 1024
CHUNK_LENGTH = 78

with WavProcessor() as proc:
    chunks = []

    try:
        with MicArray(RATE, CHANNELS, CHUNK_SIZE)  as mic:
            for chunk in mic.read_chunks():
                ts = calendar.timegm(time.gmtime())
                WAVE_OUTPUT_FILENAME = "smartsound_"+str(ts)+".wav"
                chunks.append(chunk)
                if len(chunks) == CHUNK_LENGTH:
                    frames = np.concatenate(chunks)

                    direction = mic.get_direction(frames)
                    pixels.wakeup(direction)

                    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
                    wf.setnchannels(CHANNELS)
                    wf.setframerate(RATE)
                    wf.setsampwidth(mic.pyaudio_instance.get_sample_size(mic.pyaudio_instance.get_format_from_width(2)))
                    wf.writeframes(b''.join(frames))
                    wf.close()

                    (rate, sig) =  wav.read(WAVE_OUTPUT_FILENAME)
                    if sig.dtype != np.int16:
                        raise TypeError('Bad sample type: %r' % sig.dtype)

                    predictions = proc.get_predictions(rate, sig)
                    prettyPrediction = format_predictions(predictions)

                    if (prettyPrediction):
                        print('Timestamp: {} | Detection: {} | Position: {}'.format(str(ts), prettyPrediction, int(direction)))

                    chunks = []

    except KeyboardInterrupt:
        pass
