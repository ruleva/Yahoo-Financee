from pyspark.sql import SparkSession
from pyspark.sql.functions import col, avg
from pyspark.sql.types import StructType, StructField, StringType, DoubleType
from pyspark.sql.functions import from_json
from kafka import KafkaConsumer
import json

# Kafka Configuration
KAFKA_TOPIC = "stock-data"
KAFKA_SERVER = "kafka:9092"

# Initialize Spark Session
spark = SparkSession.builder \
    .appName("RealTimeStockProcessing") \
    .getOrCreate()

# Kafka Consumer
consumer = KafkaConsumer(
    KAFKA_TOPIC,
    bootstrap_servers=KAFKA_SERVER,
    value_deserializer=lambda v: json.loads(v.decode("utf-8"))
)

# Define Schema for Incoming Data
schema = StructType([
    StructField("timestamp", StringType(), True),
    StructField("ticker", StringType(), True),
    StructField("open", DoubleType(), True),
    StructField("high", DoubleType(), True),
    StructField("low", DoubleType(), True),
    StructField("close", DoubleType(), True),
    StructField("volume", DoubleType(), True)
])

# Real-Time Processing
for message in consumer:
    data = message.value  # Read data from Kafka
    df = spark.createDataFrame([data], schema=schema)  # Convert to Spark DataFrame

    # Example: Calculate Moving Average
    df = df.withColumn("average_price", (col("high") + col("low")) / 2)

    # Show the processed data
    df.show()

    # You can send this processed data to another Kafka topic or store in a database
