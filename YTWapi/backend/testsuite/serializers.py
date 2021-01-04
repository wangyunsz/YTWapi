# create by: wangyun
# create at: 2020/9/3 11:15
from rest_framework import serializers

from backend.testsuite.models import TTestSuiteMain, TTestSuiteTestCase, TExecuteConfig, TExecuteEnv


# 测试集主表
class TTestSuiteMainSerializer(serializers.ModelSerializer):
    class Meta:
        model = TTestSuiteMain
        fields = '__all__'


# 测试集用例表
class TTestSuiteTestCaseSerializer(serializers.ModelSerializer):
    title = serializers.ReadOnlyField(source='tc_id.title')

    class Meta:
        model = TTestSuiteTestCase
        read_only_fields = ('id', 'title')
        fields = ('id', 'tsid', 'tc_list', 'title')


# 测试执行设置表
class TExecuteConfigSerializer(serializers.ModelSerializer):
    suite_name = serializers.ReadOnlyField(source='tsid.suite_name')

    class Meta:
        model = TExecuteConfig
        read_only_fields = ('id', 'suite_name')
        fields = ('id', 'execute_name', 'tsid', 'suite_name', 'remark')


# 测试集环境表
class TExecuteEnvSerializer(serializers.ModelSerializer):
    env_name = serializers.ReadOnlyField(source='env_id.env_name')
    address = serializers.ReadOnlyField(source='env_id.address')

    class Meta:
        model = TExecuteEnv
        read_only_fields = ('id', 'env_name', 'address')
        fields = ('id', 'eid', 'env_id', 'env_name', 'address')

