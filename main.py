import os
import base64
from glob import glob
import requests
import json

# OpenAI API Key
api_key = os.environ['OPENAI_API_KEY']

prompts = '''
Respond in a loadable JSON format.
Task:
Look at the given image and fill the JSON value with given instruction. 
JSON object has two keys named "description", "objects". 
Please fill the "description" value with the one sentence expression as detail as you can.
Then, please fill the "objects" value with the list of objects you can find in the given image.
Response Format:
{
"description": str,
"objects": list
}
* Make sure the JSON is loadable with json.loads().
    '''

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}"
}


def get_payload(base64_image):
    payload = {
        "model": "gpt-4-vision-preview",
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": prompts
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
    img_list = glob('data/baeksan-dc/220704/L/B/*')
    img_fn = img_list[0]
    base64_image = encode_image(img_fn)
    payload = get_payload(base64_image)
    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

    content = response.json()['choices'][0]['message']['content']
    json.loads(''.join(content.split('\n')[1:-1]))


if __name__ == '__main__':
    main()
