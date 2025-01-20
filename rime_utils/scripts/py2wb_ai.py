import os
import re
import sys
import shutil
from pathlib import Path
from data.wubi86yd import get_wubi86yd
from timer import timer
from is_chinese_char import is_chinese_char

wubi86yd = get_wubi86yd()

def is_valid_word(word):
    """检查词组是否包含非文字字符"""
    return not any(char in '.,()0123456789qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM' for char in word)

def process_word(word, weight, wubi86yd):
    """处理单个词组，生成五笔编码"""
    if len(word) == 1:
        return f'{word}\t{wubi86yd.get(word, "xxxx")}\t{weight}\n'
    elif len(word) == 2:
        return f'{word}\t{wubi86yd[word[0]][:2]}{wubi86yd[word[1]][:2]}\t{weight}\n'
    elif len(word) == 3:
        return f'{word}\t{wubi86yd[word[0]][0]}{wubi86yd[word[1]][0]}{wubi86yd[word[2]][:2]}\t{weight}\n'
    else:
        return f'{word}\t{wubi86yd[word[0]][0]}{wubi86yd[word[1]][0]}{wubi86yd[word[2]][0]}{wubi86yd[word[-1]][0]}\t{weight}\n'

@timer
def convert(src_dir, out_dir, file_endswith_filter):
    """转换源文件夹中的文件到目标文件夹"""
    dict_num = 0
    num = 0  # 统计文件中不包含在 wubi86yd 中的字的行数
    count = 0  # 统计文件中词组包含非文字行的数量

    # 遍历源文件夹文件，处理
    for file_path in src_dir.iterdir():
        if file_path.is_file() and file_path.name.endswith(file_endswith_filter):
            dict_num += 1
            print(f'☑️  已加载第 {dict_num} 份码表 » {file_path}')

            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()

            res = ''
            for line in lines:
                if not is_chinese_char(line[0]):
                    res += line
                else:
                    line_arr = line.strip().split('\t')
                    word = line_arr[0]
                    weight = line_arr[2] if len(line_arr) > 2 else '0'

                    if not is_valid_word(word):
                        count += 1
                        print(f'{count} - {line.strip()}')
                        continue

                    for char in word:
                        if char not in wubi86yd:
                            num += 1
                            print(f'{num} - {word}')
                            res += f'{word}\txxxx\t{weight}\n'
                            break
                    else:
                        res += process_word(word, weight, wubi86yd)

            with open(out_dir / file_path.name, 'w', encoding='utf-8') as o:
                o.write(res)

if __name__ == '__main__':
    current_dir = Path.cwd()

    src = 'src'
    out = 'out'
    file_endswith_filter = ''
    multifile_out_mode = 0

    # 命令行输入选项
    for i, arg in enumerate(sys.argv):
        if arg == "-i":
            src = sys.argv[i + 1]
        elif arg == '-o':
            out = sys.argv[i + 1]
        elif arg == '-f':
            file_endswith_filter = sys.argv[i + 1]
        elif arg == '-m':
            multifile_out_mode = sys.argv[i + 1]

    src_dir = current_dir / src  # 设置待处理的拼音词库文件夹
    out_dir = current_dir / out  # 转换后输出的五笔词库文件夹

    # 如果存在输出文件，先删除
    if out_dir.exists():
        shutil.rmtree(out_dir)
    os.mkdir(out_dir)

    convert(src_dir, out_dir, file_endswith_filter)