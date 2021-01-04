# create by: wangyun
# create at: 2020/9/30 14:26
import random


class Random:

    def __init__(self):
        pass

    # 从某个范围中获取整数
    def get_random_num_from_range(self, min, max):
        try:
            return random.randint(int(min), int(max))
        except:
            return None

    # 随机字符串（默认大小写字母、数字）
    def get_random_str(self, length=None, choice='1234567890ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'):
        rstr = ''
        try:
            for i in range(int(length)):
                rstr += random.choice(choice)
            return rstr
        except:
            return None

