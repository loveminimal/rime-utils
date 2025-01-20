# 处理五笔词库 - 删除非国标 8105-2023 单字及其所组词语
# - en_dicts/1en_ext.dict.yaml
# - en_dicts/2en..dict.yaml
# - en_dicts/3en_ext_yd.dict.yaml
# 支持：
# ... 按字数合并排序
# ... 按字数分表生成
# 
import os
import sys
import re
import shutil
from pathlib import Path
from header import get_en_header
from timer import timer

@timer
def convert(SRC_DIR, OUT_DIR, FILE_ENDSWITH_FILETER, MULTIFILE_OUT_MODE):
	# 遍历源文件夹文件，处理
	dict_num = 0
	res_dict = {}
	code_list = []
	lines_total = []

	for file_path in SRC_DIR.iterdir():
		if file_path.is_file() and file_path.name.endswith(FILE_ENDSWITH_FILETER):
			dict_num = dict_num + 1
			print('☑️  已加载第 %d 份码表 » %s' % (dict_num, file_path))

			with open(file_path, 'r', encoding='utf-8') as f:
				lines = f.readlines()
				lines_total.extend(lines)

	# 设定最大统计字长列表 - 15个字
	word_len_list = list(range(60))
	# lines_list = set()
	lines_list = []
	for word_len in word_len_list:
		res = ''
		for line in lines_total:
			# 从首个包含 8105 单字开头的行开始处理
			# if line[0] not in '&#-. ' and line.strip() not in ['name: en', 'version: "2024-12-27"','version: "2024-12-28"','sort: by_weight','name: en_ext','name: en_ext_yd','']:
			if line[0] not in '&#-. ' and line.strip() not in \
				['name: en', \
				'version: "2024-12-27"',\
				'version: "2024-12-28"',\
				'sort: by_weight',\
				'name: en_ext',\
				'name: en_ext_yd',\
				'']:
				# print(line)
				line_list = re.split(r'\t+',line.strip())
				if len(line_list) < 2:
					print(line)
				word = line_list[0]
				# code = line_list[1].lower()
				code = re.sub( r'(-|\'|:)', '', line_list[1].upper())
				weight = line_list[2] if len(line_list) > 2 else '0'

				# 按字长顺序过滤依次处理 1, 2, 3, 4 ...
				# if len(word) == word_len and all(w in pinyin8105 for w in word):
				if len(word) == word_len:
					# 仅处理已合成词典中 不存在 或 已存在但编码不同的字词
					# if word not in res_dict or code not in res_dict[word]:
					if True:
					# if not any(w in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ' for w in code):
						res = res + f'{word}\t{code}\t{weight}\n'
						# code_list.append(code)
						# res_dict[word] = code_list
						lines_list.append(f'{word}\t{code}\t{weight}\n')

		# if len(res.strip()) > 0:
		# 	MULTIFILE_OUT_MODE = int(MULTIFILE_OUT_MODE)
		# 	# 按字长生成多个文件
		# 	if MULTIFILE_OUT_MODE == 1:
		# 		with open(OUT_DIR / f'en_{word_len}.dict.yaml', 'a', encoding='utf-8') as o:
		# 			print('✅  » 已合并处理生成 %s 字文件' % word_len)
		# 			o.write(get_en_header(f'en_{word_len}.dict.yaml'))
		# 			o.write(res)
		# 	# 统一生成在单个文件
		# 	elif MULTIFILE_OUT_MODE == 0:
		# 		with open(OUT_DIR / f'en.dict.yaml', 'a', encoding='utf-8') as o:
		# 			print('✅  » 已合并处理生成 %s 字词语' % word_len)
		# 			word_len == 1 and o.write(get_en_header(f'en.dict.yaml'))	# 仅字长为 1 时添加表头
		# 			o.write(res)

	# lines_list = list(set(lines_list))
	# print(len(lines_list))
	unique_list = []
	[unique_list.append(item) for item in lines_list if item not in unique_list]
	# unique_list = [item for item in lines_list]
	# unique_list.sort(key=lambda x: x.casefold())
	# print(len(unique_list))
	result = ''.join(unique_list)
	with open(OUT_DIR / f'en.dict.yaml', 'a', encoding='utf-8') as o:
		print(f'✅  » 已合并排序去重英文码表 - 共 {len(lines_list)} » {len(unique_list)} 条')
		o.write(get_en_header(f'en.dict.yaml'))	# 仅字长为 1 时添加表头
		o.write(result)

if __name__ == '__main__':
	current_dir = Path.cwd()

	src = 'en_dicts'
	out = 'out'
	file_endswith_filter = '.dict.yaml'
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
