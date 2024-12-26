from datetime import datetime

def get_header(file_name):
    header = f'''
# Rime dictionary - {file_name}
# encoding: utf-8
# 
# --- 说明 ---
# 该字典是基于官方码表版本
# - https://github.com/rime/rime-wubi
# 
# 修改内容：
# - 删除非国标 8105-2023 单字及其所组词语 
# - 按字数进行分表处理
# - 合并全国省区县扩展词表
# 
# 其他参考码表：
# - https://github.com/KyleBing/rime-wubi86-jidian
# 
---
name: {'.'.join(file_name.split('.')[:-2])}
version: {datetime.now().date()}
sort: by_weight
use_preset_vocabulary: false
...
'''
    return header.strip() + '\n'