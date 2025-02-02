# get_en_dict.py 
# by Jack Liu
# 生成英文词典词库，方便查词
# 词库来源 https://github.com/KyleBing/english-vocabulary
# 
import os
import sys
import re
import shutil
from pathlib import Path
from rime_utils.data.header import get_en_dict_header
from rime_utils.utils.timer import timer

@timer
def convert(src_dir, out_dir, file_endswith_filter, multifile_out_mode):
	# 遍历源文件夹文件，处理
	dict_num = 0
	res_dict = {}
	code_list = []
	lines_total = []

	for file_path in src_dir.iterdir():
		if file_path.is_file() and file_path.name.endswith(file_endswith_filter):
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
			# print(line)
			line_list = re.split(r'\t+',line.strip())
			if len(line_list) < 2:
				print(line)
			en = line_list[0].strip()
			zh = ''.join(line_list[1].split(' ')[1:])
			zh = re.sub(r'([a-z]+\.)', r' \1', zh)
			weight = line_list[2] if len(line_list) > 2 else '0'

			# 按字长顺序过滤依次处理 1, 2, 3, 4 ...
			if len(en) == word_len:
				if all(ch not in en for ch in ' -./'):
					lines_list.append(f'{en} {zh}\t{en.lower()}\n')



	unique_list = []
	[unique_list.append(item) for item in lines_list if item not in unique_list]
	# unique_list.sort()
	unique_list.sort(key=lambda x: x.casefold())
	result = ''.join(unique_list)
	with open(out_dir / f'{out_file}', 'a', encoding='utf-8') as o:
		print(f'✅  » 已合并排序去重英文码表 - 共 {len(lines_list)} » {len(unique_list)} 条')
		o.write(get_en_dict_header(f'{out_file}'))	# 仅字长为 1 时添加表头
		o.write(result)

if __name__ == '__main__':
	current_dir = Path.cwd()

	src = 'src'
	out = 'out'
	file_endswith_filter = 'en2zh.txt'
	multifile_out_mode = 0

	out_file = 'en.dict.yaml'

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
