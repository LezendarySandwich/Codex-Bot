import asyncio
import discord
from discord.ext import commands
import logging
from timeloop import Timeloop
from util import constants
from util import codeforces_manager as cf

tl = Timeloop()

class rating_rank_stalk(commangs.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        