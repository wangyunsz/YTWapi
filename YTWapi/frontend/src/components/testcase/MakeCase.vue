<template>
  <div>
    <!-- 面包屑 -->
    <el-breadcrumb separator-class="el-icon-arrow-right">
      <el-breadcrumb-item :to="{ path: '/home' }">首页</el-breadcrumb-item>
      <el-breadcrumb-item>测试管理</el-breadcrumb-item>
      <el-breadcrumb-item>录制生成用例</el-breadcrumb-item>
    </el-breadcrumb>

    <!-- 列表数据区 -->
    <template>
      <el-table
        :data="makeCaseData"
        border
        stripe
        ref="makeCaseRef"
        @row-click="clickMakeCaseRow"
        >
        <!-- 可展开 接口列表 -->
        <el-table-column type="expand">
          <template slot-scope="fscope">
            <el-table
            :data="makeCaseInterfaceListData"
            border stripe size="mini">
              <el-table-column type="index" label="序号"></el-table-column>
              <el-table-column prop="mc_id" label="录制脚本文件ID" v-if="false"></el-table-column>
              <el-table-column prop="step_no" label="步骤顺序" v-if="false"></el-table-column>
              <el-table-column prop="req_addr" label="请求地址"></el-table-column>
              <el-table-column prop="req_type" label="请求方式"></el-table-column>
              <el-table-column prop="case_instance" label="选择接口实例">
                <template slot-scope="scope">
                  <el-select v-model="scope.row.instance_id" placeholder="请选择">
                    <el-option
                      v-for="item in caseInstanceOptionsList[scope.row.id-1]"
                      :key="item.value"
                      :label="item.label"
                      :value="item.value">
                    </el-option>
                  </el-select>
                </template>
              </el-table-column>
              <el-table-column label="操作">
                <template slot-scope="scope">
                  <el-tooltip effect="dark" content="查看详情" placement="top" :enterable="false">
                    <el-button type="primary" size="mini" @click="showMakeCaseInterfaceDialog(scope.row)">详情</el-button>
                  </el-tooltip>
                  <el-tooltip effect="dark" content="删除" placement="top" :enterable="false">
                    <el-button type="danger" icon="el-icon-delete" size="mini" @click="deleteMakeCaseInterfaceDialog(scope.row)"></el-button>
                  </el-tooltip>
                </template>
              </el-table-column>
            </el-table>
          </template>
        </el-table-column>
        <el-table-column type="index" label="#"></el-table-column>
        <el-table-column prop="name" label="名称"></el-table-column>
        <el-table-column prop="create_time" label="创建时间"></el-table-column>
        <el-table-column label="操作">
          <template slot-scope="scope">
            <el-tooltip effect="dark" content="生成用例" placement="top" :enterable="false">
              <el-button type="success" size="mini" @click="makeCaseDialog(scope.row)">生成用例</el-button>
            </el-tooltip>
            <el-tooltip effect="dark" content="删除" placement="top" :enterable="false">
              <el-button type="danger" icon="el-icon-delete" size="mini" @click="deleteMakeCaseDialog(scope.row)"></el-button>
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

    <!-- 接口详情查看 -->
    <el-dialog
      title="接口详情"
      :visible.sync="showMakeCaseInterfaceDialogVisible"
      width="60%"
      center
      @close="showMakeCaseInterfaceDialogClose"
      >
      <el-form label-width="90px" :model="makeCaseInterfaceDialogData" size="mini">

        <el-row>
          <el-col :span="5">
            <el-form-item label="请求URL">
              <el-input v-model="makeCaseInterfaceDialogData.req_type" disabled></el-input>
            </el-form-item>
          </el-col>
          <el-col :span="17">
            <el-input v-model="makeCaseInterfaceDialogData.req_addr" size="mini" disabled></el-input>
          </el-col>
        </el-row>
        <template>
          <el-tabs tab-position="left" v-model="makeCaseInterfaceDetailActiveName" @tab-click="makeCaseInterfaceDetailHandleClick">
            <el-tab-pane label="请求头" name="first">
              <el-row>
                <el-col :span="22">
                  <el-input type="textarea" :autosize="{ minRows: 8, maxRows: 16}" v-model="makeCaseInterfaceDialogData.req_header" disabled></el-input>
                </el-col>
              </el-row>
            </el-tab-pane>
            <el-tab-pane label="请求体" name="second">
              <el-row>
                <el-col :span="22">
                  <el-input type="textarea" :autosize="{ minRows: 8, maxRows: 16}" v-model="makeCaseInterfaceDialogData.req_body" disabled></el-input>
                </el-col>
              </el-row>
            </el-tab-pane>
            <el-tab-pane label="响应头" name="third">
              <el-row>
                <el-col :span="22">
                  <el-input type="textarea" :autosize="{ minRows: 8, maxRows: 16}" v-model="makeCaseInterfaceDialogData.res_header" disabled></el-input>
                </el-col>
              </el-row>
            </el-tab-pane>
            <el-tab-pane label="响应体" name="fourth">
              <el-row>
                <el-col :span="22">
                  <el-input type="textarea" :autosize="{ minRows: 8, maxRows: 16}" v-model="makeCaseInterfaceDialogData.res_body" disabled></el-input>
                </el-col>
              </el-row>
            </el-tab-pane>
          </el-tabs>
        </template>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button type="primary" @click="showMakeCaseInterfaceDialogVisible = false">关 闭</el-button>
      </span>
    </el-dialog>

    <!-- 删除脚本生成用例文件 -->
   <el-dialog
      title="提示"
      :visible.sync="deleteMakeCaseDialogVisible"
      width="30%"
      @close="deleteMakeCaseDialogClose"
      :close-on-click-modal="false">
      <span>请确认是否删除？</span>
      <span slot="footer" class="dialog-footer">
        <el-button @click="deleteMakeCaseDialogVisible = false">取 消</el-button>
        <el-button type="primary" @click="deleteMakeCaseSure">确 定</el-button>
      </span>
    </el-dialog>

    <!-- 删除生成用例接口 -->
    <el-dialog
      title="提示"
      :visible.sync="deleteMakeCaseInterfaceDialogVisible"
      width="30%"
      @close="deleteMakeCaseInterfaceDialogClose"
      :close-on-click-modal="false">
      <span>请确认是否删除？</span>
      <span slot="footer" class="dialog-footer">
        <el-button @click="deleteMakeCaseInterfaceDialogVisible = false">取 消</el-button>
        <el-button type="primary" @click="deleteMakeCaseInterfaceSure">确 定</el-button>
      </span>
    </el-dialog>

    <!-- 生成用例窗口 -->
    <el-dialog
      title="生成用例"
      :visible.sync="makeCaseDialogVisible"
      center
      @close="makeCaseDialogClose">
      <el-form label-width="120px" :model="addTestCaseList"
        :rules="addTestCaseListRules" ref="addTestCaseListRef">
        <el-row>
          <el-col :span="12">
            <el-form-item label="测试用例编号" prop="number">
              <el-input v-model="addTestCaseList.number" placeholder="请输入"></el-input>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="测试用例标题" prop="title">
              <el-input v-model="addTestCaseList.title" placeholder="请输入"></el-input>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row>
          <el-col :span="12">
            <el-form-item label="归属项目模块" prop="mid">
              <el-cascader
                v-model="relate_id"
                :options="moduleOptions"
                :props="{ expandTrigger: 'hover' }"
                @change="moduleHandleChange"
                clearable>
              </el-cascader>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="业务流程" prop="bsid">
              <el-input v-model="addTestCaseList.bsid" placeholder="请输入"></el-input>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row>
          <el-col :span="12">
            <el-form-item label="优先级" prop="level">
              <el-select v-model="addTestCaseList.level" placeholder="请选择">
                  <el-option
                    v-for="item,index in level"
                    :key="index"
                    :value="item">
                  </el-option>
                </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="是否启用" prop="is_enable">
              <el-switch
                v-model="addTestCaseList.is_enable ? true : false"
                active-color="#13ce66"
                inactive-color="#ff4949"
                @change="addIsEnableChange">
              </el-switch>
            </el-form-item>
          </el-col>
        </el-row>

        <el-row>
          <el-col :span="12">
            <el-form-item label="创建人" prop="creator">
              <el-input v-model="addTestCaseList.creator" placeholder="请输入"></el-input>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="创建时间" prop="create_time">
              <el-input v-model="addTestCaseList.create_time" placeholder="自动生成" disabled></el-input>
            </el-form-item>
          </el-col>
        </el-row>

        <el-form-item label="更新时间" prop="update_time" v-if="false">
          <el-input v-model="addTestCaseList.update_time" placeholder="自动生成" disabled></el-input>
        </el-form-item>
        <el-form-item label="备注" prop="remark">
          <el-input type="textarea" v-model="addTestCaseList.remark" placeholder="请输入"></el-input>
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="makeCaseDialogVisible = false">取 消</el-button>
        <el-button type="primary" @click="makeCaseNext">下一步</el-button>
      </span>
    </el-dialog>



  </div>
</template>

<script>
  export default {
    data() {
      return {
        baseUrl: this.$root.URL + '/makecase/',
        baseUrl_interface: this.$root.URL + '/makecaseinterface/',
        makeCaseData: [],
        queryInfo: {
          curpage: 1,
          pagesize: 10
        },
        total: 0,
        // 生成用例
        makeCaseDialogVisible: false,
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
        level: [0,1,2,3],
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

        //删除
        deleteMakeCaseDialogVisible: false,
        deleteMakeCaseUrl: '',

        // 展开行id标记
        curRowId: null,
        // 生成用例接口
        makeCaseInterfaceListData: [],
        makeCaseInterfaceDialogData: [],
        showMakeCaseInterfaceDialogVisible: false,
        makeCaseInterfaceDetailActiveName: 'first',
        deleteMakeCaseInterfaceDialogVisible: false,
        deleteMakeCaseInterfaceUrl: '',

        caseInstanceOptionsList: [
          [{
            value: '选项1',
            label: '黄金糕'
          }, {
            value: '选项2',
            label: '双皮奶'
          }],
          [{
            value: '选项1',
            label: '黄金糕'
          }, {
            value: '选项2',
            label: '双皮奶'
          }, {
            value: '选项3',
            label: '蚵仔煎'
          }],
          [{
            value: '选项4',
            label: '龙须面'
          }, {
            value: '选项5',
            label: '北京烤鸭'
          }],
        ],
      }
    },
    created() {
      this.getMakeCaseList()
    },
    methods: {
      // 列表
      getMakeCaseList() {
        this.$http.get(this.baseUrl, {params: this.queryInfo}).then(res => {
          if(res.status !== 200) return
          console.log(res)
          this.makeCaseData = res.data.results
          this.total = res.data.total
        })
      },
      // 分页
      handleSizeChange(val) {
        this.queryInfo.pagesize = val
        this.queryInfo.curpage = 1
        this.getMakeCaseList()
      },
      handleCurrentChange(val) {
        this.queryInfo.curpage = val
        this.getMakeCaseList()
      },
      // 点击表格行触发事件
      clickMakeCaseRow(row) {
        // 展开行
        this.$refs.makeCaseRef.toggleRowExpansion(row)
        // 显示接口列表数据（防止重复请求，点击行触发关闭展开页时，不触发）
        if (this.curRowId == row.id) return
        this.getMakeCaseInterfaceList(row.id)
        this.curRowId = row.id
      },
      // 列表
      getMakeCaseInterfaceList(id) {
        this.$http.get(this.baseUrl_interface, {params: {mc_id: id}}).then(res => {
          if(res.status !== 200) return
          console.log(res)
          this.makeCaseInterfaceListData = res.data
        })
      },
      //
      showMakeCaseInterfaceDialog(row) {
        this.showMakeCaseInterfaceDialogVisible = true
        this.makeCaseInterfaceDialogData = row
      },
      showMakeCaseInterfaceDialogClose() {
        this.makeCaseInterfaceDialogData = []
      },
      // 详情页，切换查看请求响应
      makeCaseInterfaceDetailHandleClick(tab, event) {

      },
      // 点击删除接口
      deleteMakeCaseInterfaceDialog(row) {
        this.deleteMakeCaseInterfaceDialogVisible = true
        this.deleteMakeCaseInterfaceUrl = this.baseUrl_interface + row.id + '/'
      },
      // 监听删除窗口关闭
      deleteMakeCaseInterfaceDialogClose() {
        this.deleteMakeCaseInterfaceUrl = ''
      },
      // 删除确定
      deleteMakeCaseInterfaceSure() {
        this.$http.delete(this.deleteMakeCaseInterfaceUrl).then(res => {
          if(res.status !== 204) {
            this.$message.error('删除失败！')
            return
          }
          this.$message.success('删除成功！')
          this.deleteMakeCaseInterfaceDialogVisible = false
          this.getMakeCaseInterfaceList(this.curRowId)
        })
      },
      // 生成用例
      makeCaseDialog(row) {
        this.makeCaseDialogVisible = true
        this.getModuleOptions()
        this.addTestCaseList.title = row.name
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
      // 监控窗口关闭
      makeCaseDialogClose() {
        this.relate_id = null
        this.moduleOptions = []
        this.addTestCaseList = {
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
      },
      // 下一步
      makeCaseNext() {
        this.$refs.addTestCaseListRef.validate(async valid => {
          if(!valid) return
          // 查询，名称不能重复
          const {data: resq} = await this.$http.get(this.$root.URL + '/testcase/', {params: {number: this.addTestCaseList.number}})
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
          this.$http.post(this.$root.URL + '/testcase/', this.addTestCaseList).then(res => {
            if(res.status !== 201) {
              this.$message.error('新增失败！')
              return
            }
            this.$message.success('新增成功！')
            this.makeCaseDialogVisible = false
            // 刷新界面
            this.getMakeCaseList()
          })

        })
      },


      // 删除录制用例文件
      deleteMakeCaseDialog(row) {
        this.deleteMakeCaseDialogVisible = true
        this.deleteMakeCaseUrl = this.baseUrl + row.id + '/'
      },
      // 监听删除窗口关闭
      deleteMakeCaseDialogClose() {
        this.deleteMakeCaseUrl = ''
      },
      // 删除确定
      deleteMakeCaseSure() {
        this.$http.delete(this.deleteMakeCaseUrl).then(res => {
          if(res.status !== 204) {
            this.$message.error('删除失败！')
            return
          }
          this.$message.success('删除成功！')
          this.deleteMakeCaseDialogVisible = false
          this.getMakeCaseList()
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
    }
  }
</script>

<style lang="less" scoped>
</style>
