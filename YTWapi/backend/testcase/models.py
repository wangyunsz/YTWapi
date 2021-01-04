# create by: wangyun
# create at: 2020/8/26 10:50

from django.db import models
from backend.interface.models import TInterfaceCase


# 录制生成用例表
class TMakeCaseMain(models.Model):
    name = models.CharField(max_length=255, blank=True, null=False, verbose_name='名称')
    create_time = models.DateTimeField(blank=True, null=True, verbose_name='创建时间')
    objects = models.Manager()

    class Meta:
        db_table = 'yt_003_makecase_main'


# 录制用例接口列表
class TMakeCaseInterfaceList(models.Model):
    mc_id = models.ForeignKey(TMakeCaseMain, on_delete=models.CASCADE)
    step_no = models.IntegerField(blank=True, null=False, verbose_name='步骤顺序')
    req_addr = models.CharField(max_length=255, blank=True, null=False, verbose_name='请求地址')
    req_type = models.CharField(max_length=255, blank=True, null=False, verbose_name='请求方式')
    req_header = models.CharField(max_length=2000, blank=True, null=True, verbose_name='请求头')
    req_body = models.TextField(blank=True, null=True, verbose_name='请求体')
    res_header = models.CharField(max_length=2000, blank=True, null=True, verbose_name='响应头')
    res_body = models.TextField(blank=True, null=True, verbose_name='响应体')
    instance_id = models.IntegerField(blank=True, null=True, verbose_name='接口实例id')

    objects = models.Manager()

    class Meta:
        db_table = 'yt_003_makecase_interface_list'


# 测试用例主表
class TTestCaseMain(models.Model):
    # 是否启用枚举值
    class IsEnable(models.IntegerChoices):
        NO = 0
        YES = 1

    # 优先级
    class LevelOption(models.IntegerChoices):
        LEVEL_0 = 0
        LEVEL_1 = 1
        LEVEL_2 = 2
        LEVEL_3 = 3

    number = models.CharField(max_length=255, blank=True, null=False, verbose_name='测试用例编号')
    title = models.CharField(max_length=255, blank=True, null=False, verbose_name='测试用例标题')
    mid = models.IntegerField(blank=True, null=True, verbose_name='归属模块ID')
    bsid = models.IntegerField(blank=True, null=True, verbose_name='业务流程ID')
    level = models.IntegerField(blank=True, null=True, choices=LevelOption.choices, verbose_name='优先级')
    is_enable = models.IntegerField(blank=True, null=False, choices=IsEnable.choices, default=IsEnable.NO,
                                    verbose_name='是否启用')
    creator = models.CharField(max_length=255, blank=True, null=True, verbose_name='创建人')
    create_time = models.DateTimeField(blank=True, null=True, verbose_name='创建时间')
    update_time = models.DateTimeField(blank=True, null=True, verbose_name='更新时间')
    remark = models.CharField(max_length=1000, blank=True, null=True, verbose_name='备注')
    objects = models.Manager()

    class Meta:
        db_table = 'yt_003_testcase_main'


# 测试用例步骤表
class TTestCaseStep(models.Model):
    tc_id = models.ForeignKey(TTestCaseMain, on_delete=models.CASCADE)
    inc_id = models.ForeignKey(TInterfaceCase, on_delete=models.CASCADE)
    header = models.CharField(max_length=2000, blank=True, null=True, verbose_name='请求头')
    body = models.TextField(blank=True, null=True, verbose_name='请求体')
    step_no = models.IntegerField(blank=True, null=False, verbose_name='测试用例步骤')
    objects = models.Manager()

    class Meta:
        db_table = 'yt_003_testcase_step'


# 测试用例断言表
class TTestCaseAssert(models.Model):
    # 字段归属枚举
    class FieldOwner(models.TextChoices):
        HEADER = 'res_header'
        BODY = 'res_body'

    # 断言值匹配类型枚举值
    class AssertType(models.TextChoices):
        CONTAINS = 'contains'
        EQUAL = 'equals'

    sid = models.ForeignKey(TTestCaseStep, on_delete=models.CASCADE)
    field_owner = models.CharField(max_length=50, blank=True, null=False, choices=FieldOwner.choices,
                                   verbose_name='字段归属')
    field_name = models.CharField(max_length=255, blank=True, null=False, verbose_name='字段名')
    field_node = models.CharField(max_length=255, blank=True, null=False, verbose_name='字段节点路径')
    assert_type = models.CharField(max_length=10, blank=True, null=True, choices=AssertType.choices,
                                   verbose_name='断言类型')
    field_value = models.CharField(max_length=255, blank=True, null=False, verbose_name='字段值')
    objects = models.Manager()

    class Meta:
        db_table = 'yt_003_testcase_assert'

