import chardet

def detect_file_encoding(file_path):
    with open(file_path, 'rb') as f:
        raw_data = f.read()
    
    result = chardet.detect(raw_data)
    return result['encoding']

# 检测当前文件的编码格式
# current_file = __file__  # 获取当前文件的路径
# encoding = detect_file_encoding(current_file)
# print(f"当前文件的编码格式是: {encoding}")