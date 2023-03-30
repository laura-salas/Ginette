import asyncio
import discord
from discord.ext import commands 
from dotenv import load_dotenv 
from enum import Enum
import os
import random 
from typing import List

# local modules 
from chatter import *
from faq import *

load_dotenv()

start_sequence = "\nA:"
restart_sequence = "\n\nQ: "

description = "A discord bot that uses GPT3 API to converse with users. "
TOKEN = os.getenv('DISCORD_API')
CHATTER_CHANNEL = int(os.getenv('CHATTER_CHANNEL'))
FAQ_CHANNEL = int(os.getenv('FAQ_CHANNEL'))
FAQ_DB = int(os.getenv('FAQ_DB_CHANNEL'))

intents = discord.Intents.all()

intents.members = True
intents.message_content = True
Embed = discord.Embed

intents.reactions = True
intents.members = True
client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix="$", description=description, intents=intents)
recentEmoji = [""]


@client.event
async def on_raw_reaction_add(reaction):
    if reaction.channel_id == CHATTER_CHANNEL:
        await react_to_message(reaction)
    
@client.event
async def on_message(message):
    if message.author == client.user:
        return
    else:
        # chatting with ginette
        if message.channel.id == client.get_channel(CHATTER_CHANNEL).id:
            await chat_with_ginette(message, client)
        # faq handling 
        # elif message.channel.id == client.get_channel(FAQ_CHANNEL).id:
        #     await reply_to_question(message, client, client.get_channel(FAQ_DB))
        elif client.user in message.mentions:
            await reply_to_question(message, client, client.get_channel(FAQ_DB))
        # new faq database addition
        elif message.channel.id == client.get_channel(FAQ_DB).id:
            await validate_faq_add(message, client, client.get_channel(FAQ_DB))

@client.event
async def on_ready(): 
    initialize_ginette(client.get_channel(CHATTER_CHANNEL))
    print('We have logged in as {0.user}'.format(client))
    
client.run(TOKEN)
