import os


def extract_and_save(input_file, output_file):
    # 打开输入文件和输出文件
    with open(input_file, 'r', encoding='utf-8') as infile, open(output_file, 'w', encoding='utf-8') as outfile:
        for line in infile:
            # 忽略注释行和空行
            if line.startswith('#') or line.strip() == '':
                continue
            # 分割每一行
            parts = line.strip().split('\t')  # 使用制表符分割
            if len(parts) >= 4:  # 确保行中有足够的列
                character = parts[1]  # 汉字列
                pinyin = parts[3]  # 拼音列（假设拼音在第4列）
                # 拆分多个读音
                pinyin_list = [p.strip() for p in pinyin.split(',')]
                # 遍历每个读音，生成新的行
                for p in pinyin_list:
                    outfile.write(f"{character}\t{p}\n")


if __name__ == "__main__":
    # 默认路径
    default_input_file = "../meta/8105通用规范汉字表.yaml"
    default_output_file = "../out/8105_pinyin_with_tone.yaml"

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
