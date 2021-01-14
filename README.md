# Training Text2Speech Using DeepSpeech

## AMI Scripts

Will require pydub, ffmpeg

    python split_audio.py AMI_WAV_PATH AMI_LABELS OUTPUT_DIRECTORY # splits AMI audio into chunks of about 15 seconds

## TalkBank CallHome Scripts

Will require pydub, ffmpeg
    
    python split_audio.py TALKBANK_MP3_PATH CHA_LABELS_PATH OUTPUT_DIRECTORY

## Universal Scripts

    python combine_csv.py INPUT_DIRECTORY # finds all csvs in DIRECTORY and outputs combined.csv

    python randomize_csv.py CSV_PATH # randomizes csv rows

    python split_csv.py CSV_PATH OUTPUT_DIRECTORY # split data into 70-15-15

## Training the DeepSpeech Model

Note: this repo's scripts create data with 16000hz sample rate. It is recommended to have all audio files with this sample rate.

    git clone --branch v0.9.3 https://github.com/mozilla/DeepSpeech
    cd DeepSpeech
    mkdir training_csvs
    mkdir fine_tuning_checkpoints
    mkdir output_models

- Add the unzipped checkpoint to fine_tuning_checkpoints
  
- Add the csv files to training_csvs

```
python3 DeepSpeech.py --n_hidden 2048 --checkpoint_dir fine_tuning_checkpoints/deepspeech-0.9.3-checkpoint --epochs 3 --train_files training_csvs/train.csv --dev_files training_csvs/dev.csv --test_files training_csvs/test.csv --learning_rate 0.0001 --export_dir output_models --load_cudnn
```

## Using the DeepSpeech model

### Requirements (Windows version, only diff is how to create the virtualenv)

    # Create and activate virtualenv
    python -m venv ./tmp/deepspeech-venv/
    .\tmp\deepspeech-venv\Scripts\activate

    pip3 install deepspeech

### Usage

    deepspeech --model MODEL_PATH --audio AUDIO_FILE_PATH.wav