import sys
import librosa
import librosa.display
import numpy as np
import matplotlib.pyplot as plt
from pydub import AudioSegment
import subprocess

#Creating a mel spectrogram using the librosa package and open-source pydub library

PATH = "./Queries/"
filename = 'convert.mp3'
filetype = filename[-3:]

def create_spectrogram(audio_path):
    y, sr = librosa.load(audio_path)
    audio, _ = librosa.effects.trim(y)
    tempo = librosa.beat.tempo(audio)
    librosa.display.waveplot(audio, sr=sr)
    spectrogram = librosa.feature.melspectrogram(audio, sr=sr, n_mels=200)
    spectrogram_decible = librosa.power_to_db(spectrogram, ref=np.max)
    librosa.display.specshow(spectrogram_decible, sr=sr)
    # plt.colorbar(format='%+2.0f dB')
    plt.show()
    return tempo


if filetype == 'mp3':
    #Convert to wav
    # try:
        # Opening file and extracting segment
        song = AudioSegment.from_file(PATH+filename, format='mp3', start_second=0, duration=30)

        # Saving
        song.export( filename[:-4]+'-snippet.wav', format="wav")
        wav_path = './{path}'.format(path=filename[:-4]+'-snippet.wav')
        print("hey")
        create_spectrogram(wav_path)
    # except:
    #     sys.exit("File does not exist")

elif filename[-3:] == 'wav':
    try:
        create_spectrogram("{path}{filename}".format(path=PATH, filename=filename))
    except:
        sys.exit("File does not exist")
else:
    sys.exit("Unsupported filetype, please input a .mp3 or .wav file")

