# classify.py

import os, shutil
from config import *


def classify_files(directory_a: str, directory_b: str, directory_c: str, directory_d: str, target_labels: list, output: bool = False) -> int:
    """
    Copy files with only one target label from input labels directory to output directory.\n
    将输入标签目录中仅含有一个目标标签的文件复制到输出目录。
    - directory_a: Input images directory, 输入图片目录
    - directory_b: Input labels directory, 输入标签目录
    - directory_c: Output images directory, 输出图片目录
    - directory_d: Output labels directory, 输出标签目录
    - target_labels: List of target labels, 目标标签列表
    - return: Number of files copied, 复制的文件数量
    """
    os.makedirs(directory_c, exist_ok=True)
    os.makedirs(directory_d, exist_ok=True)
    copied_files_count = 0
    for label_file in os.listdir(directory_b):
        if not label_file.endswith(".txt"):
            continue

        label_file_path = os.path.join(directory_b, label_file)
        with open(label_file_path, "r") as file:
            labels = [line.split()[0] for line in file.read().splitlines() if line]

            if len(labels) == 1 and int(labels[0]) in target_labels:
                base_filename = os.path.splitext(label_file)[0]
                img_paths = [os.path.join(directory_a, f"{base_filename}{ext}") for ext in IMAGE_FILE_EXTENSIONS]
                found_files = [path for path in img_paths if os.path.exists(path)]

                if len(found_files) == 0:
                    print(f"Image file not found, 找不到图片文件: {base_filename}")
                    continue
                elif len(found_files) > 1:
                    print(f"Multiple image files found, 存在多个同名图片文件: {base_filename}")
                    continue
                else:
                    img_path = found_files[0]

                shutil.copy(label_file_path, os.path.join(directory_d, label_file))
                shutil.copy(img_path, os.path.join(directory_c, os.path.basename(img_path)))
                copied_files_count += 1

                if output and copied_files_count % 50 == 0:
                    print(f"Copied {copied_files_count} files so far, 已复制{copied_files_count}个文件")

    if output:
        print(f"Total processed files, 总共处理的文件数: {copied_files_count}")

    return copied_files_count


if __name__ == "__main__":
    directory_a = input("Enter the input image directory path, 请输入图片文件夹路径: ")
    directory_b = input("Enter the input label directory path, 请输入标签文件夹路径: ")
    directory_c = input("Enter the output image directory path, 请输入输出图片文件夹路径: ")
    directory_d = input("Enter the output label directory path, 请输入输出标签文件夹路径: ")
    target_labels = list(map(int, input("Enter the target labels (separated by space), 请输入目标标签{用空格分隔): ").split()))
    classify_files(directory_a, directory_b, directory_c, directory_d, target_labels, True)
