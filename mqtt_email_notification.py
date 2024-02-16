
import os
import sys
import threading
from uuid import uuid4
import Adafruit_DHT
import yagmail
from awscrt import mqtt, io, auth, http
from awsiot import mqtt_connection_builder
import json  # Assuming JSON is used for command-line args parsing if needed

# Use environment variables for sensitive information
my_email_password = os.getenv("MY_EMAIL_PASSWORD", "example_password")
my_email_client = yagmail.SMTP('random_email@example.com', my_email_password)

TEMP_SENSOR = Adafruit_DHT.DHT11
SENSOR_GPIO_PIN = 4

# MQTT client ID and default message count
mqtt_client_id = "mqtt-client-" + str(uuid4())
msg_count = 10
message_received_count = 0
all_messages_received_event = threading.Event()

# MQTT connection events
def handle_connection_interrupt(connection, error, **kwargs):
    """Handle unexpected disconnection."""
    print(f"Connection lost. Error: {error}")

def handle_connection_restored(connection, return_code, session_present, **kwargs):
    """Handle reconnection."""
    print(f"Connection restored. Return code: {return_code}, Session: {session_present}")
    if return_code == mqtt.ConnectReturnCode.ACCEPTED and not session_present:
        print("Re-subscribing to topics...")
        resubscribe_to_topics(connection)

def resubscribe_to_topics(connection):
    """Resubscribe to all topics after reconnection."""
    resubscribe_result, _ = connection.resubscribe_existing_topics()
    resubscribe_result.add_done_callback(handle_resubscribe_complete)

def handle_resubscribe_complete(resubscribe_result):
    """Handle the completion of the resubscription process."""
    results = resubscribe_result.result()
    print(f"Resubscribe finished: {results}")
    for topic, qos in results['topics']:
        if qos is None:
            sys.exit(f"Failed to resubscribe to topic: {topic}")

# Message received event handling
def handle_message_received(topic, payload, dup, qos, retain, **kwargs):
    """Handle incoming MQTT messages and send an email notification."""
    message_content = f"{payload.decode()} 
"
    print(f"Message on '{topic}': {message_content}")
    global message_received_count
    message_received_count += 1
    if message_received_count >= msg_count:
        all_messages_received_event.set()
        try:
            my_email_client.send(to='random_email@example.com', subject="MQTT Message Notification", contents=message_content)
            print("Notification email sent.
")
        except Exception as e:
            print(f"Failed to send email: {e}")

if __name__ == '__main__':
    # Initialize MQTT connection to AWS IoT
    event_loop_group = io.EventLoopGroup(1)
    host_resolver = io.DefaultHostResolver(event_loop_group)
    client_bootstrap = io.ClientBootstrap(event_loop_group, host_resolver)
    
    mqtt_connection = mqtt_connection_builder.mtls_from_path(
        endpoint="YOUR_AWS_IOT_ENDPOINT",
        cert_filepath="YOUR_CERTIFICATE_FILE_PATH",
        pri_key_filepath="YOUR_PRIVATE_KEY_FILE_PATH",
        client_bootstrap=client_bootstrap,
        ca_filepath="YOUR_CA_FILE_PATH",
        client_id=mqtt_client_id,
        clean_session=False,
        keep_alive_secs=6
    )

    print("Connecting to AWS IoT Core...")
    connect_future = mqtt_connection.connect()
    # Wait for the connection to complete
    connect_future.result()
    print("Connected to AWS IoT Core")

    # Subscribe to your MQTT topic(s) here
    # Example: mqtt_connection.subscribe(topic="your/topic", qos=mqtt.QoS.AT_LEAST_ONCE, callback=handle_message_received)
    
    try:
        print("MQTT message handling loop started...")
        all_messages_received_event.wait()  # Wait until all messages are received or use another condition
    except KeyboardInterrupt:
        print("Program interrupted by user. Exiting...")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Clean up and close the connection
        if mqtt_connection:
            disconnect_future = mqtt_connection.disconnect()
            disconnect_future.result()
            print("Disconnected from AWS IoT Core")
