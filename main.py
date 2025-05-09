from typing import Union
import librosa 
import librosa.display 
import matplotlib.pyplot as plt
from fastapi import FastAPI
import sounddevice as sd
import numpy as np
from scipy.signal import welch
from scipy.signal import get_window
import matplotlib.pyplot as plt
import sounddevice
# app = FastAPI()


# @app.get("/")
# def read_root():
#     return {"Hello": "World"}


# @app.get("/items/{item_id}")
# def read_item(item_id: int, q: Union[str, None] = None):
#     return {"item_id": item_id, "q": q}



# 1) 녹음 설정
samplerate = 22100  # 44.1 kHz 사람 귀 들리는 대부분 커버 
duration   = 5      # 초 단위 녹음 길이

print("녹음 시작...")
recording = sd.rec(int(samplerate * duration), samplerate=samplerate, channels=1, dtype='float32')
sd.wait()  # 녹음 완료 대기
signal = recording.flatten()
signal = signal - np.mean(signal) # 노이즈 제거 과정
print("녹음 완료")

# 2) 윈도우 적용 (예: Hamming)
window = np.hamming(len(signal))
windowed = signal * window

# 3) FFT
fft_vals = np.fft.rfft(windowed)
fft_amp  = np.abs(fft_vals)

# 4) 주파수 축 생성
freqs = np.fft.rfftfreq(len(windowed), d=1/samplerate)

# 5) 스펙트럼 플롯
plt.figure(figsize=(10, 4))
plt.plot(freqs, fft_amp)
plt.title("Bee Sound Spectrum")
plt.xlabel("Frequency [Hz]")
plt.ylabel("Amplitude")
plt.xlim(0, 500)  # Nyquist
plt.tight_layout()
plt.show()

# 6) 스펙토그램 (옵션)
plt.figure(figsize=(10, 4))
plt.specgram(signal, NFFT=1024, Fs=samplerate, noverlap=512, scale='dB')
plt.title("Bee Sound Spectrogram")
plt.xlabel("Time [s]")
plt.ylabel("Frequency [Hz]")
plt.colorbar(label="Intensity [dB]")
plt.tight_layout()
plt.show()