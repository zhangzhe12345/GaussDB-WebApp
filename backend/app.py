from flask import Flask, request, jsonify
from flask_cors import CORS
from spark_connector import GaussDBConnector, get_jdbc_connection
import json
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)

# 初始化数据库连接
environment = os.getenv("ENVIRONMENT", "local")
db_connector = GaussDBConnector(environment=environment)

@app.route('/api/health', methods=['GET'])
def health_check():
    """健康检查接口"""
    try:
        # 尝试连接数据库
        conn = get_jdbc_connection(environment)
        conn.close()
        return jsonify({"status": "healthy", "database": "connected"})
    except Exception as e:
        return jsonify({"status": "unhealthy", "database": "disconnected", "error": str(e)}), 500

@app.route('/api/users', methods=['GET'])
def get_users():
    """获取用户列表 - 使用Spark读取或直接JDBC"""
    try:
        result = db_connector.read_data("users")
        # 如果返回的是列表（JDBC模式），直接使用；如果是DataFrame（Spark模式），需要转换
        if isinstance(result, list):
            users = result
        else:
            # Spark DataFrame模式
            users = [json.loads(row) for row in result.toJSON().collect()]
        return jsonify({"success": True, "data": users})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/users', methods=['POST'])
def create_user():
    """创建新用户"""
    try:
        data = request.json
        if not data or not data.get('name') or not data.get('email'):
            return jsonify({"success": False, "error": "姓名和邮箱是必填项"}), 400
        
        conn = get_jdbc_connection(environment)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (name, email, age, created_at) VALUES (%s, %s, %s, CURRENT_TIMESTAMP) RETURNING id",
            (data.get('name'), data.get('email'), data.get('age', 18))
        )
        user_id = cursor.fetchone()[0]
        conn.commit()
        cursor.close()
        conn.close()
        
        return jsonify({"success": True, "message": "用户创建成功", "id": user_id})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/products', methods=['GET'])
def get_products():
    """获取产品列表 - 使用Spark读取或直接JDBC"""
    try:
        result = db_connector.read_data("products")
        # 如果返回的是列表（JDBC模式），直接使用；如果是DataFrame（Spark模式），需要转换
        if isinstance(result, list):
            products = result
        else:
            # Spark DataFrame模式
            products = [json.loads(row) for row in result.toJSON().collect()]
        return jsonify({"success": True, "data": products})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/products', methods=['POST'])
def create_product():
    """创建新产品"""
    try:
        data = request.json
        if not data or not data.get('name') or not data.get('price'):
            return jsonify({"success": False, "error": "产品名称和价格是必填项"}), 400
        
        conn = get_jdbc_connection(environment)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO products (name, price, category, stock_quantity, created_at) VALUES (%s, %s, %s, %s, CURRENT_TIMESTAMP) RETURNING id",
            (data.get('name'), data.get('price'), data.get('category', ''), data.get('stock_quantity', 0))
        )
        product_id = cursor.fetchone()[0]
        conn.commit()
        cursor.close()
        conn.close()
        
        return jsonify({"success": True, "message": "产品创建成功", "id": product_id})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/orders', methods=['GET'])
def get_orders():
    """获取订单列表 - 使用Spark读取或直接JDBC"""
    try:
        result = db_connector.read_data("orders")
        # 如果返回的是列表（JDBC模式），直接使用；如果是DataFrame（Spark模式），需要转换
        if isinstance(result, list):
            orders = result
        else:
            # Spark DataFrame模式
            orders = [json.loads(row) for row in result.toJSON().collect()]
        return jsonify({"success": True, "data": orders})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/orders', methods=['POST'])
def create_order():
    """创建订单"""
    try:
        data = request.json
        if not data or not data.get('user_id') or not data.get('product_id') or not data.get('quantity'):
            return jsonify({"success": False, "error": "用户ID、产品ID和数量是必填项"}), 400
        
        # 获取产品价格
        conn = get_jdbc_connection(environment)
        cursor = conn.cursor()
        cursor.execute("SELECT price FROM products WHERE id = %s", (data.get('product_id'),))
        product = cursor.fetchone()
        if not product:
            cursor.close()
            conn.close()
            return jsonify({"success": False, "error": "产品不存在"}), 404
        
        price = float(product[0])
        quantity = int(data.get('quantity'))
        total_price = price * quantity
        
        cursor.execute(
            "INSERT INTO orders (user_id, product_id, quantity, total_price, order_date) VALUES (%s, %s, %s, %s, CURRENT_TIMESTAMP) RETURNING id",
            (data.get('user_id'), data.get('product_id'), quantity, total_price)
        )
        order_id = cursor.fetchone()[0]
        conn.commit()
        cursor.close()
        conn.close()
        
        return jsonify({"success": True, "message": "订单创建成功", "id": order_id, "total_price": total_price})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/analytics/sales', methods=['GET'])
def get_sales_analytics():
    """销售数据分析 - 使用Spark进行复杂查询或直接SQL"""
    try:
        if db_connector.use_spark:
            # 使用Spark进行聚合分析
            orders_df = db_connector.read_data("orders")
            from pyspark.sql import functions as F
            
            analytics_df = orders_df.groupBy("product_id") \
                .agg(
                    F.count("*").alias("order_count"),
                    F.sum("quantity").alias("total_quantity"),
                    F.sum("total_price").alias("total_revenue"),
                    F.avg("total_price").alias("avg_order_value")
                ) \
                .orderBy(F.desc("total_revenue"))
            
            analytics = [json.loads(row) for row in analytics_df.toJSON().collect()]
        else:
            # 使用直接SQL进行聚合分析
            query = """
                SELECT 
                    product_id,
                    COUNT(*) as order_count,
                    SUM(quantity) as total_quantity,
                    SUM(total_price) as total_revenue,
                    AVG(total_price) as avg_order_value
                FROM orders
                GROUP BY product_id
                ORDER BY total_revenue DESC
            """
            analytics = db_connector.execute_query(query)
        
        return jsonify({"success": True, "data": analytics})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/analytics/users', methods=['GET'])
def get_user_analytics():
    """用户数据分析 - 使用Spark或直接SQL"""
    try:
        if db_connector.use_spark:
            # 使用Spark进行聚合分析
            orders_df = db_connector.read_data("orders")
            from pyspark.sql import functions as F
            
            user_stats = orders_df.groupBy("user_id") \
                .agg(
                    F.count("*").alias("order_count"),
                    F.sum("total_price").alias("total_spent")
                )
            
            user_stats_list = [json.loads(row) for row in user_stats.toJSON().collect()]
        else:
            # 使用直接SQL进行聚合分析
            query = """
                SELECT 
                    user_id,
                    COUNT(*) as order_count,
                    SUM(total_price) as total_spent
                FROM orders
                GROUP BY user_id
            """
            user_stats_list = db_connector.execute_query(query)
        
        return jsonify({"success": True, "data": user_stats_list})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)


