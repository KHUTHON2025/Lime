import sounddevice as sd
import numpy as np
import matplotlib.pyplot as plt
import queue
import requests

# 파라미터
samplerate = 22100   # 샘플링 레이트
duration   = 5       # 윈도우 길이 (초)
threshold  = 60     # Alert 임계 진폭
low_f, high_f = 80, 160  # 관심 대역 (Hz)

sound_detect_queue = queue.Queue()

def detect_sound():
    # 1) 녹음
    print(f"\n▶ 다음 {duration}초간 녹음합니다...")
    recording = sd.rec(int(samplerate*duration),
                    samplerate=samplerate, channels=1, dtype='float32')
    sd.wait()
    signal = recording.flatten()
    signal -= np.mean(signal)  # DC 제거

    # 2) 윈도우 적용
    window = np.hamming(len(signal))
    windowed = signal * window

    print("window")
    # 3) FFT
    fft_vals = np.fft.rfft(windowed)
    fft_amp  = np.abs(fft_vals)
    freqs    = np.fft.rfftfreq(len(windowed), d=1/samplerate)
    print("fft")

    # 4) 관심 대역 분석
    mask      = (freqs >= low_f) & (freqs <= high_f)
    band_amps = fft_amp[mask]
    band_freq = freqs[mask]
    max_amp   = band_amps.max()
    max_freq  = band_freq[band_amps.argmax()]
    print("width")

    # 5) Alert 여부
    if max_amp > threshold:
        print(f"🚨 Alert! {max_freq:.1f} Hz 대역에서 진폭 {max_amp:.1f} 감지 (임계치={threshold})")
        sound_detect_queue.put_nowait("1")

    else:
        print(f"정상: {low_f}–{high_f} Hz 구간 최대 진폭 {max_amp:.1f}")

    # (원하면 여기서 플롯을 띄울 수도 있지만, 루프가 중단될 때까지 계속 기록만 합니다.)
    print("end")

if __name__ == "__main__":
    try:
        while True:
            # 1) 녹음
            print(f"\n▶ 다음 {duration}초간 녹음합니다...")
            recording = sd.rec(int(samplerate*duration),
                            samplerate=samplerate, channels=1, dtype='float32')
            sd.wait()
            signal = recording.flatten()
            signal -= np.mean(signal)  # DC 제거

            # 2) 윈도우 적용
            window = np.hamming(len(signal))
            windowed = signal * window

            print("window")
            # 3) FFT
            fft_vals = np.fft.rfft(windowed)
            fft_amp  = np.abs(fft_vals)
            freqs    = np.fft.rfftfreq(len(windowed), d=1/samplerate)
            print("fft")

            # 4) 관심 대역 분석
            mask      = (freqs >= low_f) & (freqs <= high_f)
            band_amps = fft_amp[mask]
            band_freq = freqs[mask]
            max_amp   = band_amps.max()
            max_freq  = band_freq[band_amps.argmax()]
            print("width")

            # 5) Alert 여부
            if max_amp > threshold:
                #sound_detect_queue.put_nowait("1")
                requests.get("http://localhost:8000/sound_detect")
                print(f"🚨 Alert! {max_freq:.1f} Hz 대역에서 진폭 {max_amp:.1f} 감지 (임계치={threshold})")
            else:
                print(f"정상: {low_f}–{high_f} Hz 구간 최대 진폭 {max_amp:.1f}")

            # (원하면 여기서 플롯을 띄울 수도 있지만, 루프가 중단될 때까지 계속 기록만 합니다.)
            print("end")
    except KeyboardInterrupt:
        print("\n루프를 중단했습니다. 프로그램을 종료합니다.")
