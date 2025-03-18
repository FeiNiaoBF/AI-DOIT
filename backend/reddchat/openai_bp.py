from flask import Blueprint, request, jsonify, render_template

# 创建 Blueprint
bp = Blueprint('chat_bp', __name__, url_prefix='/chat')

# 默认消息
default_messages = [
    {"role": "assistant", "content": "您好，我是您的AI助手。有什么我可以帮助您的吗？", "timestamp": datetime.datetime.now()}
]

# 会话字典，用于存储用户的聊天记录
sessions = {}


def get_session_id():
    """获取会话 ID，目前实现为固定返回 'default_session'，可扩展为根据用户信息生成唯一 ID"""
    return "default_session"


def get_chat_history(session_id):
    """获取指定会话的聊天记录"""
    if session_id not in sessions:
        sessions[session_id] = default_messages.copy()
    return sessions[session_id]


def format_messages_for_openai(messages):
    """将内部消息格式化为 OpenAI API 所需格式"""
    return [
        {"role": "system" if msg["role"] == "assistant" else msg["role"], "content": msg["content"]}
        for msg in messages if "content" in msg
    ]


@bp.route('/', methods=['GET'])
def index():
    """渲染聊天页面"""
    session_id = openai_service.get_session_id()
    return render_template("chat/index.html", conversation=openai_service.get_chat_history(session_id))


@bp.route('/send', methods=['POST'])
def send_message():
    """处理用户发送的消息"""
    try:
        # 获取会话 ID 和用户消息
        session_id = openai_service.get_session_id()
        data = request.json
        user_message = data.get("message", "")

        if not user_message.strip():
            return jsonify({"error": "请填入消息"}), 400

        # 处理用户消息并获取 AI 响应
        ai_response = openai_service.process_user_message(session_id, user_message)

        return jsonify({
            "success": True,
            "message": ai_response
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@bp.route('/history', methods=['GET'])
def get_history():
    """获取聊天记录"""
    session_id = openai_service.get_session_id()
    chat_history = openai_service.get_chat_history(session_id)
    return jsonify({"history": chat_history})


@bp.route('/clear', methods=['POST'])
def clear_history():
    """清除聊天记录"""
    session_id = openai_service.get_session_id()
    openai_service.clear_history(session_id)
    return jsonify({"success": True, "message": "记录已清除"})


@bp.route('/settings', methods=['GET', 'POST'])
def settings():
    """管理聊天设置"""
    if request.method == 'GET':
        # 获取当前设置
        settings_data = openai_service.get_settings()
        return jsonify(settings_data)
    else:
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


@bp.route('/settings', methods=['POST'])
def settings():
    return 'Settings Index'
