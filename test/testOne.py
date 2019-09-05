import numpy as np
import predict
import os

file_name = os.path.join(os.path.dirname(__file__), '..', 'chainsaw', '04-1 Chainsaw.wav')
(predicted_class, predicted_proba, le) = predict.predict(file_name)
print("The predicted class is:", predicted_class, '\n')

for i in range(len(predicted_proba)):
    category = le.inverse_transform(np.array([i]))
    print(category[0], "\t\t : ", format(predicted_proba[i], '.32f'))
