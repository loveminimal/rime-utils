import os
import sys
import re
import shutil
from pathlib import Path
from rime_utils.data.header import get_header
from rime_utils.utils.timer import timer
from rime_utils.utils.detect_file_encoding import detect_file_encoding
from is_chinese_char import is_chinese_char

@timer
def convert(src_dir, out_dir, file_endswith_filter, multifile_out_mode):
	# 遍历源文件夹文件，处理
	dict_num = 0
	res_dict = {}
	res_list = []
	res_list_set = set()
	code_list = []
	lines_total = []

	for file_path in src_dir.iterdir():
		if file_path.is_file() and file_path.name.endswith(file_endswith_filter):
			dict_num = dict_num + 1
			file_encoding = detect_file_encoding(file_path)
			print('☑️  已加载第 %d 份码表 » %s - %s' % (dict_num, file_path, file_encoding))

		# 	if file_encoding == 'GB2312':
		# 		file_encoding = 'GB18030'

			# with open(file_path, 'r', encoding=file_encoding) as f:
			# 	content = f.read()


		# with open(out_dir / f'out.txt', 'a', encoding='utf-8') as o:
		# 	o.write(content)


			with open(file_path, 'r', encoding='utf-8') as f:
				lines = f.readlines()
				lines_total.extend(lines)


	# 设定最大统计字长列表 - 15个字
	word_len_list = list(range(40))

	for word_len in word_len_list:
		res = ''
		for line in lines_total:
			# 从首个以中文字符开头的行开始处理
			if is_chinese_char(line[0]) or line[0] in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
				line_list = re.split(r'[\t]+',line.strip())
				# print(line_list)
				word = re.sub(r'[a-z]', '',line_list[0])
				# code = line_list[1]
				weight = line_list[1] if len(line_list) > 1 else '0'

				# 按字长顺序过滤依次处理 1, 2, 3, 4 ...
				# if len(word) == word_len and all(w in pinyin8105 for w in word):
				if len(word) == word_len:
					# 仅处理已合成词典中 不存在 或 已存在但编码不同的字词
					if word not in res_list_set:
						res = res + f'{word}\t{weight}\n'
						res_list_set.add(word)
			else:
				continue

		if len(res.strip()) > 0:
			multifile_out_mode = int(multifile_out_mode)
			# 按字长生成多个文件
			if multifile_out_mode == 1:
				with open(out_dir / f'wubi86_{word_len}.dict.yaml', 'a', encoding='utf-8') as o:
					print('✅  » 已合并处理生成 %s 字文件' % word_len)
					o.write(get_header(f'wubi86_{word_len}.dict.yaml'))
					o.write(res)
			# 统一生成在单个文件
			elif multifile_out_mode == 0:
				with open(out_dir / f'big.txt', 'a', encoding='utf-8') as o:
					print('✅  » 已合并处理生成 %s 字词语' % word_len)
					# word_len == 1 and o.write(get_header(f'wubi86.dict.yaml'))	# 仅字长为 1 时添加表头
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

	convert(src_dir, out_dir, file_endswith_filter, multifile_out_mode)
