import automatic_speech_recognition as asr

pipeline = asr.load('deepspeech2', lang='en')
pipeline.model.summary()     # TensorFlow model

#file = './Testing/sample.wav'  # sample rate 16 kHz, and 16 bit depth
file = input("Enter file name, NA to quit: ")
while file != "NA":
    sample = asr.utils.read_audio('.\Testing\sample1.wav')
    sentences = pipeline.predict([sample])
    print(sentences)
    file = input("Enter file name, NA to quit: ")
