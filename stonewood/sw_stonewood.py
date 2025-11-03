import random
import discord
from discord.ext import commands
import requests


class Stonewood(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="plus-one", description="Use with the I am Moonslice card.")
    async def one(self, ctx: discord.ApplicationContext):
        return await ctx.respond(content=random.choice(["Draw a card. Scry 1.", "Untap a land.", "Create a 1/1 colorless Servo artifact creature token.", "Exile the top two cards of your library. You may play one of those cards this turn.", "Use the /v3_p1p1 command on CERA with a set argument of your choice. An opponent chooses a card from that pack. Conjure a copy of that card into your hand.", "Put a prowess counter on target creature.", "Use the /minus-three command on CERA. *(I am Moonslice doesn't lose loyalty counters from this.)*"]))

    @commands.slash_command(name="minus-three", description="Use with the I am Moonslice card.")
    async def three(self, ctx: discord.ApplicationContext):
        return await ctx.respond(content=random.choice(["Proliferate twice.", "Destroy up to one target nonbasic land.", "Choose a nonlegendary Angel token from Scryfall and create that token.", "Remove all counters from all permanents other than I am Moonslice.", "You become the monarch and it becomes day. Untap three lands.", "Each player sacrifices a creature. If you sacrificed a creature this way, draw a card.", "Conjure a copy of a card Omni most recently referenced in a post into your hand.", "Use the /minus-seven command on CERA. *(I am Moonslice doesn't lose loyalty counters from this.)*"]))

    @commands.slash_command(name="minus-seven", description="Use with the I am Moonslice card.")
    async def seven(self, ctx: discord.ApplicationContext):
        return await ctx.respond(content=random.choice(["Destroy up to two target permanents with a prime mana value.", "Visit https://lp-cards-viewer.vercel.app/custom-cards/rzp and choose a land or spell card. Conjure a copy of that card into exile, and you may play that card this turn. If you cast a spell this way, you may cast it without paying its mana cost.", "If this is the first game of the match, then at the beginning of the third game this match, you win the game. *(If this match doesn't have a third game, nothing happens.)*", 'You get an emblem with "Spells you cast have delve," and "Nonland cards in your graveyard have dredge 4."']))

    @commands.slash_command(name="scryfall-update", description="Updates the bulk data used by the application.")
    async def update(self, ctx: discord.ApplicationContext):
        await ctx.respond(content="Updating! Please wait a few moments before issuing another command.", ephemeral=True)
        resp = requests.get("https://api.scryfall.com/bulk-data")
        body = resp.json()
        download_uri = None
        for direction in body['data']:
            if direction['type'] == 'default_cards':
                download_uri = direction['download_uri']
        if download_uri is None:
            return await ctx.send(content="Updating default_cards failed. Contact Moon.")
        deep_resp = requests.get(download_uri)
        with open("default-cards.json", "wb") as fd:
            for chunk in deep_resp.iter_content(chunk_size=128):
                fd.write(chunk)


def setup(bot):
    bot.add_cog(Stonewood(bot))
