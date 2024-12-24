import os
import shutil
from pathlib import Path
# from scripts.old.header import get_header
from data.pinyin8105 import pinyin8105
from data.wubi86wm18030 import get_wubi86wm18030

wubi86wm18030 = get_wubi86wm18030()

def convert(SRC_DIR, OUT_DIR, FILE_ENDSWITH_FILETER):
	# 遍历源文件夹文件，处理
	for file_path in SRC_DIR.iterdir():
		if file_path.is_file():
			file_name = file_path.name
			# print(file_name)
			if not file_name.endswith(FILE_ENDSWITH_FILETER):
				continue

			src_file_path = SRC_DIR / file_name
			out_file_path = OUT_DIR / file_name
			
			# 添加词库头
			# with open(out_file_path, 'a', encoding='utf-8') as o:
			#     o.write(get_header(file_name))


			with open(src_file_path, 'r', encoding='utf-8') as f:
				num = 0
				res = ''
				res_dict = {}
				for line in f.readlines():
					if not line.startswith(('#', ' ', '\n', '-', '.', 'n', 'v', 's', 'c')):    # 忽略非词表行
						line_arr = line.strip().split('\t')
						# print(len(line_arr[1]))
						# if (len(line_arr[0]) == 1 and ('\u4e00' <= line_arr[0][:1] <= '\u9fff')):
						# if (len(line_arr[1]) == 1 and len(line_arr[0]) > 2 and line_arr[1] in pinyin8105):
						# if len(line_arr[0]) == 1:
							# if (line_arr[1] not in pinyin8105):
							# 	print('不在8105通用字表中了 - %s' % line_arr[1])
							# res_dict[line_arr[0]] = line_arr[1]

						if wubi86wm18030.get(line_arr[0]):
							res = res + f'{line_arr[0]}\t{wubi86wm18030[line_arr[0]]}\t{line_arr[1]}\n'
						else:
							num = num + 1
							# print('' + num + line_arr[0])
							print(f'{num} - {line_arr[0]}')
				
				# for key, value in res_dict.items():
				# 	res = res + f'{key}\t{value}\n'


				with open(out_file_path, 'w', encoding='utf-8') as o:
					o.write(res)


current_dir = Path.cwd()
src_dir = current_dir / 'src'
out_dir = current_dir / 'out'

# 如果存在输出文件，先删除
if os.path.exists(out_dir):
	shutil.rmtree(out_dir)
os.mkdir(out_dir)

convert(src_dir, out_dir, 'set.yaml')
