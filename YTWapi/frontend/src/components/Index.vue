<template>
  <el-container class="home-container">
    <!-- 头部区 -->
    <el-header>
      <div>
        <img style="width: 60px; height: 60px" src="../assets/img/head.png" fit="fill" alt="">
        <span>YTWapi测试平台</span>
      </div>
      <el-button type="info" @click="logout" size="mini">退出</el-button>
    </el-header>
    <el-container>
      <!-- 左侧区 -->
      <el-aside :width="isCollapse ? '64px' : '200px' ">
        <!-- 折叠、展开导航栏 -->
        <div class="toggle-button" @click="toggleCollapse">
          <i :class="isCollapse ? 'el-icon-s-unfold' : 'el-icon-s-fold' "></i>
        </div>

        <el-menu background-color="#333744" text-color="#fff"
                active-text-color="#409eff" unique-opened :collapse="isCollapse"
                :collapse-transition="false" :default-active="this.$router.path" router>
          <!-- 一级菜单 -->
          <el-submenu :index="item.name" v-for="item,index in menulist" :key="index">
            <template slot="title">
              <i :class="item.icon"></i>
              <span>{{item.autoName}}</span>
            </template>
            <!-- 二级菜单 -->
            <el-menu-item :index="subitem.name" v-for="subitem,subindex in item.children" :key="subindex">
              <template slot="title">
                <i :class="subitem.icon"></i>
                <span>{{subitem.autoName}}</span>
              </template>
            </el-menu-item>
          </el-submenu>
        </el-menu>
      </el-aside>
      <el-container>
        <!-- 主体区 -->
        <el-main>
          <router-view></router-view>
        </el-main>
        <!-- 底部区 -->
        <el-footer>
          <span>© 2020 wyun 版权所有&nbsp;</span>
          <el-link href="https://beian.miit.gov.cn/" target="_blank">&nbsp;粤ICP备20051367号</el-link>
        </el-footer>
      </el-container>
    </el-container>
  </el-container>
</template>

<script>
  export default {
    data() {
      return {
        // 左侧菜单数据
        menulist: [
          // {
          //   name: 'home',
          //   icon: 'el-icon-s-home',
          //   autoName: '首页'
          // },
          // {
          //   name: 'users',
          //   icon: 'el-icon-user-solid',
          //   autoName: '用户管理'
          // },
          {
            name: 'project',
            icon: 'el-icon-s-management',
            autoName: '项目管理',
            children: [
              {
                name: 'projectconfig',
                icon: 'el-icon-menu',
                autoName: '项目配置'
              },
              {
                name: 'envconfig',
                icon: 'el-icon-menu',
                autoName: '环境配置'
              }
            ]
          },
          {
            name: 'interface',
            icon: 'el-icon-s-platform',
            autoName: '接口管理',
            children: [
              {
                name: 'interfaceconfig',
                icon: 'el-icon-menu',
                autoName: '接口配置'
              },
              {
                name: 'instance',
                icon: 'el-icon-menu',
                autoName: '接口实例'
              },
              // {
              //   name: 'business',
              //   icon: 'el-icon-menu',
              //   autoName: '业务流程'
              // }
            ]
          },
          {
            name: 'testcase',
            icon: 'el-icon-s-order',
            autoName: '用例管理',
            children: [
              // {
              //   name: 'makecase',
              //   icon: 'el-icon-menu',
              //   autoName: '录制生成用例'
              // },
              {
                name: 'testcase',
                icon: 'el-icon-menu',
                autoName: '测试用例'
              },
            ]
          },
          {
            name: 'execute',
            icon: 'el-icon-s-operation',
            autoName: '执行管理',
            children: [
              {
                name: 'testsuite',
                icon: 'el-icon-menu',
                autoName: '测试集'
              },
              {
                name: 'executeconfig',
                icon: 'el-icon-menu',
                autoName: '执行设置'
              },
            ]
          },
          {
            name: 'taskmanagement',
            icon: 'el-icon-time',
            autoName: '任务管理',
            children: [
              {
                name: 'task',
                icon: 'el-icon-menu',
                autoName: '任务列表'
              },
            ]
          }
        ],
        isCollapse: false
      }
    },
    methods: {
      logout: function(){
        window.sessionStorage.clear()
        this.$router.push('/login')
      },
      // 切换菜单折叠、展开
      toggleCollapse: function(){
        this.isCollapse = !this.isCollapse
      }
    }
  }
</script>

<style lang="less" scoped>
  .home-container {
    height: 100%;
  }
  .el-header {
    background-color: #373d41;
    display: flex;
    justify-content: space-between;
    padding-left: 0;
    align-items: center;
    color: #fff;
    font-size: 16px;
    > div {
      display: flex;
      align-items: center;
    }
    span {
      margin-left: 15px;
    }
  }
  .el-aside {
    background-color: #333744;
    .toggle-button {
      background-color: #4a5064;
      font-size: 20px;
      line-height: 24px;
      color: #fff;
      text-align: center;
      cursor: pointer;
    }
    .el-menu {
      border-right: 0;
    }
  }
  .el-main {
    background-color: #eaedf1;
  }
  .el-footer {
    text-align: left;
    display: flex;
    align-items: center;
    font-size: 12px;
    .el-link {
      font-size: 12px;
    }
  }
</style>
