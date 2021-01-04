# create by: wangyun
# create at: 2020/8/26 10:50
from rest_framework import serializers

from backend.testcase.models import TTestCaseMain, TTestCaseStep, TTestCaseAssert, TMakeCaseMain, TMakeCaseInterfaceList


# 录制用例文件列表
class TMakeCaseMainSerializer(serializers.ModelSerializer):
    create_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")

    class Meta:
        model = TMakeCaseMain
        fields = '__all__'


# 录制用例接口列表
class TMakeCaseInterfaceListSerializer(serializers.ModelSerializer):

    class Meta:
        model = TMakeCaseInterfaceList
        fields = '__all__'


# 测试用例主表
class TTestCaseMainSerializer(serializers.ModelSerializer):
    pid = serializers.ReadOnlyField(source='mid.pid')   # 项目id
    project_name = serializers.ReadOnlyField(source='pid.project_name')
    module_name = serializers.ReadOnlyField(source='mid.module_name')   # 模块名称
    # 日期时间格式化
    create_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    update_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")

    class Meta:
        model = TTestCaseMain
        read_only_fields = ('id', 'pid', 'project_name')
        fields = ('id', 'number', 'title', 'pid', 'project_name', 'mid', 'module_name', 'bsid', 'level', 'is_enable', 'creator', 'create_time', 'update_time', 'remark')


# 测试用例步骤
class TTestCaseStepSerializer(serializers.ModelSerializer):
    case_name = serializers.ReadOnlyField(source='inc_id.case_name')

    class Meta:
        model = TTestCaseStep
        read_only_fields = ('id', 'case_name')
        fields = ('id', 'tc_id', 'inc_id', 'case_name', 'header', 'body', 'step_no')


# 测试用例预期结果表
class TTestCaseAssertSerializer(serializers.ModelSerializer):

    class Meta:
        model = TTestCaseAssert
        fields = '__all__'



