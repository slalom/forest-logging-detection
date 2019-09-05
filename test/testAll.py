import numpy as np
import predict
import os
import pandas as pd

directory = os.path.join(os.path.dirname(__file__), '..', 'chainsaw')

predictions = []

for file_name in os.listdir(directory):
  (predicted_class, predicted_proba, le) = predict.predict(os.path.join(directory, file_name))
  predictions.append(predicted_class)

df = pd.DataFrame(predictions, columns=['class_name'])

print(df.class_name.value_counts(normalize=True))