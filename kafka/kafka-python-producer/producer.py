from confluent_kafka import Producer

# Producer configuration
producer_config = {
    'bootstrap.servers': 'localhost:9092',  # Change to the appropriate broker(s)
}

# Create a Kafka producer
producer = Producer(producer_config)

# Produce a message to a Kafka topic
producer.produce('my-topic', key='key', value='Hello, Kafka!')

# Wait for any outstanding messages to be delivered and delivery reports to be received
producer.flush()