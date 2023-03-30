import os
from dotenv import load_dotenv

from chatter import *
from faq import *

import discord
import random 
import asyncio
from typing import List
from enum import Enum
 
from discord.ext import commands 

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
        elif message.channel.id == client.get_channel(FAQ_CHANNEL).id:
            await reply_to_question(message, client, client.get_channel(FAQ_DB))

@client.event
async def on_ready(): 
    initialize_ginette(client.get_channel(CHATTER_CHANNEL))
    print('We have logged in as {0.user}'.format(client))
    
client.run(TOKEN)
