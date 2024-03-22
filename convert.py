# convert.py
from config import *

from PIL import Image
import os
import xml.etree.ElementTree as ET


def convert(size: tuple, original_box: tuple) -> tuple:
    """
    - size: image size, 图片尺寸
    - original_box: original bounding box coordinates, 原始边界框坐标
    - return: converted bounding box coordinates, 转换后的边界框坐标
    """
    dw = 1.0 / size[0]
    dh = 1.0 / size[1]
    x_center = (original_box[0] + original_box[1]) / 2.0
    y_center = (original_box[2] + original_box[3]) / 2.0
    width = original_box[1] - original_box[0]
    height = original_box[3] - original_box[2]
    x_center *= dw
    width *= dw
    y_center *= dh
    height *= dh
    return (x_center, y_center, width, height)


def convert_files(directory_a: str, directory_b: str, directory_c: str, label_list: list, output: bool = False) -> int:
    """
    Convert VOC format labels to YOLO format labels.\n
    将VOC格式的标签转换为YOLO格式的标签。
    - directory_a: images directory, 图片目录
    - directory_b: XML labels directory, XML标签目录
    - directory_c: txt labels output directory, txt标签输出目录
    - label_list: label list, 标签列表
    - return: number of converted labels, 转换标签数量
    """
    os.makedirs(directory_c, exist_ok=True)
    converted_labels_count = 0
    for file_name in os.listdir(directory_b):
        if file_name.endswith(".xml"):
            base_file_name = os.path.splitext(file_name)[0]
            img_paths = [os.path.join(directory_a, f"{base_file_name}{ext}") for ext in IMAGE_FILE_EXTENSIONS]
            img_path = None
            found_files = [path for path in img_paths if os.path.exists(path)]

            if len(found_files) == 0:
                print(f"Image file not found, 找不到图片文件: {base_file_name}")
                continue
            elif len(found_files) > 1:
                print(f"Multiple image files found, 存在多个同名图片文件: {base_file_name}")
                continue
            else:
                img_path = found_files[0]

            xml_path = os.path.join(directory_b, file_name)
            txt_path = os.path.join(directory_c, f"{base_file_name}.txt")

            img = Image.open(img_path)
            image_width, image_height = img.size

            in_file = open(xml_path, encoding="utf-8")
            tree = ET.parse(in_file)
            root = tree.getroot()

            with open(txt_path, "w", encoding="utf-8") as out_file:
                for obj in root.iter("object"):
                    difficult = obj.find("difficult").text if obj.find("difficult") else "0"
                    if difficult == "1":  # Skip difficult objects, 跳过有difficult标记的标签
                        continue
                    label_name = obj.find("name").text
                    if label_name in label_list:
                        label_id = label_list.index(label_name)
                        xmlbox = obj.find("bndbox")
                        original_box = (float(xmlbox.find("xmin").text), float(xmlbox.find("xmax").text), float(xmlbox.find("ymin").text), float(xmlbox.find("ymax").text))
                        normalized_box = convert((image_width, image_height), original_box)
                        out_file.write(str(label_id) + " " + " ".join([str(a) for a in normalized_box]) + "\n")
                        converted_labels_count += 1
            in_file.close()

            if output:
                print(f"Label file converted, 已转换标签文件: {file_name}")

    if output:
        print(f"Total labels converted, 总共转换标签数: {converted_labels_count}")

    return converted_labels_count


if __name__ == "__main__":
    image_directory = input("Enter the directory of images, 输入图片目录: ")
    xml_directory = input("Enter the directory of xml labels, 输入xml标签目录: ")
    txt_directory = input("Enter the output directory of txt labels, 输入txt标签输出目录: ")
    label_list = input("Enter the label list, 输入类别列表: ").split()
    convert_files(image_directory, xml_directory, txt_directory, label_list, True)
