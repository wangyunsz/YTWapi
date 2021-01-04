# create by: wangyun
# create at: 2020/5/9 11:48
import json
import re

""""
对请求响应处理功能优化
支持功能：
1. 读取报文中字段的值
    1.1 读取xml格式报文字段的值： 使用的是正则匹配的方式实现，根据字段标签读取值，可能存在多个值，则返回值为列表；
    1.2 读取json格式报文字段的值： 使用节点路径的方式实现，根据节点路径可能存在列表，值可能存在多个，按不同路径及值存为字典；
2. 更新字段值
    2.1 更新xml格式报文字段值： 支持按标签（即字段名）更新，同时支持指定位置更新（标记：${字段名}）；
        支持更新单个值，多个值，当存在多个匹配时，只支持更新第一个值或更新所有的值。
    2.2 更新json格式报文字段值： 仅支持按指定精确路径更新单个值。
"""


def xml_get_field_value(body, field, value_dict=None):
    """
    获取xml报文中的字段值，若存在多个则为列表
    :param body: 请求体或响应体
    :param field: 字段名
    :param value_dict: 字段值字典
    :return: value_dict： 值字典，field单个匹配，值为字符串；多个匹配 ，值为列表
    """
    # 忽略大小写
    pattern = re.compile('<' + field + '>(.*)</' + field + '>', re.I)
    result_list = pattern.findall(body)
    if not result_list:
        print('参数[%s]提取失败，无匹配值。' % field)
    elif len(result_list) == 1:
        value_dict[field] = result_list[0]
    else:
        value_dict[field] = result_list
    return value_dict


def xml_update_field_value(body, field, value_dict):
    """
    更新xml报文中的字段值，若同字段名称更新多个值，则传入字典中的值为列表或元组等序列
    :param body: 目标xml，请求体
    :param field: 字段名
    :param value_dict: 字段值，字符串或列表，元组类型
    :return:
    """
    value = value_dict
    # 正则匹配规则
    pattern = re.compile('<' + field + '>.*</' + field + '>', re.I)
    # 1. 值为字符串，更新参数值
    if isinstance(value, str):
        # 只替换第一个
        new_value = '<' + field + '>' + value + '</' + field + '>'
        body = re.sub(pattern, new_value, body, count=1)
        return body
    # 2. 值为列表或元组等序列
    # 匹配搜索所有满足项
    findall = pattern.findall(body)
    if len(findall) != len(value):
        print('传入的参数[%s]，值长度与实际长度[%s]不匹配。' % (value, len(findall)))
        return None
    for n, o in zip(value, findall):
        old_value = o
        new_value = '<' + field + '>' + n + '</' + field + '>'
        body = body.replace(old_value, new_value, 1)

    return body


def json_get_field_value(data_dict, field, value_dict=None):
    """
    获取节点所有记录
    :param data_dict: json请求体或响应体，字典格式
    :param field: 节点路径
    :param value_dict: 值字典
    :return: value_dict: 当field路径未完全指定时，返回2重嵌套字典
    """
    if value_dict is None:
        value_dict = dict()

    node = field
    # 字典初始化，该字典用于存放细分节点（下一个节点遍历前一个节点并组合）
    # 示例：{
    #       'a': ['a'],
    #       'b': ['a.b[0]'],
    #       'c': ['a.b[0].c[0]', 'a.b[0].c[1]',
    #                       'a.b[0].c[2]', 'a.b[0].c[3]',
    #                       'a.b[0].c[4]'],
    #       'd': []
    #       }
    node_key = dict(zip(node, [[] for x in node]))
    # 字典初始化，该字典用于存放各节点数据，和上面类似
    node_key_data = dict(zip(node, [[] for x in node]))
    try:
        # 第一重循环，按节点路径遍历
        for n in range(len(node)):
            # 获取前一节点的节点路径组合，以及节点值组合
            if n == 0:
                if node[0] not in data_dict:
                    break
                # 存放至字典对应的节点中
                node_key[node[0]].append(node[n])
                node_key_data[node[0]].append(data_dict[node[0]])
                continue
            # 前一个节点的数据、以及组合个数
            back_data = node_key_data[node[n-1]]
            back_no = len(node_key[node[n-1]])
            # 第二重循环，根据前一个节点的组合数量，遍历每一个节点路径
            for v in range(back_no):
                # 若当前节点，在对应的节点路径数据中不存在
                # 有可能是指定列表索引位置的方式，包含[]
                if node[n] not in back_data[v]:
                    if '[' in node[n] and ']' in node[n]:
                        node_key[node[n]].append(node_key[node[n - 1]][v] + '.' + node[n])
                        this_node, this_node_index_str = node[n].split('[')
                        try:
                            this_node_index = int(this_node_index_str.split(']')[0])
                        except:
                            print('参数节点[%s]索引值不存在。' % node[n])
                            this_node_index = None
                        node_key_data[node[n]].append(back_data[v][this_node][this_node_index])
                        continue
                    else:
                        continue

                # 当前路径，当前节点的数据
                cur_node_data = back_data[v][node[n]]
                # 判断如果是字典，说明不用细分，直接获取对应的节点名称以及节点数据值即可
                if isinstance(cur_node_data, dict):
                    node_key[node[n]].append(node_key[node[n - 1]][v] + '.' + node[n])
                    node_key_data[node[n]].append(cur_node_data)
                    continue

                # 如果非字典，则可能为列表，或达到最后一层节点的数据了
                # 处理最后一层节点
                if n == len(node) - 1:
                    node_key[node[n]].append(node_key[node[n - 1]][v] + '.' + node[n])
                    node_key_data[node[n]].append(cur_node_data)
                    continue

                # 前面的情况都不是，那么只剩下最后一种，该节点对应数据为列表形式了
                # 获取列表长度
                cur_node_len = len(cur_node_data)
                # 第三重循环，根据列表数量，分别需要组合前面的节点路径，再获取对应的节点名以及节点数据
                for vn in range(cur_node_len):
                    node_key[node[n]].append(node_key[node[n - 1]][v] + '.' + node[n] + '[' + str(vn) + ']')
                    node_key_data[node[n]].append(cur_node_data[vn])
        # print(node_key)
        # print(node_key_data)
    except:
        pass
    # 判断如果节点没有嵌套列表这种，就不用多层返回了
    if node_key[node[-1]]:
        # 内层key和外层key相等
        if '.'.join(field) == node_key[node[-1]][0]:
            value_dict['.'.join(field)] = node_key_data[node[-1]][0]
        # 嵌套2层字典的场景
        else:
            value_dict['.'.join(field)] = dict(zip(node_key[node[-1]], node_key_data[node[-1]]))
    else:
        value_dict['.'.join(field)] = None

    return value_dict


def is_exist_node(node, json_str, i=0):
    """
    判断节点路径是否存在
    :param node: 字段节点路径， 列表类型
    :param json_str: json报文
    :param i: 计数标志
    :return: True or False
    """
    # 当前节点索引（负向）
    node_index = -len(node) + i
    if node[node_index] not in json_str:
        # 如果包含[n]形式，说明节点为列表，需处理
        if '[' in node[node_index] and ']' in node[node_index]:
            list_node, list_index = node[node_index].split('[')
            index = list_index.split(']')[0]
            if index is None or index == '':
                print('ERROR: [%s]参数传入错误，请指定列表[%s]索引.' % (node, list_node))
                return False
            else:
                index = int(index)
            return is_exist_node(node, json_str[list_node][index], i + 1)
        else:
            print('[%s]字段节点[%s]不存在.' % (node, node[node_index]))
            return False
    # 判断如果当前节点为最后一个节点，则返回True
    if node_index == -1:
        return True

    return is_exist_node(node, json_str[node[node_index]], i + 1)


# 递归调用，更新json中的字段值
def update_json_step(node, json_str, value, i=0):
    # 当前节点索引（负向）
    node_index = -len(node) + i
    if node[node_index] not in json_str:
        # 如果包含[n]形式，说明节点为列表，需处理
        if '[' in node[node_index] and ']' in node[node_index]:
            list_node, list_index = node[node_index].split('[')
            index = list_index.split(']')[0]
            if index is None or index == '':
                print('ERROR: 参数传入错误，请指定列表[%s]索引.' % list_node)
            else:
                index = int(index)
            return update_json_step(node, json_str[list_node][index], value, i + 1)

    # 判断如果当前节点为最后一个节点，则更新value值
    if node_index == -1:
        json_str[node[-1]] = value
        return json_str

    return update_json_step(node, json_str[node[node_index]], value, i + 1)


class ReqResHandle:

    def __init__(self, data_type, data_msg, fields, value_dict=None):
        """
        处理请求体或响应体数据，读取或更新字段值
        :param data_type:  数据类型：xml，json
        :param data_msg: 请求体或响应体
        :param fields: 字段值，支持多字读方式，字段间逗号隔开；或传入列表、元组
                        json格式：节点路径，支持指定列表索引位置的方式（如：a.b[1].c[2].d），也支持按节点提取所有（如：a.b.c.d）
        :param value_dict: 以字典键值对保存字段值(注：当单个字段对应多个值时，xml以列表方式返回，json则返回多重嵌套字典)
        """
        self.data_type = data_type
        self.data = data_msg
        # fields支持str，list方式，str自动转换为list
        if isinstance(fields, str):
            self.fields = fields
            self.fields_list = []
            if ',' in fields:
                self.fields_list = fields.strip().split(',')
            else:
                self.fields_list.append(fields.strip())
        elif isinstance(fields, list):
            self.fields_list = fields
        else:
            self.fields_list = list(fields)
        # 初始化字典值
        if value_dict is None:
            self.value_dict = dict()
        else:
            self.value_dict = value_dict

    def get_fields_value(self):
        """
        获取字段值
        1. 支持获取多个字段值，输入字符串或列表， 元组
        """
        step_dict = self.value_dict
        # 字段列表循环获取
        for p in self.fields_list:
            if p == '':
                continue
            # 处理xml格式报文
            if self.data_type.upper() == 'XML':
                step_dict = xml_get_field_value(self.data, p, step_dict)
            # 处理json格式报文
            elif self.data_type.upper() == 'JSON':
                # 获取层级(使用.隔开)
                node = p.split('.')
                # json转换字典
                if isinstance(self.data, dict):
                    temp = self.data
                else:
                    temp = json.loads(self.data)

                step_dict = json_get_field_value(temp, node, step_dict)
            # 非 xml，json的数据格式，报错退出
            else:
                print('ERROR: 不支持此数据类型[%s]' % self.data_type)
                break
        return step_dict

    def update_fields_value(self):
        """
        更新字段值
        支持更新单个字段值，多个字段值（字段名 字符串或列表、元组，字段值 字典）
        """
        req_body = self.data
        # 字段列表循环更新
        for p in self.fields_list:
            # 入参类型判断
            if isinstance(self.value_dict, dict):
                # 参数在字典中不存在，则跳过
                if p not in self.value_dict.keys():
                    print('ERROR： 字典中不存在参数[%s]。' % p)
                    continue
                # 获取字典中参数的值
                value = self.value_dict[p]
            elif isinstance(self.value_dict, str):
                value = self.value_dict
            else:
                print('函数入参[%s]类型不支持，请传入字符串或字典。' % self.value_dict)
                break
            # 更新数据类型为 xml 的参数值
            if self.data_type.upper() == 'XML':
                req_body = xml_update_field_value(req_body, p, value)
            # 更新数据类型为 json 的参数值
            elif self.data_type.upper() == 'JSON':
                # json转换字典
                if not isinstance(req_body, dict):
                    req_body = json.loads(req_body)
                # 获取层级
                node = p.split('.')
                # 判断值是否为字典（因为提取字段值时，会有2重字典的场景，所以适配了这种情况）
                if isinstance(value, dict):
                    for k in value.keys():
                        k_node = k.split('.')
                        if not is_exist_node(k_node, req_body):
                            continue
                        update_json_step(k_node, req_body, value[k])
                else:
                    if not is_exist_node(node, req_body):
                        continue
                    # 调用递归函数更新字段值
                    update_json_step(node, req_body, value)

            # 非 xml，json的数据格式，报错退出
            else:
                print('ERROR: 不支持此数据类型[%s]' % self.data_type)
                break

        return req_body

