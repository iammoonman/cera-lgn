import io
import json
import discord
from discord.ext import commands
import pickle
from webimporter import cubecobra
from webimporter import mtgadrafttk
from io import BytesIO

with open("guild.pickle", "rb") as f:
    guild = pickle.load(f)


class Flamewave(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(guild_ids=[guild], description="Query CubeCubra for a cube.")
    @discord.default_permissions(manage_roles=True)
    @discord.option(name="cc_id", description="CubeCobra ID.")
    @discord.option(name="len_p", description="Size of the packs.", min=1, max=150, default=15)
    async def cc_cube(self, ctx: discord.ApplicationContext, cc_id: str, len_p: int):
        await ctx.defer(ephemeral=True)
        try:
            raw = cubecobra.get_cube(cc_id, len_p)
        except:
            return await ctx.respond(
                "Something went wrong. You may have entered an invalid CubeCobra ID. Otherwise, contact Moon.",
                ephemeral=True,
            )
        cube = discord.File(io.StringIO(json.dumps(raw)), filename=f"{cc_id}_{self.getSeqID()}.json")
        await ctx.respond(content=f"Here is your cube with id {cc_id}.", file=cube, ephemeral=True)

    @commands.slash_command(guild_ids=[guild], description="Query CubeCobra for a cube and get a P1P1.")
    @discord.default_permissions(manage_roles=True)
    @discord.option(name="cc_id", description="CubeCobra ID.")
    @discord.option(name="seed", description="Seed for the pack, if you have one.", default="0")
    async def cc_p1p1(self, ctx: discord.ApplicationContext, cc_id: str, seed: str):
        await ctx.defer()
        try:
            uri, new_seed = cubecobra.get_cube_p1p1(cc_id, seed)
        except:
            return await ctx.respond(
                "Something went wrong. You may have entered an invalid CubeCobra ID. Otherwise, contact Moon.",
            )
        return await ctx.respond(content=uri)
    
    @commands.slash_command(guild_ids=[guild], description="Get the TTS cards out of MTGADraft.tk")
    @discord.default_permissions(manage_roles=True)
    @discord.option(name="file", description="The DraftLog file.", type=discord.Attachment)
    async def tk_log(self, ctx: discord.ApplicationContext, file: discord.Attachment):
        await ctx.defer()
        f = BytesIO(await file.read())
        f2 = mtgadrafttk.create_mtgadrafttk(f)
        return


def setup(bot):
    bot.add_cog(Flamewave(bot))
