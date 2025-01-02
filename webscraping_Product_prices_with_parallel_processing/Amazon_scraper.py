import requests
from bs4 import BeautifulSoup
import re
import random
import time
from difflib import SequenceMatcher
import multiprocessing
def similarity(a, b):
    a_lower, b_lower = a.lower(), b.lower()
    base_similarity = SequenceMatcher(None, a_lower, b_lower).ratio()
    a_numbers = re.findall(r'\d+', a_lower)
    b_numbers = re.findall(r'\d+', b_lower)
    if a_numbers != b_numbers:
        return base_similarity * 0.5
    return base_similarity


def parse_amazon_page(content, product_name, price_digit_limit=None):
    soup = BeautifulSoup(content, 'html.parser')
    product_prices = []
    titles = soup.findAll("h2", attrs={"class": "a-size-base-plus a-spacing-none a-color-base a-text-normal"})

    for title in titles:
        spans = title.findAll("span")
        for span in spans:
            name = span.text.strip()
            similarity_score = similarity(product_name, name)
            if similarity_score >= 0.1:
                price_tag = title.find_next("span", attrs={"class": "a-price-whole"})
                if price_tag:
                    raw_price = price_tag.text.strip()
                    numeric_price = re.sub(r"[^\d]", "", raw_price)
                    if price_digit_limit:
                        integer_part = numeric_price.split('.')[0]
                        if len(integer_part) != price_digit_limit:
                            continue
                    product_prices.append((name, numeric_price))
    # print(product_prices)
    return product_prices


def scrape_amazon(product_name, price_digit_limit, queue, max_retries=5, retry_delay=5):
    url = f"https://www.amazon.eg/s?k={product_name.replace(' ', '+')}&language=en"
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
                # time.sleep(2)
                results = parse_amazon_page(response.content, product_name, price_digit_limit)
                queue.put(("amazon", results))
                print("Amazon results sent to queue")
                return
            else:
                print(f"Unexpected status code: {response.status_code}")
                queue.put([])
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}. Retrying in {retry_delay} seconds... (Attempt {attempt + 1}/{max_retries})")
            time.sleep(retry_delay)
            queue.put([])  # Empty list after retries failed



