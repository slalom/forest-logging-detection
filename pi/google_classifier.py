import argparse
import numpy as np
import scipy.io.wavfile as wav
from audio.processor import WavProcessor, format_predictions

parser = argparse.ArgumentParser(description='Read file and process audio')
parser.add_argument('file_name', type=str, help='File to read and process')

def classify(file_name):

    (rate, sig) =  wav.read(file_name)
    if sig.dtype != np.int16:
        raise TypeError('Bad sample type: %r' % sig.dtype)

    with WavProcessor() as proc:
        predictions = proc.get_predictions(rate, sig)

    print(predictions)

if __name__ == '__main__':
    args = parser.parse_args()
    classify(**vars(args))