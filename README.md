# 🛒 Market Price Estimation System

The **Market Price Estimation System** is a smart pricing assistant for online sellers. It automatically scrapes product listings from major e-commerce platforms (Amazon and Jumia), analyzes market prices, removes outliers, and recommends an optimized selling price — all through a simple API.

## 🚀 Features

- 🔍 **Parallel Web Scraping** using multiprocessing for fast data collection
- 📊 **Statistical Analysis** to compute min, max, and average prices
- ❗ **Outlier Detection** using IQR method to clean unrealistic values
- 💡 **Price Recommendation Engine** with profit estimation and competitiveness feedback
- 📈 **Profitability Metrics** based on your cost and suggested price
- 🌐 **REST API** via FastAPI, deployable on Hugging Face Spaces

## 🛠️ System Architecture
market-price-estimation/
├── Amazon_scraper.py # Scrapes product data from Amazon using BeautifulSoup
├── Jumia_scraper.py # Scrapes product data from Jumia
├── parallel_execution.py # Runs both scrapers in parallel using multiprocessing
├── price_analysis.py # Analyzes prices, removes outliers, and gives suggestions
├── API_main.py # Exposes the system as an API using FastAPI
├── requirements.txt # Python dependencies
└── README.md # Project documentation


Contributions are welcome! Feel free to open issues or submit pull requests.

� License
This project is licensed under the MIT License.

Built with ❤️ by Abdallah Mohamed
