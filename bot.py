import discord
import responses
from ds_token import token
from scraper import weather_scraper

# voice = discord.VoiceState(deaf = True, mute = False, self_mute = False, 
# self_deaf = False, self_stream = False, self_video = False, suppress = True, afk = True)

async def on_message(message, user_message, is_private):
    try:
        response = responses.handle_response(user_message)
        
        if is_private:
            await message.author.send(response)
        else:
            message.channel.send(response)

    except Exception as e:
        print(e)

def run_discord_bot():
    TOKEN = token()
    client = discord.Client(intents=discord.Intents.all())

    @client.event
    async def on_ready():
        print(f'{client.user} is now running')


    @client.event
    async def on_message(message):
        if message.author == client.user:
            return


        username = str(message.author)
        user_message = str(message.content)
        channel = str(message.channel)

        print(f"{username} said: '{user_message}' ({channel})")

        await message.channel.send(f"{username} said: '{user_message}' ({channel})")


        if user_message[0] == '$':
            user_message = user_message[1:]
            
            if user_message == 'hello':

                await message.channel.send('hello there')


            if user_message == 'name':
                await message.channel.send(message.author)
            else:
                pass

            if user_message == 'channel':
                await message.channel.send(message.channel)
            else:
                pass

            if user_message.startswith('weather'):

                weatherparts = user_message.split(" ")

                city = weatherparts[1]

                weather = weather_scraper(city)

                weather_msg = city + ': ' + weather

                await message.channel.send(weather_msg)


    client.run(TOKEN)
