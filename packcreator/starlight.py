import json
import discord
import pickle
from . import p_caller
import io
from discord.ext import commands

set_choices = [
    ["Fifth Edition", "5ed"],
    ["Aether Revolt", "aer"],
    ["Adventures in the Forgotten Realms", "afr"],
    ["Amonkhet", "akh"],
    ["Battle for Zendikar", "bfz"],
    ["Born of the Gods", "bng"],
    ["Dragon's Maze", "dgm"],
    ["Dark Ascension", "dka"],
    ["Dominaria", "dom"],
    ["Dragons of Tarkir", "dtk"],
    ["Throne of Eldraine", "eld"],
    ["Eternal Masters", "ema"],
    ["Eldrich Moon", "emn"],
    ["Fate Reforged", "frf"],
    ["FUN", "fun"],
    ["Guilds of Ravnica", "grn"],
    ["Gatecrash", "gtc"],
    ["Hour of Devastation", "hou"],
    ["Ikoria: Lair of Behemoths", "iko"],
    ["Journey into Nyx", "jou"],
    ["Kaldheim", "khm"],
    ["Kaladesh", "kld"],
    ["Khans of Tarkir", "ktk"],
    ["Magic 2014", "m14"],
    ["Magic 2015", "m15"],
    ["Core Set 2019", "m19"],
    ["Core Set 2020", "m20"],
    ["Core Set 2021", "m21"],
    ["Modern Horizons 1", "mh1"],
    ["Modern Horizons 2", "mh2"],
    ["Modern Masters", "mma"],
    ["Midnight Hunt", "mid"],
    ["Mirage", "mir"],
    ["Kamigawa: Neon Dynasty", "neo"],
    ["Oath of the Gatewatch", "ogw"],
    ["Magic Origins", "ori"],
    ["Rivals of Ixalan", "rix"],
    ["Ravnica Allegaince", "rna"],
    ["Rise of the Eldrazi", "roe"],
    ["Return to Ravnica", "rtr"],
    ["Shadows over Innistrad", "soi"],
    ["Streets of New Capenna", "snc"],
    ["Strixhaven: School of Mages", "stx"],
    ["Stronghold", "sth"],
    ["Tempest", "tmp"],
    ["Theros Beyond Death", "thb"],
    ["Theros", "ths"],
    ["Urza's Destiny", "uds"],
    ["Visions", "vis"],
    ["Crimson Vow", "vow"],
    ["War of the Spark", "war"],
    ["Weatherlight", "wth"],
    ["Ixalan", "xln"],
    ["Zendikar Rising", "znr"],
]

set_choices_v3 = [["Adventures in the Forgotten Realms", "afr"], ["Pauper Masters", "ppm"]]


with open("guild.pickle", "rb") as f:
    guild = pickle.load(f)


class Starlight(commands.Cog):
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

    async def get_sets(ctx: discord.AutocompleteContext):
        return [discord.OptionChoice(s[0], s[1]) for s in set_choices if ctx.value.lower() in s[0].lower()][:20]

    @commands.slash_command(guild_ids=[guild], description="Create packs.")
    @discord.default_permissions(manage_roles=True)
    @discord.option(
        name="set",
        description="Choose the set.",
        options=[discord.OptionChoice(s[0], s[1]) for s in set_choices][:10],
        autocomplete=get_sets,
        type=str,
    )
    @discord.option(
        name="num",
        description="Number of packs.",
        min_value=1,
        max_value=72,
        default=36,
        type=int,
    )
    @discord.option(
        name="lands",
        description="Include a basic land pack from this set?",
        type=bool,
        default=False,
    )
    async def pack(self, ctx: discord.ApplicationContext, set: str, num: int, lands: bool):
        await ctx.defer(ephemeral=True)
        try:
            raw = p_caller.get_packs(set, num, lands)
        except:
            return await ctx.respond("Something went wrong. Be sure to click the autocomplete options instead of typing out the name of the set. Otherwise, contact Moon.", ephemeral=True)
        packs = discord.File(io.StringIO(json.dumps(raw)), filename=f"{set}_{self.getSeqID()}.json")
        await ctx.respond(content=f"Here are your {num} packs of {set}", file=packs, ephemeral=True)

    @commands.slash_command(guild_ids=[guild], description="Query CubeCubra for a cube.")
    @discord.default_permissions(manage_roles=True)
    @discord.option(name="cc_id", description="CubeCobra ID.")
    async def cube(self, ctx: discord.ApplicationContext, cc_id: str):
        await ctx.defer(ephemeral=True)
        #try:
        raw = p_caller.get_cube(cc_id)
        #except:
            #return await ctx.respond("Something went wrong. You may have entered an invalid CubeCobra ID. Otherwise, contact Moon.", ephemeral=True)
        cube = discord.File(io.StringIO(json.dumps(raw)), filename=f"{cc_id}_{self.getSeqID()}.json")
        await ctx.respond(content=f"Here is your cube with id {cc_id}.", file=cube, ephemeral=True)

    async def get_sets_v3(ctx: discord.AutocompleteContext):
        return [discord.OptionChoice(s[0], s[1]) for s in set_choices_v3 if ctx.value.lower() in s[0].lower()][:20]

    @commands.slash_command(guild_ids=[guild], description="Create packs.")
    @discord.default_permissions(manage_roles=True)
    @discord.option(
        name="set",
        description="Choose the set.",
        options=[discord.OptionChoice(s[0], s[1]) for s in set_choices_v3][:10],
        autocomplete=get_sets_v3,
        type=str,
    )
    @discord.option(
        name="num",
        description="Number of packs.",
        min_value=1,
        max_value=72,
        default=36,
        type=int,
    )
    @discord.option(
        name="lands",
        description="Include a basic land pack from this set?",
        type=bool,
        default=False,
    )
    async def pack_v3(self, ctx: discord.ApplicationContext, set: str, num: int, lands: bool):
        await ctx.defer(ephemeral=True)
        try:
            raw = p_caller.get_packs_v3(set, num, lands)
        except:
            return await ctx.respond("Something went wrong. Be sure to click the autocomplete options instead of typing out the name of the set. Otherwise, contact Moon.", ephemeral=True)
        packs = discord.File(io.StringIO(json.dumps(raw)), filename=f"{set}_{self.getSeqID()}.json")
        await ctx.respond(content=f"Here are your {num} packs of {set}", file=packs, ephemeral=True)


def setup(bot):
    bot.add_cog(Starlight(bot))
