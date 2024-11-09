# Future-Invaders-Bot

## How to use

The only command it supports now is `/cardsearch` followed by the card you’re looking for. It will use the [Future Invaders API](https://futureinvaders.com/api/doc/intro) to search for the card, and it will return the first result.

You can also ask for it to return the card in a given language, french or english by using respectively "fr" or "en" in the `language` field.
If no language is specified, english is default.

Funnily enough, if you’re query contains the english name of the card but ask for the french version, it will, as expected, return the french version.

## Setting up the bot Discord-wise

1. Create an application on the [Discord developer portal](https://discord.com/developers/applications)
2. Take note of the `CLIENT ID` in the *OAuth2* tab
3. Take note and **KEEP SECRET** the `Token` in the *Bot* tab
4. Rename `.env.template` to `.env`
5. Copy your **SECRET** `Token` in the `TOKEN` field of the `.env` file
6. Invite the bot to a server using this link: `https://discordapp.com/oauth2/authorize?client_id=CLIENTID&scope=bot`, replacing `CLIENTID` by the `CLIENT ID` you took note

## Setting up the bot Python-wise

1. Create a virtual environment with `python -m venv .` (it will create it in the current folder)
2. Activate it (depending on your OS, for UNIX systems, it should be `source bin/activate`)
3. Install the required python modules with `pip install -r requirements.txt`
4. Run the bot with `python main.py`