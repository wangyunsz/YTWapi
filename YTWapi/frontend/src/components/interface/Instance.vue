<template>
	<div>
		<!-- 面包屑 -->
		<el-breadcrumb separator-class="el-icon-arrow-right">
		  <el-breadcrumb-item :to="{ path: '/home' }">首页</el-breadcrumb-item>
		  <el-breadcrumb-item>接口管理</el-breadcrumb-item>
		  <el-breadcrumb-item>接口实例</el-breadcrumb-item>
		</el-breadcrumb>

    <!-- 卡片区域 -->
    <el-card class="box-card">
      <el-form :inline="true" :model="queryInfo" class="demo-form-inline" size="mini">
        <el-form-item label="实例名称">
          <el-input v-model="queryInfo.case_name" placeholder="实例名称" clearable></el-input>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="getInstanceList">查询</el-button>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="addDialogVisible = true">添加</el-button>
        </el-form-item>
      </el-form>

      <!-- 列表数据区 -->
      <template>
        <el-table
          :data="tableData"
          border
          stripe>
          <el-table-column type="index" label="#"></el-table-column>
          <el-table-column prop="intf_id" label="接口ID" v-if="false"></el-table-column>
          <el-table-column prop="interface_name" label="接口名称"></el-table-column>
          <el-table-column prop="interface_path" label="接口地址"></el-table-column>
          <el-table-column prop="case_name" label="实例名称"></el-table-column>
          <el-table-column prop="case_description" label="实例说明"></el-table-column>
          <el-table-column prop="is_selected" label="是否默认">
            <template slot-scope="scope">
              <el-tag type="success" v-if="scope.row.is_selected">默认</el-tag>
              <el-tag type="danger" v-else>非默认</el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="remark" label="备注"></el-table-column>

          <el-table-column label="操作" min-width="90px">
            <template slot-scope="scope">
              <el-tooltip effect="dark" content="修改" placement="top" :enterable="false">
                <el-button type="primary" icon="el-icon-edit" size="mini" @click="editInstanceDialog(scope.row)"></el-button>
              </el-tooltip>
              <el-tooltip effect="dark" content="删除" placement="top" :enterable="false">
                <el-button type="danger" icon="el-icon-delete" size="mini" @click="deleteInstanceDialog(scope.row)"></el-button>
              </el-tooltip>
              <el-tooltip effect="dark" content="接口实例配置" placement="top" :enterable="false">
                <el-button type="primary" icon="el-icon-setting" size="mini" @click="instanceConfigDialog(scope.row)"></el-button>
              </el-tooltip>
            </template>
          </el-table-column>
        </el-table>
      </template>

      <!-- 分页 -->
      <el-pagination
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
        :current-page="queryInfo.curpage"
        :page-sizes="[5, 10, 20, 50, 100]"
        :page-size="queryInfo.pagesize"
        layout="total, sizes, prev, pager, next, jumper"
        :total="total">
      </el-pagination>
    </el-card>

    <!-- 新增功能 -->
    <el-dialog
      title="新增接口实例"
      :visible.sync="addDialogVisible"
      width="50%"
      center @close="addInstanceClose"
      :close-on-click-modal="false">
      <el-form label-width="100px" :model="instanceForm"
        :rules="addInstanceRules" ref="addInstanceRef">
        <el-form-item label="接口ID" prop="intf_id">
         <el-select v-model="instanceForm.intf_id" placeholder="请选择" @change="relateInterface">
            <el-option
              v-for="item,index in idValue"
              :key="index"
              :value="item.intf_id">
              <span>{{ item.intf_id }}--{{ item.label }}</span>
            </el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="接口名称" prop="interface_name">
          <el-input v-model="instanceForm.interface_name" placeholder="自动带出" disabled></el-input>
        </el-form-item>
        <el-form-item label="接口地址" prop="interface_path">
          <el-input v-model="instanceForm.interface_path" placeholder="自动带出" disabled></el-input>
        </el-form-item>
        <el-form-item label="实例名称" prop="case_name">
          <el-input v-model="instanceForm.case_name"></el-input>
        </el-form-item>
        <el-form-item label="实例说明" prop="case_description">
          <el-input v-model="instanceForm.case_description"></el-input>
        </el-form-item>
        <el-form-item label="是否默认" prop="is_selected">
          <el-select v-model="instanceForm.is_selected" placeholder="请选择">
            <el-option
              v-for="item in [{value: 1, label: '默认'}, {value: 0, label: '非默认'}]"
              :key="item.value"
              :label="item.label"
              :value="item.value">
            </el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="备注" prop="remark">
          <el-input type="textarea" v-model="instanceForm.remark"></el-input>
        </el-form-item>

      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="addDialogVisible = false">取 消</el-button>
        <el-button type="primary" @click="addInstance">确 定</el-button>
      </span>
    </el-dialog>

    <!-- 修改接口 -->
    <el-dialog
      title="修改接口实例"
      :visible.sync="editDialogVisible"
      width="50%"
      center @close="editInstanceClose"
      :close-on-click-modal="false">
      <el-form label-width="100px" :model="instanceForm"
        :rules="addInstanceRules" ref="editInstanceRef">
        <el-form-item label="接口ID" prop="intf_id">
         <el-select v-model="instanceForm.intf_id" placeholder="请选择" @change="relateInterface" disabled>
            <el-option
              v-for="item,index in idValue"
              :key="index"
              :value="item.intf_id">
              <span>{{ item.intf_id }}--{{ item.label }}</span>
            </el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="接口名称" prop="interface_name">
          <el-input v-model="instanceForm.interface_name" placeholder="自动带出" disabled></el-input>
        </el-form-item>
        <el-form-item label="接口地址" prop="interface_path">
          <el-input v-model="instanceForm.interface_path" placeholder="自动带出" disabled></el-input>
        </el-form-item>
        <el-form-item label="实例名称" prop="case_name">
          <el-input v-model="instanceForm.case_name"></el-input>
        </el-form-item>

        <el-form-item label="实例说明" prop="case_description">
          <el-input type="textarea" v-model="instanceForm.case_description"></el-input>
        </el-form-item>
        <el-form-item label="是否默认" prop="is_selected">
          <el-select v-model="instanceForm.is_selected" placeholder="请选择">
            <el-option
              v-for="item in [{value: 1, label: '默认'}, {value: 0, label: '非默认'}]"
              :key="item.value"
              :label="item.label"
              :value="item.value">
            </el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="备注" prop="remark">
          <el-input type="textarea" v-model="instanceForm.remark"></el-input>
        </el-form-item>

      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="editDialogVisible = false">取 消</el-button>
        <el-button type="primary" @click="editInstance">确 定</el-button>
      </span>
    </el-dialog>

    <!-- 删除 -->
    <!-- 删除接口弹窗对话框 -->
    <el-dialog
      title="提示"
      :visible.sync="deleteDialogVisible"
      width="30%"
      @close="deleteInstanceClose"
      :close-on-click-modal="false">
      <span>请确认是否删除？</span>
      <span slot="footer" class="dialog-footer">
        <el-button @click="deleteDialogVisible = false">取 消</el-button>
        <el-button type="primary" @click="deleteInstance">确 定</el-button>
      </span>
    </el-dialog>

    <!-- 接口实例配置 -->
    <el-dialog
      title="接口实例配置"
      :visible.sync="instanceConfigDialogVisible"
      width="80%"
      center @close="instanceConfigDialogClose"
      :close-on-click-modal="false">
      <el-form label-width="100px" :model="instanceConfigForm"
       ref="instanceConfigRef" size="mini">
        <el-collapse v-model="activeNames" @change="handleChange">
          <el-collapse-item title="接口信息" name="1">
            <el-card class="box-card">
              <el-form-item label="接口ID" prop="intf_id">
               <el-select v-model="instanceConfigForm.intf_id" placeholder="自动带出" @change="relateInterface" disabled>
                  <el-option
                    v-for="item,index in idValue"
                    :key="index"
                    :value="item.intf_id">
                    <span>{{ item.intf_id }}--{{ item.label }}</span>
                  </el-option>
                </el-select>
              </el-form-item>
              <el-form-item label="接口名称" prop="interface_name">
                <el-input v-model="instanceConfigForm.interface_name" placeholder="自动带出" disabled></el-input>
              </el-form-item>
              <el-form-item label="接口地址" prop="interface_path">
                <el-input v-model="instanceConfigForm.interface_path" placeholder="自动带出" disabled></el-input>
              </el-form-item>
            </el-card>
          </el-collapse-item>
          <el-collapse-item title="接口实例信息" name="2">
            <el-card class="box-card">
              <el-form-item label="实例名称" prop="case_name">
                <el-input v-model="instanceConfigForm.case_name" disabled></el-input>
              </el-form-item>

              <el-form-item label="实例说明" prop="case_description">
                <el-input type="textarea" v-model="instanceConfigForm.case_description" disabled></el-input>
              </el-form-item>
              <el-form-item label="是否默认" prop="is_selected">
                <el-select v-model="instanceConfigForm.is_selected" placeholder="请选择" disabled>
                  <el-option
                    v-for="item in [{value: 1, label: '默认'}, {value: 0, label: '非默认'}]"
                    :key="item.value"
                    :label="item.label"
                    :value="item.value">
                  </el-option>
                </el-select>
              </el-form-item>
              <el-form-item label="备注" prop="remark">
                <el-input type="textarea" v-model="instanceConfigForm.remark" disabled></el-input>
              </el-form-item>
            </el-card>
          </el-collapse-item>
          <el-collapse-item title="初始化字段值配置[固定值/函数生成]" name="3">
            <el-card class="box-card">
              <!-- 列表数据区 -->
              <template>
                <el-tabs v-model="fieldInitTab" type="border-card" @tab-click="fieldInitTabChange">
                  <el-tab-pane label="请求头" name="header">
                    <el-button type="primary" @click="addHeaderFieldInitDialogClick" size="small">添加</el-button>
                    <el-table :data="headerFieldInitList" border stripe size="mini">
                      <el-table-column type="index" label="#"></el-table-column>
                      <el-table-column prop="inc_id" label="接口实例ID" v-if="false"></el-table-column>
                      <el-table-column prop="field_owner" label="字段归属"></el-table-column>
                      <el-table-column prop="field_name" label="字段名称"></el-table-column>
                      <el-table-column prop="field_node" label="字段节点路径"></el-table-column>
                      <el-table-column prop="field_value" label="字段值"></el-table-column>
                      <el-table-column label="操作" min-width="90px">
                        <template slot-scope="scope">
                          <el-tooltip effect="dark" content="修改" placement="top" :enterable="false">
                            <el-button type="primary" icon="el-icon-edit" size="mini" @click="editHeaderFieldInitDialog(scope.row)"></el-button>
                          </el-tooltip>
                          <el-tooltip effect="dark" content="删除" placement="top" :enterable="false">
                            <el-button type="danger" icon="el-icon-delete" size="mini" @click="deleteHeaderFieldInitDialog(scope.row)"></el-button>
                          </el-tooltip>
                        </template>
                      </el-table-column>
                    </el-table>
                  </el-tab-pane>
                 <el-tab-pane label="请求体" name="body">
                    <el-button type="primary" @click="addBodyFieldInitDialogClick" size="small">添加</el-button>
                    <el-table :data="bodyFieldInitList" border stripe size="mini">
                      <el-table-column type="index" label="#"></el-table-column>
                      <el-table-column prop="inc_id" label="接口实例ID" v-if="false"></el-table-column>
                      <el-table-column prop="field_owner" label="字段归属"></el-table-column>
                      <el-table-column prop="field_name" label="字段名称"></el-table-column>
                      <el-table-column prop="field_node" label="字段节点路径"></el-table-column>
                      <el-table-column prop="field_value" label="字段值"></el-table-column>
                      <el-table-column label="操作" min-width="90px">
                        <template slot-scope="scope">
                          <el-tooltip effect="dark" content="修改" placement="top" :enterable="false">
                            <el-button type="primary" icon="el-icon-edit" size="mini" @click="editBodyFieldInitDialog(scope.row)"></el-button>
                          </el-tooltip>
                          <el-tooltip effect="dark" content="删除" placement="top" :enterable="false">
                            <el-button type="danger" icon="el-icon-delete" size="mini" @click="deleteBodyFieldInitDialog(scope.row)"></el-button>
                          </el-tooltip>
                        </template>
                      </el-table-column>
                    </el-table>
                  </el-tab-pane>
                </el-tabs>
              </template>
            </el-card>
          </el-collapse-item>
          <el-collapse-item title="初始化字段配置[接口资源池关联获取]" name="4">
            <el-card class="box-card">
              <!-- POOL列表数据区 -->
              <template>
                <el-tabs v-model="FieldPoolTab" type="border-card" @tab-click="getFieldPoolTabChange">
                  <el-tab-pane label="从Pool读取" name="get">
                    <el-button type="primary" @click="addGetFieldPoolDialogClick" size="small">添加</el-button>
                    <el-table :data="getFieldPoolList" border stripe size="mini">
                      <el-table-column type="index" label="#"></el-table-column>
                      <el-table-column prop="inc_id" label="接口实例ID" v-if="false"></el-table-column>
                      <el-table-column prop="field_owner" label="字段归属"></el-table-column>
                      <el-table-column prop="handle_type" label="操作类型"></el-table-column>
                      <el-table-column prop="field_name" label="字段名称"></el-table-column>
                      <el-table-column prop="field_node" label="字段节点路径"></el-table-column>
                      <el-table-column prop="pool_field" label="Pool字段名称"></el-table-column>
                      <el-table-column label="操作" min-width="90px">
                        <template slot-scope="scope">
                          <el-tooltip effect="dark" content="修改" placement="top" :enterable="false">
                            <el-button type="primary" icon="el-icon-edit" size="mini" @click="editGetFieldPoolDialog(scope.row)"></el-button>
                          </el-tooltip>
                          <el-tooltip effect="dark" content="删除" placement="top" :enterable="false">
                            <el-button type="danger" icon="el-icon-delete" size="mini" @click="deleteGetFieldPoolDialog(scope.row)"></el-button>
                          </el-tooltip>
                        </template>
                      </el-table-column>
                    </el-table>
                  </el-tab-pane>
                 <el-tab-pane label="写入Pool中" name="set">
                    <el-button type="primary" @click="addSetFieldPoolDialogClick" size="small">添加</el-button>
                    <el-table :data="setFieldPoolList" border stripe size="mini">
                      <el-table-column type="index" label="#"></el-table-column>
                      <el-table-column prop="inc_id" label="接口实例ID" v-if="false"></el-table-column>
                      <el-table-column prop="field_owner" label="字段归属"></el-table-column>
                      <el-table-column prop="handle_type" label="操作类型"></el-table-column>
                      <el-table-column prop="field_name" label="字段名称"></el-table-column>
                      <el-table-column prop="field_node" label="字段节点路径"></el-table-column>
                      <el-table-column prop="pool_field" label="Pool字段名称"></el-table-column>
                      <el-table-column label="操作" min-width="90px">
                        <template slot-scope="scope">
                          <el-tooltip effect="dark" content="修改" placement="top" :enterable="false">
                            <el-button type="primary" icon="el-icon-edit" size="mini" @click="editSetFieldPoolDialog(scope.row)"></el-button>
                          </el-tooltip>
                          <el-tooltip effect="dark" content="删除" placement="top" :enterable="false">
                            <el-button type="danger" icon="el-icon-delete" size="mini" @click="deleteSetFieldPoolDialog(scope.row)"></el-button>
                          </el-tooltip>
                        </template>
                      </el-table-column>
                    </el-table>
                  </el-tab-pane>
                </el-tabs>
              </template>
            </el-card>
          </el-collapse-item>
          <el-collapse-item title="字段断言设置[初步断言/通用型断言]" name="5">
            <el-card class="box-card">
              <template>
                <el-button type="primary" @click="addFieldAssertDialogClick" size="small">添加</el-button>
                <el-table :data="fieldAssertList" border stripe size="mini">
                  <el-table-column type="index" label="#"></el-table-column>
                  <el-table-column prop="inc_id" label="接口实例ID" v-if="false"></el-table-column>
                  <el-table-column prop="field_owner" label="字段归属"></el-table-column>
                  <el-table-column prop="field_name" label="字段名"></el-table-column>
                  <el-table-column prop="field_node" label="字段节点路径"></el-table-column>
                  <el-table-column prop="assert_type" label="断言类型"></el-table-column>
                  <el-table-column prop="field_value" label="字段值"></el-table-column>
                  <el-table-column label="操作">
                    <template slot-scope="scope">
                      <el-tooltip effect="dark" content="修改" placement="top" :enterable="false">
                        <el-button type="primary" icon="el-icon-edit" size="mini" @click="editFieldAssertDialog(scope.row)"></el-button>
                      </el-tooltip>
                      <el-tooltip effect="dark" content="删除" placement="top" :enterable="false">
                        <el-button type="danger" icon="el-icon-delete" size="mini" @click="deleteFieldAssertDialog(scope.row)"></el-button>
                      </el-tooltip>
                    </template>
                  </el-table-column>
                </el-table>
              </template>
            </el-card>
          </el-collapse-item>
        </el-collapse>

      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="instanceConfigDialogVisible = false">取 消</el-button>
        <el-button type="primary" @click="saveInstanceConfig">完 成</el-button>
      </span>
    </el-dialog>

    <!-- 新增 请求头初始化字段 -->
    <el-dialog
      title="新增初始化字段"
      :visible.sync="addHeaderFieldInitDialogVisible"
      width="50%"
      center @close="addHeaderFieldInitDialogClose"
      :close-on-click-modal="false">
      <el-form label-width="120px" :model="headerFieldInitTableForm"
        :rules="headerFieldInitTableFormRules" ref="headerFieldInitTableFormRef">
        <el-form-item label="接口实例ID" prop="inc_id" v-if="false">
          <el-input v-model="headerFieldInitTableForm.inc_id"></el-input>
        </el-form-item>
        <el-form-item label="字段归属" prop="field_owner">
          <el-input v-model="headerFieldInitTableForm.field_owner" disabled></el-input>
        </el-form-item>
        <el-form-item label="字段名称" prop="field_name">
          <el-input v-model="headerFieldInitTableForm.field_name"></el-input>
        </el-form-item>
        <el-form-item label="字段节点路径" prop="field_node">
          <el-input v-model="headerFieldInitTableForm.field_node"></el-input>
        </el-form-item>
        <el-form-item label="字段值" prop="field_value">
          <el-input v-model="headerFieldInitTableForm.field_value"></el-input>
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="addHeaderFieldInitDialogVisible = false">取 消</el-button>
        <el-button type="primary" @click="saveHeaderFieldInit">确 定</el-button>
      </span>
    </el-dialog>

    <!-- 删除 -->
    <el-dialog
      title="提示"
      :visible.sync="deleteHeaderFieldInitDialogVisible"
      width="30%"
      @close="deleteHeaderFieldInitDialogClose"
      :close-on-click-modal="false">
      <span>请确认是否删除？</span>
      <span slot="footer" class="dialog-footer">
        <el-button @click="deleteHeaderFieldInitDialogVisible = false">取 消</el-button>
        <el-button type="primary" @click="deleteHeaderFieldInit">确 定</el-button>
      </span>
    </el-dialog>

    <!-- 修改 请求头初始化字段 -->
    <el-dialog
      title="修改初始化字段"
      :visible.sync="editHeaderFieldInitDialogVisible"
      width="50%"
      center @close="editHeaderFieldInitDialogClose"
      :close-on-click-modal="false">
      <el-form label-width="120px" :model="headerFieldInitTableForm"
        :rules="headerFieldInitTableFormRules" ref="headerFieldInitTableFormRef">
        <el-form-item label="接口实例ID" prop="inc_id" v-if="false">
          <el-input v-model="headerFieldInitTableForm.inc_id"></el-input>
        </el-form-item>
        <el-form-item label="字段归属" prop="field_owner">
          <el-input v-model="headerFieldInitTableForm.field_owner" disabled></el-input>
        </el-form-item>
        <el-form-item label="字段名称" prop="field_name">
          <el-input v-model="headerFieldInitTableForm.field_name"></el-input>
        </el-form-item>
        <el-form-item label="字段节点路径" prop="field_node">
          <el-input v-model="headerFieldInitTableForm.field_node"></el-input>
        </el-form-item>
        <el-form-item label="字段值" prop="field_value">
          <el-input v-model="headerFieldInitTableForm.field_value"></el-input>
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="editHeaderFieldInitDialogVisible = false">取 消</el-button>
        <el-button type="primary" @click="saveEditHeaderFieldInit">确 定</el-button>
      </span>
    </el-dialog>

    <!-- 新增 请求体初始化字段 -->
    <el-dialog
      title="新增初始化字段"
      :visible.sync="addBodyFieldInitDialogVisible"
      width="50%"
      center @close="addBodyFieldInitDialogClose"
      :close-on-click-modal="false">
      <el-form label-width="120px" :model="bodyFieldInitTableForm"
        :rules="bodyFieldInitTableFormRules" ref="bodyFieldInitTableFormRef">
        <el-form-item label="接口实例ID" prop="inc_id" v-if="false">
          <el-input v-model="bodyFieldInitTableForm.inc_id"></el-input>
        </el-form-item>
        <el-form-item label="字段归属" prop="field_owner">
          <el-input v-model="bodyFieldInitTableForm.field_owner" disabled></el-input>
        </el-form-item>
        <el-form-item label="字段名称" prop="field_name">
          <el-input v-model="bodyFieldInitTableForm.field_name"></el-input>
        </el-form-item>
        <el-form-item label="字段节点路径" prop="field_node">
          <el-input v-model="bodyFieldInitTableForm.field_node"></el-input>
        </el-form-item>
        <el-form-item label="字段值" prop="field_value">
          <el-input v-model="bodyFieldInitTableForm.field_value"></el-input>
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="addBodyFieldInitDialogVisible = false">取 消</el-button>
        <el-button type="primary" @click="saveBodyFieldInit">确 定</el-button>
      </span>
    </el-dialog>

    <!-- 删除 -->
    <el-dialog
      title="提示"
      :visible.sync="deleteBodyFieldInitDialogVisible"
      width="30%"
      @close="deleteBodyFieldInitDialogClose"
      :close-on-click-modal="false">
      <span>请确认是否删除？</span>
      <span slot="footer" class="dialog-footer">
        <el-button @click="deleteBodyFieldInitDialogVisible = false">取 消</el-button>
        <el-button type="primary" @click="deleteBodyFieldInit">确 定</el-button>
      </span>
    </el-dialog>

    <!-- 修改 请求体初始化字段 -->
    <el-dialog
      title="修改初始化字段"
      :visible.sync="editBodyFieldInitDialogVisible"
      width="50%"
      center @close="editBodyFieldInitDialogClose"
      :close-on-click-modal="false">
      <el-form label-width="120px" :model="bodyFieldInitTableForm"
        :rules="bodyFieldInitTableFormRules" ref="bodyFieldInitTableFormRef">
        <el-form-item label="接口实例ID" prop="inc_id" v-if="false">
          <el-input v-model="bodyFieldInitTableForm.inc_id"></el-input>
        </el-form-item>
        <el-form-item label="字段归属" prop="field_owner">
          <el-input v-model="bodyFieldInitTableForm.field_owner" disabled></el-input>
        </el-form-item>
        <el-form-item label="字段名称" prop="field_name">
          <el-input v-model="bodyFieldInitTableForm.field_name"></el-input>
        </el-form-item>
        <el-form-item label="字段节点路径" prop="field_node">
          <el-input v-model="bodyFieldInitTableForm.field_node"></el-input>
        </el-form-item>
        <el-form-item label="字段值" prop="field_value">
          <el-input v-model="bodyFieldInitTableForm.field_value"></el-input>
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="editBodyFieldInitDialogVisible = false">取 消</el-button>
        <el-button type="primary" @click="saveEditBodyFieldInit">确 定</el-button>
      </span>
    </el-dialog>

    <!-- POOL------------------------ -->
    <!-- 新增 请求头初始化字段 -->
    <el-dialog
      title="新增从POOL中读取字段"
      :visible.sync="addGetFieldPoolDialogVisible"
      width="50%"
      center @close="addGetFieldPoolDialogClose"
      :close-on-click-modal="false">
      <el-form label-width="120px" :model="fieldPoolTableForm"
        :rules="fieldPoolTableFormRules" ref="fieldPoolTableFormRef">
        <el-form-item label="接口实例ID" prop="inc_id" v-if="false">
          <el-input v-model="fieldPoolTableForm.inc_id"></el-input>
        </el-form-item>
        <el-form-item label="字段归属" prop="field_owner">
          <el-select v-model="fieldPoolTableForm.field_owner" placeholder="请选择">
            <el-option
              v-for="item,index in field_owner"
              :key="index"
              :label="item.label"
              :value="item.value">
              <span style="float: left">{{ item.label }}</span>
              <span style="float: right; color: #8492a6; font-size: 13px">{{ item.value }}</span>
            </el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="操作类型" prop="handle_type" v-if="false">
          <el-input v-model="fieldPoolTableForm.handle_type" disabled></el-input>
        </el-form-item>
        <el-form-item label="字段名称" prop="field_name">
          <el-input v-model="fieldPoolTableForm.field_name"></el-input>
        </el-form-item>
        <el-form-item label="字段节点路径" prop="field_node">
          <el-input v-model="fieldPoolTableForm.field_node"></el-input>
        </el-form-item>
        <el-form-item label="Pool字段名称" prop="pool_field">
          <el-input v-model="fieldPoolTableForm.pool_field"></el-input>
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="addGetFieldPoolDialogVisible = false">取 消</el-button>
        <el-button type="primary" @click="saveGetFieldPool">确 定</el-button>
      </span>
    </el-dialog>

    <!-- 删除 -->
    <el-dialog
      title="提示"
      :visible.sync="deleteGetFieldPoolDialogVisible"
      width="30%"
      @close="deleteGetFieldPoolDialogClose"
      :close-on-click-modal="false">
      <span>请确认是否删除？</span>
      <span slot="footer" class="dialog-footer">
        <el-button @click="deleteGetFieldPoolDialogVisible = false">取 消</el-button>
        <el-button type="primary" @click="deleteGetFieldPool">确 定</el-button>
      </span>
    </el-dialog>

    <!-- 修改 请求头初始化字段 -->
    <el-dialog
      title="修改初始化字段"
      :visible.sync="editGetFieldPoolDialogVisible"
      width="50%"
      center @close="editGetFieldPoolDialogClose"
      :close-on-click-modal="false">
      <el-form label-width="120px" :model="fieldPoolTableForm"
        :rules="fieldPoolTableFormRules" ref="fieldPoolTableFormRef">
        <el-form-item label="接口实例ID" prop="inc_id" v-if="false">
          <el-input v-model="fieldPoolTableForm.inc_id"></el-input>
        </el-form-item>
        <el-form-item label="字段归属" prop="field_owner">
          <el-select v-model="fieldPoolTableForm.field_owner" placeholder="请选择">
            <el-option
              v-for="item,index in field_owner"
              :key="index"
              :label="item.label"
              :value="item.value">
              <span style="float: left">{{ item.label }}</span>
              <span style="float: right; color: #8492a6; font-size: 13px">{{ item.value }}</span>
            </el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="操作类型" prop="handle_type" v-if="false">
          <el-input v-model="fieldPoolTableForm.handle_type" disabled></el-input>
        </el-form-item>
        <el-form-item label="字段名称" prop="field_name">
          <el-input v-model="fieldPoolTableForm.field_name"></el-input>
        </el-form-item>
        <el-form-item label="字段节点路径" prop="field_node">
          <el-input v-model="fieldPoolTableForm.field_node"></el-input>
        </el-form-item>
        <el-form-item label="Pool字段名称" prop="pool_field">
          <el-input v-model="fieldPoolTableForm.pool_field"></el-input>
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="editGetFieldPoolDialogVisible = false">取 消</el-button>
        <el-button type="primary" @click="saveEditGetFieldPool">确 定</el-button>
      </span>
    </el-dialog>

    <!-- 新增 写入Pool中字段设置 -->
    <el-dialog
      title="新增写入Pool中字段"
      :visible.sync="addSetFieldPoolDialogVisible"
      width="50%"
      center @close="addSetFieldPoolDialogClose"
      :close-on-click-modal="false">
      <el-form label-width="120px" :model="setFieldPoolTableForm"
        :rules="setFieldPoolTableFormRules" ref="setFieldPoolTableFormRef">
        <el-form-item label="接口实例ID" prop="inc_id" v-if="false">
          <el-input v-model="setFieldPoolTableForm.inc_id"></el-input>
        </el-form-item>
        <el-form-item label="字段归属" prop="field_owner">
          <el-select v-model="setFieldPoolTableForm.field_owner" placeholder="请选择">
            <el-option
              v-for="item,index in field_owner"
              :key="index"
              :label="item.label"
              :value="item.value">
              <span style="float: left">{{ item.label }}</span>
              <span style="float: right; color: #8492a6; font-size: 13px">{{ item.value }}</span>
            </el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="操作类型" prop="handle_type" v-if="false">
          <el-input v-model="setFieldPoolTableForm.handle_type" disabled></el-input>
        </el-form-item>
        <el-form-item label="字段名称" prop="field_name">
          <el-input v-model="setFieldPoolTableForm.field_name"></el-input>
        </el-form-item>
        <el-form-item label="字段节点路径" prop="field_node">
          <el-input v-model="setFieldPoolTableForm.field_node"></el-input>
        </el-form-item>
        <el-form-item label="Pool字段名称" prop="pool_field">
          <el-input v-model="setFieldPoolTableForm.pool_field"></el-input>
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="addSetFieldPoolDialogVisible = false">取 消</el-button>
        <el-button type="primary" @click="saveSetFieldPool">确 定</el-button>
      </span>
    </el-dialog>

    <!-- 删除 -->
    <el-dialog
      title="提示"
      :visible.sync="deleteSetFieldPoolDialogVisible"
      width="30%"
      @close="deleteSetFieldPoolDialogClose"
      :close-on-click-modal="false">
      <span>请确认是否删除？</span>
      <span slot="footer" class="dialog-footer">
        <el-button @click="deleteSetFieldPoolDialogVisible = false">取 消</el-button>
        <el-button type="primary" @click="deleteSetFieldPool">确 定</el-button>
      </span>
    </el-dialog>

    <!-- 修改 请求体初始化字段 -->
    <el-dialog
      title="修改初始化字段"
      :visible.sync="editSetFieldPoolDialogVisible"
      width="50%"
      center @close="editSetFieldPoolDialogClose"
      :close-on-click-modal="false">
      <el-form label-width="120px" :model="setFieldPoolTableForm"
        :rules="setFieldPoolTableFormRules" ref="setFieldPoolTableFormRef">
        <el-form-item label="接口实例ID" prop="inc_id" v-if="false">
          <el-input v-model="setFieldPoolTableForm.inc_id"></el-input>
        </el-form-item>
        <el-form-item label="字段归属" prop="field_owner">
          <el-select v-model="setFieldPoolTableForm.field_owner" placeholder="请选择">
            <el-option
              v-for="item,index in field_owner"
              :key="index"
              :label="item.label"
              :value="item.value">
              <span style="float: left">{{ item.label }}</span>
              <span style="float: right; color: #8492a6; font-size: 13px">{{ item.value }}</span>
            </el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="操作类型" prop="handle_type" v-if="false">
          <el-input v-model="setFieldPoolTableForm.handle_type" disabled></el-input>
        </el-form-item>
        <el-form-item label="字段名称" prop="field_name">
          <el-input v-model="setFieldPoolTableForm.field_name"></el-input>
        </el-form-item>
        <el-form-item label="字段节点路径" prop="field_node">
          <el-input v-model="setFieldPoolTableForm.field_node"></el-input>
        </el-form-item>
        <el-form-item label="Pool字段名称" prop="pool_field">
          <el-input v-model="setFieldPoolTableForm.pool_field"></el-input>
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="editSetFieldPoolDialogVisible = false">取 消</el-button>
        <el-button type="primary" @click="saveEditSetFieldPool">确 定</el-button>
      </span>
    </el-dialog>

    <!-- 断言 -->
    <!-- 新增 字段断言 -->
    <el-dialog
      title="新增字段断言"
      :visible.sync="addFieldAssertDialogVisible"
      width="50%"
      center @close="addFieldAssertDialogClose"
      :close-on-click-modal="false">
      <el-form label-width="120px" :model="fieldAssertTableForm"
        :rules="fieldAssertTableFormRules" ref="fieldAssertTableFormRef">
        <el-form-item label="接口实例ID" prop="inc_id" v-if="false">
          <el-input v-model="fieldAssertTableForm.inc_id"></el-input>
        </el-form-item>
        <el-form-item label="字段归属" prop="field_owner">
          <el-select v-model="fieldAssertTableForm.field_owner" placeholder="请选择">
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
          <el-input v-model="fieldAssertTableForm.field_name"></el-input>
        </el-form-item>
        <el-form-item label="字段节点路径" prop="field_node">
          <el-input v-model="fieldAssertTableForm.field_node"></el-input>
        </el-form-item>
        <el-form-item label="断言类型" prop="assert_type">
          <el-select v-model="fieldAssertTableForm.assert_type" placeholder="请选择">
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
          <el-input v-model="fieldAssertTableForm.field_value"></el-input>
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="addFieldAssertDialogVisible = false">取 消</el-button>
        <el-button type="primary" @click="saveFieldAssert">确 定</el-button>
      </span>
    </el-dialog>

    <!-- 删除 -->
    <el-dialog
      title="提示"
      :visible.sync="deleteFieldAssertDialogVisible"
      width="30%"
      @close="deleteFieldAssertDialogClose"
      :close-on-click-modal="false">
      <span>请确认是否删除？</span>
      <span slot="footer" class="dialog-footer">
        <el-button @click="deleteFieldAssertDialogVisible = false">取 消</el-button>
        <el-button type="primary" @click="deleteFieldAssert">确 定</el-button>
      </span>
    </el-dialog>

    <!-- 修改 字段断言 -->
    <el-dialog
      title="修改字段断言"
      :visible.sync="editFieldAssertDialogVisible"
      width="50%"
      center @close="editFieldAssertDialogClose"
      :close-on-click-modal="false">
      <el-form label-width="120px" :model="fieldAssertTableForm"
        :rules="fieldAssertTableFormRules" ref="fieldAssertTableFormRef">
        <el-form-item label="接口实例ID" prop="inc_id" v-if="false">
          <el-input v-model="fieldAssertTableForm.inc_id"></el-input>
        </el-form-item>
        <el-form-item label="字段归属" prop="field_owner">
          <el-select v-model="fieldAssertTableForm.field_owner" placeholder="请选择">
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
          <el-input v-model="fieldAssertTableForm.field_name"></el-input>
        </el-form-item>
        <el-form-item label="字段节点路径" prop="field_node">
          <el-input v-model="fieldAssertTableForm.field_node"></el-input>
        </el-form-item>
        <el-form-item label="断言类型" prop="assert_type">
          <el-select v-model="fieldAssertTableForm.assert_type" placeholder="请选择">
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
          <el-input v-model="fieldAssertTableForm.field_value"></el-input>
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="editFieldAssertDialogVisible = false">取 消</el-button>
        <el-button type="primary" @click="saveEditFieldAssert">确 定</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
  export default {
    data() {
      return {
        baseurl: this.$root.URL + '/instance/',
        baseurl_intf: this.$root.URL + '/interfaceconfig/',
        baseurl_fieldinit: this.$root.URL + '/fieldinit/',
        baseurl_fieldpool: this.$root.URL + '/fieldpool/',
        baseurl_fieldassert: this.$root.URL + '/fieldassert/',
        // 搜索
        queryInfo: {
          case_name: '',
          curpage: 1,
          pagesize: 10
        },
        total: 0,
        //列表
        tableData: [],
        // 增加
        addDialogVisible: false,
        instanceForm: {
          intf_id: '',
          interface_name: '',
          interface_path: '',
          case_name: '',
          case_description: '',
          is_selected: 0,
          remark: '',
        },
        idValue: [],
        interfaceList: [],
        addInstanceRules: {
          intf_id: [
            {
              required: true, message: '接口ID不能为空', trigger: 'blur'
            }
          ],
          interface_name: [
            {
              required: true, message: '接口名称不能为空', trigger: 'blur'
            }
          ],
          interface_path: [
            {
              required: true, message: '接口地址不能为空', trigger: 'blur'
            }
          ],
          case_name: [
            {
              required: true, message: '实例名称不能为空', trigger: 'blur'
            },
            {
              min: 0, max: 50, message: '0~50个字符', trigger: 'blur'
            }
          ],
          case_description: [
            {
              required: false
            },
            {
              min: 0, max: 100, message: '1~100个字符', trigger: 'blur'
            }
          ],
          is_selected: [
            {
              required: true, message: '是否默认不能为空', trigger: 'blur'
            }
          ],
          remark: [
            {
              required: false
            },
            {
              min: 1, max: 100, message: '1~100个字符', trigger: 'blur'
            }
          ]
        },

        // 修改
        editDialogVisible: false,
        editUrl: '',
        updateCount: 0,
        // 删除
        deleteDialogVisible: false,
        deleteUrl: '',
        case_id: null,

        // 配置接口实例
        instanceConfigDialogVisible: false,
        activeNames: ['3','4','5'],
        instanceConfigForm: {
          id: null,
          intf_id: null,
          interface_name: '',
          interface_path: '',
          case_name: '',
          case_description: '',
          is_selected: 0,
          remark: '',
        },
        // 实例字段初始化配置
        instanceUpdateCount: 0,
        fieldInitTab: 'header',
        // 初始化字段 header
        addHeaderFieldInitDialogVisible: false,
        headerFieldInitList: [],
        headerFieldInitTableForm: {
          inc_id: null,
          field_owner: '',
          field_name: '',
          field_node: '',
          field_value: ''
        },
        headerFieldInitTableFormRules: {
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
          field_value: [
            {
              required: false
            }
          ],
        },
        // header edit
        editHeaderFieldInitDialogVisible: false,
        headerFieldInitDialogUpdateCount: 0,
        editHeaderFieldInitUrl: '',
        // header delete
        deleteHeaderFieldInitDialogVisible: false,
        deleteHeaderFieldInitUrl: '',

        // 初始化字段 body
        addBodyFieldInitDialogVisible: false,
        bodyFieldInitList: [],

        bodyFieldInitTableForm: {
          inc_id: null,
          field_owner: '',
          field_name: '',
          field_node: '',
          field_value: ''
        },
        bodyFieldInitTableFormRules: {
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
          field_value: [
            {
              required: false
            }
          ],
        },
        // body edit
        editBodyFieldInitDialogVisible: false,
        bodyFieldInitDialogUpdateCount: 0,
        editBodyFieldInitUrl: '',
        // body delete
        deleteBodyFieldInitDialogVisible: false,
        deleteBodyFieldInitUrl: '',

        // ------------POOL-----------------------
        field_owner: [
          {
            value: 'body',
            label: '请求体'
          },
          {
            value: 'header',
            label: '请求头'
          },
        ],
        // 从pool中读取
        FieldPoolTab: 'get',
        // 新增
        addGetFieldPoolDialogVisible: false,
        getFieldPoolList: [],
        fieldPoolTableForm: {
          inc_id: null,
          field_owner: '',
          handle_type: '',
          field_name: '',
          field_node: '',
          pool_field: ''
        },
        fieldPoolTableFormRules: {
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
          pool_field: [
            {
              required: true, message: 'Pool字段名称不能为空', trigger: 'blur'
            }
          ],
        },
        // get edit
        editGetFieldPoolDialogVisible: false,
        getFieldPoolDialogUpdateCount: 0,
        editGetFieldPoolUrl: '',
        // get delete
        deleteGetFieldPoolDialogVisible: false,
        deleteGetFieldPoolUrl: '',

        // 初始化字段 set
        addSetFieldPoolDialogVisible: false,
        setFieldPoolList: [],

        setFieldPoolTableForm: {
          inc_id: null,
          field_owner: '',
          handle_type: '',
          field_name: '',
          field_node: '',
          pool_field: ''
        },
        setFieldPoolTableFormRules: {
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
          pool_field: [
            {
              required: true, message: 'Pool字段名称不能为空', trigger: 'blur'
            }
          ],
        },
        // set edit
        editSetFieldPoolDialogVisible: false,
        setFieldPoolDialogUpdateCount: 0,
        editSetFieldPoolUrl: '',
        // set delete
        deleteSetFieldPoolDialogVisible: false,
        deleteSetFieldPoolUrl: '',

        // ----------断言---------------
        // 初始化字段 assert
        addFieldAssertDialogVisible: false,
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
        fieldAssertList: [],
        fieldAssertTableForm: {
          inc_id: null,
          field_owner: 'res_body',
          field_name: '',
          field_node: '',
          assert_type: '',
          field_value: ''
        },
        fieldAssertTableFormRules: {
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
        // assert edit
        editFieldAssertDialogVisible: false,
        fieldAssertDialogUpdateCount: 0,
        editFieldAssertUrl: '',
        // assert delete
        deleteFieldAssertDialogVisible: false,
        deleteFieldAssertUrl: '',
      }
    },
    created() {
      this.getInstanceList()
      this.getSelected()
    },
    methods: {
      // 列表
      getInstanceList: function(){
        this.$http.get(this.baseurl, {params: this.queryInfo}).then(res => {
            this.tableData = res.data.results
            this.total = res.data.total
          })
      },

      // 分页
      handleSizeChange(newsize){
        this.queryInfo.pagesize = newsize
        this.queryInfo.curpage = 1
        this.getInstanceList()

      },
      handleCurrentChange(newpage){
        this.queryInfo.curpage = newpage
        this.getInstanceList()

      },
      // 新增
      // 新增接口对话框关闭事件：重置对话框内容
      addInstanceClose: function() {
        this.$refs.addInstanceRef.resetFields()
        this.updateCount = 0
      },
      // 获取接口信息，处理显示为下拉选项
      getSelected: function() {
        this.$http.get(this.baseurl_intf).then(res => {
          // console.log(res)
          if(res.status !== 200) return
          // console.log(res.data.length)
          for(var i=0;i<res.data.length;i++){
            const value = {
              intf_id: '',
              label: ''
            }
            value.intf_id = res.data[i].id
            value.label = res.data[i].interface_name + "--" + res.data[i].interface_path
            // console.log(value)
            this.idValue.push(value)
          }
        })
      },
      // 接口ID改变，自动带出关联接口信息
      relateInterface() {
        this.$http.get(this.baseurl_intf + this.instanceForm.intf_id).then(res => {
          // console.log(res)
          if(res.status !== 200) return

          this.instanceForm.interface_name = res.data.interface_name
          this.instanceForm.interface_path = res.data.interface_path
          // console.log(this.addEnvForm)
        })
      },

      //新增接口-点击确定按钮事件
      addInstance: function(){
        // console.log(this.instanceForm)

        this.$refs.addInstanceRef.validate(valid => {
          if(!valid) return
          //发起请求
          this.$http.post(this.baseurl, this.instanceForm).then(res => {
            if(res.status !== 201) {
              this.$message.error('新增失败！')
              return
            }
            this.$message.success('新增成功！')
            this.addDialogVisible = false
            this.getInstanceList()
          })
        })
      },

      //修改
      // 监控修改对话窗关闭
      editInstanceClose: function() {
        this.$refs.editInstanceRef.resetFields()
        this.updateCount = 0
        },
      // 点击修改按钮
      async editInstanceDialog(row) {
        this.editDialogVisible = true
        const {data: res} = await this.$http.get(this.baseurl + row.id.toString())
        this.instanceForm = res
        this.editUrl = this.baseurl + row.id.toString() + '/'
      },
      //修改环境-点击确定按钮事件
      editInstance: function(){
        this.$refs.editInstanceRef.validate(valid => {
          if(!valid) return
          if(this.updateCount <= 1) {
            this.editDialogVisible = false
            return
          }
          this.$http.put(this.editUrl, this.instanceForm).then(res => {
            if(res.status !== 200) {
              this.$message.error('修改失败！')
              return
            }
            this.$message.success('修改接口实例成功！')
            this.editDialogVisible = false
            this.getInstanceList()
          })
        })
      },

      // 删除
      // 点击删除按钮事件
      deleteInstanceDialog(row){
        this.deleteDialogVisible = true
        this.case_id = row.id
        this.deleteUrl = this.baseurl + row.id.toString() + '/'
      },
      // 监听删除对话框关闭事件
      deleteInstanceClose: function() {
        this.deleteDialogVisible = false
        this.deleteUrl = ''
        this.case_id = null
      },
      // 删除-确认按钮
      async deleteInstance(){
        const {data: resd} = await this.$http.delete(this.deleteUrl)
        //关联删除
        const {data: res_fieldinit} = await this.$http.delete(this.baseurl_fieldinit + 'deletes/', {params: {inc_id: this.case_id}})
        const {data: res_fieldpool} = await this.$http.delete(this.baseurl_fieldpool + 'deletes/', {params: {inc_id: this.case_id}})
        const {data: res_fieldassert} = await this.$http.delete(this.baseurl_fieldassert + 'deletes/', {params: {inc_id: this.case_id}})

        this.$message.success('删除项目成功！')
        this.deleteDialogVisible = false
        this.getInstanceList()
      },

      // -----------------接口实例配置-------------------
      handleChange(val) {
      },
      // 接口实例配置对话框关闭
      instanceConfigDialogClose() {
        this.$refs.instanceConfigRef.resetFields()
        this.instanceUpdateCount = 0
        // 重置界面页签
        this.fieldInitTab = 'header'
        this.FieldPoolTab = 'get'
        // 重置界面表格数据
        this.headerFieldInitList = []
        this.bodyFieldInitList = []
        this.getFieldPoolList = []
        this.setFieldPoolList = []
        this.fieldAssertList = []
      },
      // 接口实例配置，点击按钮触发事件
      async instanceConfigDialog(row) {
        this.instanceConfigDialogVisible = true
        const {data: res} = await this.$http.get(this.baseurl + row.id.toString())
        // console.log(res)
        this.instanceConfigForm = res
        this.getHeaderFieldInitList()
        this.showGetFieldPoolList()
        this.getFieldAssertList()
      },
      // 点击确认按钮，保存
      saveInstanceConfig() {
        this.instanceConfigDialogVisible = false
      },
      // ----------------字段初始化 header-----------------
      fieldInitTabChange(val) {
        // console.log(val.name)
        if(val.name == 'header'){
          this.getHeaderFieldInitList()
        }else{
          this.getBodyFieldInitList()
        }
      },
      // 获取list
      getHeaderFieldInitList() {
        this.$http.get(this.baseurl_fieldinit, {params: {inc_id: this.instanceConfigForm.id, field_owner: this.fieldInitTab}}).then(res => {
          // console.log(res)
          this.headerFieldInitList = res.data
        })
      },
      // 新增
      addHeaderFieldInitDialogClose() {
        this.$refs.headerFieldInitTableFormRef.resetFields()
        this.headerFieldInitDialogUpdateCount = 0
      },
      addHeaderFieldInitDialogClick() {
        this.addHeaderFieldInitDialogVisible = true
        this.headerFieldInitTableForm.inc_id = this.instanceConfigForm.id
        this.headerFieldInitTableForm.field_owner = this.fieldInitTab
        // console.log(this.headerFieldInitTableForm)
      },
      saveHeaderFieldInit() {
        this.$refs.headerFieldInitTableFormRef.validate(valid => {
          if(!valid) return
          this.$http.post(this.baseurl_fieldinit, this.headerFieldInitTableForm).then(res => {
            if(res.status !== 201) {
              this.$message.error('新增字段失败！')
              return
            }
            this.$message.success('新增字段成功！')
            this.addHeaderFieldInitDialogVisible = false
            this.getHeaderFieldInitList()
          })
        })
      },
      // header edit监控对话窗关闭
      editHeaderFieldInitDialogClose() {
        this.$refs.headerFieldInitTableFormRef.resetFields()
        this.headerFieldInitDialogUpdateCount = 0
      },
      // 点击修改按钮
      async editHeaderFieldInitDialog(row) {
        this.editHeaderFieldInitDialogVisible = true
        const {data: res} = await this.$http.get(this.baseurl_fieldinit + row.id.toString())
        this.headerFieldInitTableForm = res
        console.log(this.headerFieldInitTableForm)
        this.editHeaderFieldInitUrl = this.baseurl_fieldinit + row.id.toString() + '/'
      },
      // 修改保存
      saveEditHeaderFieldInit() {
        // console.log(this.headerFieldInitTableForm)
        this.$refs.headerFieldInitTableFormRef.validate(valid => {
          if(!valid) return
          if(this.headerFieldInitDialogUpdateCount <= 1) {
            this.editHeaderFieldInitDialogVisible = false
            return
          }
          this.$http.put(this.editHeaderFieldInitUrl, this.headerFieldInitTableForm).then(res => {
            if(res.status !== 200) {
              this.$messages.error('修改字段失败！')
              return
            }
            this.$message.success('修改字段成功！')
            this.editHeaderFieldInitDialogVisible = false
            this.getHeaderFieldInitList()
          })
        })
      },

      // header 删除
      deleteHeaderFieldInitDialog(row) {
        this.deleteHeaderFieldInitDialogVisible = true
        this.deleteHeaderFieldInitUrl = this.baseurl_fieldinit + row.id.toString() + '/'
      },
      deleteHeaderFieldInitDialogClose() {
        this.deleteHeaderFieldInitUrl = ''
      },
      deleteHeaderFieldInit() {
        this.$http.delete(this.deleteHeaderFieldInitUrl).then(res => {
          if(res.status !== 204) {
            this.$message.error('删除字段失败！')
            return
          }
          this.$message.success('删除字段成功！')
          this.deleteHeaderFieldInitDialogVisible = false
          this.getHeaderFieldInitList()
        })
      },

      // 初始化字段 body
      // 获取list
      getBodyFieldInitList() {
        this.$http.get(this.baseurl_fieldinit, {params: {inc_id: this.instanceConfigForm.id, field_owner: this.fieldInitTab}}).then(res => {
          // console.log(res)
          this.bodyFieldInitList = res.data
        })
      },
      addBodyFieldInitDialogClick() {
        this.addBodyFieldInitDialogVisible = true
        this.bodyFieldInitTableForm.inc_id = this.instanceConfigForm.id
        this.bodyFieldInitTableForm.field_owner = this.fieldInitTab
      },
      addBodyFieldInitDialogClose() {
        this.$refs.bodyFieldInitTableFormRef.resetFields()
        this.bodyFieldInitDialogUpdateCount = 0
      },
      saveBodyFieldInit() {
        this.$refs.bodyFieldInitTableFormRef.validate(valid => {
          if(!valid) return
          this.$http.post(this.baseurl_fieldinit, this.bodyFieldInitTableForm).then(res => {
            if(res.status !== 201) {
              this.$message.error('新增字段失败！')
              return
            }
            this.$message.success('新增字段成功！')
            this.addBodyFieldInitDialogVisible = false
            this.getBodyFieldInitList()
          })
        })
      },
      // body edit监控对话窗关闭
      editBodyFieldInitDialogClose() {
        this.$refs.bodyFieldInitTableFormRef.resetFields()
        this.bodyFieldInitDialogUpdateCount = 0
      },
      // 点击修改按钮
      async editBodyFieldInitDialog(row) {
        this.editBodyFieldInitDialogVisible = true
        const {data: res} = await this.$http.get(this.baseurl_fieldinit + row.id.toString())
        this.bodyFieldInitTableForm = res
        // console.log(this.bodyFieldInitTableForm)
        this.editBodyFieldInitUrl = this.baseurl_fieldinit + row.id.toString() + '/'
      },
      // 修改保存
      saveEditBodyFieldInit() {
        // console.log(this.headerFieldInitTableForm)
        this.$refs.bodyFieldInitTableFormRef.validate(valid => {
          if(!valid) return
          if(this.bodyFieldInitDialogUpdateCount <= 1) {
            this.editBodyFieldInitDialogVisible = false
            return
          }
          this.$http.put(this.editBodyFieldInitUrl, this.bodyFieldInitTableForm).then(res => {
            if(res.status !== 200) {
              this.$message.error('修改接口失败！')
              return
            }
            this.$message.success('修改字段成功！')
            this.editBodyFieldInitDialogVisible = false
            this.getBodyFieldInitList()
          })
        })
      },

      // header 删除
      deleteBodyFieldInitDialog(row) {
        this.deleteBodyFieldInitDialogVisible = true
        this.deleteBodyFieldInitUrl = this.baseurl_fieldinit + row.id.toString() + '/'
      },
      deleteBodyFieldInitDialogClose() {
        this.deleteBodyFieldInitUrl = ''
      },
      deleteBodyFieldInit() {
        this.$http.delete(this.deleteBodyFieldInitUrl).then(res => {
          if(res.status !== 204) {
            this.$message.error('删除字段失败！')
            return
          }
          this.$message.success('删除字段成功！')
          this.deleteBodyFieldInitDialogVisible = false
          this.getBodyFieldInitList()
        })
      },

      // ---------POOL-------------
      // ---字段初始化 header--
      getFieldPoolTabChange(val) {
        // console.log(val.name)
        if(val.name == 'get'){
          this.showGetFieldPoolList()
        }else{
          this.showSetFieldPoolList()
        }
      },
      // 获取list
      showGetFieldPoolList() {
        this.$http.get(this.baseurl_fieldpool, {params: {inc_id: this.instanceConfigForm.id, handle_type: this.FieldPoolTab}}).then(res => {
          // console.log(res)
          this.getFieldPoolList = res.data
        })
      },
      // 新增
      addGetFieldPoolDialogClose() {
        this.$refs.fieldPoolTableFormRef.resetFields()
        this.getFieldPoolDialogUpdateCount = 0
      },
      addGetFieldPoolDialogClick() {
        this.addGetFieldPoolDialogVisible = true
        this.fieldPoolTableForm.inc_id = this.instanceConfigForm.id
        this.fieldPoolTableForm.handle_type = this.FieldPoolTab
        // console.log(this.fieldPoolTableForm)
      },
      saveGetFieldPool() {
        this.fieldPoolTableForm.handle_type = 'get'
        this.$refs.fieldPoolTableFormRef.validate(valid => {
          if(!valid) return
          this.$http.post(this.baseurl_fieldpool, this.fieldPoolTableForm).then(res => {
            if(res.status !== 201) {
              this.$message.error('新增失败！')
              return
            }
            this.$message.success('新增成功！')
            this.addGetFieldPoolDialogVisible = false
            this.showGetFieldPoolList()
          })
        })
      },
      // header edit监控对话窗关闭
      editGetFieldPoolDialogClose() {
        this.$refs.fieldPoolTableFormRef.resetFields()
        this.getFieldPoolDialogUpdateCount = 0
      },
      // 点击修改按钮
      async editGetFieldPoolDialog(row) {
        this.editGetFieldPoolDialogVisible = true
        const {data: res} = await this.$http.get(this.baseurl_fieldpool + row.id.toString())
        this.fieldPoolTableForm = res
        // console.log(this.fieldPoolTableForm)
        this.editGetFieldPoolUrl = this.baseurl_fieldpool + row.id.toString() + '/'
      },
      // 修改保存
      saveEditGetFieldPool() {
        // console.log(this.fieldPoolTableForm)
        this.$refs.fieldPoolTableFormRef.validate(valid => {
          if(!valid) return
          if(this.getFieldPoolDialogUpdateCount <= 1) {
            this.editGetFieldPoolDialogVisible = false
            return
          }
          this.$http.put(this.editGetFieldPoolUrl, this.fieldPoolTableForm).then(res => {
            if(res.status !== 200) {
              this.$message.error('修改失败！')
              return
            }
            this.$message.success('修改成功！')
            this.editGetFieldPoolDialogVisible = false
            this.showGetFieldPoolList()
          })
        })
      },

      // header 删除
      deleteGetFieldPoolDialog(row) {
        this.deleteGetFieldPoolDialogVisible = true
        this.deleteGetFieldPoolUrl = this.baseurl_fieldpool + row.id.toString() + '/'
      },
      deleteGetFieldPoolDialogClose() {
        this.deleteGetFieldPoolUrl = ''
      },
      deleteGetFieldPool() {
        this.$http.delete(this.deleteGetFieldPoolUrl).then(res => {
          if(res.status !== 204) {
            this.$message.error('删除失败！')
            return
          }
          this.$message.success('删除成功！')
          this.deleteGetFieldPoolDialogVisible = false
          this.showGetFieldPoolList()
        })
      },

      // 初始化字段 body
      // 获取list
      showSetFieldPoolList() {
        this.$http.get(this.baseurl_fieldpool, {params: {inc_id: this.instanceConfigForm.id, handle_type: this.FieldPoolTab}}).then(res => {
          // console.log(res)
          this.setFieldPoolList = res.data
        })
      },
      addSetFieldPoolDialogClick() {
        this.addSetFieldPoolDialogVisible = true
        this.setFieldPoolTableForm.inc_id = this.instanceConfigForm.id
        this.setFieldPoolTableForm.handle_type = this.FieldPoolTab
      },
      addSetFieldPoolDialogClose() {
        this.$refs.setFieldPoolTableFormRef.resetFields()
        this.setFieldPoolDialogUpdateCount = 0
      },
      saveSetFieldPool() {
        this.setFieldPoolTableForm.handle_type = 'set'
        this.$refs.setFieldPoolTableFormRef.validate(valid => {
          if(!valid) return
          this.$http.post(this.baseurl_fieldpool, this.setFieldPoolTableForm).then(res => {
            if(res.status !== 201) {
              this.$message.error('新增失败！')
              return
            }
            this.$message.success('新增成功！')
            this.addSetFieldPoolDialogVisible = false
            this.showSetFieldPoolList()
          })
        })
      },
      // body edit监控对话窗关闭
      editSetFieldPoolDialogClose() {
        this.$refs.setFieldPoolTableFormRef.resetFields()
        this.setFieldPoolDialogUpdateCount = 0
      },
      // 点击修改按钮
      async editSetFieldPoolDialog(row) {
        this.editSetFieldPoolDialogVisible = true
        const {data: res} = await this.$http.get(this.baseurl_fieldpool + row.id.toString())
        this.setFieldPoolTableForm = res
        console.log(this.setFieldPoolTableForm)
        this.editSetFieldPoolUrl = this.baseurl_fieldpool + row.id.toString() + '/'
      },
      // 修改保存
      saveEditSetFieldPool() {
        // console.log(this.fieldPoolTableForm)
        this.$refs.setFieldPoolTableFormRef.validate(valid => {
          if(!valid) return
          if(this.setFieldPoolDialogUpdateCount <= 1) {
            this.editSetFieldPoolDialogVisible = false
            return
          }
          this.$http.put(this.editSetFieldPoolUrl, this.setFieldPoolTableForm).then(res => {
            if(res.status !== 200) {
              this.$message.error('修改失败！')
              return
            }
            this.$message.success('修改字段成功！')
            this.editSetFieldPoolDialogVisible = false
            this.showSetFieldPoolList()
          })
        })
      },

      // header 删除
      deleteSetFieldPoolDialog(row) {
        this.deleteSetFieldPoolDialogVisible = true
        this.deleteSetFieldPoolUrl = this.baseurl_fieldpool + row.id.toString() + '/'
      },
      deleteSetFieldPoolDialogClose() {
        this.deleteSetFieldPoolUrl = ''
      },
      deleteSetFieldPool() {
        this.$http.delete(this.deleteSetFieldPoolUrl).then(res => {
          if(res.status !== 204) {
            this.$message.error('删除失败！')
            return
          }
          this.$message.success('删除字段成功！')
          this.deleteSetFieldPoolDialogVisible = false
          this.showSetFieldPoolList()
        })
      },

      // ------------断言----------------
      // 获取list
      getFieldAssertList() {
        this.$http.get(this.baseurl_fieldassert, {params: {inc_id: this.instanceConfigForm.id}}).then(res => {
          // console.log(res)
          this.fieldAssertList = res.data
        })
      },
      // 新增
      addFieldAssertDialogClose() {
        this.$refs.fieldAssertTableFormRef.resetFields()
        this.fieldAssertDialogUpdateCount = 0
      },
      addFieldAssertDialogClick() {
        this.addFieldAssertDialogVisible = true
        this.fieldAssertTableForm.inc_id = this.instanceConfigForm.id
        // console.log(this.fieldAssertTableForm)
      },
      saveFieldAssert() {
        this.$refs.fieldAssertTableFormRef.validate(valid => {
          if(!valid) return
          this.$http.post(this.baseurl_fieldassert, this.fieldAssertTableForm).then(res => {
            if(res.status !== 201) {
              this.$message.error('新增失败！')
              return
            }
            this.$message.success('新增字段成功！')
            this.addFieldAssertDialogVisible = false
            this.getFieldAssertList()
          })
        })
      },
      // header edit监控对话窗关闭
      editFieldAssertDialogClose() {
        this.$refs.fieldAssertTableFormRef.resetFields()
        this.fieldAssertDialogUpdateCount = 0
      },
      // 点击修改按钮
      async editFieldAssertDialog(row) {
        this.editFieldAssertDialogVisible = true
        const {data: res} = await this.$http.get(this.baseurl_fieldassert + row.id.toString())
        this.fieldAssertTableForm = res
        console.log(this.fieldAssertTableForm)
        this.editFieldAssertUrl = this.baseurl_fieldassert + row.id.toString() + '/'
      },
      // 修改保存
      saveEditFieldAssert() {
        // console.log(this.fieldAssertTableForm)
        this.$refs.fieldAssertTableFormRef.validate(valid => {
          if(!valid) return
          if(this.fieldAssertDialogUpdateCount <= 1) {
            this.editFieldAssertDialogVisible = false
            return
          }
          this.$http.put(this.editFieldAssertUrl, this.fieldAssertTableForm).then(res => {
            if(res.status !== 200) {
              this.$message.error('修改失败！')
              return
            }
            this.$message.success('修改字段成功！')
            this.editFieldAssertDialogVisible = false
            this.getFieldAssertList()
          })
        })
      },

      // header 删除
      deleteFieldAssertDialog(row) {
        this.deleteFieldAssertDialogVisible = true
        this.deleteFieldAssertUrl = this.baseurl_fieldassert + row.id.toString() + '/'
      },
      deleteFieldAssertDialogClose() {
        this.deleteFieldAssertUrl = ''
      },
      deleteFieldAssert() {
        this.$http.delete(this.deleteFieldAssertUrl).then(res => {
          if(res.status !== 204) {
            this.$message.error('删除失败！')
            return
          }
          this.$message.success('删除成功！')
          this.deleteFieldAssertDialogVisible = false
          this.getFieldAssertList()
        })
        
      },
    },
    watch: {
      // 监听项目信息是否有修改，如果没有修改 updateCount>1。 (打开修改页面时会自动加1，后续每一个修改都会加1）
      // 监控接口实例修改
      instanceForm: {
           handler (val) {
             if (val) {
               this.updateCount++
               // console.log(this.updateCount)
          }
        },
        deep: true
      },
      // 监控接口实例配置（暂无作用）
      instanceConfigForm: {
           handler (val) {
             if (val) {
               this.instanceUpdateCount++
               // console.log(this.updateCount)
          }
        },
        deep: true
      },
      // 监控header、body初始化字段修改
      headerFieldInitTableForm: {
           handler (val) {
             if (val) {
               this.headerFieldInitDialogUpdateCount ++
               // console.log(this.updateCount)
          }
        },
        deep: true
      },
      // 监控header、body初始化字段修改
      bodyFieldInitTableForm: {
           handler (val) {
             if (val) {
               this.bodyFieldInitDialogUpdateCount ++
               // console.log(this.updateCount)
          }
        },
        deep: true
      },
      // 监控pool初始化字段修改
      fieldPoolTableForm: {
           handler (val) {
             if (val) {
               this.getFieldPoolDialogUpdateCount ++
               // console.log(this.updateCount)
          }
        },
        deep: true
      },
      // 监控pool初始化字段修改
      setFieldPoolTableForm: {
           handler (val) {
             if (val) {
               this.setFieldPoolDialogUpdateCount ++
               // console.log(this.updateCount)
          }
        },
        deep: true
      },
      // 监控assert初始化字段修改
      fieldAssertTableForm: {
           handler (val) {
             if (val) {
               this.fieldAssertDialogUpdateCount ++
               // console.log(this.updateCount)
          }
        },
        deep: true
      }
    }
  }
</script>

<style>
</style>
