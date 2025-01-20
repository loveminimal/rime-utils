# 根据 meta/wubi86_yellow_dog.wb.dict.yaml 生成单字的词典 - 约 10 万单字
import os
import shutil
from pathlib import Path


def convert(src_dir, out_dir, file_endswith_filter):
	# 遍历源文件夹文件，处理
	for file_path in src_dir.iterdir():
		if file_path.is_file():
			file_name = file_path.name
			# print(file_name)
			if not file_name.endswith(file_endswith_filter):
				continue

			src_file_path = src_dir / file_name
			out_file_path = out_dir / file_name
			
			# 添加词库头
			# with open(out_file_path, 'a', encoding='utf-8') as o:
			#     o.write(get_header(file_name))


			with open(src_file_path, 'r', encoding='utf-8') as f:
				num = 0
				res = ''
				res_dict = {}
				for line in f.readlines():
					if not line.startswith(('#', ' ', '\n')):    # 忽略非词表行
						line_arr = line.strip().split('\t')
						
						key = line_arr[0]
						val = line_arr[1]

						if len(key) == 1:
							if key not in res_dict.keys():
								res_dict[key] = val
							else:
								if len(val) > len(res_dict[key]):
									res_dict[key] = val


							# res = res + f'{line_arr[1]}\t{line_arr[0]}\n'
				
				for key, value in res_dict.items():
					res = res + f'{key}\t{value}\n'


				with open(out_file_path, 'w', encoding='utf-8') as o:
					o.write(res)


if __name__ == '__main__':
	current_dir = Path.cwd()
	src_dir = current_dir / 'meta'
	out_dir = current_dir / 'out'

	# 如果存在输出文件，先删除
	if os.path.exists(out_dir):
		shutil.rmtree(out_dir)
	os.mkdir(out_dir)

	convert(src_dir, out_dir, 'wubi86_yellow_dog.wb.dict.yaml')