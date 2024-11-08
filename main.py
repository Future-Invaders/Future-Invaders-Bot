import discord
import json
import os
import requests
from discord import guild_only
from dotenv import load_dotenv
from markdownify import markdownify
from requests.exceptions import HTTPError


load_dotenv() # load all the variables from the env file
LANGUAGES = ['en', 'fr']
bot = discord.Bot()

def process_response(response: str, language: str):
    if response['cards'] is None:
        return "No cards found :("
    else:
        return embed_card(response['cards'][0], language)

def embed_card(card: dict, language: str):
    embed = discord.Embed(
        title=f"{card['name'][language]}",
        description=f"{card['faction']['name'][language]} {card['type']['name'][language]}",
        color=discord.Colour.blurple(), # Pycord provides a class with default colors you can choose from
    )
    if card['cost'] == "":
        card['cost'] = "None"
    if card['income'] == "":
        card['income'] = "None"
    card_body = markdownify(card['body'][language])
    embed.add_field(name="Resources", value=f"**Cost:** {card['cost']} **Income:** {card['income']}", inline=True)
    embed.add_field(name="Combat", value=f"**Weapons:** {card['weapons']} **Durability:** {card['durability']}", inline=True)
    embed.add_field(name="Effect", value=f"{card_body}",inline=False)
    embed.add_field(name="Database link", value=f"{card['url']}")
    embed.set_footer(text=f"Rarity: {card['rarity']['name'][language]} - Release: {card['release']['name'][language]}")
    embed.set_thumbnail(url=f"{card['images'][language]['path']}")

    return embed

async def languages(context: discord.ApplicationContext):
    return LANGUAGES

@bot.event
async def on_ready():
    print(f"{bot.user} is ready and online!")

@bot.slash_command(name="hello", description="Say hello to the bot")
async def hello(context: discord.ApplicationContext):
    await context.respond("Hey!")

#async def cardsearch(context: discord.ApplicationContext, query: discord.SlashCommandOptionType.string, languages: discord.Option(str, autocomplete=discord.utils.basic_autocomplete(languages))):
@bot.slash_command(name="cardsearch", description="Search for a card")
@guild_only()
async def cardsearch(
    context: discord.ApplicationContext,
    query: discord.Option(str),
    languages: discord.Option(str, autocomplete=discord.utils.basic_autocomplete(languages), default=LANGUAGES[0])
    ):
    try:
        url = os.getenv('API_ENDPOINT')
        response = requests.get(f"{url}/cards", params={'name': query})
        response.raise_for_status()
        answer = process_response(response.json(), languages)
        await context.respond(embed=answer)
    except HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"Other error occurred: {err}")
    

bot.run(os.getenv('TOKEN')) # run the bot with the token