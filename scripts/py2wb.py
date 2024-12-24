import os
import shutil
from pathlib import Path
# from header import get_header
from data.wubi86yd import get_wubi86yd

wubi86yd = get_wubi86yd()

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
					if line.startswith(('#', ' ', '\n', '-', '.', 'n', 'v', 's', 'c')):    # 忽略非词表行
						res = res + line
					else:
						line_arr = line.strip().split('\t')

						word = line_arr[0]
						pinyin = line_arr[1]

						if len(word) == 1:
							# ^ 单字情况
							if wubi86yd.get(word):
								res = res + f'{word}\t{wubi86yd[word]}\t{pinyin}\n'
							else:
								num = num + 1
								# print('' + num + word)
								print(f'{num} - {word}')
								res = res + f'{word}\txxxx\t{pinyin}\n'
						elif len(word) == 2:
							# ^ 2字词
							res = res + f'{word}\t{wubi86yd[word[0]][:2]}{wubi86yd[word[1]][:2]}\t{pinyin}\n'
						elif len(word) == 3:
							# ^ 3字词
							res = res + f'{word}\t{wubi86yd[word[0]][0]}{wubi86yd[word[1]][0]}{wubi86yd[word[2]][:2]}\t{pinyin}\n'
						elif len(word) >= 4:
							# ^ 4+字词
							res = res + f'{word}\t{wubi86yd[word[0]][0]}{wubi86yd[word[1]][0]}{wubi86yd[word[2]][0]}{wubi86yd[word[len(word) - 1]][0]}\t{pinyin}\n'

				
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

convert(src_dir, out_dir, 'simp.dict.yaml')
