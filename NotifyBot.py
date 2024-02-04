import discord
import asyncio
import json
import requests
import re

def extract_price(price_str):
    return int(re.sub(r'[^0-9]', '', price_str))

class FruitMonitorBot(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.emoji_dict = {}
        self.update_interval_hours = 4

    async def on_ready(self):
        print(f'Logged in, {self.user}')
        for emoji in self.emojis:
            self.emoji_dict[emoji.name] = emoji.id

    async def on_message(self, message):
        if message.author == self.user:
            return

        if message.content.startswith("$hello"):
            await message.channel.send("Hello cutie")
        elif message.content.startswith("$start_monitoring"):
            await self.initiate_monitoring(message)
        elif message.content.startswith("$force_update"):
            await self.update_stock_info(message)

    async def initiate_monitoring(self, message):
        await message.channel.send(f"Monitoring will start in fruits in {message.channel.name} ")
        await asyncio.sleep(60 * 60 * 3.5)
        while True:
            await self.update_stock_info(message)
            await asyncio.sleep(60 * 60 * self.update_interval_hours)

    async def update_stock_info(self, message):
        try:
            response = requests.get('Yoursite.com')
            response.raise_for_status()
            data = response.json()

            in_stock = {k: extract_price(v) for k, v in data.items() if 'Out of Stock' not in v}

            sorted_items = sorted(in_stock.items(), key=lambda x: x[1], reverse=True)

            items_strings = [
                f"<:{item.replace('-', '')}:{self.emoji_dict.get(item.replace('-', ''), '')}>{item.split('-')[0]}: ${price:,}"
                for item, price in sorted_items
            ]

            result = '\n'.join(items_strings)
            await message.channel.send(result)
            await message.channel.send("<@&1133244097184923688>")
        except requests.RequestException as e:
            print(f"Error updating stock information: {e}")
            await message.channel.send("Error updating stock information. Please try again later.")

if __name__ == "__main__":
    client = FruitMonitorBot()
    client.run('Your token')
