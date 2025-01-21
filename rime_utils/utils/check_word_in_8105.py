import sys
from pathlib import Path
from is_chinese_char import is_chinese_char
from rime_utils.data.char_8105 import char_8105


def check_word_in_8105(src_dir, out_dir, file_endswith_filter):
    # 遍历源文件夹文件，处理
    num = 0
    for file_path in src_dir.iterdir():
        if file_path.is_file() and file_path.name.endswith(file_endswith_filter):
            print('» %s' % file_path)
            try:
                with open(src_dir / file_path.name, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                    for line in lines:
                        if is_chinese_char(line[0]) and line[0] not in char_8105:
                            num = num + 1
                            print(f'{num} - {line.strip()}')
            except Exception as e:
                print(f"无法读取文件 {file_path.name}: {e}")

    if num == 0:
        print('✅ 未包含不在 pkg_8105 内的字词')
    else:
        print(f'❌ 共包含 %d 个不在 pkg_8105 内的字词' % num)


def get_user_input():
    # 获取当前脚本所在目录的上级目录，即项目根目录
    current_dir = Path(__file__).resolve().parent.parent

    # 获取源目录路径
    src = input(f"请输入源目录路径 (默认: {current_dir}/wubi86_meta): ") or 'wubi86_meta'
    src_dir = current_dir / src

    # 获取输出目录路径
    out = input(f"请输入输出目录路径 (默认: {current_dir}/out): ") or 'out'
    out_dir = current_dir / out

    # 获取文件后缀过滤条件
    file_endswith_filter = input("请输入文件后缀过滤条件 (默认: '86.dict.yaml'): ") or '86.dict.yaml'

    return src_dir, out_dir, file_endswith_filter


if __name__ == '__main__':
    src_dir, out_dir, file_endswith_filter = get_user_input()

    # 调试输出，查看拼接后的路径
    print(f'src_dir: {src_dir}')
    print(f'out_dir: {out_dir}')

    # 确保源目录存在
    if not src_dir.exists():
        print(f"源目录 {src_dir} 不存在！")
        sys.exit(1)

    # 执行检查
    check_word_in_8105(src_dir, out_dir, file_endswith_filter)
