from pyspark.sql import SparkSession
from pyspark import SparkConf
import jaydebeapi
import os
from gaussdb_config import GaussDBConfig

class GaussDBConnector:
    """GaussDB Spark连接器（支持降级到直接JDBC）"""
    
    def __init__(self, environment=None):
        if environment is None:
            environment = os.getenv("ENVIRONMENT", "local")
        self.config = GaussDBConfig.get_config(environment)
        self.spark = None
        self.use_spark = False
        self._init_spark()
        
    def _init_spark(self):
        """尝试创建Spark会话，失败时降级到直接JDBC"""
        try:
            self.spark = self._create_spark_session()
            self.use_spark = True
            print("Spark 会话创建成功")
        except Exception as e:
            print(f"Spark 初始化失败，将使用直接 JDBC 连接: {str(e)}")
            self.spark = None
            self.use_spark = False
        
    def _create_spark_session(self):
        """创建Spark会话"""
        conf = SparkConf().setAppName("GaussDB-WebApp") \
            .set("spark.executor.memory", "1g") \
            .set("spark.driver.memory", "1g") \
            .set("spark.sql.adaptive.enabled", "true")
        
        # 尝试设置JDBC驱动路径（如果存在）
        jdbc_jar = "/opt/spark/jars/postgresql-42.6.0.jar"
        if os.path.exists(jdbc_jar):
            conf.set("spark.jars", jdbc_jar)
        
        return SparkSession.builder \
            .config(conf=conf) \
            .getOrCreate()
    
    def read_data(self, table_name):
        """使用Spark读取GaussDB数据，失败时使用直接JDBC"""
        if self.use_spark and self.spark:
            try:
                df = self.spark.read \
                    .format("jdbc") \
                    .option("url", self.config["url"]) \
                    .option("dbtable", table_name) \
                    .option("user", self.config["user"]) \
                    .option("password", self.config["password"]) \
                    .option("driver", self.config["driver"]) \
                    .load()
                return df
            except Exception as e:
                print(f"Spark读取数据错误: {str(e)}，降级到直接JDBC")
                return self._read_data_jdbc(table_name)
        else:
            return self._read_data_jdbc(table_name)
    
    def _read_data_jdbc(self, table_name):
        """使用直接JDBC读取数据（返回列表格式）"""
        import os
        environment = os.getenv("ENVIRONMENT", "local")
        # 使用已有的配置创建连接
        import psycopg2
        conn = psycopg2.connect(
            host=self.config["host"],
            port=self.config["port"],
            database=self.config["database"],
            user=self.config["user"],
            password=self.config["password"]
        )
        try:
            cursor = conn.cursor()
            cursor.execute(f"SELECT * FROM {table_name}")
            columns = [desc[0] for desc in cursor.description]
            rows = cursor.fetchall()
            cursor.close()
            # 转换为字典列表格式
            result = [dict(zip(columns, row)) for row in rows]
            return result
        finally:
            conn.close()
    
    def write_data(self, df, table_name, mode="append"):
        """使用Spark写入GaussDB数据，失败时使用直接JDBC"""
        if self.use_spark and self.spark:
            try:
                df.write \
                    .format("jdbc") \
                    .option("url", self.config["url"]) \
                    .option("dbtable", table_name) \
                    .option("user", self.config["user"]) \
                    .option("password", self.config["password"]) \
                    .option("driver", self.config["driver"]) \
                    .mode(mode) \
                    .save()
            except Exception as e:
                print(f"Spark写入数据错误: {str(e)}")
                raise
        else:
            raise NotImplementedError("直接JDBC写入功能需要单独实现")
    
    def execute_query(self, query):
        """执行SQL查询（通过Spark SQL或直接JDBC）"""
        if self.use_spark and self.spark:
            try:
                return self.spark.sql(query)
            except Exception as e:
                print(f"Spark SQL执行错误: {str(e)}")
                raise
        else:
            # 使用直接JDBC执行查询
            import psycopg2
            conn = psycopg2.connect(
                host=self.config["host"],
                port=self.config["port"],
                database=self.config["database"],
                user=self.config["user"],
                password=self.config["password"]
            )
            try:
                cursor = conn.cursor()
                cursor.execute(query)
                columns = [desc[0] for desc in cursor.description] if cursor.description else []
                rows = cursor.fetchall()
                cursor.close()
                conn.commit()
                # 转换为字典列表格式
                result = [dict(zip(columns, row)) for row in rows] if columns else []
                return result
            finally:
                conn.close()
    
    def close(self):
        """关闭Spark会话"""
        if self.spark:
            self.spark.stop()


# 直接JDBC连接版本（备用，用于简单操作）
def get_jdbc_connection(environment=None):
    """获取JDBC直接连接"""
    import os
    if environment is None:
        environment = os.getenv("ENVIRONMENT", "local")
    config = GaussDBConfig.get_config(environment)
    
    try:
        # 尝试使用jaydebeapi连接
        jdbc_jar = "/opt/spark/jars/postgresql-42.6.0.jar"
        if os.path.exists(jdbc_jar):
            conn = jaydebeapi.connect(
                config["driver"],
                config["url"],
                [config["user"], config["password"]],
                jdbc_jar
            )
        else:
            # 如果没有jar文件，使用psycopg2作为备选
            import psycopg2
            conn = psycopg2.connect(
                host=config["host"],
                port=config["port"],
                database=config["database"],
                user=config["user"],
                password=config["password"]
            )
        return conn
    except Exception as e:
        print(f"JDBC连接错误: {str(e)}")
        # 如果jaydebeapi失败，使用psycopg2
        try:
            import psycopg2
            return psycopg2.connect(
                host=config["host"],
                port=config["port"],
                database=config["database"],
                user=config["user"],
                password=config["password"]
            )
        except Exception as e2:
            print(f"psycopg2连接也失败: {str(e2)}")
            raise


