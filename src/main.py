from typing import Union
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from model import gen_frames, detect_queue, undetect_queue
from geoex import get_address_by_id, get_detect_url
from sound import detect_sound
import asyncio
import uuid
#import firebase

app = FastAPI()
app.state.test = 0
@app.get("/")
def read_root(q: Union[str, None] = None):
    return {"status": "success"}

@app.get("/hive/{id}")
def read_item(id: int):
    return {"hive_id": id, "address":get_address_by_id(id), "live_url": f"https://calf-exact-anteater.ngrok-free.app/video_feed?={uuid.uuid4()}","detect_url": get_detect_url(id)}

@app.get("/video_feed")
def video_feed():
    return StreamingResponse(
        gen_frames(),
        #detect_loop(),
        media_type="multipart/x-mixed-replace; boundary=frame"
    )

@app.get("/voice")
def voice():
    return {"status":detect_sound()}

@app.get("/detect")
async def detect():
    """
    SSE 형식으로 감지 이벤트를 스트리밍합니다.
    클라이언트는 EventSource로 아래와 같은 형태의 메시지를 수신.
    """
    async def event_generator():
        loop = asyncio.get_event_loop()
        while True:
            # 큐에 메시지가 들어올 때까지 대기 (블로킹 작업을 threadpool로)
            msg = await loop.run_in_executor(None, detect_queue.get)
            # SSE 포맷: data: 메시지\n\n
            yield f"data: {msg}\n\n"

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream"
    )

@app.get("/detectt")
async def detectt():
    """
    SSE 형식으로 감지 이벤트를 스트리밍합니다.
    클라이언트는 EventSource로 아래와 같은 형태의 메시지를 수신.
    """
    async def event_generator():
        loop = asyncio.get_event_loop()
        while True:
            # 큐에 메시지가 들어올 때까지 대기 (블로킹 작업을 threadpool로)
            msg = await loop.run_in_executor(None, undetect_queue.get)
            # SSE 포맷: data: 메시지\n\n
            yield f"data: {msg}\n\n"

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream"
    )

# 추가 작업
# import sounddevice as sd
# import numpy as np
# import queue


# def detect_sound():
#     # 파라미터
#     samplerate = 22100   # 샘플링 레이트
#     duration   = 5       # 윈도우 길이 (초)
#     threshold  = 60     # Alert 임계 진폭
#     low_f, high_f = 80, 160  # 관심 대역 (Hz)

#     while True:
#         # 1) 녹음
#         print(f"\n▶ 다음 {duration}초간 녹음합니다...")
#         recording = sd.rec(int(samplerate*duration),
#                         samplerate=samplerate, channels=1, dtype='float32')
#         sd.wait()
#         signal = recording.flatten()
#         signal -= np.mean(signal)  # DC 제거

#         # 2) 윈도우 적용
#         window = np.hamming(len(signal))
#         windowed = signal * window

#         print("window")
#         # 3) FFT
#         fft_vals = np.fft.rfft(windowed)
#         fft_amp  = np.abs(fft_vals)
#         freqs    = np.fft.rfftfreq(len(windowed), d=1/samplerate)
#         print("fft")

#         # 4) 관심 대역 분석
#         mask      = (freqs >= low_f) & (freqs <= high_f)
#         band_amps = fft_amp[mask]
#         band_freq = freqs[mask]
#         max_amp   = band_amps.max()
#         max_freq  = band_freq[band_amps.argmax()]
#         print("width")

#         # 5) Alert 여부
#         if max_amp > threshold:
#             print(f"🚨 Alert! {max_freq:.1f} Hz 대역에서 진폭 {max_amp:.1f} 감지 (임계치={threshold})")
#             app.state.test = 100
#         else:
#             print(f"정상: {low_f}–{high_f} Hz 구간 최대 진폭 {max_amp:.1f}")
# asyncio.create_task(detect_sound())
           