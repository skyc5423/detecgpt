import numpy as np
import gradio as gr
from model.groudingdino import GDinoInferencer
from PIL import Image, ImageDraw

from prompts import *
from utils import *
import requests
import json
import os

api_key = os.environ['OPENAI_API_KEY']

def inference(x: np.ndarray):
    # Resize along the long length and padding to 512, 512 to match the size.
    img = Image.fromarray(x)
    img = resize_long(img, 512)
    original_size = img.size
    img = pad_to_square(img, 512)

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

    img = crop_to_original(img, original_size)

    return np.array(img)


if __name__ == '__main__':
    inferencer = GDinoInferencer('cpu')

    with gr.Blocks() as demo:
        gr.Markdown("Flip text or image files using this demo.")
        with gr.Row():
            image_input = gr.Image(height=512, width=512)
        with gr.Row():
            image_output = gr.Image(height=512, width=512)
        image_button = gr.Button("Detect")

        image_button.click(inference, inputs=image_input, outputs=image_output)

    demo.launch()
