import pyaudio
import wave
import calendar
import time
import math
import numpy as np
from pixels import pixels
from gcc_phat import gcc_phat

# run getDeviceInfo.py to get index
RESPEAKER_INDEX = 2  # refer to input device id
RESPEAKER_RATE = 16000
RESPEAKER_CHANNELS = 4 
RESPEAKER_WIDTH = 2
CHUNK = 1024
RECORD_SECONDS = 5
# 4-array
MIC_GROUP_N = 2
MIC_GROUP = [[0, 2], [1, 3]]
SOUND_SPEED = 343.2
MIC_DISTANCE_4 = 0.08127
MAX_TDOA_4 = MIC_DISTANCE_4 / float(SOUND_SPEED)

CHUNK_LEN = int(RESPEAKER_RATE / CHUNK * RECORD_SECONDS)
MID_CHUNK = int(CHUNK_LEN / 2)

def get_direction(buf):
    best_guess = None
    tau = [0] * MIC_GROUP_N
    theta = [0] * MIC_GROUP_N
    for i, v in enumerate(MIC_GROUP):
        tau[i], _ = gcc_phat(buf[v[0]::4], buf[v[1]::4], fs=RESPEAKER_RATE, max_tau=MAX_TDOA_4, interp=1)
        theta[i] = math.asin(tau[i] / MAX_TDOA_4) * 180 / math.pi

    if np.abs(theta[0]) < np.abs(theta[1]):
        if theta[1] > 0:
            best_guess = (theta[0] + 360) % 360
        else:
            best_guess = (180 - theta[0])
    else:
        if theta[0] < 0:
            best_guess = (theta[1] + 360) % 360
        else:
            best_guess = (180 - theta[1])

        best_guess = (best_guess + 270) % 360

    best_guess = (-best_guess + 120) % 360
    return best_guess

def record():
    ts = calendar.timegm(time.gmtime())
    WAVE_OUTPUT_FILENAME = "smartsound_"+str(ts)+".wav"

    p = pyaudio.PyAudio()

    stream = p.open(
        rate=RESPEAKER_RATE,
        #format=p.get_format_from_width(RESPEAKER_WIDTH),
        format=pyaudio.paInt16,
        channels=RESPEAKER_CHANNELS,
        input=True,
        input_device_index=RESPEAKER_INDEX,)

    print("* recording " + WAVE_OUTPUT_FILENAME)
    frames = []
    chunks = [] 
    for i in range(0, CHUNK_LEN):
        data = stream.read(CHUNK)
        a = np.fromstring(data,dtype=np.int16)[0::4]
        frames.append(a.tostring())
        if (i <= MID_CHUNK):
            chunks.append(a)
            
    chunkBuffer = np.concatenate(chunks)
    direction = get_direction(chunkBuffer)
    pixels.wakeup(direction)
    print('\n{}'.format(direction))

    stream.stop_stream()
    stream.close()

    print("* done recording " + WAVE_OUTPUT_FILENAME)
    p.terminate()

    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(1)
    wf.setsampwidth(p.get_sample_size(p.get_format_from_width(RESPEAKER_WIDTH)))
    wf.setframerate(RESPEAKER_RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

    return WAVE_OUTPUT_FILENAME

def main():
    record()

if __name__ == '__main__':
    main()
