import record
import classifier

while True:
    smartsoundwave = record.record()
    (class_name, prob) = classifier.classify(smartsoundwave)
    f = open("inference.txt", "a")
    output = '{}:{}:{}'.format(smartsoundwave,class_name,prob)
    f.write(output)
    f.close()