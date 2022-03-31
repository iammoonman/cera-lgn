import pickle
import discord
import re
import json


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


intents = discord.Intents.default()
intents.members = True
bot = discord.Client(intents=intents)


@bot.event
async def on_ready():
    print("Logged in as")
    print(bot.user.name)
    print(bot.user.id)
    print("------")


@bot.event
async def on_message(message):
    if message.author.id == bot.user.id:
        return
    if message.content.startswith("$"):
        if message.content.startswith("$list"):
            list = "aer afr akh bbd bfz bng dgm dka dom dtk eld ema emn frf grn gtc hou iko jou khm kld ktk m14 m15 m19 m20 m21 mh1 mh2 mid mir neo ogw ori rix rna roe rtr soi stx ths uds vis vow war xln znr"
            return await message.channel.send(list)
        elif message.content.startswith("$pack"):
            # $pack setcode number_optional_else_1
            # DMs the packs to that player
            # Do testing to see how many packs is the maximum
            if message.author.dm_channel == None:
                dmchann = await message.author.create_dm()
            else:
                dmchann = message.author.dm_channel
            setcode = re.search("(?<=\s)\S+", message.content).group()
            anount = re.search("(?<=\s)\d+", message.content).group()
            anount = int(anount)
            if anount == 0:
                return await message.channel.send(
                    "I can't give you zero packs of {}.".format(setcode)
                )
            import tts_output

            try:
                raw = tts_output.get_packs(setcode, anount)
            except:
                return await message.channel.send(
                    "Something went wrong. The set you're trying to spawn may not be supported."
                )
            with open("packs.json", "w") as f:
                json.dump(raw, f)
            with open("packs.json", "rb") as f:
                save = discord.File(
                    f, filename="{}packs{}.json".format(setcode, getSeqID())
                )
                await dmchann.send(
                    "Here are your {} packs of {}.".format(anount, setcode), file=save
                )
            return


with open("token.pickle", "rb") as f:
    token = pickle.load(f)
bot.run(token)
