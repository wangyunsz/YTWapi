# create by: wangyun
# create at: 2020/8/18 23:04
from django.db import models

from backend.project.models import TProject, TProjectModule


# 是否启用枚举值
class IsEnable(models.IntegerChoices):
    NO = 0
    YES = 1


# 接口主表
class TInterfaceMain(models.Model):
    # 请求方式枚举值
    class Method(models.TextChoices):
        GET = 'GET'
        POST = 'POST'
        HEAD = 'HEAD'
        PUT = 'PUT'
        DELETE = 'DELETE'
        CONNECT = 'CONNECT'
        OPTIONS = 'OPTIONS'
        TRACE = 'TRACE'
        PATCH = 'PATCH'

    # 协议枚举值
    class DataType(models.TextChoices):
        XML = 'XML'
        JSON = 'JSON'
        FORM = 'FORM'

    pid = models.ForeignKey(TProject, null=True, on_delete=models.SET_NULL)
    mid = models.ForeignKey(TProjectModule, null=True, on_delete=models.SET_NULL)
    interface_code = models.CharField(max_length=255, blank=True, null=False, verbose_name='接口编号')
    interface_name = models.CharField(max_length=255, blank=True, null=False, verbose_name='接口名称')
    interface_path = models.CharField(max_length=255, blank=True, null=False, verbose_name='接口地址')
    method = models.CharField(max_length=10, blank=True, null=False, choices=Method.choices, verbose_name='请求方式')
    request_header = models.CharField(max_length=2000, blank=True, null=True, verbose_name='请求头样例')
    request_body = models.TextField(blank=True, null=True, verbose_name='请求体样例')
    response_header = models.CharField(max_length=2000, blank=True, null=True, verbose_name='响应头样例')
    response_body = models.TextField(blank=True, null=True, verbose_name='响应体样例')
    datatype = models.CharField(max_length=10, blank=True, null=False, choices=DataType.choices, verbose_name='数据格式')
    is_enable = models.IntegerField(blank=True, null=False, choices=IsEnable.choices, default=IsEnable.NO, verbose_name='是否启用')
    creator = models.CharField(max_length=255, blank=True, null=True, verbose_name='创建人')
    create_time = models.DateTimeField(blank=True, null=True, verbose_name='创建时间')
    update_time = models.DateTimeField(blank=True, null=True, verbose_name='更新时间')
    remark = models.CharField(max_length=1000, blank=True, null=True, verbose_name='备注')
    objects = models.Manager()

    class Meta:
        db_table = 'yt_002_interface_main'


# 接口实例表
class TInterfaceCase(models.Model):
    intf_id = models.ForeignKey(TInterfaceMain, on_delete=models.CASCADE)
    case_name = models.CharField(max_length=255, blank=True, null=False, verbose_name='实例名称')
    case_description = models.CharField(max_length=255, blank=True, null=True, verbose_name='实例说明')
    is_selected = models.IntegerField(blank=True, null=False, choices=IsEnable.choices, default=IsEnable.NO, verbose_name='是否默认')
    remark = models.CharField(max_length=1000, blank=True, null=True, verbose_name='备注')
    objects = models.Manager()

    class Meta:
        db_table = 'yt_002_interface_case'


# 实例字段初始化配置表(函数生成)
class TInterfaceCaseFieldInitConfig(models.Model):
    # 字段归属枚举
    class FieldOwner(models.TextChoices):
        HEADER = 'header'
        BODY = 'body'

    inc_id = models.ForeignKey(TInterfaceCase, on_delete=models.CASCADE)
    field_owner = models.CharField(max_length=50, blank=True, null=False, choices=FieldOwner.choices, verbose_name='字段归属')
    field_name = models.CharField(max_length=255, blank=True, null=False, verbose_name='字段名称')
    field_node = models.CharField(max_length=255, blank=True, null=False, verbose_name='字段节点路径')
    field_value = models.CharField(max_length=255, blank=True, null=True, verbose_name='字段值')

    objects = models.Manager()

    class Meta:
        db_table = 'yt_002_interface_case_field_init_config'


# 实例字段初始化配置(资源池获取）
class TInterfaceCaseFieldPool(models.Model):
    # 字段归属枚举
    class FieldOwner(models.TextChoices):
        HEADER = 'header'
        BODY = 'body'

    # 字段归属枚举
    class HandleType(models.TextChoices):
        GET = 'get'
        SET = 'set'

    inc_id = models.ForeignKey(TInterfaceCase, on_delete=models.CASCADE)
    field_owner = models.CharField(max_length=50, blank=True, null=False, choices=FieldOwner.choices, verbose_name='字段归属')
    handle_type = models.CharField(max_length=50, blank=True, null=False, choices=HandleType.choices, verbose_name='操作类型')
    field_name = models.CharField(max_length=255, blank=True, null=False, verbose_name='字段名称')
    field_node = models.CharField(max_length=255, blank=True, null=False, verbose_name='字段节点路径')
    pool_field = models.CharField(max_length=255, blank=True, null=True, verbose_name='Pool字段名称')

    objects = models.Manager()

    class Meta:
        db_table = 'yt_002_interface_case_field_pool'


# 实例字段断言表
class TAssertSceneFieldAssert(models.Model):
    # 字段归属枚举
    class FieldOwner(models.TextChoices):
        HEADER = 'res_header'
        BODY = 'res_body'

    # 断言值匹配类型枚举值
    class AssertType(models.TextChoices):
        CONTAINS = 'contains'
        EQUAL = 'equals'

    inc_id = models.ForeignKey(TInterfaceCase, on_delete=models.CASCADE)
    field_owner = models.CharField(max_length=50, blank=True, null=False, choices=FieldOwner.choices,
                                   verbose_name='字段归属')
    field_name = models.CharField(max_length=255, blank=True, null=False, verbose_name='字段名')
    field_node = models.CharField(max_length=255, blank=True, null=False, verbose_name='字段节点路径')
    assert_type = models.CharField(max_length=10, blank=True, null=True, choices=AssertType.choices, verbose_name='断言类型')
    field_value = models.CharField(max_length=255, blank=True, null=False, verbose_name='字段值')
    objects = models.Manager()

    class Meta:
        db_table = 'yt_002_interface_case_field_assert'


# 业务流程主表
class TBusinessMain(models.Model):
    busi_name = models.CharField(max_length=255, blank=True, null=False, verbose_name='业务流程名称')
    objects = models.Manager()

    class Meta:
        db_table = 'yt_002_business_main'


# 业务流程步骤表
class TBusinessStep(models.Model):
    bsid = models.ForeignKey(TBusinessMain, on_delete=models.CASCADE)
    inc_id = models.ForeignKey(TInterfaceCase, on_delete=models.CASCADE)
    step_no = models.IntegerField(blank=True, null=False, verbose_name='业务流程步骤')
    objects = models.Manager()

    class Meta:
        db_table = 'yt_002_business_step'

