import discord
from ds_token import token

TOKEN = token()

client = discord.Client(intents=discord.Intents.all())

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):

    if message.content == '%Hello':
        await message.channel.send('World!')

client.run(TOKEN)
