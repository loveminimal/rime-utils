# get_pinyin_8105_str.py
# 根据 meta/8105通用规范汉字表.yaml 生成 8105 字符串
import os
import shutil
from pathlib import Path


# 遍历源文件夹文件，处理
def convert():
    for file_path in src_dir.iterdir():
        if file_path.is_file():
            file_name = file_path.name
            if not file_name.endswith('8105通用规范汉字表.yaml'):
                continue

            print(file_name)

            src_file_path = src_dir / file_name
            out_file_path = out_dir / file_name

            with open(src_file_path, 'r', encoding='utf-8') as f:
                num = 0
                res = ''
                for line in f.readlines():
                    if line.startswith(('#', ' ', '\n', '-', '.', 'n', 'v', 's', 'c')):  # 忽略非词表行
                        # res = res + line
                        continue

                    else:
                        line_list = line.strip().split('\t')
                        res = res + f'{line_list[1]}'

                print(f'字符长度: {len(res)}' )
                return res
            # with open(out_file_path, 'w', encoding='utf-8') as o:
            #     o.write(res)


current_dir = Path.cwd()
src_dir = current_dir / 'meta'
out_dir = current_dir / 'out'

# 如果存在输出文件，先删除
if os.path.exists(out_dir):
    shutil.rmtree(out_dir)
os.mkdir(out_dir)

convert()
