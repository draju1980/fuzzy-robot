import os
import feedparser
import json
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

def send_discord_message(webhook_url, message):
    """
    Send a message to a Discord channel using a webhook URL.
    """
    payload = {"content": message}
    headers = {"Content-Type": "application/json"}
    response = requests.post(webhook_url, data=json.dumps(payload), headers=headers)
    if response.status_code != 204:
        print(f"Error sending Discord message: {response.text}")

def send_slack_message(webhook_url, message):
    """
    Send a message to a Slack channel using a webhook URL.
    """
    payload = {"text": message}
    headers = {"Content-Type": "application/json"}
    response = requests.post(webhook_url, data=json.dumps(payload), headers=headers)
    if response.status_code != 200:
        print(f"Error sending Slack message: {response.text}")

def send_telegram_message(bot_token, chat_id, message):
    """
    Send a message to a Telegram chat using a bot token and chat ID.
    """
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message
    }
    response = requests.post(url, data=payload)
    if response.status_code != 200:
        print(f"Error sending Telegram message: {response.text}")

def read_rss_feed(url):
    """
    Read the RSS feed from the given URL and return the latest message
    if it was posted within the last hour.
    """
    feed = feedparser.parse(url)
    if feed.entries:
        latest_entry = feed.entries[0]
        published_time = datetime(*latest_entry.published_parsed[:6])
        one_hour_ago = datetime.now() - timedelta(hours=1)
        if published_time > one_hour_ago:
            soup = BeautifulSoup(latest_entry.description, 'html.parser')
            description_text = soup.get_text(separator=' ')
            message = f"Title: {latest_entry.title}\nLink: {latest_entry.link}\nDescription: {description_text}"
            return message
    return None

if __name__ == "__main__":
    # Load secrets from environment variables
    discord_webhook_url = os.getenv('DISCORD_WEBHOOK_URL')
    slack_webhook_url = os.getenv('SLACK_WEBHOOK_URL')
    telegram_bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
    telegram_chat_id = os.getenv('TELEGRAM_CHAT_ID')
    
    # RSS feed URL
    rss_url = "https://status.zetachain.com/history.rss"
    
    # Read the latest message from the RSS feed
    latest_message = read_rss_feed(rss_url)

    if latest_message:
        # Check if the message is a scheduled event
        is_scheduled_event = "THIS IS A SCHEDULED EVENT" in latest_message
        # Check if the current hour is midnight
        is_midnight = datetime.now().hour == 0

        # Send messages based on conditions
        if is_scheduled_event:
            if is_midnight:
                # Send scheduled event messages only at midnight
                if discord_webhook_url:
                    send_discord_message(discord_webhook_url, latest_message)
                if slack_webhook_url:
                    send_slack_message(slack_webhook_url, latest_message)
                if telegram_bot_token and telegram_chat_id:
                    send_telegram_message(telegram_bot_token, telegram_chat_id, latest_message)
        else:
            # Send non-scheduled event messages immediately
            if discord_webhook_url:
                send_discord_message(discord_webhook_url, latest_message)
            if slack_webhook_url:
                send_slack_message(slack_webhook_url, latest_message)
            if telegram_bot_token and telegram_chat_id:
                send_telegram_message(telegram_bot_token, telegram_chat_id, latest_message)