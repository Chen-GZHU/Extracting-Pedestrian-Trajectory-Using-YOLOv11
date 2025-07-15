import os
import yaml
from ultralytics import YOLO
import argparse

def train_yolo_model(weights_path, data_yaml_path, epochs=100, imgsz=640, batch_size=16):
    """
    使用YOLOv11训练模型。
    """
    if not os.path.exists(weights_path):
        raise FileNotFoundError(f"预训练权重文件不存在: {weights_path}")

    if not os.path.exists(data_yaml_path):
        raise FileNotFoundError(f"数据集配置文件不存在: {data_yaml_path}")

    # 加载预训练权重
    model = YOLO(weights_path)

    # 开始训练
    results = model.train(
        data=data_yaml_path,  # 数据集配置文件路径
        epochs=epochs,  # 训练轮数
        imgsz=imgsz,  # 输入图片尺寸
        batch=batch_size,  # 批量大小
        device='auto',  # 自动识别 GPU/CPU，提高兼容性
        name='yolov11_custom',  # 训练任务名称
    )

    print("✅ 训练完成！")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='YOLOv11 训练工具')

    parser.add_argument('--weights_path', type=str, required=True, help='预训练权重路径')
    parser.add_argument('--data_yaml_path', type=str, required=True, help='数据集配置文件路径')
    parser.add_argument('--epochs', type=int, default=300, help='训练轮数')
    parser.add_argument('--imgsz', type=int, default=640, help='输入图片尺寸')
    parser.add_argument('--batch_size', type=int, default=16, help='批量大小')

    args = parser.parse_args()

    train_yolo_model(
        args.weights_path,
        args.data_yaml_path,
        epochs=args.epochs,
        imgsz=args.imgsz,
        batch_size=args.batch_size
    )
