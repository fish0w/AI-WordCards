import openai
import streamlit as st

from config import OPENAI_KEY
openai.api_key = OPENAI_KEY

from openai import OpenAI


def ensure_within_limits(messages, max_tokens=8000):
    """
    Ensure the total number of tokens of the messages is within max_tokens.
    If not, truncate oldest messages.
    """
    total_tokens = sum([len(msg["content"]) for msg in messages])

    while total_tokens > max_tokens:
        removed_message = messages.pop(0)
        total_tokens -= len(removed_message["content"])

    return messages


def ask_gpt(system_prompt, user_input="", model="gpt-3.5-turbo-0125", is_json=False, is_show=True,firewall_prompt=""):

        messages = [{"role": "system", "content": f"{system_prompt}"}, {"role": "system", "content": f"{firewall_prompt}"}, {'role': 'user', 'content': f"{user_input}"}]
        client = OpenAI(api_key=OPENAI_KEY)
        if is_json:
            response = client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=0.8,
                stream=True,
                response_format={ "type": "json_object" }
            )
        else:
            response = client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=0.8,
                stream=True,
            )

        placeholder = st.empty()

        answer = ""
        for chunk in response:
            if chunk.choices[0].delta.content is not None:
                ans_piece = chunk.choices[0].delta.content
                with placeholder.container():
                    answer += ans_piece
                    if is_show:
                        with st.chat_message("assistant"):
                            st.caption(f"{answer}")

            else:
                continue
        return answer
