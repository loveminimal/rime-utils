def is_chinese_char(char):
    code = ord(char)
    return (0x4E00 <= code <= 0x9FFF) or \
           (0x3400 <= code <= 0x4DBF) or \
           (0x20000 <= code <= 0x2A6DF) or \
           (0x2A700 <= code <= 0x2B73F) or \
           (0xF900 <= code <= 0xFAFF)

# 测试
# print(is_chinese_char('中'))  # True
# print(is_chinese_char('A'))   # False