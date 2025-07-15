# Extracting Pedestrian Trajectory Using YOLOv11

[![Python](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/)  
[![License: MIT](https://img.shields.io/badge/license-MIT-green)](./LICENSE)  

> Automatically extract pedestrian trajectories from videos using YOLOv11 and generate visualization results.

---

## 🚀 Quick Start

1. **Clone repository**  
   ```bash
   git clone https://github.com/Chen-GZHU/Extracting-Pedestrian-Trajectory-Using-YOLOv11.git
   cd Extracting-Pedestrian-Trajectory-Using-YOLOv11
2. **Install dependencies**
   ```bash
    pip install -r requirements.txt
3. **Extract trajectories**
    ```bash
    python src/Pedestrian_Tracking.py \
      --input path/to/video.mp4 \
      --output path/to/trajectories.csv \
      --conf-thres 0.4 \
      --iou-thres 0.45
4. **Visualize results**
    ```bash
    python src/visualization.py

