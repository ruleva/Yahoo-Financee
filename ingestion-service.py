import yfinance as yf
import json
import time
from kafka import KafkaProducer

# Конфигурација
TICKER = "AAPL"
INTERVAL = 60  # Време во секунди
KAFKA_TOPIC = "stock-data"
KAFKA_SERVER = "kafka:9092"

# Конекција со Kafka
producer = KafkaProducer(
    bootstrap_servers=KAFKA_SERVER,
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

def fetch_stock_data(ticker):
    """Презема податоци за цената на акцијата од Yahoo Finance"""
    stock = yf.Ticker(ticker)
    hist = stock.history(period="1d", interval="1m")
    if not hist.empty:
        latest_data = hist.iloc[-1]
        return {
            "timestamp": str(latest_data.name),
            "ticker": ticker,
            "open": latest_data["Open"],
            "high": latest_data["High"],
            "low": latest_data["Low"],
            "close": latest_data["Close"],
            "volume": latest_data["Volume"],
        }
    return None

def main():
    """Испраќа податоци во Kafka на секоја минута"""
    while True:
        data = fetch_stock_data(TICKER)
        if data:
            producer.send(KAFKA_TOPIC, value=data)
            print(f"Sent to Kafka: {data}")
        else:
            print("No data fetched.")
        time.sleep(INTERVAL)

if __name__ == "__main__":
    main()
