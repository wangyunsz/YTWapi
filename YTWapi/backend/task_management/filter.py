# create by: wangyun
# create at: 2020/9/22 11:13
import django_filters

from backend.task_management.models import TTaskManagementMain, TTestCaseResult, TTestCaseStepResult


# 任务表
class TTaskManagementMainFilter(django_filters.rest_framework.FilterSet):
    execute_stamp = django_filters.CharFilter(field_name='execute_stamp')
    task_id = django_filters.CharFilter(field_name='task_id')
    task_name = django_filters.CharFilter(field_name='task_name', lookup_expr='icontains')
    status = django_filters.CharFilter(field_name='status')

    class Meta:
        model = TTaskManagementMain
        fields = ('id', 'execute_stamp', 'task_id', 'task_name', 'status')


# 测试用例执行结果
class TTestCaseResultFilter(django_filters.rest_framework.FilterSet):
    execute_stamp = django_filters.CharFilter(field_name='execute_stamp')

    class Meta:
        model = TTestCaseResult
        fields = ('id', 'execute_stamp')


# 测试用例步骤执行结果
class TTestCaseStepResultFilter(django_filters.rest_framework.FilterSet):
    execute_stamp = django_filters.CharFilter(field_name='execute_stamp')
    number = django_filters.CharFilter(field_name='number')

    class Meta:
        model = TTestCaseStepResult
        fields = ('id', 'execute_stamp', 'number')
