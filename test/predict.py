from keras.models import load_model
from sklearn.preprocessing import LabelEncoder
import librosa
import numpy as np
import tensorflow as tf

tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)

model = load_model('train/saved_models/weights.best.basic_cnn.hdf5')
le = LabelEncoder()
le.classes_ = np.load('train/saved_models/classes.npy')

num_rows = 40
num_columns = 174
num_channels = 1
max_pad_len = 174


def extract_features(file_name):
    try:
        audio, sample_rate = librosa.load(
            file_name, res_type='kaiser_fast', duration=4)
        mfccs = librosa.feature.mfcc(y=audio, sr=sample_rate, n_mfcc=40)
        pad_width = max_pad_len - mfccs.shape[1]
        mfccs = np.pad(mfccs, pad_width=(
            (0, 0), (0, pad_width)), mode='constant')

    except Exception as e:
        print("Error encountered while parsing file: ", file_name, e)
        return None

    return mfccs


def predict(file_name):
    prediction_feature = extract_features(file_name)
    prediction_feature = prediction_feature.reshape(
        1, num_rows, num_columns, num_channels)

    predicted_vector = model.predict_classes(prediction_feature)
    predicted_class = le.inverse_transform(predicted_vector)

    predicted_proba_vector = model.predict_proba(prediction_feature)
    predicted_proba = predicted_proba_vector[0]
    return (predicted_class[0], predicted_proba, le)