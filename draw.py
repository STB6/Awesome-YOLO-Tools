# draw.py

import os
from PIL import Image, ImageDraw
from config import *


def draw_yolo_boxes(directory_a: str, directory_b: str, directory_c: str, output: bool = False) -> int:
    """
    Draw bounding boxes on images based on YOLO labels.\n
    基于YOLO标签在图像上绘制边界框。
    - directory_a: Input images directory, 输入图片目录
    - directory_b: Input labels directory, 输入标签目录
    - directory_c: Output images directory, 输出图片目录
    - return: Number of images drawn, 绘制的图片数
    """
    os.makedirs(directory_c, exist_ok=True)
    drawn_files_count = 0
    for label_file in os.listdir(directory_b):
        if label_file.endswith(".txt"):
            base_file_name = os.path.splitext(label_file)[0]
            image_paths = [os.path.join(directory_a, f"{base_file_name}{ext}") for ext in IMAGE_FILE_EXTENSIONS]
            image_path = None
            found_files = [path for path in image_paths if os.path.exists(path)]

            if len(found_files) == 0:
                print(f"Image file not found, 找不到图片文件: {base_file_name}")
                continue
            elif len(found_files) > 1:
                print(f"Multiple image files found, 存在多个同名图片文件: {base_file_name}")
                continue
            else:
                image_path = found_files[0]

            output_path = os.path.join(directory_c, base_file_name + "_drawn.jpg")

            img = Image.open(image_path)
            draw = ImageDraw.Draw(img)
            img_width, img_height = img.size

            with open(os.path.join(directory_b, label_file), "r") as f:
                for line in f:
                    _, x_center, y_center, width, height = [float(x) for x in line.strip().split()]
                    left = (x_center - width / 2) * img_width
                    top = (y_center - height / 2) * img_height
                    right = (x_center + width / 2) * img_width
                    bottom = (y_center + height / 2) * img_height
                    draw.rectangle([left, top, right, bottom], outline="red", width=2)
            img.save(output_path)
            drawn_files_count += 1

            if output:
                print(f"Image file drawn, 绘制图片文件: {base_file_name}.jpg")

    if output:
        print(f"Total images drawn, 总共绘制的图片数: {drawn_files_count}")

    return drawn_files_count


if __name__ == "__main__":
    directory_a = input("Input images directory: ")
    directory_b = input("Input labels directory: ")
    directory_c = input("Output images directory: ")
    draw_yolo_boxes(directory_a, directory_b, directory_c)
