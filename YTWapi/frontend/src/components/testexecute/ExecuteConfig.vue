<template>
  <div>
    <el-breadcrumb separator-class="el-icon-arrow-right">
      <el-breadcrumb-item :to="{ path: '/home' }">首页</el-breadcrumb-item>
      <el-breadcrumb-item>执行管理</el-breadcrumb-item>
      <el-breadcrumb-item>执行设置</el-breadcrumb-item>
    </el-breadcrumb>

    <!-- 卡片区域 -->
    <el-card class="box-card">
      <el-form :inline="true" :model="queryInfo" class="demo-form-inline" size="mini">
        <el-form-item label="执行任务名称">
          <el-input v-model="queryInfo.execute_name" placeholder="执行任务名称" clearable></el-input>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="getExecuteConfigList">查询</el-button>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="addExecuteConfigDialogClick">添加</el-button>
        </el-form-item>
      </el-form>

      <!-- 列表数据区 -->
        <template>
          <el-table :data="executeConfigData" border stripe>
            <el-table-column type="index" label="#"></el-table-column>
            <el-table-column prop="execute_name" label="执行任务名称"></el-table-column>
            <el-table-column prop="tsid" label="测试集ID" v-if="false"></el-table-column>
            <el-table-column prop="suite_name" label="测试集名称"></el-table-column>
            <el-table-column prop="remark" label="说明"></el-table-column>
            <el-table-column label="操作">
              <template slot-scope="scope">
                <el-tooltip effect="dark" content="修改" placement="top" :enterable="false">
                  <el-button type="primary" icon="el-icon-edit" size="mini" @click="editExecuteConfigDialog(scope.row)"></el-button>
                </el-tooltip>
                <el-tooltip effect="dark" content="删除" placement="top" :enterable="false">
                  <el-button type="danger" icon="el-icon-delete" size="mini" @click="deleteExecuteConfigDialog(scope.row)"></el-button>
                </el-tooltip>
                <el-tooltip effect="dark" content="执行任务" placement="top" :enterable="false">
                  <el-button type="success" size="mini" @click="executeTask(scope.row)">执行</el-button>
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
          :page-sizes="[10, 20, 50, 100]"
          :page-size="queryInfo.pagesize"
          layout="total, sizes, prev, pager, next, jumper"
          :total="total">
        </el-pagination>
    </el-card>

    <!-- 新增对话框 -->
    <el-dialog
      title="新增执行任务"
      :visible.sync="addExecuteConfigDialogVisible"
      width="50%"
      center
      :close-on-click-modal="false"
      @close="addExecuteConfigDialogClose">
      <el-form :model="executeConfigForm" status-icon :rules="executeConfigFormRules" ref="executeConfigFormRef" label-width="120px">
        <el-form-item label="执行任务名称" prop="execute_name">
          <el-input v-model="executeConfigForm.execute_name" placeholder="请输入"></el-input>
        </el-form-item>
        <el-form-item label="测试集" prop="tsid">
          <el-select v-model="executeConfigForm.tsid" placeholder="请选择">
             <el-option
               v-for="item,index in tsOptions"
               :key="index"
               :value="item.tsid"
               :label="item.label">
             </el-option>
           </el-select>
        </el-form-item>
        <el-form-item label="说明" prop="remark">
          <el-input type="textarea" v-model="executeConfigForm.remark"></el-input>
        </el-form-item>

        <el-card>
          <el-cascader
            placeholder="选择环境"
            v-model="relate_id"
            :options="envOptions"
            :props="{ expandTrigger: 'hover' }"
            @change="envHandleChange"
            clearable
            size="small"
            style="width: 87%">
          </el-cascader>
          <el-row :gutter="24">
            <el-col :span="21">
              <el-input v-model="addExecuteEnvForm.address" placeholder="环境地址,自动带出" disabled size="small"></el-input>
            </el-col>
            <el-col :span="3">
              <el-button type="primary" @click="addExecuteEnvClick" size="small">增加</el-button>
            </el-col>
          </el-row>

          <el-table :data="executeEnvData" border stripe size="small">
            <el-table-column type="index" label="#"></el-table-column>
            <el-table-column prop="eid" label="执行任务ID" v-if="false"></el-table-column>
            <el-table-column prop="env_id" label="环境ID" v-if="false"></el-table-column>
            <el-table-column prop="env_name" label="环境名称"></el-table-column>
            <el-table-column prop="address" label="地址"></el-table-column>
            <el-table-column label="操作" min-width="40px">
              <template slot-scope="scope">
                <el-tooltip effect="dark" content="删除" placement="top" :enterable="false" >
                  <el-button id="index" type="danger" icon="el-icon-delete" size="mini" @click="addDeleteExecuteEnvDialog(scope.$index)"></el-button>
                </el-tooltip>
              </template>
            </el-table-column>
          </el-table>
        </el-card>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="addExecuteConfigDialogVisible = false">取 消</el-button>
        <el-button type="primary" @click="addExecuteConfigSave">确 定</el-button>
      </span>
    </el-dialog>

    <!-- 修改对话框 -->
    <el-dialog
      title="修改执行任务"
      :visible.sync="editExecuteConfigDialogVisible"
      width="50%"
      center
      :close-on-click-modal="false"
      @close="editExecuteConfigDialogClose">
      <el-form :model="executeConfigForm" status-icon :rules="executeConfigFormRules" ref="executeConfigFormRef" label-width="120px">
        <el-form-item label="执行任务名称" prop="execute_name">
          <el-input v-model="executeConfigForm.execute_name" placeholder="请输入"></el-input>
        </el-form-item>
        <el-form-item label="测试集" prop="tsid">
          <el-select v-model="executeConfigForm.tsid" placeholder="请选择">
             <el-option
               v-for="item,index in tsOptions"
               :key="index"
               :value="item.tsid"
               :label="item.label">
             </el-option>
           </el-select>
        </el-form-item>
        <el-form-item label="说明" prop="remark">
          <el-input type="textarea" v-model="executeConfigForm.remark"></el-input>
        </el-form-item>

        <el-card>
          <el-cascader
            placeholder="选择环境"
            v-model="relate_id"
            :options="envOptions"
            :props="{ expandTrigger: 'hover' }"
            @change="envHandleChange"
            size="small"
            style="width: 87%"
            clearable>
          </el-cascader>
          <el-row :gutter="24">
            <el-col :span="21">
              <el-input v-model="addExecuteEnvForm.address" placeholder="环境地址,自动带出" disabled size="small"></el-input>
            </el-col>
            <el-col :span="3">
              <el-button type="primary" @click="EditAddExecuteEnvClick" size="small">增加</el-button>
            </el-col>
          </el-row>

          <el-table :data="executeEnvData" border stripe size="small">
            <el-table-column type="index" label="#"></el-table-column>
            <el-table-column prop="eid" label="执行任务ID" v-if="false"></el-table-column>
            <el-table-column prop="env_id" label="环境ID" v-if="false"></el-table-column>
            <el-table-column prop="env_name" label="环境名称"></el-table-column>
            <el-table-column prop="address" label="地址"></el-table-column>
            <el-table-column label="操作" min-width="40px">
              <template slot-scope="scope">
                <el-tooltip effect="dark" content="删除" placement="top" :enterable="false" >
                  <el-button type="danger" icon="el-icon-delete" size="mini" @click="EditDeleteExecuteEnvDialog(scope.row)"></el-button>
                </el-tooltip>
              </template>
            </el-table-column>
          </el-table>
        </el-card>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="editExecuteConfigDialogVisible = false">取 消</el-button>
        <el-button type="primary" @click="editExecuteConfigSave">确 定</el-button>
      </span>
    </el-dialog>

    <!-- 删除 -->
    <el-dialog
      title="提示"
      :visible.sync="deleteExecuteConfigDialogVisible"
      width="30%"
      @close="deleteExecuteConfigDialogClose"
      :close-on-click-modal="false">
      <span>请确认是否删除？</span>
      <span slot="footer" class="dialog-footer">
        <el-button @click="deleteExecuteConfigDialogVisible = false">取 消</el-button>
        <el-button type="primary" @click="deleteExecuteConfigSure">确 定</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
  export default {
    data() {
      return {
        baseUrl: this.$root.URL + '/executeconfig/',
        baseUrl_env: this.$root.URL + '/executeenv/',
        baseUrl_testsuite: this.$root.URL + '/testsuite/',
        baseUrl_executetask: this.$root.URL + '/executetask/',
        baseUrl_task: this.$root.URL + '/task/',
        // 查询、分页
        queryInfo: {
          execute_name: '',
          curpage: 1,
          pagesize: 10
        },
        total: 0,
        // 列表
        executeConfigData: [],
        // 新增
        addExecuteConfigDialogVisible: false,
        tsOptions: [],
        executeConfigForm: {
          execute_name: '',
          tsid: null,
          remark: ''
        },
        executeConfigFormRules: {
          execute_name: [
            {
              required: true, message: '请输入执行任务名称', trigger: 'blur'
            },
            {
              min: 1, max: 255, message: '执行任务名称在1~255个字符之间', trigger: 'blur'
            }
          ],
          tsid:[
            {
              required: true, message: '请选择测试集', trigger: 'blur'
            },
          ]
        },
        // 环境设置
        executeEnvData: [],
        envOptions: [],
        relate_id: null,
        addExecuteEnvForm: {
          eid: null,
          env_id: null,
          env_name: '',
          address: ''
        },

        // 修改
        editExecuteConfigDialogVisible: false,
        editExecuteConfigID: null,

        // 删除
        deleteExecuteConfigDialogVisible: false,
        deleteExecuteConfigID: null,

      }
    },
    created() {
      this.getExecuteConfigList()
    },
    methods: {
      // 列表
      getExecuteConfigList() {
        this.$http.get(this.baseUrl, {params: this.queryInfo}).then(res => {
          if(res.status !== 200) return
          this.executeConfigData = res.data.results
          this.total = res.data.total
        })
      },
      // 分页
      handleSizeChange(newsize){
        this.queryInfo.pagesize = newsize
        this.queryInfo.curpage = 1
        this.getExecuteConfigList()
      },
      handleCurrentChange(newpage){
        this.queryInfo.curpage = newpage
        this.getExecuteConfigList()

      },

      // 新增
      // 获取测试集下拉选项
      getTsOptions() {
        this.$http.get(this.baseUrl_testsuite).then(res => {
          if(res.status !== 200) return
          for(var i=0;i<res.data.length;i++) {
            const value = {
              tsid: null,
              label: ''
            }
            value.tsid = res.data[i].id
            value.label = res.data[i].suite_name
            this.tsOptions.push(value)
          }
        })
      },
      // 点击添加按钮触发事件
      addExecuteConfigDialogClick() {
        this.addExecuteConfigDialogVisible = true
        this.getTsOptions()
        this.getProjectEnvList()
      },
      // 关闭新增对话框触发事件
      addExecuteConfigDialogClose() {
        this.$refs.executeConfigFormRef.resetFields()
        // 清空下拉
        this.tsOptions = []
        this.envOptions = []
        // 清空环境列表
        this.executeEnvData = []
        this.relate_id = null
        this.addExecuteEnvForm = {
          eid: null,
          env_id: null,
          env_name: '',
          address: ''
        }
      },
      // 新增 保存
      addExecuteConfigSave() {
        this.$refs.executeConfigFormRef.validate(valid => {
          if(!valid) return
          // 判断是否选择了环境
          if(!this.executeEnvData.length) {
            this.$message.error('未选择执行环境！')
            return
          }
          // 新增执行任务
          this.$http.post(this.baseUrl, this.executeConfigForm).then(res => {
            if(res.status !== 201) {
              this.$message.error('新增失败！')
              return
            }
            // 新增执行任务环境
            for(let i=0;i<this.executeEnvData.length;i++) {
              this.executeEnvData[i].eid = res.data.id
              this.$http.post(this.baseUrl_env, this.executeEnvData[i]).then(rese => {
                if(rese.status !== 201) {
                  this.$message.error('新增执行任务成功，但执行环境[' + this.executeEnvData[i].env_name + ']添加失败！')
                }
              })
            }
            this.$message.success('新增成功！')
            this.addExecuteConfigDialogVisible = false
            this.getExecuteConfigList()
          })

        })
      },
      // 环境 选择环境下拉选项值获取
      getProjectEnvList() {
        // 获取项目名称列表
        this.$http.get(this.$root.URL + '/projectconfig/').then(resp => {
          if(resp.status !== 200) return
          if(resp.data.length == 0) return
          // console.log(resp.data)
          // 添加进option列表
          for(var i=0;i<resp.data.length;i++) {
            // 获取项目对应的所有环境
            const childOption = []
            this.$http.get(this.$root.URL + '/envconfig/', {params: {pid: resp.data[i].id}}).then(rese => {
              if(rese.status !== 200) return
              if(rese.data.length == 0) return
              // console.log(rese.data)
              for(var m=0;m<rese.data.length;m++){
                childOption.push({
                  value: rese.data[m].id,
                  label: rese.data[m].env_name
                })
              }
            })
            // 将项目及环境添加到option
            if(childOption) {
              this.envOptions.push({
                value: resp.data[i].id,
                label: resp.data[i].project_name,
                children: childOption
              })
            }else{
              this.envOptions.push({
                value: resp.data[i].id,
                label: resp.data[i].project_name
              })
            }
          }
          // console.log(this.envOptions)
        })
      },
      // 选择环境触发
      envHandleChange(val) {
        this.addExecuteEnvForm.env_id = val[1]
        const url = this.$root.URL + '/envconfig/' + this.addExecuteEnvForm.env_id + '/'
        this.$http.get(url).then(resq => {
          if(resq.status !== 200) return
          console.log(resq)
          this.addExecuteEnvForm.env_name = resq.data.env_name
          this.addExecuteEnvForm.address = resq.data.address
        })

      },
      // 环境 增加
      addExecuteEnvClick() {
        if(!this.addExecuteEnvForm.env_id) {
          this.$message.info('请先选择环境！')
          return
        }
        this.executeEnvData.push(this.addExecuteEnvForm)
        // 清空
        this.relate_id = []
        this.addExecuteEnvForm = {
          eid: null,
          env_id: null,
          env_name: '',
          address: ''
        }
      },
      // 新增界面 环境删除
      addDeleteExecuteEnvDialog(index) {
        // console.log(index)
        this.executeEnvData.splice(index, 1)
      },

      // 修改界面 环境列表
      getExecuteEnvList() {
        this.$http.get(this.baseUrl_env, {params: {eid: this.editExecuteConfigID}}).then(res => {
          if(res.status !== 200) return
          this.executeEnvData = res.data
        })
      },

      // 修改
      // 点击修改按钮触发
      async editExecuteConfigDialog(row) {
        this.editExecuteConfigDialogVisible = true
        // 页面数据赋值
        const {data: res} = await this.$http.get(this.baseUrl + row.id + '/')
        this.executeConfigForm = res
        this.editExecuteConfigID = res.id
        // 环境列表刷新
        this.getExecuteEnvList()
        // 下拉列表获取
        this.getTsOptions()
        this.getProjectEnvList()
      },

      // 修改对话框关闭事件
      editExecuteConfigDialogClose() {
        this.$refs.executeConfigFormRef.resetFields()
        // 修改ID清空
        this.editExecuteConfigID
        // 清空下拉
        this.tsOptions = []
        this.envOptions = []
        // 清空环境列表
        this.executeEnvData = []
        this.relate_id = null
        this.addExecuteEnvForm = {
          eid: null,
          env_id: null,
          env_name: '',
          address: ''
        }
      },
      // 修改界面 新增环境
      EditAddExecuteEnvClick() {
        if(!this.addExecuteEnvForm.env_id) {
          this.$message.info('请先选择环境！')
          return
        }
        this.addExecuteEnvForm.eid = this.editExecuteConfigID
        this.$http.post(this.baseUrl_env, this.addExecuteEnvForm).then(res => {
          if(res.status !== 201) {
            this.$message.error('新增环境失败！')
            return
          }
          this.$message.success('新增成功！')
          this.getExecuteEnvList()
        })
        // 清空
        this.relate_id = []
        this.addExecuteEnvForm = {
          eid: null,
          env_id: null,
          env_name: '',
          address: ''
        }
      },
      // 修改界面 删除环境
      EditDeleteExecuteEnvDialog(row) {
        this.$http.delete(this.baseUrl_env + row.id + '/').then(res => {
          if(res.status !== 204) {
            this.$message.error('删除失败！')
            return
          }
          this.getExecuteEnvList()
        })
      },
      // 修改保存
      editExecuteConfigSave() {
        this.$refs.executeConfigFormRef.validate(valid => {
          if(!valid) return
          // 判断是否选择了环境
          if(!this.executeEnvData.length) {
            this.$message.error('未设置执行环境！')
            return
          }
          // 修改执行任务
          this.$http.put(this.baseUrl + this.editExecuteConfigID + '/', this.executeConfigForm).then(res => {
            if(res.status !== 200) {
              this.$message.error('修改失败！')
              return
            }
            this.$message.success('修改成功！')
            this.editExecuteConfigDialogVisible = false
            this.getExecuteConfigList()
          })

        })
      },

      // 删除环境
      deleteExecuteConfigDialog(row) {
        this.deleteExecuteConfigDialogVisible = true
        this.deleteExecuteConfigID = row.id
      },
      // 删除对话框关闭
      deleteExecuteConfigDialogClose() {
        this.deleteExecuteConfigID = ''
      },
      // 删除确认(后端默认级联删除执行环境信息)
      deleteExecuteConfigSure() {
        this.$http.delete(this.baseUrl + this.deleteExecuteConfigID + '/').then(res => {
          if(res.status !== 204) {
            this.$message.error('删除失败！')
            return
          }
          this.$message.success('删除成功！')
          this.deleteExecuteConfigDialogVisible = false
          this.getExecuteConfigList()
        })
      },
      // 点击 执行
      executeTask(row) {
        // 任务管理表
        var taskForm = {
          execute_stamp: '',
          task_id: '',
          task_name: '',
          start_time: null,
          status: '',
          end_time: null
        }
        // console.log(row)
        // 发送请求,执行测试用例
        this.$http.get(this.baseUrl_executetask, {params: {eid: row.id}}).then(res => {
          if(res.status !== 200) {
            this.$message.error('系统异常，执行失败！')
            return
          }
          // 获取任务，检查是否有相同执行任务已经在队列中
          this.$http.get(this.baseUrl_task, {params: {task_name: row.execute_name}}).then(resq => {
            if(resq.status !== 200) {
              this.$message.error('系统异常，执行失败！')
              return
            }
            // console.log(resq.data)
            if(resq.data.length > 0){
              for(let i=0;i<resq.data.length;i++){
                if(resq.data[i].status == '未开始' || resq.data[i].status == '进行中'){
                  this.$message.info('系统中存在未开始或进行中的任务，相同任务不能重复执行！')
                  return
                }
              }
            }
            // 新增 任务
            // console.log(res.data)
            taskForm.task_id = res.data
            taskForm.task_name = row.execute_name
            taskForm.start_time = this.getNowFormatDate()
            taskForm.status = '未开始'
            this.$http.post(this.baseUrl_task, taskForm).then(rest => {
              if(rest.status !== 201) {
                this.$message.error('任务已启动，但系统新增该任务数据失败！')
                return
              }
              this.$message.success('任务启动成功，请到任务管理模块查看执行结果！')

            })
          })

        })
      },
      getNowFormatDate() {//获取当前时间
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

    }
  }
</script>

<style>
</style>
