import record
import classifier
import google_classifier
import warnings
#from simple_salesforce import Salesforce 

while True:
    smartsoundwave = record.record()
    #(class_name, prob) = classifier.classify(smartsoundwave)
    predictions = google_classifier.classify(smartsoundwave)

   
    #f = open("inference.txt", "a")
    #if (prob[4] > 0.999):
    #    output = '{}\n'.format("Chainsaw noise detected!")
        # sf = Salesforce(username='iothackathon@slalom.com', password='Lucy2019!', security_token='Mi5Efyth7eJFjW5BEEFVCCMnq')
        # sf.Sound__c.create({'Predicted_Sound__c' : 'Chainsaw', 'Device_Number__c' : 'ABC123', 'Volume__c' : 26.72})
    #    f.write(output)
    #f.close()
