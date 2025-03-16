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

    def chat_completion(self, messages: List[dict]) -> str:
        """
        聊天完成

        Args:
            messages: 聊天消息列表

        Returns:
            AI生成的回复
        """
        return self.client.chat.completions.create(
            model=self.default_model,
            messages=messages
        ).choices[0].message.content
