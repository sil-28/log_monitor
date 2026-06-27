import csv
import requests
import os
from dotenv import load_dotenv
import sys
import time

# load variables from .env
load_dotenv()
Token_telegram = os.getenv("Token_telegram")
Chat_ID_telegram = os.getenv("Chat_ID_telegram")

def send_message_telegram(mex):
    url = f"https://api.telegram.org/bot{Token_telegram}/sendMessage"
    payload = {'chat_id' : Chat_ID_telegram,
               'text' : mex}
    
    try:
        # send request to Telegram server
        requests.post(url, json = payload)
    except Exception as e:
        print(f"Error sending message on telegram: {e}")

# open the specified log file. If not specified, use the default one
if len(sys.argv)>1:
    input_file = sys.argv[1]
else:
    input_file = 'system.log'

output_file = 'report_errors.csv'

print("Starting analysis of the log file\n")

# open log file and create csv file
try:
    with open(input_file, 'r') as log_file:
        with open(output_file, 'w', newline='', encoding='utf-8') as csv_file:
            writer_csv = csv.writer(csv_file, delimiter=";")
            
            if os.stat(output_file).st_size == 0:
                # write table header
                writer_csv.writerow(['Date', 'Time', 'Level', 'Message'])
                csv_file.flush()
                
            while(True):
                row = log_file.readline()
                
                if not row:
                    time.sleep(1) 
                    continue
                
                if 'ERROR' in row or 'CRITICAL' in row:
                    # divide the row based on the blank spaces
                    parts = row.split()
                    
                    # Seccurity check: verify that the row has enough elements
                    if len(parts)>=4:
                        date = parts[0]
                        time_str = parts[1]
                        level = parts[2]
                        message = " ".join(parts[3:])
                        
                        # write in the table
                        writer_csv.writerow([date, time_str, level, message])
                        csv_file.flush()
                        
                        # if the level is Critical, send an allert on telegram
                        if level == 'CRITICAL':
                            mex = f"🚨 ALERT  from log file {input_file} 🚨\n\n Date: {date} {time_str}\nLevel: {level}\nAnomaly: {message}"
                            send_message_telegram(mex)
                            print("-> Critical anomaly detected! Notification sent.")
                        
    print("Analysis completed")
    
except FileNotFoundError:
    print(f"❌ Error: The file '{input_file}' doesn't exist.")
except PermissionError:
    print(f"❌ Error: Permission denied for '{input_file}'.")
except KeyboardInterrupt:
    print("\n👋 Monitoring stopped by user.")

