# 更新设置选项（目前实现为固定返回成功消息）
from flask import Blueprint, request, jsonify, render_template

bp = Blueprint('chat_bp', __name__)

chat_history = [
    {"role": "bot", "message": "Hello, how can I help you today?"}
]


@bp.route('/chat', methods=['POST'])
def chat():
    message = request.json["message"]
    if message is None:
        return jsonify(success=False, error="No message provided")
    response = {"role": "user", "message": message}
    return jsonify(success=True, response=response)


@bp.route('/stream', methods=['GET'])
def stream():
    return 'Stream Index'


@bp.route('/settings', methods=['GET', 'POST'])
def settings():
    return 'Settings Index'
