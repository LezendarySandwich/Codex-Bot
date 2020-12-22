import asyncio
import discord
from discord.ext import commands
import logging
import pymongo
from util import constants as constant
from util import codeforces_manager as cf
from util import discord_manager as dm

logger = logging.getLogger(__name__)

class code_stalk(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
    
    async def check_submissions(self):
        while True:
            for member in self.guild.members:
                problems = await cf.get_latest_submissions(member.nick or member.name, self.collection)
                for problem in problems:
                    await self.channel.send(embed=dm.embed_code_stalk(problem=problem))

    @commands.Cog.listener()
    async def on_ready(self):
        self.guild = discord.utils.get(self.bot.guilds, name=constant.GUILD)
        self.channel = discord.utils.get(self.guild.channels, name=constant.DISCORD_BOT_CHANNEL_NAME)
        self.client = pymongo.MongoClient(constant.MONOGODB_URI)
        self.collection = self.client["CodeStalker"]["Users"]
        if not self.channel:
            logger.critical("Code-Stalk channel not set")
        else:
            logger.info(f'{self.bot.user} connected to server {self.guild.name}!')
            task = asyncio.create_task(self.check_submissions())
            await task


def setup(bot):
    bot.add_cog(code_stalk(bot))