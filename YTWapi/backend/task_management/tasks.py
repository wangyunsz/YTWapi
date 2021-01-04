# create by: wangyun
# create at: 2020/9/17 16:37
from __future__ import absolute_import, unicode_literals

from datetime import datetime

from celery import shared_task
from celery.task import Task
from backend.task_management.execute.execute_task import ExecuteTask
from backend.task_management.models import TTaskManagementMain
from backend.testsuite.models import TExecuteConfig


# 通过时间戳字段，将执行任务与测试用例结果关联
def save_stamp(eid, stamp):
    # 查询测试执行配置表，找到执行配置表ID
    test_execute_obj = TExecuteConfig.objects.filter(id=eid)
    execute_name = test_execute_obj[0].execute_name
    task_obj = TTaskManagementMain.objects.get(task_name=execute_name, status='未开始')
    if not task_obj:
        return None
    task_obj.execute_stamp = stamp
    task_obj.save()


class TaskAfter(Task):

    def on_success(self, retval, task_id, args, kwargs):
        task_obj = TTaskManagementMain.objects.get(task_id=task_id)
        task_obj.status = '成功'
        task_obj.end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        task_obj.save()
        return super(TaskAfter, self).on_success(retval, task_id, args, kwargs)

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        task_obj = TTaskManagementMain.objects.get(task_id=task_id)
        task_obj.status = '失败'
        task_obj.end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        task_obj.save()
        return super(TaskAfter, self).on_failure(exc, task_id, args, kwargs, einfo)


@shared_task(base=TaskAfter)
def testcase_execute(eid):
    time_stamp = ExecuteTask(eid).start_run()
    save_stamp(eid, time_stamp)





