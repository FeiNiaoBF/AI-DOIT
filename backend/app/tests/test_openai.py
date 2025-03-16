import unittest
from unittest.mock import patch, MagicMock
import pytest

# 导入服务
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

    @patch('app.services.openai_service.OpenAI')  # 使用openai.OpenAI的Mock, 替换真实的OpenAI类
    def test_client_property(self, mock_openai):
        mock_instance = MagicMock()
        mock_openai.return_value = mock_instance

        # 测试默认模型
        openai_service = OpenAIService('test_api_key', 'deepseek-chat')
        mock_openai.assert_called_once_with(
            api_key='test_api_key',
            base_url='https://api.deepseek.com/'
        )
        # 验证客户端被正确设置
        self.assertEqual(openai_service.client, mock_instance)

        print("类 Mock 调用记录:", mock_openai.mock_calls)
        # 查看实例方法的调用记录
        print("实例 Mock 方法调用:", mock_instance.method_calls)

    @patch('app.services.openai_service.OpenAI')
    def test_demo_chat_response(self, mock_openai):
        """测试聊天方法返回正确的响应"""
        # 设置模拟响应
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = "world"

        # 配置模拟实例
        mock_instance = MagicMock()
        mock_openai.return_value = mock_instance
        mock_instance.chat.completions.create.return_value = mock_response

        openai_service = OpenAIService('test_api_key', 'deepseek-chat')

        messages = [{"role": "user", "content": "hello"}]
        # TODO
        response = openai_service.chat_completion(messages)
        self.assertEqual(response, "world")

        # 验证调用过程
        mock_instance.chat.completions.create.assert_called_once()
        call_args = mock_instance.chat.completions.create.call_args
        self.assertEqual(call_args.kwargs['model'], 'deepseek-chat')
        self.assertEqual(call_args.kwargs['messages'], messages)
