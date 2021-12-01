import sys
import librosa
import librosa.display
import numpy as np
import matplotlib.pyplot as plt
from pydub import AudioSegment
import subprocess

PATH = "./Queries/"
filename = 'convert.mp3'
filetype = filename[-3:]
AudioSegment.converter = "C:\\Tools\\ffmpeg\\bin"

def create_spectrogram(audio_path):
    y, sr = librosa.load(audio_path)
    # trim silent edges
    audio, _ = librosa.effects.trim(y)
    librosa.display.waveplot(audio, sr=sr)


    n_fft = 2048
    # D = np.abs(librosa.stft(audio[:n_fft], n_fft=n_fft, hop_length=n_fft+1))
    # plt.plot(D);

    hop_length = 512
    # D = np.abs(librosa.stft(audio, n_fft=n_fft,  hop_length=hop_length))
    # librosa.display.specshow(D, sr=sr, x_axis='time', y_axis='linear');
    # plt.colorbar();

    # DB = librosa.amplitude_to_db(D, ref=np.max)
    # librosa.display.specshow(DB, sr=sr, hop_length=hop_length, x_axis='time', y_axis='log');
    # plt.colorbar(format='%+2.0f dB');


    spectrogram = librosa.feature.melspectrogram(audio, sr=sr, n_fft=n_fft, hop_length=hop_length, n_mels=90)
    spectrogram_decible = librosa.power_to_db(spectrogram, ref=np.max)
    librosa.display.specshow(spectrogram_decible, sr=sr, hop_length=hop_length)
    # plt.colorbar(format='%+2.0f dB')
    plt.show()


if filetype == 'mp3':
    #Convert to wav
    # try:
    # sound = AudioSegment.from_mp3("{path}{filename}".format(path=PATH, filename=filename))
    # sound = AudioSegment.from_mp3("convert.mp3")
    subprocess.call(['ffmpeg','-t','30','convert.mp3', 'convert.mp3', '-y'])
    subprocess.call(['ffmpeg','-i','convert.mp3','convert.wav'])
    

    # startTime = 10 * 1000
    # endTime = 40 * 1000
    # snippet = sound[startTime:endTime]

    wav_path = "{path}{wav_filename}".format(path=PATH, wav_filename=filename[:-3] + "wav")
    # sound.export(wav_path, format="wav")
    create_spectrogram(wav_path)
    # except:
    #     sys.exit("File does not exist")

elif filename[-3:] == 'wav':
    # try:
    create_spectrogram("{path}{filename}".format(path=PATH, filename=filename))
    # except:
    #     sys.exit("File does not exist")
else:
    sys.exit("Unsupported filetype, please input a .mp3 or .wav file")

