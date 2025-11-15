<template>
  <div>
    <h2>销售分析</h2>
    
    <el-row :gutter="20">
      <el-col :span="12">
        <el-card class="box-card">
          <template #header>
            <div class="card-header">
              <span>产品销售统计</span>
              <el-button type="primary" @click="loadSalesAnalytics">刷新</el-button>
            </div>
          </template>
          
          <el-table :data="salesData" v-loading="loading" style="width: 100%">
            <el-table-column prop="product_id" label="产品ID" width="100"></el-table-column>
            <el-table-column prop="order_count" label="订单数" width="100"></el-table-column>
            <el-table-column prop="total_quantity" label="总销量" width="100"></el-table-column>
            <el-table-column prop="total_revenue" label="总收入" width="120">
              <template #default="scope">
                ¥{{ scope.row.total_revenue }}
              </template>
            </el-table-column>
            <el-table-column prop="avg_order_value" label="平均订单金额" width="140">
              <template #default="scope">
                ¥{{ scope.row.avg_order_value ? scope.row.avg_order_value.toFixed(2) : '0.00' }}
              </template>
            </el-table-column>
          </el-table>
        </el-card>
      </el-col>
      
      <el-col :span="12">
        <el-card class="box-card">
          <template #header>
            <div class="card-header">
              <span>用户消费统计</span>
              <el-button type="primary" @click="loadUserAnalytics">刷新</el-button>
            </div>
          </template>
          
          <el-table :data="userData" v-loading="userLoading" style="width: 100%">
            <el-table-column prop="user_id" label="用户ID" width="100"></el-table-column>
            <el-table-column prop="order_count" label="订单数" width="100"></el-table-column>
            <el-table-column prop="total_spent" label="总消费" width="120">
              <template #default="scope">
                ¥{{ scope.row.total_spent }}
              </template>
            </el-table-column>
          </el-table>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import { analyticsService } from '../services/api'

export default {
  name: 'SalesAnalytics',
  data() {
    return {
      salesData: [],
      userData: [],
      loading: false,
      userLoading: false
    }
  },
  mounted() {
    this.loadSalesAnalytics()
    this.loadUserAnalytics()
  },
  methods: {
    async loadSalesAnalytics() {
      this.loading = true
      try {
        const response = await analyticsService.getSalesAnalytics()
        if (response.data.success) {
          this.salesData = response.data.data
        } else {
          this.$message.error('加载销售数据失败: ' + response.data.error)
        }
      } catch (error) {
        this.$message.error('请求失败: ' + error.message)
      } finally {
        this.loading = false
      }
    },
    
    async loadUserAnalytics() {
      this.userLoading = true
      try {
        const response = await analyticsService.getUserAnalytics()
        if (response.data.success) {
          this.userData = response.data.data
        } else {
          this.$message.error('加载用户数据失败: ' + response.data.error)
        }
      } catch (error) {
        this.$message.error('请求失败: ' + error.message)
      } finally {
        this.userLoading = false
      }
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


