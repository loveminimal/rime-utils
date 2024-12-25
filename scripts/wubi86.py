import os
import shutil
from pathlib import Path
from header import get_header
# from data.wubi86yd import get_wubi86yd
from data.pinyin8105 import pinyin8105


def convert(SRC_DIR, OUT_DIR, FILE_ENDSWITH_FILETER):
	# 遍历源文件夹文件，处理
	for file_path in SRC_DIR.iterdir():
		if file_path.is_file():
			file_name = file_path.name
			# print(file_name)
			if not file_name.endswith(FILE_ENDSWITH_FILETER):
				continue
			print(file_name)

			src_file_path = SRC_DIR / file_name
			out_file_path = OUT_DIR / file_name
			
			# 添加词库头
			# with open(out_file_path, 'w', encoding='utf-8') as o:
			# 	o.write(get_header(file_name))


			with open(src_file_path, 'r', encoding='utf-8') as f:
				num = 0
				res = ''
				res_dict = {}
				for line in f.readlines():
					if line[0] in pinyin8105:
							
						line_list = line.strip().split('\t')
						word = line_list[0]
						code = line_list[1]
						weight = len(line_list) > 2 and line_list[2] or 0

						if len(word) > 1:
							continue

						if  word not in res and all(w in pinyin8105 for w in word):
							res = res + f'{word}\t{code}\t{weight}\n'


				with open(out_file_path, 'a', encoding='utf-8') as o:
					o.write(res)


current_dir = Path.cwd()
src_dir = current_dir / 'src'
out_dir = current_dir / 'out'

# 如果存在输出文件，先删除
if os.path.exists(out_dir):
	shutil.rmtree(out_dir)
os.mkdir(out_dir)

convert(src_dir, out_dir, 'wubi86.dict.yaml')
