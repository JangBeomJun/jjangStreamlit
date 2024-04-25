from PyPDF2 import PdfReader
import tiktoken
from openai import OpenAI
import textwrap
import deepl
import streamlit as st 
import os
client = OpenAI(
    api_key = st.secrets["open_spi_key"]
)
def summarize_text(user_text, lang="en"):
    if lang == "en":
        message = [
            {"role": "system", "content": "You are a helpful assistant in the summary"},
            {"role": "user", "content": f"Summarize the following. \n {user_text}"}
        ]

    elif lang == "ko" :
        message = [    
            {"role": "system", "content": "You are a helpful assistant in the summary"},
            {"role": "user", "content": f"다음의 내용을 한국어로 요약해 주세요. \n {user_text}"}
        ]

    response = client.chat.completions.create(
        model = "gpt-3.5-turbo",
        messages=message,
        max_tokens=2000,
        temperature=0.3,
        n = 1
    )

    summary = response.choices[0].message.content
    return summary

def summarize_text_final(text_list, lang = "en"):
    joined_summary = " ".join(text_list)

    enc = tiktoken.encoding_for_model("gpt-3.5-turbo")
    token_num = len(enc.encode(joined_summary))

    req_max_token = 2000
    final_summary = ""
    if token_num < req_max_token:
        final_summary= summarize_text(joined_summary, lang)

    return token_num, final_summary

def translate_en_to_korean_using_openai(text):
    user_content = f"Translate the follwing English sentences into Korean.\n {text}"
    message = [ {"role": "user", "content": user_content}]
    
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=message,
        max_tokens=2000,
        temperature=0.3,
        n=1
    )

    assistant_reply = response.choices[0].message.content

    return assistant_reply

def translate_english_to_korean_using_deepl(text):
    auth_key = st.secrets["deepl_key"]
    translator = deepl.Translator(auth_key)
    
    result = translator.translate_text(text,target_lang="KO")
    
    return result.text
