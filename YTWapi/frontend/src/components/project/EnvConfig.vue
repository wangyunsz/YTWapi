<template>
  <div>
    <el-breadcrumb separator-class="el-icon-arrow-right">
      <el-breadcrumb-item :to="{ path: '/home' }">首页</el-breadcrumb-item>
      <el-breadcrumb-item>项目管理</el-breadcrumb-item>
      <el-breadcrumb-item>环境配置</el-breadcrumb-item>
    </el-breadcrumb>

    <!-- 卡片区域 -->
    <el-card class="box-card">

      <!-- 查询区 -->
      <el-form :inline="true" :model="queryInfo" class="demo-form-inline" size="mini">
        <el-form-item label="环境名称">
          <el-input v-model="queryInfo.env_name" placeholder="环境名称" clearable></el-input>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="getEnvList">查询</el-button>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="addEnvDialogClick">添加</el-button>
        </el-form-item>
      </el-form>

      <!-- 列表数据区 -->
        <template>
          <el-table :data="tableData" border stripe>
            <el-table-column type="index" label="#">
            </el-table-column>
            <el-table-column prop="pid" label="项目ID" v-if="false"></el-table-column>
            <el-table-column prop="project_code" label="项目英文名"></el-table-column>
            <el-table-column prop="project_name" label="项目名称"></el-table-column>
            <el-table-column prop="describe" label="描述" v-if="false"></el-table-column>
            <el-table-column prop="env_name" label="环境名称"></el-table-column>
            <el-table-column prop="protocol" label="协议类型"></el-table-column>
            <el-table-column prop="address" label="IP地址端口/域名"></el-table-column>
            <el-table-column prop="is_enable" label="是否启用">
              <template slot-scope="scope">
                <el-switch
                  v-model="scope.row.is_enable == 1 ? true : false"
                  active-color="#13ce66"
                  inactive-color="#ff4949"
                  disabled>
                </el-switch>
              </template>
            </el-table-column>
            <el-table-column prop="remark" label="备注"></el-table-column>
            <el-table-column label="操作">
              <template slot-scope="scope">
                <el-tooltip effect="dark" content="修改" placement="top" :enterable="false">
                  <el-button type="primary" icon="el-icon-edit" size="mini" @click="editEnvDialog(scope.row)"></el-button>
                </el-tooltip>
                <el-tooltip effect="dark" content="删除" placement="top" :enterable="false">
                  <el-button type="danger" icon="el-icon-delete" size="mini" @click="deleteEnvDialog(scope.row)"></el-button>
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

      <!-- 新增环境对话框 -->
      <el-dialog
        title="新增环境"
        :visible.sync="addDialogVisible"
        width="50%"
        center
        :close-on-click-modal="false"
        @close="addEnvClose">
        <el-form :model="envForm" status-icon :rules="envFormRules" ref="envFormRef" label-width="150px">
          <el-form-item label="项目ID" prop="pid">
           <el-select v-model="pidSelected" placeholder="请选择" @change="relatePreject">
              <el-option
                v-for="item,index in pidValue"
                :key="index"
                :value="item.pid">
                <span>{{ item.pid }}--{{ item.label }}</span>
              </el-option>
            </el-select>
          </el-form-item>

          <el-form-item label="项目英文名" prop="project_code">
            <el-input v-model="envForm.project_code" placeholder="自动带出" disabled></el-input>
          </el-form-item>
          <el-form-item label="项目名称" prop="project_name">
            <el-input v-model="envForm.project_name" placeholder="自动带出" disabled></el-input>
          </el-form-item>
          <el-form-item label="描述" prop="describe">
            <el-input type="textarea" v-model="envForm.describe" placeholder="自动带出" disabled></el-input>
          </el-form-item>
          <el-form-item label="环境名称" prop="env_name">
            <el-input v-model="envForm.env_name"></el-input>
          </el-form-item>
          <el-form-item label="协议类型" prop="protocol">
            <el-select v-model="envForm.protocol" placeholder="请选择">
              <el-option
                v-for="item,index in protocolList"
                :key="index"
                :value="item">
              </el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="IP地址端口/域名" prop="address">
            <el-input v-model="envForm.address" placeholder="示例: http://127.0.0.1:8000/apiTest"></el-input>
          </el-form-item>
          <el-form-item label="是否启用" prop="is_enable">
            <el-switch
              v-model="envForm.is_enable ? true : false"
              active-color="#13ce66"
              inactive-color="#ff4949"
              @change="isEnableChange">
            </el-switch>
          </el-form-item>
          <el-form-item label="备注" prop="remark">
            <el-input type="textarea" v-model="envForm.remark"></el-input>
          </el-form-item>

        </el-form>
        <span slot="footer" class="dialog-footer">
          <el-button @click="addDialogVisible = false">取 消</el-button>
          <el-button type="primary" @click="addEnv">确 定</el-button>
        </span>
      </el-dialog>

      <!-- 修改环境 对话框 -->
      <el-dialog
        title="修改环境"
        :visible.sync="editDialogVisible"
        width="50%"
        center
        :close-on-click-modal="false"
        @close="editEnvClose">
        <el-form :model="envForm" status-icon :rules="envFormRules" ref="envFormRef" label-width="150px">
          <el-form-item label="项目ID" prop="pid">
           <el-select v-model="envForm.pid" placeholder="请选择" @change="relatePreject" disabled>
              <el-option
                v-for="item,index in pidValue"
                :key="index"
                :value="item.pid">
                <span>{{ item.pid }}--{{ item.label }}</span>
              </el-option>
            </el-select>
          </el-form-item>

          <el-form-item label="项目英文名" prop="project_code">
            <el-input v-model="envForm.project_code" placeholder="自动带出" disabled></el-input>
          </el-form-item>
          <el-form-item label="项目名称" prop="project_name">
            <el-input v-model="envForm.project_name" placeholder="自动带出" disabled></el-input>
          </el-form-item>
          <el-form-item label="描述" prop="describe">
            <el-input type="textarea" v-model="envForm.describe" placeholder="自动带出" disabled></el-input>
          </el-form-item>
          <el-form-item label="环境名称" prop="env_name">
            <el-input v-model="envForm.env_name"></el-input>
          </el-form-item>
          <el-form-item label="协议类型" prop="protocol">
            <el-select v-model="envForm.protocol" placeholder="请选择">
              <el-option
                v-for="item,index in protocolList"
                :key="index"
                :value="item">
              </el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="IP地址端口/域名" prop="address">
            <el-input v-model="envForm.address" placeholder="示例: http://127.0.0.1:8000/apiTest"></el-input>
          </el-form-item>
          <el-form-item label="是否启用" prop="is_enable">
            <el-switch
              v-model="envForm.is_enable ? true : false"
              active-color="#13ce66"
              inactive-color="#ff4949"
              @change="isEnableChange">
            </el-switch>
          </el-form-item>
          <el-form-item label="备注" prop="remark">
            <el-input type="textarea" v-model="envForm.remark"></el-input>
          </el-form-item>

        </el-form>
        <span slot="footer" class="dialog-footer">
          <el-button @click="editDialogVisible = false">取 消</el-button>
          <el-button type="primary" @click="editEnv">确 定</el-button>
        </span>
      </el-dialog>

      <!-- 删除环境 -->
      <el-dialog
        title="提示"
        :visible.sync="deleteDialogVisible"
        width="30%"
        @close="deleteEnvClose"
        :close-on-click-modal="false">
        <span>请确认是否删除？</span>
        <span slot="footer" class="dialog-footer">
          <el-button @click="deleteDialogVisible = false">取 消</el-button>
          <el-button type="primary" @click="deleteEnv">确 定</el-button>
        </span>
      </el-dialog>
  </div>
</template>

<script>
  export default {
    data() {
      return {
        baseurl: this.$root.URL + '/envconfig/',
        baseurl_p: this.$root.URL + '/projectconfig/',
        tableData: [],
        queryInfo: {
          env_name: '',
          curpage: 1,
          pagesize: 10,
        },
        total: 0,

        // 新增
        addDialogVisible: false,
        // pid下拉选
        pidSelected: '',
        pidValue: [],
        projectList: [],
        // 协议类型
        protocolList: ['HTTP', 'HTTPS'],
        // 是否启用设置
        // isEnableValue: true,
        // 新增界面-对应字段及初始值
        envForm: {
          pid: '',
          project_code: '',
          project_name: '',
          describe: '',
          env_name: '',
          protocol: 'HTTP',
          address: '',
          is_enable: 1,
          remark: ''
        },
        envFormRules: {
          pid: [
            {
              required: true, message: '项目ID不能为空', trigger: 'blur'
            }
          ],
          project_code: [
            {
              required: true, message: '项目英文名不能为空', trigger: 'blur'
            }
          ],
          project_name: [
            {
              required: true, message: '项目名称不能为空', trigger: 'blur'
            }
          ],
          describe: [
            {
              required: false,
            }
          ],
          env_name: [
            {
              required: true, message: '环境名称不能为空', trigger: 'blur'
            },
            {
              min: 1, max: 50, message: '环境名称在1~50个字符之间', trigger: 'blur'
            }
          ],
          protocol: [
            {
              required: true
            }
          ],
          address: [
            {
              required: true, message: 'IP地址端口/域名不能为空', trigger: 'blur'
            },
            {
              min: 1, max: 2000, message: '项目英文名在1~2000个字符之间', trigger: 'blur'
            }
          ],
          is_enable: [
            {
              required: true
            }
          ],
          remark: [
            {
              required: false
            },
            {
              min: 0, max: 500, message: '项目英文名在0~500个字符之间', trigger: 'blur'
            }
          ],
        },

        //修改环境
        editDialogVisible: false,
        editUrl: '',
        // 修改次数
        updateCount: 0,

        // 删除环境
        deleteDialogVisible: false,
        deleteUrl: '',
      }
    },
    created() {
      this.getEnvList()
    },
    methods: {
      // 获取环境列表
      getEnvList: function() {
          this.$http.get(this.baseurl, {params: this.queryInfo}).then(res => {
          this.tableData = res.data.results
          this.total = res.data.total
        })
      },
      // 分页
      handleSizeChange: function(newsize){
        // console.log(newsize)
        this.queryInfo.pagesize = newsize
        this.queryInfo.curpage = 1
        this.getEnvList()
      },
      handleCurrentChange: function(newpage){
        // console.log(newpage)
        this.queryInfo.curpage = newpage
        this.getEnvList()
      },
      // 新增
      addEnvDialogClick() {
        this.addDialogVisible = true
        this.getSelected()
      },
      // 对话框关闭事件
      addEnvClose: function() {
        this.$refs.envFormRef.resetFields()
        this.updateCount = 0
        // 清空项目ID下拉选项
        this.pidSelected = ''
        this.pidValue = []
      },
      //新增项目-点击确定按钮事件
      addEnv: function(){
        this.$refs.envFormRef.validate(valid => {
          if(!valid) return
          //发起添加项目请求
          this.$http.post(this.baseurl, this.envForm).then(res => {
            if(res.status !== 201) {
              this.$message.error('新增失败！')
              return
            }
            this.$message.success('添加环境成功！')
            this.addDialogVisible = false
            this.getEnvList()
          })
        })
      },
      // 获取项目信息，处理显示为下拉选项
      getSelected: function() {
        this.$http.get(this.baseurl_p).then(res => {
          if(res.status !== 200) return
          for(var i=0;i<res.data.length;i++){
            const value = {
              pid: '',
              label: ''
            }
            value.pid = res.data[i].id
            value.label = res.data[i].project_code + "--" + res.data[i].project_name
            // console.log(value)
            this.pidValue.push(value)
          }
        })
      },
      // 项目ID改变，自动带出关联项目信息
      relatePreject() {
        this.envForm.pid = this.pidSelected
        this.$http.get(this.baseurl_p + this.pidSelected).then(res => {
          // console.log(res)
          if(res.status !== 200) return

          this.envForm.project_code = res.data.project_code
          this.envForm.project_name = res.data.project_name
          this.envForm.describe = res.data.describe
          // console.log(this.envForm)
        })
      },
      // 点击是否启用
      isEnableChange: function(e){
         e ? this.envForm.is_enable = 1 : this.envForm.is_enable = 0
         // console.log(e, this.envForm.is_enable)
      },

      // -----修改环境---------
      // 对话框关闭事件：修改环境对话框关闭，重置对话框内容
      editEnvClose: function() {
        this.$refs.envFormRef.resetFields()
        this.updateCount = 0
        this.editUrl = ''
      },
      // 点击修改按钮事件
      async editEnvDialog(row) {
        this.editDialogVisible = true
        this.editUrl = this.baseurl + row.id + '/'
        const {data: res} = await this.$http.get(this.editUrl)
        this.envForm = res
      },

      //修改环境-点击确定按钮事件
      editEnv: function(){
        this.$refs.envFormRef.validate(valid => {
          if(!valid) return
          if(this.updateCount > 1) {
            this.$http.put(this.editUrl, this.envForm).then(res => {
              if(res.status !== 200) {
                this.$message.error('修改失败！')
                return
              }
              this.$message.success('修改成功！')
              this.editDialogVisible = false
              this.getEnvList()
            })
          }
        })
      },

      // ------------删除环境---------------
      // 点击删除按钮事件
      deleteEnvDialog(row) {
        // console.log(row)
        this.deleteDialogVisible = true
        this.deleteUrl = this.baseurl + row.id + '/'
      },
      // 监听删除对话框关闭事件
      deleteEnvClose: function() {
        this.deleteDialogVisible = false
        this.deleteUrl = ''
      },
      // 删除项目-确认按钮
      deleteEnv(){
        this.$http.delete(this.deleteUrl).then(res => {
          if(res.status !== 204) {
            this.$message.error('删除失败！')
            return
          }
          this.$message.success('删除项目成功！')
          this.deleteDialogVisible = false
          this.getEnvList()
        })
      }
    },
    watch:{
      // 监听项目信息是否有修改，如果没有修改 updateCount>1。 (打开修改页面时会自动加1，后续每一个修改都会加1）
      envForm: {
           handler (val) {
             if (val) {
               this.updateCount++
               // console.log(this.updateCount)
          }
        },
        deep: true
      }
    }
  }
</script>

<style lang="less" scoped>

</style>
