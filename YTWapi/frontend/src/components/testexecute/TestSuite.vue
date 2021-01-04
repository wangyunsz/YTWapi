<template>
  <div>
    <el-breadcrumb separator-class="el-icon-arrow-right">
      <el-breadcrumb-item :to="{ path: '/home' }">首页</el-breadcrumb-item>
      <el-breadcrumb-item>执行管理</el-breadcrumb-item>
      <el-breadcrumb-item>测试集</el-breadcrumb-item>
    </el-breadcrumb>

    <!-- 卡片区域 -->
    <el-card class="box-card">
      <el-form :inline="true" :model="queryInfo" class="demo-form-inline" size="mini">
        <el-form-item label="测试集名称">
          <el-input v-model="queryInfo.suite_name" placeholder="测试集名称" clearable></el-input>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="getTestSuiteList">查询</el-button>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="addTestSuiteDialogVisible = true">添加</el-button>
        </el-form-item>
      </el-form>

  <!-- 列表数据区 -->
    <template>
      <el-table :data="testSuiteData" border stripe>
        <el-table-column type="index" label="#"></el-table-column>
        <el-table-column prop="suite_name" label="测试集名称"></el-table-column>
        <el-table-column prop="remark" label="说明"></el-table-column>
        <el-table-column label="操作">
          <template slot-scope="scope">
            <el-tooltip effect="dark" content="修改" placement="top" :enterable="false">
              <el-button type="primary" icon="el-icon-edit" size="mini" @click="editTestSuiteDialog(scope.row)"></el-button>
            </el-tooltip>
            <el-tooltip effect="dark" content="删除" placement="top" :enterable="false">
              <el-button type="danger" icon="el-icon-delete" size="mini" @click="deleteTestSuiteDialog(scope.row)"></el-button>
            </el-tooltip>
            <el-tooltip effect="dark" content="挑选测试用例" placement="top" :enterable="false">
              <el-button type="primary" icon="el-icon-setting" size="mini" @click="selectTestCaseDialogClick(scope.row)"></el-button>
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
      title="新增测试集"
      :visible.sync="addTestSuiteDialogVisible"
      width="50%"
      center
      :close-on-click-modal="false"
      @close="addTestSuiteDialogClose">
      <el-form :model="testSuiteForm" status-icon :rules="testSuiteFormRules" ref="testSuiteFormRef" label-width="150px">
        <el-form-item label="测试集名称" prop="suite_name">
          <el-input v-model="testSuiteForm.suite_name" placeholder="请输入"></el-input>
        </el-form-item>
        <el-form-item label="说明" prop="remark">
          <el-input type="textarea" v-model="testSuiteForm.remark"></el-input>
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="addTestSuiteDialogVisible = false">取 消</el-button>
        <el-button type="primary" @click="addTestSuiteSave">确 定</el-button>
      </span>
    </el-dialog>

  <!-- 修改对话框 -->
  <el-dialog
    title="修改测试集"
    :visible.sync="editTestSuiteDialogVisible"
    width="50%"
    center
    :close-on-click-modal="false"
    @close="editTestSuiteDialogClose">
    <el-form :model="testSuiteForm" status-icon :rules="testSuiteFormRules" ref="testSuiteFormRef" label-width="150px">
      <el-form-item label="测试集名称" prop="suite_name">
        <el-input v-model="testSuiteForm.suite_name" placeholder="请输入"></el-input>
      </el-form-item>
      <el-form-item label="说明" prop="remark">
        <el-input type="textarea" v-model="testSuiteForm.remark"></el-input>
      </el-form-item>
    </el-form>
    <span slot="footer" class="dialog-footer">
      <el-button @click="editTestSuiteDialogVisible = false">取 消</el-button>
      <el-button type="primary" @click="editTestSuiteSave">确 定</el-button>
    </span>
  </el-dialog>

  <!-- 删除 -->
  <el-dialog
    title="提示"
    :visible.sync="deleteTestSuiteDialogVisible"
    width="30%"
    @close="deleteTestSuiteDialogClose"
    :close-on-click-modal="false">
    <span>请确认是否删除？</span>
    <span slot="footer" class="dialog-footer">
      <el-button @click="deleteTestSuiteDialogVisible = false">取 消</el-button>
      <el-button type="primary" @click="deleteTestSuiteSure">确 定</el-button>
    </span>
  </el-dialog>

  <!-- 挑选测试用例 -->
  <el-dialog
    title="挑选测试用例"
    :visible.sync="selectTestCaseDialogVisible"
    width="50%"
    center
    :close-on-click-modal="false"
    @close="selectTestCaseDialogClose">
    <span>{{test_suite_name}}</span>
    <el-card>
      <el-tree
        ref="tree"
        :data="testCaseTree"
        show-checkbox
        node-key="id"
        :props="defaultProps"
        :default-expand-all="true"
        :highlight-current="true">
      </el-tree>
    </el-card>
    <span slot="footer" class="dialog-footer">
      <el-button @click="selectTestCaseDialogVisible = false">取 消</el-button>
      <el-button type="primary" @click="selectTestCaseSave">确 定</el-button>
    </span>
  </el-dialog>

  </div>
</template>

<script>
  export default {
    data() {
      return {
        baseUrl: this.$root.URL + '/testsuite/',
        baseUrl_testcase: this.$root.URL + '/testsuitetestcase/',
        testSuiteData: [],
        queryInfo: {
          suite_name: '',
          curpage: 1,
          pagesize: 10,
        },
        total: 0,
        // 测试集 新增
        addTestSuiteDialogVisible: false,
        testSuiteForm: {
          suite_name: '',
          remark: ''
        },
        testSuiteFormRules: {
          suite_name: [
            {
              required: true, message: '测试集名称不能为空', trigger: 'blur'
            },
            {
              min: 1, max: 255, message: '测试集名称在1~255个字符之间', trigger: 'blur'
            }
          ],
          remark: [
            {
              required: false,
            },
            {
              min: 0, max: 500, message: '说明在1~500个字符之间', trigger: 'blur'
            }
          ],
        },
        // 修改
        editTestSuiteDialogVisible: false,
        editTestSuiteUrl: '',
        editTestSuiteUpdateCount: 0,
        // 删除
        deleteTestSuiteDialogVisible: false,
        deleteTestSuiteUrl: '',
        testSuiteID: '',
        // 挑选测试用例
        selectTestCaseDialogVisible: false,
        test_suite_name: '',
        testCaseTree: [],
        defaultProps: {
          children: 'children',
          label: 'label'
        },
        testCaseForm: {
          tsid: null,
          tc_list: ''
        },
      }
    },
    created() {
      this.getTestSuiteList()
      this.getTestCaseTree()
    },
    methods: {
      // 列表
      getTestSuiteList() {
        this.$http.get(this.baseUrl, {params: this.queryInfo}).then(res => {
          if(res.status !== 200) return
          console.log(res)
          this.testSuiteData = res.data.results
          this.total = res.data.total
        })
      },
      // 分页
      handleSizeChange(val) {
        this.queryInfo.pagesize = val
        this.queryInfo.curpage = 1
        this.getTestSuiteList()
      },
      handleCurrentChange(val) {
        this.queryInfo.curpage = val
        this.getTestSuiteList()
      },
      // 新增
      addTestSuiteDialogClose() {
        this.$refs.testSuiteFormRef.resetFields()
        this.editTestSuiteUpdateCount = 0
      },
      addTestSuiteSave() {
        this.$refs.testSuiteFormRef.validate(valid => {
          if(!valid) return
          this.$http.post(this.baseUrl, this.testSuiteForm).then(res => {
            if(res.status !== 201){
              this.$message.error('新增失败！')
              return
            }
            this.$message.success('新增成功！')
            this.addTestSuiteDialogVisible = false
            this.getTestSuiteList()
          })
        })
      },

      // 修改
      editTestSuiteDialogClose() {
        this.$refs.testSuiteFormRef.resetFields()
        this.editTestSuiteUpdateCount = 0
        this.editTestSuiteUrl = ''
      },
      editTestSuiteDialog(row) {
        this.$http.get(this.baseUrl + row.id + '/').then(res => {
          if(res.status !== 200) {
            this.$message.error('系统异常，数据获取失败！')
            return
          }
          this.testSuiteForm = res.data
        })
        this.editTestSuiteDialogVisible = true
        this.editTestSuiteUrl = this.baseUrl + row.id + '/'
      },
      editTestSuiteSave() {
        this.$refs.testSuiteFormRef.validate(valid => {
          if(!valid) return
          if(this.editTestSuiteUpdateCount > 1) {
            this.editTestSuiteDialogVisible = false
            return
          }
          this.$http.put(this.editTestSuiteUrl, this.testSuiteForm).then(res => {
            if(res.status !== 200){
              this.$message.error('修改失败！')
              return
            }
            this.$message.success('修改成功！')
            this.editTestSuiteDialogVisible = false
            this.getTestSuiteList()
          })
        })
      },
      // 删除
      deleteTestSuiteDialog(row) {
        this.deleteTestSuiteDialogVisible = true
        this.deleteTestSuiteUrl = this.baseUrl + row.id + '/'
        this.testSuiteID = row.id
      },
      deleteTestSuiteDialogClose() {
        this.deleteTestSuiteUrl = ''
      },
      deleteTestSuiteSure() {
        this.$http.delete(this.deleteTestSuiteUrl).then(res => {
          if(res.status !== 204) {
            this.$message.error('删除失败！')
            return
          }
          this.$message.success('删除成功！')
          this.deleteTestSuiteDialogVisible = false
          this.getTestSuiteList()
        })
      },

      // 测试集挑选测试用例
      // 点击挑选测试用例按钮
      selectTestCaseDialogClick(row) {
        // console.log(row)
        this.selectTestCaseDialogVisible = true
        this.test_suite_name = row.suite_name
        this.testCaseForm.tsid = row.id
        // this.getTestCaseTree()
        // 获取并设置勾选项
        this.$http.get(this.baseUrl_testcase, {params: {tsid: this.testCaseForm.tsid}}).then(resq => {
          if(resq.status !== 200) return
          if(resq.data.length == 0) return
          // console.log(resq)
          const selectedCase = resq.data[0].tc_list.indexOf(",") ? resq.data[0].tc_list.split(",") : [resq.data[0].tc_list]
          console.log(selectedCase)
          this.$nextTick(() => {
            this.$refs.tree.setCheckedKeys(selectedCase)
          })
        })
      },
      // 挑选测试用例对话框关闭事件
      selectTestCaseDialogClose() {
        this.test_suite_name = ''
        this.testCaseForm = {
          tsid: null,
          tc_list: ''
        }
        // 清空勾选项
        this.$nextTick(() => {
          this.$refs.tree.setCheckedKeys([])
        })
      },
      // 获取测试集测试用例

      // 挑选测试用例对话框 保存
      selectTestCaseSave() {
        // 获取当前所有选中用例id
        let selectedCase = this.$refs.tree.getCheckedKeys(true)
        this.testCaseForm.tc_list = selectedCase.toString()
        // console.log(this.testCaseForm)
        // 先查询是否存在测试集的用例
        this.$http.get(this.baseUrl_testcase, {params: {tsid: this.testCaseForm.tsid}}).then(resq => {
          if(resq.status !== 200) {
            this.$message.error('系统异常，查询测试集数据异常！')
            return
          }
          // 如果数据库已存在数据，修改
          if(resq.data.length) {
            this.$http.put(this.baseUrl_testcase + resq.data[0].id + '/', this.testCaseForm).then(res => {
              if(res.status !== 200) {
                this.$message.error('挑选测试用例保存失败！')
                return
              }
              this.$message.success('保存成功！')
              this.selectTestCaseDialogVisible = false
            })
          }else { // 新增
            this.$http.post(this.baseUrl_testcase, this.testCaseForm).then(res => {
              if(res.status !== 201) {
                this.$message.error('挑选测试用例保存失败！')
                return
              }
              this.$message.success('保存成功！')
              this.selectTestCaseDialogVisible = false
            })
          }
        })
      },

      // 获取测试用例树型结构
      getTestCaseTree() {
        // 获取项目名称列表
        const projectTree = []
        this.$http.get(this.$root.URL + '/projectconfig/').then(resp => {
          if(resp.status !== 200) return
          if(resp.data.length == 0) return

          // 第一重循环：添加项目
          for(var i=0;i<resp.data.length;i++) {
            // 获取项目对应的所有模块
            const moduleTree = []
            const pid = resp.data[i].id
            const pname = resp.data[i].project_name
            this.$http.get(this.$root.URL + '/module/', {params: {pid: resp.data[i].id}}).then(resm => {
              if(resm.status !== 200) return
              if(resm.data.length == 0) return

              // 第二重循环：添加模块
              for(var m=0;m<resm.data.length;m++){
                // 获取模块对应的所有测试用例
                const caseTree = []
                const mid = resm.data[m].id
                const mname = resm.data[m].module_name
                this.$http.get(this.$root.URL + '/testcase/', {params: {mid: resm.data[m].id}}).then(rest => {
                  if(rest.status !== 200) return
                  if(rest.data.length == 0) return

                  // 第三重循环：添加用例
                  for(var t=0;t<rest.data.length;t++) {
                    caseTree.push({
                      id: rest.data[t].id,
                      label: '[' + rest.data[t].level + '] ' + rest.data[t].title,
                      // 不启用的用例,设置不可勾选
                      disabled: rest.data[t].is_enable == 0 ? true : false
                    })
                  }
                  // 第三重循环完成，添加数据
                  if(caseTree.length > 0) {
                    moduleTree.push({
                      id: 'm' + mid,  // 增加字母，区分id
                      label: mname,
                      children: caseTree
                    })
                  }else {
                    moduleTree.push({
                      id: 'm' + mid,
                      label: mname,
                      disabled: true
                    })
                  }

                })
              } // 2
              // 第二重循环内，添加数据
              if(moduleTree) {
                projectTree.push({
                  id: 'p' + pid,
                  label: pname,
                  children: moduleTree
                })
              }else {
                projectTree.push({
                  id: 'p' + pid,
                  label: pname,
                  disabled: true
                })
              }
            })
          } // 1
        })
        this.testCaseTree.push({
                  id: 't1',
                  label: '测试用例',
                  children: projectTree
                })
        console.log('testCaseTree', this.testCaseTree)
      }
    },
    watch: {
      testSuiteForm: {
        handler(val) {
          if(val) {
            this.editTestSuiteUpdateCount++
          }
        }
      }

    }
  }
</script>

<style lang="less" scoped>
</style>
