import json
from azure.cosmos import CosmosClient, exceptions
from azure.eventhub import EventHubConsumerClient

# Azure Event Hub connection details
eventhub_connection_str = ""  # Your Event Hub connection string
eventhub_name = ""  # Your Event Hub name
consumer_group = ""  # Consumer group name (default, unless you use another one)

# Azure Cosmos DB connection details
cosmos_endpoint = ""
cosmos_key = ""
database_name = ""  # Your Cosmos DB database name
container_name = ""  # Your Cosmos DB container name

# Initialize Cosmos DB client
cosmos_client = CosmosClient(cosmos_endpoint, cosmos_key)
database = cosmos_client.get_database_client(database_name)
container = database.get_container_client(container_name)

# Callback function for processing events and storing in Cosmos DB
def on_event(partition_context, event):
    try:
        # Parse the event data
        event_data = json.loads(event.body_as_str())
        print(f"Processing event: {event_data}")

        # Add a unique ID for each event, using sequence number as a unique ID
        event_data["id"] = str(event.sequence_number)

        # Insert the event into Cosmos DB
        container.create_item(event_data)
        print(f"Event stored in Cosmos DB: {event_data}")

        # Update checkpoint to keep track of processed events
        partition_context.update_checkpoint(event)

    except exceptions.CosmosHttpResponseError as e:
        print(f"Error storing event in Cosmos DB: {e}")

# Create a consumer client to listen to events from Event Hub
def consume_events():
    consumer_client = EventHubConsumerClient.from_connection_string(
        eventhub_connection_str,
        consumer_group,
        eventhub_name=eventhub_name,
    )

    try:
        with consumer_client:
            print("Listening for events...")
            consumer_client.receive(
                on_event=on_event,
                starting_position="@latest",  # Start from the latest events
            )
    except KeyboardInterrupt:
        print("Stopped listening for events.")
    finally:
        consumer_client.close()

if __name__ == "__main__":
    consume_events()
