# Weather Window

A Raspberry Pi weather station that reports to AWS. A DHT11 sensor measures temperature and humidity, the readings go to AWS IoT Core over MQTT, and alerts go out by email when a threshold is crossed.

## Architecture

1. Raspberry Pi reads the DHT11 on GPIO 4 and publishes with `mqtt_email_notification.py`.
2. AWS IoT Core receives the messages.
3. Lambda functions handle connect, store and send-message: they write readings to DynamoDB and trigger alerts.
4. SNS sends the email notification.

## Infrastructure

Terraform in this repository (`main.tf`, `variables.tf`, `outputs.tf`, `backend.tf`) creates the IoT thing, the Lambda execution role and policy, and the Lambda functions. Remote state goes to an S3 bucket, so set the bucket name in `backend.tf` first.

The Lambda zip files are expected next to `main.tf` and are not in this repository.

## Running it

```bash
terraform init
terraform apply
pip install Adafruit_DHT awscrt awsiotsdk boto3
python mqtt_email_notification.py
```

Fill in the certificate, private key and CA file paths in the script. The IoT endpoint is read from an SSM parameter called `iot_endpoint`. Email credentials come from the `MY_EMAIL_PASSWORD` environment variable.
