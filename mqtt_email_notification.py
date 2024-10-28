import os
import Adafruit_DHT
import json
from uuid import uuid4
from awscrt import mqtt, io, auth, http
from awsiot import mqtt_connection_builder
import boto3
import time

# AWS IoT Endpoint and Thing Details
ssm_client = boto3.client('ssm')
iot_endpoint = ssm_client.get_parameter(Name='iot_endpoint', WithDecryption=True)['Parameter']['Value']
mqtt_client_id = "mqtt-client-" + str(uuid4())

temp_sensor = Adafruit_DHT.DHT11
sensor_gpio_pin = 4

ssm_client = boto3.client('ssm')
dynamodb_client = boto3.client('dynamodb')

def on_connection_interrupted(connection, error, **kwargs):
    print(f"Connection interrupted. Error: {error}")

def on_connection_resumed(connection, return_code, session_present, **kwargs):
    print(f"Connection resumed. Return code: {return_code}, Session present: {session_present}")

if __name__ == '__main__':
    # Initialize MQTT connection to AWS IoT
    event_loop_group = io.EventLoopGroup(1)
    host_resolver = io.DefaultHostResolver(event_loop_group)
    client_bootstrap = io.ClientBootstrap(event_loop_group, host_resolver)
    
    mqtt_connection = mqtt_connection_builder.mtls_from_path(
        endpoint=iot_endpoint,
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
    connect_future.result()
    print("Connected to AWS IoT Core")

    try:
        while True:
            humidity, temperature = Adafruit_DHT.read_retry(temp_sensor, sensor_gpio_pin)
            if humidity is not None and temperature is not None:
                message = {
                    "temperature": temperature,
                    "humidity": humidity,
                    "timestamp": time.time()
                }
                message_json = json.dumps(message)
                mqtt_connection.publish(
                    topic="weather/data",
                    payload=message_json,
                    qos=mqtt.QoS.AT_LEAST_ONCE
                )
                print(f"Published message: {message_json}")
                # Store data in DynamoDB
                date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                dynamodb_client.put_item(
                    TableName='ESP32_Data',
                    Item={
                        'date': {'S': date},
                        'temperature': {'N': str(temperature)},
                        'humidity': {'N': str(humidity)}
                    }
                )
            else:
                print("Failed to get reading from the sensor.")
            time.sleep(10)
    except KeyboardInterrupt:
        print("Program interrupted by user. Exiting...")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if mqtt_connection:
            disconnect_future = mqtt_connection.disconnect()
            disconnect_future.result()
            print("Disconnected from AWS IoT Core")
