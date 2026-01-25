import os
import requests
from dotenv import load_dotenv

load_dotenv()

class StockApp:
    def __init__(self):
        self.API_KEY = os.getenv("API_KEY")
        self.base_URL = "https://www.alphavantage.co"

    def getStockInfo(self, name):
        function = "TIME_SERIES_DAILY"
        symbol = name
        url = f"{self.base_URL}/query?function={function}&symbol={symbol}&outputsize=compact&apikey={self.API_KEY}"
        response = requests.get(url)

        if (response.status_code == 200):
            data = response.json()
            return data;
        else:
            print(f"Failed to retrive {name} stock.")

    def printStockInfo(self, symbol, stock_info):
        if not stock_info or "Time Series (Daily)" not in stock_info:
            print("No data available to print.")
            return

        time_series = stock_info["Time Series (Daily)"]
        recent_date = list(time_series.keys())[0]
        stock_info = time_series[recent_date]

        print(f"{symbol} ({recent_date}):")
        print(f"Open: ${stock_info["1. open"]}")
        print(f"High: ${stock_info["2. high"]}")
        print(f"Low: ${stock_info["3. low"]}")
        print(f"Close: ${stock_info["4. close"]}")
        print(f"Volume: {stock_info["5. volume"]}")

if __name__ == "__main__":
    app = StockApp()
    ticker = input("Enter a stock (ticker): ").capitalize()

    stock_info = app.getStockInfo(ticker)
    app.printStockInfo(ticker, stock_info);

