import os
import time
import shutil
import threading

import psutil
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from dotenv import load_dotenv

load_dotenv()

slack_token = os.getenv("SLACKTOKEN")
channel_id = os.getenv("CHANNEL")

client = WebClient(token=slack_token)


def send_slack_message(message: str):
    try:
        response = client.chat_postMessage(channel=channel_id, text=message)
        print("Slack message sent:", response)
    except SlackApiError as e:
        print(f"Slack API error: {e.response['error']}")


def in_between(number, lowerbound, upperbound):
    return lowerbound <= number <= upperbound


def cpu_temp_check(interval=60):
    try:
        while True:
            temps = psutil.sensors_temperatures()
            if "coretemp" in temps and temps["coretemp"]:
                cpu_temp = temps["coretemp"][0].current
                if in_between(cpu_temp, 60, 75):
                    print("CPU temp normal")
                    print(cpu_temp)
                else:
                   send_slack_message(
                    f"🚨 CPU temp has exceeded limits: {cpu_temp}")
            else:
                send_slack_message(
                    f"🚨 CPU temp unretrievable")
            time.sleep(interval)
    except KeyboardInterrupt:
        print("Stopped by user")


def monitor_cpu(interval=60, threshold=70):
    try:
        while True:
            usage = psutil.cpu_percent(interval=1)
            if usage > threshold:
                send_slack_message(
                    f"🚨 CPU usage is high: {usage}% (threshold: {threshold}%)")
            else:
                print("CPU usage normal")
            time.sleep(interval)
    except KeyboardInterrupt:
        print("Stopped by user")


def disk_usage_high(mount_point="/", threshold_percent=90):
    total, used, _ = shutil.disk_usage(mount_point)
    percent_used = used / total * 100
    return percent_used > threshold_percent, percent_used


def disk_monitor_usage(interval=60, threshold=90):
    try:
        while True:
            high_usage, percent = disk_usage_high("/", threshold)
            if high_usage:
                send_slack_message(
                    f"🚨 Disk usage is high: {percent:.2f}% on mount point `/`")
            else:
                print("Disk usage normal")
            time.sleep(interval)
    except KeyboardInterrupt:
        print("Stopped by user")


if __name__ == "__main__":
    cpu_thread = threading.Thread(target=monitor_cpu, kwargs={"interval": 60})
    disk_thread = threading.Thread(target=disk_monitor_usage,
                                   kwargs={"interval": 60})
    cpu_temp_thread = threading.Thread(target=cpu_temp_check,
                                       kwargs={"interval": 60})

    cpu_thread.start()
    cpu_temp_thread.start()
    disk_thread.start()

    cpu_thread.join()
    cpu_temp_thread.join()
    disk_thread.join()
