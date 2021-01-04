# create by: wangyun
# create at: 2020/9/14 19:35
import json
import time
from datetime import datetime

from backend.common.func_handle import func_suite
from backend.interface.models import TInterfaceCase, TInterfaceCaseFieldInitConfig, TAssertSceneFieldAssert, \
    TInterfaceMain, TInterfaceCaseFieldPool
from backend.project.models import TEnvironment, TProjectModule, TProject
from backend.task_management.execute.intf_request import RequestBase
from backend.task_management.execute.request_respond_handle import ReqResHandle
from backend.task_management.models import TTestCaseStepResult, TTestCaseResult
from backend.testcase.models import TTestCaseStep, TTestCaseAssert, TTestCaseMain
from backend.testsuite.models import TExecuteConfig, TExecuteEnv, TTestSuiteTestCase


# 增加测试步骤结果
def add_test_case_step_result(execute_stamp, number, name, code, request_type, address, data_type, request_header, request_body, response_header, response_body, result, remark, create_time=datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')):
    return TTestCaseStepResult.objects.create(execute_stamp=execute_stamp, number=number, name=name, code=code, request_type=request_type, address=address, data_type=data_type, request_header=request_header, request_body=request_body,  response_header=response_header, response_body=response_body, result=result, remark=remark, create_time=datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'))


# 增加测试用例结果
def add_test_case_result(execute_stamp, number, title, project, module, level, result, remark, create_time=datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')):
    return TTestCaseResult.objects.create(execute_stamp=execute_stamp, number=number, title=title, project=project, module=module, level=level, result=result, remark=remark,create_time=datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'))


# 解析函数配置信息，返回函数名称，参数值字典
# 传入value格式如： ${timestamp(stamp='%Y%m%d', days=1)}
def analysis_func_info(value):
    """
    解析函数配置信息，返回函数名称，参数值字典
    :param value:
    :return:
    """
    if '(' not in value:
        return None
    value_list = value[2:-2].split('(')
    func_name = value_list[0].strip()
    params_dict = {}
    if value_list[1] != '':
        # 去除引号，分割成列表: ${timestamp(stamp='%Y%m%d', days=1, set_time='000000')}
        p_list = value_list[1].replace('\'', '').replace('\"', '').split(',')
        for p in p_list:
            key, value = p.split('=')
            params_dict[key.strip()] = value.strip()

    return func_name, params_dict


# 执行测试用例类
class ExecuteTask:

    def __init__(self, eid):
        self.eid = eid  # 执行任务ID
        self.execute_stamp = datetime.now().strftime('%Y%m%d%H%M%S%f')

    def start_run(self):
        print('start.....after 10s...................')
        time.sleep(10000)
        eid = int(self.eid)
        # 第一步：根据ID，找到执行设置表中的测试集，查出执行环境及要执行的测试用例列表
        # 查询测试执行配置表，找到执行配置表ID
        test_execute_obj = TExecuteConfig.objects.filter(id=eid)
        if test_execute_obj is None:
            return self.execute_stamp
        # 执行设置表id
        test_execute_id = test_execute_obj[0].id
        # 测试集表id
        test_suite_id = test_execute_obj[0].tsid
        # 根据测试执行设置表id，查询执行环境
        env_list_obj = TExecuteEnv.objects.filter(eid=test_execute_id)
        print('env_list_obj:', env_list_obj)
        if env_list_obj is None:
            # return 'error，执行环境未设置！'
            return self.execute_stamp

        # 获取测试执行环境列表（存储环境id） env_id_list
        env_id_list = []
        for obj in env_list_obj:
            env_id_list.append(obj.env_id_id)
        print('env_id_list:', env_id_list)
        # 处理环境列表，转化为 项目id-->环境地址 字典  pid_address_dict
        pid_address_dict = {}
        for eid in env_id_list:
            # 项目环境表一条记录
            env_obj = TEnvironment.objects.filter(id=eid)
            # 项目id、环境地址
            pid = env_obj[0].pid_id
            address = env_obj[0].address
            # 添加到字典中
            pid_address_dict[pid] = address
        print('pid_address_dict:', pid_address_dict)

        # 获取测试集 测试用例id列表 test_case_id_list
        testcase_obj = TTestSuiteTestCase.objects.filter(tsid=test_suite_id)
        if testcase_obj is None:
            print('error，测试集未挑选测试用例！')
            return self.execute_stamp
        test_case_id_list = [int(i) for i in testcase_obj[0].tc_list.split(',')]
        print('test_case_id_list:', test_case_id_list)

        # 第二步：第一重循环（用例），循环遍历测试用例id
        for cid in test_case_id_list:

            # 测试用例信息： 测试用例归属项目、模块，测试用例编号
            test_case_main_obj = TTestCaseMain.objects.filter(id=cid)
            testcase_module_obj = TProjectModule.objects.filter(id=test_case_main_obj[0].mid)
            testcase_module = testcase_module_obj[0].module_name
            # print(testcase_module)
            testcase_project_obj = TProject.objects.filter(id=testcase_module_obj[0].pid_id)
            testcase_project = testcase_project_obj[0].project_name
            # print(testcase_project)
            testcase_number = test_case_main_obj[0].number
            # 判断测试用例是否启用（暂不处理）

            # 获取测试步骤列表对象，测试步骤按从前到后顺序排列
            test_step_obj = TTestCaseStep.objects.filter(tc_id=cid).order_by('step_no')
            print('test_step_obj', test_step_obj)
            if test_step_obj is None:
                # 'error，测试用例缺少步骤！'
                continue
            # print(test_step_obj)

            # 临时pool池，用于存放多接口关联的字段值
            field_pool_dict = {}
            # 测试用例执行结果、备注
            test_case_result = ''
            test_case_result_remark = ''

            # 第二重循环（步骤），遍历每一个测试步骤
            for step_obj in test_step_obj:
                # 测试步骤执行结果
                test_step_result = ''
                test_step_result_remark = ''

                # step1: 从测试步骤中获取
                # 获取测试步骤id step_id
                step_id = step_obj.id
                # A1: 获取测试步骤中请求头、请求体信息
                # 请求头格式str需要转换为字典
                step_request_head = json.loads(step_obj.header)
                step_request_body = step_obj.body
                # A2: 获取接口实例中关联的初始化字段配置信息、断言信息
                # 获取测试步骤对应的测试实例id step_instance_id
                step_instance_id = step_obj.inc_id_id
                # 获取接口实例对象
                instance_obj = TInterfaceCase.objects.filter(id=step_instance_id)
                # 获取接口实例表id、接口实例对应的接口id
                instance_id = instance_obj[0].id
                intf_id = instance_obj[0].intf_id_id
                # A2-1： 根据接口实例id，获取初始化字段配置对象
                instance_field_init_list_obj = TInterfaceCaseFieldInitConfig.objects.filter(inc_id=instance_id)
                # 根据初始化字段配置对象，生成字典:请求头字段初始字典、请求体字段初始字典
                instance_head_field_init_dict = {}
                instance_body_field_init_dict = {}
                for instance_field_init_obj in instance_field_init_list_obj:
                    field_owner = instance_field_init_obj.field_owner
                    field_node = instance_field_init_obj.field_node
                    field_value = instance_field_init_obj.field_value
                    if field_owner == 'header':
                        instance_head_field_init_dict[field_node] = field_value
                    else:
                        instance_body_field_init_dict[field_node] = field_value
                print('instance_head_field_init_dict', instance_head_field_init_dict)
                print('instance_body_field_init_dict', instance_body_field_init_dict)
                # A2-2： 根据接口实例id，获取Pool操作字段
                instance_field_pool_list_obj = TInterfaceCaseFieldPool.objects.filter(inc_id=instance_id)

                # 从pool中读取，写入pool中的请求头、请求体字段，生成字典
                instance_head_get_pool_dict = {}
                instance_body_get_pool_dict = {}
                instance_head_set_pool_dict = {}
                instance_body_set_pool_dict = {}
                for instance_field_pool_obj in instance_field_pool_list_obj:
                    pool_field_owner = instance_field_pool_obj.field_owner
                    pool_handle_type = instance_field_pool_obj.handle_type
                    # 从pool中读取，存储 pool字段名称--->读取后写入数据对应的字段节点路径
                    if pool_handle_type == 'get':
                        if pool_field_owner == 'header':
                            instance_head_get_pool_dict[instance_field_pool_obj.pool_field] = instance_field_pool_obj.field_node
                        else:
                            instance_body_get_pool_dict[instance_field_pool_obj.pool_field] = instance_field_pool_obj.field_node
                    # 写入pool，存储 字段名称 ---> 所读取数据对应字段的节点路径
                    else:
                        if pool_field_owner == 'header':
                            instance_head_set_pool_dict[instance_field_pool_obj.field_name] = instance_field_pool_obj.field_node
                        else:
                            instance_body_set_pool_dict[instance_field_pool_obj.field_name] = instance_field_pool_obj.field_node
                print('instance_head_get_pool_dict', instance_head_get_pool_dict)
                print('instance_body_get_pool_dict', instance_body_get_pool_dict)
                print('instance_head_set_pool_dict', instance_head_set_pool_dict)
                print('instance_body_set_pool_dict', instance_body_set_pool_dict)
                # A2-3: 根据接口实例id，获取字段断言对象
                print('----------A2-3------------')
                instance_field_assert_list_obj = TAssertSceneFieldAssert.objects.filter(inc_id=instance_id)
                print('instance_field_assert_list_obj', instance_field_assert_list_obj)

                # A3: 根据测试步骤id，获取测试步骤中配置的断言信息对象
                step_field_assert_list_obj = TTestCaseAssert.objects.filter(sid=step_id)

                # A4： 根据接口表id，根据对象即可找到：接口归属项目、接口地址、请求方式、数据格式
                interface_obj = TInterfaceMain.objects.filter(id=intf_id)
                data_type = interface_obj[0].datatype
                method = interface_obj[0].method

                # step2：请求参数初始化
                # 归属项目id
                pid = interface_obj[0].pid_id
                # 根据项目id，查出环境
                if pid not in pid_address_dict.keys():
                    test_case_result = '失败'
                    test_case_result_remark = 'error, 项目环境未设置!'
                    print(test_case_result_remark)
                    continue
                address = pid_address_dict[pid]

                # B1：拼接完整的接口请求地址：根据归属项目查询出测试执行环境，测试执行环境 + 接口地址组装完整地址
                request_url = address + interface_obj[0].interface_path
                print('request_url', request_url)
                # B2：请求头、请求体字段初始化：
                # 检查接口实例初始化字段配置表，根据配置的请求头、请求体字段或字段生成函数（先根据函数生成值），更新请求头、请求体
                # 对字段中value值是通过定义函数去生成的，需要先生成值（暂不处理）
                # 替换更新，请求头 初始化字段值
                if instance_head_field_init_dict is not None:
                    for field in instance_head_field_init_dict.keys():
                        head_param_value = instance_head_field_init_dict[field]
                        # 判断字段值是否配置按函数生成
                        # 传入格式如： ${timestamp(stamp='%Y%m%d', days=1)}
                        new_value_list = []
                        func_name, params_dict = None, {}
                        if '${' in head_param_value and ')}' in head_param_value:
                            new_value_list = analysis_func_info(head_param_value)
                            if new_value_list:
                                func_name = new_value_list[0]
                                params_dict = new_value_list[1]
                                print(params_dict)
                                # ！！！！！！！！！动态执行函数！！！！！！！！！！！！！
                                return_value = func_suite(func_name, **params_dict)
                                if return_value:
                                    head_param_value = return_value
                                else:
                                    test_step_result_remark += '获取[' + head_param_value + ']值为空；'
                        # 更新值
                        step_request_head = ReqResHandle(data_type, step_request_head, field, {
                            field: head_param_value}).update_fields_value()
                # 替换更新，请求体 初始化字段值
                if instance_body_field_init_dict is not None:
                    for field in instance_body_field_init_dict.keys():
                        body_param_value = instance_body_field_init_dict[field]
                        # 判断字段值是否配置按函数生成
                        # 传入格式如： ${timestamp(stamp='%Y%m%d', days=1)}
                        new_value_list = []
                        func_name, params_dict = None, {}
                        if '${' in body_param_value and ')}' in body_param_value:
                            new_value_list = analysis_func_info(body_param_value)
                            if new_value_list:
                                func_name = new_value_list[0]
                                params_dict = new_value_list[1]
                                # ！！！！！！！！！动态执行函数！！！！！！！！！！！！！
                                body_return_value = func_suite(func_name, **params_dict)
                                if body_return_value:
                                    body_param_value = body_return_value
                                else:
                                    test_step_result_remark += '获取[' + body_param_value + ']值为空；'
                        # 更新值
                        step_request_body = ReqResHandle(data_type, step_request_body, field, {
                            field: body_param_value}).update_fields_value()

                # B3: pool中获取字段值，更新请求头、请求体
                if instance_head_get_pool_dict is not None:
                    for field in instance_head_get_pool_dict.keys():
                        # 判断字段是否在临时pool中存有，没有则跳过
                        if field not in field_pool_dict.keys():
                            print('从pool中读取字段值失败，临时pool中不存在[' + field + ']字段！')
                            test_step_result_remark += '从pool中读取字段值失败，临时pool中不存在[' + field + ']字段！'
                            continue
                        field_value = field_pool_dict[field]
                        field_node_key = instance_head_get_pool_dict[field]
                        value_dict = {field_node_key: field_value}
                        step_request_head = ReqResHandle(data_type, step_request_head, field_node_key, value_dict).update_fields_value()
                if instance_body_get_pool_dict is not None:
                    for field in instance_body_get_pool_dict.keys():
                        # 判断字段是否在临时pool中存有，没有则跳过
                        if field not in field_pool_dict.keys():
                            print('从pool中读取字段值失败，临时pool中不存在[' + field + ']字段！')
                            test_step_result_remark += '从pool中读取字段值失败，临时pool中不存在[' + field + ']字段！'
                            continue
                        field_value = field_pool_dict[field]
                        field_node_key = instance_body_get_pool_dict[field]
                        value_dict = {field_node_key: field_value}
                        step_request_body = ReqResHandle(data_type, step_request_body, field_node_key, value_dict).update_fields_value()

                print(step_request_head)
                print(step_request_body)
                # step3: 发起请求、获取响应结果
                res = RequestBase(method, request_url, step_request_body, step_request_head, data_type).get_respond()
                res_head = res.headers
                if res.content:
                    res_body = res.text
                else:
                    res_body = ''

                # step4： 响应断言
                # C1：进行响应结果断言：初始化配置的断言、测试用例步骤配置的断言
                if res_body is None:
                    test_step_result = '失败'
                    test_step_result_remark += '响应结果为空'
                    # 写入数据库
                    add_test_case_step_result(execute_stamp=self.execute_stamp, number=testcase_number, name=instance_obj[0].case_name, code=interface_obj[0].interface_code, request_type=interface_obj[0].method, address=request_url, data_type=interface_obj[0].datatype, request_header=step_request_head, request_body=step_request_body, response_header=res_head, response_body=res_body, result=test_step_result, remark=test_step_result_remark)
                    # 更新用例结果
                    test_case_result = '失败'
                    continue
                # C1-1： 初始化配置的断言信息，进行断言
                # 遍历进行断言
                if instance_field_assert_list_obj is not None:
                    for instance_field_assert_obj in instance_field_assert_list_obj:
                        if instance_field_assert_obj.field_owner == 'res_header':
                            head_field_value_dict = ReqResHandle(data_type, res_head, instance_field_assert_obj.field_node).get_fields_value()
                            if head_field_value_dict is None:
                                test_step_result = '失败'
                                test_step_result_remark += '获取字段[' + instance_field_assert_obj.field_node + ']失败;'
                                continue
                            res_field_value = head_field_value_dict[instance_field_assert_obj.field_node]
                            if instance_field_assert_obj.assert_type == 'contains':
                                if instance_field_assert_obj.field_value not in res_field_value:
                                    test_step_result = '失败'
                                    test_step_result_remark += '断言[' + instance_field_assert_obj.field_node + '] ' + \
                                                              instance_field_assert_obj.assert_type + ' [' + instance_field_assert_obj.field_value + '], 实际[' + res_field_value + ']'
                            else:
                                if instance_field_assert_obj.field_value != res_field_value:
                                    test_step_result = '失败'
                                    test_step_result_remark += '断言[' + instance_field_assert_obj.field_node + '] ' + \
                                                              instance_field_assert_obj.assert_type + ' [' + instance_field_assert_obj.field_value + '], 实际[' + res_field_value + ']'
                        else:   # 响应体断言
                            head_field_value_dict = ReqResHandle(data_type, res_body,
                                                                instance_field_assert_obj.field_node).get_fields_value()
                            if head_field_value_dict is None:
                                test_step_result = '失败'
                                test_step_result_remark += '获取字段[' + instance_field_assert_obj.field_node + ']失败;'
                                continue
                            res_field_value = head_field_value_dict[instance_field_assert_obj.field_node]
                            if instance_field_assert_obj.assert_type == 'contains':
                                if instance_field_assert_obj.field_value not in res_field_value:
                                    test_step_result = '失败'
                                    test_step_result_remark += '断言[' + instance_field_assert_obj.field_node + '] ' + \
                                                              instance_field_assert_obj.assert_type + ' [' + instance_field_assert_obj.field_value + '], 实际[' + res_field_value + ']'
                            else:
                                if instance_field_assert_obj.field_value != res_field_value:
                                    test_step_result = '失败'
                                    test_step_result_remark += '断言[' + instance_field_assert_obj.field_node + '] ' + \
                                                              instance_field_assert_obj.assert_type + ' [' + instance_field_assert_obj.field_value + '], 实际[' + res_field_value + ']'
                # C1-2： 测试用例步骤中配置的断言
                if step_field_assert_list_obj is not None:
                    for step_field_assert_obj in step_field_assert_list_obj:
                        if step_field_assert_obj.field_owner == 'res_header':
                            body_field_value_dict = ReqResHandle(data_type, res_head,
                                                                step_field_assert_obj.field_node).get_fields_value()
                            if body_field_value_dict is None:
                                test_step_result = '失败'
                                test_step_result_remark += '获取字段[' + step_field_assert_obj.field_node + ']失败;'
                                continue
                            res_field_value = body_field_value_dict[step_field_assert_obj.field_node]
                            if step_field_assert_obj.assert_type == 'contains':
                                if step_field_assert_obj.field_value not in res_field_value:
                                    test_step_result = '失败'
                                    test_step_result_remark += '断言[' + step_field_assert_obj.field_node + '] ' + \
                                                              step_field_assert_obj.assert_type + ' [' + step_field_assert_obj.field_value + '], 实际[' + res_field_value + ']'
                            else:
                                if step_field_assert_obj.field_value != res_field_value:
                                    test_step_result = '失败'
                                    test_step_result_remark += '断言[' + step_field_assert_obj.field_node + '] ' + \
                                                              step_field_assert_obj.assert_type + ' [' + step_field_assert_obj.field_value + '], 实际[' + res_field_value + ']'
                        else:
                            body_field_value_dict = ReqResHandle(data_type, res_body,
                                                                step_field_assert_obj.field_node).get_fields_value()
                            if body_field_value_dict is None:
                                test_step_result = '失败'
                                test_step_result_remark += '获取字段[' + step_field_assert_obj.field_node + ']失败;'
                                continue
                            res_field_value = body_field_value_dict[step_field_assert_obj.field_node]
                            if step_field_assert_obj.assert_type == 'contains':
                                if step_field_assert_obj.field_value not in res_field_value:
                                    test_step_result = '失败'
                                    test_step_result_remark += '断言[' + step_field_assert_obj.field_node + '] ' + \
                                                              step_field_assert_obj.assert_type + ' [' + step_field_assert_obj.field_value + '], 实际[' + res_field_value + ']'
                            else:
                                if step_field_assert_obj.field_value != res_field_value:
                                    test_step_result = '失败'
                                    test_step_result_remark += '断言[' + step_field_assert_obj.field_node + '] ' + \
                                                              step_field_assert_obj.assert_type + ' [' + step_field_assert_obj.field_value + '], 实际[' + res_field_value + ']'

                # C2： 检查接口实例初始化配置Pool表，根据配置的字段，获取响应头、响应体中的字段保存保存到临时Pool
                if test_step_result == '失败':
                    test_step_result_remark = '断言失败！' + test_step_result_remark
                    # 写入数据库
                    add_test_case_step_result(execute_stamp=self.execute_stamp, number=testcase_number, name=instance_obj[0].case_name,
                                              code=interface_obj[0].interface_code,
                                              request_type=interface_obj[0].method, address=request_url,
                                              data_type=interface_obj[0].datatype, request_header=step_request_head,
                                              request_body=step_request_body, response_header=res_head,
                                              response_body=res_body, result=test_step_result,
                                              remark=test_step_result_remark)
                    # 更新用例结果
                    test_case_result = '失败'
                    continue
                # C2-1: 响应头字段
                if instance_head_set_pool_dict is not None:
                    for head_set_pool_key in instance_head_set_pool_dict:
                        # 读取值
                        res_head_set_pool_key_value_dict = ReqResHandle(data_type, res_head, instance_head_set_pool_dict[head_set_pool_key]).get_fields_value()
                        # 存至临时pool
                        field_pool_dict[head_set_pool_key] = res_head_set_pool_key_value_dict[instance_head_set_pool_dict[head_set_pool_key]]
                # C2-2: 响应体字段
                if instance_body_set_pool_dict is not None:
                    for body_set_pool_key in instance_body_set_pool_dict:
                        # 读取值
                        res_body_set_pool_key_value_dict = ReqResHandle(data_type, res_body,
                                                                        instance_body_set_pool_dict[
                                                                            body_set_pool_key]).get_fields_value()
                        # 存至临时pool
                        field_pool_dict[body_set_pool_key] = res_body_set_pool_key_value_dict[
                            instance_body_set_pool_dict[body_set_pool_key]]

                # step5: 测试步骤结果更新
                if test_step_result == '':
                    test_step_result = '成功'
                # 如果步骤执行失败，则测试用例结果为失败
                if test_step_result == '失败':
                    test_case_result = '失败'
                # 将测试步骤执行结果写入数据库
                add_test_case_step_result(execute_stamp=self.execute_stamp, number=testcase_number, name=instance_obj[0].case_name, code=interface_obj[0].interface_code, request_type=interface_obj[0].method, address=request_url, data_type=interface_obj[0].datatype, request_header=step_request_head, request_body=step_request_body, response_header=res_head, response_body=res_body, result=test_step_result, remark=test_step_result_remark)
                print('写入步骤结果成功')

            # 测试用例结果更新
            print('--------测试用例结果部分-------------', self.execute_stamp)
            if test_case_result == '':
                test_case_result = '成功'
            # 将测试用例执行结果写入数据库
            add_test_case_result(execute_stamp=self.execute_stamp, number=testcase_number, title=test_case_main_obj[0].title, project=testcase_project, module=testcase_module, level=test_case_main_obj[0].level, result=test_case_result, remark=test_case_result_remark, create_time=datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'))
            print('写入用例结果成功')
        return self.execute_stamp
