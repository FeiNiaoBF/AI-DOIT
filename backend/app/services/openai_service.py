# openai service
from openai import OpenAI


class OpenAIService(OpenAI):
    """OpenAI service"""

    def __init__(self):
        super(OpenAIService, self).__init__(
            api_key='api_key',
            base_url='https://api.openai.com/',
        )


