import os
from flask import Flask, jsonify
from flask_cors import CORS

from .config import get_config


def create_app(config_class=None):
    """创建并配置 Flask 应用实例"""
    # 获取配置
    if not config_class:
        config_class = get_config()
    # create and configure the app
    # __name__：告诉 Flask 当前模块的名称，用于确定应用根目录。
    # instance_relative_config=True：允许从实例文件夹（默认为项目根目录下的 instance 目录）加载配置文件。
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config_class)
    # 允许跨域请求
    CORS(app, resources={r"/api/*": {"origins": "*"}})
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
    """统一错误处理"""

    @app.errorhandler(404)
    def handle_404(e):
        return jsonify({
            "status": "error",
            "message": "Resource not found"
        }), 404

    @app.errorhandler(500)
    def handle_500(e):
        return jsonify({
            "status": "error",
            "message": "Internal server error"
        }), 500
