import librosa
import librosa.display
import IPython.display
import random
from librosa.feature.rhythm import tempogram
from scipy.io.wavfile import read            #read wav files
import os 
import cv2
import numpy as np
import matplotlib.pyplot as plt 
import tensorflow as tf
from keras.models import model_from_json


# LOADING A SAVED MODEL
def load_latest_model():
    json_file = open('model.json', 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    loaded_model = model_from_json(loaded_model_json)
    loaded_model.load_weights("model.h5")
    loaded_model.compile(loss='binary_crossentropy', optimizer='rmsprop', metrics=['accuracy'])
    return loaded_model

#Load Model
model = load_latest_model()
#Predict
genres = ["blues", "classical", "country", "disco", "hiphop", "jazz", "metal", "pop", "reggae", "rock"]

def prepImg(filepath):
    img_array = cv2.imread(filepath)
    new_array = cv2.resize(img_array, (432,288))
    return new_array.reshape(-1, 432, 288, 3)

FILENAME = './convert-spectogram.png'

prediction = model.predict(prepImg(FILENAME))
# print(prediction)
genreIndices = (-prediction[0]).argsort()[:2]
result_genres = [(genres[i], prediction[0][i]) for i in genreIndices]
print(result_genres)


y, sr = librosa.load('convert-snippet.wav')

#Add rounded values into seperate array as we need exact confidence later
sample_data = []
for genre in result_genres:
    sample_data.append((genre[0], round(150*genre[1])))    

sample_audio = []

for genre in sample_data:
    for samples in range(genre[1]):
        sample_audio.append('D:\\Downloads\\archive (1)\\Data\\genres_original\\{}\\{}.{:0>5d}.wav'.format(genre[0], genre[0], random.randint(0, 99)))

output_audio = None
n_samples = 0
for audio in sample_audio:
    current_y, current_sr = librosa.load(audio)
    if output_audio is None:
        output_audio = current_y*0
    # current_audio = librosa.feature.inverse.mel_to_audio(audio)    #returns audio
    try:
        output_audio += current_y
        n_samples += 1
    except:
        continue

# print(current_y)
# output_audio = output_audio / n_samples
print(output_audio/n_samples)
# print(y.max())
OUT_PATH = 'D:\\Downloads\\archive (1)\\Generation\\test.wav'

audio, _ = librosa.effects.trim(output_audio)

spec = librosa.feature.melspectrogram(output_audio, sr=sr, n_mels=255)
spectrogram_decible = librosa.amplitude_to_db(spec, ref=np.max)
librosa.display.specshow(spectrogram_decible, sr=sr)
# spec = librosa.feature.melspectrogram(output_audio, sr=sr)
#librosa.display.specshow(spec)
plt.savefig('D:\\Downloads\\archive (1)\\Generation\\test.png')
plt.show()

# IPython.display.Audio(data=current_y, rate=22050,autoplay=True)

    #2 options here:
        #1 - convert current audio to chroma or stft to adjust frequencies then convert back to audio series (more percise)

        #2 - 
            #final_audio = current_audio * 0
            #final_audio += current_audio / 100
            # literally just average all data and return an averaged song
    