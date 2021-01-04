# create by: wangyun
# create at: 2020/8/17 17:03
from django.conf.urls import url
from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

from backend.interface.views import TInterfaceMainViewSet, TInterfaceCaseViewSet, TInterfaceCaseFieldInitConfigViewSet, \
    TAssertSceneFieldAssertViewSet, TInterfaceCaseFieldPoolViewSet, TBusinessMainViewSet, TBusinessStepViewSet
from backend.project.views import TProjectViewSet, TEnvironmentViewSet, TProjectModuleViewSet
from backend.task_management.views import execute_task, TTaskManagementMainViewSet, TTestCaseResultViewSet, \
    TTestCaseStepResultViewSet
from backend.testcase.views import TTestCaseMainViewSet, TTestCaseStepViewSet, TTestCaseAssertViewSet, \
    TMakeCaseMainViewSet, TMakeCaseInterfaceListViewSet
from backend.testsuite.views import TTestSuiteMainViewSet, TTestSuiteTestCaseViewSet, TExecuteConfigViewSet, \
    TExecuteEnvViewSet

routers = routers.DefaultRouter()
# 项目管理
routers.register('projectconfig', TProjectViewSet)
routers.register('envconfig', TEnvironmentViewSet)
routers.register('module', TProjectModuleViewSet)
# 接口管理
routers.register('interfaceconfig', TInterfaceMainViewSet)
routers.register('instance', TInterfaceCaseViewSet)
routers.register('fieldinit', TInterfaceCaseFieldInitConfigViewSet)
routers.register('fieldpool', TInterfaceCaseFieldPoolViewSet)
routers.register('fieldassert', TAssertSceneFieldAssertViewSet)
routers.register('business', TBusinessMainViewSet)
routers.register('businessstep', TBusinessStepViewSet)
# 测试用例
routers.register('makecase', TMakeCaseMainViewSet)
routers.register('makecaseinterface', TMakeCaseInterfaceListViewSet)
routers.register('testcase', TTestCaseMainViewSet)
routers.register('testcasestep', TTestCaseStepViewSet)
routers.register('testcaseassert', TTestCaseAssertViewSet)
# 测试执行设置
routers.register('testsuite', TTestSuiteMainViewSet)
routers.register('testsuitetestcase', TTestSuiteTestCaseViewSet)
routers.register('executeconfig', TExecuteConfigViewSet)
routers.register('executeenv', TExecuteEnvViewSet)
# 任务管理
routers.register('task', TTaskManagementMainViewSet)
routers.register('testcaseresult', TTestCaseResultViewSet)
routers.register('testcasestepresult', TTestCaseStepResultViewSet)


urlpatterns = [
    path(r'', include(routers.urls)),

    # rest_framework_simplejwt自带的得到token
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # 刷新JWT
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # 验证token
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    # 执行任务
    path('executetask/', execute_task)
]
