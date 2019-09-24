import record
import classify as classify
from simple_salesforce import Salesforce
import os

while True:
  sample = record.record()
  class_name = classify.classify(sample)
  if class_name == 'drilling':
    print('Drilling detected!')
    sf = Salesforce(username=os.environ['sf.username'], password=os.environ['sf.password'], security_token=os.environ['sf.token'])
    sf.Sound__c.create({'Predicted_Sound__c' : 'Chainsaw', 'Device_Number__c' : 'ABC123', 'Volume__c' : 26.72})