from datetime import datetime, timezone
import asyncio
from telethon import TelegramClient, events
from okxtradefunctions import categorize_message  # Updated function name
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Telegram API credentials from .env file
username = os.getenv("TELEGRAM_USERNAME")
phone = os.getenv("TELEGRAM_PHONE")
api_id = os.getenv("TELEGRAM_API_ID")
api_hash = os.getenv("TELEGRAM_API_HASH")

# Channel to be monitored
channel = 'https://t.me/channelid'  
file_name = 'signal.txt'  

# Start date for processing messages
d_min = 27  # Start day
m_min = 2   # Start month
y_min = 2024  # Start year

# End date for processing messages
# Example: If you want to process messages for 10 days, set the appropriate end date.
d_max = 10  # End day
m_max = 3   # End month
y_max = 2024  # End year

# Function to process new incoming messages
async def handle_new_message(event):
    message = event.message

    if message.date < datetime(y_max, m_max, d_max, tzinfo=timezone.utc) and message.date > datetime(y_min, m_min, d_min, tzinfo=timezone.utc):
        # Process only text messages
        if len(message.text) < 42 and not message.media:
            content = f'|Transaction: {categorize_message(message.text)} \n'  # Updated function name
            # Write the message to a file
            with open(file_name, 'a', encoding='utf-8') as file:
                file.write(content)

# Start the TelegramClient
async def main():
    async with TelegramClient(username, api_id, api_hash) as client:
        # Add event handler for new messages
        client.add_event_handler(handle_new_message, events.NewMessage(chats=channel))
        print("TelegramClient started. Listening for messages...")
        # Keep listening for messages indefinitely
        await client.run_until_disconnected()

# Run the main function
if __name__ == '__main__':
    asyncio.run(main())
