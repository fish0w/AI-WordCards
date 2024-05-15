
import datetime
import os
import streamlit as st
from langcontrl import load_translation



def initialTextColor():
    _ = load_translation(st.session_state.lang)
    col1, col2 = st.columns(2)
    with col1:
        text_color_bt=_("text color")
        text_color = st.color_picker(f":orange[{text_color_bt}]", "#FFFFFF")
    with col2:
        bg_color_bt=_("text bg_color")
        background_color = st.color_picker(f":orange[{bg_color_bt}]", "#000000")
    hex_background_color = background_color.lstrip('#')  # Remove '#' if it exists
    hex_text_color = text_color.lstrip('#')  # Remove '#' if it exists

    return hex_text_color, hex_background_color,
def hex_to_rgb(hex_color):
    return tuple(int(hex_color[i:i + 2], 16) for i in (0, 2, 4))

def lanChooser(lang):
    _ = load_translation(st.session_state.lang)
    char_per_line_bt = _("char per line")
    if lang == "chinese":

        max_length = 20
    else:
            max_length = 40

    return max_length
import textwrap
from PIL import Image, ImageDraw, ImageFont


def text_to_image(text, font_size, text_color, bg_color, max_line_length, center_first_line=False):
    font = ImageFont.truetype("fonts/msyh.ttf", font_size)

    invisible_line = 'invisible'
    text =text + '\n' + invisible_line

    paragraphs = text.split('\n')

    lines = [textwrap.wrap(paragraph, width=max_line_length) for paragraph in paragraphs]

    lines = [line for sublist in lines for line in sublist]

    max_line_width = max(font.getsize(line)[0] for line in lines)
    total_height = len(lines) * font.getsize(lines[0])[1]
    img = Image.new('RGB', (max_line_width, total_height), bg_color)
    d = ImageDraw.Draw(img)

    y_text = 0
    for i, line in enumerate(lines):
        if line == invisible_line:
            d.text((0, y_text), line, fill=bg_color, font=font)
        else:
                width, height = d.textsize(line, font=font)
                d.text(((max_line_width - width) / 2, y_text), line, fill=text_color, font=font)

        y_text += font.getsize(line)[1]

    return img
def concatenate_images(image_path1, img2,word=""):
    img1 = Image.open(image_path1)
    width1, height1 = img1.size
    width2, height2 = img2.size

    max_width = max(width1, width2)

    img1 = img1.resize((max_width, int(height1 * max_width / width1)), Image.ANTIALIAS)
    img2 = img2.resize((max_width, int(height2 * max_width / width2)), Image.ANTIALIAS)
    user_album_dir = f"pic_cards"
    if not os.path.exists(user_album_dir):
        os.makedirs(user_album_dir)
    new_img = Image.new('RGB', (max_width, img1.height + img2.height))
    timestamp = datetime.datetime.now().strftime("%y%m%d%H%M%S")
    filename = f"{word}-Card-{timestamp}.jpg"
    image_path = os.path.join(user_album_dir, filename)
    new_img.paste(img1, (0, 0))
    new_img.paste(img2, (0, img1.height))

    new_img.save(image_path)
    return image_path
