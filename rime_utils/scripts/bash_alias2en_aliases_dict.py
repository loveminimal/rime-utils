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
from header import get_en_aliases_header
from timer import timer

@timer
def convert(src_dir, out_dir, file_endswith_filter, multifile_out_mode):
	# 遍历源文件夹文件，处理
	dict_num = 0
	lines = []

	for file_path in src_dir.iterdir():
		if file_path.is_file() and file_path.name.endswith(file_endswith_filter):
			dict_num = dict_num + 1
			print('☑️  已加载第 %d 份码表 » %s' % (dict_num, file_path))

			with open(file_path, 'r', encoding='utf-8') as f:
				lines = f.readlines()

	lines_list = []
	res = ''
	is_start = False
	for line in lines:
		if not is_start and not line.startswith('alias'):
			continue
		# elif line.strip() == '':
		# 	res = res + line
		else:
			is_start = True
			if not line.startswith('#') and line.strip() != '':
				line_list = re.split(r'(alias |=["\'])',line.strip()[:-1])
				# ['', 'alias ', 'cphs', '="', 'cp ~/.bash_aliases ~/.shell/']
				alias = line_list[2]
				cmd = line_list[4]

				res = res + f'{cmd}\t{alias}\t0\n'
			else:
				res = res + line
		
	with open(out_dir / f'en_aliases.dict.yaml', 'a', encoding='utf-8') as o:
		print(f'✅  » 已合并排序去重英文码表 - 共 {len(lines_list)} 条')
		o.write(get_en_aliases_header(f'en_aliases.dict.yaml'))	# 仅字长为 1 时添加表头
		o.write(res)

if __name__ == '__main__':
	current_dir = Path.cwd()

	src = 'dicts/en_dicts'
	out = 'out'
	file_endswith_filter = '.bash_aliases'
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
