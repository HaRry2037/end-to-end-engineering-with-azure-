import json
from azure.eventhub import EventHubProducerClient, EventData
from faker import Faker
import random
import time

# Azure Event Hub connection details
connection_str = ""
eventhub_name = ""  # The name of your Event Hub

# Initialize Faker to generate random data
faker = Faker(['en_US'])

# Function to generate random event data
def generate_data():
    data = {
        'user_id': random.getrandbits(32),
        'event_type': random.choice(['click', 'view', 'purchase']),
        'country': faker.country_code(),
        'city': faker.city(),
        'device': random.choice(['mobile', 'desktop', 'tablet']),
        'product_id': random.getrandbits(32),
        'price': round(random.uniform(5, 500.0), 2),
        'quantity': random.randint(1, 100),
        'timestamp': round(time.time())  # Correct usage of time from time module
    }
    return data

# Function to send events to Event Hub
def send_event_to_eventhub():
    # Create a producer client for Event Hub
    producer = EventHubProducerClient.from_connection_string(connection_str, eventhub_name=eventhub_name)

    # Create a batch to send multiple messages
    event_data_batch = producer.create_batch()

    # Generate and add events to the batch
    for _ in range(10):  # Change 10 to any number you want for the number of events to send
        event_data = generate_data()
        event_data_batch.add(EventData(json.dumps(event_data)))

    # Send the batch to Event Hub
    producer.send_batch(event_data_batch)
    
    # Use len() to get the number of messages in the batch
    print(f"Sent batch to Event Hub: {len(event_data_batch)} messages.")

# Run the function to send events
if __name__ == "__main__":
    send_event_to_eventhub()

