import pyaudio
import wave
import calendar
import time
import numpy as np

RESPEAKER_RATE = 16000
RESPEAKER_CHANNELS = 4 
RESPEAKER_WIDTH = 2
# run getDeviceInfo.py to get index
RESPEAKER_INDEX = 2  # refer to input device id
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

    print("* done recording " + WAVE_OUTPUT_FILENAME)

    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    #wf.setnchannels(RESPEAKER_CHANNELS)
    wf.setnchannels(1)
    wf.setsampwidth(p.get_sample_size(p.get_format_from_width(RESPEAKER_WIDTH)))
    wf.setframerate(RESPEAKER_RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

    return WAVE_OUTPUT_FILENAME