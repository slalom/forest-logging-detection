import sys
import numpy as np
import time
import calendar
import wave
from mic_array import MicArray
from pixels import pixels

RATE = 16000
CHANNELS = 4
CHUNK_SIZE = 1024
CHUNK_LENGTH = 78

def main():
    chunks = []

    try:
        with MicArray(RATE, CHANNELS, CHUNK_SIZE)  as mic:
            for chunk in mic.read_chunks():
                ts = calendar.timegm(time.gmtime())
                WAVE_OUTPUT_FILENAME = "testsound_"+str(ts)+".wav"
                #print('per chunk size:{}'.format(len(chunk)))
                chunks.append(chunk)
                #print('length of chunks:{}'.format(len(chunks)))
                if len(chunks) == CHUNK_LENGTH:
                    frames = np.concatenate(chunks)
                    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
                    wf.setnchannels(4)
                    wf.setframerate(RATE)
                    wf.setsampwidth(mic.pyaudio_instance.get_sample_size(mic.pyaudio_instance.get_format_from_width(2)))
                    wf.writeframes(b''.join(frames))
                    wf.close()

                    direction = mic.get_direction(frames)
                    pixels.wakeup(direction)
                    print('\n{}'.format(int(direction)))

                    chunks = []

    except KeyboardInterrupt:
        pass

if __name__ == '__main__':
    main()
