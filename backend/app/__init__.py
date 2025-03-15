import os
from flask import Flask, jsonify
from openai import OpenAI


def create_app(conf=None):
    """初始化app"""
    app = Flask(__name__)
    # 加载配置
    app.config.from_object(conf)

    # 启动相关服务

    # openai
    # reddit
    # schedule
    # ...

    @app.route('/')
    def hello_world():  # put application's code here
        return jsonify({'message': 'Hello, World!'})

    if __name__ == '__main__':
        app.run()

    return app