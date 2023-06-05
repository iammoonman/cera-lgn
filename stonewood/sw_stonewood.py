from discord.ext import commands
import pickle


with open("guild.pickle", "rb") as f:
    guild = pickle.load(f)


class Stonewood(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


def setup(bot):
    bot.add_cog(Stonewood(bot))
