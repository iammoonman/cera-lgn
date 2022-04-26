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


set_choices = []


@bot.command(
    name="pack",
    description="Create packs from the set of your choice.",
    options=[
        interactions.Option(
            name="set",
            description="Should be obvious.",
            type=interactions.OptionType.STRING,
            required=True,
            choices=[interactions.Choice(name=i[0], value=i[1]) for i in set_choices],
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
                interactions.Choice(name="Yes", value=True),
                interactions.Choice(name="No", value=False),
            ],
        ),
    ],
)
async def create_pack(
    ctx: interactions.CommandContext, set: str, number: int, lands: bool
):
    # Attachments aren't implemented yet
    # Instead of DM, use an ephemeral message in the channel.
    m = await ctx.send("hello")
    await m.edit(files=[interactions.File("packs.json")])
    return


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
async def post_rule(ctx: interactions.CommandContext, rule=""):
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
