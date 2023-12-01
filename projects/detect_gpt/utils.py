import base64
from io import BytesIO
import os
from PIL import Image
from prompts import *

api_key = os.environ['OPENAI_API_KEY']


def get_payload(base64_image, prompt):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    payload = {
        "model": "gpt-4-vision-preview",
        "messages": [
            {
                "role": "system",
                "content": prompt_system
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": prompt
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    },
                ]
            }
        ],
        "max_tokens": 1000
    }
    return headers, payload


def pil_to_base64(image):
    buffered = BytesIO()
    image.save(buffered, format="JPEG")
    return base64.b64encode(buffered.getvalue()).decode('utf-8')


def resize_long(img, length):
    w, h = img.size
    if w > h:
        return img.resize((length, int(h * length / w)))
    else:
        return img.resize((int(w * length / h), length))


def pad_to_square(img, length):
    w, h = img.size
    bg = Image.new(img.mode, (length, length), (255, 255, 255))
    bg.paste(img, ((length - w) // 2, (length - h) // 2))
    return bg


def crop_to_original(img, size):
    w, h = img.size
    return img.crop(((w - size[0]) // 2, (h - size[1]) // 2, (w + size[0]) // 2, (h + size[1]) // 2))
