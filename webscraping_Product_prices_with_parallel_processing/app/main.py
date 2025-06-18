from parallel_execution import scrape_product_multiprocessing
from Amazon_scraper import scrape_amazon
from Jumia_scraper import scrape_jumia
import numpy as np
from price_analysis import market_price_estimation,get_products_list
from Amazon_scraper import scrape_amazon
from PIL import Image  # To open the saved image for preview

if __name__ == '__main__':
    product_name = 'soundcore r50 nc'
    cost_price = 1000
    user_price = 1500

    # Get prices from web scrapers
    response = market_price_estimation(product_name, cost_price, user_price)
    print(response)
    # print("Scraped Prices:", prices)
    # min_price, avg_price, max_price = get_MinMaxAverage(prices)
    # Generate image
    # image_buffer = plot_your_price(user_price, min_price,max_price,avg_price)

    # if image_buffer is None:
    #     print("Error: Could not generate price comparison plot.")
    # else:
    #     # Save to a file
    #     with open("price_comparison.png", "wb") as f:
    #         f.write(image_buffer.getvalue())
    #
    #     print("Image saved as 'price_comparison.png'")
    #
    #     # Open image for preview (optional)
    #     img = Image.open("price_comparison.png")
    #     img.show()

    #
    # recommendations = recommend_price(min_price,avg_price,max_price,user_price, cost_price,prices)
    # for key, value in recommendations.items():
    #     print(f"{key}: {value}")
    # ans = get_prices_analysis(prices,cost_price,user_price)
    # print(ans)
