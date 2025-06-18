from parallel_execution import scrape_product_multiprocessing
import numpy as np
import matplotlib.pyplot as plt
import io
from typing import List, Dict, Any
import json
import re

prices_list = []
# min_price=0
# avg_price=0
# max_price = 0
from typing import List, Any, Tuple


def loop_prices(source_list: List[List[Any]], source_name: str) -> Tuple[List[dict], List[int]]:
    products = []
    prices_list = []

    for item in source_list:
        try:
            product_name = item[0]
            price = int(item[1])
            product_link = item[2] if len(item) > 2 else ""
            image_link = item[3] if len(item) > 3 else ""

            product = {
                "product_name": product_name,
                "source": source_name,
                "price": price,
                "product link": product_link,
                "image link": image_link
            }
            products.append(product)
            prices_list.append(price)
        except (ValueError, IndexError, TypeError):
            print(f"Error: Skipping invalid price data from {source_name}")

    return products, prices_list

def get_products_list(product_name: str, your_cost: float):
    amazon, jumia = scrape_product_multiprocessing(product_name, your_cost)

    products = []
    all_prices = []

    amazon_products, amazon_prices = loop_prices(amazon, "Amazon")
    jumia_products, jumia_prices = loop_prices(jumia, "Jumia")

    products.extend(amazon_products)
    products.extend(jumia_products)

    all_prices.extend(amazon_prices)
    all_prices.extend(jumia_prices)

    return products, all_prices

# def generate_prompt(product_name, your_cost):
#     products, _ = get_products_list(product_name, your_cost)
#
#     prompt = (f"Filter the given product list to include only closely related products."
#               f" The response should only be the filtered product list in valid JSON format, without any explanations or additional text."
#               f" Ensure the output is a properly formatted JSON array of dictionaries."
#               f" Real product name: {product_name}\nProduct list: {json.dumps(products, ensure_ascii=False, indent=2)}\n"
#               f"Example JSON output:\n"
#               f"["
#               f"{{\"product_name\": \"Soundcore R50i NC Wireless Bluetooth Headphones - Black\", \"source\": \"Amazon\", \"price\": 1150}},"
#               f"{{\"product_name\": \"Soundcore R50i NC True Wireless Earbuds 10mm Drivers with Big Bass, Bluetooth 5.3, 45H Playtime, IP54-Sweatguard Waterproof, AI Clear Calls with 4 Mics, 22 Preset EQs via App-Black\", \"source\": \"Amazon\", \"price\": 1390}},"
#               f"{{\"product_name\": \"Soundcore R50i NC True Wireless Earbuds 10mm Drivers with Big Bass, Bluetooth 5.3, 45H Playtime, IP54-Sweatguard Waterproof, AI Clear Calls with 4 Mics, 22 Preset EQs via App-White\", \"source\": \"Amazon\", \"price\": 1713}},"
#               f"{{\"product_name\": \"Soundcore R50i NC True Wireless Earbuds with Big Bass, Bluetooth 5.3, 45H Playtime, IP54-Sweatguard Waterproof, AI Clear Calls with 4 Mics, 22 Preset EQs via App-GREEN Local warranty\", \"source\": \"Amazon\", \"price\": 1550}}"
#               f"]"
#               )
#
#     return prompt

# def get_filtered_product_list(product_name, your_cost):
#     prompt = generate_prompt(product_name, your_cost)
#
#     genai.configure(api_key="AIzaSyAzp-WRPAi4IaALmpjyRh2yo0qsPmFMxdI")
#     model = genai.GenerativeModel("gemini-2.0-flash")
#     response = model.generate_content(prompt)
#
#     try:
#         # Parse response into JSON
#         filtered_products = json.loads(response.text)
#         if isinstance(filtered_products, list):
#             return filtered_products
#         else:
#             return []
#     except json.JSONDecodeError:
#         return []


# def extract_json(response_text):
#     match = re.search(r"\[.*\]", response_text, re.DOTALL)  # Extracts JSON part
#     if match:
#         return match.group(0)
#     return None
#
# def extract_prices(response_text):
#     json_text = extract_json(response_text)
#     if not json_text:
#         return "Invalid API response: No JSON found"
#
#     try:
#         products = json.loads(json_text)  # Convert JSON string to Python list
#         prices = [product["price"] for product in products if "price" in product]
#         return prices
#     except json.JSONDecodeError as e:
#         return f"Invalid JSON format: {e}"

def remove_outliers(prices, multiplier=1.0):
    if not prices:
        print("Warning: The prices list is empty. Returning an empty list.")
        return []
    try:
        prices = list(map(int, prices))
    except ValueError:
        print("Error: Could not convert prices to integers. Check data format.")
        return []

    if len(prices) < 2:
        print("Warning: Not enough data points to compute outliers.")
        return prices

    Q1 = np.percentile(prices, 25)
    Q3 = np.percentile(prices, 75)
    IQR = Q3 - Q1
    lower_bound = Q1 - multiplier * IQR
    upper_bound = Q3 + multiplier * IQR
    return [price for price in prices if lower_bound <= price <= upper_bound]


def get_MinMaxAverage(updated_price_list):
    filtered_prices = remove_outliers(updated_price_list)

    if not filtered_prices:
        print("Error: No valid prices available.")
        return None, None, None

    try:
        filtered_prices = list(map(int, filtered_prices))
        mini = np.min(list(map(int, updated_price_list)))
        maxi = np.max(list(map(int, updated_price_list)))
        average = round(np.mean(filtered_prices), 2)
    except ValueError:
        print("Error: Could not compute min/max/average due to invalid data.")
        return None, None, None

    return mini, average, maxi

def normalize(price, min_price, max_price):
    if min_price is None or max_price is None:
        print("Error: Cannot normalize due to missing price data.")
        return np.pi / 2
    if min_price == max_price:
        return np.pi / 2
    return np.pi - ((price - min_price) / (max_price - min_price) * np.pi)



def plot_your_price(your_price, min_price,max_price,avg_price):


    if min_price is None or max_price is None or avg_price is None:
        print("Error: Cannot plot due to missing price data.")
        return None  # Return None if the image cannot be generated

    fig, ax = plt.subplots(figsize=(8, 4), subplot_kw={'projection': 'polar'})

    # Create the three segments (Min = Red, Mid = Yellow, Max = Green)
    ax.barh(1, np.pi / 3, left=2 * np.pi / 3, color='red', height=0.5)
    ax.barh(1, np.pi / 3, left=np.pi / 3, color='yellow', height=0.5)
    ax.barh(1, np.pi / 3, left=0, color='green', height=0.5)

    # Plot your price marker
    norm_price = normalize(your_price, min_price, max_price)
    ax.plot([norm_price, norm_price], [0, 1], color="black", linewidth=3, marker="o", markersize=10)

    # Labels
    ax.text(np.pi + 0.1, 1.2, f"Min: {int(min_price)}", ha="center", fontsize=10, color="black", fontweight="bold")
    ax.text(np.pi / 2, 1.2, f"Avg: {int(avg_price)}", ha="center", fontsize=10, color="black", fontweight="bold")
    ax.text(-0.1, 1.2, f"Max: {int(max_price)}", ha="center", fontsize=10, color="black", fontweight="bold")

    # Final styling
    plt.title("Your Price Compared to Market", fontsize=12, fontweight="bold", color="black")
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_frame_on(False)
    plt.show()
    # Save the plot to an in-memory buffer
    img_buffer = io.BytesIO()
    plt.savefig(img_buffer, format="png", bbox_inches="tight")  # Save the figure to the buffer
    plt.close(fig)
    img_buffer.seek(0)

    return img_buffer

def recommend_price(min_price, avg_price, max_price, user_price, user_cost, price_list):
    # Calculate quartiles
    q1 = float(np.percentile(price_list, 25))
    q3 = float(np.percentile(price_list, 75))

    # Price Adjustment Suggestion based on market range
    if user_price < min_price:
        price_suggestion = f"Your price is too low. Consider increasing it to at least {min_price}."
    elif user_price > max_price:
        price_suggestion = f"Your price is too high. Consider lowering it below {max_price}."
    else:
        price_suggestion = "Your price is competitive in the market."

    # Market Competitiveness Rating
    if user_price < q1:
        competitiveness = "Very Cheap (Consider increasing your price!)"
    elif q1 <= user_price <= q3:
        competitiveness = "Competitive (Good price in the market)"
    else:
        competitiveness = "Expensive (Consider lowering your price)"

    # Recommended Selling Price Range (ensuring at least 10% profit)
    recommended_price = max(user_cost * 1.1, q1)  # Ensure minimum profit of 10%
    recommended_range = (round(recommended_price, 2), round(q3, 2))

    # Relationship between User Price and Average Price
    if user_price < avg_price:
        avg_relation = f"Your price is below the average market price ({avg_price}). You may have room to increase it."
    elif user_price > avg_price:
        avg_relation = f"Your price is above the average market price ({avg_price}). Ensure your product quality justifies the price."
    else:
        avg_relation = "Your price matches the average market price."

    # Profit Calculation
    profit_margin = user_price - user_cost
    profit_percentage = (profit_margin / user_cost) * 100 if user_cost > 0 else 0

    return {
        "min_price": min_price,
        "max_price": max_price,
        "avg_price": avg_price,
        "user_price": user_price,
        "price_suggestion": price_suggestion,
        "competitiveness": competitiveness,
        "recommended_range": recommended_range,
        "avg_relation": avg_relation,
        "profit_margin": f"{round(profit_margin, 2)} EGP",
        "profit_percentage": f"{round(profit_percentage, 2)}%"
    }


def get_prices_analysis(prices, cost_price, user_price):
    prices = [float(p) for p in prices]
    min_price, avg_price, max_price = get_MinMaxAverage(prices)
    min_price, avg_price, max_price = int(min_price), float(avg_price), int(max_price)
    # image_buffer = plot_your_price(user_price, min_price, max_price, avg_price)
    recommendations = recommend_price(min_price, avg_price, max_price, user_price, cost_price, prices)
    recommendations["recommended_range"] = tuple(map(float, recommendations["recommended_range"]))
    return recommendations


def market_price_estimation(product_name , cost_price , user_price):
    products,prices  = get_products_list(product_name,cost_price)
    recommendations = get_prices_analysis(prices, cost_price, user_price)
    response={
        "products": products,
        "recommendations": recommendations,
    }

    return response