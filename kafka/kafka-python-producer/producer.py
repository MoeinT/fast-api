from confluent_kafka import Producer
import csv
import time

# Producer configuration
producer_config = {
    'bootstrap.servers': '127.0.0.1:9092',  # Change to the appropriate broker(s)
}

producer = Producer(producer_config)

# Open and read the CSV file
with open("../data/indexProcessed.csv", newline='') as csvfile:
    csv_reader = csv.reader(csvfile)
    
    # Iterate through each row in the CSV file
    for row in csv_reader:
        try:
            message = ",".join(row)  # Convert the CSV row to a string
            producer.produce("my-topic", key='key', value=message)
            producer.flush()  # Flush to ensure the message is sent immediately
        except Exception as e:
            print(f"An error occurred while sending a message: {e}")
        
        # Wait for 10 seconds before sending the next message
        time.sleep(10)






# # Create a Kafka producer
# producer = Producer(producer_config)

# # Produce a message to a Kafka topic
# producer.produce('my-topic', key='key', value="Farima is my love.")

# # Wait for any outstanding messages to be delivered and delivery reports to be received
# producer.flush()