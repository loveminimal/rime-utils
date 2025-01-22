import re
from pathlib import Path
from rime_utils.data.char_8105 import char_8105
from rime_utils.utils.timer import timer
from rime_utils.data.header import get_header_wubi


@timer
def filter_8105(src_dir, out_dir, file_endswith_filter):
    # print(src_dir, out_dir)
    dict_num = 0
    lines_total = []
    res_dict = {}


    for filepath in src_dir.iterdir():
        if filepath.is_file() and filepath.name.endswith(file_endswith_filter):
            dict_num = dict_num + 1
            print('☑️  已加载第 %d 份码表 » %s' % (dict_num, filepath))

            with open(filepath, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                lines_total.extend(lines)
        
    word_len_list = list(range(26))

    with open(out_dir / out_file_name, 'a', encoding='utf-8') as o:
        res = ''
        line_count_sum = 0
        for word_len in word_len_list:
            line_count = 0  # 符合条件的行数

            for line in lines_total:
                if line[0] not in char_8105:
                    continue

                # parts = line.strip().split('\t')
                parts = re.split(r'\t+',line.strip())
                if len(parts) >= 3:
                    word, code, weight = parts[0], parts[1], parts[2]
                elif len(parts) == 2:
                    word, code, weight = parts[0], parts[1], 0
                else:
                    continue  # 跳过格式不正确的行

                if len(word) != word_len:
                    continue

                # 🚨 这里 code.split(' ')[i] in pinyin_8105_map[w] 本来写成了
                # code in pinyin_8105_map[w] 导致只能输出长度为 1 的字
                # if all((w in char_8105 and code.split(' ')[i] in pinyin_8105_map[w]) for i, w in enumerate(word)):
                if all(w in char_8105 for i, w in enumerate(word)):
                    
                    if word not in res_dict:
                        line_count += 1
                        res +=  f'{word}\t{code}\t{weight}\n'
                        res_dict[word] = set()
                        res_dict[word].add(code)
                        continue

                    if code not in res_dict[word]:
                        line_count += 1
                        res +=  f'{word}\t{code}\t{weight}\n'
                        res_dict[word].add(code)

            if (line_count) > 0:
                line_count_sum += line_count
                print('✅  » 已合并处理生成 %s 字词语，共计 %s 行' % (word_len, line_count))

        print('☑️  共生成 %s 行数据' % (line_count_sum))
        o.write(get_header_wubi(out_file_name))
        o.write(res)



if __name__ == '__main__':
    proj_dir = Path(__file__).resolve().parent.parent

    print(proj_dir)
    default_file_endswith_filter = ''

    default_src_dir = 'src'
    default_out_dir = 'out'

    src_dir = input(f"输入文件目录（默认：{default_src_dir}）：").strip() or default_src_dir
    out_dir = input(f"输出文件目录（默认：{default_out_dir}）：").strip() or default_out_dir
    # file_endswith_filter = input(f"请输入输入过滤的文件末尾字符串（默认：{default_file_endswith_filter}）：").strip() or default_file_endswith_filter
    file_endswith_filter = default_file_endswith_filter

    src_dir = proj_dir / src_dir  # 设置待处理的拼音词库文件夹
    out_dir = proj_dir / out_dir  # 转换后输出的五笔词库文件夹

    out_file_name = 'wubi86.dict.yaml'
    out_file_path = out_dir / out_file_name
    
    if out_file_path.exists():
        out_file_path.unlink()
        
    # 如果存在输出文件，先删除
    if not out_dir.exists():
        out_dir.mkdir()

    filter_8105(src_dir, out_dir, file_endswith_filter)
