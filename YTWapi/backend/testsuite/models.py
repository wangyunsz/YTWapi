# create by: wangyun
# create at: 2020/9/3 11:05
from django.db import models

from backend.project.models import TEnvironment


# 测试集设置主表
class TTestSuiteMain(models.Model):
    suite_name = models.CharField(max_length=255, blank=True, null=False, verbose_name='测试集名称')
    remark = models.CharField(max_length=500, blank=True, null=True, verbose_name='说明')
    objects = models.Manager()

    class Meta:
        db_table = 'yt_004_testsuite_main'


# 测试集用例表
class TTestSuiteTestCase(models.Model):
    tsid = models.ForeignKey(TTestSuiteMain, on_delete=models.CASCADE)  # 测试集id
    tc_list = models.TextField(blank=True, null=True, verbose_name='测试用例ID列表')
    objects = models.Manager()

    class Meta:
        db_table = 'yt_004_testsuite_testcase'


# 测试执行配置表
class TExecuteConfig(models.Model):
    execute_name = models.CharField(max_length=255, blank=True, null=False, verbose_name='执行任务名称')
    tsid = models.ForeignKey(TTestSuiteMain, on_delete=models.CASCADE)
    remark = models.CharField(max_length=500, blank=True, null=True, verbose_name='说明')
    objects = models.Manager()

    class Meta:
        db_table = 'yt_004_testsuite_execute_config'


# 执行环境
class TExecuteEnv(models.Model):
    eid = models.ForeignKey(TExecuteConfig, on_delete=models.CASCADE)
    env_id = models.ForeignKey(TEnvironment, on_delete=models.CASCADE)
    objects = models.Manager()

    class Meta:
        db_table = 'yt_004_testsuite_execute_env'

