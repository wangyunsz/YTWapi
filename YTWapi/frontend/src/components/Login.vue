<template>
  <div>
    <el-card class="box-card">
      <el-form :model="loginForm" status-icon :rules="loginFormRules" ref="loginFormRef" label-width="80px" class="login-box">
        <h3 class="login-title">欢迎登录</h3>
        <el-form-item label="账号" prop="username">
          <el-input type="text" v-model="loginForm.username" placeholder="请输入账号" ></el-input>
        </el-form-item>
        <el-form-item label="密码" prop="password">
          <el-input type="password" v-model="loginForm.password" placeholder="请输入密码" @keyup.enter.native="submitForm"></el-input>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="submitForm">登陆</el-button>
          <el-button @click="resetForm">重置</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script>
  export default {
    data() {
      return {
        baseUrl: this.$root.URL + '/login/',
        loginForm: {
          username: 'admin',
          password: 'admin'
        },
        loginFormRules: {
          username: [
            {
              required: true, message: '请输入用户名', trigger: 'blur'
            },
            {
              min: 1, max: 50, message: '用户名在1~50个字符之间', trigger: 'blur'
            }
          ],
          password: [
            {
              required: true, message: '请输入密码', trigger: 'blur'
            },
            {
              min: 1, max: 50, message: '密码在1~50个字符之间', trigger: 'blur'
            }
          ],
        }
      }
    },
    methods: {
      submitForm() {
        this.$refs.loginFormRef.validate(valid => {
          if(!valid) return
          this.$http.post(this.baseUrl, this.loginForm).then(res => {
            if(res.status !== 200) {
              this.$message.error('登陆失败！')
              return
            }
            this.$message.success('登陆成功！')
            window.sessionStorage.setItem('token', res.data.access)
            console.log('session:', window.sessionStorage.getItem('token'))
            this.$router.push('/home')
          })
        })
      },
      resetForm() {
        this.$refs.loginFormRef.resetFields()
      }
    }
  }
</script>

<style lang="less" scoped>
  .login-box {
    border: 1px solid #DCDFE6;
    width: 350px;
    margin: 180px auto;
    padding: 35px 35px 15px 35px;
    border-radius: 5px;
    -webkit-border-radius: 5px;
    -moz-border-radius: 5px;
    box-shadow: 0 0 25px #909399;
  }

  .login-title {
    text-align: center;
    margin: 0 auto 40px auto;
    color: #303133;
  }
</style>
