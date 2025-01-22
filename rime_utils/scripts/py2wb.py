import re
from pathlib import Path
from rime_utils.data.wubi86_18030_map import wubi86_18030_map
from rime_utils.data.char_8105 import char_8105
from rime_utils.utils.timer import timer
from rime_utils.utils.is_chinese_char import is_chinese_char



@timer
def convert(src_dir, out_dir, file_endswith_filter):
    dict_num = 0
    num = 0  # 统计文件中不包含在 wubi86_18030_map 中的字的行数
    res = ''  # 生成的词库串
    res_dict = {}
    count = 0  # 统计文件中词组包含非文字行的数量

    # 遍历源文件夹文件，处理
    for file_path in src_dir.iterdir():
        res_set = set()

        if file_path.is_file():
            dict_num = dict_num + 1

            if not file_path.name.endswith(file_endswith_filter):
                continue
            print('☑️  已加载第 %d 份码表 » %s' % (dict_num, file_path))

            # 添加词库头
            # with open(out_dir / file_path.name, 'a', encoding='utf-8') as o:
            #     o.write(get_header(file_name))

            with open(src_dir / file_path.name, 'r', encoding='utf-8') as f:
                lines_list = f.readlines()

        for line in lines_list:
            if is_chinese_char(line[0]):
                line_arr = re.split(r'\s{0,2}\t\s{0,2}', line.strip())
                
                if len(line_arr) == 1:
                    word, pinyin, weight = line_arr[0], 'zzzz', 0
                elif len(line_arr) == 2:
                    if line_arr[1][0] in '1234567890':
                        word, pinyin, weight = line_arr[0], 'zzzz', line_arr[1]
                    else:
                        word, pinyin, weight = line_arr[0], line_arr[1], 0
                elif len(line_arr) >= 3:
                        if line_arr[1][0] in '1234567890':
                            word, pinyin, weigth = line_arr[0], line_arr[2], line_arr[1]
                        else:
                            word, pinyin, weight = line_arr[0], line_arr[1], line_arr[2]
                    


            # 统计并列出文件中词组包含的非文字行
            ctn = False
            for w in word:
                # if w in '+/.,()0123456789qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM':
                if w not in char_8105:
                    count = count + 1
                    # print(f'{count} - {line.strip()}')
                    ctn = True
            if ctn:
                continue
                
            # 对字词进行遍历处理并组合成五笔字库结构
            if len(word) == 1:
                # ^ 单字情况
                if wubi86_18030_map.get(word):
                    res_set.add(f'{word}\t{wubi86_18030_map[word]}\t{weight}\n')
                else:
                    num = num + 1
                    print(f'{num} - {word}')
                    res_set.add(f'{word}\tzzzz\t{weight}\n')
            elif len(word) == 2:
                # ^ 2字词
                for w in word:
                    if not wubi86_18030_map.get(w):
                        num = num + 1
                        print(f'{num} - {word}')

                res_set.add(f'{word}\t{wubi86_18030_map[word[0]][:2]}{wubi86_18030_map[word[1]][:2]}\t{weight}\n')
            elif len(word) == 3:
                # ^ 3字词
                for w in word:
                    if not wubi86_18030_map.get(w):
                        num = num + 1
                        print(f'{num} - {word}')

                res_set.add(f'{word}\t{wubi86_18030_map[word[0]][0]}{wubi86_18030_map[word[1]][0]}{wubi86_18030_map[word[2]][:2]}\t{weight}\n')
            elif len(word) >= 4:
                # ^ 4+字词
                for w in word:
                    if not wubi86_18030_map.get(w):
                        num = num + 1
                        print(f'{num} - {word}')

                res_set.add(f'{word}\t{wubi86_18030_map[word[0]][0]}{wubi86_18030_map[word[1]][0]}{wubi86_18030_map[word[2]][0]}{wubi86_18030_map[word[len(word) - 1]][0]}\t{weight}\n')

        res = ''.join(res_set)
        with open(out_dir / (file_path.stem + '.dict.yaml'), 'w', encoding='utf-8') as o:
            o.write(res)


if __name__ == '__main__':
    proj_dir = Path(__file__).resolve().parent.parent
    
    print(proj_dir)

    
    out_file = 'py2wb.dict.yaml'

    default_file_endswith_filter = '.txt'
    default_src_dir = 'src/data'
    default_out_dir = 'out'
    
    src_dir = input(f"输入文件目录（默认：{default_src_dir}）：").strip() or default_src_dir
    out_dir = input(f"输出文件目录（默认：{default_out_dir}）：").strip() or default_out_dir
    file_endswith_filter = input(f"过滤的文件末尾（默认：{default_file_endswith_filter}）：").strip() or default_file_endswith_filter
    
    src_dir = proj_dir / src_dir  # 设置待处理的拼音词库文件夹
    out_dir = proj_dir / out_dir  # 转换后输出的五笔词库文件夹

    # 如果存在输出文件，先删除
    if not out_dir.exists():
        out_dir.mkdir()

    convert(src_dir, out_dir, file_endswith_filter)
