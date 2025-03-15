from flask import Flask, jsonify


def create_app(conf=None):
    """初始化app"""
    app = Flask(__name__, instance_relative_config=True)
    # 加载配置
    app.config.from_object(
        SECRET='dev',
    )

    if conf:
        app.config.from_mapping(conf)
    else:
        app.config.from_pyfile('config.py', silent=True)

    @app.route('/')
    def hello_world():  # put application's code here
        return jsonify({'message': 'Hello, World!'})

    if __name__ == '__main__':
        app.run()
    # 启动相关服务

    # openai

    # reddit
    # schedule
    # ...


    return app
