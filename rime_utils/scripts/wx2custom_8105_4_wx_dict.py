# 根据末尾配置提取万象词库为自用格式
# --- AMZ 
# --- modified by Jack Liu

import os
import sys
import shutil
from pathlib import Path
# from data.pinyin8105 import pinyin8105
from data.char_8105 import char_8105

str_with_tone    = 'āáǎàōóǒòēéěèīíǐìūúǔùǖǘǚǜüńňǹ'
str_without_tone = 'aaaaooooeeeeiiiiuuuuvvvvvnnn'
list_with_tone = list(str_with_tone)
list_without_tone = list(str_without_tone)

def process_rime_dicts(input_dir, output_dir, start_index=1, end_index=2):
    """
    处理词典文件，将拼音数据中的指定范围内的内容提取并处理。

    :param input_dir: 输入目录路径
    :param output_dir: 输出目录路径
    :param start_index: 处理的开始分号索引（默认为1）
    :param end_index: 处理的结束分号索引（默认为2）
    """
    # 确保输出目录存在
    os.makedirs(output_dir, exist_ok=True)

    # 遍历输入目录中的所有文件
    for filename in os.listdir(input_dir):
        # 过滤掉不重要的词典，如 corrections.dict.yaml
        # if filename.endswith('corrections.dict.yaml'):
        #     print(f'已过滤的文件: {filename}')
        #     continue


        if filename.endswith('.yaml') or filename.endswith('.txt'):
            input_file = os.path.join(input_dir, filename)
            output_file = os.path.join(output_dir, filename)

            # 读取文件内容
            with open(input_file, 'r', encoding='utf-8') as infile:
                lines = infile.readlines()

            processed_data = []
            processing = False

            for line in lines:
                line = line.strip()

                # 不喜欢带调的（与其他可能使用的拼音词库同步后会冲突），转换成不带调的
                for idx, char in enumerate(list_with_tone):
                    line = line.replace(char, list_without_tone[idx])

                # 检查是否遇到以汉字开头的行，并开始处理
                if not processing and any('\u4e00' <= char <= '\u9fff' for char in line):
                # if not processing and all(char in pinyin8105 for char in line):
                    processing = True

                if processing:
                    # 分割行内容
                    parts = line.split('\t')
                    
                    if len(line) == 0 or line[0] in '-nvsu.# ':
                        processed_data.append(line)
                        continue

                    # 跳过格式不正确的行，保留原数据
                    # if len(parts) < 3 and not all(char in pinyin8105 for char in parts[0]):
                    if any(char not in char_8105 for char in parts[0]):
                        # processed_data.append(line)
                        # processed_data.append(line)
                        continue

                    chinese_part = parts[0]
                    rime_data = parts[1]

                    # 将拼音数据分割成多个部分
                    rime_parts = rime_data.split(' ')
                    processed_rime_parts = []

                    for rime_part in rime_parts:
                        # 处理每个拼音部分
                        segments = rime_part.split(';')
                        if len(segments) > end_index:
                            # 提取第一个分号前的所有字母
                            first_segment = segments[0]

                            # 提取指定范围内的字符（从 start_index 到 end_index）
                            # middle_segment = segments[start_index:end_index] if len(segments) > start_index else ''
                            middle_segment = segments[start_index:end_index] if len(segments) > start_index else ''
                            # 2025-01-10 16:11 这里增加五笔前二辅助码
                            # middle_segment.extend(segments[7:8])
                            # 使用分号分隔
                            processed_rime_parts.append(f"{first_segment};{';'.join(middle_segment)};")
                        else:
                            # 处理没有足够分号的情况，直接用第一个分号前拼音
                            processed_rime_parts.append(segments[0])

                    # 合并处理后的拼音数据
                    processed_rime_data = ' '.join(processed_rime_parts)
                    result = f"{chinese_part}\t{processed_rime_data}\t" + '\t'.join(parts[2:])
                    processed_data.append(result)
                else:
                    # 直接添加未处理的行（如注释）
                    processed_data.append(line)

            # 将处理后的数据写入新的文件
            with open(output_file, 'w', encoding='utf-8') as outfile:
                for item in processed_data:
                    outfile.write(item + '\n')
            print(f'已处理并保存: {output_file}')
# 调用函数并指定输入和输出目录，分号之间代表了你想要的辅助码部分
# input_dir = 'new_cn_dicts'  # 输入目录
# output_dir = 'hxnew_cn_dicts'  # 输出目录
# start_index = 8  # 自定义开始分号索引
# end_index = 9    # 自定义结束分号索引
# input_dir = 'dicts/rime-frost/cn_dicts'  # 输入目录 - 白霜拼音
input_dir = '../rime_wanxiang_pro/cn_dicts'  # 输入目录 - 雾淞拼音
output_dir = 'dicts/rime-wx/cn_dicts'  # 输出目录
start_index = 7  # 自定义开始分号索引
end_index = 8    # 自定义结束分号索引

# 7,8 是五笔前二  3,4 是自然码 1,9 是全部 2,3 是鹤形  2.4 就是自然码+鹤形

if __name__ == '__main__':
    current_dir = Path.cwd()

    for i, arg in enumerate(sys.argv):
        if arg == "-i":
            input_dir = sys.argv[i + 1]
        elif arg == '-o':
            output_dir = sys.argv[i + 1]


    src_dir = current_dir / input_dir		    # 设置待处理的拼音词库文件夹
    out_dir =  current_dir / output_dir			# 转换后输出的五笔词库文件夹



        # 如果存在输出文件，先删除
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    os.mkdir(output_dir)

    process_rime_dicts(input_dir, output_dir, start_index, end_index)
