import cv2, threading, time

# 1) 전역 카메라 + 프레임 버퍼
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    raise RuntimeError("카메라 열기 실패")

latest_frame = None
frame_lock = threading.Lock()

def capture_loop():
    global latest_frame
    while True:
        ret, frame = cap.read()
        if not ret:
            continue
        # 모델 속도를 위해,, 해상도 조절
        frame = cv2.resize(frame, (640, 480))
        with frame_lock:
            latest_frame = frame
        # 너무 빠른 루프 방지
        time.sleep(0.01)

# 백그라운드 스레드로 시작
threading.Thread(target=capture_loop, daemon=True).start()

def gen_frames():
    """
    전역 latest_frame을 읽어서
    YOLO 추론 → JPEG 인코딩 → yield
    """
    from ultralytics import YOLO
    model = YOLO('./model/yolov8s3/weights/best.pt')

    while True:
        with frame_lock:
            frame = None if latest_frame is None else latest_frame.copy()
        if frame is None:
            time.sleep(0.01)
            continue

        # 2) 추론
        res = model(frame, conf=0.25, verbose=False)[0]
        annotated = res.plot()

        # 3) JPEG로 인코딩
        ret, buf = cv2.imencode('.jpg', annotated)
        if not ret:
            continue

        # 4) 스트리밍 바이트 생성
        yield (
            b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' +
            buf.tobytes() +
            b'\r\n'
        )

# @app.get("/video_feed")
# def video_feed():
#     return StreamingResponse(
#         gen_frames(),
#         media_type="multipart/x-mixed-replace; boundary=frame"
#     )