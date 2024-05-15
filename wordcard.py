import streamlit as st
from langcontrl import select_language
from ask_gpt import ask_gpt
from stablediff import generate_by_sd16, sd_tans_prompt
from draw import show_pic
from text2pic import text_to_image,hex_to_rgb,initialTextColor,lanChooser,concatenate_images

trans_sample = "<Apple>\n I like eating apples"
trans_prompt = "you skilled in describing things with the most accurate {lang} words. I will give you a word, If it's not in {lang}, please translate it into {lang}, and create a short {lang} sentence using the most common vocabulary in {lang}. Your answer should be in {lang}, and formatted like this: <Word>\n Sentence. The word should be wrapped in <>. Here's an example: <Apple>\n I like Apple. The sentence structure should be flexible and the content as humorous as possible. Do not explain, just give the answer directly.your answer is all in {lang} Here's the word I'm giving you:"

def del_session_states(states, is_rerun=True):
    for state in states:
        print(state)
        if state in st.session_state:
            del st.session_state[state]
            print(f"{state} deleted")
    if is_rerun:
        st.rerun()


def initialize_session_states(states, initial_value=None):
    for state in states:
        if state not in st.session_state:
            st.session_state[state] = initial_value




def wordCard():
    st.set_page_config(layout="wide")
    _, lang = select_language()
    title=_("title")
    st.markdown(f"<h4 style='text-align: center;'>{title}</h4>",
                unsafe_allow_html=True)
    st.divider()
    session_state = ["lang"]
    initialize_session_states(session_state)
    if "sentences" not in st.session_state:
        st.session_state["sentences"] = {}
    if "words" not in st.session_state:
        st.session_state["words"] = []
    if "img_urls" not in st.session_state:
        st.session_state["img_urls"] = [""] * 20
    if "image_text_url_list" not in st.session_state:
        st.session_state["image_text_url_list"]=[""] *20

    if "text_list" not in st.session_state:
        st.session_state["text_list"]=[""] *20
    if "images_per_row" not in st.session_state:
        st.session_state["images_per_row"] =4
    with st.sidebar:
        text_color, background_color = initialTextColor()
        max_length = lanChooser(lang)
    col1, col2 = st.columns(2)
    with col1:
        text_area=_("text area")
        st.markdown(f"<h4 style='text-align: center;'>{text_area}</h4>",
                    unsafe_allow_html=True)
        col1_con=st.container(border=True,height=800)
    with col2:
        pic_area=_("text area")
        st.markdown(f"<h4 style='text-align: center;'>{pic_area}</h4>",
                    unsafe_allow_html=True)
        con2_con=st.container(height=800)

    with col1_con:
        input_info = _("input info")
        words = st.text_area(_("Enter word/words list"),help=input_info)
        word_list = words.split('\n')
        if len(word_list) <= 20:
            word_list = [w for w in word_list if w]
            # st.write(word_list)
            system_prompt = trans_prompt.format(lang=lang)
            if st.button(_("Start Making Sentence"), use_container_width=True,type="primary"):
                st.session_state.words = []
                for w in word_list:
                    s = ask_gpt(system_prompt, w)
                    new_word = s.split(">")[0] + ">"
                    st.session_state.words.append(s.split(">")[0] + ">")
                    st.session_state["sentences"][new_word] = s
                st.rerun()
            if st.session_state["sentences"]:
                count = 0
                for w, s in st.session_state["sentences"].items():
                    st.text_input(w, s)
                    if st.button(_("create picture"), key=s, use_container_width=True):
                        draw_prompt = ask_gpt(sd_tans_prompt, s)
                        img_url = generate_by_sd16(draw_prompt,name=w)[0]
                        st.session_state["img_urls"][count]=img_url
                        if s:
                            img_io = text_to_image(s, 50, hex_to_rgb(text_color),
                                                   hex_to_rgb(background_color), max_length, False)
                            if img_url:
                                st.session_state.image_text_url_list[count] = concatenate_images(img_url,
                                    img_io,word=w)

                        if w:
                            st.session_state.text_list[count] = s
                        st.rerun()
                    count += 1
            with con2_con:
                word_pic_dict = dict(zip(st.session_state["words"],st.session_state["image_text_url_list"]))

                show_pic(word_pic_dict)
            if st.sidebar.button(_("restart"), use_container_width=True):
                del_session_states(["sentences", "words", "img_urls","image_text_url_list"])


        else:
            st.info(_("no more 20") + f'({len(word_list)})')

if __name__ == '__main__':
    wordCard()
