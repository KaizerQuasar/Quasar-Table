import discord
import asyncio
import json
import requests
import re

def extract_price(price_str):
    return int(re.sub(r'[^0-9]', '', price_str))

intents = discord.Intents.all()
intents.message_content = True

client = discord.Client(intents=intents)
emoji_dict = {}
update_interval_hours = 4

async def update_stock_info(message):
    try:
        response = requests.get('Yoursite.com')
        response.raise_for_status()  # Raise an exception for 4xx and 5xx status codes
        data = response.json()

        in_stock = {k: extract_price(v) for k, v in data.items() if 'Out of Stock' not in v}

        sorted_items = sorted(in_stock.items(), key=lambda x: x[1], reverse=True)

        items_strings = [
            f"<:{item.replace('-', '')}:{emoji_dict.get(item.replace('-', ''), '')}>{item.split('-')[0]}: ${price:,}"
            for item, price in sorted_items
        ]

        result = '\n'.join(items_strings)
        await message.channel.send(result)
        await message.channel.send("<@&1133244097184923688>")
    except requests.RequestException as e:
        print(f"Error updating stock information: {e}")
        await message.channel.send("Error updating stock information. Please try again later.")

async def initiate_monitoring(message):
    await message.channel.send(f"Monitoring will start in fruits in {message.channel.name} ")

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
    for emoji in client.emojis:
        emoji_dict[emoji.name] = emoji.id

@client.event
async def on_message(message):
    if message.content.startswith("$hello"):
        await message.channel.send("Hello cutie")
    elif message.content.startswith("$start_monitoring"):
        await initiate_monitoring(message)
        await asyncio.sleep(60 * 60 * 3.5)
        while True:
            await update_stock_info(message)
            await asyncio.sleep(60 * 60 * update_interval_hours)
    elif message.content.startswith("$force_update"):
        await update_stock_info(message)


client.run('Your token')
