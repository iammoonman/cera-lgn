import io
import json
import discord
from discord.ext import commands
import pickle
from webimporter import cubecobra

with open("guild.pickle", "rb") as f:
    guild = pickle.load(f)


class Flamewave(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(guild_ids=[guild], description="Query CubeCubra for a cube.")
    @discord.default_permissions(manage_roles=True)
    @discord.option(name="cc_id", description="CubeCobra ID.")
    @discord.option(name="len_p", description="Size of the packs.", min=1, max=150, default=15)
    async def cube(self, ctx: discord.ApplicationContext, cc_id: str, len_p: int):
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


def setup(bot):
    bot.add_cog(Flamewave(bot))
