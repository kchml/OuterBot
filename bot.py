import discord
import responses
from ds_token import token
from scraper import weather_scraper, ytlink_scraper
from discord.ext import commands
from discord import FFmpegPCMAudio


async def on_message(message, user_message, is_private):
    try:
        response = responses.handle_response(user_message)
        
        if is_private:
            await message.author.send(response)
        else:
            message.channel.send(response)

    except Exception as e:
        print(e)


TOKEN = token()
client = commands.Bot(intents=discord.Intents.all(), command_prefix = '$')

@client.event
async def on_ready():
    print(f'{client.user} is now running')

@client.command()
async def test(ctx):
    await ctx.send("test passed correctly")

@client.command(pass_context = True)
async def join(ctx):
    if (ctx.author.voice):
        channel = ctx.message.author.voice.channel
        voice = await channel.connect()
        source = FFmpegPCMAudio('song.mp3')
        player = voice.play(source)

    else:
        await ctx.send("You are not in the voice channel.")

@client.command(pass_context = True)
async def pause(ctx):
    voice = discord.utils.get(client.voice_clients, guild = ctx.guild)
    if voice.is_playing():
        voice.pause()
    else:
        await ctx.send("No audio playing at the moment.")

@client.command(pass_context = True)
async def leave(ctx):
    if (ctx.voice_client):
        await ctx.guild.voice_client.disconnect()
        await ctx.send("Bye, have a great time!")
    else:
        await ctx.send('I am not in a voice channel!')

@client.command(pass_context = True)
async def resume(ctx):
    voice = discord.utils.get(client.voice_clients, guild = ctx.guild)
    if voice.is_paused():
        voice.resume()
    else:
        await ctx.send("Not any song is paused.")

@client.command(pass_context = True)
async def stop(ctx):
    voice = discord.utils.get(client.voice_clients, guild = ctx.guild)
    voice.stop()

# @client.command(pass_context = True)
# async def play(ctx, arg):
#     voice = ctx.guild.voice_client
#     source = FFmpegPCMAudio(arg)
#     player = voice.play(source)

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    username = str(message.author)
    user_message = str(message.content)
    channel = str(message.channel)

    if user_message[0] == '$':
        user_message = user_message[1:]
        
        if user_message == 'hello':
            await message.channel.send('hello there')

        if user_message == 'name':
            await message.channel.send(message.author)

        if user_message == 'channel':
            await message.channel.send(message.channel)

        if user_message.startswith('weather'):

            weatherparts = user_message.split(" ", 1)
            city = weatherparts[1]
            weather = weather_scraper(city)
            if weather != None:
                weather_msg = f'Temperature in {city}: {weather}°C'
                await message.channel.send(weather_msg)
            else:
                await message.channel.send("Can't find that place.")

        if user_message.startswith('ytlink'):

            ytlinkparts = user_message.split(" ", 1)
            phrase = ytlinkparts[1]
            phrase = phrase.replace(" ", "+")
            ytlink = ytlink_scraper(phrase)  
            if ytlink != None:
                await message.channel.send(ytlink)
            else:
                await message.channel.send("Can't find that thing.")

        if user_message == 'help':
            help_message = ""
            help_message = help_message + '$hello - saying hello to you\n'
            help_message = help_message + '$name - saying your name\n'
            help_message = help_message + '$channel - saying the channel in which you are\n'
            help_message = help_message + '$weather <city> - saying the temperature in the city\n'
            help_message = help_message + '$ytlink <phrase> - searching a link to a typed phrase on youtube\n'

            await message.channel.send(help_message)

    await client.process_commands(message)

            
client.run(TOKEN)
