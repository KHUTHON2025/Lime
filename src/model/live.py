import cv2
from ultralytics import YOLO

# model = YOLO('yolov8s.pt')

model = YOLO('./yolov8s3/weights/best.pt').half()

# 2) 웹캠 열기 (0: 기본 카메라)
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    raise RuntimeError("웹캠을 열 수 없습니다")

# 3) 매 프레임마다 추론 및 시각화
while True:
    ret, frame = cap.read()
    if not ret:
        break

    # (Optional) 해상도 조정 — 속도 향상을 위해
    # frame = cv2.resize(frame, (640, 480))

    # 4) 모델에 프레임 전달 (stream=True 로 스트리밍 모드)
    results = model(source=frame, conf=0.25, verbose=False, stream=True)

    # 스트리밍 모드는 제너레이터를 반환하므로, 한 프레임만 처리
    for res in results:
        # res.orig_img 에 원본 BGR 이미지가 들어 있고,
        # res.plot() 으로 박스/레이블 그린 이미지를 얻습니다
        annotated = res.plot()
        break

    # 5) 화면에 출력
    cv2.imshow('YOLOv8 Real-time', annotated)

    # 'q' 키를 누르면 종료
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 6) 정리
cap.release()
cv2.destroyAllWindows()