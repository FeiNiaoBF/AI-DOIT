import unittest
from unittest.mock import patch, MagicMock
import pytest
from openai import OpenAI

# 直接导入服务
from app.services.openai_service import OpenAIService


class TestOpenAI(unittest.TestCase):
    """测试AI服务"""

    def test_init_openai(self):
        """
        测试AI服务初始化
        需要满足OpenAI和DeepSeek API的要求
        """
        # 默认使用deepseek-chat模型和DeepSeek API
        openai_service = OpenAIService('api_key')
        self.assertIsNotNone(openai_service)
        self.assertEqual(openai_service.api_key, 'api_key')
        self.assertEqual(openai_service.base_url, 'https://api.deepseek.com/')
        self.assertEqual(openai_service.default_model, 'deepseek-chat')
        self.assertEqual(openai_service.provider, 'deepseek')

    def test_models_property(self):
        """测试模型列表属性"""
        openai_service = OpenAIService()
        self.assertIsNotNone(openai_service.models)
        self.assertEqual(set(openai_service.models), {
            'deepseek-chat',
            'deepseek-reasoner',
            'gpt-3.5-turbo',
            'gpt-4o-mini',
            'gpt-4o'
        })

    def test_change_model_same_provider(self):
        """测试在同一提供商内切换模型"""
        openai_service = OpenAIService('api_key')
        # 初始模型是deepseek-chat
        self.assertEqual(openai_service.default_model, 'deepseek-chat')

        # 切换到deepseek-reasoner
        openai_service.change_model('deepseek-reasoner')
        self.assertIsNotNone(openai_service)
        self.assertEqual(openai_service.api_key, 'api_key')
        self.assertEqual(
            openai_service.base_url,
            'https://api.deepseek.com/'
        )
        self.assertEqual(openai_service.provider, 'deepseek')
        self.assertEqual(openai_service.default_model, 'deepseek-reasoner')

    def test_change_model_different_provider(self):
        """测试在不同提供商内切换模型"""
        openai_service = OpenAIService('api_key')
        # 初始模型是deepseek-chat
        self.assertEqual(openai_service.default_model, 'deepseek-chat')
        self.assertEqual(openai_service.provider, 'deepseek')

        # 切换到gpt
        openai_service.change_model('gpt-4o')
        self.assertIsNotNone(openai_service)
        self.assertEqual(openai_service.api_key, 'api_key')
        self.assertEqual(
            openai_service.base_url,
            'https://api.openai.com/v1/'
        )
        self.assertEqual(openai_service.provider, 'openai')
        self.assertEqual(openai_service.default_model, 'gpt-4o')

    def test_invalid_model(self):
        """测试指定无效模型时引发异常"""
        with self.assertRaises(ValueError):
            OpenAIService(model='invalid-model')
        service = OpenAIService()
        with self.assertRaises(ValueError):
            service.change_model('invalid-model')

    def test_openai_client(self):
        """测试OpenAI客户端"""
        openai_service = OpenAIService('api_key')
        self.assertIsNotNone(openai_service.client)
        self.assertIsInstance(openai_service.client, OpenAI)

