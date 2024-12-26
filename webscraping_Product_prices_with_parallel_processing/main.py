from webscraping_Product_prices_with_parallel_processing.parallel_execution import scrape_product_multiprocessing

if __name__ == '__main__':
    scrape_product_multiprocessing(product_name="soundcore r50i nc",price_digit_limit = 4)
