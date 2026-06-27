import csv
import requests
import os
from dotenv import load_dotenv

load_dotenv()
Token_telegram = os.getenv("Token_telegram")
Chat_ID_telegram = os.getenv("Chat_ID_telegram")

def send_message_telegram(mex):
    url = f"https://api.telegram.org/bot{Token_telegram}/sendMessage"
    payload = {'chat_id' : Chat_ID_telegram,
               'text' : mex}
    
    try:
        requests.post(url, json = payload)
    except Exception as e:
        print(f"Error sending message on telegram: {e}")


input_file = 'app.log'
output_file = 'report_errors.csv'

print("Starting analysis of the log file\n")

with open(input_file, 'r') as log_file, open(output_file, 'w', newline='', encoding='utf-8') as csv_file:
    
    writer_csv = csv.writer(csv_file, delimiter=";")
    writer_csv.writerow(['Date', 'Time', 'Level', 'Message'])
    
    for row in log_file:
        if 'ERROR' in row or 'CRITICAL' in row:
            parts = row.split()
            
            date = parts[0]
            time = parts[1]
            level = parts[2]
            message = " ".join(parts[3:])
            
            writer_csv.writerow([date, time, level, message])
            
            if level == 'CRITICAL':
                mex = f"🚨 ALLERT  🚨\n\n Date: {date} {time}\nLevel: {level}\nAnomaly: {message}"
                send_message_telegram(mex)
                print("-> notification sent")
    
print("Analysis completed")
            


"""
# open log file as read only
with open('app.log', 'r') as log_file:
    # open output file as write only
    with open('report_errors.txt', 'w') as output_file:
        print("Starting analysis of the log file\n")
        output_file.write("--- REPORT ERRORS FOUNDED ---\n\n")
        
        for row in log_file:
            if "ERROR" in row or "CRITICAL" in row:
                print(f"Anomaly founded: {row.strip()}")
                
                output_file.write(row)
print("Analysis completed")
"""