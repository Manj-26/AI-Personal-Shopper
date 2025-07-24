import streamlit as st # type: ignore
from langdetect import detect # type: ignore
from googletrans import Translator # type: ignore

translator = Translator()

# Detect language (Hindi, Bengali, Tamil, etc.)
def detect_language(text):
    try:
        lang = detect(text)
        return lang
    except:
        return "unknown"

# Translate user input to English (for GPT)
def translate_to_english(text, source_lang):
    try:
        if source_lang == 'en':
            return text
        translated = translator.translate(text, src=source_lang, dest='en')
        return translated.text
    except:
        return text

# (Optional) Translate final GPT result back to user’s language
def translate_to_user_lang(text, target_lang):
    try:
        if target_lang == 'en':
            return text
        translated = translator.translate(text, src='en', dest=target_lang)
        return translated.text
    except:
        return text

# Format product cards
def format_products(products):
    for item in products:
        with st.container():
            cols = st.columns([1, 3])
            with cols[0]:
                st.image(item['image'], width=100)
            with cols[1]:
                st.subheader(item['title'])
                st.write(f"💰 ₹{item['price']}")
                st.write(item['description'])
                st.markdown(f"[🔗 View Product]({item['image']})", unsafe_allow_html=True)
            st.markdown("---")
