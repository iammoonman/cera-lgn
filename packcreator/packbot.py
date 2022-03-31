import json
import interactions
import pickle

with open("token.pickle", "rb") as f:
    token = pickle.load(f)

bot = interactions.Client(token=token)


@bot.event
async def on_ready():
    print("Logged in as")
    # print(bot.user.name)
    # print(bot.user.id)
    print("------")


@bot.command(name="test", description="test command")
async def test(ctx):
    print("hello world")
    await ctx.send("hello world")


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
async def create_pack(ctx, set: str, number: int, lands: bool):
    # Attachments aren't implemented yet
    # Instead of DM, use an ephemeral message in the channel.
    return


bot.start()
