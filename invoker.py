import discord
import pickle

with open("token.pickle", "rb") as f:
    token = pickle.load(f)

bot = discord.Bot()


@bot.event
async def on_ready():
    print("Logged in as")
    print(bot.user.name)
    print(bot.user.id)
    print("-------")
    print("Loading cogs:")
    bot.load_extension("packcreator.starlight")
    print("Starlight invoked")
    bot.load_extension("drafthandler.glintwing")
    print("Glintwing invoked")
    bot.load_extension("cardgetter.smokespew")
    print("Smokespew invoked")
    bot.load_extension("webimporter.flamewave")
    print("Flamewave invoked")
    print("Syncing commands...")
    await bot.sync_commands()
    print("Commands synced.")


bot.run(token)
