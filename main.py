import discord
from discord.ext import commands
from discord import FFmpegPCMAudio
from apikey import *
from profanity_check import predict
import requests, json

# initialize bot
intents = discord.Intents.default()
intents.members = True
intents.message_content = True
client = commands.Bot(command_prefix='!', intents=intents)

# this function is executed when the bot is ready to receive commands
@client.event
async def on_ready():
    print('The bot is ready for use')
    print('-------------------------')

# when a user types !hello this function will run
@client.command()
async def hi(ctx):
    url = "https://dad-jokes.p.rapidapi.com/random/joke"

    headers = {
        "X-RapidAPI-Key": JOKE_API,
        "X-RapidAPI-Host": "dad-jokes.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers)

    joke = json.loads(response.text)['body']

    await ctx.send(f"hi! \n\n{joke[0]['setup']}\n\n{joke[0]['punchline']}")


# detect when someone joins your server and send a message
@client.event
async def on_member_join(member):
    channel = client.get_channel(CHANNEL_ID)
    await channel.send('Hello')

# detect when someone leaves your server and send a message
@client.event
async def on_member_remove(member):
    channel = client.get_channel(CHANNEL_ID)
    await channel.send('Goodbye')

@client.command(pass_context=True)
async def join(ctx):
    if (ctx.author.voice):
        channel = ctx.message.author.voice.channel
        voice = await channel.connect()
        source = FFmpegPCMAudio('dog-barking.wav')
        player = voice.play(source)
    else:
        await ctx.send('You must be in a voice channel to run this command.')

# if the bot is in a voice channel then it'll leave and send message
@client.command(pass_context=True)
async def leave(ctx):
    if (ctx.voice_client):
        await ctx.guild.voice_client.disconnect()
        await ctx.send('I\'ve left the voice channel')
    else:
        await ctx.send('I am not in a voice channel')

# detecting specific words through events
@client.event
async def on_message(message):
    if predict([message.content]) > 0:
        await message.delete()
        await message.channel.send('Don\'t send that again')

# link the bot to the web app (tells the bot to run)
client.run(BOT_TOKEN)

