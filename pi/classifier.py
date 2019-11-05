import numpy as np
import librosa
from keras.models import load_model
from sklearn.preprocessing import LabelEncoder
import os
import tensorflow as tf
import scipy.io.wavfile as wav

tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)

model_file = os.path.join(os.path.dirname(__file__), 'models', 'weights.best.basic_cnn.hdf5')
model = load_model(model_file)
le = LabelEncoder()
classes_file = os.path.join(os.path.dirname(__file__), 'models', 'classes.npy')
le.classes_ = np.load(classes_file)

num_rows = 40
num_columns = 174 
num_channels = 1
max_pad_len = 174

def extract_features(wave_name):
    try:
        (rate, sig) =  wav.read(wave_name)
        mfccs = librosa.feature.mfcc(y=sig, sr=rate, n_mfcc=40)
        pad_width = max_pad_len - mfccs.shape[1]
        mfccs = np.pad(mfccs, pad_width=((0, 0), (0, pad_width)), mode='constant')
    except Exception as e:
        print("Error encountered while parsing file: ", wave_name, e)
        return None

    return mfccs

def classify(file_name):
    prediction_feature = extract_features(file_name)
    print (prediction_feature.shape)
    prediction_feature = prediction_feature.reshape(
        1, num_rows, num_columns, num_channels)

    predicted_vector = model.predict_classes(prediction_feature)
    predicted_class = le.inverse_transform(predicted_vector)

    predicted_proba_vector = model.predict_proba(prediction_feature)
    predicted_proba = predicted_proba_vector[0]
    return (predicted_class[0], predicted_proba, le)