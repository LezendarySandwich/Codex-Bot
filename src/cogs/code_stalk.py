import asyncio
import discord
from discord.ext import commands
import logging
from util import constants
from util import codeforces_manager as cf
from util import discord_manager as dm
from util import database_manager as db

logger = logging.getLogger(__name__)


class code_stalk(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    async def check_submissions(self):
        while True:
            members = await self.guild.fetch_members(limit=None).flatten()
            for member in members:
                handle = member.nick or member.name
                subbed = await db.stalk_sub_check(handle)
                if not subbed: 
                    logger.info(f'handle:{handle} Not subbed')
                    continue
                problems = await cf.get_latest_submissions(handle)
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
        '''
        User.display_name, which will try to to use the users server-specific nickname, but will fall back to the general username if that is not found
        '''
        handle = ctx.message.author.display_name
        await db.stalk_sub_update(handle, False)
        await ctx.channel.send(f'Switching off the services for {handle}')
    
    @stalk.command(brief="Re/Subscribe to the stalking services of the bot")
    async def on(self, ctx):
        handle = ctx.message.author.display_name
        await db.stalk_sub_update(handle, True)
        await ctx.channel.send(f'Switching on the services for {handle}')

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
    logger.setLevel(logging.INFO)
    bot.add_cog(code_stalk(bot))
