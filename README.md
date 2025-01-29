
# OKX Trade Automation

This project is a **Telegram trading bot** that interacts with the OKX API. It listens for messages in a specific Telegram channel, categorizes them, and executes trades on the OKX platform based on those messages.

## 📌 Table of Contents
1. [Project Overview](#project-overview)
2. [Features](#features)
3. [Requirements](#requirements)
4. [Setup Instructions](#setup-instructions)
5. [Environment Variables](#environment-variables)
6. [Usage Example](#usage-example)
7. [Deploying on AWS EC2](#deploying-on-aws-ec2)
8. [Contributing](#contributing)
9. [License](#license)

---

## 📌 Project Overview
This bot integrates with the **OKX exchange API** to automate trading based on signals received from a Telegram channel. It categorizes messages and executes **long/short trades** based on specific keywords.

## 🎯 Features
- ✅ Monitors a specified Telegram channel for **trading signals**  
- ✅ Categorizes messages (`🟣`, `🔴`, `🟡`, `🟢`) for different **trade types**  
- ✅ Executes trades using the **OKX API** (long/short positions)  
- ✅ Supports leverage, contract value, and **position sizing**  
- ✅ Trade actions include **opening and closing positions** with custom sizes  

---

## 🛠 Requirements
- Python 3.8 or later  
- `telethon` for Telegram interaction  
- `okx` API SDK for trading  
- `dotenv` for managing environment variables  
- `asyncio` for handling asynchronous operations  
- **.env file** for sensitive data (API keys, Telegram credentials)  

---

## ⚙️ Setup Instructions

### 📌 Step 1: Clone the Repository
Clone the repository to your local machine by running:

```
git clone https://github.com/muhammedozdemir57/okx-tradeautomation.git
cd okx-tradeautomation
```

### 📌 Step 2: Create a Virtual Environment
Create a virtual environment by running:

```
python3 -m venv venv
source venv/bin/activate   # For Linux/MacOS
venv\Scriptsctivate      # For Windows
```

### 📌 Step 3: Install Dependencies
Install the required dependencies using:

```
pip install -r requirements.txt
```

### 📌 Step 4: Set Up Environment Variables
Create a `.env` file in the root directory and add the following:

```
TELEGRAM_USERNAME=your_telegram_username
TELEGRAM_PHONE=your_telegram_phone_number
TELEGRAM_API_ID=your_telegram_api_id
TELEGRAM_API_HASH=your_telegram_api_hash

OKX_API_KEY=your_okx_api_key
OKX_SECRET_KEY=your_okx_secret_key
OKX_PASSPHRASE=your_okx_passphrase
```

Replace placeholders with **actual credentials**:
- Get Telegram API keys from the **Telegram Developer Portal**.
- Get OKX API keys from **OKX account settings**.

---

## ▶️ Running the Bot
Run the bot using the following command:

```
python main.py
```

The bot will monitor the Telegram channel for messages and execute trades accordingly.

---

## 📌 Usage Example

💡 Example Message:

```
🟣 BTC-USD 10
```

This will **open a short position** for BTC-USD with a **leverage of 10**.

The bot responds to the following:
- **🟣 / 🔴** → Short Positions  
- **🟡 / 🟢** → Long Positions  
- **CLOSED / KAPATTIM** → Close Positions  

---

## 🚀 Deploying on AWS EC2

### 📌 Step 1: Launch an EC2 Instance
1. Go to **AWS Management Console**  
2. Create a new **EC2 instance** (Ubuntu recommended)  
3. Open necessary ports (**22 for SSH**)  

### 📌 Step 2: SSH into the Instance
SSH into your EC2 instance by running:

```
ssh -i /path/to/key.pem ubuntu@your-ec2-ip
```

### 📌 Step 3: Install Dependencies on EC2
Install the required dependencies on your EC2 instance:

```
sudo apt update
sudo apt install python3-pip python3-venv
```

### 📌 Step 4: Clone the Repository on EC2
Clone the repository on your EC2 instance:

```
git clone https://github.com/muhammedozdemir57/okx-tradeautomation.git
cd okx-tradeautomation
```

### 📌 Step 5: Set Up the Environment & Install Requirements
Install the required dependencies on EC2:

```
pip3 install -r requirements.txt
```

### 📌 Step 6: Run the Bot on EC2
Run the bot on your EC2 instance:

```
python3 main.py
```

---

## 🤝 Contributing
Feel free to contribute by opening **issues** or submitting **pull requests**. All contributions are **welcome**!

---
