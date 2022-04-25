from fileinput import filename
import sys
import librosa
import librosa.display
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from pydub import AudioSegment
import subprocess
import os

#Creating a mel spectrogram using the librosa package and open-source pydub library
def get_song_logistics(y,sr):
    duration = librosa.get_duration(y=y,sr=sr)
    onset_env = librosa.onset.onset_strength(y, sr=sr)
    tempo = librosa.beat.tempo(onset_envelope=onset_env, sr=sr)
    return {'duration':duration,'tempo':list(tempo)[0]}

def create_spectrogram(audio_path, song_name, audio_parent_path):
    y, sr = librosa.load(audio_path)
    audio, _ = librosa.effects.trim(y)
    librosa.display.waveshow(audio, sr=sr)
    spectrogram = librosa.feature.melspectrogram(audio, sr=sr, n_mels=200)
    spectrogram_decible = librosa.amplitude_to_db(spectrogram, ref=np.max)
    librosa.display.specshow(spectrogram_decible, sr=sr)
    # plt.colorbar(format='%+2.0f dB')
    plt.margins(0)
    plt.savefig(audio_parent_path / f"{song_name}-spectrogram.png", bbox_inches='tight', pad_inches=0)
    return [y,sr]

def generate_spectrogram(file_path):
    plt.close()
    file_name = file_path.split('/')[-1]
    file_type = file_name.split('.')[1]
    song_name = file_name.split('.')[0]
    file_path = os.path.abspath(file_path)

    file_parent_path = Path('\\'.join(file_path.split('\\')[:-1]))
    print(file_path,file_name,file_type,song_name, file_parent_path)
    # Opening file and extracting segment
    if file_name.endswith('.mp3') or file_name.endswith('.MP3'): 
        song = AudioSegment.from_mp3(file_path)
    elif file_name.endswith('.wav') or file_name.endswith('.WAV'): 
        song = AudioSegment.from_wav(file_path)

    # song = AudioSegment.from_file(file_path, format=file_type, start_second=0, duration=20)
    print("SEGMENTED YOOOOOOOOOO")
    # Saving
    # wav_path = './{path}'.format(path=file_name[:-4]+'-snippet.wav')
    wav_path = Path(file_parent_path) / Path(song_name +'-snippet.wav')
    song.export(wav_path, format="wav")
    vals = create_spectrogram(wav_path, song_name, file_parent_path)
    return get_song_logistics(vals[0],vals[1])
    # sys.exit("File does not exist") 