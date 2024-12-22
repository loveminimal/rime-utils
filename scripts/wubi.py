import os
import shutil
from pathlib import Path
# from scripts.old.header import get_header


current_dir = Path.cwd()
src_dir = current_dir / 'draft'
out_dir = current_dir / 'out'

# 如果存在输出文件，先删除
if os.path.exists(out_dir):
	shutil.rmtree(out_dir)
os.mkdir(out_dir)

# 遍历源文件夹文件，处理
for file_path in src_dir.iterdir():
	if file_path.is_file():
		file_name = file_path.name
		# print(file_name)
		if  file_name.endswith('.draft.txt'):
			continue

		src_file_path = src_dir / file_name
		out_file_path = out_dir / file_name
		
		# 添加词库头
		# with open(out_file_path, 'a', encoding='utf-8') as o:
		#     o.write(get_header(file_name))


		with open(src_file_path, 'r', encoding='utf-8') as f:
			num = 0
			for line in f.readlines():
				if not line.startswith(('#', ' ', '\n')):    # 忽略非词表行
					line_arr = line.strip().split(' ')
					# print(len(line_arr[1]))
					res = ''
					# if (len(line_arr[1]) == 1 and ('\u4e00' <= line_arr[1][:1] <= '\u9fff')):
					if (len(line_arr[1]) == 1):
						# print(f'{line_arr[1]}\t{line_arr[0]}')
						res = line_arr[1] + '\t' + line_arr[0] + '\n'
					
					with open(out_file_path, 'a', encoding='utf-8') as o:
					    o.write(res)


