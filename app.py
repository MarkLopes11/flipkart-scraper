# app.py

from flask import Flask, render_template, request, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

def scrape_flipkart_products(product_name, limit=3):
    if not product_name:
        return []
        
    query = product_name.replace(' ', '+')
    url = f"https://www.flipkart.com/search?q={query}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error during request: {e}")
        return []

    soup = BeautifulSoup(response.content, "html.parser")
    products = []

    CARD_SELECTORS = "div[data-id]"
    LINK_SELECTORS = "a.VJA3rP, a.CGtC98, a.s1Q9rs, a._1fQZEK"
    NAME_SELECTORS = "div.KzDlHZ, a.wjcEIp, div.s1Q9rs, div._4rR01T, a.IRpwTa"
    PRICE_SELECTORS = "div.Nx9bqj, div._30jeq3"
    IMAGE_SELECTORS = "img.DByuf4, img._396cs4"

    product_cards = soup.select(CARD_SELECTORS)
        
    print(f"Found {len(product_cards)} potential product cards. Analyzing...")

    for card in product_cards:
        if len(products) >= limit:
            break

        name_element = card.select_one(NAME_SELECTORS)
        price_element = card.select_one(PRICE_SELECTORS)
        image_element = card.select_one(IMAGE_SELECTORS)
        link_element = card.select_one(LINK_SELECTORS)

        if name_element and price_element and image_element and link_element:
            try:
                product_url = link_element.get('href')
                if not product_url.startswith('http'):
                    product_url = "https://www.flipkart.com" + product_url

                products.append({
                    "item": name_element.get_text(strip=True),
                    "price": price_element.get_text(strip=True),
                    "photo_url": image_element.get('src'),
                    "product_url": product_url  
                })
            except AttributeError:
                continue
            
    return products


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search')
def search():
    query = request.args.get('q', '')
    if not query:
        return jsonify([])
    results = scrape_flipkart_products(query, limit=3)
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)