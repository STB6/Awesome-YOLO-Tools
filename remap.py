# remap.py

import os


def remap_tags(directory: str, labels_map: dict, output: bool = False) -> int:
    """
    Remap tags in the specified directory according to the tag_map.\n
    根据tag_map映射表重新映射指定目录中的标签。
    - directory: Label directory, 标签目录
    - labels_map: Tag remapping table, 标签重映射表
    - return: Number of remapped tags, 重新映射的标签数
    """
    remapped_files_count = 0

    for label_file in os.listdir(directory):
        if not label_file.endswith(".txt"):
            continue

        label_file_path = os.path.join(directory, label_file)
        with open(label_file_path, "r") as file:
            lines = file.read().splitlines()

        new_lines = []
        for line in lines:
            parts = line.split()
            if not parts:
                continue

            label = int(parts[0])
            if label in labels_map:
                parts[0] = str(labels_map[label])
                new_lines.append(" ".join(parts))
                remapped_files_count += 1
            elif output:
                print(f"Skipped unmapped label, 跳过未映射的标签: {label} in {label_file}")

        with open(label_file_path, "w") as file:
            file.write("\n".join(new_lines))

    if output:
        print(f"FTotal tags remapped, 总共重新映射的标签数: {remapped_files_count}")

    return remapped_files_count


if __name__ == "__main__":
    directory_base = input("Enter the directory of YOLO labels, 输入YOLO标签目录: ")
    labels_map = {0: 3, 1: 4, 2: 1, 3: 2, 4: 3, 5: 0, 6: 0}
    remap_tags(directory_base, labels_map, True)
