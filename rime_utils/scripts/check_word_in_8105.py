
import sys
from pathlib import Path
from data.pinyin8105 import pinyin8105
from is_chinese_char import is_chinese_char


def check_word_in_8105(SRC_DIR, OUT_DIR, FILE_ENDSWITH_FILTER):
	# 遍历源文件夹文件，处理
	num = 0
	for file_path in SRC_DIR.iterdir():
		if file_path.is_file() and file_path.name.endswith(FILE_ENDSWITH_FILTER):
			print('» %s' % file_path)
			with open(SRC_DIR / file_path.name, 'r', encoding='utf-8') as f:
				lines = f.readlines()
				for line in lines:
					# if not line.startswith(('#', ' ', '\n', '-', '.', 'n', 'v', 's', 'c', 'u')) and line[0] not in pinyin8105:
					if is_chinese_char(line[0]) and line[0] not in pinyin8105:
						num = num + 1
						print(f'{num} - {line.strip()}')

	if num == 0:
		print('✅ 未包含不在 8105 内的字词')	
	else:
		print(f'❌ 共包含 %d 个不在 8105 内的字词' % num)

if __name__ == '__main__':
	current_dir = Path.cwd()
	src = '../src'
	out = '../out'
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

	src_dir = current_dir / src				# 设置待处理的拼音词库文件夹
	out_dir =  current_dir / out			# 转换后输出的五笔词库文件夹


	check_word_in_8105(src_dir, out_dir, file_endswith_filter)
