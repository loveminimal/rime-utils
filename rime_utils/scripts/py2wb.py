import os
import re
import sys
import shutil
from pathlib import Path
# from header import get_header
from data.wubi86yd import get_wubi86yd
from timer import timer
from is_chinese_char import is_chinese_char

wubi86yd = get_wubi86yd()

@timer
def convert(src_dir, out_dir, file_endswith_filter):
	dict_num = 0
	num = 0			# 统计文件中不包含在 wubi86yd 中的字的行数
	res = ''		# 生成的词库串
	res_dict = {}
	count = 0		# 统计文件中词组包含非文字行的数量

	# 遍历源文件夹文件，处理
	for file_path in src_dir.iterdir():
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
			if not is_chinese_char(line[0]):
				res = res + line
			else:
				line_arr = line.strip().split('\t')

				word = line_arr[0]
				# pinyin = line_arr[1]
				pinyin = ''
				weight =  line_arr[2] if len(line_arr) > 1 else '0'

				# 统计并列出文件中词组包含的非文字行
				ctn = False
				for w in word:
					if w in '.,()0123456789qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM':
						count = count + 1
						print(f'{count} - {line.strip()}')
						ctn = True
				if ctn:
					continue

				# 对字词进行遍历处理并组合成五笔字库结构
				if len(word) == 1:
					# ^ 单字情况
					if wubi86yd.get(word):
						res = res + f'{word}\t{wubi86yd[word]}\t{pinyin}{weight}\n'
					else:
						num = num + 1
						print(f'{num} - {word}')
						res = res + f'{word}\txxxx\t{pinyin}{weight}\n'
				elif len(word) == 2:
					# ^ 2字词
					for w in word:
						if not wubi86yd.get(w):
							num = num + 1
							print(f'{num} - {word}')

					res = res + f'{word}\t{wubi86yd[word[0]][:2]}{wubi86yd[word[1]][:2]}\t{pinyin}{weight}\n'
				elif len(word) == 3:
					# ^ 3字词
					for w in word:
						if not wubi86yd.get(w):
							num = num + 1
							print(f'{num} - {word}')

					res = res + f'{word}\t{wubi86yd[word[0]][0]}{wubi86yd[word[1]][0]}{wubi86yd[word[2]][:2]}\t{pinyin}{weight}\n'
				elif len(word) >= 4:
					# ^ 4+字词
					for w in word:
						if not wubi86yd.get(w):
							num = num + 1
							print(f'{num} - {word}')

					res = res + f'{word}\t{wubi86yd[word[0]][0]}{wubi86yd[word[1]][0]}{wubi86yd[word[2]][0]}{wubi86yd[word[len(word) - 1]][0]}\t{pinyin}{weight}\n'


		with open(out_dir / file_path.name, 'w', encoding='utf-8') as o:
			o.write(res)


if __name__ == '__main__':
	current_dir = Path.cwd()

	src = 'src'
	out = 'out'
	file_endswith_filter = ''
	multifile_out_mode = 0

	# 命令行输入选项
	# ... py scripts/wubi86.py [-i src] [-o out] [-f file_endswith_filter] [-m multifile_out_mode]
	for i, arg in enumerate(sys.argv):
		if arg == "-i":
			src = sys.argv[i + 1]
		elif arg == '-o':
			out = sys.argv[i + 1]
		elif arg == '-f':
			file_endswith_filter = sys.argv[i + 1]
		elif arg == '-m':
			multifile_out_mode = sys.argv[i + 1]

	src_dir = current_dir / src				# 设置待处理的拼音词库文件夹
	out_dir =  current_dir / out			# 转换后输出的五笔词库文件夹

	# 如果存在输出文件，先删除
	if out_dir.exists():
		shutil.rmtree(out_dir)
	os.mkdir(out_dir)

	convert(src_dir, out_dir, file_endswith_filter)
