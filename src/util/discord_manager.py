import discord
import logging
from datetime import datetime
from . import constants

logger = logging.getLogger(__name__)


def embed_code_stalk(problem):
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
