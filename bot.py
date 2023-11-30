import nextcord
from nextcord.ext.commands import Bot
import os
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv('DISCORD_TOKEN')

intents = nextcord.Intents.all()
bot = Bot(intents=intents)

@bot.event
async def on_ready():
    print("The bot is now running!")
    print("------------------------")

for cogpath in os.listdir("cogs"):
    if cogpath.endswith(".py"):
        bot.load_extension(f'cogs.{cogpath[:-3]}')

bot.run(BOT_TOKEN)