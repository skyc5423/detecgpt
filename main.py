import os
import base64
from glob import glob
import requests
import json
from PIL import Image, ImageDraw
import numpy as np
from model.groudingdino import Inferencer
from tqdm import tqdm
from prompts import *

# OpenAI API Key
api_key = os.environ['OPENAI_API_KEY_BUF']

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}"
}


def get_payload(base64_image, prompt):
    payload = {
        "model": "gpt-4-vision-preview",
        "messages": [
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
    return payload


def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')


def main():
    img_list = glob('data/google_dining/*')
    # img_list = glob('data/baeksan-dc/220704/L/B/*')
    for idx, img_fn in enumerate(tqdm(img_list)):
        base64_image = encode_image(img_fn)
        payload = get_payload(base64_image, prompt_dish_multiple)
        response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

        content = response.json()['choices'][0]['message']['content']
        print(content)
        output = json.loads(''.join(content.split('\n')[1:-1]))
        # print(output)
        inferencer = Inferencer('cpu')
        img = Image.open(img_fn).resize((512, 512))
        draw = ImageDraw.Draw(img)
        for obj in output['foods']:
            bboxes = inferencer.predict_dino(img, obj)
            for bbox in bboxes:
                r, g, b = np.random.randint(0, 255, 3)
                bbox = tuple(np.int16(bbox.detach().cpu().numpy()))
                draw.rectangle(bbox, outline=(r, g, b), width=1)
                if isinstance(obj, dict):
                    obj = obj['name']
                draw.text(bbox, obj, (r, g, b))
        img.save(f'output/{img_fn.split("/")[-1]}')

if __name__ == '__main__':
    main()
