# Weather Window: Weather Monitoring System 🌦️

## 📜 Abstract
- **Objective**: Develop a Raspberry Pi-based weather observation system.
- **Features**: Measures temperature, humidity, and atmospheric pressure.
- **Alerts**: Activates alerts through email, LED signals, or auditory alarms upon threshold breaches.
- **Integration**: Utilizes AWS Lambda and AWS SNS for efficient email notifications.

## 🛠️ Prerequisites
- Raspberry Pi with internet access.
- DHT11 sensor (or compatible) for environmental readings.
- Python 3.
- An AWS account for AWS Lambda, AWS IoT Core, and AWS SNS.
- Required Python libraries: `Adafruit_DHT`, `awscrt`, `boto3`, `awsiot`.
- Terraform for infrastructure provisioning.

## 📦 Installation
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/dragonscypher/Weather-Window.git
   ```
2. **Install Dependencies**:
   ```bash
   pip install Adafruit_DHT awscrt boto3
   ```

## ⚙️ Configuration
- Fill in AWS IoT Core details and other AWS resource information in the Python script.
- Set email credentials as environment variables:
  ```bash
  export MY_EMAIL_PASSWORD='your_secure_password'
  ```
- Terraform is used to create the required AWS infrastructure, including AWS IoT Thing, Lambda functions, and a DynamoDB table for storing sensor data.

## 🚀 Usage
1. **Provision AWS Resources**:
   Run Terraform to create the necessary AWS resources:
   ```bash
   terraform init
   terraform apply
   ```
2. **Start the System**:
   ```bash
   python mqtt_email_notification.py
   ```
3. Monitor weather data, store it in DynamoDB, and receive alerts based on set thresholds.

## 📝 Project Overview
The Weather Monitoring System, "Weather Window," leverages AWS IoT Core to collect and send weather data (temperature and humidity) from a DHT11 sensor connected to a Raspberry Pi. The collected data is published to AWS IoT Core using MQTT, stored in a DynamoDB table, and notifications are sent using AWS Lambda functions and SNS.

### Key Features:
- **AWS IoT Core Integration**: The system uses MQTT to publish sensor data to AWS IoT Core, ensuring real-time updates.
- **Data Storage**: Weather data is stored in DynamoDB for historical reference and analysis.
- **AWS Lambda**: Lambda functions are used to process messages, store data, and send alerts.
- **Notifications**: Email notifications are sent using AWS SNS based on threshold values for temperature and humidity.

## 🗺️ System Architecture
The system architecture for "Weather Window" involves multiple components working together to provide real-time weather monitoring and alerting. Below is a high-level overview:

1. **Raspberry Pi**: Collects data from the DHT11 sensor and publishes it to AWS IoT Core using MQTT.
2. **AWS IoT Core**: Serves as the central messaging broker that receives data from the Raspberry Pi.
3. **AWS Lambda Functions**: Processes the incoming data, stores it in DynamoDB, and triggers alerts.
4. **AWS DynamoDB**: Stores weather data for historical reference and analysis.
5. **AWS SNS**: Sends email notifications when the data breaches the defined thresholds.

![System Architecture Diagram](system_architecture.png)

## 💡 Contributing
Your contributions are welcome! Open an issue or pull request to suggest changes or additions.

## 📄 License
This project is under the [MIT License](https://choosealicense.com/licenses/mit/).

