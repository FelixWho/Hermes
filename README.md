# Testing Speech to Text Libraries

## AMI Scripts

Will require pydub, ffmpeg

    python split_audio.py AMI_WAV_PATH.wav AMI_LABELS.xml OUTPUT_DIRECTORY # splits AMI audio into chunks of about 15 seconds

## Universal Scripts

    python randomize_csv.py CSV_PATH.csv # randomizes csv rows

    python split_csv.py CSV_PATH.csv OUTPUT_DIRECTORY # split data into 70-15-15

## Automatic-Speech-Recognition

### Requirements

    pip install automatic-speech-recognition

### Usage

    python Automatic-Speech-Recognition.py

## DeepSpeech

### Requirements (Windows, only diff is how to create the virtualenv)

    # Create and activate virtualenv
    python -m venv ./tmp/deepspeech-venv/
    .\tmp\deepspeech-venv\Scripts\activate

    pip3 install deepspeech

    curl -LO https://github.com/mozilla/DeepSpeech/releases/download/v0.9.3/deepspeech-0.9.3-models.pbmm
    curl -LO https://github.com/mozilla/DeepSpeech/releases/download/v0.9.3/deepspeech-0.9.3-models.scorer

### Usage

    deepspeech --model deepspeech-0.9.3-models.pbmm --scorer deepspeech-0.9.3-models.scorer --audio AUDIO_FILE_PATH.wav