# ectract.py

import os


def extract_labels(directory: str) -> set:
    """
    Extract all YOLO labels in the directory folder.\n
    提取directory目录中的所有YOLO标签。
    - directory: YOLO labels directory, YOLO标签目录
    - return: label set, 标签集合
    """
    return {line.split()[0] for label_file in os.listdir(directory) if label_file.endswith(".txt") for line in open(os.path.join(directory, label_file), "r")}


if __name__ == "__main__":
    directory = input("Enter the directory of YOLO labels, 输入YOLO标签目录: ")
    print(sorted(extract_labels(directory)))
