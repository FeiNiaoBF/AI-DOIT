import unittest
from unittest.mock import patch, MagicMock
import pytest

# 导入服务
from app.services.openai_service import OpenAIService
from click import option
from openai import models


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
        option = {
            "messages": messages,
        }
        response = openai_service.chat_completion(option)
        self.assertEqual(response, "world")

        # 验证调用过程
        mock_instance.chat.completions.create.assert_called_once()
        call_args = mock_instance.chat.completions.create.call_args
        self.assertEqual(call_args.kwargs['model'], 'deepseek-chat')
        self.assertEqual(call_args.kwargs['messages'], messages)

    @patch('app.services.openai_service.OpenAI')
    def test_chat_response_with_option(self, mock_openai):
        """测试带选项的聊天完成功能"""
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
        options = {
            "messages": messages,
            "temperature": 0.5,
            "models": "deepseek-chat"
        }
        response = openai_service.chat_completion(options)
        self.assertEqual(response, "world")

        # 验证调用过程
        mock_instance.chat.completions.create.assert_called_once()
        call_args = mock_instance.chat.completions.create.call_args
        self.assertEqual(call_args.kwargs['model'], 'deepseek-chat')
        self.assertEqual(call_args.kwargs['messages'], messages)

    @patch('app.services.openai_service.OpenAI')
    def test_temperature_parameter(self, mock_openai):
        """测试temperature参数控制创意性"""
        # 设置模拟响应
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = "测试回复"

        # 配置模拟实例
        mock_instance = MagicMock()
        mock_openai.return_value = mock_instance
        mock_instance.chat.completions.create.return_value = mock_response

        service = OpenAIService('test_api_key')

        # 测试默认temperature
        messages = [{"role": "user", "content": "测试"}]
        service.chat_completion(messages)
        default_args = mock_instance.chat.completions.create.call_args
        self.assertEqual(default_args.kwargs['temperature'], 0.7)  # 默认值应为0.7

        # 测试自定义temperature
        service.chat_completion(messages, temperature=0.2)
        custom_args = mock_instance.chat.completions.create.call_args
        self.assertEqual(custom_args.kwargs['temperature'], 0.2)

        # 测试无效temperature
        with self.assertRaises(ValueError):
            service.chat_completion(messages, temperature=2.5)  # 超出有效范围

    @patch('app.services.openai_service.OpenAI')
    def test_max_tokens_parameter(self, mock_openai):
        """测试max_tokens参数控制响应长度"""
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = "测试回复"

        mock_instance = MagicMock()
        mock_openai.return_value = mock_instance
        mock_instance.chat.completions.create.return_value = mock_response

        service = OpenAIService('test_api_key')

        # 测试设置max_tokens
        messages = [{"role": "user", "content": "生成一个长回复"}]
        service.chat_completion(messages, max_tokens=500)
        token_args = mock_instance.chat.completions.create.call_args
        self.assertEqual(token_args.kwargs['max_tokens'], 500)

    @patch('app.services.openai_service.OpenAI')
    def test_stream_response(self, mock_openai):
        """测试流式响应功能"""
        # 模拟流式响应
        chunk1 = MagicMock()
        chunk1.choices = [MagicMock()]
        chunk1.choices[0].delta.content = "第一"

        chunk2 = MagicMock()
        chunk2.choices = [MagicMock()]
        chunk2.choices[0].delta.content = "部分"

        chunk3 = MagicMock()
        chunk3.choices = [MagicMock()]
        chunk3.choices[0].delta.content = "内容"

        mock_instance = MagicMock()
        mock_openai.return_value = mock_instance
        mock_instance.chat.completions.create.return_value = [chunk1, chunk2, chunk3]

        service = OpenAIService('test_api_key')

        # 测试流式响应
        messages = [{"role": "user", "content": "测试"}]
        result = []
        for chunk in service.chat_completion_stream(messages):
            result.append(chunk)

        self.assertEqual(result, ["第一", "部分", "内容"])
        stream_args = mock_instance.chat.completions.create.call_args
        self.assertTrue(stream_args.kwargs['stream'])
