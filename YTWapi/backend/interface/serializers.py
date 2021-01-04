# create by: wangyun
# create at: 2020/8/18 23:07
from rest_framework import serializers

from backend.interface.models import TInterfaceMain, TInterfaceCase, TInterfaceCaseFieldInitConfig, \
    TAssertSceneFieldAssert, TInterfaceCaseFieldPool, TBusinessMain, TBusinessStep


# 接口主表
class TInterfaceSerializer(serializers.ModelSerializer):
    project_code = serializers.ReadOnlyField(source='pid.project_code')
    project_name = serializers.ReadOnlyField(source='pid.project_name')
    describe = serializers.ReadOnlyField(source='pid.describe')
    module_name = serializers.ReadOnlyField(source='mid.module_name')

    # 日期时间格式化
    create_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    update_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")

    class Meta:
        model = TInterfaceMain
        read_only_fields = ('id', 'project_code', 'project_name', 'describe')
        fields = ('id', 'pid', 'project_code', 'project_name', 'describe', 'mid', 'module_name', 'interface_code', 'interface_name',
                  'interface_path', 'method', 'request_header', 'request_body', 'response_header', 'response_body',
                  'datatype', 'is_enable', 'creator', 'create_time', 'update_time', 'remark')


# 接口实例表
class TInterfaceCaseSerializer(serializers.ModelSerializer):
    interface_name = serializers.ReadOnlyField(source='intf_id.interface_name')
    interface_path = serializers.ReadOnlyField(source='intf_id.interface_path')

    class Meta:
        model = TInterfaceCase
        read_only_fields = ('id', 'interface_name', 'interface_path')
        fields = ('id', 'intf_id', 'interface_name', 'interface_path', 'case_name', 'case_description', 'is_selected', 'remark')


# 实例字段初始化配置表
class TInterfaceCaseFieldInitConfigSerializer(serializers.ModelSerializer):

    class Meta:
        model = TInterfaceCaseFieldInitConfig
        fields = '__all__'


# 实例字段初始化配置表
class TInterfaceCaseFieldPoolSerializer(serializers.ModelSerializer):

    class Meta:
        model = TInterfaceCaseFieldPool
        fields = '__all__'


# 实例字段断言表
class TAssertSceneFieldAssertSerializer(serializers.ModelSerializer):

    class Meta:
        model = TAssertSceneFieldAssert
        fields = '__all__'


# 业务流程
class TBusinessMainSerializer(serializers.ModelSerializer):

    class Meta:
        model = TBusinessMain
        fields = '__all__'


# 业务流程步骤
class TBusinessStepSerializer(serializers.ModelSerializer):

    class Meta:
        model = TBusinessStep
        read_only_fields = ('id', 'case_name')
        fields = ('id', 'bsid', 'inc_id', 'step_no')
