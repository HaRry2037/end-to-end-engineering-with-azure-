import json
from azure.eventhub import EventHubConsumerClient

# Azure Event Hub connection details
connection_str = "Endpoint=sb://druidevent1.servicebus.windows.net/;SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=9SPwe6obP/vQMmSljB369kULZF89O6NfM+AEhNS3g9w="
eventhub_name = "ecommerce-events"  # The name of your Event Hub
consumer_group = "$Default"  # The consumer group name. Change if using a custom consumer group.

# Callback function for processing received events
def on_event(partition_context, event):
    print(f"Received event from partition {partition_context.partition_id}: {event}")
    try:
        event_data = json.loads(event.body_as_str())  # Parse event data
        print(f"Event data: {event_data}")
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
    # Checkpoint to mark the event as processed
    partition_context.update_checkpoint(event)

# Create a ConsumerClient instance and consume events
def consume_events():
    # Create the consumer client using the connection string and consumer group name
    client = EventHubConsumerClient.from_connection_string(connection_str, consumer_group, eventhub_name=eventhub_name)

    try:
        with client:
            print("Listening for events. Press Ctrl+C to stop.")
            # Begin receiving events starting from the latest event
            client.receive(
                on_event=on_event,
                starting_position="@latest",  # Start from the latest event
                consumer_group=consumer_group,
                eventhub_name=eventhub_name
            )
    except KeyboardInterrupt:
        print("Interrupted by user. Stopping event consumption.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        print("Shutting down client...")
        client.close()

if __name__ == "__main__":
    consume_events()
