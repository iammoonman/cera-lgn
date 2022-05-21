import json
import discord
import pickle
import tts_output
import io

with open("token.pickle", "rb") as f:
    token = pickle.load(f)

with open("guild.pickle", "rb") as f:
    guild = pickle.load(f)

bot = discord.Bot()


@bot.event
async def on_ready():
    print("Logged in as")
    print(bot.user.name)
    print(bot.user.id)
    print("------")


set_choices = [
    ["Fifth Edition", "5ed"],
    ["Aether Revolt", "aer"],
    ["Adventures in the Forgotten Realms", "afr"],
    ["Amonkhet", "akh"],
    ["Battlebond", "bbd"],
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
    ["Strixhaven: School of Mages", "stx"],
    ["Theros Beyond Death", "thb"],
    ["Theros", "ths"],
    ["Urza's Destiny", "uds"],
    ["Visions", "vis"],
    ["Crimson Vow", "vow"],
    ["War of the Spark", "war"],
    ["Ixalan", "xln"],
    ["Zendikar Rising", "znr"],
]


async def get_sets(ctx: discord.AutocompleteContext):
    return [
        discord.OptionChoice(s[0], s[1])
        for s in set_choices
        if ctx.value.lower() in s[0].lower()
    ][:20]


@bot.slash_command(guild_ids=[guild])
@discord.default_permissions(manage_roles=True, description="Create packs.")
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
    max_value=48,
    default=36,
    type=int,
)
@discord.option(
    name="lands",
    description="Include a basic land pack from this set?",
    type=bool,
    default=False,
)
async def pack(ctx: discord.ApplicationContext, set: str, num: int, lands: bool):
    await ctx.defer(ephemeral=True)
    raw = tts_output.get_packs(set, num, lands)
    packs = discord.File(
        io.StringIO(json.dumps(raw)), filename=f"{set}_{getSeqID()}.json"
    )
    await ctx.respond(
        content=f"Here are your {num} packs of {set}", file=packs, ephemeral=True
    )


@bot.slash_command(guild_ids=[guild], description="Query CubeCubra for a cube.")
@discord.default_permissions(manage_roles=True)
@discord.option(name="cc_id", description="CubeCobra ID.")
async def cube(ctx: discord.ApplicationContext, cc_id: str):
    await ctx.defer(ephemeral=True)
    try:
        raw = tts_output.get_cube(cc_id)
    except:
        return await ctx.respond("Something went wrong. Contact Moon.", ephemeral=True)
    cube = discord.File(
        io.StringIO(json.dumps(raw)), filename=f"{cc_id}_{getSeqID()}.json"
    )
    await ctx.respond(
        content=f"Here is your cube with id {cc_id}.", file=cube, ephemeral=True
    )


def getSeqID():
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


bot.run(token)
