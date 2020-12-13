# -*- coding: utf-8 -*-
import pyaudio
import wave
import numpy as np
import time
timeout = time.time() + 19*3600
import warnings
warnings.filterwarnings('ignore')
def Monitor():
    CHUNK = 2048
    FORMAT = pyaudio.paInt16
    CHANNELS = 4
    RATE = 44100
    WAVE_OUTPUT_FILENAME = "cache.wav"
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)
    print("start caching records")
    frames = []
    l2 = 0
    l1 = 0
    th = 0
    data = stream.read(CHUNK)
    data_tmp = data
    while (time.time() < timeout):
        for i in range(0, 100):
            data = stream.read(CHUNK)
            audio_data = np.fromstring(data, dtype=np.short)
            if max(audio_data)>150:
                th = 1
            else:
                th = 0
            if th == 1:
                if l1 == 1:
                    frames.append(data)
                if l1 == 0:
                    if l2 == 1:
                        frames.append(data)   
                    if l2 == 0:
                        frames.append(data_tmp)
                        frames.append(data)
            else:
                if l1 == 1:
                    frames.append(data)
            l2 = l1
            l1 = th
            th = 0
            data_tmp = data
    stream.stop_stream()
    stream.close()
    p.terminate()
    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()
 
if __name__ == '__main__':
    Monitor()
