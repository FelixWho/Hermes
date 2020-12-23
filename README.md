# Testing Speech to Text Libraries

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