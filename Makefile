setup.env:
	pipenv install

setup.download.dataSet:
	aws s3 cp s3://sf-iot-hackathon/UrbanSound8K.tar.gz . && \
	tar xf UrbanSound8K.tar.gz && \
	aws s3 cp s3://sf-iot-hackathon/chainsaw.tar.gz . && \
	tar xf chainsaw.tar.gz

setup.download.models:
	mkdir -p train/saved_models && \
	aws s3 cp s3://sf-iot-hackathon/weights.best.basic_cnn.hdf5 train/saved_models/weights.best.basic_cnn.hdf5 && \
	aws s3 cp s3://sf-iot-hackathon/classes.npy train/saved_models/classes.npy

test.one:
	python test/testOne.py

test.all:
	python test/testAll.py

run.detect:
	python detect/detect.py