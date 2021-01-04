# create by: wangyun
# create at: 2020/8/17 17:00
from django.db import models


# 项目管理表
class TProject(models.Model):
    project_code = models.CharField(max_length=255, blank=True, null=False, verbose_name='项目英文名')
    project_name = models.CharField(max_length=255, blank=True, null=False, verbose_name='项目名称')
    describe = models.CharField(max_length=1000, blank=True, null=True, verbose_name='项目说明')
    objects = models.Manager()

    class Meta:
        db_table = 'yt_001_project'


# 是否启用枚举值
class IsEnable(models.IntegerChoices):
    NO = 0
    YES = 1


# 环境地址表
class TEnvironment(models.Model):
    # 协议枚举值
    class Protocol(models.TextChoices):
        HTTP = 'HTTP'
        HTTPS = 'HTTPS'

    pid = models.ForeignKey(TProject, on_delete=models.CASCADE)
    env_name = models.CharField(max_length=255, blank=True, null=False, verbose_name='环境名称')
    protocol = models.CharField(max_length=10, blank=True, null=False, choices=Protocol.choices, default=Protocol.HTTP, verbose_name='协议类型')
    address = models.CharField(max_length=255, blank=True, null=False, verbose_name='IP地址端口/域名')
    is_enable = models.IntegerField(blank=True, null=False, choices=IsEnable.choices, default=IsEnable.NO, verbose_name='是否启用')
    remark = models.CharField(max_length=1000, blank=True, null=True, verbose_name='备注')
    objects = models.Manager()

    class Meta:
        db_table = 'yt_001_project_environment'


# 模块表
class TProjectModule(models.Model):
    pid = models.ForeignKey(TProject, on_delete=models.CASCADE)
    module_name = models.CharField(max_length=255, blank=True, null=False, verbose_name='模块名称')
    objects = models.Manager()

    class Meta:
        db_table = 'yt_001_project_module'

