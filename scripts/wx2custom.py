# 根据末尾配置提取万象词库为自用格式
# --- AMZ 

import os
import shutil

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

                # 检查是否遇到以汉字开头的行，并开始处理
                if not processing and any('\u4e00' <= char <= '\u9fff' for char in line):
                    processing = True

                if processing:
                    # 分割行内容
                    parts = line.split('\t')
                    
                    # 跳过格式不正确的行，保留原数据
                    if len(parts) < 3:
                        processed_data.append(line)
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
                            middle_segment = segments[start_index] if len(segments) > start_index else ''
                            # 使用分号分隔
                            processed_rime_parts.append(f"{first_segment};{middle_segment}")
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

# 调用函数并指定输入和输出目录，分号之间代表了你想要的辅助码部分
# input_dir = 'new_cn_dicts'  # 输入目录
# output_dir = 'hxnew_cn_dicts'  # 输出目录
# start_index = 8  # 自定义开始分号索引
# end_index = 9    # 自定义结束分号索引
input_dir = 'cn_dicts_wx'  # 输入目录
output_dir = 'out'  # 输出目录
start_index = 3  # 自定义开始分号索引
end_index = 4    # 自定义结束分号索引

# 7,8 是五笔前二  3,4 是自然码

if __name__ == '__main__':
        # 如果存在输出文件，先删除
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    os.mkdir(output_dir)

    process_rime_dicts(input_dir, output_dir, start_index, end_index)
