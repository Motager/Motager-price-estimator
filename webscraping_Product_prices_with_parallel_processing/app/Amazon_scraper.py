import requests
from bs4 import BeautifulSoup
import re
import random
import time
from difflib import SequenceMatcher


def extract_prefix_and_number(text):
    match = re.search(r'([A-Za-z]+)(\d+)', text)
    if match:
        return match.group(1), match.group(2)
    return None, None  # No valid match


def similarity(a, b):
    a_lower, b_lower = a.lower(), b.lower()
    a_prefix, a_number = extract_prefix_and_number(a_lower)
    b_prefix, b_number = extract_prefix_and_number(b_lower)
    if not a_prefix or not b_prefix or not a_number or not b_number:
        return 0
    if (a_prefix != b_prefix) or (a_number != b_number):
        return 0
    if a_number not in b_lower:
        return 0
    base_similarity = SequenceMatcher(None, a_lower, b_lower).ratio()
    return base_similarity


def parse_amazon_page(content, product_name, your_cost):
    soup = BeautifulSoup(content, 'html.parser')
    price_digit_limit = len(f"{your_cost}")
    product_prices = []
    products = soup.findAll("div", attrs={"data-component-type": "s-search-result"})

    for product in products[:20]:
        title = product.find("h2", attrs={"class": "a-size-base-plus"})
        if not title:
            continue

        spans = title.findAll("span")
        for span in spans:
            name = span.text.strip()
            similarity_score = similarity(product_name, name)
            if similarity_score >= 0.0:
                # Get product link
                product_link = ""
                link_tag = title.find_parent("a")
                if link_tag and 'href' in link_tag.attrs:
                    product_link = "https://www.amazon.eg" + link_tag['href']

                # Get image link
                image_link = ""
                img_tag = product.find("img", attrs={"class": "s-image"})
                if img_tag and 'src' in img_tag.attrs:
                    image_link = img_tag['src']

                price_tag = product.find("span", attrs={"class": "a-price-whole"})
                if price_tag:
                    raw_price = price_tag.text.strip()
                    numeric_price = re.sub(r"[^\d]", "", raw_price)

                    if not numeric_price:
                        continue

                    integer_part = numeric_price.split('.')[0]
                    if ((len(integer_part) == price_digit_limit) or (len(integer_part) == price_digit_limit + 1)) and (
                            int(integer_part) > int(your_cost)):
                        product_prices.append((name, numeric_price, product_link, image_link))

    if not product_prices:
        print("Warning: No valid prices found on Amazon.")

    return product_prices


def scrape_amazon(product_name, your_cost, queue, max_retries=3, retry_delay=3):
    url = f"https://www.amazon.eg/s?k={product_name.replace(' ', '+')}&language=en"
    print(f"Fetching: {url}")

    headers = {
        "User-Agent": random.choice([
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.5481.77 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36"
        ]),
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://www.google.com/",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Connection": "keep-alive",
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
                print("Page fetched successfully with status code: 200")

                results = parse_amazon_page(response.content, product_name, your_cost)
                queue.put(("amazon", results))

                print("Amazon results sent to queue")  # Fix: Now this line runs
                return results  # Fix: Ensures function exits properly

            else:
                print(f"Unexpected status code: {response.status_code}")
                queue.put([])

        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}. Retrying in {retry_delay} seconds... (Attempt {attempt + 1}/{max_retries})")
            time.sleep(retry_delay)

    print("Failed to fetch Amazon data after multiple attempts.")
    queue.put([])  # Ensure the queue gets an empty list if all retries fail
