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
AudioSegment.converter = "C:\\Tools\\ffmpeg\\bin"

def create_spectrogram(audio_path):
    y, sr = librosa.load(audio_path)
    audio, _ = librosa.effects.trim(y)
    librosa.display.waveplot(audio, sr=sr)
    n_fft = 2048
    hop_length = 512

    #Create a Mel Spectrogram using the librosa library
    spectrogram = librosa.feature.melspectrogram(audio, sr=sr, n_fft=n_fft, hop_length=hop_length, n_mels=90)
    spectrogram_decible = librosa.power_to_db(spectrogram, ref=np.max)
    librosa.display.specshow(spectrogram_decible, sr=sr, hop_length=hop_length)
    plt.show()


if filetype == 'mp3':
    #Convert to wav
    #WIP: working to fix pydub library issues

    # sound = AudioSegment.from_mp3("{path}{filename}".format(path=PATH, filename=filename))
    # sound = AudioSegment.from_mp3("convert.mp3")
    subprocess.call(['ffmpeg','-t','30','convert.mp3', 'convert.mp3', '-y'])
    subprocess.call(['ffmpeg','-i','convert.mp3','convert.wav'])
    wav_path = "{path}{wav_filename}".format(path=PATH, wav_filename=filename[:-3] + "wav")
    # sound.export(wav_path, format="wav")
    create_spectrogram(wav_path)


elif filename[-3:] == 'wav':
    create_spectrogram("{path}{filename}".format(path=PATH, filename=filename))

else:
    sys.exit("Unsupported filetype, please input a .mp3 or .wav file")

