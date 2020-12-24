import discord
import logging
from datetime import datetime
from . import constants

logger = logging.getLogger(__name__)


async def embed_code_stalk(problem):
    '''
    returns an embed to send to channel for the problem
    :param problem: object of type Problem
    :rtype: discord embed
    '''
    tags = ', '.join(problem.tags)
    r_embed = discord.Embed(title=problem.handle, type="rich")
    r_embed.set_author(
        name="CodexBot",
        icon_url=constants.CODEX_ICON_URI)
    r_embed.add_field(name="Task", value=problem.problem_name)
    r_embed.add_field(name="Rating", value=problem.rating)
    r_embed.add_field(name="Tags", value=tags)
    r_embed.add_field(name="Link", value=problem.url_get())
    return r_embed

async def embed_rank_stalk(ranklist, contest_name: str):
    '''
    :param ranklist: object of tuple (member, rank) sorted by rank
    :param contest_name: str. Name of the contest
    :rtype: discord embed
    '''
    r_embed = discord.Embed(title=contest_name, type="rich")
    r_embed.set_author(
        name="CodexBot",
        icon_url=constants.CODEX_ICON_URI)
    for member, rank in ranklist:
        r_embed.add_field(name=str(rank), value=member, inline=False)
    return r_embed

async def embed_rating_stalk(rating_change):
    '''
    :param ranklist: dict of (member: (oldRating, newRating))
    :rtype: discord embed
    '''
    r_embed = discord.Embed(title='Congratulations', type='rich', colour=discord.Colour.gold())
    r_embed.set_author(
        name="CodexBot",
        icon_url=constants.CODEX_ICON_URI)
    for member, (old_rating, new_rating) in rating_change.items():
        if new_rating > old_rating:
            r_embed.add_field(name=member, value=f'{str(old_rating)} -----> {str(new_rating)}', inline=False)
    return r_embed