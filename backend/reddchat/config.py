import os
from typing import Type

from dotenv import load_dotenv

# 加载环境变量
# 取得项目根目录
BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
env_path = os.path.join(BASE_DIR, '.env')
if not os.path.exists(env_path):
    raise FileNotFoundError(f".env file not found at {env_path}")
load_dotenv(env_path)


class Config:
    """配置基类"""
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.getenv('SECRET_KEY', 'your-default-unsecure-secret')
    # 服务配置
    HOST = os.getenv('HOST', '0.0.0.0')
    PORT = int(os.getenv('PORT', 5000))
    # 数据库配置
    DATABASE_URL = os.getenv('DATABASE_URL')
    DATABASE_PATH = os.path.join(BASE_DIR, 'instance', 'reddchat.sqlite')
    # OpenAI 配置
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    OPENAI_API_URL = os.getenv('OPENAI_API_URL', 'https://api.openai.com/v1/')
    OPENAI_MODEL = os.getenv('OPENAI_MODEL', 'deepseek')
    OPENAI_TEMPERATURE = float(os.getenv('OPENAI_TEMPERATURE', 0.7))

    @classmethod
    def validate_config(cls):
        """验证配置项"""
        required = [
            'SECRET_KEY',
            'OPENAI_API_KEY'
        ]

        missing = [var for var in required if not getattr(cls, var)]
        if missing:
            raise ValueError(f"Missing required config variables: {missing}")

    @classmethod
    def init_app(cls, app):
        """应用初始化扩展"""
        cls.validate_config()
        app.config.update(
            CONFIG_CLASS=cls.__name__,
            ENV=os.getenv('FLASK_ENV', 'development')
        )


class DevelopmentConfig(Config):
    """开发环境配置"""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{Config.DATABASE_PATH}"


class TestingConfig(Config):
    """测试环境配置"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"


class ProductionConfig(Config):
    """生产环境配置"""
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')


config_mapping = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}


def get_config():
    """动态获取配置类"""
    env = os.getenv('FLASK_ENV', 'development').lower()
    return config_mapping.get(env, config_mapping['default'])
