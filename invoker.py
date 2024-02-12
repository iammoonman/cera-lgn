import os
import discord

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
    bot.load_extension("stonewood.sw_starlight")
    print("Starlight invoked")
    bot.load_extension("stonewood.sw_glintwing")
    print("Glintwing invoked")
    bot.load_extension("stonewood.sw_stonewood")
    print("Stonewood invoked")
    bot.load_extension("stonewood.sw_flamewave")
    print("Flamewave invoked")
    print("Syncing commands...")
    await bot.sync_commands()
    print("Commands synced.")


bot.run(os.environ['token'])
