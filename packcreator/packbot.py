import json
import interactions
import pickle

# import interactions.ext.enhanced
import io

with open("token.pickle", "rb") as f:
    token = pickle.load(f)

bot = interactions.Client(token=token)
# bot.load("interactions.ext.enhanced")

with open("guild.pickle", "rb") as f:
    guild = pickle.load(f)


@bot.event
async def on_ready():
    print("Logged in as")
    # print(bot.user.name)
    # print(bot.user.id)
    print("------")
    # for c in await bot._http.get_application_commands(bot.me.id):
    #     await bot._http.delete_application_command(bot.me.id,c['id'])


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


@bot.command(
    name="pack",
    description="Create packs from the set of your choice.",
    options=[
        interactions.Option(
            name="set",
            description="Should be obvious.",
            type=interactions.OptionType.STRING,
            required=True,
            autocomplete=True,
        ),
        interactions.Option(
            name="number",
            description="How many packs you want.",
            type=interactions.OptionType.INTEGER,
            required=True,
            min_value=1,
            max_value=72,
        ),
        interactions.Option(
            name="lands",
            description="Include a land pack?",
            type=interactions.OptionType.STRING,
            required=False,
            choices=[
                interactions.Choice(name="Yes", value="Y"),
                interactions.Choice(name="No", value="N"),
            ],
        ),
    ],
    scope=guild,
)
async def create_pack(
    ctx: interactions.CommandContext, set: str, number: int, lands: str = "N"
):
    import tts_output

    await ctx.defer()

    raw = tts_output.get_packs(set, number, lands == "Y")
    packs = io.StringIO(json.dumps(raw))
    m = await ctx.send(
        content=f"Here are your {number} packs of {set}.",
        # files=[
        #     interactions.File(filename=f"{number}_of_{set}_{getSeqID()}.json", fp=packs)
        # ],  # Put the number back on the end
        # ephemeral=True,
    )
    await m.edit(
        files=[
            interactions.File(filename=f"{number}_of_{set}_{getSeqID()}.json", fp=packs)
        ]
    )
    return


@bot.command(
    name="cube",
    description="Import a cube from CubeCobra.",
    options=[
        interactions.Option(
            name="id",
            description="The cube's Cube ID, as shown on its Overview page.",
            type=interactions.OptionType.STRING,
            required=True,
        )
    ],
    scope=guild,
)
async def create_cube(ctx: interactions.CommandContext, id: str):
    # return await ctx.send("This command isn't ready yet.")
    import tts_output

    await ctx.defer()
    raw = tts_output.get_cube(id)
    if raw is None:
        return await ctx.send("That cube could not be found.", ephemeral=True)
    packs = io.StringIO(json.dumps(raw))
    m = await ctx.send(
        content=f"Here's your cube.",
        # files=[interactions.File(filename=f"cube_{id}.json", fp=packs)],
        # ephemeral=True,
    )
    m.edit(files=[interactions.File(filename=f"cube_{id}.json", fp=packs)])
    return


@bot.autocomplete(command="pack", name="set")
async def set_autocomplete(ctx, set=""):
    set_choices.sort(key=lambda x: set.lower() in x[0].lower(), reverse=True)
    to_send = [
        interactions.Choice(name=i[0], value=i[1]) for i in set_choices
    ]
    return await ctx.populate(to_send[:25])


# @bot.command(
#     name="rule",
#     description="Reference a specific Magic rule.",
#     options=[
#         interactions.Option(
#             name="start_typing",
#             type=interactions.OptionType.STRING,
#             description="Start typing to find your rule, beginning with its rule number.",
#             required=True,
#             autocomplete=True,
#         )
#     ],
#     scope=guild,
# )
# async def post_rule(ctx: interactions.CommandContext, start_typing=""):
#     with open("rules.pickle", "rb") as f:
#         rules: list[dict] = pickle.load(f)
#     r = next((d for d in rules if d["refer"] == start_typing), "Not found.")
#     return await ctx.send(r["text"])


# @bot.autocomplete(command="rule", name="start_typing")
# async def do_autocomplete(ctx, start_typing=""):
#     # rules = [{"text":"","refer":""}]
#     with open("rules.pickle", "rb") as f:
#         rules = pickle.load(f)
#     choices = [
#         interactions.Choice(
#             name=r["text"][:80] + ("..." if len(r["text"]) > 80 else ""),
#             value=r["refer"],
#         )
#         for r in rules
#         if r["text"][: len(start_typing)] == start_typing
#     ]
#     to_send = choices[: min(len(choices), 25)]
#     return await ctx.populate(to_send)


bot.start()
