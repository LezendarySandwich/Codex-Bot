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
                problems = await cf.get_latest_submissions(member.nick or member.name)
                for problem in problems:
                    await self.channel.send(embed=await dm.embed_code_stalk(problem=problem))
            # sleep to schedule the logging messages
            await asyncio.sleep(2)

    @commands.group(brief='Commands for subscribing/unsubscribing to the services of the bot',
                    invoke_without_command=True)
    async def stalk(self, ctx):
        """Subscribe/Unsubscribe to the services of this bot to stalk you (lol)"""
        await ctx.send_help(ctx.command)

    @stalk.command(brief="Unsubscribe from the stalking services of the bot")
    async def off(self, ctx):
        pass
    
    @stalk.command(brief="Re/Subscribe to the stalking services of the bot")
    async def on(self, ctx):
        pass

    @commands.Cog.listener()
    async def on_ready(self):
        self.guild = discord.utils.get(self.bot.guilds, name=constants.GUILD)
        self.channel = self.bot.get_channel(constants.DISCORD_BOT_CHANNEL_ID)
        if not self.channel:
            logger.critical("Code-Stalk channel not set")
        else:
            logger.info(
                f'{self.bot.user} connected to server {self.guild.name}!')
            task = asyncio.create_task(self.check_submissions())


def setup(bot):
    bot.add_cog(code_stalk(bot))
