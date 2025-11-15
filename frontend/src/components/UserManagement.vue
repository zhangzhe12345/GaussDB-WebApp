<template>
  <div>
    <h2>用户管理</h2>
    
    <el-card class="box-card">
      <template #header>
        <div class="card-header">
          <span>添加新用户</span>
        </div>
      </template>
      
      <el-form :model="userForm" :rules="rules" ref="userFormRef" label-width="80px">
        <el-form-item label="姓名" prop="name">
          <el-input v-model="userForm.name" placeholder="请输入姓名"></el-input>
        </el-form-item>
        <el-form-item label="邮箱" prop="email">
          <el-input v-model="userForm.email" placeholder="请输入邮箱"></el-input>
        </el-form-item>
        <el-form-item label="年龄" prop="age">
          <el-input-number v-model="userForm.age" :min="1" :max="120"></el-input-number>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="submitUserForm">添加用户</el-button>
          <el-button @click="resetForm">重置</el-button>
        </el-form-item>
      </el-form>
    </el-card>
    
    <el-card class="box-card" style="margin-top: 20px;">
      <template #header>
        <div class="card-header">
          <span>用户列表</span>
          <el-button type="primary" @click="loadUsers">刷新</el-button>
        </div>
      </template>
      
      <el-table :data="users" v-loading="loading" style="width: 100%">
        <el-table-column prop="id" label="ID" width="80"></el-table-column>
        <el-table-column prop="name" label="姓名"></el-table-column>
        <el-table-column prop="email" label="邮箱"></el-table-column>
        <el-table-column prop="age" label="年龄" width="80"></el-table-column>
        <el-table-column prop="created_at" label="创建时间"></el-table-column>
      </el-table>
    </el-card>
  </div>
</template>

<script>
import { userService } from '../services/api'

export default {
  name: 'UserManagement',
  data() {
    return {
      users: [],
      loading: false,
      userForm: {
        name: '',
        email: '',
        age: 18
      },
      rules: {
        name: [
          { required: true, message: '请输入姓名', trigger: 'blur' }
        ],
        email: [
          { required: true, message: '请输入邮箱', trigger: 'blur' },
          { type: 'email', message: '请输入正确的邮箱地址', trigger: 'blur' }
        ]
      }
    }
  },
  mounted() {
    this.loadUsers()
  },
  methods: {
    async loadUsers() {
      this.loading = true
      try {
        const response = await userService.getUsers()
        if (response.data.success) {
          this.users = response.data.data
        } else {
          this.$message.error('加载用户数据失败: ' + response.data.error)
        }
      } catch (error) {
        this.$message.error('请求失败: ' + error.message)
      } finally {
        this.loading = false
      }
    },
    
    async submitUserForm() {
      this.$refs.userFormRef.validate(async (valid) => {
        if (valid) {
          try {
            const response = await userService.createUser(this.userForm)
            if (response.data.success) {
              this.$message.success('用户添加成功')
              this.resetForm()
              this.loadUsers()
            } else {
              this.$message.error('添加用户失败: ' + response.data.error)
            }
          } catch (error) {
            this.$message.error('请求失败: ' + error.message)
          }
        }
      })
    },
    
    resetForm() {
      this.userForm = { name: '', email: '', age: 18 }
      this.$refs.userFormRef?.resetFields()
    }
  }
}
</script>

<style scoped>
.box-card {
  margin-bottom: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style>


