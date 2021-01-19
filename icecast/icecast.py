import aiohttp
import discord
import lavalink
import struct
import re
import json
from redbot.core import commands


class IceCast(commands.Cog):
    """icecast stream reader."""

    async def red_delete_data_for_user(self, **kwargs):
        """ Nothing to delete """
        return

    def __init__(self, bot):
        self.bot = bot
        self.session = aiohttp.ClientSession()

    async def _icecast(self, url: str):
        try:
            async with self.session.get(url) as resp:
                json = json.loads(resp)
                streams = json['icecasts']['source']
                for s in streams:
                    if s['listenurl'] == 'http://pantelwolf.info:12345/fisherman' && s['bitrate']:
                        title = s['title']
                        listeners = s['listeners']
                        return title, listeners

        except (KeyError, aiohttp.client_exceptions.ClientConnectionError):
            return None, None

    def cog_unload(self):
        self.bot.loop.create_task(self.session.close())

    @commands.guild_only()
    @commands.command(aliases=["icynp"])
    async def icecast(self, ctx, url=None):
        """Show Icecast stream information, if any."""
        if not url:
          url = 'https://radio.pantelwolf.info:12345/status-json.xsl'
        icy = await self._icecast(url)
        if not icy[0]:
            return await ctx.send(
                f"Can't read the stream information for <{player.current.uri if not url else url}>, it may not be an Icecast radio station or there may be no stream information available."
            )
        song = f"**[{icy[0]}]({url})**\n"
        embed = discord.Embed(colour=await ctx.embed_colour(), title="Now Playing", description=song)
        await ctx.send(embed=embed)
