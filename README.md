# Real-Time Fault-Tolerant Log Streamer & Telegram Alerter

A production-ready Python automation tool designed for continuous, real-time monitoring of system logs (similar to the Linux `tail -f` command). It dynamically streams incoming log data, parses anomalies (`ERROR` and `CRITICAL`) into a structured CSV report on the fly, and instantly dispatches high-priority alerts via the Telegram Bot API.

## Features

- **Live Stream Processing:** Instead of parsing static files, the script remains active, watching the target log file and processing new entries instantly as they are appended.
- **Resource Optimized:** Implements smart polling with controlled delays (`time.sleep`) to keep CPU utilization close to 0% during idle periods.
- **Dynamic CLI Input:** Accepts custom log paths directly from the terminal, defaulting to `system.log` if no argument is provided.
- **Fail-Safe & Fault-Tolerant:** Wrapped in robust exception handling blocks to gracefully manage `FileNotFoundError`, `PermissionError`, and user interruption (`KeyboardInterrupt`) without data loss.
- **Immediate I/O Flushing:** Forces data writing to disk immediately after an anomaly is found (`csv_file.flush()`), preventing data loss in case of sudden hardware failures.
- **Security First:** Strictly decoupling code from secrets by managing API credentials through environment variables via `python-dotenv`.

## Project Structure

- `analizzatore.py`: Core production script containing the streaming logic and exception handlers.
- `requirements.txt`: Clean inventory of third-party dependencies (`requests`, `python-dotenv`).
- `.env`: (Local only) Private environment variables holding sensitive API tokens.
- `.gitignore`: Configured to keep local log streams and authentication keys secure from version tracking.

## Installation & Setup
1. Clone the repository.
2. Install dependencies: `pip install -r requirements.txt` (we will create this next).
3. Create a `.env` file with your `Token_telegram` and `Chat_ID_telegram`.

## Usage
Run `python2 analyzer.py` to start live monitoring on the default `system.log`. 
To monitor a specific, custom log stream run `python analyzer.py path/to/your/active_stream.log`