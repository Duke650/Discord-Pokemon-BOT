import discord
from discord.ext import commands
import requests
import os
from dotenv import load_dotenv
from discord.ext.commands import Bot, Context
from unittest.mock import Mock

load_dotenv()
TOKEN = os.environ.get('DISCORD_BOT_TOKEN')

intents = discord.Intents.all()

bot = commands.Bot(command_prefix="!", intents=intents)

POKE_URL = "https://pokeapi.co/api/v2/pokemon/"

response = requests.get(f"{POKE_URL}?limit=2000")
allPokemonNames = { pokemon['name'] for pokemon in response.json()['results'] }

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name} ({bot.user.id})")
    # await simulate_member_join()

@bot.event
async def on_member_join(member):
    
    await member.send(f"Welcome to the Server, {member.name}!")

# async def simulate_member_join():
#     # Create a mock Guild object
#     guild = Mock()
#     # Create a mock Member object
#     member = Mock()
#     # Manually trigger the on_member_join event
#     await bot.on_member_join(member)


@bot.command()
async def hello(contex):
    await contex.send("Hello There")

    

@bot.listen("on_message")
async def on_message(message):
    if message.author == bot.user:
        return
    if "hello" in message.content.lower():
        await message.add_reaction("🤙")
    
    context = await bot.get_context(message)
    if context.valid:
        return
    
    words = { word.lower() for word in message.content.split() }

    matchingNames = words.intersection(allPokemonNames)

    for pokemonName in matchingNames:
        response = requests.get(POKE_URL + pokemonName)
        data = response.json()
        spriteURL = data.get("sprites").get("versions").get("generation-v").get("black-white").get('animated').get("front_default")
        print("URL =>>",spriteURL)
        if not spriteURL:
            spriteURL = data['sprites']['front_default']
        embed = discord.Embed(title = f"You mentioned {pokemonName}!")
        embed.set_image(url=spriteURL)
        await message.channel.send(embed=embed)

bot.run(TOKEN)