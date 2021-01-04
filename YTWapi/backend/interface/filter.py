# create by: wangyun
# create at: 2020/8/21 11:48
import django_filters

from backend.interface.models import TInterfaceCaseFieldInitConfig, TInterfaceCaseFieldPool, TAssertSceneFieldAssert, \
    TBusinessMain, TBusinessStep, TInterfaceMain, TInterfaceCase


# 接口主表
class TInterfaceMainFilter(django_filters.rest_framework.FilterSet):
    pid = django_filters.NumberFilter(field_name='pid')
    interface_code = django_filters.CharFilter(field_name='interface_code', lookup_expr='icontains')
    interface_name = django_filters.CharFilter(field_name='interface_name', lookup_expr='icontains')
    interface_path = django_filters.CharFilter(field_name='interface_path', lookup_expr='icontains')
    mid = django_filters.NumberFilter(field_name='mid')

    class Meta:
        model = TInterfaceMain
        fields = ('pid', 'mid', 'interface_code', 'interface_name', 'interface_path')


# 接口实例表
class TInterfaceCaseFilter(django_filters.rest_framework.FilterSet):
    intf_id = django_filters.NumberFilter(field_name='intf_id')
    case_name = django_filters.CharFilter(field_name='case_name', lookup_expr='icontains')

    class Meta:
        model = TInterfaceCase
        fields = ('intf_id', 'case_name')


# 实例字段初始化配置表
class TInterfaceCaseFieldInitConfigFilter(django_filters.rest_framework.FilterSet):
    inc_id = django_filters.NumberFilter(field_name='inc_id')
    field_owner = django_filters.CharFilter(field_name='field_owner')
    field_name = django_filters.CharFilter(field_name='field_name')
    field_node = django_filters.CharFilter(field_name='field_node')
    field_value = django_filters.CharFilter(field_name='field_value')

    class Meta:
        model = TInterfaceCaseFieldInitConfig
        fields = ('inc_id', 'field_owner', 'field_name', 'field_node', 'field_value')


# 实例字段初始化配置表 Pool
class TInterfaceCaseFieldPoolFilter(django_filters.rest_framework.FilterSet):
    inc_id = django_filters.NumberFilter(field_name='inc_id')
    field_owner = django_filters.CharFilter(field_name='field_owner')
    handle_type = django_filters.CharFilter(field_name='handle_type')
    field_name = django_filters.CharFilter(field_name='field_name')
    field_node = django_filters.CharFilter(field_name='field_node')
    pool_field = django_filters.CharFilter(field_name='pool_field')

    class Meta:
        model = TInterfaceCaseFieldPool
        fields = ('inc_id', 'field_owner', 'handle_type', 'field_name', 'field_node', 'pool_field')


# 实例字段初始化配置表 assert
class TAssertSceneFieldAssertFilter(django_filters.rest_framework.FilterSet):
    inc_id = django_filters.NumberFilter(field_name='inc_id')
    field_owner = django_filters.CharFilter(field_name='field_owner')
    field_name = django_filters.CharFilter(field_name='field_name')
    field_node = django_filters.CharFilter(field_name='field_node')
    assert_type = django_filters.CharFilter(field_name='assert_type')
    field_value = django_filters.CharFilter(field_name='field_value')

    class Meta:
        model = TAssertSceneFieldAssert
        fields = ('inc_id', 'field_owner', 'field_name', 'field_node', 'assert_type', 'field_value')


# 业务流程
class TBusinessMainFilter(django_filters.rest_framework.FilterSet):
    busi_name = django_filters.CharFilter(field_name='busi_name', lookup_expr='icontains')

    class Meta:
        model = TBusinessMain
        fields = ('busi_name',)


# 业务流程步骤
class TBusinessStepFilter(django_filters.rest_framework.FilterSet):
    bsid = django_filters.NumberFilter(field_name='bsid')
    inc_id = django_filters.NumberFilter(field_name='inc_id')
    step_no = django_filters.NumberFilter(field_name='step_no')

    class Meta:
        model = TBusinessStep
        fields = ('bsid', 'inc_id', 'step_no')

