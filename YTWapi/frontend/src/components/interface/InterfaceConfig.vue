<template>
	<div>
		<!-- 面包屑 -->
		<el-breadcrumb separator-class="el-icon-arrow-right">
		  <el-breadcrumb-item :to="{ path: '/home' }">首页</el-breadcrumb-item>
		  <el-breadcrumb-item>接口管理</el-breadcrumb-item>
		  <el-breadcrumb-item>接口配置</el-breadcrumb-item>
		</el-breadcrumb>

    <!-- 卡片区域 -->
    <el-card class="box-card">
      <!-- 查询区 -->
      <el-form :inline="true" :model="queryInfo" class="demo-form-inline" size="mini">
        <el-form-item label="接口编号">
          <el-input v-model="queryInfo.interface_code" placeholder="接口编号" clearable></el-input>
        </el-form-item>
        <el-form-item label="接口名称">
          <el-input v-model="queryInfo.interface_name" placeholder="接口名称" clearable></el-input>
        </el-form-item>
        <el-form-item label="接口地址">
          <el-input v-model="queryInfo.interface_path" placeholder="接口地址" clearable></el-input>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="getInterfaceList">查询</el-button>
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
          <el-table-column prop="pid" label="项目ID" v-if="false"></el-table-column>
          <el-table-column prop="project_code" label="项目英文名"></el-table-column>
          <el-table-column prop="project_name" label="项目名称"></el-table-column>
          <el-table-column prop="describe" label="描述" v-if="false"></el-table-column>
          <el-table-column prop="mid" label="归属模块ID" v-if="false"></el-table-column>
          <el-table-column prop="module_name" label="归属模块"></el-table-column>
          <el-table-column prop="interface_code" label="接口编号"></el-table-column>
          <el-table-column prop="interface_name" label="接口名称"></el-table-column>
          <el-table-column prop="interface_path" label="接口地址"></el-table-column>
          <el-table-column prop="method" label="请求方式"></el-table-column>
          <el-table-column prop="datatype" label="数据格式"></el-table-column>
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

          <el-table-column label="操作" min-width="90px">
            <template slot-scope="scope">
              <el-tooltip effect="dark" content="修改" placement="top" :enterable="false">
                <el-button type="primary" icon="el-icon-edit" size="mini" @click="editInterfaceDialog(scope.row)"></el-button>
              </el-tooltip>
              <el-tooltip effect="dark" content="删除" placement="top" :enterable="false">
                <el-button type="danger" icon="el-icon-delete" size="mini" @click="deleteInterfaceDialog(scope.row)"></el-button>
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
      title="新增接口"
      :visible.sync="addDialogVisible"
      width="50%"
      center @close="addInterfaceClose"
      :close-on-click-modal="false">
      <el-form label-width="100px" :model="interfaceForm"
        :rules="addInterfaceRules" ref="addInterfaceRef">
        <el-form-item label="项目ID" prop="pid">
         <el-select v-model="interfaceForm.pid" placeholder="请选择" @change="relatePreject">
            <el-option
              v-for="item,index in pidValue"
              :key="index"
              :value="item.pid">
              <span>{{ item.pid }}--{{ item.label }}</span>
            </el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="项目英文名" prop="project_code">
          <el-input v-model="interfaceForm.project_code" placeholder="自动带出" disabled></el-input>
        </el-form-item>
        <el-form-item label="项目名称" prop="project_name">
          <el-input v-model="interfaceForm.project_name" placeholder="自动带出" disabled></el-input>
        </el-form-item>
        <el-form-item label="描述" prop="describe">
          <el-input type="textarea" v-model="interfaceForm.describe" placeholder="自动带出" disabled></el-input>
        </el-form-item>

        <el-form-item label="归属模块" prop="mid">
          <el-select v-model="interfaceForm.mid" placeholder="请选择">
              <el-option
                v-for="item,index in moduleOptions"
                :key="index"
                :label="item.label"
                :value="item.mid">
              </el-option>
            </el-select>
        </el-form-item>
        <el-form-item label="接口编号" prop="interface_code">
          <el-input v-model="interfaceForm.interface_code"></el-input>
        </el-form-item>
        <el-form-item label="接口名称" prop="interface_name">
          <el-input v-model="interfaceForm.interface_name"></el-input>
        </el-form-item>
        <el-form-item label="接口地址" prop="interface_path">
          <el-input v-model="interfaceForm.interface_path"></el-input>
        </el-form-item>
        <el-form-item label="请求方式" prop="method">
          <el-select v-model="interfaceForm.method" placeholder="请选择">
              <el-option
                v-for="item,index in allMethod"
                :key="index"
                :value="item">
              </el-option>
            </el-select>
        </el-form-item>
        <el-form-item label="请求头样例" prop="request_header">
          <el-input type="textarea" v-model="interfaceForm.request_header" placeholder="仅用于展示或记录"></el-input>
        </el-form-item>
        <el-form-item label="请求体样例" prop="request_body">
          <el-input type="textarea" v-model="interfaceForm.request_body" placeholder="仅用于展示或记录"></el-input>
        </el-form-item>
        <el-form-item label="响应头样例" prop="response_header">
          <el-input type="textarea" v-model="interfaceForm.response_header" placeholder="仅用于展示或记录"></el-input>
        </el-form-item>
        <el-form-item label="响应体样例" prop="response_body">
          <el-input type="textarea" v-model="interfaceForm.response_body" placeholder="仅用于展示或记录"></el-input>
        </el-form-item>
        <el-form-item label="数据格式" prop="datatype">
          <el-select v-model="interfaceForm.datatype" placeholder="请选择">
              <el-option
                v-for="item,index in allDatatype"
                :key="index"
                :value="item">
              </el-option>
            </el-select>
        </el-form-item>
        <el-form-item label="是否启用" prop="is_enable">
          <el-switch
            v-model="interfaceForm.is_enable ? true : false"
            active-color="#13ce66"
            inactive-color="#ff4949"
            @change="isEnableChange">
          </el-switch>
        </el-form-item>
        <el-form-item label="创建人" prop="creator">
          <el-input v-model="interfaceForm.creator"></el-input>
        </el-form-item>
        <el-form-item label="创建时间" prop="create_time">
          <el-input v-model="interfaceForm.create_time" placeholder="自动带出" disabled></el-input>
        </el-form-item>
       <el-form-item label="更新时间" prop="update_time" v-if="false">
          <el-input v-model="interfaceForm.update_time"></el-input>
        </el-form-item>
        <el-form-item label="备注" prop="remark">
          <el-input type="textarea" v-model="interfaceForm.remark"></el-input>
        </el-form-item>

      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="addDialogVisible = false">取 消</el-button>
        <el-button type="primary" @click="addInterface">确 定</el-button>
      </span>
    </el-dialog>

    <!-- 修改接口 -->
    <el-dialog
      title="修改接口"
      :visible.sync="editDialogVisible"
      width="50%"
      center @close="editInterfaceClose"
      :close-on-click-modal="false">
      <el-form label-width="100px" :model="interfaceForm"
        :rules="addInterfaceRules" ref="editInterfaceRef">
        <el-form-item label="项目ID" prop="pid">
         <el-select v-model="interfaceForm.pid" placeholder="请选择" @change="relatePreject" disabled>
            <el-option
              v-for="item,index in pidValue"
              :key="index"
              :value="item.pid">
              <span>{{ item.pid }}--{{ item.label }}</span>
            </el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="项目英文名" prop="project_code">
          <el-input v-model="interfaceForm.project_code" placeholder="自动带出" disabled></el-input>
        </el-form-item>
        <el-form-item label="项目名称" prop="project_name">
          <el-input v-model="interfaceForm.project_name" placeholder="自动带出" disabled></el-input>
        </el-form-item>
        <el-form-item label="描述" prop="describe">
          <el-input type="textarea" v-model="interfaceForm.describe" placeholder="自动带出" disabled></el-input>
        </el-form-item>

        <el-form-item label="归属模块" prop="mid">
          <el-select v-model="interfaceForm.mid" placeholder="请选择">
            <el-option
              v-for="item,index in moduleOptions"
              :key="index"
              :label="item.label"
              :value="item.mid">
            </el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="接口编号" prop="interface_code">
          <el-input v-model="interfaceForm.interface_code"></el-input>
        </el-form-item>
        <el-form-item label="接口名称" prop="interface_name">
          <el-input v-model="interfaceForm.interface_name"></el-input>
        </el-form-item>
        <el-form-item label="接口地址" prop="interface_path">
          <el-input v-model="interfaceForm.interface_path"></el-input>
        </el-form-item>
        <el-form-item label="请求方式" prop="method">
          <el-select v-model="interfaceForm.method" placeholder="请选择">
              <el-option
                v-for="item,index in allMethod"
                :key="index"
                :value="item">
              </el-option>
            </el-select>
        </el-form-item>
        <el-form-item label="请求头样例" prop="request_header">
          <el-input type="textarea" v-model="interfaceForm.request_header" placeholder="仅用于展示或记录"></el-input>
        </el-form-item>
        <el-form-item label="请求体样例" prop="request_body">
          <el-input type="textarea" v-model="interfaceForm.request_body" placeholder="仅用于展示或记录"></el-input>
        </el-form-item>
        <el-form-item label="响应头样例" prop="response_header">
          <el-input type="textarea" v-model="interfaceForm.response_header" placeholder="仅用于展示或记录"></el-input>
        </el-form-item>
        <el-form-item label="响应体样例" prop="response_body">
          <el-input type="textarea" v-model="interfaceForm.response_body" placeholder="仅用于展示或记录"></el-input>
        </el-form-item>
        <el-form-item label="数据格式" prop="datatype">
          <el-select v-model="interfaceForm.datatype" placeholder="请选择">
              <el-option
                v-for="item,index in allDatatype"
                :key="index"
                :value="item">
              </el-option>
            </el-select>
        </el-form-item>
        <el-form-item label="是否启用" prop="is_enable">
          <el-switch
            v-model="interfaceForm.is_enable ? true : false"
            active-color="#13ce66"
            inactive-color="#ff4949"
            @change="isEnableChange">
          </el-switch>
        </el-form-item>
        <el-form-item label="创建人" prop="creator">
          <el-input v-model="interfaceForm.creator"></el-input>
        </el-form-item>
        <el-form-item label="创建时间" prop="create_time">
          <el-input v-model="interfaceForm.create_time" placeholder="自动带出" disabled></el-input>
        </el-form-item>
        <el-form-item label="更新时间" prop="update_time">
          <el-input v-model="interfaceForm.update_time" placeholder="自动带出" disabled></el-input>
        </el-form-item>
        <el-form-item label="备注" prop="remark">
          <el-input type="textarea" v-model="interfaceForm.remark"></el-input>
        </el-form-item>

      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="editDialogVisible = false">取 消</el-button>
        <el-button type="primary" @click="editInterface">确 定</el-button>
      </span>
    </el-dialog>

    <!-- 删除 -->
    <!-- 删除接口弹窗对话框 -->
    <el-dialog
      title="提示"
      :visible.sync="deleteDialogVisible"
      width="30%"
      @close="deleteInterfaceClose"
      :close-on-click-modal="false">
      <span>删除接口，会关联删除该接口配置的实例以及测试用例中引用该接口实例的步骤，请确认是否删除？</span>
      <span slot="footer" class="dialog-footer">
        <el-button @click="deleteDialogVisible = false">取 消</el-button>
        <el-button type="primary" @click="deleteInterface">确 定</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
  export default {
    data() {
      return {
        baseurl: this.$root.URL + '/interfaceconfig/',
        baseurl_p: this.$root.URL + '/projectconfig/',
        baseurl_m: this.$root.URL + '/module/',
        // 搜索
        queryInfo: {
          interface_code: '',
          interface_name: '',
          interface_path: '',
          curpage: 1,
          pagesize: 10
        },
        total: 0,
        //列表
        tableData: [],
        // 增加
        addDialogVisible: false,
        interfaceForm: {
          pid: null,
          project_code: '',
          project_name: '',
          describe: '',
          mid: null,
          module_name: '',
          interface_code: '',
          interface_name: '',
          interface_path: '',
          method: '',
          request_header: '',
          request_body: '',
          response_header: '',
          response_body: '',
          datatype: '',
          is_enable: 1,
          creator: '',
          create_time: null,
          update_time: null,
          remark: '',
        },
        pidValue: [],
        projectList: [],
        allMethod: ['GET', 'POST', 'PUT', 'DELETE', 'HEAD', 'OPTIONS', 'CONNECT', 'TRACE', 'PATCH'],
        allDatatype: ['JSON', 'XML', 'FORM'],
        // 归属模块
        moduleOptions: [],
        addInterfaceRules: {
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
          mid: [
            {
              required: false
            },
          ],
          interface_code: [
            {
              required: true, message: '接口编号不能为空', trigger: 'blur'
            },
            {
              min: 1, max: 50, message: '1~50个字符', trigger: 'blur'
            }
          ],
          interface_name: [
            {
              required: true, message: '接口名称不能为空', trigger: 'blur'
            },
            {
              min: 1, max: 50, message: '1~50个字符', trigger: 'blur'
            }
          ],
          interface_path: [
            {
              required: true, message: '接口地址不能为空', trigger: 'blur'
            },
            {
              min: 1, max: 500, message: '1~500个字符', trigger: 'blur'
            }
          ],
          method: [
            {
              required: true, message: '请求方式不能为空', trigger: 'blur'
            }
          ],
          request_header: {required: false},
          request_body: {required: false},
          response_header: {required: false},
          response_body: {required: false},
          datatype: [
            {
              required: true, message: '数据格式不能为空', trigger: 'blur'
            }
          ],
          creator: {required: false},
          remark: {required: false},
        },

        // 修改
        editDialogVisible: false,
        editUrl: '',
        updateCount: 0,
        // 删除
        deleteDialogVisible: false,
        deleteUrl: '',
      }
    },
    created() {
      this.getInterfaceList()
      this.getSelected()
    },
    methods: {
      // 列表
      getInterfaceList: function(){
        this.$http.get(this.baseurl, {params: this.queryInfo}).then(res => {
            this.tableData = res.data.results
            this.total = res.data.total
          })
      },
      // 分页
      handleSizeChange(newsize){
        this.queryInfo.pagesize = newsize
        this.queryInfo.curpage = 1
        this.getInterfaceList()

      },
      handleCurrentChange(newpage){
        this.queryInfo.curpage = newpage
        this.getInterfaceList()

      },
      // 新增
      // 新增接口对话框关闭事件：重置对话框内容
      addInterfaceClose: function() {
        this.$refs.addInterfaceRef.resetFields()
        this.updateCount = 0
        this.moduleOptions = []
      },
      // 获取项目信息，处理显示为下拉选项
      getSelected: function() {
        this.$http.get(this.baseurl_p).then(res => {
          if(res.status !== 200) return
          for(let i=0;i<res.data.length;i++){
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
        this.$http.get(this.baseurl_p + this.interfaceForm.pid).then(res => {
          if(res.status !== 200) return

          this.interfaceForm.project_code = res.data.project_code
          this.interfaceForm.project_name = res.data.project_name
          this.interfaceForm.describe = res.data.describe
          // 选择项目后，获取项目对应的归属模块(先清空后获取)
          this.interfaceForm.mid = ''
          this.moduleOptions = []
          this.getModuleOptions()
        })
      },
      // 项目模块（可编辑下拉框），获取下拉选项
      getModuleOptions() {
        this.$http.get(this.baseurl_m, {params: {pid: this.interfaceForm.pid}}).then(res => {
          if(res.status !== 200) return
          for(let m=0;m<res.data.length;m++){
            const value = {
              mid: res.data[m].id,
              label: res.data[m].module_name
            }
            this.moduleOptions.push(value)
          }
        })
      },

      // 点击是否启用
      isEnableChange: function(e){
         e ? this.interfaceForm.is_enable = 1 : this.interfaceForm.is_enable = 0
      },
      //新增接口-点击确定按钮事件
      addInterface: function(){
        // 创建时间、更新时间赋值
        this.interfaceForm.create_time = this.getNowFormatDate()
        this.interfaceForm.update_time = this.getNowFormatDate()
        this.$refs.addInterfaceRef.validate(valid => {
          if(!valid) return
          //发起请求
          this.$http.post(this.baseurl, this.interfaceForm).then(res => {
            if(res.status !== 201) {
              this.$message.error('新增失败！')
              return
            }
            // 自动生成默认的接口实例
            const instanceForm = {
              intf_id: res.data.id,
              case_name: res.data.interface_name + '(default)',
              case_description: '这是自动生成的接口实例',
              is_selected: 1,
              remark: '',
            }
            this.$http.post(this.$root.URL + '/instance/', instanceForm).then(resi => {
              if(resi.status !== 201) {
                this.$message.error('新增接口成功，但生成该接口的接口实例时失败！')
              }
            })
            this.$message.success('新增接口成功！系统自动生成该接口的接口实例！')
            this.addDialogVisible = false
            this.getInterfaceList()
          })
        })
      },

      //修改
      // 监控修改对话窗关闭
      editInterfaceClose: function() {
        this.$refs.editInterfaceRef.resetFields()
        this.updateCount = 0
        this.moduleOptions = []
        },
      // 点击修改按钮
      async editInterfaceDialog(row) {
        this.editDialogVisible = true
        const {data: res} = await this.$http.get(this.baseurl + row.id.toString())
        this.interfaceForm = res
        this.editUrl = this.baseurl + row.id.toString() + '/'
        // 获取归属模块下拉框
        this.getModuleOptions()
      },
      //修改环境-点击确定按钮事件
      editInterface: function(){
        this.interfaceForm.update_time = this.getNowFormatDate()
        this.$refs.editInterfaceRef.validate(valid => {
          if(!valid) return
          if(this.updateCount <= 1) {
            this.editDialogVisible = false
            return
          }
          this.$http.put(this.editUrl, this.interfaceForm).then(res => {
            if(res.status !== 200) {
              this.$message.error('修改失败！')
              return
            }
            this.$message.success('修改接口成功！')
            this.editDialogVisible = false
            this.getInterfaceList()
          })

        })
      },

      // 删除
      // 点击删除按钮事件
      deleteInterfaceDialog(row){
        this.deleteDialogVisible = true
        this.deleteUrl = this.baseurl + row.id.toString() + '/'
      },
      // 监听删除对话框关闭事件
      deleteInterfaceClose: function() {
        this.deleteDialogVisible = false
        this.deleteUrl = ''
      },
      // 删除-确认按钮
      async deleteInterface(){
        const {data: resd} = await this.$http.delete(this.deleteUrl)
        this.$message.success('删除成功！')
        this.deleteDialogVisible = false
        this.getInterfaceList()
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
      // 监听项目信息是否有修改，如果没有修改 updateCount>1。 (打开修改页面时会自动加1，后续每一个修改都会加1）
      interfaceForm: {
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

<style>
</style>
