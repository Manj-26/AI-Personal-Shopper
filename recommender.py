import requests
import openai
import pandas as pd

# 🔐 Your OpenAI API key here (get from https://platform.openai.com/account/api-keys)
openai.api_key = "sk-...replace_with_yours..."

def extract_intent_with_gpt(query):
    prompt = f"""
    You are an AI shopping assistant. A user said: "{query}"
    Extract the user's:
    - Budget (₹)
    - Product category (e.g., shoes, gifts, clothes)
    - Purpose (e.g., personal use, gift)
    - Style or preference (eco-friendly, modern, etc.)

    Return a JSON like:
    {{
        "budget": 1000,
        "category": "gifts",
        "purpose": "gift",
        "style": "eco-friendly"
    }}
    """

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        temperature=0.4,
        messages=[{"role": "user", "content": prompt}]
    )

    try:
        text = response['choices'][0]['message']['content']
        parsed = eval(text)
        return parsed
    except:
        return None

def fetch_products():
    url = "https://fakestoreapi.com/products"
    response = requests.get(url)
    return response.json()

def filter_products(products, intent):
    df = pd.DataFrame(products)

    # Apply budget filter
    if intent.get("budget"):
        df = df[df["price"] <= intent["budget"]]

    # Apply category filter if known
    if intent.get("category"):
        cat = intent["category"].lower()
        df = df[df["title"].str.lower().str.contains(cat) | df["category"].str.lower().str.contains(cat)]

    # Style keywords
    if intent.get("style"):
        style = intent["style"].lower()
        df = df[df["description"].str.lower().str.contains(style)]

    return df.sort_values("price").head(3)

def get_top_products(query):
    intent = extract_intent_with_gpt(query)
    if not intent:
        return [], None

    products = fetch_products()
    top_picks = filter_products(products, intent)

    explanation = f"Top picks under ₹{intent['budget']} for {intent['purpose']} — filtered by style: {intent.get('style', 'any')}."

    return top_picks.to_dict(orient="records"), explanation
