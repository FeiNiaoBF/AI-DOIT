# openai_service.py
from typing import List
from openai import OpenAI
import logging

logger = logging.getLogger(__name__)


class OpenAIService:
    """
    AI服务类，支持OpenAI和DeepSeek API
    提供多模型支持和统一的接口
    """

    # 支持的模型列表
    SUPPORTED_MODELS = [
        'deepseek-chat',
        'deepseek-reasoner',
        'gpt-3.5-turbo',
        'gpt-4o-mini',
        'gpt-4o'
    ]

    # API提供商
    API_PROVIDERS = {
        'deepseek-chat': 'deepseek',
        'deepseek-reasoner': 'deepseek',
        'gpt-3.5-turbo': 'openai',
        'gpt-4o-mini': 'openai',
        'gpt-4o': 'openai'
    }

    # 基础URL
    BASE_URLS = {
        'deepseek': 'https://api.deepseek.com/',
        'openai': 'https://api.openai.com/v1/'
    }

    def __init__(self,
                 api_key: str = 'api_key',
                 model: str = 'deepseek-chat'):
        """
        初始化AI服务

        Args:
            api_key: API密钥
            model: 默认使用的模型

        Raises:
            ValueError: 如果指定了不支持的模型
        """
        if model not in self.SUPPORTED_MODELS:
            raise ValueError(f"不支持的模型: {model}。支持的模型: {', '.join(self.SUPPORTED_MODELS)}")

        self.api_key = api_key
        self.default_model = model
        self.provider = self.API_PROVIDERS[model]
        self.base_url = self.BASE_URLS[self.provider]

        # 初始化客户端
        self.client = OpenAI(
            api_key=api_key,
            base_url=self.base_url
        )

    @property
    def models(self) -> List[str]:
        """获取支持的模型列表"""
        return self.SUPPORTED_MODELS

    def change_model(self, model: str) -> None:
        """
        更改使用的模型

        Args:
            model: 要使用的模型名称

        Raises:
            ValueError: 如果指定了不支持的模型
        """
        if model not in self.SUPPORTED_MODELS:
            raise ValueError(f"不支持的模型: {model}。支持的模型: {', '.join(self.SUPPORTED_MODELS)}")
        self.default_model = model
        # 切换提供商
        provider = self.API_PROVIDERS[model]
        # 如果提供商变更，需要重新初始化客户端
        if provider != self.provider:
            self.provider = provider
            self.base_url = self.BASE_URLS[provider]
            self.client = OpenAI(
                api_key=self.api_key,
                base_url=self.base_url
            )

    def chat_completion(self, options, **kwargs):
        """
        输入相关参数，聊天完成，返回AI生成的回复

        Args:
            options: 聊天消息列表或包含消息列表的选项字典
            **kwargs: 其他参数，当options是消息列表时使用
            比如：
            {
                "model": "gpt-4o",
                "messages": [
                            {"role": "system", "content": "Hello"},
                            {"role": "user", "content": "How are you?"}
                ],
                "temperature": 0.7
                "max_tokens": 100
                "stream": False
            }

        Returns:
            AI生成的回复

        Raises:
            ValueError: 如果temperature超出范围或消息格式不正确
        """
        # 处理输入可能是消息列表的情况
        if isinstance(options, list):
            messages = options
            params = {
                "model": self.default_model,
                "messages": messages,
                **kwargs
            }
        # 处理输入是选项字典的情况
        elif isinstance(options, dict):
            if 'messages' in options:
                # 复制选项字典以避免修改原始数据
                params = options.copy()
                # 确保使用默认模型（如果未指定）
                if 'model' not in params:
                    params['model'] = self.default_model
            else:
                # 如果没有messages键，则假定整个字典是messages
                params = {
                    "model": self.default_model,
                    "messages": options,
                    **kwargs
                }
        else:
            raise ValueError("options必须是消息列表或包含消息列表的字典")

        # 验证temperature
        if 'temperature' in params:
            temperature = params['temperature']
            if temperature is not None and (temperature < 0 or temperature > 2):
                raise ValueError("temperature必须在0到2之间")

        # 设置默认temperature（如果未指定）
        if 'temperature' not in params:
            params['temperature'] = 0.7

        response = self.client.chat.completions.create(**params)
        return response.choices[0].message.content

    def chat_completion_stream(self, messages, temperature=0.7, max_tokens=None, **kwargs):
        """
        流式聊天完成，逐步返回生成内容

        Args:
            messages: 消息列表
            temperature: 温度参数
            max_tokens: 最大令牌数
            **kwargs: 其他参数

        Yields:
            str: 每个生成的内容片段
        """
        # 处理输入可能是选项字典的情况
        if isinstance(messages, dict) and 'messages' in messages:
            options = messages
            messages = options.pop('messages')
            temperature = options.get('temperature', temperature)
            max_tokens = options.get('max_tokens', max_tokens)

        # 构建参数
        params = {
            "model": self.default_model,
            "messages": messages,
            "temperature": temperature,
            "stream": True
        }

        if max_tokens is not None:
            params["max_tokens"] = max_tokens

        params.update(kwargs)

        for chunk in self.client.chat.completions.create(**params):
            if hasattr(chunk.choices[0], 'delta') and hasattr(chunk.choices[0].delta, 'content'):
                content = chunk.choices[0].delta.content
                if content:
                    yield content
