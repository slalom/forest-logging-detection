import record
import classify as classify

while True:
  sample = record.record()
  class_name = classify.classify(sample)
  if class_name == 'drilling':
    print('Drilling detected!')