import os
import tempfile
import pytest
from reddchat import create_app
from reddchat.db import get_db, init_db
from reddchat.config import TestingConfig

# 读取测试数据SQL文件
with open(os.path.join(os.path.dirname(__file__), "test_db.sql"), "rb") as f:
    _data_sql = f.read().decode("utf8")


@pytest.fixture
def app():
    """创建并配置测试应用实例"""
    # 创建临时文件作为测试数据库
    db_fd, db_path = tempfile.mkstemp()

    # 创建一个 TestingConfig 的子类，覆盖 DATABASE_PATH
    class TestConfig(TestingConfig):
        DATABASE_PATH = db_path

    # 使用测试配置创建应用
    app = create_app(TestConfig)

    # 在应用上下文中初始化数据库并加载测试数据
    with app.app_context():
        init_db()
        get_db().executescript(_data_sql)

    # 存储文件描述符和路径，以便稍后清理
    app.config['DB_FD'] = db_fd
    app.config['DB_PATH'] = db_path

    yield app

    # 测试结束后关闭并删除临时数据库
    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def client(app):
    """创建测试客户端"""
    return app.test_client()


@pytest.fixture
def runner(app):
    """创建命令行运行器"""
    return app.test_cli_runner()

