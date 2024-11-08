"""Discord bot for the Future Invaders card game"""

import os
import requests
import discord
from discord import guild_only
from dotenv import load_dotenv
from markdownify import markdownify
from requests.exceptions import HTTPError


load_dotenv() # load all the variables from the env file
API_LANGUAGES = ['en', 'fr']
bot = discord.Bot()

def process_response(response: str, language: str):
    """Returns the result of a card query, nicely formatted"""
    if response['cards'] is None:
        return "No cards found :("
    return embed_card(response['cards'][0], language)

def embed_card(card: dict, language: str):
    """Formats an embed to display a card"""
    embed = discord.Embed(
        title=f"{card['name'][language]}",
        description=f"{card['faction']['name'][language]} {card['type']['name'][language]}",
        # TODO: use faction color
        color=discord.Colour.blurple(),
    )
    if card['cost'] == "":
        card['cost'] = "None"
    if card['income'] == "":
        card['income'] = "None"
    card_body = markdownify(card['body'][language])
    rarity = card['rarity']['name'][language]
    release = card['release']['name'][language]
    embed.add_field(name="Resources",
                    value=f"**Cost:** {card['cost']} **Income:** {card['income']}",
                    inline=True)
    embed.add_field(name="Combat",
                    value=f"**Weapons:** {card['weapons']} **Durability:** {card['durability']}",
                    inline=True)
    embed.add_field(name="Effect", value=f"{card_body}",inline=False)
    embed.add_field(name="Database link", value=f"{card['url']}")
    embed.set_footer(text=f"Rarity: {rarity} - Release: {release}")
    embed.set_thumbnail(url=f"{card['images'][language]['path']}")

    return embed

async def languages(_: discord.ApplicationContext):
    """Returns the languages supported by the API"""
    return API_LANGUAGES

@bot.event
async def on_ready():
    """Actions to do when the bot is online"""
    print(f"{bot.user} is ready and online!")

@bot.slash_command(name="cardsearch", description="Search for a card")
@guild_only()
async def cardsearch(
    context: discord.ApplicationContext,
    query: discord.Option(str),
    language: discord.Option(str,
                             autocomplete=discord.utils.basic_autocomplete(languages),
                             default=API_LANGUAGES[0])
    ):
    """Searches for a card given its language"""
    try:
        url = os.getenv('API_ENDPOINT')
        response = requests.get(f"{url}/cards", params={'name': query}, timeout=10)
        response.raise_for_status()
        answer = process_response(response.json(), language)
        if answer is str:
            await context.respond(content=answer)
        if answer is discord.Embed:
            await context.respond(embed=answer)
    except HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")

bot.run(os.getenv('TOKEN')) # run the bot with the token
