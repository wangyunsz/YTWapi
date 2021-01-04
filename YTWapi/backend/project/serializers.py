# create by: wangyun
# create at: 2020/8/14 22:51
from rest_framework import serializers
from backend.project.models import TProject, TEnvironment, TProjectModule


# 项目配置
class TProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = TProject
        fields = '__all__'


# 环境配置
class TEnvironmentSerializer(serializers.ModelSerializer):
    project_code = serializers.ReadOnlyField(source='pid.project_code')
    project_name = serializers.ReadOnlyField(source='pid.project_name')
    describe = serializers.ReadOnlyField(source='pid.describe')

    class Meta:
        model = TEnvironment
        read_only_fields = ('id', 'project_code', 'project_name', 'describe')
        fields = ('id', 'pid', 'project_code', 'project_name', 'describe', 'env_name', 'protocol', 'address', 'is_enable', 'remark')


# 模块配置
class TProjectModuleSerializer(serializers.ModelSerializer):
    project_code = serializers.ReadOnlyField(source='pid.project_code')
    project_name = serializers.ReadOnlyField(source='pid.project_name')

    class Meta:
        model = TProjectModule
        read_only_fields = ('id', 'project_code', 'project_name')
        fields = ('id', 'pid', 'project_code', 'project_name', 'module_name')

