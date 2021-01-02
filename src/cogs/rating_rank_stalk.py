import asyncio
import discord
from discord.ext import commands
import logging
import time
from util import constants
from util import codeforces_manager as cf
from util import discord_manager as dm
from util import database_manager as db

logger = logging.getLogger(__name__)

class rating_rank_stalk(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    async def contest_new(self):
        logger.warn('Checking Contests')
        for i in range(2):
            members = await self.guild.fetch_members(limit=None).flatten()
            contest_name, contest_id = None, None
            rating_change, rank_members = dict(), list()
            # rank_members = list(member, rank)
            for member in members:
                contest = await cf.latest_get_contest(member.nick or member.name)
                if contest is None or time.time() - contest['ratingUpdateTimeSeconds'] > 100000: continue
                checked = await db.contest_check(contest['contestId'])
                if checked: continue
                if contest_name is None: 
                    contest_name = contest['contestName']
                    contest_id = contest['contestId']
                if contest_id is not contest['contestId']: continue
                rating_change[member.nick or member.name] = (contest['oldRating'], contest['newRating'])
                rank_members.append((member.nick or member.name, contest['rank']))
            logger.warn(f'contenst name: {contest_name}, contest id: {contest_id}')
            if contest_name:
                # sort according to ranks
                rank_members.sort(key=lambda x: x[1])
                await self.channel.send(embed=await dm.embed_rank_stalk(ranklist=rank_members, contest_name=contest_name))
                await self.channel.send(embed=await dm.embed_rating_stalk(rating_change=rating_change))
                await db.insert_contest(contestId=contest_id)

    async def do_every(self, period, f, *args):
        def g_tick():
            t = time.time()
            while True:
                t += period
                yield max(t - time.time(),0)
        g = g_tick()
        while True:
            await asyncio.sleep(next(g))
            await f(*args)

    @commands.Cog.listener()
    async def on_ready(self):
        self.guild = discord.utils.get(self.bot.guilds, name=constants.GUILD)
        self.channel = self.bot.get_channel(constants.HALL_OF_FAME_ID)
        if not self.channel:
            logger.critical('Hall of fame channel not set')
        else:
            logger.info('Connected to Hall Of Fame')
            await self.do_every(constants.CONTEST_CHECK, self.contest_new)

def setup(bot):
    logger.setLevel(logging.INFO)
    bot.add_cog(rating_rank_stalk(bot))