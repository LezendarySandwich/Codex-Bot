import asyncio
import logging
import os
from util import constants

from discord.ext import commands

root_logger = logging.getLogger()
logger = logging.getLogger(__name__)

'''
Set Handler for root logger to direct log messages to discord channel
'''


class Logging(commands.Cog, logging.Handler):
    def __init__(self, bot, channel_id):
        logging.Handler.__init__(self)
        self.bot = bot
        self.channel_id = channel_id
        self.queue = asyncio.Queue()
        self.task = None
        self.logger = logging.getLogger(self.__class__.__name__)

    @commands.Cog.listener()
    async def on_ready(self):
        self.task = asyncio.create_task(self._log_task())
        width = 79
        stars = f'`{"*" * width}`'
        msg = f'`***{"Bot running":^{width - 6}}***`'
        self.logger.log(level=100, msg=stars)
        self.logger.log(level=100, msg=msg)
        self.logger.log(level=100, msg=stars)

    async def _log_task(self):
        while True:
            record = await self.queue.get()
            channel = self.bot.get_channel(self.channel_id)
            if channel is None:
                # Channel no longer exists.
                root_logger.removeHandler(self)
                self.logger.warning(
                    'Logging channel not available,'
                    'disabling Discord log handler.')
                break
            try:
                msg = self.format(record)
                await channel.send(msg)
            except BaseException:
                self.handleError(record)

    # logging.Handler overrides below.

    def emit(self, record):
        self.queue.put_nowait(record)

    def close(self):
        if self.task:
            self.task.cancel()


def setup(bot):
    if constants.LOGGING_COG_CHANNEL_ID is None:
        logger.info(
            'Skipping installation of logging cog'
            'as logging channel is not provided.')
        return

    logging_cog = Logging(bot, constants.LOGGING_COG_CHANNEL_ID)
    logging_cog.setLevel(logging.WARN)
    logging_cog.setFormatter(
        logging.Formatter(
            fmt='{asctime}:{levelname}:{name}:{message}',
            style='{',
            datefmt='%d-%m-%Y %H:%M:%S'))
    root_logger.addHandler(logging_cog)
    bot.add_cog(logging_cog)
