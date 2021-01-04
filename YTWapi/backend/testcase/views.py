# create by: wangyun
# create at: 2020/8/26 10:51
from django_filters import rest_framework
from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response

from backend.common.paginations import StandarPagination
from backend.testcase.filter import TTestCaseMainFilter, TTestCaseStepFilter, TTestCaseAssertFilter, \
    TMakeCaseInterfaceListFilter
from backend.testcase.models import TTestCaseMain, TTestCaseStep, TTestCaseAssert, TMakeCaseMain, TMakeCaseInterfaceList
from backend.testcase.serializers import TTestCaseMainSerializer, TTestCaseStepSerializer, TTestCaseAssertSerializer, \
    TMakeCaseMainSerializer, TMakeCaseInterfaceListSerializer


# 录制用例文件列表
class TMakeCaseMainViewSet(viewsets.ModelViewSet):
    queryset = TMakeCaseMain.objects.filter().order_by('-id')
    serializer_class = TMakeCaseMainSerializer
    pagination_class = StandarPagination  # 分页


# 录制用例接口列表
class TMakeCaseInterfaceListViewSet(viewsets.ModelViewSet):
    queryset = TMakeCaseInterfaceList.objects.all().order_by('id')
    serializer_class = TMakeCaseInterfaceListSerializer

    filter_backends = (rest_framework.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter,)
    filter_class = TMakeCaseInterfaceListFilter
    search_fields = ('=mc_id',)

    @action(methods=['delete'], detail=False)
    def deletes(self, request, *args, **kwargs):
        mc_id = request.query_params.get('mc_id', None)
        delete = TTestCaseStep.objects.filter(mc_id=mc_id).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# 测试用例主表
class TTestCaseMainViewSet(viewsets.ModelViewSet):
    queryset = TTestCaseMain.objects.filter().order_by('id')
    serializer_class = TTestCaseMainSerializer

    filter_backends = (rest_framework.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter,)
    filter_class = TTestCaseMainFilter
    search_fields = ('=number', 'title', 'mid')


# 测试用例步骤表
class TTestCaseStepViewSet(viewsets.ModelViewSet):
    queryset = TTestCaseStep.objects.all().order_by('id')
    serializer_class = TTestCaseStepSerializer

    filter_backends = (rest_framework.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter,)
    filter_class = TTestCaseStepFilter
    search_fields = ('=tc_id', '=inc_id')

    @action(methods=['delete'], detail=False)
    def deletes(self, request, *args, **kwargs):
        inc_id = request.query_params.get('tc_id', None)
        delete = TTestCaseStep.objects.filter(inc_id=inc_id).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# 测试用例步骤断言
class TTestCaseAssertViewSet(viewsets.ModelViewSet):
    queryset = TTestCaseAssert.objects.all().order_by('id')
    serializer_class = TTestCaseAssertSerializer

    filter_backends = (rest_framework.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter,)
    filter_class = TTestCaseAssertFilter
    search_fields = ('=sid', 'field_owner')

    @action(methods=['delete'], detail=False)
    def deletes(self, request, *args, **kwargs):
        inc_id = request.query_params.get('sid', None)
        delete = TTestCaseAssert.objects.filter(inc_id=inc_id).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
