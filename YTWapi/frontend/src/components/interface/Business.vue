<template>
  <div>
    <!-- 面包屑 -->
    <el-breadcrumb separator-class="el-icon-arrow-right">
      <el-breadcrumb-item :to="{ path: '/home' }">首页</el-breadcrumb-item>
      <el-breadcrumb-item>接口管理</el-breadcrumb-item>
      <el-breadcrumb-item>业务流程</el-breadcrumb-item>
    </el-breadcrumb>

    <!-- 卡片区域 -->
    <el-row :gutter="20">
      <el-col :span="6">
        <el-card class="box-card">
          <el-input placeholder="业务流程名称" v-model="busi_name" size="mini">
            <el-button slot="append" icon="el-icon-search" @click="queryBusiness" size="mini"></el-button>
          </el-input>
          <el-button type="text" @click="addBusinessDialogVisible = true">添加</el-button>
          <el-table :data="businessTableData" stripe size="small"
          @row-click="busiRowClick" :highlight-current-row="isHighlight">
            <el-table-column type="index" label="#"></el-table-column>
            <el-table-column prop="busi_name" label="业务流程名称" show-overflow-tooltip></el-table-column>
            <el-table-column label="操作" fit="false" min-width="55px">
              <template slot-scope="scope">
                <el-button type="text" @click="editBusinessDialog(scope.row)" size="mini">修改</el-button>
                <el-button type="text" @click="deleteBusinessDialog(scope.row)" size="mini">删除</el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-card>
      </el-col>
      <el-col :span="18">
        <el-card class="box-card">
          <span><b>{{cur_row_business.busi_name}}</b></span>
          <el-button style="float: right;" type="text" @click="addBusinessStep">添加步骤</el-button>
        </el-card>
        
        <el-collapse v-model="activeNames" @change="handleChange">
          <el-card class="box-card" v-for="item,index in curBusinessStepList" :key="index">
<!--            <el-button class="stepchange" icon="el-icon-top" size="mini" round></el-button>
            <el-button class="stepchange" icon="el-icon-bottom" size="mini" round></el-button> -->
            <el-button class="stepdel" icon="el-icon-delete" size="mini" round @click="deleteBusinessStep(item.id, item.step_no)"></el-button>
            <el-collapse-item :title="'步骤 '+(index+1)+'： '+item.case_name" :name="index">
              <div>心存光明，生活处处皆精彩；</div>
            </el-collapse-item>
          </el-card>
        </el-collapse>
      </el-col>
    </el-row>

    <!-- 业务流程 添加 -->
    <el-dialog
      title="添加业务流程名称"
      :visible.sync="addBusinessDialogVisible"
      center
      @close="addBusinessDialogClose">
      <el-form label-width="120px" :model="businessList"
        :rules="businessListRules" ref="businessListRef">
        <el-form-item label="业务流程名称" prop="busi_name">
          <el-input v-model="businessList.busi_name" placeholder="请输入"></el-input>
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button type="primary" @click="addBusinessSave">确 定</el-button>
        <el-button @click="addBusinessDialogVisible = false">取 消</el-button>
      </span>
    </el-dialog>

    <!-- 业务流程 修改 -->
    <el-dialog
      title="修改业务流程名称"
      :visible.sync="editBusinessDialogVisible"
      center
      @close="editBusinessDialogClose">
      <el-form label-width="120px" :model="businessList"
        :rules="businessListRules" ref="businessListRef">
        <el-form-item label="业务流程名称" prop="busi_name">
          <el-input v-model="businessList.busi_name" placeholder="请输入"></el-input>
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button type="primary" @click="editBusinessSave">确 定</el-button>
        <el-button @click="editBusinessDialogVisible = false">取 消</el-button>
      </span>
    </el-dialog>

    <!-- 删除 -->
    <el-dialog
      title="提示"
      :visible.sync="deleteBusiDialogVisible"
      width="30%"
      @close="deleteBusiDialogClose"
      :close-on-click-modal="false">
      <span>请确认是否删除？</span>
      <span slot="footer" class="dialog-footer">
        <el-button @click="deleteBusiDialogVisible = false">取 消</el-button>
        <el-button type="primary" @click="deleteBusiness">确 定</el-button>
      </span>
    </el-dialog>

    <!-- 业务流程步骤 添加 -->
    <el-dialog
      title="添加业务流程步骤"
      :visible.sync="addBusinessStepDialogVisible"
      center
      @close="addBusinessStepDialogClose">
      <el-form label-width="120px" :model="businessStepForm"
        :rules="businessStepFormRules" ref="businessStepFormRef">
        <el-form-item label="业务流程ID" prop="bsid" v-if="false">
          <el-input v-model="businessStepForm.bsid" placeholder="请输入"></el-input>
        </el-form-item>
        <el-form-item label="接口实例名称" prop="inc_id">
          <el-select v-model="businessStepForm.inc_id" filterable placeholder="请搜索并选择">
            <el-option
              v-for="item in caseNameList"
              :key="item.id"
              :value="item.id"
              :label="item.case_name">
            </el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="步骤" prop="step_no" v-if="false">
          <el-input v-model="businessStepForm.step_no" placeholder="请输入"></el-input>
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button type="primary" @click="addBusinessStepSave">确 定</el-button>
        <el-button @click="addBusinessStepDialogVisible = false">取 消</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
  export default {
    data(){
      return {
        baseUrl: this.$root.URL + '/business/',
        baseUrl_step: this.$root.URL + '/businessstep/',
        // 表格单击，高亮显示、并获取该行记录
        isHighlight: false,
        cur_row_business: {
          id: null,
          busi_name: ''
        },
        // 列表
        businessTableData: [],
        busi_name: '',
        total: 0,
        // 新增
        addBusinessDialogVisible: false,
        businessList: {
          busi_name: '',
        },
        businessListRules: {
          busi_name: [
            {
              required: true, message: '业务流程名称不能为空', trigger: 'blur'
            },
            {
              min: 1, max: 250, message: '1~250个字符', trigger: 'blur'
            }
          ],
        },

        // 修改
        editBusinessDialogVisible: false,
        editBusiUpdateCount: 0,
        editBusiUrl: '',
        // 删除
        deleteBusiDialogVisible: false,
        deleteBusiUrl: '',

        // 业务流程步骤
        curBusinessStepList: [],
        activeNames: [],
        addBusinessStepDialogVisible: false,
        businessStepForm: {
          bsid: null,
          inc_id: null,
          case_name: '',
          step_no: null
        },
        // 接口实例id、名称下拉选项列表
        caseNameList: [],
        businessStepFormRules: {
          inc_id: [
            {
              required: true, message: '接口实例名称不能为空', trigger: 'blur'
            },
          ],
        },

      }
    },
    created() {
      this.queryBusiness()
    },
    methods: {
      // 查询
      queryBusiness: function() {
        this.axios.get(this.baseUrl, {params: {busi_name: this.busi_name}}).then(res => {
          // console.log(res)
          this.businessTableData = res.data
          // console.log(this.businessTableData)
          this.total = res.data.total
        })
        this.cur_row_business = {id:null, busi_name:''}
      },
      // 业务流程列表表格行单击事件
      busiRowClick(row) {
        this.isHighlight = true
        this.cur_row_business.id = row.id
        this.cur_row_business.busi_name = row.busi_name
        // console.log(this.cur_row_business)
        // 刷新步骤
        this.getCurBusinessStepList()
      },

      // 新增对话框关闭事件
      addBusinessDialogClose() {
        this.$refs.businessListRef.resetFields()
        this.editBusiUpdateCount = 0
      },
      // 新增业务流程保存
      addBusinessSave() {
        this.$refs.businessListRef.validate(async valid => {
          if(!valid) return
          // 查询，名称不能重复
          const {data: resq} = await this.$http.get(this.baseUrl, {params: {busi_name: this.businessList.busi_name}})
          // console.log(resq.length)
          if(resq.length > 0) {
            this.$message.error('业务流程名称已存在。')
            return
          }
          //发起请求
          // console.log(this.businessList)
          this.$http.post(this.baseUrl, this.businessList).then(res => {
            if(res.status !== 201) {
              this.$message.error('新增失败！')
              return
            }
            this.$message.success('新增成功！')
            this.addBusinessDialogVisible = false
            this.queryBusiness()
          })
        })
      },

      // 修改
      editBusinessDialogClose() {
        this.$refs.businessListRef.resetFields()
        this.editBusiUpdateCount = 0
        this.editBusiUrl = ''
      },
      async editBusinessDialog(row) {
        this.editBusinessDialogVisible = true
        const {data: res} = await this.$http.get(this.baseUrl + row.id)
        this.businessList = res
        this.editBusiUrl = this.baseUrl + row.id + '/'
      },
      editBusinessSave() {
        this.$refs.businessListRef.validate(async valid => {
          if(!valid) return
          // 查询，名称不能重复
          const {data: resq} = await this.$http.get(this.baseUrl, {params: {busi_name: this.businessList.busi_name}})
          // console.log(resq.length)
          if(resq.length > 0) {
            this.$message.error('业务流程名称已存在。')
            return
          }
          if(this.editBusiUpdateCount > 1) {
            const {data: res} = await this.$http.put(this.editBusiUrl, this.businessList)
            // 失败处理暂缺
            this.$message.success('修改成功！')
          }
          this.editBusinessDialogVisible = false
          this.queryBusiness()
        })
      },
      // 删除
      deleteBusiDialogClose() {
        this.deleteBusiUrl = ''
      },
      deleteBusinessDialog(row) {
        this.deleteBusiDialogVisible = true
        this.deleteBusiUrl = this.baseUrl + row.id + '/'
      },
      async deleteBusiness() {
        const {data: resd} = await this.$http.delete(this.deleteBusiUrl)
        this.$message.success('删除成功！')
        this.deleteBusiDialogVisible = false
        this.queryBusiness()
      },

      // 步骤列表
      getCurBusinessStepList() {
        this.$http.get(this.baseUrl_step, {params:{bsid:this.cur_row_business.id}}).then(res => {
          this.curBusinessStepList = res.data
        })
      },
      handleChange(val) {
        // console.log(val)
      },
      // 添加步骤
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

      addBusinessStepDialogClose() {
        this.$refs.businessStepFormRef.resetFields()
        this.caseNameList = []
        this.businessStepForm = {
          bsid: null,
          inc_id: null,
          case_name: '',
          step_no: null
        }
      },
      addBusinessStep() {
        // 判断是否已选中业务流程
        if(this.cur_row_business.id == null) {
          this.$message.info('请先在业务流程列表中单击选中业务流程!')
          return
        }
        this.addBusinessStepDialogVisible = true
        // 下拉框值获取
        this.getCaseNameList()
      },
      addBusinessStepSave() {
        this.businessStepForm.bsid = this.cur_row_business.id
        // 从最大的步骤号递增1
        if(this.curBusinessStepList.length == 0){
          this.businessStepForm.step_no = 1
        }else{
          this.businessStepForm.step_no = this.curBusinessStepList.slice(-1)[0].step_no + 1
        }
        this.$http.post(this.baseUrl_step, this.businessStepForm).then(res => {
          if(res.status !== 201) {
            this.$message.error('新增失败！')
            return
          }
          this.$message.success('新增成功！')
          this.addBusinessStepDialogVisible = false
          this.getCurBusinessStepList()
        })

      },
      // 删除步骤
      deleteBusinessStep(id, step_no) {
        // console.log(id, step_no)
        this.$http.delete(this.baseUrl_step + id).then(res => {
          if(res.status !== 204){
            this.$message.error('系统异常！')
            return
          }
          this.$message.success('删除成功！')
          this.getCurBusinessStepList()
        })

      }
    },
    watch: {
      businessList: {
           handler (val) {
             if (val) {
               this.editBusiUpdateCount++
          }
        },
        deep: true
      }
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
