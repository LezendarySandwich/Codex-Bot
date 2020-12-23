import discord
from discord.ext import commands
import util.constants as constant
import logging
from pathlib import Path

root_logger = logging.getLogger()

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix=commands.when_mentioned_or(
    '! '), description="Codex Discord Bot", intents=intents)

cogs = [file.stem for file in Path('src', 'cogs').glob('*.py')]

for extension in cogs:
    bot.load_extension(f'cogs.{extension}')
logging.info(f'Cogs loaded: {", ".join(bot.cogs)}')

bot.run(constant.BOT_TOKEN)