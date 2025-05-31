import os
import time
import shutil
import threading
import platform
import multiprocessing
import psutil
import time
import socket
import datetime
import logging
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from dotenv import load_dotenv
from datetime import datetime


night_log = "night_log.log"
logging.basicConfig(
    filename=night_log,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


load_dotenv()

slack_token = os.getenv("SLACKTOKEN")
app_token = os.getenv("SLACKAPP_TOKEN")  # You need this for Socket Mode
channel_id = os.getenv("CHANNEL")

client = WebClient(token=slack_token)
app = App(token=slack_token)

"""check if it is 11am - 5am"""
def nightime():
    now = datetime.now().time()
    return now >= datetime.strptime("23:00", "%H:%M").time() or now <= datetime.strptime("05:00", "%H:%M").time()
def send_slack_message(message: str):
    try:
        response = client.chat_postMessage(channel=channel_id, text=message)
        print("Slack message sent:", response)
        if nightime():
            logging.info(message)
        else:
            return  
    except SlackApiError as e:
        print(f"Slack API error: {e.response['error']}")


def in_between(number, lowerbound, upperbound):
    return lowerbound <= number <= upperbound


def ethernet_grab(interface="eth0"):
    stats = psutil.net_if_stats()
    return stats.get(interface, None) and stats[interface].isup


def ethernet_check(interval=60):
    while True:
        if ethernet_grab("eth0"):
            print("Ethernet connection: eth0 is up")
        else:
            send_slack_message("🚨 Ethernet connection not successful")
        time.sleep(interval)


def cpu_temp_check(interval=60):
    while True:
        temps = psutil.sensors_temperatures()
        if "coretemp" in temps and temps["coretemp"]:
            cpu_temp = temps["coretemp"][0].current
            if in_between(cpu_temp, 1, 75):
                print(f"CPU temp normal: {cpu_temp}")
            else:
                send_slack_message(f"🚨 CPU temp high: {cpu_temp}°C")
        else:
            send_slack_message("🚨 CPU temp not retrievable")
        time.sleep(interval)


def monitor_cpu(interval=60, threshold=70):
    while True:
        global usage
        usage = psutil.cpu_percent(interval=1)
        if usage > threshold:
            send_slack_message(f"🚨 CPU usage high: {usage:.2f}% (threshold: {threshold}%)")
        else:
            print(f"CPU usage normal: {usage:.2f}%")
        time.sleep(interval)


def disk_usage_high(mount_point="/", threshold_percent=90):
    total, used, _ = shutil.disk_usage(mount_point)
    percent_used = used / total * 100
    return percent_used > threshold_percent, percent_used


def disk_monitor_usage(interval=60, threshold=90):
    while True:
        high_usage, percent = disk_usage_high("/", threshold)
        if high_usage:
            send_slack_message(f"🚨 Disk usage high: {percent:.2f}% on `/`")
        else:
            print(f"Disk usage normal: {percent:.2f}%")
        time.sleep(interval)
# Uptime
def get_uptime():
    with open('/proc/uptime', 'r') as f:
        uptime_seconds = float(f.readline().split()[0])
# Bytes sent and recieved
bytes_sent = psutil.net_io_counters()
#status of alpaca api
#TODO GET API KEY SET UP METHOD THROUGH REQUESTS TO VALIDATE

@app.command("/vitals")
def handle_vitals_command(ack, respond, command):
    ack()
    
    # Example dummy values — ensure you have real data here
    system_name = platform.system()
    hostname = socket.gethostname() 
    memory_usage = psutil.virtual_memory()[2]
    memory_usage_gb = psutil.virtual_memory()[3]/1000000000
    disk_usage = 62
    process_count = multiprocessing.cpu_count()
    uptime_seconds = get_uptime()
    bytes_recv = 3.21
    urls_info = "https://example.com/monitor"

    user = command["user_name"]
    
    respond(
        f"""📊 *System Information*
🌍 *System Name:* `{system_name}`
📌 *Hostname:* `{hostname}`
🖥️ *CPU Usage:* `{usage:.2f}%`
🧠 *Memory Usage:* `{memory_usage}% ({memory_usage_gb} GB)`
💽 *Disk Usage:* `{disk_usage}%`
👾 *Process Count:* `{process_count}`
🕰️ *Uptime:* `{uptime_seconds}`
🌐 *Network Info:*
    📤 *Bytes Sent:* `{bytes_sent} GB`
    📥 *Bytes Recv:* `{bytes_recv} GB`
🔑 *API Keys:*
    🦙 *Alpaca:* `{alpaca_bool}`
🔗 *Monitor URL:* <{urls_info}>
"""
    )


if __name__ == "__main__":
    # Start background monitoring threads
    threading.Thread(target=monitor_cpu, kwargs={"interval": 60}).start()
    threading.Thread(target=disk_monitor_usage, kwargs={"interval": 60}).start()
    threading.Thread(target=cpu_temp_check, kwargs={"interval": 60}).start()
    threading.Thread(target=ethernet_check, kwargs={"interval": 60}).start()

    # Start Slack slash command listener
    SocketModeHandler(app, app_token).start()
