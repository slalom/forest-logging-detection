import numpy as np
import scipy.io.wavfile as wav
import time
import calendar
import wave
import seeed_dht
import requests,json
from audio.processor import WavProcessor, format_predictions
from mic_array import MicArray
from pixels import pixels
from collections import deque, Counter

RATE = 16000
CHANNELS = 4
CHUNK_SIZE = 1024
CHUNK_LENGTH = 78

with WavProcessor() as proc:
    chunks = []
    chainsawQ = deque([0,0,0,0,0,0,0,0])
    createCase = 0

    try:
        with MicArray(RATE, CHANNELS, CHUNK_SIZE)  as mic:
            for chunk in mic.read_chunks():
                ts = calendar.timegm(time.gmtime())
                WAVE_OUTPUT_FILENAME = "smartsound_"+str(ts)+".wav"
                chunks.append(chunk)
                if len(chunks) == CHUNK_LENGTH:
                    frames = np.concatenate(chunks)

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
                    
                    lowerP = prettyPrediction.lower()
                    recognizable = "vehicle" in lowerP or "chainsaw" in lowerP or "car" in lowerP or "lawn" in lowerP or "animal" in lowerP or "manmade" in lowerP
                    containsChainsaw = "chainsaw" in lowerP

                    headers = {'Content-Type': 'application/json'}
                    endpoint = 'http://192.168.1.1:3000'

                    if (prettyPrediction and recognizable):
                        direction = mic.get_direction(frames)
                        pixels.wakeup(direction)
                        sensor = seeed_dht.DHT("22", 12)
                        humi, temp = sensor.read()

                        chainsawQ.popleft()
                        if (containsChainsaw):
                            chainsawQ.append(1)
                        else:
                            chainsawQ.append(0)

                        if not humi is None:
                            print('Timestamp: {0} | Detection: {1} | Position: {2} | Humidity {3:.1f}% | Temperature {4:.1f}'.format(str(ts), prettyPrediction, int(direction), humi, temp))
                        else:
                            print('Timestamp: {} | Detection: {} | Position: {}'.format(str(ts), prettyPrediction, int(direction)))

                        chainsawSum = sum(chainsawQ)
                        print('queue:{}, sum:{}'.format(chainsawQ, chainsawSum))

                        if (chainsawSum >= 3):
                            print('Chainsaw occurred multiple times. File Case!')
                            createCase = 1
                        else:
                            createCase = 0

                        body = {'Predicted_Sound__c': prettyPrediction, 'Device_Number__c': 'ABC123', 'Position__c': int(direction), 'Temperature__c': round(temp, 2), 'Humidity__c': round(humi, 2), 'Create_Case__c': createCase}
                        #requests.post(endpoint,data=json.dumps(body),headers=headers)

                        if (chainsawSum >= 3):
                            chainsawQ = deque([0,0,0,0,0,0,0,0])
                    else:
                        print('Timestamp: {} | Unrecognizable noise'.format(str(ts)))

                    chunks = []

    except KeyboardInterrupt:
        pass
