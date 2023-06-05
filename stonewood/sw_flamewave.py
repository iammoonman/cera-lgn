import io
import json
import time
import discord
from discord.ext import commands
from discord.ext.pages import Paginator, Page
import pickle
from requests.utils import quote

import requests
import flamewave
from io import BytesIO

with open("guild.pickle", "rb") as f:
    guild = pickle.load(f)


class Flamewave(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def getSeqID(self):
        try:
            with open("counter.pickle", "rb") as f:
                e = pickle.load(f)
        except:
            with open("counter.pickle", "wb") as f:
                pickle.dump(0, f)
            e = 0
        with open("counter.pickle", "wb") as f:
            pickle.dump(e + 1, f)
        return str(e + 1)

    @commands.slash_command(guild_ids=[guild], description="Query CubeCubra for a cube.")
    @discord.option(name="cc_id", description="CubeCobra ID.")
    @discord.option(name="len_p", description="Size of the packs.", min=1, max=150, default=15)
    async def cc_cube(self, ctx: discord.ApplicationContext, cc_id: str, len_p: int):
        await ctx.defer(ephemeral=True)
        try:
            raw = flamewave.cubecobra.get_cube(cc_id, len_p)
        except:
            return await ctx.respond(
                "Something went wrong. You may have entered an invalid CubeCobra ID. Otherwise, contact Moon.",
                ephemeral=True,
            )
        cube = discord.File(io.StringIO(json.dumps(raw)), filename=f"{cc_id}_{self.getSeqID()}.json")
        await ctx.respond(content=f"Here is your cube with id {cc_id}.", file=cube, ephemeral=True)

    @commands.slash_command(guild_ids=[guild], description="Query CubeCobra for a cube and get a P1P1.")
    @discord.option(name="cc_id", description="CubeCobra ID.")
    @discord.option(name="seed", description="Seed for the pack, if you have one.", default="0")
    async def cc_p1p1(self, ctx: discord.ApplicationContext, cc_id: str, seed: str):
        await ctx.defer()
        try:
            uri, new_seed = flamewave.cubecobra.get_cube_p1p1(cc_id, seed)
        except:
            return await ctx.respond(
                "Something went wrong. You may have entered an invalid CubeCobra ID. Otherwise, contact Moon.",
            )
        return await ctx.respond(content=uri)

    @commands.slash_command(guild_ids=[guild], description="Get the TTS cards out of MTGADraft.tk")
    @discord.option(name="file", description="The DraftLog file.", type=discord.Attachment)
    async def dm_log(self, ctx: discord.ApplicationContext, file: discord.Attachment):
        await ctx.defer(ephemeral=True)
        f = BytesIO(await file.read())
        f2, n = flamewave.draftmancer.full_draftmancer_log(f)
        new_file = discord.File(io.StringIO(json.dumps(f2)), filename=f"draft_{n}.json")
        await ctx.respond(file=new_file, ephemeral=True)
        return

    @commands.slash_command(guild_ids=[guild], description="Search Scryfall for cards.")
    @discord.option(name="query", description="Query for cards the same way you would on Scryfall.", type=str)
    async def scry_search(self, ctx: discord.ApplicationContext, query: str):
        await ctx.defer()
        full_json = []
        full_set_json = []
        time.sleep(0.25)
        response = requests.get(f"https://api.scryfall.com/cards/search?q={quote(query)}", headers={"UserAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:95.0) Gecko/20100101 Firefox/95.0"})
        full_json += (resjson := response.json())["data"]
        while resjson["has_more"]:
            time.sleep(0.25)
            response = requests.get(resjson["next_page"], headers={"UserAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:95.0) Gecko/20100101 Firefox/95.0"})
            full_set_json += (resjson := response.json())["data"]
        paginator = Paginator(pages=[Page(content=f'{c["scryfall_uri"][:-3]}discord') for c in full_json])
        await paginator.respond(ctx.interaction)
        return


def setup(bot):
    bot.add_cog(Flamewave(bot))
