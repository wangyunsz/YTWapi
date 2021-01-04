<template>
  <div>
    <el-breadcrumb separator-class="el-icon-arrow-right">
      <el-breadcrumb-item :to="{ path: '/home' }">首页</el-breadcrumb-item>
      <el-breadcrumb-item>任务管理</el-breadcrumb-item>
      <el-breadcrumb-item>任务列表</el-breadcrumb-item>
    </el-breadcrumb>

    <!-- 卡片区域 -->
    <el-card class="box-card">
      <el-form :inline="true" :model="queryInfo" class="demo-form-inline" size="mini">
        <el-form-item label="任务名称">
          <el-input v-model="queryInfo.task_name" placeholder="任务名称" clearable></el-input>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="getTaskList">查询</el-button>
        </el-form-item>
      </el-form>

    <!-- 列表数据区 -->
      <template>
        <el-table :data="taskListData" border stripe v-loading="loading">
          <el-table-column type="index" label="#"></el-table-column>
          <el-table-column prop="execute_stamp" label="执行时间戳" v-if="false"></el-table-column>
          <el-table-column prop="task_id" label="任务ID" v-if="false"></el-table-column>
          <el-table-column prop="task_name" label="任务名称"></el-table-column>
          <el-table-column prop="start_time" label="开始时间" :formatter="timeFormat"></el-table-column>
          <el-table-column prop="status" label="状态">
            <template slot-scope="scope">
                  <el-tag type="success" v-if="scope.row.status == '成功'">成功</el-tag>
                  <el-tag type="danger" v-else-if="scope.row.status == '失败'">失败</el-tag>
                  <el-tag type="info" v-else-if="scope.row.status == '未开始'">未开始或进行中</el-tag>
                </template>
          </el-table-column>
          <el-table-column prop="end_time" label="结束时间" :formatter="timeFormat"></el-table-column>
          <el-table-column label="操作">
            <template slot-scope="scope">
              <el-tooltip effect="dark" content="查看结果" placement="top" :enterable="false">
                <el-button type="primary" icon="el-icon-view" size="mini" @click="showTaskResultDialog(scope.row)"></el-button>
              </el-tooltip>
              <el-tooltip effect="dark" content="删除" placement="top" :enterable="false">
                <el-button type="danger" icon="el-icon-delete" size="mini" @click="deleteTaskDialog(scope.row)"></el-button>
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

    <!-- 删除 -->
    <el-dialog
      title="提示"
      :visible.sync="deleteTaskDialogVisible"
      width="30%"
      @close="deleteTaskDialogClose"
      :close-on-click-modal="false">
      <span>请确认是否删除？</span>
      <span slot="footer" class="dialog-footer">
        <el-button @click="deleteTaskDialogVisible = false">取 消</el-button>
        <el-button type="primary" @click="deleteTaskSure">确 定</el-button>
      </span>
    </el-dialog>

    <!-- 查看执行结果对话框 -->
    <el-dialog
      title="执行结果"
      :visible.sync="showTaskResultDialogVisible"
      width="90%"
      center
      @close="showTaskResultClose">

      <el-row v-model="resultComputed">
        <el-col :span="5">
          <span>测试用例总数：</span>
          <span>{{ resultComputed.caseTotal }}</span>
        </el-col>
        <el-col :span="4">
          <span>成功：</span>
          <span>{{ resultComputed.caseSuccess }}</span>
        </el-col>
        <el-col :span="4">
          <span>失败：</span>
          <span>{{ resultComputed.caseFail }}</span>
        </el-col>
        <el-col :span="4">
          <span>其他：</span>
          <span>{{ resultComputed.caseOther }}</span>
        </el-col>
        <el-col :span="2">
          <el-progress :text-inside="true" :stroke-width="16" :percentage="resultComputed.passRate" :status="passRateStatus"></el-progress>
        </el-col>
      </el-row>
      <br>
      <el-row>
        <el-col :span="13">
          <span>{{ curTaskName }}</span>
        </el-col>
        <el-col :span="8">
          <span>总耗时：</span>
          <span v-if="parseInt(resultComputed.timeConsume/3600) > 0 ? true : false">{{ parseInt(resultComputed.timeConsume/3600) }} 小时 {{ parseInt((resultComputed.timeConsume%3600)/60) }} 分 {{ resultComputed.timeConsume%60 }} 秒</span>
          <span v-else-if="parseInt(resultComputed.timeConsume/60) > 0 ? true : false">{{ parseInt(resultComputed.timeConsume/60) }} 分 {{ resultComputed.timeConsume%60 }} 秒</span>
          <span v-else>{{ resultComputed.timeConsume%60 }} 秒</span>
        </el-col>
      </el-row>
      <el-table
      :data="testCaseResultData"
      ref="testCaseResultRef"
      @row-click="clicktestCaseResultRow"
      border stripe size="mini">
        <!-- 可展开 测试步骤 部分 -->
        <el-table-column type="expand">
          <template slot-scope="fscope">
            <el-table
            :data="testCaseStepResultData"
            border stripe size="mini">
              <el-table-column type="index" label="序号"></el-table-column>
              <el-table-column prop="name" label="步骤名称"></el-table-column>
              <el-table-column prop="result" label="执行结果">
                <template slot-scope="scope">
                  <el-tag type="success" v-if="scope.row.result == '成功'">成功</el-tag>
                  <el-tag type="danger" v-else-if="scope.row.result == '失败'">失败</el-tag>
                  <el-tag type="info" v-else>{{scope.row.result}}</el-tag>
                </template>
              </el-table-column>
              <el-table-column prop="remark" label="备注"></el-table-column>
              <el-table-column label="操作">
                <template slot-scope="scope">
                  <el-tooltip effect="dark" content="查看详情" placement="top" :enterable="false">
                    <el-button type="primary" size="mini" @click="showTestCaseStepResultDialog(scope.row)">详情</el-button>
                  </el-tooltip>
                </template>
              </el-table-column>
            </el-table>
          </template>
        </el-table-column>

        <el-table-column type="index" label="#"></el-table-column>
        <el-table-column prop="execute_stamp" label="执行时间戳" v-if="false"></el-table-column>
        <el-table-column prop="number" label="测试用例编号"></el-table-column>
        <el-table-column prop="title" label="测试用例标题"></el-table-column>
        <el-table-column prop="project" label="项目"></el-table-column>
        <el-table-column prop="module" label="模块"></el-table-column>
        <el-table-column prop="level" label="优先级"></el-table-column>
        <el-table-column prop="result" label="执行结果">
          <template slot-scope="scope">
                <el-tag type="success" v-if="scope.row.result == '成功'">成功</el-tag>
                <el-tag type="danger" v-else-if="scope.row.result == '失败'">失败</el-tag>
                <el-tag type="info" v-else>{{scope.row.result}}</el-tag>
              </template>
        </el-table-column>
        <el-table-column prop="remark" label="备注"></el-table-column>
        <el-table-column prop="create_time" label="创建时间" :formatter="timeFormat"></el-table-column>
      </el-table>

      <br>
      <!-- 分页 -->
      <el-pagination
        @size-change="subHandleSizeChange"
        @current-change="subHandleCurrentChange"
        :current-page="testCaseResultInfo.curpage"
        :page-sizes="[10, 20, 50, 100]"
        :page-size="testCaseResultInfo.pagesize"
        layout="total, sizes, prev, pager, next, jumper"
        :total="subTotal">
      </el-pagination>
    </el-dialog>

    <!-- 测试步骤详情查看 -->
    <el-dialog
      title="测试步骤详情"
      :visible.sync="showTestCaseStepResultDialogVisible"
      width="80%"
      center
      @close="showTestCaseStepResultDialogClose"
      >
      <el-form label-width="90px" :model="testCaseStepDetailData" size="mini">
        <el-row>
          <el-col :span="11">
            <el-form-item label="步骤名称">
              <el-input v-model="testCaseStepDetailData.name" disabled></el-input>
            </el-form-item>
          </el-col>
          <el-col :span="11">
            <el-form-item label="接口编号">
              <el-input v-model="testCaseStepDetailData.code" disabled></el-input>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row>
          <el-col :span="4">
            <el-form-item label="请求URL">
              <el-input v-model="testCaseStepDetailData.request_type" disabled></el-input>
            </el-form-item>
          </el-col>
          <el-col :span="16">
            <el-input v-model="testCaseStepDetailData.address" size="mini" disabled></el-input>
          </el-col>
          <el-col :span="2">
            <el-input v-model="testCaseStepDetailData.data_type" size="mini" disabled></el-input>
          </el-col>
        </el-row>
        <template>
          <el-tabs tab-position="left" v-model="testCaseStepDetailActiveName" @tab-click="testCaseStepDetailHandleClick">
            <el-tab-pane label="请求头" name="first">
              <el-row>
                <el-col :span="22">
                  <el-input type="textarea" :autosize="{ minRows: 8, maxRows: 16}" v-model="testCaseStepDetailData.request_header"></el-input>
                </el-col>
              </el-row>
            </el-tab-pane>
            <el-tab-pane label="请求体" name="second">
              <el-row>
                <el-col :span="22">
                  <el-input type="textarea" :autosize="{ minRows: 8, maxRows: 16}" v-model="testCaseStepDetailData.request_body"></el-input>
                </el-col>
              </el-row>
            </el-tab-pane>
            <el-tab-pane label="响应头" name="third">
              <el-row>
                <el-col :span="22">
                  <el-input type="textarea" :autosize="{ minRows: 8, maxRows: 16}" v-model="testCaseStepDetailData.response_header"></el-input>
                </el-col>
              </el-row>
            </el-tab-pane>
            <el-tab-pane label="响应体" name="fourth">
              <el-row>
                <el-col :span="22">
                  <el-input type="textarea" :autosize="{ minRows: 8, maxRows: 16}" v-model="testCaseStepDetailData.response_body"></el-input>
                </el-col>
              </el-row>
            </el-tab-pane>
          </el-tabs>
        </template>

        <br>
        <el-row>
          <el-col :span="11">
            <el-form-item label="执行结果">
              <el-input v-model="testCaseStepDetailData.result" disabled></el-input>
            </el-form-item>
          </el-col>
          <el-col :span="11">
            <el-form-item label="创建时间">
              <el-input v-model="testCaseStepDetailData.create_time" disabled></el-input>
            </el-form-item>
          </el-col>
        </el-row>

        <el-row>
          <el-col :span="22">
            <el-form-item label="备注">
              <el-input type="textarea" v-model="testCaseStepDetailData.remark" disabled></el-input>
            </el-form-item>
          </el-col>
        </el-row>

      </el-form>

      <span slot="footer" class="dialog-footer">
        <el-button type="primary" @click="showTestCaseStepResultDialogVisible = false">关 闭</el-button>
      </span>
    </el-dialog>

  </div>
</template>

<script>
  import moment from 'moment'
  export default {
    data() {
      return {
        loading: true,
        baseUrl: this.$root.URL + '/task/',
        baseUrl_case_result: this.$root.URL + '/testcaseresult/',
        baseUrl_step_result: this.$root.URL + '/testcasestepresult/',
        queryInfo: {
          task_name: '',
          curpage: 1,
          pagesize: 10
        },
        total: 0,
        taskListData: [],

        // 删除任务
        deleteTaskDialogVisible: false,
        deleteTaskUrl: '',
        deleteTimeStamp: '',
        // 结果查看
        showTaskResultDialogVisible: false,
        testCaseResultData: [],
        resultComputed: {
          caseTotal: 0,
          caseSuccess: 0,
          caseFail: 0,
          caseOther: 0,
          passRate: 0,
          timeConsume: 0
        },
        curTaskName: '',
        passRateStatus: 'success',
        // 分页
        testCaseResultInfo: {
          execute_stamp: '',
          curpage: 1,
          pagesize: 10
        },
        subTotal: 0,
        // 测试步骤
        testCaseStepResultData: [],

        // 详情查看
        testCaseStepDetailData: {
          name: '',
          code: '',
          request_type: '',
          address: '',
          data_type: '',
          request_header: '',
          request_body: '',
          response_header: '',
          response_body: '',
          result: '',
          remark: '',
          create_time: ''
        },
        showTestCaseStepResultDialogVisible: false,
        testCaseStepDetailActiveName: 'first',
      }
    },
    created() {
      this.getTaskList()
    },
    methods: {
      // 列表
      getTaskList() {
        this.$http.get(this.baseUrl, {params: this.queryInfo}).then(res => {
          if(res.status !== 200) return
          console.log(res)
          this.taskListData = res.data.results
          this.total = res.data.total
          this.loading = false
        })
      },
      // 分页
      handleSizeChange(val) {
        this.queryInfo.pagesize = val
        this.queryInfo.curpage = 1
        this.getTaskList()
      },
      handleCurrentChange(val) {
        this.queryInfo.curpage = val
        this.getTaskList()
      },

      // 删除
      deleteTaskDialog(row) {
        this.deleteTaskDialogVisible = true
        this.deleteTaskUrl = this.baseUrl + row.id + '/'
        this.deleteTimeStamp = row.execute_stamp
      },
      deleteTaskDialogClose() {
        this.deleteTaskUrl = ''
      },
      deleteTaskSure() {
        this.$http.delete(this.deleteTaskUrl).then(res => {
          if(res.status !== 204) {
            this.$message.error('删除失败！')
            return
          }
          // 关联删除测试用例及步骤执行结果
          this.$http.delete(this.baseUrl_case_result + 'deletes/', {params: {execute_stamp: this.deleteTimeStamp}}).then(restc => {
            if(restc.status !== 204) {
              this.$message.error('关联删除测试用例执行结果失败！')
            }
          })
          this.$http.delete(this.baseUrl_step_result + 'deletes/', {params: {execute_stamp: this.deleteTimeStamp}}).then(rests => {
            if(rests.status !== 204) {
              this.$message.error('关联删除测试步骤执行结果失败！')
            }
          })
          this.$message.success('删除成功！')
          this.deleteTaskDialogVisible = false
          this.getTaskList()
        })
      },

      // ---------查看结果----------
      // 查看结果按钮
      showTaskResultDialog(row) {
        this.showTaskResultDialogVisible = true
        this.testCaseResultInfo.execute_stamp = row.execute_stamp
        // 测试用例列表，统计结果
        this.curTaskName = row.task_name
        // 计算耗时
        const time1 = moment(moment(row.start_time).format("YYYY-MM-DD HH:mm:ss"))
        const time2 =  moment(moment(row.end_time).format("YYYY-MM-DD HH:mm:ss"))
        this.resultComputed.timeConsume = time2.diff(time1, "second")

        // 列表
        this.getTestCaseResult()
      },
      // 窗口关闭
      showTaskResultClose() {
        this.testCaseResultData = []
        this.testCaseResultInfo.execute_stamp = ''
        this.resultComputed = {
          caseTotal: 0,
          caseSuccess: 0,
          caseFail: 0,
          caseOther: 0,
          passRate: 0,
          timeConsume: 0
        }
        this.curTaskName = ''
      },
      // 点击表格行触发事件
      clicktestCaseResultRow(row) {
        // 展开用例
        this.$refs.testCaseResultRef.toggleRowExpansion(row)
        // 显示测试步骤列表数据
        this.getTestCaseStepResult(row.number)
      },
      // 获取测试用例执行结果列表, 计算测试用例结果
      getTestCaseResult() {
        if(!this.testCaseResultInfo.execute_stamp) return
        this.$http.get(this.baseUrl_case_result, {params: this.testCaseResultInfo}).then(res => {
          if(res.status !== 200) return
          this.testCaseResultData = res.data.results
          this.subTotal = res.data.total

          // 计算测试执行结果
          if(this.testCaseResultData == []) return
          // 测试用例总数
          this.resultComputed.caseTotal = this.subTotal
          // 测试用例成功、失败、其他数
          for(let i=0;i<this.testCaseResultData.length;i++) {
            let result = this.testCaseResultData[i].result
            if(result == '成功') {
              this.resultComputed.caseSuccess = this.resultComputed.caseSuccess + 1
            }else if(result == '失败') {
              this.resultComputed.caseFail = this.resultComputed.caseFail + 1
            }else{
              this.resultComputed.caseOther = this.resultComputed.caseOther + 1
            }
          }
          // 测试通过率(百分比)
          this.resultComputed.passRate = this.resultComputed.caseTotal == 0 ? 0 : (this.resultComputed.caseSuccess / this.resultComputed.caseTotal).toFixed(2) * 100
          // 通过率条形图颜色
          this.getPassRateStatus()
        })
      },
      getPassRateStatus() {
        if(this.resultComputed.passRate >= 50 && this.resultComputed.passRate <= 80) {
          this.passRateStatus = 'warning'
        }else if (this.resultComputed.passRate < 50) {
          this.passRateStatus = 'exception'
        }else{
          this.passRateStatus = 'success'
        }
      },
      // ------测试步骤-----
      // 列表
      getTestCaseStepResult(number) {
        // 执行时间戳、测试用例编号为空，则跳过
        if(!this.testCaseResultInfo.execute_stamp) return
        if(!number) return
        this.$http.get(this.baseUrl_step_result, {params: {execute_stamp:this.testCaseResultInfo.execute_stamp, number: number}}).then(res => {
          if(res.status !== 200) return
          this.testCaseStepResultData = res.data
        })
      },
      // 详情查看
      showTestCaseStepResultDialog(row) {
        this.showTestCaseStepResultDialogVisible = true
        this.testCaseStepDetailData = row
      },
      // 关闭详情
      showTestCaseStepResultDialogClose() {
        this.testCaseStepDetailData = []
      },
      // 详情页，切换查看请求响应
      testCaseStepDetailHandleClick(tab, event) {

      },

      // 执行结果页面分页
      subHandleSizeChange(val) {
        this.testCaseResultInfo.pagesize = val
        this.testCaseResultInfo.curpage = 1
        this.getTestCaseResult()
      },
      subHandleCurrentChange(val) {
        this.testCaseResultInfo.curpage = val
        this.getTestCaseResult()
      },
      // 时间日期格式
      timeFormat(row, col) {
        let date = row[col.property]
        return date ? moment(date).format("YYYY-MM-DD HH:mm:ss") : ''
      }
    },
    watch: {

    }
  }
</script>

<style>
</style>
