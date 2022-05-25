
import discord
import pickle

with open('token.pickle', 'rb') as f:
    token = pickle.load(f)

bot = discord.Bot()

@bot.event
async def on_ready():
    print("Logged in as")
    print(bot.user.name)
    print(bot.user.id)
    print('-------')
    print('Loading cogs:')
    bot.load_extension('packcreator.starlight.py')
    print('Starlight invoked')
    bot.load_extension('drafthandler.glintwing.py')
    print('Glintwing invoked')

bot.run(token)