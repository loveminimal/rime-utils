# 根据 meta/8105.py.yaml 生成不带声调一字一音的拼音词库
import os
import shutil
from pathlib import Path


current_dir = Path.cwd()
src_dir = current_dir / 'meta'
out_dir = current_dir / 'out'

str1 = 'āáǎàōóǒòēéěèīíǐìūúǔùǖǘǚǜüńňǹ'
str2 = 'aaaaooooeeeeiiiiuuuuvvvvvnnn'
list_str1 = list(str1)
list_str2 = list(str2)

# 如果存在输出文件，先删除
if os.path.exists(out_dir):
    shutil.rmtree(out_dir)
os.mkdir(out_dir)

# 遍历源文件夹文件，处理
for file_path in src_dir.iterdir():
    if file_path.is_file():
        file_name = file_path.name
        if not file_name.endswith(('8105.py.yaml')):
            continue

        print(file_name)
        
        src_file_path = src_dir / file_name
        out_file_path = out_dir / file_name

        with open(src_file_path, 'r', encoding='utf-8') as f:
            num = 0
            res = ''
            for line in f.readlines():
                if line.startswith(('#', ' ', '\n', '-', '.', 'n', 'v', 's', 'c')):    # 忽略非词表行
                    res = res + line
                else:
                    # line.replace()
                    # print(line.strip())
                    for idx, char in enumerate(list_str1):
                        line = line.replace(char, list_str2[idx])
                    # print(line)

                    line_list = line.strip().split('\t')

                    ll3_set = set(line_list[3].split(', '))
                    if len(ll3_set) >= 1:
                        for pinyin in ll3_set:
                            res = res + f'{line_list[1]}\t{pinyin}\n'
                    else:
                        res = res + f'{line_list[1]}\t{pinyin}\n'


            # str1 = 'āáǎàōóǒòēéěèīíǐìūúǔùǖǘǚǜü'
            # str2 = 'aaaaooooeeeeiiiiuuuuvvvvv'
            

                    
            with open(out_file_path, 'w', encoding='utf-8') as o:
                o.write(res)


