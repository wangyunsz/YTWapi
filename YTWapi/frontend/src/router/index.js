import Vue from 'vue'
import Router from 'vue-router'
import Login from '@/components/Login'
import Home from '../components/Home.vue'
import Index from '../components/Index.vue'
import Users from '../components/user/Users.vue'
import ProjectConfig from '../components/project/ProjectConfig.vue'
import EnvConfig from '../components/project/EnvConfig.vue'
import InterfaceConfig from '../components/interface/InterfaceConfig.vue'
import Instance from '../components/interface/Instance.vue'
import Business from '../components/interface/Business.vue'
import MakeCase from '../components/testcase/MakeCase.vue'
import TestCase from '../components/testcase/TestCase.vue'
import TestSuite from '../components/testexecute/TestSuite.vue'
import ExecuteConfig from '../components/testexecute/ExecuteConfig.vue'
import Task from '../components/task/Task.vue'


Vue.use(Router)

const router = new Router({
  routes: [
    {
      path: '/',
      name: 'Login',
      component: Login,
      redirect: '/login'
    },
    {
      path: '/login',
      name: 'Login',
      component: Login
    },
    {
      path: '/index',
      name: 'Index',
      component: Index,
      redirect: '/home',
      children: [
        {
          path: '/home',
          name: 'Home',
          component: Home
        },
        {
          path: '/user',
          name: 'Users',
          component: Users
        },
        {
          path: '/projectconfig',
          name: 'ProjectConfig',
          component: ProjectConfig
        },
        {
          path: '/envconfig',
          name: 'EnvConfig',
          component: EnvConfig
        },
        {
          path: '/interfaceconfig',
          name: 'InterfaceConfig',
          component: InterfaceConfig
        },
        {
          path: '/instance',
          name: 'Instance',
          component: Instance
        },
//        {
//          path: '/business',
//          name: 'Business',
//          component: Business
//        },
//        {
//          path: '/makecase',
//          name: 'MakeCase',
//          component: MakeCase
//        },
        {
          path: '/testcase',
          name: 'TestCase',
          component: TestCase
        },
        {
          path: '/testsuite',
          name: 'TestSuite',
          component: TestSuite
        },
        {
          path: '/executeconfig',
          name: 'ExecuteConfig',
          component: ExecuteConfig
        },
        {
          path: '/task',
          name: 'Task',
          component: Task
        },
      ]
    }
  ]
})

// 设置导航守卫
router.beforeEach((to, from, next) => {
  if(to.path === '/login') return next()
  const tokenStr = window.sessionStorage.getItem('token')
  if(!tokenStr) return next('/login')
  next()
})

export default router
