
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
- An AWS account for AWS Lambda and AWS SNS.
- Required Python libraries: `Adafruit_DHT`, `awscrt`, `yagmail`, `awsiot`.

## 📦 Installation
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/dragonscypher/Weather-Window.git   ```
2. **Install Dependencies**:
   ```bash
   pip install Adafruit_DHT awscrt yagmail awsiot
   ```

## ⚙️ Configuration
- Fill in AWS IoT Core details in `mqtt_email_notification.py`.
- Set email credentials as environment variables:
  ```bash
  export MY_EMAIL_PASSWORD='your_secure_password'
  ```

## 🚀 Usage
1. **Start the System**:
   ```bash
   python mqtt_email_notification.py
   ```
2. Monitor weather data and receive alerts based on set thresholds.

## 💡 Contributing
Your contributions are welcome! Open an issue or pull request to suggest changes or additions.

## 📄 License
This project is under the [MIT License](https://choosealicense.com/licenses/mit/).
