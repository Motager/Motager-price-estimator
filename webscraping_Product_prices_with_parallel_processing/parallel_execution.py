import multiprocessing
from  Jumia_scraper import scrape_jumia
from Amazon_scraper import scrape_amazon

def scrape_product_multiprocessing(product_name,price_digit_limit=None):
    product_name = "soundcore r50i nc"
    price_digit_limit = 4
    queue = multiprocessing.Queue()  # Create a queue to store results

    # Create processes
    amazonScrapingProcess = multiprocessing.Process(target=scrape_amazon, args=(product_name, price_digit_limit, queue))
    jumiaScrapingProcess = multiprocessing.Process(target=scrape_jumia, args=(product_name, price_digit_limit, queue))

    # Start the processes
    amazonScrapingProcess.start()
    jumiaScrapingProcess.start()

    # Wait for the processes to complete
    # amazonScrapingProcess.join()
    # jumiaScrapingProcess.join()

    # Retrieve results from the queue
    results_amazon = queue.get()  # Get the results from Amazon
    results_jumia = queue.get()  # Get the results from Jumia

    # Combine the results from both sources
    all_results = {}

    if results_amazon:  # If Amazon returned results
        for result in results_amazon:
            all_results[result[0]] = result[1]
    if results_jumia:  # If Jumia returned results
        for result in results_jumia:
            all_results[result[0]] = result[1]

    # Print combined results
    for key, value in all_results.items():
        print(f"{key} --> {value}".format(key, value))
