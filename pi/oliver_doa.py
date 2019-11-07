import sys
import numpy as np
import time
import calendar
import wave
from mic_array import MicArray
from pixels import pixels

RATE = 16000
CHANNELS = 4
VAD_FRAMES = 10     # ms
DOA_FRAMES = 5000    # ms

def main():
    chunks = []
    #doa_chunks = int(DOA_FRAMES / VAD_FRAMES)
    doa_chunks = 500

    try:
        with MicArray(RATE, CHANNELS, RATE * VAD_FRAMES / 1000)  as mic:
            for chunk in mic.read_chunks():
                ts = calendar.timegm(time.gmtime())
                WAVE_OUTPUT_FILENAME = "testsound_"+str(ts)+".wav"
                chunks.append(chunk)
                if len(chunks) == doa_chunks:
                    frames = np.concatenate(chunks)
                    direction = mic.get_direction(frames)
                    pixels.wakeup(direction)
                    print('\n{}'.format(int(direction)))
                    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
                    wf.setnchannels(4)
                    wf.setframerate(RATE)
                    wf.setsampwidth(mic.pyaudio_instance.get_sample_size(mic.pyaudio_instance.get_format_from_width(2)))
                    wf.writeframes(b''.join(frames))
                    wf.close()
                    print('\nwritten')

                    chunks = []

    except KeyboardInterrupt:
        pass

if __name__ == '__main__':
    main()
