# create by: wangyun
# create at: 2020/8/18 23:06
from django_filters import rest_framework
from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response

from backend.common.paginations import StandarPagination
from backend.interface.filter import TInterfaceCaseFieldInitConfigFilter, TInterfaceCaseFieldPoolFilter, \
    TAssertSceneFieldAssertFilter, TBusinessMainFilter, TBusinessStepFilter, TInterfaceMainFilter, TInterfaceCaseFilter
from backend.interface.models import TInterfaceMain, TInterfaceCase, TInterfaceCaseFieldInitConfig, \
    TAssertSceneFieldAssert, TInterfaceCaseFieldPool, TBusinessMain, TBusinessStep
from backend.interface.serializers import TInterfaceSerializer, TInterfaceCaseSerializer, \
    TInterfaceCaseFieldInitConfigSerializer, TAssertSceneFieldAssertSerializer, TInterfaceCaseFieldPoolSerializer, \
    TBusinessMainSerializer, TBusinessStepSerializer


# 接口主表
class TInterfaceMainViewSet(viewsets.ModelViewSet):
    queryset = TInterfaceMain.objects.all()
    serializer_class = TInterfaceSerializer

    pagination_class = StandarPagination  # 分页
    filter_backends = (rest_framework.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter,)
    filter_class = TInterfaceMainFilter
    search_fields = ('=pid', 'interface_code', 'interface_name', 'interface_path', 'mid')


# 接口实例
class TInterfaceCaseViewSet(viewsets.ModelViewSet):
    queryset = TInterfaceCase.objects.all()
    serializer_class = TInterfaceCaseSerializer

    pagination_class = StandarPagination  # 分页
    filter_backends = (rest_framework.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter,)
    filter_class = TInterfaceCaseFilter
    search_fields = ('intf_id', 'case_name')


# 实例字段初始化配置表
class TInterfaceCaseFieldInitConfigViewSet(viewsets.ModelViewSet):
    queryset = TInterfaceCaseFieldInitConfig.objects.all()
    serializer_class = TInterfaceCaseFieldInitConfigSerializer

    filter_backends = (rest_framework.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter,)
    filter_class = TInterfaceCaseFieldInitConfigFilter
    search_fields = ('=inc_id', '=field_owner')

    @action(methods=['delete'], detail=False)
    def deletes(self, request, *args, **kwargs):
        inc_id = request.query_params.get('inc_id', None)
        delete = TInterfaceCaseFieldInitConfig.objects.filter(inc_id=inc_id).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# 实例字段初始化配置表 Pool
class TInterfaceCaseFieldPoolViewSet(viewsets.ModelViewSet):
    queryset = TInterfaceCaseFieldPool.objects.all()
    serializer_class = TInterfaceCaseFieldPoolSerializer

    filter_backends = (rest_framework.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter,)
    filter_class = TInterfaceCaseFieldPoolFilter
    search_fields = ('=inc_id', '=field_owner', '=handle_type')

    @action(methods=['delete'], detail=False)
    def deletes(self, request, *args, **kwargs):
        inc_id = request.query_params.get('inc_id', None)
        delete = TInterfaceCaseFieldPool.objects.filter(inc_id=inc_id).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# 实例字段断言表
class TAssertSceneFieldAssertViewSet(viewsets.ModelViewSet):
    queryset = TAssertSceneFieldAssert.objects.all()
    serializer_class = TAssertSceneFieldAssertSerializer

    filter_backends = (rest_framework.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter,)
    filter_class = TAssertSceneFieldAssertFilter
    search_fields = ('=inc_id', '=field_owner')

    @action(methods=['delete'], detail=False)
    def deletes(self, request, *args, **kwargs):
        inc_id = request.query_params.get('inc_id', None)
        delete = TAssertSceneFieldAssert.objects.filter(inc_id=inc_id).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# 业务流程
class TBusinessMainViewSet(viewsets.ModelViewSet):
    queryset = TBusinessMain.objects.all()
    serializer_class = TBusinessMainSerializer

    filter_backends = (rest_framework.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter,)
    filter_class = TBusinessMainFilter
    search_fields = ('busi_name', )


# 业务流程步骤
class TBusinessStepViewSet(viewsets.ModelViewSet):
    queryset = TBusinessStep.objects.all().order_by('step_no')
    serializer_class = TBusinessStepSerializer

    filter_backends = (rest_framework.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter,)
    filter_class = TBusinessStepFilter
    search_fields = ('=bsid', '=inc_id', '=step_no')

