import requests
from bs4 import BeautifulSoup
import re
import random
import time
from Amazon_scraper import similarity
import multiprocessing

def parse_jumia_page(content, product_name, price_digit_limit=None):
    soup = BeautifulSoup(content, 'html.parser')
    product_prices = []
    titles = soup.findAll("h3", attrs={"class": "name"})

    for title in titles:
        name = title.text.strip()
        similarity_score = similarity(product_name, name)
        if similarity_score >= 0.1:
            price_tag = title.find_next("div", attrs={"class": "prc"})
            if price_tag:
                raw_price = price_tag.text.strip()
                numeric_price = re.sub(r"[^\d.]", "", raw_price)
                price_parts = numeric_price.split('.')
                integer_part = price_parts[0]
                decimal_part = price_parts[1] if len(price_parts) > 1 else ""
                if price_digit_limit:
                    if len(integer_part) != price_digit_limit:
                        continue
                product_prices.append((name, numeric_price))
    # print(product_prices)
    return product_prices


def scrape_jumia(product_name, price_digit_limit, queue, max_retries=5, retry_delay=5):
    url = f"https://www.jumia.com.eg/catalog/?q={product_name.replace(' ', '+')}"
    print(url)
    headers = {
        "User-Agent": random.choice([
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.5481.77 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36"
        ]),
        "Accept-Language": "en-US,en;q=0.9"
    }

    for attempt in range(max_retries):
        try:
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code in [506, 503]:
                print(
                    f"Error {response.status_code}. Retrying in {retry_delay} seconds... (Attempt {attempt + 1}/{max_retries})")
                time.sleep(retry_delay)
                continue
            if response.status_code == 200:
                print(f"Page fetched successfully with status code: {response.status_code}")
                # time.sleep(1.5)
                results = parse_jumia_page(response.content, product_name, price_digit_limit)
                queue.put(("jumia", results))
                print("jumia results sent to queue")
                return
            else:
                print(f"Unexpected status code: {response.status_code}")
                queue.put([])
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}. Retrying in {retry_delay} seconds... (Attempt {attempt + 1}/{max_retries})")
            time.sleep(retry_delay)
            queue.put([])  # Empty list after retries failed




