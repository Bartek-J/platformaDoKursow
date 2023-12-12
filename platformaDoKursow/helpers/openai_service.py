from openai.openai_object import OpenAIObject
from platformaDoKursow.settings import OPENAI_API_KEY
from importlib import import_module
from os import getenv
import openai



MODEL = 'gpt-4'
INSTRUCTION = '''
    You are only to response in json format, determining if question is correct,
    you will receice questions with fields question, answer_key, user_answer and max_points
    you must determine each questions how many points is answer worth from 0 to max_points, you can give half points
    but not smaller decimals. As result please only return single number without any other text wchich is summaried,
    points given to user in json with structure:
    example: { 'points': 21 }
'''


class ChatGPTServiceError(Exception): ...


class ChatGPTService:
    def __init__(self, instruction: str, temperature: float = 1.25, model: str = MODEL) -> None:
        self.instruction = instruction
        self.model = model
        self.temperature = temperature

    def run(self) -> None:
        openai.api_key = OPENAI_API_KEY
        try:
            return self._process_gpt_response(
                openai.ChatCompletion.create(
                    model=self.model,
                    temperature=self.temperature,
                    messages=[
                        {'role': 'system', 'content': INSTRUCTION},
                        {'role': 'user', 'content': self.instruction}
                    ]
                )
            )
        except (openai.error.APIError, openai.error.Timeout, openai.error.RateLimitError,
                openai.error.APIConnectionError, openai.error.InvalidRequestError,
                openai.error.AuthenticationError, openai.error.ServiceUnavailableError) as e:
            raise ChatGPTServiceError(str(e))

    def _process_gpt_response(self, gpt_response: OpenAIObject) -> list[str]:
        return [response.message.content for response in gpt_response['choices']]
