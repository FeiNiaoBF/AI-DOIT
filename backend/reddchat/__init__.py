import os
from flask import Flask, jsonify
from flask_cors import CORS


def create_app(test_config=None):
    # create and configure the app
    # __name__：告诉 Flask 当前模块的名称，用于确定应用根目录。
    # instance_relative_config=True：允许从实例文件夹（默认为项目根目录下的 instance 目录）加载配置文件。
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        # DATABASE：数据库文件路径，存储在实例文件夹中
        DATABASE=os.path.join(app.instance_path, 'reddchat.sqlite')
    )
    # 允许跨域请求
    CORS(app)
    # 加载环境配置
    if test_config is None:
        # Load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # Load the test config if passed in
        app.config.from_mapping(test_config)
    # ensure the instance folder exists
    try:
        # 实例文件夹：存储不应提交到版本控制的文件（如数据库、密钥）
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import openai_bp
    app.register_blueprint(openai_bp.bp, url_prefix='/api')

    return app


def register_error_handlers(app):
    """注册错误处理程序"""
    pass
