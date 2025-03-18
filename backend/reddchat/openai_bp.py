# 更新设置选项（目前实现为固定返回成功消息）
from flask import Blueprint, request, jsonify, render_template

bp = Blueprint('chat_bp', __name__, url_prefix='/chat')

chat_history = [
    {"role": "bot", "message": "Hello, how can I help you today?"}
]


@bp.route('/', methods=['GET'])
def index():
    return render_template("chat/index.html", chat_history=chat_history)


@bp.route('/chat', methods=['POST'])
def chat():
    data = request.json["message"]
    chat_history.append({"role": "user", "message": data})
    return jsonify(success=True)


@bp.route('/stream', methods=['GET'])
def stream():
    return 'Stream Index'


@bp.route('/settings', methods=['GET', 'POST'])
def settings():
    return 'Settings Index'
