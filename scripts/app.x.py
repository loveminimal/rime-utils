# 测试脚本 ❌
import os
import shutil
from pathlib import Path
from header import get_header


current_dir = Path.cwd()
src_dir = current_dir / 'src'
out_dir = current_dir / 'out'

# 如果存在输出文件，先删除
if os.path.exists(out_dir):
    shutil.rmtree(out_dir)
os.mkdir(out_dir)

# 遍历源文件夹文件，处理
for file_path in src_dir.iterdir():
    if file_path.is_file():
        file_name = file_path.name
        print(file_name)
        if not file_name.endswith(('dict.yaml', 'dict.yml')):
            continue

        src_file_path = src_dir / file_name
        out_file_path = out_dir / file_name
        
        # 添加词库头
        with open(out_file_path, 'a', encoding='utf-8') as o:
            o.write(get_header(file_name))


        with open(src_file_path, 'r', encoding='utf-8') as f:
            num = 0
            for line in f.readlines():
                if not line.startswith(('#', ' ', '\n', '-', '.', 'n', 'v', 's', 'c')):    # 忽略非词表行
                    line_arr = line.strip().split('\t')
                    # print(line_arr)
                    la1 = line_arr[1].split('; ')
                    la1[len(la1) - 1] = la1[len(la1) - 1][:-1]
                    # print(la1)
                    res_la1 = ''
                    for wpy in la1:
                        wpy_arr = wpy.split(';')

                        wpy_arr.pop(-1) # hanxin
                        wpy_arr.pop(-2) # tiger
                        wpy_arr.pop(-2) # cj
                        wpy_arr.pop(-2) # jdh

                        wpy_arr.pop(1)  # moqi
                        wpy_arr.pop(1)  # flypy
                        wpy_arr.pop(1)  # zrm
 
                        # print(';'.join(wpy_arr))
                        res_la1 = res_la1 + ';'.join(wpy_arr) + '; '    
                    # print(line_arr[0] + '\t' + res_la1[:-1] + '\t' + line_arr[2])
                    
                    with open(out_file_path, 'a', encoding='utf-8') as o:
                        o.write(line_arr[0] + '\t' + res_la1[:-1] + '\t' + line_arr[2] + '\n')


