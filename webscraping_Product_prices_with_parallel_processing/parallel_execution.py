import multiprocessing
from  Jumia_scraper import scrape_jumia
from Amazon_scraper import scrape_amazon

# # Assuming the multithreaded scrape functions are imported:
# # scrape_amazon_multithreaded and scrape_jumia_multithreaded
#
# def scrape_product(product_name, price_digit_limit, scraper_function):
#     return scraper_function([product_name], price_digit_limit)
#
# def scrape_product_in_parallel(product_name, price_digit_limit=None):
#     with Pool(processes=2) as pool:  # Create two processes: one for Jumia, one for Amazon
#         # Dispatch multithreaded scrapers for Amazon and Jumia
#         results = pool.starmap(
#             scrape_product_multithreaded,
#             [
#                 (product_name, price_digit_limit, scrape_jumia_multithreaded),
#                 (product_name, price_digit_limit, scrape_amazon_multithreaded)
#             ]
#         )
#
#     # Combine results from both sources
#     all_prices = {}
#     for result in results:
#         all_prices.update(result)
#
#     return all_prices
#
def scrape_product_multiprocessing(product_name,price_digit_limit=None):
    p1 = multiprocessing.process(target=scrape_amazon,args=(product_name,price_digit_limit))
    p2 = multiprocessing.process(target=scrape_jumia,args=(product_name,price_digit_limit))
    p1.start()
    p2.start()
    p1.join()
    p2.join()
