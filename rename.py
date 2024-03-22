# rename.py

import hashlib, os
from config import *


def rename_files(directory_a: str, directory_b: str, output: bool = False) -> int:
    """
    Rename image and label files based on the hash value of the image, automatically delete duplicate files and labels.\n
    基于图片的哈希值重命名图片和标签文件,自动删除重复文件和标签。
    - directory_a: Image files directory, 图片文件目录
    - directory_b: Label files directory, 标签文件目录
    - return: Number of files processed, 处理的文件数量
    """
    renamed_files_count = 0
    hash_set = set()

    for file in os.listdir(directory_a):
        if not any(file.endswith(ext) for ext in IMAGE_FILE_EXTENSIONS):
            continue

        base_file_name, file_ext = os.path.splitext(file)
        img_paths = [os.path.join(directory_a, base_file_name + ext) for ext in IMAGE_FILE_EXTENSIONS]
        found_files = [path for path in img_paths if os.path.exists(path)]

        if len(found_files) > 1:
            print(f"Multiple image files found, 存在多个同名图片文件: {base_file_name}")
            continue

        img_path = found_files[0]
        with open(img_path, "rb") as f:
            bytes_data = f.read()
            readable_hash = hashlib.sha256(bytes_data).hexdigest().upper()

        if readable_hash in hash_set:
            if output:
                print(f"Duplicate hash detected, deleting file and label, 检测到重复哈希, 删除文件和标签: {base_file_name}")
            os.remove(img_path)

            label_file_path = os.path.join(directory_b, base_file_name + ".txt")
            if os.path.exists(label_file_path):
                os.remove(label_file_path)
        else:
            label_file_path = os.path.join(directory_b, base_file_name + ".txt")
            if not os.path.exists(label_file_path):
                print(f"Label file not found, 找不到标签文件: {base_file_name}.txt")
                continue

            hash_set.add(readable_hash)
            short_hash = readable_hash[:16]
            new_file_name = f"{short_hash}{file_ext}"
            new_label_file_name = f"{short_hash}.txt"
            new_img_path = os.path.join(directory_a, new_file_name)
            new_label_file_path = os.path.join(directory_b, new_label_file_name)
            os.rename(img_path, new_img_path)
            os.rename(label_file_path, new_label_file_path)
            renamed_files_count += 1

            if output:
                print(f"Renamed file, 重命名文件: {base_file_name}{file_ext} -> {new_file_name}")

    if output:
        print(f"Total files renamed, 总共重命名的文件数: {renamed_files_count}")

    return renamed_files_count


if __name__ == "__main__":
    directory_a = input("Enter the image files directory, 输入图片文件目录: ")
    directory_b = input("Enter the label files directory, 输入标签文件目录: ")
    rename_files(directory_a, directory_b, True)
