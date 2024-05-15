import base64

import openai
from langcontrl import load_translation
from config import OPENAI_KEY
from config import SD_API_KEY
from  draw import  save_image
# 设置 OpenAI API 密钥
openai.api_key = OPENAI_KEY

import requests
import streamlit as st

sd_tans_prompt = """Now, you serve as a prompt generator based on input descriptions. Your task is to deeply understand my input
 of a scene description, identifying characters, actions, and settings within. Keep in mind, the content you generate is for 
 an AI painter, which solely understands concrete prompts instead of abstract concepts. I will provide brief descriptions 
 i, and you need to deliver accurate prompts for me in English. Refer to the following example input: 
   'An office lady sitting by the road.' The example prompt output should resemble the following structure:"：1 girl, office lady, solo, (16yo), sexy,beautiful detailed eyes, light blush, black hair, long hair, (mole under eye:0.8), nose blush , looking at viewer, suits, white shirt, striped miniskirt, (lace black pantyhose:1.2), black heels, LV bags, thighhighs, spread legs, 
sitting, street, shop border, akihabara , tokyo, tree, rain, cloudy, beautifully detailed background, depth of field, loli, 
realistic, ambient light, (cinematic composition:1.3), neon lights, HDR, Accent Lighting, pantyshot, fish eye lens.following are the desciption:"""

art_styles_dict = {"Anime": "anime","Comic Book Style": "comic-book","Sketch": "line-art","Pixel Art": "pixel-art","Photorealistic": "3d-model"}

import time


def progress_bar(text, sec=1):
    my_bar = st.progress(0, text=text)

    for percent_complete in range(100):
        time.sleep(sec / 100)
        my_bar.progress(percent_complete + 1, text=text)
    time.sleep(sec)
    my_bar.empty()


def generate_by_sd16(user_input,ratio="1024x1024", style="anime", seed=0, num=1, name="_"):
    _=load_translation(st.session_state['lang'])
    engine_id = "stable-diffusion-v1-6"
    api_host = 'https://api.stability.ai'
    api_key = SD_API_KEY
    width, height = ratio.split('x')
    try:
        response = requests.post(
            f"{api_host}/v1/generation/{engine_id}/text-to-image",
            headers={
                "Content-Type": "application/json",
                "Accept": "application/json",
                "Authorization": f"Bearer {api_key}"
            },
            json={
                "text_prompts": [
                    {
                        "text": user_input,
                        "weight": 0.8
                    }
                ],
                "cfg_scale": 25,
                "height": int(height),
                "width": int(width),
                "samples": num,
                "steps": 50,
                "style_preset": style,
                "seed": seed
            },

        )
        if response.status_code != 200:
            raise Exception(str(response.text))
        data = response.json()
        img_urls = []
        for i, image in enumerate(data["artifacts"]):
            img_data = base64.b64decode(image["base64"])
            file_url = save_image(img_data, name=name)
            img_urls.append(file_url)
            return img_urls

    except Exception as e:
        warning_info=_("draw_warning_info")

        st.warning(
            f"{warning_info}{e}")
        progress_bar("", 10)
        st.rerun()


resolution_dict = {
    "9:19": "576x1216",
    "9:20": "576x1280",
    "9:10": "1152x1280",
    "1:1": "1024x1024",
    "4:3": "1024x768",
    "16:10": "1024x640",
    "16:9": "1024x576",
    "3:2": "1536x1024",
    "21:9": "1344x576",
}


def sdxl_raito_dict(ratio_str):
    if ratio_str in resolution_dict:
        return resolution_dict[ratio_str].split('x')
    else:
        return None
