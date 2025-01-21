# -*- coding: utf-8 -*-

"""
文件编码检测工具

该脚本用于检测指定文件的编码格式。通过读取文件的二进制数据，并使用 `chardet` 库来推测文件的编码格式。

使用方法：
1. 将 `file_path` 替换为需要检测的文件路径。
2. 运行脚本，输出文件的编码格式。

依赖库：
- chardet: 用于检测文件编码格式。可以通过 `pip install chardet` 安装。

"""

import chardet


def detect_file_encoding(file_path):
    """
    检测文件的编码格式

    :param file_path: 文件路径
    :return: 文件的编码格式
    """
    with open(file_path, 'rb') as f:
        raw_data = f.read()

    result = chardet.detect(raw_data)
    return result['encoding']


if __name__ == "__main__":
    # 检测当前文件的编码格式
    current_file = __file__  # 获取当前文件的路径
    encoding = detect_file_encoding(current_file)
    print(f"当前文件的编码格式是: {encoding}")
