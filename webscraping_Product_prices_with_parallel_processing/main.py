from parallel_execution import scrape_product_multiprocessing
import time

if __name__ == '__main__':
    Product_List = ["Soundcore r50i nc", "Samsung galaxy S24 ultra", "Nike Black shoes"]
    price_limits = []  # To store the price limits for all products

    # Input price limits for all products
    for product in Product_List:
        price_limit = int(input(f"Enter the digit limit for the price for {product}: "))
        price_limits.append(price_limit)

    # Multiprocessing execution for all products
    print("\nRunning multiprocessing scraping for all products...")
    for product, price_limit in zip(Product_List, price_limits):
        print(f"\nMultiprocessing scraping for {product}...")
        amazon, jumia= scrape_product_multiprocessing(product, price_limit)

        # Ensure results are not None
        if amazon is None:
            amazon = []
        if jumia is None:
            jumia = []

        print("\nAmazon Results:")
        if amazon:
            for name, price in amazon:
                print(f"{name} -----> {price}")
        else:
            print("No Amazon results found.")

        print("\nJumia Results:")
        if jumia:
            for name, price in jumia:
                print(f"{name} -----> {price}")
        else:
            print("No Jumia results found.")

