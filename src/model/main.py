import cv2
from ultralytics import YOLO

# model = YOLO('yolov8s.pt')

model = YOLO('./yolov8s3/weights/best.pt').half()
results = model('./t2.jpg', conf=0.3) #conf로 n% 이상인 객체만 탐지
boxes = results[0].boxes

xyxy = boxes.xyxy   # (N,4) 텐서: [x1, y1, x2, y2]
confs = boxes.conf  # (N,) 텐서: confidence
clses = boxes.cls   # (N,) 텐서: class index
print("xyxy:", xyxy)
print()
print("confs:", confs) #신뢰도
print()
print("clses:", clses) #총 갯수. 개체별 종류

plots = results[0].plot()
cv2.imshow("plot", plots)
cv2.waitKey(0)
cv2.destroyAllWindows()