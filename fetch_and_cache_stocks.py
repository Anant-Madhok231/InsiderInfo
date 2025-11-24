import time
import requests
import json
from config import Config

ALPHA_VANTAGE_BASE_URL = "https://www.alphavantage.co/query"
STOCK_LIST = [
    'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'META', 'NVDA', 'TSLA', 'JPM', 'V', 'JNJ',
    'WMT', 'PG', 'MA', 'UNH', 'HD', 'BAC', 'DIS', 'ADBE', 'NFLX', 'CRM'
]  # 20 stocks

API_KEY = Config.ALPHA_VANTAGE_API_KEY
INTERVAL = '5min'
CACHE_FILE = 'stocks_cache.json'


def fetch_and_cache():
    stocks_data = {}
    for symbol in STOCK_LIST:
        try:
            # 1. Fetch intraday data
            params = {
                'function': 'TIME_SERIES_INTRADAY',
                'symbol': symbol,
                'interval': INTERVAL,
                'apikey': API_KEY,
                'outputsize': 'compact',
                'datatype': 'json',
            }
            response = requests.get(ALPHA_VANTAGE_BASE_URL, params=params)
            data = response.json()
            time_series_key = f"Time Series ({INTERVAL})"
            bars = data.get(time_series_key, {})
            if not bars:
                print(f"No intraday data for {symbol}: {data}")
                continue
            latest_time = sorted(bars.keys(), reverse=True)[0]
            latest_bar = bars[latest_time]
            open_price = float(latest_bar['1. open'])
            high_price = float(latest_bar['2. high'])
            low_price = float(latest_bar['3. low'])
            close_price = float(latest_bar['4. close'])
            volume = int(latest_bar['5. volume'])
            # 2. Fetch company overview
            overview_params = {
                'function': 'OVERVIEW',
                'symbol': symbol,
                'apikey': API_KEY
            }
            overview_resp = requests.get(ALPHA_VANTAGE_BASE_URL, params=overview_params)
            overview = overview_resp.json()
            name = overview.get('Name', symbol)
            market_cap = float(overview.get('MarketCapitalization', 0))
            pe_ratio = float(overview.get('PERatio', 0)) if overview.get('PERatio') else None
            change = close_price - open_price
            change_percent = (change / open_price) * 100 if open_price else 0.0
            stock_data = {
                'symbol': symbol,
                'name': name,
                'price': close_price,
                'change': change,
                'change_percent': f"{change_percent:.2f}%",
                'volume': volume,
                'market_cap': market_cap,
                'pe_ratio': pe_ratio,
                'high_24h': high_price,
                'low_24h': low_price,
                'itr': '',
                'last_updated': latest_time
            }
            stocks_data[symbol] = stock_data
            print(f"Updated {symbol} at {latest_time}")
            time.sleep(13)  # 5 requests/minute
        except Exception as e:
            print(f"Error updating {symbol}: {e}")
            continue
    # Save to file
    with open(CACHE_FILE, 'w') as f:
        json.dump(stocks_data, f, indent=2)
    print(f"Saved {len(stocks_data)} stocks to {CACHE_FILE}")

def main():
    while True:
        print("\n--- Fetching and caching stock data ---")
        fetch_and_cache()
        print("Sleeping for 5 minutes...")
        time.sleep(300)  # 5 minutes

if __name__ == "__main__":
    main() 