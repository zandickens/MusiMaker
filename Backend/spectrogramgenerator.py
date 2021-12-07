import sys
import librosa
import librosa.display
import numpy as np
import matplotlib.pyplot as plt
from pydub import AudioSegment
import subprocess

#Creating a mel spectrogram using the librosa package and open-source pydub library

def create_spectrogram(audio_path):
    y, sr = librosa.load(audio_path)
    audio, _ = librosa.effects.trim(y)
    tempo = librosa.beat.tempo(audio)
    librosa.display.waveplot(audio, sr=sr)
    spectrogram = librosa.feature.melspectrogram(audio, sr=sr, n_mels=200)
    spectrogram_decible = librosa.amplitude_to_db(spectrogram, ref=np.max)
    librosa.display.specshow(spectrogram_decible, sr=sr)
    # plt.colorbar(format='%+2.0f dB')
    plt.savefig(audio_path[:-11] + "spectrogram")
    # plt.show()
    return tempo

def generate_spectrogram(filename):
    filetype = filename[-3:]
    path = '../static/queries/'+filename + '/'
    filepath = path + filename
    print(path + filename,filetype)
    #Convert to wav

    # Opening file and extracting segment
    song = AudioSegment.from_file(filepath, format=filetype, start_second=0, duration=30)
    # Saving
    # wav_path = './{path}'.format(path=filename[:-4]+'-snippet.wav')
    wav_path = path+ '/' + filename[:-4]+'-snippet.wav'
    song.export(wav_path, format="wav")
    create_spectrogram(wav_path)
    # sys.exit("File does not exist")