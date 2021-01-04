# create by: wangyun
# create at: 2020/4/19 9:30
import json

import requests


"""
接口发送请求，并返回响应信息
1. 支持获取响应头
2. 支持获取响应体
"""


class RequestBase:

    def __init__(self, request_type, request_url, request_body, request_headers, intf_type=None):
        """
        请求接口公共类
        :param request_type: 请求类型：post, get
        :param request_url: 请求url地址
        :param request_headers:  请求头
        :param request_body:  请求体（xml类型传入字符串格式，json类型数据必须传入json格式，不能传入字典）
        :param intf_type:  接口类型：webservice， api，分别对应接口数据格式：xml， json
        """
        self.request_type = request_type
        self.request_url = request_url
        self.request_body = request_body
        self.request_headers = request_headers

        self.intf_type = intf_type
        self.res = self.__send_request()

    # 发送请求
    def __send_request(self):
        if not isinstance(self.request_type, str):
            print('请求类型格式错误。')
            return None
        if self.request_type.upper() not in ['GET', 'POST', 'HEAD', 'OPTIONS', 'PUT', 'DELETE', 'TRACE', 'CONNECT']:
            print('请求类型不存在。')
            return None
        # my_log().debug('发送请求： 请求类型[%s], 请求地址[%s], 请求头[%s], 请求体[%s]' % (self.request_type, self.request_url, self.request_headers, self.request_body))
        res = requests.request(method=self.request_type, url=self.request_url, data=self.request_body.encode('utf-8'), headers=self.request_headers)
        # my_log().debug('返回响应： %s', res)
        return res

    # 获取响应
    def get_respond(self):
        return self.res

    # 获取响应头
    def get_respond_head(self):
        head = self.res.headers
        # my_log().debug('响应头： %s' % head)
        return head

    # 获取响应体
    def get_respond_body(self):
        if self.res.content:
            respond = self.res.text
            # my_log().debug('响应体： %s' % respond)
            return respond
