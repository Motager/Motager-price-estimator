import multiprocessing
from  Jumia_scraper import scrape_jumia
from Amazon_scraper import scrape_amazon
import time

def scrape_product_multiprocessing(product_name,your_cost):
    queue = multiprocessing.Queue()

    # Create processes
    p1 = multiprocessing.Process(target=scrape_amazon, args=(product_name, your_cost, queue))
    p2 = multiprocessing.Process(target=scrape_jumia, args=(product_name, your_cost, queue))

    # Start processes
    p1.start()
    p2.start()

    # Wait for processes to complete
    p1.join()
    p2.join()

    # Debugging: Check the queue size after processes finish
    print(f"Queue size after both processes finish: {queue.qsize()}")

    # Retrieve results from queue
    results_amazon = []
    results_jumia = []

    # Check if queue has results
    while not queue.empty():
        try:

           site, results = queue.get()
        # print(f"Results from {site}: {results}")  # Debugging output
           if site == 'amazon':
              results_amazon = results
           elif site == 'jumia':
              results_jumia = results

        except Exception as e:
            print(e)

    # Return results and total time
    return results_amazon, results_jumia