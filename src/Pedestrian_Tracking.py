import cv2
from ultralytics import YOLO
import torch
from collections import defaultdict
from shapely.geometry import Point, Polygon
import numpy as np
import cvzone
# 选择设备：如果有GPU，使用GPU（cuda），否则使用CPU
device = "cuda" if torch.cuda.is_available() else "cpu"
# 加载YOLOv11模型到GPU
model = YOLO("your weights path").to(device)
names=model.names
# 打开视频文件
cap = cv2.VideoCapture(r"your video")

# 创建轨迹存储字典 {track_id: {frame_id: (x, y, w, h)}}
trajectories = defaultdict(dict)

# 增加帧计数器
frame_id = 0
area = [] #测量区域的顶点坐标

with open("output_tracks.txt", "w") as f:
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # 使用YOLOv11进行跟踪
        results = model.track(
            source=frame,
            persist=True,  # 保持ID连续性
            device=device,
            conf=0.5,  # 置信度阈值
            iou=0.5,  # NMS阈值
            tracker = 'botsort.yaml',

        )

        # 记录当前帧所有检测目标
        if results[0].boxes.id is not None:
            boxes = results[0].boxes.xywh.cpu().tolist()
            track_ids = results[0].boxes.id.cpu().numpy().astype(int)
            class_ids = results[0].boxes.cls.cpu().numpy().astype(int)
            for class_id, track_id, box in zip(class_ids,track_ids, boxes):
                x, y, w, h = box
                c = names[class_id]
                cx = int(x + x) // 2
                cy = int(y + y) // 2
                result = cv2.pointPolygonTest(np.array(area, np.int32), ((cx, cy)), False)
                if result>=0:
                    f.write(f"{frame_id} {class_id} {track_id} {x:.4f} {y:.4f} {w:.4f} {h:.4f}\n")

                    # 存储到字典用于后续分析
                    trajectories[track_id][frame_id] = (class_id, x, y, w, h)

        frame_id += 1  # 更新帧号
        cv2.polylines(frame, [np.array(area, np.int32)], True, (255, 0, 255), 2)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
# 关闭资源
cap.release()

