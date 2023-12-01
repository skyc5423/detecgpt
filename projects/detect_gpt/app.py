import numpy as np
import gradio as gr
from model.groudingdino import GDinoInferencer
from PIL import ImageDraw

from prompts import *
from utils import *
import requests
import json
import os

api_key = os.environ['OPENAI_API_KEY']


def preprocess_img(img):
    img = Image.fromarray(img)
    img = resize_long(img, 512)
    original_size = img.size
    img = pad_to_square(img, 512)
    return img, original_size


def request_gpt(img, text_input):
    headers, payload = get_payload(pil_to_base64(img), text_input)
    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
    content = response.json()['choices'][0]['message']['content']
    print(content)
    output = json.loads(content)

    return output


def draw_bbox(img, output):
    # draw bbox and make coco style annotation
    annotations = {}
    draw = ImageDraw.Draw(img)
    for obj in output['objects']:
        bboxes = inferencer.predict_dino(img, obj)
        for bbox in bboxes:
            r, g, b = np.random.randint(0, 255, 3)
            bbox = tuple(np.int16(bbox.detach().cpu().numpy()))
            draw.rectangle(bbox, outline=(r, g, b), width=1)
            if isinstance(obj, dict):
                obj = obj['name']
            draw.text(bbox, obj, (r, g, b))
            annotations[obj] = bbox

    return img, annotations


def inference(x: np.ndarray, text_input):
    img, original_size = preprocess_img(x)
    output = request_gpt(img, text_input)
    img, coco = draw_bbox(img, output)
    img = crop_to_original(img, original_size)
    return np.array(img), coco


if __name__ == '__main__':
    inferencer = GDinoInferencer('cpu')

    with gr.Blocks() as demo:
        with gr.Row():
            image_input = gr.Image(height=512, width=512)
            image_output = gr.Image(height=512, width=512)
        with gr.Row():
            text_input = gr.Textbox(lines=5, label="Input")
            text_output = gr.Textbox(lines=5, label="Output")

        image_button = gr.Button("Detect")
        image_button.click(inference, inputs=[image_input, text_input], outputs=[image_output, text_output])

    demo.launch()
