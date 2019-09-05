import sounddevice as sd
import librosa
import numpy as np
from keras.models import load_model
from sklearn.preprocessing import LabelEncoder
import os
import tensorflow as tf

tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)

model_file = os.path.join(os.path.dirname(__file__), '..', 'train', 'saved_models', 'weights.best.basic_cnn.hdf5')
model = load_model(model_file)
le = LabelEncoder()
classes_file = os.path.join(os.path.dirname(__file__), '..', 'train', 'saved_models', 'classes.npy')
le.classes_ = np.load(classes_file)

num_rows = 40
num_columns = 174
num_channels = 1
max_pad_len = 174


def classify(sample):
    mfccs = librosa.feature.mfcc(
        y=sample['data'], sr=sample['rate'], n_mfcc=40)
    pad_width = max_pad_len - mfccs.shape[1]
    mfccs = np.pad(mfccs, pad_width=((0, 0), (0, pad_width)), mode='constant')

    prediction_feature = mfccs.reshape(1, num_rows, num_columns, num_channels)

    predicted_vector = model.predict_classes(prediction_feature)
    predicted_class = le.inverse_transform(predicted_vector)
    return predicted_class[0]
