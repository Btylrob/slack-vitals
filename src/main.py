import shutil
import os
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from dotenv import load_dotenv

load_dotenv()

slack_token = os.getenv('SLACKTOKEN')
channel_id = os.getenv('CHANNEL')


client = WebClient(token=slack_token)

def disk_usage_high(mount_point="/", threshold_percent=90):
    """Disk usage monitor logic"""
    total, used, free = shutil.disk_usage(mount_point)
    percent_used = used / total * 100
    return percent_used > threshold_percent, percent_used

if __name__ == "__main__":
    high_usage, percent = disk_usage_high("/", 90)
    
    if high_usage:
        try:
            result = client.chat_postMessage(
                channel=channel_id,
                text=f"🚨 Disk usage is high: {percent:.2f}% on mount point `/`"
            )
            print(result)
        except SlackApiError as e:
            print(f"Error: {e}")
    else:
        result = client.chat_postMessage(
            channel=channel_id,
            text="🚨 Testing"
        )