# -*- coding: utf-8 -*-

"""
函数执行时间统计装饰器

该脚本实现了一个装饰器 `timer`，用于统计被装饰函数的执行时间。通过记录函数开始和结束的时间戳，计算并输出函数的执行时间。

使用方法：
1. 在需要统计执行时间的函数上添加 `@timer` 装饰器。
2. 调用函数时，会自动输出函数的执行时间。

依赖库：
- 无

作者: [Jack Liu]
日期: [2025-01-21]
版本: 1.0
"""

import time
from functools import wraps


def timer(func):
    """
    统计函数执行时间的装饰器

    该装饰器会记录被装饰函数的执行时间，并在函数执行完成后输出执行时间。

    :param func: 被装饰的函数
    :return: 装饰后的函数
    """

    @wraps(func)  # 保留原函数的元信息（如函数名、文档字符串等）
    def wrapper(*args, **kwargs):
        start_time = time.time()  # 记录函数开始执行的时间
        result = func(*args, **kwargs)  # 执行被装饰的函数
        end_time = time.time()  # 记录函数执行结束的时间
        print(f"⏰ 函数 {func.__name__} 执行时间: {end_time - start_time:.4f} 秒")
        return result  # 返回函数的执行结果

    return wrapper


# 示例用法
if __name__ == "__main__":
    @timer
    def example_function(n):
        """
        示例函数，模拟耗时操作
        """
        time.sleep(n)
        print("示例函数执行完毕")


    # 测试装饰器
    example_function(2)  # 调用示例函数，输出执行时间
