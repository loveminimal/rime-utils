import os
from pathlib import Path


def get_wubi86_18030_map(input_file, output_file):
    wubi86_18030_map = {}
    # 打开输入文件和输出文件
    with open(input_file, 'r', encoding='utf-8') as infile, open(output_file, 'w', encoding='utf-8') as outfile:
        for line in infile:
            # 忽略注释行和空行
            if line.startswith('#') or line.strip() == '':
                continue
            # 分割每一行
            parts = line.strip().split('\t')  # 使用制表符分割
            if len(parts) >= 2:  # 确保行中有足够的列
                character = parts[0]  # 汉字列
                code = parts[1]  # 拼音列（假设拼音在第4列）

                wubi86_18030_map[character] = code

                # 写入输出文件，汉字和拼音用制表符隔开
                # outfile.write(f"{character}\t{pinyin_no_tone}\n")
        outfile.write(f"wubi86_18030_map={wubi86_18030_map}")
        # print(pinyin_map.__str__())
        # return pinyin_map


if __name__ == "__main__":
    # 项目包路径 rime_utils/rime_utils/
    proj_dir = Path(__file__).parent.parent
    print(proj_dir)

    # 默认路径
    default_input_file = proj_dir / 'meta' / 'wubi86_18030单字10万.dict.yaml'
    default_output_file = proj_dir / 'out' / 'wubi86_18030_map.py'

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
        get_wubi86_18030_map(input_file, output_file)
        print(f"处理完成！结果已保存到 {output_file}")
    except Exception as e:
        print(f"发生错误：{e}")
