import discord
import responses
from ds_token import token
from scraper import weather_scraper, ytlink_scraper
from discord.ext import commands
from discord import FFmpegPCMAudio
import os
import yt_dlp


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

@client.command(pass_context = True)
async def ytplay(ctx, *, url:str):
    for file in os.listdir('./'):
        if file == 'song.mp3':
            os.remove(file)

    if (ctx.author.voice):
        channel = ctx.message.author.voice.channel

        if (ctx.voice_client):
            voice = discord.utils.get(client.voice_clients, guild = ctx.guild)
        else:
            voice = await channel.connect()

        ydl_opts = {
            'format': 'bestaudio',
            'keepvideo': 'False',
            'postporcessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }


        if url.startswith('http') or url.startswith('www.') or url.startswith('youtube.com'):
            pass
        else:
            link = ytlink_scraper(url)
            url = link

        with yt_dlp.YoutubeDL(ydl_opts) as ydlp:
            ydlp.download([url])

        for file in os.listdir('./'):
            if file.endswith(".mp3"):
                os.rename(file, 'song.mp3')
            elif file.endswith('.m4a'):
                os.rename(file, 'song.mp3')
            elif file.endswith('.webm'):
                os.rename(file, 'song.mp3')
                
        source = FFmpegPCMAudio('song.mp3')
        player = voice.play(source)
        print('kaczka')



    else:
        await ctx.send("You are not in the voice channel.")

@client.command(pass_context = True)
async def hello(ctx):
    await ctx.send("Hello there!")

@client.command(pass_context = True)
async def weather(ctx, city:str):
    wth = weather_scraper(city)
    if wth != None:
        weather_msg = f'Temperature in {city}: {wth}°C'
        await ctx.send(weather_msg)
    else:
        await ctx.send("Can't find that place.")

@client.command(pass_context = True)
async def ytlink(ctx, *, phrase:str):
    link = ytlink_scraper(phrase)

    if link != None:
        await ctx.send(link)
    else:
        await ctx.send("Can't find that thing.")

async def help(ctx):

    help_message = ""
    help_message = help_message + '$hello - saying hello to you.\n'
    help_message = help_message + '$ytplay - playing music from youtube which you typed after space. It can be direct link or just a phrase.\n'
    help_message = help_message + '$pause - pausing current music.\n'
    help_message = help_message + '$stop - stoping current music.\n'
    help_message = help_message + '$resume - resuming current music.\n'
    help_message = help_message + '$leave - leaving from the voice channel.\n'
    help_message = help_message + '$weather <city> - saying the temperature in the city\n'
    help_message = help_message + '$ytlink <phrase> - searching a link to a typed phrase on youtube\n'

    await ctx.send(help_message)
            
client.run(TOKEN)
