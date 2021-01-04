# create by: wangyun
# create at: 2020/9/3 11:29
from django_filters import rest_framework
from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response

from backend.common.paginations import StandarPagination
from backend.testsuite.filter import TTestSuiteMainFilter, TTestSuiteTestCaseFilter, TExecuteConfigFilter, \
    TExecuteEnvFilter
from backend.testsuite.models import TTestSuiteMain, TTestSuiteTestCase, TExecuteConfig, TExecuteEnv
from backend.testsuite.serializers import TTestSuiteMainSerializer, TTestSuiteTestCaseSerializer, \
    TExecuteConfigSerializer, TExecuteEnvSerializer


# 测试集主表
class TTestSuiteMainViewSet(viewsets.ModelViewSet):
    queryset = TTestSuiteMain.objects.filter().order_by('id')
    serializer_class = TTestSuiteMainSerializer

    pagination_class = StandarPagination  # 分页
    filter_backends = (rest_framework.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter,)
    filter_class = TTestSuiteMainFilter
    search_fields = ('suite_name', )


# 测试集用例表
class TTestSuiteTestCaseViewSet(viewsets.ModelViewSet):
    queryset = TTestSuiteTestCase.objects.all()
    serializer_class = TTestSuiteTestCaseSerializer

    filter_backends = (rest_framework.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter,)
    filter_class = TTestSuiteTestCaseFilter
    search_fields = ('id', 'tsid')


# 测试执行配置表
class TExecuteConfigViewSet(viewsets.ModelViewSet):
    queryset = TExecuteConfig.objects.filter().order_by('id')
    serializer_class = TExecuteConfigSerializer

    pagination_class = StandarPagination  # 分页
    filter_backends = (rest_framework.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter,)
    filter_class = TExecuteConfigFilter
    search_fields = ('id', 'execute_name')


# 测试执行环境表
class TExecuteEnvViewSet(viewsets.ModelViewSet):
    queryset = TExecuteEnv.objects.all()
    serializer_class = TExecuteEnvSerializer

    # pagination_class = StandarPagination  # 分页
    filter_backends = (rest_framework.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter,)
    filter_class = TExecuteEnvFilter
    search_fields = ('id', 'eid')

    @action(methods=['delete'], detail=False)
    def deletes(self, request, *args, **kwargs):
        eid = request.query_params.get('eid', None)
        delete = TExecuteEnv.objects.filter(eid=eid).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

