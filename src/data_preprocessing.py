import os
import yaml
import shutil
from xml.etree import ElementTree as ET

def create_yolo_dataset(annotation_dir, image_dir, classes_file, output_dir):
    """
    将VOC格式的XML标注转换为YOLO格式，并生成数据集配置文件。
    """
    if not os.path.exists(annotation_dir) or not os.path.exists(image_dir):
        raise FileNotFoundError("标注文件夹或图片文件夹不存在，请检查路径。")

    # 读取类别名称
    with open(classes_file, 'r') as f:
        classes = [line.strip() for line in f.readlines()]

    # 创建YOLO格式的标注文件
    os.makedirs(output_dir, exist_ok=True)
    labels_dir = os.path.join(output_dir, 'labels')
    images_dir = os.path.join(output_dir, 'images')
    os.makedirs(labels_dir, exist_ok=True)
    os.makedirs(images_dir, exist_ok=True)

    # 遍历XML文件并转换
    for xml_file in os.listdir(annotation_dir):
        if not xml_file.endswith('.xml'):
            continue

        # 解析XML文件
        tree = ET.parse(os.path.join(annotation_dir, xml_file))
        root = tree.getroot()

        # 获取图片尺寸
        size = root.find('size')
        img_width = int(size.find('width').text)
        img_height = int(size.find('height').text)

        # 创建YOLO格式的标注文件
        txt_file = os.path.splitext(xml_file)[0] + '.txt'
        with open(os.path.join(labels_dir, txt_file), 'w') as f:
            for obj in root.findall('object'):
                cls_name = obj.find('name').text
                cls_id = classes.index(cls_name)

                # 获取边界框坐标
                bbox = obj.find('bndbox')
                xmin = int(bbox.find('xmin').text)
                ymin = int(bbox.find('ymin').text)
                xmax = int(bbox.find('xmax').text)
                ymax = int(bbox.find('ymax').text)

                # 转换为YOLO格式（归一化中心坐标和宽高）
                x_center = (xmin + xmax) / 2 / img_width
                y_center = (ymin + ymax) / 2 / img_height
                width = (xmax - xmin) / img_width
                height = (ymax - ymin) / img_height

                # 写入文件
                f.write(f"{cls_id} {x_center} {y_center} {width} {height}\n")

        # 复制图片到images文件夹（更换为shutil以提高兼容性）
        img_file = os.path.splitext(xml_file)[0] + '.jpg'
        shutil.copy(os.path.join(image_dir, img_file), images_dir)

    # 生成数据集配置文件
    data_yaml = {
        'train': os.path.join(output_dir, 'images'),
        'val': os.path.join(output_dir, 'images'),  # 如果没有验证集，可以复用训练集
        'nc': len(classes),
        'names': classes
    }
    with open(os.path.join(output_dir, 'dataset.yaml'), 'w') as f:
        yaml.dump(data_yaml, f)

    print(f"✅ 数据集已生成，保存路径：{output_dir}")


if __name__ == "__main__":
    # 数据集路径
    annotation_dir = 'your annotation dir'   # XML标注文件夹
    image_dir =  'your image dir' # 图片文件夹
    classes_file =  'your classes file' # 类别文件
    output_dir = 'yolo dataset'  # YOLO格式数据集输出路径

    # 步骤1：生成YOLO格式数据集
    create_yolo_dataset(annotation_dir, image_dir, classes_file, output_dir)