# create by: wangyun
# create at: 2020/9/16 15:19
from django.db import models


# 任务管理表
class TTaskManagementMain(models.Model):
    execute_stamp = models.CharField(max_length=255, blank=True, null=False, verbose_name='执行时间戳')
    task_id = models.CharField(max_length=255, blank=True, null=True, verbose_name='任务ID')
    task_name = models.CharField(max_length=255, blank=True, null=False, verbose_name='任务名称')
    status = models.CharField(max_length=255, blank=True, null=False, verbose_name='任务状态')
    start_time = models.DateTimeField(blank=True, null=True, verbose_name='开始时间')
    end_time = models.DateTimeField(blank=True, null=True, verbose_name='结束时间')
    total_second = models.IntegerField(blank=True, null=True, verbose_name='总耗时（秒）')
    objects = models.Manager()

    class Meta:
        db_table = 'yt_005_task_management_main'


# 测试用例执行结果表
class TTestCaseResult(models.Model):
    execute_stamp = models.CharField(max_length=255, blank=True, null=False, verbose_name='执行时间戳')
    number = models.CharField(max_length=255, blank=True, null=False, verbose_name='测试用例编号')
    title = models.CharField(max_length=255, blank=True, null=False, verbose_name='测试用例标题')
    project = models.CharField(max_length=255, blank=True, null=False, verbose_name='归属项目')
    module = models.CharField(max_length=255, blank=True, null=False, verbose_name='归属模块')
    level = models.IntegerField(blank=True, null=True, verbose_name='优先级')
    result = models.CharField(max_length=255, blank=True, null=False, verbose_name='执行结果')
    remark = models.CharField(max_length=1000, blank=True, null=False, verbose_name='结果备注')
    create_time = models.DateTimeField(blank=True, null=True, verbose_name='生成时间')
    objects = models.Manager()

    class Meta:
        db_table = 'yt_005_testcase_result'


# 测试用例步骤执行结果表
class TTestCaseStepResult(models.Model):
    execute_stamp = models.CharField(max_length=255, blank=True, null=False, verbose_name='执行时间戳')
    number = models.CharField(max_length=255, blank=True, null=False, verbose_name='测试用例编号')
    name = models.CharField(max_length=255, blank=True, null=False, verbose_name='接口实例名称')
    code = models.CharField(max_length=255, blank=True, null=False, verbose_name='接口编号')
    request_type = models.CharField(max_length=255, blank=True, null=False, verbose_name='请求方式')
    address = models.CharField(max_length=2000, blank=True, null=False, verbose_name='请求地址')
    data_type = models.CharField(max_length=255, blank=True, null=False, verbose_name='数据格式')
    request_header = models.CharField(max_length=2000, blank=True, null=True, verbose_name='请求头')
    request_body = models.TextField(blank=True, null=True, verbose_name='请求体')
    response_header = models.CharField(max_length=2000, blank=True, null=True, verbose_name='响应头')
    response_body = models.TextField(blank=True, null=True, verbose_name='响应体')
    result = models.CharField(max_length=255, blank=True, null=False, verbose_name='执行结果')
    remark = models.CharField(max_length=1000, blank=True, null=False, verbose_name='结果备注')
    create_time = models.DateTimeField(blank=True, null=True, verbose_name='生成时间')
    objects = models.Manager()

    class Meta:
        db_table = 'yt_005_testcase_step_result'

