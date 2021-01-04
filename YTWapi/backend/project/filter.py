# create by: wangyun
# create at: 2020/9/4 16:47
import django_filters

from backend.project.models import TProjectModule, TProject, TEnvironment


# 项目
class TProjectFilter(django_filters.rest_framework.FilterSet):
    project_code = django_filters.CharFilter(field_name='project_code', lookup_expr='icontains')
    project_name = django_filters.CharFilter(field_name='project_name', lookup_expr='icontains')

    class Meta:
        model = TProject
        fields = ('id', 'project_code', 'project_name', 'describe')


# 环境
class TEnvironmentFilter(django_filters.rest_framework.FilterSet):
    pid = django_filters.NumberFilter(field_name='pid')
    env_name = django_filters.CharFilter(field_name='env_name', lookup_expr='icontains')

    class Meta:
        model = TEnvironment
        fields = ('id', 'pid', 'env_name', 'protocol', 'address', 'is_enable', 'remark')


# 模块
class TProjectModuleFilter(django_filters.rest_framework.FilterSet):
    pid = django_filters.NumberFilter(field_name='pid')
    module_name = django_filters.CharFilter(field_name='module_name')

    class Meta:
        model = TProjectModule
        fields = ('id', 'pid', 'module_name')
