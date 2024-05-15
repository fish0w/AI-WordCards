from PIL import Image
import os
from datetime import datetime
from io import BytesIO
import streamlit as st
from langcontrl import load_translation


def save_image(content, output_format="png", name=""):
    img = Image.open(BytesIO(content))
    user_album_dir = f"picture"
    os.makedirs(user_album_dir, exist_ok=True)
    save_time = datetime.now().strftime("%Y%m%d-%H%M%S")
    filename = f"{name}-{save_time}.{output_format}"
    file_url = f"{user_album_dir}/{filename}"
    img.save(file_url)
    return file_url




def show_pic(word_dict):
    lang_tool = load_translation(st.session_state.lang)
    for word,file in word_dict.items():
        word = word.replace("<", "").replace(">", "")
        if file:
            _, cola, _ = st.columns([1,2,1])
            with cola:
                st.image(file)
            with open(file, "rb") as img_file:
                img_data = img_file.read()

            col1, col2 = st.columns([1, 1])
            with col1:
                download_label = lang_tool("download")
                st.download_button(label=download_label, data=img_data, file_name=word+".png",
                                   use_container_width=True)
            with col2:
                del_label = lang_tool("delete")
                if st.button(del_label, key=file,
                             use_container_width=True):
                    if file in st.session_state["img_urls"]:
                        st.session_state["img_urls"].remove(file)


def del_pic(path, file):
    if os.path.exists(f"{path}/{file}"):
        os.remove(f"{path}/{file}")
