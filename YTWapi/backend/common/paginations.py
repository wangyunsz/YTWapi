# create by: wangyun
# create at: 2020/9/4 10:38
from collections import OrderedDict

from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class StandarPagination(PageNumberPagination):
    # page_size = 10  # 默认每页显示条数配置
    page_query_param = 'curpage'  # “页数”的请求参数名称, 默认是page
    page_size_query_param = 'pagesize'  # “分页大小”的请求参数名称

    # 进入父类 PageNumberPagination 可看响应体返回字段.
    #  def get_paginated_response(self, data):
    #  return Response(OrderedDict([
    #    ('count', self.page.paginator.count),
    #    ('next', self.get_next_link()),
    #    ('previous', self.get_previous_link()),
    #    ('results', data)
    #  ]))

    # 觉得不适用, 那就拷贝出来,重载函数, 自己多加几个字段.
    # (可通过官方文档或直接调试得知从哪些属性获取正确的值.)
    def get_paginated_response(self, data):
        return Response(
            OrderedDict([
                ('total', self.page.paginator.count),
                # ('next', self.get_next_link()),
                # ('previous', self.get_previous_link()),
                ('curpage', self.page.number),
                ('total_page', self.page.paginator.num_pages),
                ('pagesize', self.page.paginator.per_page),
                ('results', data)
            ])
        )
