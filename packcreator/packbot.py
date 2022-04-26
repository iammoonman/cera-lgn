import json
import interactions
import pickle


with open("token.pickle", "rb") as f:
    token = pickle.load(f)

bot = interactions.Client(token=token)

with open("guild.pickle", "rb") as f:
    guild = pickle.load(f)


@bot.event
async def on_ready():
    print("Logged in as")
    # print(bot.user.name)
    # print(bot.user.id)
    print("------")


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
    # Attachments aren't implemented yet
    # Instead of DM, use an ephemeral message in the channel.
    import tts_output

    raw = tts_output.get_packs(set, number, lands == "Y")
    with open("packs.json", "w") as f:
        json.dump(raw, f)
    m = await ctx.send("Creating your packs.")
    await m.edit(content="", files=[interactions.File("packs.json")])
    return


@bot.autocomplete(command="pack", name="set")
async def set_autocomplete(ctx, set="A"):
    to_send = [
        interactions.Choice(name=i[0], value=i[1])
        for i in set_choices
        if i[0][: len(set)] == set
    ]
    return await ctx.populate(to_send)


@bot.command(
    name="rule",
    description="Reference a specific Magic rule.",
    options=[
        interactions.Option(
            name="rule",
            type=interactions.OptionType.STRING,
            description="Start typing to find your rule.",
            autocomplete=True,
        )
    ],
    scope=guild,
)
async def post_rule(ctx: interactions.CommandContext, rule="1"):
    with open("rules.pickle", "rb") as f:
        rules: list[dict] = pickle.load(f)
    r = next((d for d in rules if d["refer"] == rule), "Not found.")
    return await ctx.send(r["text"])


@bot.autocomplete(command="rule", name="rule")
async def do_autocomplete(ctx, rule=""):
    # rules = [{"text":"","refer":""}]
    with open("rules.pickle", "rb") as f:
        rules = pickle.load(f)
    choices = [
        interactions.Choice(
            name=r["text"][:80] + ("..." if len(r["text"]) > 80 else ""),
            value=r["refer"],
        )
        for r in rules
        if r["text"][: len(rule)] == rule
    ]
    to_send = choices[: min(len(choices), 15)]
    return await ctx.populate(to_send)


bot.start()
