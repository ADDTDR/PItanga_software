import pyaudio
import numpy as np
from scipy.fft import fft
import time 

BANDS = 4  # Number of frequency bands

CHUNK_SIZE = 512  # Size of audio chunks
SAMPLE_RATE = 22100  # Sample rate in Hz

audio_input = pyaudio.PyAudio()
stream = audio_input.open(format=pyaudio.paInt16, channels=1, rate=SAMPLE_RATE, input=True, frames_per_buffer=CHUNK_SIZE)


def calculate_fft(data):
    spectrum = np.abs(fft(data))[:len(data) // 2]
    bands = np.array_split(spectrum, BANDS)
    return bands



import matplotlib.pyplot as plt

while True:
    audio_data = stream.read(CHUNK_SIZE)
    audio_array = np.frombuffer(audio_data, dtype=np.int16)
    bands = calculate_fft(audio_array)

    print(bands)
    print('a')

    time.sleep(1)
    # Process and visualize the bands as needed
    # You can display the magnitude of each band using Matplotlib, for instance
    # plt.plot(bands)
    # plt.show(block=False)
    # plt.pause(0.1)
    # plt.clf()  # Clear the plot

stream.stop_stream()
stream.close()
audio_input.terminate()
