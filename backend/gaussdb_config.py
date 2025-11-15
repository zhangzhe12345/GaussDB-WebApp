class GaussDBConfig:
    """GaussDB数据库配置类"""
    
    # 本地虚拟机环境配置（一主二备）
    LOCAL_CONFIG = {
        "url": "jdbc:postgresql://192.168.126.101:26000/postgres",
        "driver": "org.postgresql.Driver",
        "user": "yu",
        "password": "gauss@666",
        "host": "192.168.126.101",
        "port": "26000",
        "database": "postgres"
    }
    
    # 云开发者空间配置（伪分布式）
    CLOUD_CONFIG = {
        "url": "jdbc:postgresql://localhost:5432/clouddb",
        "driver": "org.postgresql.Driver", 
        "user": "cloud_user",
        "password": "CloudPassword123!",
        "host": "localhost",
        "port": "5432",
        "database": "clouddb"
    }
    
    @staticmethod
    def get_config(environment="local"):  # 默认改为local环境
        """根据环境获取配置"""
        import os
        # 优先使用环境变量
        if os.getenv("GAUSSDB_HOST"):
            return {
                "url": f"jdbc:postgresql://{os.getenv('GAUSSDB_HOST')}:{os.getenv('GAUSSDB_PORT', '26000')}/{os.getenv('GAUSSDB_DB', 'postgres')}",
                "driver": "org.postgresql.Driver",
                "user": os.getenv("GAUSSDB_USER", "yu"),
                "password": os.getenv("GAUSSDB_PASSWORD", "gauss@666"),
                "host": os.getenv("GAUSSDB_HOST", "192.168.126.101"),
                "port": os.getenv("GAUSSDB_PORT", "26000"),
                "database": os.getenv("GAUSSDB_DB", "postgres")
            }
        return GaussDBConfig.LOCAL_CONFIG if environment == "local" else GaussDBConfig.CLOUD_CONFIG


