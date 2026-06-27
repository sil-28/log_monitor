# Automated Log Parser & Real-Time Alert System

A lightweight Python tool designed to automate log analysis and system monitoring. It parses large log files, extracts critical anomalies into a structured CSV report, and sends instant alert notifications via Telegram API.

## Features
- **Data Parsing:** Filters and cleans unstructured text logs.
- **Structured Output:** Generates Excel-compatible CSV reports automatically.
- **Real-Time Alerting:** Integrates with Telegram Bot API for instant critical failure notifications.
- **Security First:** Uses environment variables to protect API credentials.

## How to Run
1. Clone the repository.
2. Install dependencies: `pip install -r requirements.txt` (we will create this next).
3. Create a `.env` file with your `TELEGRAM_TOKEN` and `TELEGRAM_CHAT_ID`.
4. Run `python2 analizzatore.py`.