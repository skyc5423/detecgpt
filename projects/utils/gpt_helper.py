import os
from PIL import Image
from io import BytesIO
import base64
from dataclasses import dataclass
import requests
from typing import Any


@dataclass
class Message:
    role: str
    content_type: str
    content: Any

    def __repr__(self):
        if self.content_type == 'text':
            return f'Text(role={self.role}, content_type={self.content_type}, content={self.content})'
        elif self.content_type == 'image_url':
            if isinstance(self.content, str):
                return f'Image(role={self.role}, content_type={self.content_type}, content={self.content})'
            else:
                return f'Image(role={self.role}, content_type={self.content_type}, content=Pillow Image)'

    def __init__(self, role, content_type, content):
        assert role in ['system', 'user', 'assistant'], f'role must be either system or user, but got {role}'
        assert content_type in ['text', 'image_url'], \
            f'content_type must be either text or image_url, but got {content_type}'
        self.role = role
        self.content_type = content_type
        self.content = content

    def _get_as_text(self):
        payload = {"role": self.role,
                   "content": [{"type": self.content_type,
                                self.content_type: self.content}]
                   }
        return payload

    def _get_as_image_url(self):
        img = self._encode_img(self.content)
        payload = {"role": self.role,
                   "content": [{"type": self.content_type,
                                self.content_type: {"url": f"data:image/jpeg;base64,{img}"}}]
                   }
        return payload

    def _get(self):
        if self.content_type == 'text':
            return self._get_as_text()
        elif self.content_type == 'image_url':
            return self._get_as_image_url()

    @staticmethod
    def _encode_img(img):
        if isinstance(img, str):
            img = Image.open(img)
        buffered = BytesIO()
        img.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue())
        img_str = img_str.decode('utf-8')
        return img_str


class GPTHelper:
    _PRICE_DICTIONARY = {
        'gpt-4-1106-preview': {'input': 0.01, 'output': 0.03},
        'gpt-4-vision-preview': {'input': 0.01, 'output': 0.03},
        'gpt-4': {'input': 0.03, 'output': 0.06},
        'gpt-4-32k': {'input': 0.06, 'output': 0.12},
        'gpt-3.5-turbo-1106': {'input': 0.001, 'output': 0.002},
        'gpt-3.5-turbo-instruct': {'input': 0.0015, 'output': 0.002},
    }
    _API_URL = "https://api.openai.com/v1/chat/completions"

    def __init__(self, api_key=None, model='gpt-4-vision-preview', max_tokens=1000):
        assert model in self._PRICE_DICTIONARY.keys(), f"model must be one of {self._PRICE_DICTIONARY.keys()}"
        if model != 'gpt-4-vision-preview':
            raise NotImplementedError("Only gpt-4-vision-preview is supported at the moment")

        self.api_key = api_key if api_key else os.environ['OPENAI_API_KEY']
        self.model = model
        self.max_tokens = max_tokens
        self.total_tokens = 0
        self.total_completion_tokens = 0
        self.total_prompt_tokens = 0
        self.previous_tokens = 0
        self.previous_completion_tokens = 0
        self.previous_prompt_tokens = 0
        self.last_answer = None

    def get_price(self):
        input_price = self.total_prompt_tokens * self._PRICE_DICTIONARY[self.model]['input'] / 1000.
        output_price = self.total_completion_tokens * self._PRICE_DICTIONARY[self.model]['output'] / 1000.
        return f"Total: {input_price + output_price} USD\n" \
               f"Input: {input_price} USD\n" \
               f"Output: {output_price} USD\n"

    def __repr__(self):
        return f"GPT({self.model}) \n" \
               f"total_tokens: {self.total_tokens} \n" \
               f"total_completion_tokens: {self.total_completion_tokens} \n" \
               f"total_prompt_tokens: {self.total_prompt_tokens}"

    def _get_payload(self, message_list):
        return {"model": self.model,
                "messages": [message._get() for message in message_list],
                "max_tokens": self.max_tokens}

    def _get_header(self):
        return {"Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}"}

    def _update_token_usage(self, usage):
        self.previous_tokens = usage['total_tokens']
        self.previous_completion_tokens = usage['completion_tokens']
        self.previous_prompt_tokens = usage['prompt_tokens']
        self.total_tokens += usage['total_tokens']
        self.total_completion_tokens += usage['completion_tokens']
        self.total_prompt_tokens += usage['prompt_tokens']

    def send_messages(self, message_list):
        response = requests.post(self._API_URL,
                                 headers=self._get_header(),
                                 json=self._get_payload(message_list))
        if response.status_code != 200:
            raise Exception(f"Request failed with status {response.status_code}, "
                            f"message: {response.json()['error']['message']}")
        else:
            response = response.json()
            self._update_token_usage(response['usage'])
            self.last_answer = response['choices'][0]['message']['content']
            return self.last_answer
