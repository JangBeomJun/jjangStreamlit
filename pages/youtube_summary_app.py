    
import my_yt_tran
import pdfSummary
import streamlit as st
from openai import OpenAI
import os
import tiktoken
import textwrap
import deepl

def calc_token_num(text, model="gpt-4-turbo-2024-04-09"):
    enc = tiktoken.encoding_for_model(model)
    encoded_list = enc.encode(text)
    token_num = len(encoded_list)
    
    return token_num
def divide_text(text,token_num):
    req_max_token=2000
    
    divide_num = int(token_num/req_max_token)+1
    divide_char_num = int(len(text)/divide_num)
    divide_width = divide_char_num+20
    
    divided_text_list = textwrap.wrap(text,width = divide_width)
    
    return divide_num, divided_text_list

def summarize_youtube_video(video_url,selected_lang, trans_method):
    
    if selected_lang == '영어':
        lang = 'en'
    else:
        lang = 'ko'
        
    st.video(video_url, format='video/mp4')
    
    _, yt_title, _, _, yt_duration = my_yt_tran.get_youtube_video_info(video_url)
    st.write(f"[제목] {yt_title},[길이(분:초)]{yt_duration}")
    
    yt_transcript = my_yt_tran.get_transcript_from_youtube(video_url, lang)
    
    token_num = calc_token_num(yt_transcript)
    
    div_num, divided_yt_transcripts = divide_text(yt_transcript,token_num)
    
    st.write("유튜브 동영상 내용 요약 중입니다. ㄱㄷ")
    
    summaries = []
    
    for divided_yt_transcript in divided_yt_transcripts:
        summary = pdfSummary.summarize_text(divided_yt_transcript, lang)
        summaries.append(summary)
        
    _, final_summary = pdfSummary.summarize_text_final(summaries, lang)
    
    if selected_lang== '영어':
        shorten_num = 200
    else:
        shorten_num = 120
        
    shorten_final_summary = textwrap.shorten(final_summary, shorten_num, placeholder='[..이하 생략..]')
    st.write("자막 요약: ", shorten_final_summary)
    
    if selected_lang== '영어':
        trans_result = ""
        if trans_method == 'OpenAI':
            trans_result = pdfSummary.translate_en_to_korean_using_openai(final_summary)
        elif trans_method == 'Deepl':
            trans_result = pdfSummary.translate_english_to_korean_using_deepl(final_summary)
        shorten_trans_result = textwrap.shorten(trans_result,120,placeholder='[..이하 생략..]')
        st.write("-한국어 요약(축약):",shorten_trans_result)

def button_callback():
    st.session_state['input'] = ""

st.title("유튜브 영상 요약")
url_text = st.text_input("유투브 동영상 URL 입력", key="input")

clicked_for_clear = st.button('URL 입력 내용 지우기', on_click=button_callback)

yt_lang = st.radio('유튜브 동영상 언어 선택', ['한국어','영어'], index=1, horizontal=True)

if yt_lang=='영어':
    trans_method = st.radio('번역 방법 선택', ['OpenAI', 'Deepl'], index=1,  horizontal=True)
else:
    trans_method=""
    
clicked_for_sum = st.button('동영상 내용 요약')

if url_text and clicked_for_sum:
    yt_video_url = url_text.strip()
    summarize_youtube_video(yt_video_url, yt_lang, trans_method)
