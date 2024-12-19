from datetime import datetime

def get_header(file_name):
    header = f'''
# Rime dictionary - {file_name}
# encoding: utf-8
# 
# --- 说明 ---
# 该字典是基于白霜（» 雾凇）拼音词库的万象版本
# https://github.com/iDvel/rime-ice
# https://github.com/gaboolic/rime-frost
# https://github.com/gaboolic/rime-shuangpin-fuzhuma
# https://github.com/amzxyz/rime_wanxiang_pro
# 
# 进一步精简万象词库处理为“拼音 + 五笔前二辅助码”格式
---
name: {'.'.join(file_name.split('.')[:-2])}
version: {datetime.now().date()}
sort: by_weight
use_preset_vocabulary: false
...
'''
    return header.strip() + '\n'