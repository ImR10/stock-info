import os
import requests
import time
import sqlite3
import pandas as pd

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
            print(f"{symbol} retrieved.")
            return data
        else:
            print(f"Failed to retrive {name} stock.")

    def printStockInfo(self, symbol, stock_info, c):
        if not stock_info or "Time Series (Daily)" not in stock_info:
            print("No data available to print.")
            return

        time_series = stock_info["Time Series (Daily)"]
        recent_date = list(time_series.keys())[0]
        stock_info = time_series[recent_date]

        c.execute("INSERT INTO daily_stock_prices VALUES (?, ?, ?, ?, ?, ?, ?)", (
            symbol,
            recent_date,
            stock_info["1. open"],
            stock_info["2. high"],
            stock_info["3. low"],
            stock_info["4. close"],
            stock_info["5. volume"]
        ))

        c.execute("SELECT * FROM daily_stock_prices WHERE stock = ?", (symbol,))
        db_info = c.fetchone()
        if db_info:
            print(f"{db_info[0]} ({db_info[1]}):")
            print(f"Open: ${db_info[2]}")
            print(f"High: ${db_info[3]}")
            print(f"Low: ${db_info[4]}")
            print(f"Close: ${db_info[5]}")
            print(f"Volume: {db_info[6]}\n")

        '''
        print(f"{symbol} ({recent_date}):")
        print(f"Open: ${stock_info["1. open"]}")
        print(f"High: ${stock_info["2. high"]}")
        print(f"Low: ${stock_info["3. low"]}")
        print(f"Close: ${stock_info["4. close"]}")
        print(f"Volume: {stock_info["5. volume"]}\n")
        '''

    def readWatchlist(self, filepath, c):
        with open(file_path, "r") as file:
            tickers = file.read().splitlines()

        for ticker in tickers:
            stock_info = app.getStockInfo(ticker)
            self.printStockInfo(ticker, stock_info, c)
            time.sleep(2)

        file.close()


if __name__ == "__main__":
    connect = sqlite3.connect('daily_stock_prices.db')
    c = connect.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS daily_stock_prices (
        stock TEXT,
        date TEXT,
        open REAL,
        high REAL,
        low REAL,
        close REAL,
        volume REAL
    )''')

    app = StockApp()
    file_path = 'watchlist.txt'
    try:
        app.readWatchlist(file_path, c)
    except FileNotFoundError:
        print(f"Error: The file '{file_path} wasn't found.")

    connect.commit()
    connect.close()
