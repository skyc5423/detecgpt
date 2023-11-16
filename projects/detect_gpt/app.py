import numpy as np
import gradio as gr
from model.groudingdino import GDinoInferencer
from PIL import Image, ImageDraw

import base64
from io import BytesIO
from prompts import *
import requests
import json
import os

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


def flip_image(x: np.ndarray):
    height, width = x.shape[:2]
    img = Image.fromarray(x).resize((512, 512))
    headers, payload = get_payload(pil_to_base64(img), prompt_dish_multiple)
    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

    content = response.json()['choices'][0]['message']['content']
    print(content)
    output = json.loads(''.join(content.split('\n')[1:-1]))

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
    return np.array(img.resize((width, height)))


if __name__ == '__main__':
    inferencer = GDinoInferencer('cpu')

    with gr.Blocks() as demo:
        gr.Markdown("Flip text or image files using this demo.")
        with gr.Row():
            image_input = gr.Image()
            image_output = gr.Image()
        image_button = gr.Button("Flip")

        with gr.Accordion("Open for More!"):
            gr.Markdown("Look at me...")

        image_button.click(flip_image, inputs=image_input, outputs=image_output)

    demo.launch()
