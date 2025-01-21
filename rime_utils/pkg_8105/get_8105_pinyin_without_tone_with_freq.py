import os
from pathlib import Path

def load_subtlex_ch_frequency(file_path):
    """加载 SUBTLEX-CH-CHR 词频数据"""
    frequency_data = {}
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            parts = line.strip().split()  # 使用空格或制表符分割
            if len(parts) >= 2:
                try:
                    character = parts[0]  # 字符列
                    freq = int(parts[1])  # 总频率（CHRCount）
                    frequency_data[character] = freq
                except (ValueError, IndexError):
                    # 跳过表头行或格式不正确的行
                    continue
    return frequency_data


def remove_tone(pinyin_str):
    """去除拼音中的声调符号"""
    tone_map = {
        'ā': 'a', 'á': 'a', 'ǎ': 'a', 'à': 'a',
        'ē': 'e', 'é': 'e', 'ě': 'e', 'è': 'e', 'ê̄': 'e', 'ế': 'e', 'ê̌': 'e', 'ề': 'e',
        'ī': 'i', 'í': 'i', 'ǐ': 'i', 'ì': 'i',
        'ō': 'o', 'ó': 'o', 'ǒ': 'o', 'ò': 'o',
        'ū': 'u', 'ú': 'u', 'ǔ': 'u', 'ù': 'u',
        'ǖ': 'v', 'ǘ': 'v', 'ǚ': 'v', 'ǜ': 'v', 'ü': 'v',
        'ń': 'n', 'ň': 'n', 'ǹ': 'n',
        'ḿ': 'm'
    }
    return ''.join([tone_map.get(char, char) for char in pinyin_str])


def process_file(input_file, output_file, frequency_data):
    """处理输入文件，生成带词频的拼音"""
    seen_entries = set()  # 用于去重
    with open(input_file, 'r', encoding='utf-8') as infile, open(output_file, 'w', encoding='utf-8') as outfile:
        for line in infile:
            # 忽略注释行和空行
            if line.startswith('#') or line.strip() == '':
                continue
            # 分割每一行
            parts = line.strip().split('\t')
            if len(parts) >= 4:  # 确保行中有足够的列
                character = parts[1]  # 汉字列（第 2 列）
                pinyin_str = parts[3]  # 拼音列（第 4 列）
                # 去除声调
                pinyin_list = [remove_tone(p) for p in pinyin_str.split(', ')]
                # 获取词频
                freq = frequency_data.get(character, 0)
                # 生成新的行
                for pinyin in pinyin_list:
                    entry = f"{character}\t{pinyin}\t{freq}"
                    if entry not in seen_entries:  # 去重
                        seen_entries.add(entry)
                        outfile.write(f"{entry}\n")


if __name__ == "__main__":
    # 项目包路径 rime_utils/rime_utils/
    proj_dir = Path(__file__).parent.parent
    print(proj_dir)

    # 默认路径
    default_input_file = proj_dir / 'meta' / '8105通用规范汉字表.yaml'
    default_output_file = proj_dir / 'out' / '8105_pinyin_without_tone_with_freq.yaml'
    default_frequency_file = proj_dir / 'data' / 'SUBTLEX-CH-CHR.txt'   # SUBTLEX-CH-CHR 文件路径


    # 让用户输入输入文件和输出文件的路径
    input_file = input(f"请输入输入文件的路径（默认：{default_input_file}）：").strip() or default_input_file
    output_file = input(f"请输入输出文件的路径（默认：{default_output_file}）：").strip() or default_output_file
    frequency_file = input(f"请输入词频文件的路径（默认：{default_frequency_file}）：").strip() or default_frequency_file

    # 检查输入文件是否存在
    if not os.path.exists(input_file):
        print(f"错误：文件 {input_file} 未找到，请检查路径是否正确。")
        exit(1)

    # 检查词频文件是否存在
    if not os.path.exists(frequency_file):
        print(f"错误：文件 {frequency_file} 未找到，请检查路径是否正确。")
        exit(1)

    # 加载词频数据
    frequency_data = load_subtlex_ch_frequency(frequency_file)

    # 创建输出目录（如果不存在）
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    # 调用函数处理文件
    try:
        process_file(input_file, output_file, frequency_data)
        print(f"处理完成！结果已保存到 {output_file}")
    except Exception as e:
        print(f"发生错误：{e}")
