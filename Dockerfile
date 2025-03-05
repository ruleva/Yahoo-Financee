FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY ingestion-service.py .

ENV TICKER=AAPL
ENV INTERVAL=60
ENV KAFKA_TOPIC=stock-data
ENV KAFKA_SERVER=kafka:9092

CMD ["python", "ingestion-service.py"]