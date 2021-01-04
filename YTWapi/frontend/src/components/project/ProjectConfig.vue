<template>
  <div>
    <!-- 面包屑 -->
    <el-breadcrumb separator-class="el-icon-arrow-right">
      <el-breadcrumb-item :to="{ path: '/home' }">首页</el-breadcrumb-item>
      <el-breadcrumb-item>项目管理</el-breadcrumb-item>
      <el-breadcrumb-item>项目配置</el-breadcrumb-item>
    </el-breadcrumb>
    <!-- 卡片区域 -->
    <el-card class="box-card">
      <!-- 查询区 -->
      <el-form :inline="true" :model="queryInfo" class="demo-form-inline" size="mini">
        <el-form-item label="项目英文名">
          <el-input v-model="queryInfo.project_code" placeholder="项目英文名" clearable></el-input>
        </el-form-item>
        <el-form-item label="项目名称">
          <el-input v-model="queryInfo.project_name" placeholder="项目名称" clearable></el-input>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="getProjectList">查询</el-button>
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
          <el-table-column prop="project_code" label="项目英文名"></el-table-column>
          <el-table-column prop="project_name" label="项目名称"></el-table-column>
          <el-table-column
            prop="describe"
            label="描述">
          </el-table-column>
          <el-table-column label="操作">
            <template slot-scope="scope">
              <el-tooltip effect="dark" content="修改" placement="top" :enterable="false">
                <el-button type="primary" icon="el-icon-edit" size="mini" @click="editProjectDialog(scope.row)"></el-button>
              </el-tooltip>
              <el-tooltip effect="dark" content="删除" placement="top" :enterable="false">
                <el-button type="danger" icon="el-icon-delete" size="mini" @click="deleteProjectDialog(scope.row)"></el-button>
              </el-tooltip>
              <el-tooltip effect="dark" content="模块配置" placement="top" :enterable="false">
                <el-button type="primary" icon="el-icon-setting" size="mini" @click="moduleConfigDialog(scope.row)"></el-button>
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

    <!-- 新增功能 -->
    <el-dialog
      title="新增项目"
      :visible.sync="addDialogVisible"
      width="50%"
      center @close="addProjectClose"
      :close-on-click-modal="false">
      <el-form label-width="100px" :model="projectForm"
        :rules="projectRules" ref="projectFormRef">
        <el-form-item label="项目英文名" prop="project_code">
          <el-input v-model="projectForm.project_code"></el-input>
        </el-form-item>
        <el-form-item label="项目名称" prop="project_name">
          <el-input v-model="projectForm.project_name"></el-input>
        </el-form-item>
        <el-form-item label="描述" prop="describe">
          <el-input type="textarea" v-model="projectForm.describe"></el-input>
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="addDialogVisible = false">取 消</el-button>
        <el-button type="primary" @click="addProject">确 定</el-button>
      </span>
    </el-dialog>

    <!-- 修改功能 -->
    <el-dialog
      title="修改项目"
      :visible.sync="editDialogVisible"
      width="50%"
      center @close="editProjectClose"
      :close-on-click-modal="false">
      <el-form label-width="100px" :model="projectForm"
        :rules="projectRules" ref="projectFormRef">
        <el-form-item label="项目英文名" prop="project_code">
          <el-input v-model="projectForm.project_code"></el-input>
        </el-form-item>
        <el-form-item label="项目名称" prop="project_name">
          <el-input v-model="projectForm.project_name"></el-input>
        </el-form-item>
        <el-form-item label="描述" prop="describe">
          <el-input type="textarea" v-model="projectForm.describe"></el-input>
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="editDialogVisible = false">取 消</el-button>
        <el-button type="primary" @click="editProject">确 定</el-button>
      </span>
    </el-dialog>

    <!-- 删除项目 -->
    <el-dialog
      title="提示"
      :visible.sync="deleteDialogVisible"
      width="30%"
      @close="deleteProjectClose"
      :close-on-click-modal="false">
      <span>删除项目，会关联删除该项目的模块信息及环境信息，请确认是否删除？</span>
      <span slot="footer" class="dialog-footer">
        <el-button @click="deleteDialogVisible = false">取 消</el-button>
        <el-button type="primary" @click="deleteProject">确 定</el-button>
      </span>
    </el-dialog>

    <!-- 模块配置 -->
    <el-dialog
      title="模块配置"
      :visible.sync="moduleConfigDialogVisible"
      width="50%"
      center @close="moduleConfigDialogClose"
      :close-on-click-modal="false">

      <el-button type="primary" size="mini" @click="addModuleDialogVisible = true">添加</el-button>
      <el-table :data="moduleData" border stripe>
        <el-table-column type="index" label="#"></el-table-column>
        <el-table-column prop="pid" label="项目ID" v-if="false"></el-table-column>
        <el-table-column prop="module_name" label="模块名称"></el-table-column>
        <el-table-column label="操作">
          <template slot-scope="scope">
            <el-tooltip effect="dark" content="修改" placement="top" :enterable="false">
              <el-button type="primary" icon="el-icon-edit" size="mini" @click="editModuleDialog(scope.row)"></el-button>
            </el-tooltip>
            <el-tooltip effect="dark" content="删除" placement="top" :enterable="false">
              <el-button type="danger" icon="el-icon-delete" size="mini" @click="deleteModuleDialog(scope.row)"></el-button>
            </el-tooltip>
          </template>
        </el-table-column>
      </el-table>
      <span slot="footer" class="dialog-footer">
        <el-button @click="moduleConfigDialogVisible = false">取 消</el-button>
        <el-button type="primary" @click="moduleConfigDialogVisible = false">完 成</el-button>
      </span>
    </el-dialog>

    <!-- 新增功能 -->
    <el-dialog
      title="新增模块"
      :visible.sync="addModuleDialogVisible"
      width="50%"
      center @close="addModuleDialogClose"
      :close-on-click-modal="false">
      <el-form label-width="100px" :model="moduleForm"
        :rules="moduleFormRules" ref="moduleFormRef">
        <el-form-item label="项目ID" prop="pid" v-if="false">
          <el-input v-model="moduleForm.pid"></el-input>
        </el-form-item>
        <el-form-item label="模块名称" prop="module_name">
          <el-input v-model="moduleForm.module_name"></el-input>
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="addModuleDialogVisible = false">取 消</el-button>
        <el-button type="primary" @click="addModuleSave">确 定</el-button>
      </span>
    </el-dialog>

  <!-- 修改功能 -->
    <el-dialog
      title="新增模块"
      :visible.sync="editModuleDialogVisible"
      width="50%"
      center @close="editModuleDialogClose"
      :close-on-click-modal="false">
      <el-form label-width="100px" :model="moduleForm"
        :rules="moduleFormRules" ref="moduleFormRef">
        <el-form-item label="项目ID" prop="pid" v-if="false">
          <el-input v-model="moduleForm.pid"></el-input>
        </el-form-item>
        <el-form-item label="模块名称" prop="module_name">
          <el-input v-model="moduleForm.module_name"></el-input>
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="editModuleDialogVisible = false">取 消</el-button>
        <el-button type="primary" @click="editModuleSave">确 定</el-button>
      </span>
    </el-dialog>

    <!-- 删除 -->
    <el-dialog
      title="提示"
      :visible.sync="deleteModuleDialogVisible"
      width="30%"
      @close="deleteModuleDialogClose"
      :close-on-click-modal="false">
      <span>请确认是否删除？</span>
      <span slot="footer" class="dialog-footer">
        <el-button @click="deleteModuleDialogVisible = false">取 消</el-button>
        <el-button type="primary" @click="deleteModuleSure">确 定</el-button>
      </span>
    </el-dialog>

  </div>
</template>

<script>
  export default {
    data(){
      return {
        baseurl: this.$root.URL + '/projectconfig/',
        queryInfo: {
          project_code: '',
          project_name: '',
          curpage: 1,
          pagesize: 10,
        },
        total: 0,
        tableData: [],

        // 新增项目
        addDialogVisible: false,
        projectForm: {
          project_code: '',
          project_name: '',
          describe: ''
        },
        projectRules: {
          project_code: [
            {
              required: true, message: '请输入项目英文名', trigger: 'blur'
            },
            {
              min: 1, max: 20, message: '项目英文名在1~20个字符之间', trigger: 'blur'
            }
          ],
          project_name: [
            {
              required: true, message: '请输入项目名称', trigger: 'blur'
            },
            {
              min: 1, max: 50, message: '项目名称在1~50个字符之间', trigger: 'blur'
            }
          ],
          describe: [
            {
              required: false, message: '请输入项目描述', trigger: 'blur'
            },
            {
              min: 0, max: 500, message: '项目描述在0~500个字符之间', trigger: 'blur'
            }
          ]
        },
        // 修改项目
        editDialogVisible: false,
        editUrl: '',
        //监听修改项目页面数据变化次数
        updateCount: 0,
        // 删除项目
        deleteDialogVisible: false,
        deleteUrl: '',

        // 模块配置
        baseUrl_module: this.$root.URL + '/module/',
        moduleConfigDialogVisible: false,
        moduleData: [],
        // 新增
        addModuleDialogVisible: false,
        moduleForm: {
          pid: null,
          module_name: ''
        },
        moduleFormRules: {
          module_name: [
            {
              required: true, message: '请输入模块名称', trigger: 'blur'
            },
            {
              min: 1, max: 255, message: '模块名称在1~255个字符之间', trigger: 'blur'
            }
          ],
        },
        // 修改
        editModuleDialogVisible: false,
        editModuleUrl: '',

        // 删除
        deleteModuleDialogVisible: false,
        deleteModuleUrl: '',

      }
    },
    created() {
      this.getProjectList();
    },
    methods: {
      getProjectList() {
        this.$http.get(this.baseurl, {params: this.queryInfo}).then(res => {
          this.tableData = res.data.results
          this.total = res.data.total
        })
      },
      // 分页
      handleSizeChange(newsize){
        this.queryInfo.pagesize = newsize
        this.queryInfo.curpage = 1
        this.getProjectList()
      },
      handleCurrentChange(newpage){
        this.queryInfo.curpage = newpage
        this.getProjectList()
      },
      //增加项目对话框关闭，重置对话框内容
      addProjectClose: function() {
        this.$refs.projectFormRef.resetFields()
        this.updateCount = 0
      },
      //新增项目
      addProject: function(){
        this.$refs.projectFormRef.validate(valid => {
          if(!valid) return
          //发起添加项目请求
          this.$http.post(this.baseurl, this.projectForm).then(res => {
            if(res.status !== 201) {
              this.$message.error('添加失败！')
              return
            }
            this.$message.success('添加项目成功！')
            this.addDialogVisible = false
            this.getProjectList()
          })
        })
      },
      //修改项目对话框关闭，重置对话框内容
      editProjectClose: function() {
        this.$refs.projectFormRef.resetFields()
        this.updateCount = 0
      },
      //点击修改按钮事件
      async editProjectDialog(row) {
        this.editDialogVisible = true
        this.editUrl = this.baseurl + row.id + '/'
        const {data: res} = await this.$http.get(this.editUrl)
        this.projectForm = res
      },
      //修改项目-确定按钮
      editProject(){
        this.$refs.projectFormRef.validate(valid => {
          if(!valid) return
          // 判断是否修改
          if(this.updateCount <= 1) {
            this.editDialogVisible = false
            return
          }
          this.$http.put(this.editUrl, this.projectForm).then(res => {
            if(res.status !== 200) {
              this.$message.error('修改失败！')
              return
            }
            this.$message.success('修改项目成功！')
            this.editDialogVisible = false
            this.getProjectList()
          })
        })
      },

      // 删除项目
      // 点击删除按钮事件
      deleteProjectDialog(row) {
        this.deleteDialogVisible = true
        this.deleteUrl = this.baseurl + row.id + '/'
      },
      // 监听删除对话框关闭事件
      deleteProjectClose: function() {
        this.deleteDialogVisible = false
        this.deleteUrl = ''
      },
      // 删除项目-确认按钮
      deleteProject(){
        this.$http.delete(this.deleteUrl).then(res => {
          if(res.status !== 204) {
            this.$message.error('删除失败！')
            return
          }
          this.$message.success('删除项目成功！')
          this.deleteDialogVisible = false
          this.getProjectList()
        })
      },

      // 模块配置
      moduleConfigDialogClose() {
        this.moduleForm.pid = null
      },
      moduleConfigDialog(row) {
        this.moduleConfigDialogVisible = true
        this.moduleForm.pid = row.id
        this.getModuleList()
      },
      // 列表
      getModuleList() {
        this.$http.get(this.baseUrl_module, {params: {pid: this.moduleForm.pid}}).then(res => {
          if(res.status !== 200) return
          this.moduleData = res.data
        })
      },
      addModuleDialogClose() {
        this.moduleForm.module_name = ''
      },
      addModuleSave() {
        // console.log(this.moduleForm)
        this.$refs.moduleFormRef.validate(valid => {
          if(!valid) return
          this.$http.post(this.baseUrl_module, this.moduleForm).then(res => {
            if(res.status !== 201) {
              this.$message.error('新增失败！')
              return
            }
            this.$message.success('新增成功！')
            this.addModuleDialogVisible = false
            this.getModuleList()
          })
        })
      },

      // 修改
      editModuleDialog(row) {
        // console.log(row)
        this.editModuleDialogVisible = true
        this.editModuleUrl = this.baseUrl_module + row.id + '/'
        this.moduleForm.module_name = row.module_name
      },
      editModuleDialogClose() {
        this.moduleForm.module_name = ''
      },
      editModuleSave() {
        this.$refs.moduleFormRef.validate(valid => {
          if(!valid) return
          this.$http.put(this.editModuleUrl, this.moduleForm).then(res => {
            if(res.status !== 200) {
              this.$message.error('修改失败！')
              return
            }
            this.$message.success('修改成功！')
            this.editModuleDialogVisible = false
            this.getModuleList()
          })
        })
      },
      // 删除
      deleteModuleDialog(row) {
        this.deleteModuleDialogVisible = true
        this.deleteModuleUrl = this.baseUrl_module + row.id + '/'
      },
      deleteModuleDialogClose() {
        this.deleteModuleUrl = ''
      },
      deleteModuleSure() {
        this.$http.get(this.deleteModuleUrl).then(resq => {
          if(resq.status !== 200) {
            this.$message.error('系统异常或数据库中不存在该数据！')
            return
          }
          this.$http.delete(this.deleteModuleUrl).then(res => {
            if(res.status !== 204) {
              this.$message.error('删除失败！')
              return
            }
            this.$message.success('删除成功！')
            this.deleteModuleDialogVisible = false
            this.getModuleList()
          })
        })
      }
    },
    watch:{
      // 监听项目信息是否有修改，如果没有修改 updateCount>1。 (打开修改页面时会自动加1，后续每一个修改都会加1）
      projectForm: {
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
