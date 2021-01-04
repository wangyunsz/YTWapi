# create by: wangyun
# create at: 2020/9/30 9:52
import time
import datetime


class DateTime:

    def __init__(self, stamp=None, days=0, set_time=''):
        """
        日期时间类
        :param stamp:  日期格式(如：'%Y-%m-%d %H:%M:%S.%f')，若为None，则输出时间戳格式（如：1601436837）
        :param days:    时间加减天数，默认当天
        :param set_time: 获取时间字符串，可设置固定时间，如（000000， 235959）
        """
        self.stamp = stamp
        self.days = days
        self.set_time = set_time

    def get_date_time(self):
        if not self.stamp:
            return int(time.mktime(datetime.datetime.now().timetuple()))
        try:
            now = datetime.datetime.now()
            new_date = now + datetime.timedelta(days=int(self.days))
            new_date_stamp = new_date.strftime(self.stamp)
            return new_date_stamp + self.set_time
        except:
            return None


if __name__ == '__main__':
    print(DateTime(stamp='%Y%m%d', days=5, set_time='235959').get_date_time())
