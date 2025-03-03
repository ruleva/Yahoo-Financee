import yfinance as yf
import json
import time

# Конфигурација
TICKER = "AAPL"  # Симбол на акцијата (можеш да го смениш)
INTERVAL = 60  # Време во секунди помеѓу барања (пример: 1 минута)

def fetch_stock_data(ticker):
    """Презема податоци за цената на акцијата од Yahoo Finance"""
    stock = yf.Ticker(ticker)
    hist = stock.history(period="1d", interval="1m")  # Податоци за денешниот ден на 1-минутен интервал
    if not hist.empty:
        latest_data = hist.iloc[-1]  # Последен запис
        return {
            "timestamp": str(latest_data.name),
            "open": latest_data["Open"],
            "high": latest_data["High"],
            "low": latest_data["Low"],
            "close": latest_data["Close"],
            "volume": latest_data["Volume"],
        }
    return None

def main():
    """Главна функција за континуирано прибирање податоци"""
    while True:
        data = fetch_stock_data(TICKER)
        if data:
            print(json.dumps(data, indent=4))  # Привремено го печатиме JSON-от (подоцна ќе го испратиме во Kafka)
        else:
            print("No data fetched.")
        time.sleep(INTERVAL)

if __name__ == "__main__":
    main()
