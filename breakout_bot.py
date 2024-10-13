import pandas as pd
import numpy as np
import requests
import time
from datetime import datetime
from nsepy import get_live_price
import schedule

# Telegram bot settings
TOKEN = '7849356977:AAGe89SUiLCbtM7oZ6cbPRZPi5Yky57XXxU'  # Replace with your bot token
CHAT_ID = '6367887217'  # Replace with your chat ID

# Function to send message to Telegram
def send_telegram_message(message):
    url = f'https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={CHAT_ID}&text={message}'
    requests.get(url)

# Function to check breakouts
def check_breakouts():
    stocks = ['TCS', 'RELIANCE', 'HDFCBANK', 'INFY']  # Update to include stocks priced between 50 and 500
    breakout_stocks = []

    for stock in stocks:
        price = get_live_price(stock)
        if 50 <= price <= 500:  # Filter stocks based on price
            breakout_threshold = price + 5  # Setting breakout threshold
            # Simulating breakout logic (you can refine this)
            if price > breakout_threshold:
                breakout_stocks.append(stock)

    if breakout_stocks:
        message = f'Breakout alert: {", ".join(breakout_stocks)} at prices: {", ".join([str(get_live_price(s)) for s in breakout_stocks])}'
        send_telegram_message(message)
    else:
        print("No breakouts detected.")

# Schedule to run the check before market opens
def schedule_alerts():
    schedule.every().day.at("09:00").do(check_breakouts)
    
    while True:
        schedule.run_pending()
        time.sleep(1)

# Start scheduling alerts
if __name__ == "__main__":
    schedule_alerts()
