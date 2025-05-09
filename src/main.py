from typing import Union
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from model import gen_frames, detect_queue
import asyncio
#import firebase

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

@app.get("/video_feed")
def video_feed():
    return StreamingResponse(
        gen_frames(),
        #detect_loop(),
        media_type="multipart/x-mixed-replace; boundary=frame"
    )

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