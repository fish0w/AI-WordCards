import streamlit as st
import os
import gettext
def load_translation(lang):
    """
    Load the translation file based on the selected language.

    Parameters:
    lang (str): The selected language.

    Returns:
    function: The gettext function for the selected language.
    """
    localedir = '/Users/fish/Documents/GitHub/AI-WordCards/locales'
    try:
        translate = gettext.translation('messages', localedir, languages=[lang])
    except FileNotFoundError:
        st.error(f"Translation file not found for language: {lang}")
        raise
    return translate.gettext

langdict = {'🇬🇧':['en',"english"],'🇨🇳':['zh','chinese'],"🇯🇵":['ja','japanese']}

def select_language():
    """
    Let the user select a language from a radio button list.

    Updates the session state with the selected language.
    """
    if 'lang' not in st.session_state:
        st.session_state['lang'] = 'en'
    lang_logo = st.sidebar.radio("Language", ["🇬🇧", "🇨🇳","🇯🇵"],horizontal=True,on_change=restart_onchange)
    st.session_state['lang']=langdict[lang_logo][0]
    lang=langdict[lang_logo][1]
    text=load_translation(st.session_state['lang'])
    return text,lang

def restart_onchange():
    if 'lang' in st.session_state:
        del st.session_state['lang']