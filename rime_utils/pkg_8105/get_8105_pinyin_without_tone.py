import os
from pathlib import Path


def remove_tone(pinyin):
    """去除拼音中的声调符号"""
    # 定义声调符号到无音调字母的映射
    tone_map = {
        'ā': 'a', 'á': 'a', 'ǎ': 'a', 'à': 'a',
        'ē': 'e', 'é': 'e', 'ě': 'e', 'è': 'e', 'ê̄': 'e', 'ế': 'e', 'ê̌': 'e', 'ề': 'e',
        'ī': 'i', 'í': 'i', 'ǐ': 'i', 'ì': 'i',
        'ō': 'o', 'ó': 'o', 'ǒ': 'o', 'ò': 'o',
        'ū': 'u', 'ú': 'u', 'ǔ': 'u', 'ù': 'u',
        'ǖ': 'v', 'ǘ': 'v', 'ǚ': 'v', 'ǜ': 'v', 'ü': 'v',
        'ń': 'n', 'ň': 'n', 'ǹ': 'n',
        'ḿ': 'm',
    }
    # 去除声调符号
    pinyin_no_tone = []
    for char in pinyin:
        if char in tone_map:
            pinyin_no_tone.append(tone_map[char])
        else:
            pinyin_no_tone.append(char)
    return ''.join(pinyin_no_tone)


def extract_and_save(input_file, output_file):
    # 用于存储去重后的结果，同时保持顺序
    unique_entries = []
    seen_entries = set()

    # 打开输入文件
    with open(input_file, 'r', encoding='utf-8') as infile:
        for line in infile:
            # 忽略注释行和空行
            if line.startswith('#') or line.strip() == '':
                continue
            # 分割每一行
            parts = line.strip().split('\t')    # 使用制表符分割
            if len(parts) >= 4:                 # 确保行中有足够的列
                character = parts[1]            # 汉字列
                pinyin = parts[3]               # 拼音列（假设拼音在第4列）
                # 拆分多个读音
                pinyin_list = [p.strip() for p in pinyin.split(',')]
                # 遍历每个读音，去除声调并生成新的行
                for p in pinyin_list:
                    p_no_tone = remove_tone(p)      # 去除声调符号
                    entry = f"{character}\t{p_no_tone}"
                    # 如果条目未出现过，则添加到结果中
                    if entry not in seen_entries:
                        seen_entries.add(entry)
                        unique_entries.append(entry)

    # 打开输出文件，写入去重后的结果
    with open(output_file, 'w', encoding='utf-8') as outfile:
        for entry in unique_entries:  # 保持原有顺序
            outfile.write(f"{entry}\n")


if __name__ == "__main__":
    # 项目包路径 rime_utils/rime_utils/
    proj_dir = Path(__file__).parent.parent
    print(proj_dir)

    # 默认路径
    default_input_file = proj_dir / 'meta' / '8105通用规范汉字表.yaml'
    default_output_file = proj_dir / 'out' / '8105_pinyin_without_tone.yaml'


    # 让用户输入输入文件和输出文件的路径
    input_file = input(f"请输入输入文件的路径（默认：{default_input_file}）：").strip() or default_input_file
    output_file = input(f"请输入输出文件的路径（默认：{default_output_file}）：").strip() or default_output_file

    # 检查输入文件是否存在
    if not os.path.exists(input_file):
        print(f"错误：文件 {input_file} 未找到，请检查路径是否正确。")
        exit(1)

    # 创建输出目录（如果不存在）
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    # 调用函数处理文件
    try:
        extract_and_save(input_file, output_file)
        print(f"处理完成！结果已保存到 {output_file}")
    except Exception as e:
        print(f"发生错误：{e}")
