import pyaudio
import wave
import calendar
import time
import numpy as np
from mic_array import MicArray
from pixel_ring import pixel_ring

# run getDeviceInfo.py to get index
RESPEAKER_INDEX = 2  # refer to input device id
RESPEAKER_RATE = 16000
RESPEAKER_CHANNELS = 4 
RESPEAKER_WIDTH = 2
CHUNK = 1024
RECORD_SECONDS = 5

def record():
    ts = calendar.timegm(time.gmtime())
    WAVE_OUTPUT_FILENAME = "smartsound_"+str(ts)+".wav"

    p = pyaudio.PyAudio()

    stream = p.open(
        rate=RESPEAKER_RATE,
        format=p.get_format_from_width(RESPEAKER_WIDTH),
        channels=RESPEAKER_CHANNELS,
        input=True,
        input_device_index=RESPEAKER_INDEX,)

    print("* recording " + WAVE_OUTPUT_FILENAME)
    frames = []

    for i in range(0, int(RESPEAKER_RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        a = np.fromstring(data,dtype=np.int16)[0::4]
        #frames.append(data)
        frames.append(a.tostring())

    stream.stop_stream()
    stream.close()

    print("* done recording " + WAVE_OUTPUT_FILENAME)
    p.terminate()

    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    #wf.setnchannels(RESPEAKER_CHANNELS)
    wf.setnchannels(1)
    wf.setsampwidth(p.get_sample_size(p.get_format_from_width(RESPEAKER_WIDTH)))
    wf.setframerate(RESPEAKER_RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

    #chunks = []
    #with MicArray(RESPEAKER_RATE, RESPEAKER_CHANNELS, RESPEAKER_RATE / RESPEAKER_CHANNELS) as mic:
    #    for chunk in mic.read_chunks():
    #        chunks.append(chunk)
    #        chunkframes = np.concatenate(chunks)
    #        direction = mic.get_direction(chunkframes)
    #        pixel_ring.set_direction(direction)
    #        print('\n{}'.format(int(direction)))
    #        mic.stop()

    return WAVE_OUTPUT_FILENAME

def main():
    record()

if __name__ == '__main__':
    main()
