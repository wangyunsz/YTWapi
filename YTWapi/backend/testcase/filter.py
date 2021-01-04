# create by: wangyun
# create at: 2020/8/26 10:51

import django_filters

from backend.testcase.models import TTestCaseMain, TTestCaseStep, TTestCaseAssert, TMakeCaseInterfaceList


# 生成用例接口列表
class TMakeCaseInterfaceListFilter(django_filters.rest_framework.FilterSet):
    mc_id = django_filters.NumberFilter(field_name='mc_id')
    req_addr = django_filters.CharFilter(field_name='req_addr')

    class Meta:
        model = TMakeCaseInterfaceList
        fields = ('id', 'mc_id', 'step_no', 'req_addr', 'req_type', 'req_header', 'req_body', 'res_header', 'res_body', 'instance_id')


# 测试用例主表
class TTestCaseMainFilter(django_filters.rest_framework.FilterSet):
    number = django_filters.CharFilter(field_name='number')
    title = django_filters.CharFilter(field_name='title', lookup_expr='icontains')
    mid = django_filters.NumberFilter(field_name='mid')

    class Meta:
        model = TTestCaseMain
        fields = ('id', 'number', 'title', 'mid', 'bsid', 'level', 'is_enable', 'creator', 'create_time', 'update_time', 'remark')


# 测试用例步骤
class TTestCaseStepFilter(django_filters.rest_framework.FilterSet):
    tc_id = django_filters.NumberFilter(field_name='tc_id')
    inc_id = django_filters.NumberFilter(field_name='inc_id')
    header = django_filters.CharFilter(field_name='header')
    body = django_filters.CharFilter(field_name='body')
    step_no = django_filters.NumberFilter(field_name='step_no')

    class Meta:
        model = TTestCaseStep
        fields = ('id', 'tc_id', 'inc_id', 'header', 'body', 'step_no')


# 测试用例步骤断言
class TTestCaseAssertFilter(django_filters.rest_framework.FilterSet):
    sid = django_filters.NumberFilter(field_name='sid')
    field_owner = django_filters.CharFilter(field_name='field_owner')
    field_node = django_filters.CharFilter(field_name='field_node')
    assert_type = django_filters.CharFilter(field_name='assert_type')
    field_value = django_filters.CharFilter(field_name='field_value')

    class Meta:
        model = TTestCaseAssert
        fields = ('id', 'sid', 'field_owner', 'field_node', 'assert_type', 'field_value')


