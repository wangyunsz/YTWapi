# create by: wangyun
# create at: 2020/9/5 20:09

import django_filters

from backend.testsuite.models import TTestSuiteMain, TTestSuiteTestCase, TExecuteConfig, TExecuteEnv


# 测试用例主表
class TTestSuiteMainFilter(django_filters.rest_framework.FilterSet):
    suite_name = django_filters.CharFilter(field_name='suite_name', lookup_expr='icontains')

    class Meta:
        model = TTestSuiteMain
        fields = ('id', 'suite_name', 'remark')


# 测试集测试用例
class TTestSuiteTestCaseFilter(django_filters.rest_framework.FilterSet):
    tsid = django_filters.CharFilter(field_name='tsid')

    class Meta:
        model = TTestSuiteTestCase
        fields = ('id', 'tsid')


# 测试执行设置
class TExecuteConfigFilter(django_filters.rest_framework.FilterSet):
    execute_name = django_filters.CharFilter(field_name='execute_name', lookup_expr='icontains')

    class Meta:
        model = TExecuteConfig
        fields = ('id', 'execute_name')


# 测试环境设置
class TExecuteEnvFilter(django_filters.rest_framework.FilterSet):
    eid = django_filters.NumberFilter(field_name='eid')

    class Meta:
        model = TExecuteEnv
        fields = ('id', 'eid')

