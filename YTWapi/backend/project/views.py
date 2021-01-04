# create by: wangyun
# create at: 2020/8/17 17:02
from django_filters import rest_framework
from rest_framework import viewsets, filters

from backend.common.paginations import StandarPagination
from backend.project.filter import TProjectModuleFilter, TProjectFilter, TEnvironmentFilter
from backend.project.models import TProject, TEnvironment, TProjectModule
from backend.project.serializers import TProjectSerializer, TEnvironmentSerializer, TProjectModuleSerializer
from rest_framework_simplejwt.authentication import JWTTokenUserAuthentication


# 项目列表
class TProjectViewSet(viewsets.ModelViewSet):
    # permission_classes = [permissions.IsAuthenticated]
    # authentication_classes = [JWTTokenUserAuthentication]
    queryset = TProject.objects.all().order_by('id')
    serializer_class = TProjectSerializer

    pagination_class = StandarPagination  # 分页

    filter_backends = (rest_framework.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter,)
    filter_class = TProjectFilter
    search_fields = ('project_code', 'project_name')


# 环境列表
class TEnvironmentViewSet(viewsets.ModelViewSet):
    queryset = TEnvironment.objects.all().order_by('id')
    serializer_class = TEnvironmentSerializer

    pagination_class = StandarPagination  # 分页

    filter_backends = (rest_framework.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter,)
    filter_class = TEnvironmentFilter
    search_fields = ('pid', 'project_code', 'project_name', 'env_name')


# 模块列表
class TProjectModuleViewSet(viewsets.ModelViewSet):
    queryset = TProjectModule.objects.all().order_by('id')
    serializer_class = TProjectModuleSerializer

    filter_backends = (rest_framework.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter,)
    filter_class = TProjectModuleFilter
    search_fields = ('=pid', 'module_name')
