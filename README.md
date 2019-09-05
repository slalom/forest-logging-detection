### IoT Hackathon - Chainsaw Sound detection

The Jupyter notebooks in the `train` folder have been based on Mike Smales' [repository](https://github.com/mikesmales/Udacity-ML-Capstone)


# Prerequisites

- Python 3.6
- Anaconda
- aws cli
- access to Slalom's sf-iot-hackathon S3 bucket


# Usage

## Setup

1. Create the conda environment: `make setup.conda.createEnv`
2. Download datafiles (5.6 GB): `make setup.download.dataSet`
3. (optional) Skip training and download models (1.5 MB): `make setup.download.models`

## Training the model

1. Start Jupyter notebooks: `jupyter notebook`
2. Run all the Notebooks in the train folder.
3. The models will be saved for further use in `train/saved_models`

## Test the model against chainsaw sounds

1. Test one file - `make test.one`
2. Test all chainsaw files and print stats - `make test.all`

## Run detection
1. `make run.detect`
2. Play drilling sounds. E.g. [this](https://youtu.be/gumMKccCS7U?t=150)