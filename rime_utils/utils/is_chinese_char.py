#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
判断一个字符是否为中文字符

该脚本定义了一个函数 `is_chinese_char`，用于判断给定的字符是否为中文字符。
中文字符的范围包括：
1. 基本汉字 (0x4E00 - 0x9FFF)
2. 扩展A区汉字 (0x3400 - 0x4DBF)
3. 扩展B区汉字 (0x20000 - 0x2A6DF)
4. 扩展C区汉字 (0x2A700 - 0x2B73F)
5. 扩展D区汉字 (0x2B740 - 0x2B81F)
6. 扩展E区汉字 (0x2B820 - 0x2CEAF)
7. 扩展F区汉字 (0x2CEB0 - 0x2EBEF)
8. 扩展G区汉字 (0x30000 - 0x3134F)
9. 兼容汉字 (0xF900 - 0xFAFF)

作者: [你的名字]
日期: [日期]
版本: 1.1
"""

def is_chinese_char(char: str) -> bool:
    """
    判断一个字符是否为中文字符。

    参数:
        char (str): 需要判断的单个字符。

    返回:
        bool: 如果是中文字符返回 True，否则返回 False。

    示例:
        >>> is_chinese_char('中')
        True
        >>> is_chinese_char('A')
        False
    """
    # 获取字符的 Unicode 编码
    code = ord(char)

    # 判断字符是否在以下中文字符范围内
    return (
            (0x4E00 <= code <= 0x9FFF) or  # 基本汉字
            (0x3400 <= code <= 0x4DBF) or  # 扩展A区汉字
            (0x20000 <= code <= 0x2A6DF) or  # 扩展B区汉字
            (0x2A700 <= code <= 0x2B73F) or  # 扩展C区汉字
            (0x2B740 <= code <= 0x2B81F) or  # 扩展D区汉字
            (0x2B820 <= code <= 0x2CEAF) or  # 扩展E区汉字
            (0x2CEB0 <= code <= 0x2EBEF) or  # 扩展F区汉字
            (0x30000 <= code <= 0x3134F) or  # 扩展G区汉字
            (0xF900 <= code <= 0xFAFF)  # 兼容汉字
    )


# 测试代码
if __name__ == "__main__":
    # 测试用例
    test_cases = [
        ('中', True),  # 基本汉字
        ('𠮷', True),  # 扩展B区汉字
        ('𫝆', True),  # 扩展F区汉字
        ('𫠠', True),  # 扩展G区汉字
        ('A', False),  # 英文字符
        ('あ', False),  # 日文字符
        ('🌏', False),  # 表情符号
    ]

    # 运行测试
    for char, expected in test_cases:
        result = is_chinese_char(char)
        print(f"字符: {char}, 预期: {expected}, 实际: {result}")
        assert result == expected, f"测试失败: 字符 {char} 的预期结果为 {expected}，但实际结果为 {result}"

    print("所有测试通过！")