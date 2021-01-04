<template>
  <div>
    <!-- 面包屑 -->
    <el-breadcrumb separator-class="el-icon-arrow-right">
      <el-breadcrumb-item :to="{ path: '/home' }">首页</el-breadcrumb-item>
      <el-breadcrumb-item>测试管理</el-breadcrumb-item>
      <el-breadcrumb-item>测试用例</el-breadcrumb-item>
    </el-breadcrumb>

    <!-- 卡片区域 -->
    <el-row :gutter="24">
      <el-col :span="6">
        <el-card class="box-card">
          <el-input placeholder="测试用例标题" v-model="title" size="mini">
            <el-button slot="append" icon="el-icon-search" @click="queryTestCase" size="mini"></el-button>
          </el-input>
          <el-button type="text" @click="addTestCaseDialogClick">添加</el-button>
          <el-table :data="testCaseTableData" stripe size="small"
          @row-click="testCaseRowClick" :highlight-current-row="isHighlight">
            <el-table-column type="index" label="#"></el-table-column>
            <el-table-column prop="title" label="测试用例标题" show-overflow-tooltip></el-table-column>
            <el-table-column label="操作" fit="false" min-width="25px">
              <template slot-scope="scope">
                <el-button type="text" @click="deleteTestCaseDialog(scope.row)" size="mini">删除</el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-card>
      </el-col>
      <el-col :span="18">
        <el-card class="box-card">
          <el-collapse v-model="testCaseActiveNames" @change="testCaseHandleChange">
            <span><b>{{cur_row_testcase.title}}</b></span>
            <el-button type="success" style="float: right;" @click="saveAllTestCaseStep" size="mini" v-if="false">保存步骤</el-button>
            <el-button type="primary" style="float: right;" @click="addTestCaseStep" size="mini">添加步骤</el-button>
            <el-collapse-item title="测试用例基本信息" v-if="cur_row_testcase.id ? true : false" name="testcase">
              <el-card class="box-card">
                <el-form label-width="120px" :model="testCaseList"
                  :rules="testCaseListRules" ref="testCaseListRef" size="mini">
                  <el-row :gutter="24">
                    <el-col :span="10">
                      <el-form-item label="测试用例编号" prop="number">
                        <el-input v-model="testCaseList.number" placeholder="请输入" disabled></el-input>
                      </el-form-item>
                    </el-col>
                    <el-col :span="14">
                      <el-row :gutter="24">
                        <el-col :span="20">
                          <el-form-item label="测试用例标题" prop="title">
                            <el-input v-model="testCaseList.title" placeholder="请输入"></el-input>
                          </el-form-item>
                        </el-col>
                        <el-col :span="4">
                          <el-button type="success" @click="editTestCaseSave" size="mini">保存</el-button>
                        </el-col>
                      </el-row>
                    </el-col>
                  </el-row>
                 <el-form-item label="归属项目模块" prop="mid">
                    <el-cascader
                      v-model="edit_relate_id"
                      :options="moduleOptions"
                      :props="{ expandTrigger: 'hover' }"
                      @change="editModuleHandleChange"
                      clearable>
                    </el-cascader>
                  </el-form-item>
                  <el-row :gutter="24">
                    <el-col :span="10">
                      <el-form-item label="业务流程" prop="bsid">
                        <el-input v-model="testCaseList.bsid" placeholder="请输入"></el-input>
                      </el-form-item>
                    </el-col>
                    <el-col :span="14">
                      <el-form-item label="优先级" prop="level">
                        <el-select v-model="testCaseList.level" placeholder="请选择">
                            <el-option
                              v-for="item,index in level"
                              :key="index"
                              :value="item">
                            </el-option>
                          </el-select>
                      </el-form-item>
                    </el-col>
                  </el-row>
                  <el-row :gutter="24">
                    <el-col :span="10">
                      <el-form-item label="是否启用" prop="is_enable">
                        <el-switch
                          v-model="testCaseList.is_enable ? true : false"
                          active-color="#13ce66"
                          inactive-color="#ff4949"
                          @change="isEnableChange">
                        </el-switch>
                      </el-form-item>
                    </el-col>
                    <el-col :span="14">
                      <el-form-item label="创建人" prop="creator">
                        <el-input v-model="testCaseList.creator" placeholder="请输入"></el-input>
                      </el-form-item>
                    </el-col>
                  </el-row>
                  <el-row :gutter="24">
                    <el-col :span="10">
                      <el-form-item label="创建时间" prop="create_time">
                        <el-input v-model="testCaseList.create_time" placeholder="自动生成" disabled></el-input>
                      </el-form-item>
                    </el-col>
                    <el-col :span="14">
                      <el-form-item label="更新时间" prop="update_time">
                        <el-input v-model="testCaseList.update_time" placeholder="自动生成" disabled></el-input>
                      </el-form-item>
                    </el-col>
                  </el-row>
                  <el-form-item label="备注" prop="remark">
                    <el-input type="textarea" v-model="testCaseList.remark" placeholder="请输入"></el-input>
                  </el-form-item>
                </el-form>

              </el-card>
            </el-collapse-item>
          </el-collapse>
        </el-card>

        <el-collapse v-model="activeNames" @change="testCaseStepHandleChange" accordion>
          <el-card class="box-card" v-for="item,index in allTestCaseStepList" :key="index">
<!--            <el-button class="stepchange" icon="el-icon-top" size="mini" round></el-button>
            <el-button class="stepchange" icon="el-icon-bottom" size="mini" round></el-button> -->
            <el-button class="stepdel" type="danger" size="mini" @click="deleteTestCaseStep(item.id, item.index)">删除</el-button>
            <el-button class="stepdel" type="success" size="mini" @click="saveTestCaseStep(item.id, index)">保存</el-button>
            <el-collapse-item :title="'步骤 '+(index+1)+'： '+item.case_name" :name="index">
              <div>
               <!-- 测试用例步骤输入信息设置 -->
               <el-card class="box-card">
                 <el-form label-width="120px" :model="item" :rules="itemRule" ref="itemRef">
                    <el-form-item label="接口实例名称" prop="inc_id">
                      <el-select v-model="item.inc_id" filterable placeholder="请搜索并选择" size="mini">
                        <el-option
                          v-for="incItem in caseNameList"
                          :key="incItem.id"
                          :value="incItem.id"
                          :label="incItem.case_name">
                        </el-option>
                      </el-select>
                    </el-form-item>
                    <el-form-item label="请求头" prop="header">
                      <el-input type="textarea" v-model="item.header" placeholder="请输入" size="mini"></el-input>
                    </el-form-item>
                    <el-form-item label="请求体" prop="body">
                      <el-input type="textarea" v-model="item.body" placeholder="请输入" size="mini"></el-input>
                    </el-form-item>
                  </el-form>
               </el-card>

                <!-- 初始化字段配置显示 -->
                <p v-if="item.id && item.inc_id ? true : false">接口实例字段初始化配置、字段断言</p>
                <el-tabs type="border-card" v-if="item.id && item.inc_id ? true : false"
                v-model="testCaseFieldInitTab" @tab-click="testCaseFieldInitTabChange">
                  <el-tab-pane label="请求头" name="header">
                     <el-table :data="headerFieldInitList" border stripe size="mini">
                       <el-table-column type="index" label="#"></el-table-column>
                       <el-table-column prop="inc_id" label="接口实例ID" v-if="false"></el-table-column>
                       <el-table-column prop="field_owner" label="字段归属"></el-table-column>
                       <el-table-column prop="field_name" label="字段名称"></el-table-column>
                       <el-table-column prop="field_node" label="字段节点路径"></el-table-column>
                       <el-table-column prop="field_value" label="字段值"></el-table-column>
                     </el-table>
                   </el-tab-pane>
                  <el-tab-pane label="请求体" name="body">
                     <el-table :data="bodyFieldInitList" border stripe size="mini">
                       <el-table-column type="index" label="#"></el-table-column>
                       <el-table-column prop="inc_id" label="接口实例ID" v-if="false"></el-table-column>
                       <el-table-column prop="field_owner" label="字段归属"></el-table-column>
                       <el-table-column prop="field_name" label="字段名称"></el-table-column>
                       <el-table-column prop="field_node" label="字段节点路径"></el-table-column>
                       <el-table-column prop="field_value" label="字段值"></el-table-column>
                     </el-table>
                   </el-tab-pane>
                  <el-tab-pane label="从Pool读取" name="get">
                     <el-table :data="getFieldPoolList" border stripe size="mini">
                       <el-table-column type="index" label="#"></el-table-column>
                       <el-table-column prop="inc_id" label="接口实例ID" v-if="false"></el-table-column>
                       <el-table-column prop="field_owner" label="字段归属"></el-table-column>
                       <el-table-column prop="handle_type" label="操作类型"></el-table-column>
                       <el-table-column prop="field_name" label="字段名称"></el-table-column>
                       <el-table-column prop="field_node" label="字段节点路径"></el-table-column>
                       <el-table-column prop="pool_field" label="Pool字段名称"></el-table-column>
                     </el-table>
                   </el-tab-pane>
                  <el-tab-pane label="写入Pool中" name="set">
                     <el-table :data="setFieldPoolList" border stripe size="mini">
                       <el-table-column type="index" label="#"></el-table-column>
                       <el-table-column prop="inc_id" label="接口实例ID" v-if="false"></el-table-column>
                       <el-table-column prop="field_owner" label="字段归属"></el-table-column>
                       <el-table-column prop="handle_type" label="操作类型"></el-table-column>
                       <el-table-column prop="field_name" label="字段名称"></el-table-column>
                       <el-table-column prop="field_node" label="字段节点路径"></el-table-column>
                       <el-table-column prop="pool_field" label="Pool字段名称"></el-table-column>
                     </el-table>
                   </el-tab-pane>
                  <el-tab-pane label="字段断言" name="assert">
                     <el-table :data="fieldAssertList" border stripe size="mini">
                       <el-table-column type="index" label="#"></el-table-column>
                       <el-table-column prop="inc_id" label="接口实例ID" v-if="false"></el-table-column>
                       <el-table-column prop="field_owner" label="字段归属"></el-table-column>
                       <el-table-column prop="field_name" label="字段名"></el-table-column>
                       <el-table-column prop="field_node" label="字段节点路径"></el-table-column>
                       <el-table-column prop="assert_type" label="断言类型"></el-table-column>
                       <el-table-column prop="field_value" label="字段值"></el-table-column>
                     </el-table>
                   </el-tab-pane>
                </el-tabs>

                <!-- 测试用例步骤断言设置 -->
                <el-card class="box-card">
                  <template>
                    <el-button type="primary" @click="addTestCaseAssertDialogClick" size="mini">添加</el-button>
                    <el-table :data="testCaseAssertList" border stripe size="mini">
                      <el-table-column type="index" label="#"></el-table-column>
                      <el-table-column prop="sid" label="测试步骤ID" v-if="false"></el-table-column>
                      <el-table-column prop="field_owner" label="字段归属"></el-table-column>
                      <el-table-column prop="field_name" label="字段名"></el-table-column>
                      <el-table-column prop="field_node" label="字段节点路径"></el-table-column>
                      <el-table-column prop="assert_type" label="断言类型"></el-table-column>
                      <el-table-column prop="field_value" label="字段值"></el-table-column>
                      <el-table-column label="操作">
                        <template slot-scope="scope">
                          <el-tooltip effect="dark" content="修改" placement="top" :enterable="false">
                            <el-button type="primary" icon="el-icon-edit" size="mini" @click="editTestCaseAssertDialog(scope.row)"></el-button>
                          </el-tooltip>
                          <el-tooltip effect="dark" content="删除" placement="top" :enterable="false">
                            <el-button type="danger" icon="el-icon-delete" size="mini" @click="deleteTestCaseAssertDialog(scope.row)"></el-button>
                          </el-tooltip>
                        </template>
                      </el-table-column>
                    </el-table>
                  </template>
                </el-card>
              </div>
            </el-collapse-item>
          </el-card>
        </el-collapse>
      </el-col>
    </el-row>

    <!-- 测试用例 添加 -->
    <el-dialog
      title="添加测试用例"
      :visible.sync="addTestCaseDialogVisible"
      center
      @close="addTestCaseDialogClose">
      <el-form label-width="120px" :model="addTestCaseList"
        :rules="addTestCaseListRules" ref="addTestCaseListRef">
        <el-form-item label="测试用例编号" prop="number">
          <el-input v-model="addTestCaseList.number" placeholder="请输入"></el-input>
        </el-form-item>
        <el-form-item label="测试用例标题" prop="title">
          <el-input v-model="addTestCaseList.title" placeholder="请输入"></el-input>
        </el-form-item>
        <el-form-item label="归属项目模块" prop="mid">
          <el-cascader
            v-model="relate_id"
            :options="moduleOptions"
            :props="{ expandTrigger: 'hover' }"
            @change="moduleHandleChange"
            clearable>
          </el-cascader>
        </el-form-item>
        <el-form-item label="业务流程" prop="bsid">
          <el-input v-model="addTestCaseList.bsid" placeholder="请输入"></el-input>
        </el-form-item>
        <el-form-item label="优先级" prop="level">
          <el-select v-model="addTestCaseList.level" placeholder="请选择">
              <el-option
                v-for="item,index in level"
                :key="index"
                :value="item">
              </el-option>
            </el-select>
        </el-form-item>
        <el-form-item label="是否启用" prop="is_enable">
          <el-switch
            v-model="addTestCaseList.is_enable ? true : false"
            active-color="#13ce66"
            inactive-color="#ff4949"
            @change="addIsEnableChange">
          </el-switch>
        </el-form-item>
        <el-form-item label="创建人" prop="creator">
          <el-input v-model="addTestCaseList.creator" placeholder="请输入"></el-input>
        </el-form-item>
        <el-form-item label="创建时间" prop="create_time">
          <el-input v-model="addTestCaseList.create_time" placeholder="自动生成" disabled></el-input>
        </el-form-item>
        <el-form-item label="更新时间" prop="update_time">
          <el-input v-model="addTestCaseList.update_time" placeholder="自动生成" disabled></el-input>
        </el-form-item>
        <el-form-item label="备注" prop="remark">
          <el-input type="textarea" v-model="addTestCaseList.remark" placeholder="请输入"></el-input>
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button type="primary" @click="addTestCaseSave">确 定</el-button>
        <el-button @click="addTestCaseDialogVisible = false">取 消</el-button>
      </span>
    </el-dialog>

    <!-- 删除 -->
    <el-dialog
      title="提示"
      :visible.sync="deleteTestCaseDialogVisible"
      width="30%"
      @close="deleteTestCaseDialogClose"
      :close-on-click-modal="false">
      <span>请确认是否删除？</span>
      <span slot="footer" class="dialog-footer">
        <el-button @click="deleteTestCaseDialogVisible = false">取 消</el-button>
        <el-button type="primary" @click="deleteTestCase">确 定</el-button>
      </span>
    </el-dialog>

    <!-- 断言 -->
    <!-- 新增 字段断言 -->
    <el-dialog
      title="新增字段断言"
      :visible.sync="addTestCaseAssertDialogVisible"
      width="50%"
      center @close="addTestCaseAssertDialogClose"
      :close-on-click-modal="false">
      <el-form label-width="120px" :model="testCaseAssertForm"
        :rules="testCaseAssertFormRules" ref="testCaseAssertFormRef">
        <el-form-item label="测试步骤ID" prop="sid" v-if="false">
          <el-input v-model="testCaseAssertForm.sid"></el-input>
        </el-form-item>
        <el-form-item label="字段归属" prop="field_owner">
          <el-select v-model="testCaseAssertForm.field_owner" placeholder="请选择">
            <el-option
              v-for="item,index in feildAssert_field_owner"
              :key="index"
              :label="item.label"
              :value="item.value">
              <span style="float: left">{{ item.label }}</span>
              <span style="float: right; color: #8492a6; font-size: 13px">{{ item.value }}</span>
            </el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="字段名称" prop="field_name">
          <el-input v-model="testCaseAssertForm.field_name"></el-input>
        </el-form-item>
        <el-form-item label="字段节点路径" prop="field_node">
          <el-input v-model="testCaseAssertForm.field_node"></el-input>
        </el-form-item>
        <el-form-item label="断言类型" prop="assert_type">
          <el-select v-model="testCaseAssertForm.assert_type" placeholder="请选择">
            <el-option
              v-for="item,index in feildAssert_assert_type"
              :key="index"
              :label="item.label"
              :value="item.value">
              <span style="float: left">{{ item.label }}</span>
              <span style="float: right; color: #8492a6; font-size: 13px">{{ item.value }}</span>
            </el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="字段值" prop="field_value">
          <el-input v-model="testCaseAssertForm.field_value"></el-input>
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="addTestCaseAssertDialogVisible = false">取 消</el-button>
        <el-button type="primary" @click="saveTestCaseAssert">确 定</el-button>
      </span>
    </el-dialog>

    <!-- 修改 字段断言 -->
    <el-dialog
      title="修改字段断言"
      :visible.sync="editTestCaseAssertDialogVisible"
      width="50%"
      center @close="editTestCaseAssertDialogClose"
      :close-on-click-modal="false">
      <el-form label-width="120px" :model="testCaseAssertForm"
        :rules="testCaseAssertFormRules" ref="testCaseAssertFormRef">
        <el-form-item label="测试步骤ID" prop="sid" v-if="false">
          <el-input v-model="testCaseAssertForm.sid"></el-input>
        </el-form-item>
        <el-form-item label="字段归属" prop="field_owner">
          <el-select v-model="testCaseAssertForm.field_owner" placeholder="请选择">
            <el-option
              v-for="item,index in feildAssert_field_owner"
              :key="index"
              :label="item.label"
              :value="item.value">
              <span style="float: left">{{ item.label }}</span>
              <span style="float: right; color: #8492a6; font-size: 13px">{{ item.value }}</span>
            </el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="字段名称" prop="field_name">
          <el-input v-model="testCaseAssertForm.field_name"></el-input>
        </el-form-item>
        <el-form-item label="字段节点路径" prop="field_node">
          <el-input v-model="testCaseAssertForm.field_node"></el-input>
        </el-form-item>
        <el-form-item label="断言类型" prop="assert_type">
          <el-select v-model="testCaseAssertForm.assert_type" placeholder="请选择">
            <el-option
              v-for="item,index in feildAssert_assert_type"
              :key="index"
              :label="item.label"
              :value="item.value">
              <span style="float: left">{{ item.label }}</span>
              <span style="float: right; color: #8492a6; font-size: 13px">{{ item.value }}</span>
            </el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="字段值" prop="field_value">
          <el-input v-model="testCaseAssertForm.field_value"></el-input>
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="editTestCaseAssertDialogVisible = false">取 消</el-button>
        <el-button type="primary" @click="editTestCaseAssertSave">确 定</el-button>
      </span>
    </el-dialog>

    <!-- 删除 字段断言 -->
   <el-dialog
      title="提示"
      :visible.sync="deleteTestCaseAssertDialogVisible"
      width="30%"
      @close="deleteTestCaseAssertDialogClose"
      :close-on-click-modal="false">
      <span>请确认是否删除？</span>
      <span slot="footer" class="dialog-footer">
        <el-button @click="deleteTestCaseAssertDialogVisible = false">取 消</el-button>
        <el-button type="primary" @click="deleteTestCaseAssert">确 定</el-button>
      </span>
    </el-dialog>

  </div>
</template>

<script>
  export default {
    data(){
      return {
        baseUrl: this.$root.URL + '/testcase/',
        baseUrl_step: this.$root.URL + '/testcasestep/',
        baseUrl_assert: this.$root.URL + '/testcaseassert/',

        baseurl_fieldinit: this.$root.URL + '/fieldinit/',
        baseurl_fieldpool: this.$root.URL + '/fieldpool/',
        baseurl_fieldassert: this.$root.URL + '/fieldassert/',
        // 表格单击，高亮显示、并获取该行记录
        isHighlight: false,
        cur_row_testcase: {
          id: null,
          number: '',
          title: '',
          mid: null,
          bsid: null,
          level: null,
          is_enable: 1,
          creator: '',
          create_time: null,
          update_time: null,
          remark: ''
        },
        // 列表
        testCaseTableData: [],
        title: '',
        total: 0,
        // 新增
        addTestCaseDialogVisible: false,
        level: [0,1,2,3],
        addTestCaseList: {
          number: '',
          title: '',
          mid: null,
          bsid: null,
          level: null,
          is_enable: 1,
          creator: '',
          create_time: null,
          update_time: null,
          remark: ''
        },
        // 归属项目模块
        relate_id: null,
        moduleOptions: [],
        addTestCaseListRules: {
          number: [
            {
              required: true, message: '测试用例编号不能为空', trigger: 'blur'
            },
            {
              min: 1, max: 250, message: '1~250个字符', trigger: 'blur'
            }
          ],
          title: [
            {
              required: true, message: '测试用例标题不能为空', trigger: 'blur'
            },
            {
              min: 1, max: 250, message: '1~250个字符', trigger: 'blur'
            }
          ],
          mid: [
            {
              required: true, message: '归属项目模块不能为空', trigger: 'blur'
            },
          ],
          bsid: [
            {
              required: false,
            },
          ],
          level: [
            {
              required: true, message: '优先级不能为空', trigger: 'blur'
            },
          ],
        },

        // 修改
        testCaseActiveNames: '',
        editTestCaseUpdateCount: 0,
        testCaseList: {
          number: '',
          title: '',
          mid: null,
          bsid: null,
          level: null,
          is_enable: 1,
          creator: '',
          create_time: null,
          update_time: null,
          remark: ''
        },
        // 归属项目模块
        edit_relate_id: [],

        testCaseListRules: {
          number: [
            {
              required: true, message: '测试用例编号不能为空', trigger: 'blur'
            },
            {
              min: 1, max: 250, message: '1~250个字符', trigger: 'blur'
            }
          ],
          title: [
            {
              required: true, message: '测试用例标题不能为空', trigger: 'blur'
            },
            {
              min: 1, max: 250, message: '1~250个字符', trigger: 'blur'
            }
          ],
          mid: [
            {
              required: true, message: '归属项目模块不能为空', trigger: 'blur'
            },
          ],
          level: [
            {
              required: true, message: '优先级不能为空', trigger: 'blur'
            },
          ],
        },
        // 删除
        deleteTestCaseDialogVisible: false,
        deleteTestCaseID: null,
        // 关联删除的测试步骤
        deleteStepArr: [],

        // 测试用例步骤
        allTestCaseStepList:[],
        activeNames: '',
        caseNameList: [],
        // 接口实例初始化字段配置、断言配置
        cur_step_inc_id: null,
        testCaseFieldInitTab: 'header',
        headerFieldInitList: [],
        bodyFieldInitList: [],
        getFieldPoolList: [],
        setFieldPoolList: [],
        fieldAssertList: [],

        testCaseStepForm: {
          tcid: null,
          inc_id: null,
          header: '',
          body: '',
          step_no: null
        },
        curTestCaseStepListRule: {},
        itemRule: {
          inc_id: [
            {
              required: true, message: '接口编号名称不能为空', trigger: 'blur'
            },
          ],
        },

        // 测试用例步骤断言
        cur_step_id: null,
        testCaseAssertList: [],
        // 新增断言
        addTestCaseAssertDialogVisible: false,
        testCaseAssertForm: {
          sid: null,
          field_owner: 'res_body',
          field_name: '',
          field_node: '',
          assert_type: '',
          field_value: ''
        },
        testCaseAssertFormRules: {
          field_owner: [
            {
              required: true, message: '字段归属不能为空', trigger: 'blur'
            }
          ],
          field_name: [
            {
              required: true, message: '字段名称不能为空', trigger: 'blur'
            }
          ],
          field_node: [
            {
              required: true, message: '字段节点路径不能为空', trigger: 'blur'
            }
          ],
          assert_type: [
            {
              required: true, message: '断言类型不能为空', trigger: 'blur'
            }
          ],
          field_value: [
            {
              required: true, message: '字段值不能为空', trigger: 'blur'
            }
          ],
        },
        feildAssert_field_owner: [
          {
            value: 'res_body',
            label: '响应体'
          },
          {
            value: 'res_header',
            label: '响应头'
          },
        ],
        feildAssert_assert_type: [
          {
            value: 'contains',
            label: '包含'
          },
          {
            value: 'equals',
            label: '等于'
          },
        ],
        // 修改断言
        editTestCaseAssertDialogVisible: false,
        editTestCaseAssertUrl: '',
        editTestCaseAssertChangeCount: 0,
        // 删除断言
        deleteTestCaseAssertDialogVisible: false,
        deleteTestCaseAssertUrl: '',
      }
    },
    created() {
      this.queryTestCase()
      this.getCaseNameList()
    },
    methods: {
      // 查询
      queryTestCase: function() {
        this.$http.get(this.baseUrl, {params: {title: this.title}}).then(res => {
          // console.log(res)
          this.testCaseTableData = res.data
          // console.log(this.testCaseTableData)
          this.total = res.data.total
        })
        this.cur_row_testcase = {
          id: null,
          number: '',
          title: '',
          mid: null,
          bsid: null,
          level: null,
          is_enable: 1,
          creator: '',
          create_time: null,
          update_time: null,
          remark: ''
        }
        this.testCaseList = this.cur_row_testcase
        this.editTestCaseUpdateCount = 0
      },
      // 测试用例列表表格行单击事件
      testCaseRowClick(row) {
        this.isHighlight = true
        this.$http.get(this.baseUrl + row.id).then(res => {
          if(res.status !== 200) {
            this.$message.error('系统异常！')
            return
          }
          if(res.length == 0) {
            this.$message.error('该数据在数据库中不存在！')
            return
          }
          this.cur_row_testcase = res.data
          this.testCaseList = this.cur_row_testcase
          this.getCurTestCaseStepList()
          this.editTestCaseUpdateCount = 0
          })
        // console.log(this.cur_row_testcase)
        // 重置界面默认展示的折叠页
        this.activeNames = ''
        this.testCaseActiveNames = ''
      },

      // 新增用例 归属模块，获取项目、模块层级
      getModuleOptions() {
        // 获取项目名称列表
        this.$http.get(this.$root.URL + '/projectconfig/').then(resp => {
          if(resp.status !== 200) return
          if(resp.data.length == 0) return
          // console.log(resp.data)
          // 添加进option列表
          for(var i=0;i<resp.data.length;i++) {
            // 获取项目对应的所有模块
            const childOption = []
            this.$http.get(this.$root.URL + '/module/', {params: {pid: resp.data[i].id}}).then(resm => {
              if(resm.status !== 200) return
              if(resm.data.length == 0) return
              // console.log(resm.data)
              for(var m=0;m<resm.data.length;m++){
                childOption.push({
                  value: resm.data[m].id,
                  label: resm.data[m].module_name
                })
              }
            })
            // 将项目及模块添加到option
            if(childOption) {
              this.moduleOptions.push({
                value: resp.data[i].id,
                label: resp.data[i].project_name,
                children: childOption
              })
            }else{
              this.moduleOptions.push({
                value: resp.data[i].id,
                label: resp.data[i].project_name
              })
            }
          }
          // console.log(this.moduleOptions)
        })
      },
      // 归属模块值修改触发(值为数组)
      moduleHandleChange(val) {
        // console.log(val)
        this.addTestCaseList.mid = val[1]
      },
      // 新增对话框点击是否启用
      addIsEnableChange: function(e){
         e ? this.addTestCaseList.is_enable = 1 : this.addTestCaseList.is_enable = 0
      },
      // 点击是否启用
      isEnableChange: function(e){
         e ? this.testCaseList.is_enable = 1 : this.testCaseList.is_enable = 0
      },
      // 测试用例，点击添加按钮
      addTestCaseDialogClick() {
        this.addTestCaseDialogVisible = true
        // 清空模块选项
        this.moduleOptions = []
        this.relate_id = null
        // 初始化获取归属模块信息
        this.getModuleOptions()
      },
      // 新增对话框关闭事件
      addTestCaseDialogClose() {
        this.$refs.addTestCaseListRef.resetFields()
      },
      // 新增测试用例保存
      addTestCaseSave() {
        this.$refs.addTestCaseListRef.validate(async valid => {
          if(!valid) return
          // 查询，名称不能重复
          const {data: resq} = await this.$http.get(this.baseUrl, {params: {number: this.addTestCaseList.number}})
          // console.log(resq.length)
          if(resq.length > 0) {
            this.$message.error('测试编号重复，测试用例已存在。')
            return
          }
          // 创建时间、更新时间赋值
          this.addTestCaseList.create_time = this.getNowFormatDate()
          this.addTestCaseList.update_time = this.getNowFormatDate()
          //发起请求
          // console.log(this.testCaseList)
          this.$http.post(this.baseUrl, this.addTestCaseList).then(res => {
            if(res.status !== 201) {
              this.$message.error('新增失败！')
              return
            }
            this.$message.success('新增成功！')
            this.addTestCaseDialogVisible = false
            this.queryTestCase()
          })

        })
      },

      // 获取测试用例基本信息界面，归属项目模块的值
      getEditRelateid() {
        this.$http.get(this.$root.URL + '/module/', {params: {id: this.testCaseList.mid}}).then(res => {
          if(res.status !== 200) return
          this.edit_relate_id = [res.data[0].pid, this.testCaseList.mid]
          // console.log(this.edit_relate_id)
        })
      },
      // 归属项目模块下拉框值改变事件
      editModuleHandleChange(val) {
        this.testCaseList.mid = val[1]
      },
      // 修改保存
      editTestCaseSave() {
        this.$refs.testCaseListRef.validate(valid => {
          if(!valid) return
          // 无修改
          if(this.editTestCaseUpdateCount <= 1) return
          this.testCaseList.update_time = this.getNowFormatDate()
          this.$http.put(this.baseUrl + this.testCaseList.id + '/', this.testCaseList).then(res => {
            if(res.status !== 200) {
              this.$message.error('修改失败！')
              return
            }
            this.$message.success('修改成功！')
            // 测试用例数据重新获取
            this.$http.get(this.baseUrl, {params: {title: this.title}}).then(res => {
              this.testCaseTableData = res.data
              this.total = res.data.total
            })
          })
        })
      },
      // 删除
      deleteTestCaseDialogClose() {
        this.deleteTestCaseID = null
      },
      deleteTestCaseDialog(row) {
        this.deleteTestCaseDialogVisible = true
        this.deleteTestCaseID = row.id
        // 获取测试用例所有测试步骤id
        this.$http.get(this.baseUrl_step, {params: {tc_id: row.id}}).then(res => {
          if(res.status !== 200) return
          if(res.length == 0) return
          for(var i=0;i<res.length;i++){
            this.deleteStepArr.push(res.data[i].id)
          }
        })
      },
      deleteTestCase() {
        this.$http.delete(this.baseUrl + this.deleteTestCaseID + '/').then(resd => {
          if(resd.status !== 204) {
            this.$message.error('删除失败！')
            return
          }
          // // 关联删除 测试步骤
          // this.$http.delete(this.baseUrl_step, {params: {tc_id: this.deleteTestCaseID}}).then(ress => {
          //   if(ress.status !== 204){
          //     this.$message.error('测试用例删除成功，但关联删除测试用例步骤出现异常！')
          //   }
          // })
          // // 关联删除 测试步骤断言
          // if(this.deleteStepArr.length > 0) {
          //   for(var sa=0;sa<this.deleteStepArr;sa++){
          //     this.$http.delete(this.baseUrl_assert, {params: {sid: this.deleteStepArr.slice(sa,sa+1)}}).then(resa => {
          //       if(ress.status !== 204){
          //         this.$message.error('测试用例删除成功，但关联删除测试用例步骤断言出现异常！步骤ID[' + this.deleteStepArr.slice(sa,sa+1) + ']')
          //       }
          //     })
          //   }
          // }
          this.$message.success('删除成功！')
          this.deleteTestCaseDialogVisible = false
          this.queryTestCase()
        })

      },

      // 步骤列表
      getCurTestCaseStepList() {
        this.$http.get(this.baseUrl_step, {params:{tc_id:this.cur_row_testcase.id}}).then(res => {
          // console.log(res)
          this.allTestCaseStepList = res.data
        })
      },
      // 步骤折叠展示切换触发事件
      testCaseStepHandleChange(index) {
        // 关闭折叠展示时，不处理
        // if(index == '') return // 这句会有问题，导致数据不展示
        // console.log(index)
        this.cur_step_inc_id = this.allTestCaseStepList[index].inc_id
        this.cur_step_id = this.allTestCaseStepList[index].id
        // 切换，清空原表格数据
        this.headerFieldInitList = []
        this.bodyFieldInitList = []
        this.getFieldPoolList = []
        this.setFieldPoolList = []
        this.fieldAssertList = []
        // 切换，清空断言list表数据
        this.testCaseAssertList = []
        // 切换，默认展示第一个页签，并重新获取列表数据
        this.testCaseFieldInitTab = 'header'
        this.getHeaderFieldInitList()
        // 切换，获取断言表数据
        this.getTestCaseAssertList()
      },
      // 监听测试用例基本信息折叠窗是否展开
      testCaseHandleChange(val) {
        // 展开时，获取归属项目模块的下拉选项及值
        if(this.testCaseActiveNames.length == 2) {
          // 清空界面校验信息（问题记录：B01）
          this.$refs.testCaseListRef.clearValidate()
          // 先清空下拉选项再获取
          this.moduleOptions = []
          this.getModuleOptions()
          // 清空下拉值再获取
          this.edit_relate_id = []
          this.getEditRelateid()
        }

      },

      // 获取接口实例名称下拉选项
      async getCaseNameList() {
        const {data: res} = await this.$http.get(this.$root.URL + '/instance/')
        // console.log(res)
        if(res.length == 0) return
        const caseList = []
        for(var i=0; i<res.length;i++){
          caseList.push({
            id: res[i].id,
            case_name: res[i].case_name
          })
        }
        this.caseNameList = caseList
      },

      // 添加测试步骤
      addTestCaseStep() {
        // 判断是否已选中测试用例
        if(this.cur_row_testcase.id == null) {
          this.$message.info('请先在测试用例列表中单击选中测试用例!')
          return
        }

        // 为新增的步骤，生成步骤序号
        if(this.allTestCaseStepList.length == 0){
          const aid = 1
          this.allTestCaseStepList = [{
            id: null,
            tc_id: this.cur_row_testcase.id,
            inc_id: null,
            case_name: '',
            header: '',
            body: '',
            step_no: aid
          },]
          // 添加步骤，默认展开折叠组件
          this.activeNames = this.allTestCaseStepList.length-1
          // 字段初始化界面默认重置为第一个页签
          this.testCaseFieldInitTab = 'header'
          // console.log(this.allTestCaseStepList)
          return
        }
        const aid = this.allTestCaseStepList.slice(-1)[0].step_no + 1
        this.allTestCaseStepList.push({
          id: null,
          tc_id: this.cur_row_testcase.id,
          inc_id: null,
          case_name: '',
          header: '',
          body: '',
          step_no: aid
        })
        // console.log(this.allTestCaseStepList)
        // 添加步骤，默认展开折叠组件
        this.activeNames = this.allTestCaseStepList.length-1
        // 折叠组件变化，当前展开的步骤id，实例id也跟着变化，需要进行初始化
        this.cur_step_inc_id = null
        this.cur_step_id = null
        // 涉及切换步骤，清空断言list表数据
        this.testCaseAssertList = []
        // 字段初始化界面默认重置为第一个页签
        this.testCaseFieldInitTab = 'header'
      },
      // 单步骤保存（新增、修改）
      saveTestCaseStep(id, index) {
        // console.log(this.allTestCaseStepList)
        this.$refs.itemRef[index].validate(valid => {
          if(!valid) return
          // 根据id是否为空，判断是新增还是修改
          //修改
          if(id){
            this.$http.put(this.baseUrl_step + id + '/', this.allTestCaseStepList[index]).then(resb => {
              if(resb.status !== 200) {
                this.$message.error('修改失败！')
                return
              }
              this.$message.success('修改成功！')
              // 判断是否修改了 接口实例
              if(this.cur_step_inc_id !== resb.data.inc_id) {
                this.cur_step_inc_id = resb.data.inc_id

                // 切换，清空原表格数据
                this.headerFieldInitList = []
                this.bodyFieldInitList = []
                this.getFieldPoolList = []
                this.setFieldPoolList = []
                this.fieldAssertList = []

              }
              // 为页面list赋id值，实例名称值
              this.allTestCaseStepList.splice(index, 1, resb.data)
              // 切换，默认展示第一个页签，并重新获取列表数据
              this.testCaseFieldInitTab = 'header'
              this.getHeaderFieldInitList()
            })

          }else{ // 新增
            this.$http.post(this.baseUrl_step, this.allTestCaseStepList[index]).then(resa => {
              if(resa.status !== 201) {
                this.$message.error('新增失败！')
                return
              }
              this.$message.success('新增成功！')
              // 为页面list赋id值，实例名称值
              this.allTestCaseStepList.splice(index, 1, resa.data)
              // 为当前展开的步骤，记录id和实例id
              this.cur_step_inc_id = resa.data.inc_id
              this.cur_step_id = resa.data.id

              // 新增成功后，需要刷新初始化字段表数据
              this.testCaseFieldInitTab = 'header'
              this.getHeaderFieldInitList()
            })
          }
          // console.log(this.allTestCaseStepList)
        })
      },

      // 字段初始化配置信息展示
      testCaseFieldInitTabChange(val) {
        if(val.name == 'header'){
          this.getHeaderFieldInitList()
        }else if(val.name == 'body'){
          this.getBodyFieldInitList()
        }else if(val.name == 'get'){
          this.showGetFieldPoolList()
        }else if(val.name == 'set'){
          this.showSetFieldPoolList()
        }else{
          this.getFieldAssertList()
        }
      },
      // 获取请求头list
      getHeaderFieldInitList() {
        if(this.cur_step_inc_id == null) return
        this.$http.get(this.baseurl_fieldinit, {params: {inc_id: this.cur_step_inc_id, field_owner: this.testCaseFieldInitTab}}).then(res => {
          // console.log(res)
          this.headerFieldInitList = res.data
        })
      },
      // 获取请求体list
      getBodyFieldInitList() {
        if(this.cur_step_inc_id == null) return
        this.$http.get(this.baseurl_fieldinit, {params: {inc_id: this.cur_step_inc_id, field_owner: this.testCaseFieldInitTab}}).then(res => {
          // console.log(res)
          this.bodyFieldInitList = res.data
        })
      },
      // 获取从pool读取字段list
      showGetFieldPoolList() {
        if(this.cur_step_inc_id == null) return
        this.$http.get(this.baseurl_fieldpool, {params: {inc_id: this.cur_step_inc_id, handle_type: this.testCaseFieldInitTab}}).then(res => {
          // console.log(res)
          this.getFieldPoolList = res.data
        })
      },
      // 获取写入pool字段list
      showSetFieldPoolList() {
        if(this.cur_step_inc_id == null) return
        this.$http.get(this.baseurl_fieldpool, {params: {inc_id: this.cur_step_inc_id, handle_type: this.testCaseFieldInitTab}}).then(res => {
          // console.log(res)
          this.setFieldPoolList = res.data
        })
      },
      // 获取字段断言list
      getFieldAssertList() {
        if(this.cur_step_inc_id == null) return
        this.$http.get(this.baseurl_fieldassert, {params: {inc_id: this.cur_step_inc_id}}).then(res => {
          // console.log(res)
          this.fieldAssertList = res.data
        })
      },

      // ---测试用例步骤断言---
      // 列表
      getTestCaseAssertList() {
        if(this.cur_step_id == null) return
        this.$http.get(this.baseUrl_assert, {params: {sid: this.cur_step_id}}).then(res => {
          // console.log(res)
          this.testCaseAssertList = res.data
        })
      },
      // 新增-点击添加按钮事件
      addTestCaseAssertDialogClick() {
        if(this.cur_step_id == null){
          this.$message.info('请先完成当前步骤信息！')
          return
        }
        this.addTestCaseAssertDialogVisible = true
      },
      // 新增-对话窗关闭事件
      addTestCaseAssertDialogClose() {
        this.$refs.testCaseAssertFormRef.resetFields()
        this.editTestCaseAssertChangeCount = 0
      },
      // 新增-点击保存按钮
      saveTestCaseAssert() {
        // 测试步骤ID sid赋值
        this.testCaseAssertForm.sid = this.cur_step_id
        this.$http.post(this.baseUrl_assert, this.testCaseAssertForm).then(res => {
          if(res.status !== 201) {
            this.$message.error('新增失败！')
            return
          }
          this.$message.success('新增成功！')
          this.addTestCaseAssertDialogVisible = false
          this.getTestCaseAssertList()
        })

      },
      // 修改 步骤断言
      editTestCaseAssertDialog(row) {
        this.editTestCaseAssertDialogVisible = true
        // 查询记录
        this.$http.get(this.baseUrl_assert + row.id + '/').then(resq => {
          if(resq.status !== 200) return
          if(resq.length == 0) {
            this.$message.error('修改的记录在数据库中不存在。')
            return
          }
          this.testCaseAssertForm = resq.data
        })
        this.editTestCaseAssertUrl = this.baseUrl_assert + row.id + '/'
      },
      // 修改对话框关闭事件
      editTestCaseAssertDialogClose() {
        this.$refs.testCaseAssertFormRef.resetFields()
        this.editTestCaseAssertChangeCount = 0
        this.editTestCaseAssertUrl = ''
      },
      // 修改保存
      editTestCaseAssertSave() {
        // 判断是否有进行修改
        if(this.editTestCaseAssertChangeCount <= 1){
          this.editTestCaseAssertDialogVisible = false
        }
        this.$http.put(this.editTestCaseAssertUrl, this.testCaseAssertForm).then(res => {
          if(res.status !== 200) {
            this.$message.error('修改失败！')
            return
          }
          this.$message.success('修改成功！')
          this.editTestCaseAssertDialogVisible = false
          this.getTestCaseAssertList()
        })
      },

      // 删除 步骤断言
      deleteTestCaseAssertDialog(row) {
        this.deleteTestCaseAssertDialogVisible = true
        this.deleteTestCaseAssertUrl = this.baseUrl_assert + row.id + '/'
      },
      // 删除-对话框关闭事件
      deleteTestCaseAssertDialogClose() {
        this.deleteTestCaseAssertUrl = ''
      },
      // 删除-确定按钮事件
      deleteTestCaseAssert() {
        // 查询数据库是否存在该数据
        this.$http.get(this.deleteTestCaseAssertUrl).then(resq => {
          if(resq.status !== 200) {
            this.$message.error('系统异常！')
            return
          }
          if(resq.length == 0) {
            this.$message.error('该记录在数据库中不存在。')
            return
          }
        })
        this.$http.delete(this.deleteTestCaseAssertUrl).then(res => {
          if(res.status !== 204) {
            this.$message.error('删除失败！')
            return
          }
          this.$message.success('删除成功！')
          this.deleteTestCaseAssertDialogVisible = false
          this.getTestCaseAssertList()
        })
      },

      // 保存所有步骤
      saveAllTestCaseStep(){

      },
      // 删除步骤
      deleteTestCaseStep(id, index) {
        // 判断id是否为空，为空则说明该步骤未保存到数据库
        if(id == null) {
          this.allTestCaseStepList.splice(index, 1)
          this.$message.success('删除成功！')
          this.getCurTestCaseStepList()
          return
        }
        this.$http.delete(this.baseUrl_step + id).then(res => {
          if(res.status !== 204){
            this.$message.error('删除失败！')
            return
          }
          // // 关联删除 步骤断言
          // this.$http.get(this.baseUrl_assert, {params: {sid: id}}).then(resq => {
          //   if(resq.status !== 200) return this.$message.error('删除步骤成功，但关联步骤断言信息查询失败！')
          //   if(resq.length == 0) return
          //   this.$http.delete(this.baseUrl_assert, {params: {sid: id}}).then(resa => {
          //     if(resa.status !== 204){
          //       this.$message.error('删除步骤成功，但关联步骤断言信息删除失败！')
          //       return
          //     }
          //   })
          // })
          this.$message.success('删除成功！')
          this.getCurTestCaseStepList()
        })

      },

      //获取当前时间
      getNowFormatDate() {
      	var date = new Date();
      	var seperator1 = "-";
      	var seperator2 = ":";
      	var month = date.getMonth() + 1<10? "0"+(date.getMonth() + 1):date.getMonth() + 1;
      	var strDate = date.getDate()<10? "0" + date.getDate():date.getDate();
      	var currentdate = date.getFullYear() + seperator1  + month  + seperator1  + strDate
      			+ " "  + date.getHours()  + seperator2  + date.getMinutes()
      			+ seperator2 + date.getSeconds();
      	return currentdate;
      }
    },
    watch: {
      testCaseList: {
           handler (val) {
             if (val) {
               this.editTestCaseUpdateCount++
               // console.log(this.editTestCaseUpdateCount)
          }
        },
        deep: true
      },
      testCaseAssertForm: {
           handler (val) {
             if (val) {
               this.editTestCaseAssertChangeCount++
          }
        },
        deep: true
      },
    }
  }
</script>

<style lang="less" scoped>
  .el-input-group {
    width: 80%;
  }
  .el-button {
    align-items: center;
  }
  .el-table {
    margin-top: 0px;
  }
  .showbusi {
    width: 30%;
  }
  .stepdel {
    float: right;
  }
  .stepchange {
    float: right;
  }
</style>
