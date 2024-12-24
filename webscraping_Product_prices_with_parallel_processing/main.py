import requests
from bs4 import BeautifulSoup
import re
import random
import time
from difflib import SequenceMatcher
import multiprocessing
from Amazon_scraper import scrape_amazon
from Jumia_scraper import scrape_jumia
if __name__ == '__main__':
    product_name = "soundcore r50i nc"
    price_digit_limit = 4
    queue = multiprocessing.Queue()  # Create a queue to store results

    # Create processes
    p1 = multiprocessing.Process(target=scrape_amazon, args=(product_name, price_digit_limit, queue))
    p2 = multiprocessing.Process(target=scrape_jumia, args=(product_name, price_digit_limit, queue))

    # Start the processes
    p1.start()
    p2.start()

    # Wait for the processes to complete
    p1.join()
    p2.join()

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
    print(all_results)
