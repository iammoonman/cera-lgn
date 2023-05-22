import discord
import pickle

with open("token.pickle", "rb") as f:
    token = pickle.load(f)

intents = discord.Intents.default()
intents.members = True

bot = discord.Bot(intents=intents)


@bot.event
async def on_ready():
    print("Logged in as")
    print(bot.user.name)
    print(bot.user.id)
    print("-------")
    print("Loading cogs:")
    bot.load_extension("stonewood.starlight")
    print("Starlight invoked")
    bot.load_extension("stonewood.glintwing")
    print("Glintwing invoked")
    bot.load_extension("stonewood.stonewood")
    print("Stonewood invoked")
    bot.load_extension("stonewood.flamewave")
    print("Flamewave invoked")
    print("Syncing commands...")
    await bot.sync_commands()
    print("Commands synced.")


bot.run(token)
