FROM python:3.9
LABEL authors="rulev"

WORKDIR /ingestion-service
COPY ingestion-service.py .

RUN pip install --no-cache-dir yfinance kafka-python

EXPOSE 8080
CMD ["python", "ingestion-service.py"]