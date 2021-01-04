# create by: wangyun
# create at: 2020/9/30 9:44
from backend.common.func.func_datetime import DateTime
from backend.common.func.func_random import Random


# 日期时间函数
def timestamp(**kwargs):
    return DateTime(**kwargs).get_date_time()


# 随机函数
# 随机数字
def randomnum(**kwargs):
    return Random().get_random_num_from_range(**kwargs)


# 随机字符串
def randomstr(**kwargs):
    return Random().get_random_str(**kwargs)


# ========函数动态调用==============
def func_suite(func_name, **kwargs):
    try:
        return eval(func_name)(**kwargs)
    except:
        return None


if __name__ == '__main__':
    t = {'stamp': '%Y%m%d', 'days': 1, 'set_time': '000000'}
    print(func_suite('timestamp', **t))
    print(func_suite('randomstr', length=10))

    print(func_suite('randomnum', min=0, max=100))