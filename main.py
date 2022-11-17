import json
import logging
import os
from pathlib import Path

import discord
from discord.ext import commands
from dotenv import load_dotenv

import util

load_dotenv()

SETTINGS_PATH = os.path.join(Path().absolute(), "settings/")
DEFAULT_PREFIX = "?"


async def get_prefix_for(guild):
    path = os.path.join(SETTINGS_PATH, f"guilds/{guild}.json")
    if not os.path.isfile(path):
        await util.save_setting(guild, "prefix", DEFAULT_PREFIX)

    with open(path) as f:
        return json.load(f)["prefix"]


async def get_prefix(bot, message):
    prefix = DEFAULT_PREFIX
    bot.current_guild = message.guild.id
    current_prefix = await get_prefix_for(bot.current_guild)

    if current_prefix is not None and current_prefix != DEFAULT_PREFIX:
        prefix = current_prefix

    # Allows us to @mention the bot or use the prefix
    return commands.when_mentioned_or(prefix)(bot, message)

handler = logging.FileHandler(
    filename="discord.log", encoding="utf-8", mode="w")

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix=get_prefix,
                   intents=intents, log_handler=handler)

modules = [
    "cogs.admin",
    "cogs.hero",
    "cogs.user",
    "cogs.artifact",
    "cogs.events"
]


@bot.event
async def on_ready():
    print(f'Successfully logged in as {bot.user.name} : {bot.user.id}!')

    print(f'Setting presence...', end='')
    await bot.change_presence(activity=discord.Game('Call of Dragons'))
    print('done!')

    print(f"Loading Hero information...", end="")
    err_count = 0
    hero_count = 0

    for file_name in [x[0] for x in os.walk(".\\hero_data")]:
        hero_name = file_name.split("\\")[2]

        with open(os.path.join(Path().absolute(), "hero_data", hero_name, "info.json")) as f:
            try:
                json.load(f)
                hero_count += 1
            except ValueError as e:
                err_count += 1
                print(f"JSON parse error in {hero_name} : {e}")

    print(f"done! Heroes loaded: {hero_count}. Errors found: {err_count}.")


bot.run(os.environ.get("bot_token"))
