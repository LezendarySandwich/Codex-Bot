import asyncio
import discord
from discord.ext import commands
import logging
from util import constants
from util import codeforces_manager as cf
from util import discord_manager as dm

logger = logging.getLogger(__name__)


class code_stalk(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    async def check_submissions(self):
        while True:
            members = await self.guild.fetch_members(limit=None).flatten()
            for member in members:
                print(member.name, member.nick)
                problems = await cf.get_latest_submissions(member.nick or member.name)
                for problem in problems:
                    await self.channel.send(embed=dm.embed_code_stalk(problem=problem))
            # sleep to schedule the logging messages
            await asyncio.sleep(2)

    @commands.Cog.listener()
    async def on_ready(self):
        self.guild = discord.utils.get(self.bot.guilds, name=constants.GUILD)
        self.channel = discord.utils.get(
            self.guild.channels,
            name=constants.DISCORD_BOT_CHANNEL_NAME)
        if not self.channel:
            logger.critical("Code-Stalk channel not set")
        else:
            logger.info(
                f'{self.bot.user} connected to server {self.guild.name}!')
            task = asyncio.create_task(self.check_submissions())


def setup(bot):
    bot.add_cog(code_stalk(bot))
