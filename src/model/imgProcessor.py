import cv2, threading, time
import numpy as np
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
active_until = time.time() + 10  # 5초 후에 비활성화
def gen_frames():
    """
    전역 latest_frame을 읽어서
    YOLO 추론 → JPEG 인코딩 → yield
    """
    from ultralytics import YOLO
    model = YOLO('./model/yolov8s3/weights/best.pt')

    while True:
        now = time.time()
        # 활성 시간 지나면 대기만
        if now > active_until:
            # 검정 바탕에 흰 글씨
            blank = np.zeros((480, 640, 3), dtype=np.uint8)
            cv2.putText(
                blank,
                "No event detected",
                (30, 240),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (255, 255, 255),
                2,
                cv2.LINE_AA
            )
            ret, buf = cv2.imencode('.jpg', blank)
            if not ret:
                time.sleep(0.1)
                continue
            yield (
                b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' +
                buf.tobytes() +
                b'\r\n'
            )
            time.sleep(0.1)
            continue

        with frame_lock:
            frame = None if latest_frame is None else latest_frame.copy()
        if frame is None:
            time.sleep(0.01)
            continue

        # 2) 추론
        res = model(frame, conf=0.25, verbose=False)[0]
        clses = res.boxes.cls  # (N,) 텐서: class index
        conf = res.boxes.conf
        if len(clses) > 0 and conf[0] > 0.5:
            print(f"탐지! {len(clses)}개 신뢰도 {round(max(conf)*100,1)}")
            
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