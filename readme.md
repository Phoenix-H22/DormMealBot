# Dorm Meal Booking Automation

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Status](https://img.shields.io/badge/status-Active-success)

An automated tool that books meals for dormitory students. This tool logs into the meal booking website, books meals for the next day, sends WhatsApp confirmations, and alerts on errors. Built to ensure no meal is missed, even on busy days!

## Table of Contents
- [Features](#features)
- [Setup](#setup)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
  - [Running the Script](#running-the-script)
  - [Setting Up a Cron Job](#setting-up-a-cron-job)
- [How It Works](#how-it-works)
- [Security](#security)
- [Technologies Used](#technologies-used)
- [Contributing](#contributing)
- [License](#license)

---

## Features
- Automatically logs into the meal booking website.
- Books meals for the next day.
- Sends WhatsApp confirmation messages on success.
- Sends WhatsApp alerts on errors with detailed logs.
- Secures sensitive data using encryption.
- Supports multiple users with dynamic configurations.
- Schedules daily bookings with cron jobs.

---

## Setup

### Prerequisites
- Ubuntu 22.04 (or equivalent Linux distribution)
- Python 3.10+
- Chromium and Chromedriver installed
- WhatsApp API access (with credentials)

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/dorm-meal-booking-automation.git
   cd dorm-meal-booking-automation
   ```

2. Set up a Python virtual environment:
   ```bash
   python3 -m venv bookingenv
   source bookingenv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Make sure `chromedriver` and `chromium` are installed and configured correctly.

---

## Configuration
1. Create a `.env` file in the root directory:
   ```plaintext
   ENCRYPTION_KEY=your-encryption-key
   WHATSAPP_APP_URL=https://your-whatsapp-api-url
   WHATSAPP_APP_KEY=your-app-key
   WHATSAPP_APP_SECRET=your-app-secret
   CHROMEDRIVER_PATH=/usr/bin/chromedriver
   BRAVE_PATH=/usr/bin/chromium-browser
   ```

2. Add encrypted user details to `users.json.enc`:
   Use the provided encryption script to secure sensitive data.

---

## Usage

### Running the Script
Activate the virtual environment and execute the script:
```bash
source bookingenv/bin/activate
python3 main.py
```

### Setting Up a Cron Job
1. Open the crontab editor:
   ```bash
   crontab -e
   ```

2. Add the following line to run the script daily at 7 PM:
   ```plaintext
   0 19 * * * /path/to/bookingenv/bin/python3 /path/to/main.py >> /path/to/logfile.log 2>&1
   ```

---

## How It Works
1. Decrypts the user credentials.
2. Logs into the meal booking website using Selenium.
3. Navigates through the dashboard to book meals for the next day.
4. Sends API requests to confirm the booking.
5. Notifies users of success or failure via WhatsApp.

---

## Security
- Sensitive data is stored in an encrypted JSON file (`users.json.enc`).
- `.env` file stores encryption keys and API credentials securely.
- Logs and decrypted files are cleaned up after execution.

---

## Technologies Used
- **Python 3.10+**
- **Selenium** for browser automation
- **Requests** for API interactions
- **Cryptography** for encryption
- **WhatsApp API** for notifications
- **Cron** for scheduling

---

## Contributing
Contributions are welcome! Please fork the repository, make your changes, and submit a pull request.