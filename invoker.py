import os
import discord
import stonewood.sw_glintwing

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
    if 'sw_starlight' not in bot.extensions:
        bot.load_extension("stonewood.sw_starlight")
        print("Starlight invoked")
    if 'sw_glintwing' not in bot.extensions:
        stonewood.sw_glintwing.get_tags()
        bot.load_extension("stonewood.sw_glintwing")
        print("Glintwing invoked")
    if 'sw_stonewood' not in bot.extensions:
        bot.load_extension("stonewood.sw_stonewood")
        print("Stonewood invoked")
    if 'sw_flamewave' not in bot.extensions:
        bot.load_extension("stonewood.sw_flamewave")
        print("Flamewave invoked")
    print("Syncing commands...")
    await bot.sync_commands()
    print("Commands synced.")


bot.run(os.environ['token'])
