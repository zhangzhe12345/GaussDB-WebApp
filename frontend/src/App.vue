<template>
  <div id="app">
    <el-container>
      <el-header>
        <h1>GaussDB Web Application</h1>
        <el-menu mode="horizontal" :default-active="activeIndex" @select="handleSelect">
          <el-menu-item index="1">用户管理</el-menu-item>
          <el-menu-item index="2">产品管理</el-menu-item>
          <el-menu-item index="3">订单管理</el-menu-item>
          <el-menu-item index="4">销售分析</el-menu-item>
        </el-menu>
      </el-header>
      
      <el-main>
        <router-view></router-view>
      </el-main>
    </el-container>
  </div>
</template>

<script>
export default {
  name: 'App',
  data() {
    return {
      activeIndex: '1'
    }
  },
  methods: {
    handleSelect(key) {
      const routes = ['', 'users', 'products', 'orders', 'analytics']
      this.$router.push(`/${routes[key]}`)
      this.activeIndex = key
    }
  },
  mounted() {
    // 根据当前路由设置激活菜单
    const path = this.$route.path
    if (path === '/users' || path === '/') this.activeIndex = '1'
    else if (path === '/products') this.activeIndex = '2'
    else if (path === '/orders') this.activeIndex = '3'
    else if (path === '/analytics') this.activeIndex = '4'
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

.el-header {
  background-color: #409EFF;
  color: white;
  text-align: center;
  line-height: 60px;
  padding: 0;
}

.el-header h1 {
  margin: 0;
  padding: 10px 0;
  font-size: 24px;
}

.el-menu {
  background-color: #409EFF;
  border-bottom: none;
}

.el-menu-item {
  color: white !important;
}

.el-menu-item.is-active {
  background-color: #66b1ff !important;
  color: white !important;
}

.el-main {
  padding: 20px;
}
</style>


