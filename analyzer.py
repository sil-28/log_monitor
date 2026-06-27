import csv
import requests
import os
from dotenv import load_dotenv
import sys

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
    input_file = 'app.log'

output_file = 'report_errors.csv'

print("Starting analysis of the log file\n")

# open log file and create csv file
try:
    with open(input_file, 'r') as log_file:
        with open(output_file, 'w', newline='', encoding='utf-8') as csv_file:
            writer_csv = csv.writer(csv_file, delimiter=";")
            # write table header
            writer_csv.writerow(['Date', 'Time', 'Level', 'Message'])
            
            for row in log_file:
                if 'ERROR' in row or 'CRITICAL' in row:
                    
                    # divide the row based on the blank spaces
                    parts = row.split()
                    
                    date = parts[0]
                    time = parts[1]
                    level = parts[2]
                    message = " ".join(parts[3:])
                    
                    # write in the table
                    writer_csv.writerow([date, time, level, message])
                    
                    # if the level is Critical, send an allert on telegram
                    if level == 'CRITICAL':
                        mex = f"🚨 ALLERT  🚨\n\n Date: {date} {time}\nLevel: {level}\nAnomaly: {message}"
                        send_message_telegram(mex)
                        print("-> notification sent")
                        
    print("Analysis completed")
    
except FileNotFoundError:
    print(f"❌ Error: The file '{input_file}' doesn't exist. Verify the path.")
except PermissionError:
    print(f"❌ Error: You don't have the permissions to read the file '{input_file}'.")

