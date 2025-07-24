import streamlit as st
from recommender import get_top_products
from utils import detect_language, format_products, translate_to_english, translate_to_user_lang

st.set_page_config(page_title="AI Personal Shopper", layout="wide")

st.title("🛍️ Your AI Personal Shopper")
st.write("Get smart, personalized product suggestions — in English or Hindi!")

# User input
query = st.text_input("What are you looking for?", placeholder="e.g., eco-friendly gifts under ₹1000 for mom")

if query:
    # Detect language
    lang = detect_language(query)

    # Translate query to English for GPT
    query_en = translate_to_english(query, lang)

    # Get results using translated query
    with st.spinner("Finding your perfect picks..."):
        results, explanation = get_top_products(query_en)

    # Translate explanation back to user's language (optional)
    if lang != 'en':
        explanation = translate_to_user_lang(explanation, lang)


    # Display explanation
    if explanation:
        st.markdown(f"🧠 **Why these?** {explanation}")

    # Show product cards
    if results:
        format_products(results)
    else:
        st.warning("No products matched your preferences.")
