import axios from 'axios'

const API_BASE_URL = process.env.NODE_ENV === 'production' 
  ? '/api'  // 生产环境使用相对路径，由nginx代理
  : 'http://localhost:5000/api'  // 开发环境

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000
})

export const userService = {
  getUsers: () => api.get('/users'),
  createUser: (userData) => api.post('/users', userData)
}

export const productService = {
  getProducts: () => api.get('/products'),
  createProduct: (productData) => api.post('/products', productData)
}

export const orderService = {
  getOrders: () => api.get('/orders'),
  createOrder: (orderData) => api.post('/orders', orderData)
}

export const analyticsService = {
  getSalesAnalytics: () => api.get('/analytics/sales'),
  getUserAnalytics: () => api.get('/analytics/users')
}

export default api


