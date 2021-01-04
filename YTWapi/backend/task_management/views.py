# create by: wangyun
# create at: 2020/9/13 23:02
from django.http import HttpResponse
from django_filters import rest_framework
from rest_framework import filters, viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .filter import TTaskManagementMainFilter, TTestCaseResultFilter, TTestCaseStepResultFilter
from .models import TTaskManagementMain, TTestCaseResult, TTestCaseStepResult
from .serializers import TTaskManagementMainSerializer, TTestCaseResultSerializer, TTestCaseStepResultSerializer
from .tasks import testcase_execute

from ..common.paginations import StandarPagination


# 执行任务
# 命令： celery -A YTWapi worker -l info -P gevent
def execute_task(request):
    eid = request.GET.get('eid')
    if eid is None:
        return
    task_id = testcase_execute.delay(eid)

    return HttpResponse(task_id)


# 任务管理
class TTaskManagementMainViewSet(viewsets.ModelViewSet):
    queryset = TTaskManagementMain.objects.all().order_by('-id')
    serializer_class = TTaskManagementMainSerializer

    pagination_class = StandarPagination  # 分页

    filter_backends = (rest_framework.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter,)
    filter_class = TTaskManagementMainFilter
    search_fields = ('execute_stamp', 'task_id', 'task_name', 'status')


# 测试用例结果
class TTestCaseResultViewSet(viewsets.ModelViewSet):
    queryset = TTestCaseResult.objects.all().order_by('id')
    serializer_class = TTestCaseResultSerializer

    pagination_class = StandarPagination  # 分页
    filter_backends = (rest_framework.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter,)
    filter_class = TTestCaseResultFilter
    search_fields = ('execute_stamp',)
    http_method_names = ['get', 'delete']

    @action(methods=['delete'], detail=False)
    def deletes(self, request, *args, **kwargs):
        execute_stamp = request.query_params.get('execute_stamp', None)
        delete = TTestCaseResult.objects.filter(execute_stamp=execute_stamp).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# 测试用例步骤结果
class TTestCaseStepResultViewSet(viewsets.ModelViewSet):
    queryset = TTestCaseStepResult.objects.all().order_by('id')
    serializer_class = TTestCaseStepResultSerializer

    filter_backends = (rest_framework.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter,)
    filter_class = TTestCaseStepResultFilter
    search_fields = ('execute_stamp', 'task_id')
    http_method_names = ['get', 'delete']

    @action(methods=['delete'], detail=False)
    def deletes(self, request, *args, **kwargs):
        execute_stamp = request.query_params.get('execute_stamp', None)
        delete = TTestCaseStepResult.objects.filter(execute_stamp=execute_stamp).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

