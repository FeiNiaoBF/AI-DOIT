import pytest
from openai import OpenAI

from backend.app.services.openai_service import OpenAIService


class TestOpenAI:
    """Test OpenAI service"""

    def test_init_openai(self):
        openai_service = OpenAIService()
        assert openai_service is not None
        assert isinstance(openai_service, OpenAI)
        assert openai_service.api_key == 'api_key'
        assert openai_service.base_url == 'https://api.openai.com/'
