import json
import time
import discord
from discord.ext import commands
from discord.ext.pages import Paginator, Page
import pickle

import requests
from requests.utils import quote

with open("guild.pickle", "rb") as f:
    guild = pickle.load(f)


class Stonewood(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(guild_ids=[guild], description="Search Scryfall for cards.")
    @discord.option(
        name="query",
        description="Query for cards the same way you would on Scryfall.",
        type=str,
    )
    async def scry_search(self, ctx: discord.ApplicationContext, query: str):
        await ctx.defer()
        full_json = []
        full_set_json = []
        time.sleep(0.25)
        response = requests.get(
            f"https://api.scryfall.com/cards/search?q={quote(query)}",
            headers={"UserAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:95.0) Gecko/20100101 Firefox/95.0"},
        )
        full_json += (resjson := response.json())["data"]
        while resjson["has_more"]:
            time.sleep(0.25)
            response = requests.get(
                resjson["next_page"],
                headers={"UserAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:95.0) Gecko/20100101 Firefox/95.0"},
            )
            full_set_json += (resjson := response.json())["data"]
        paginator = Paginator(pages=[Page(content=f'{c["scryfall_uri"][:-3]}discord') for c in full_json])
        await paginator.respond(ctx.interaction)
        return


def setup(bot):
    bot.add_cog(Stonewood(bot))
