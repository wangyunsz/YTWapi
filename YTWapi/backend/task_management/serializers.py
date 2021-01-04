# create by: wangyun
# create at: 2020/9/22 11:13
from rest_framework import serializers

from backend.task_management.models import TTaskManagementMain, TTestCaseResult, TTestCaseStepResult


# 任务表
class TTaskManagementMainSerializer(serializers.ModelSerializer):

    class Meta:
        model = TTaskManagementMain
        fields = '__all__'


# 测试用例结果
class TTestCaseResultSerializer(serializers.ModelSerializer):

    class Meta:
        model = TTestCaseResult
        fields = '__all__'


# 测试用例步骤结果
class TTestCaseStepResultSerializer(serializers.ModelSerializer):
    create_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")

    class Meta:
        model = TTestCaseStepResult
        fields = '__all__'

