import json
import time
import discord
from discord.ext import commands
from discord.ext.pages import Paginator, Page
import pickle

import requests
from requests.utils import quote

with open("guild.pickle", "rb") as f:
    guild = pickle.load(f)


class Smokespew(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(guild_ids=[guild], description="Search Scryfall for cards.")
    @discord.option(
        name="query",
        description="Query for cards the same way you would on Scryfall.",
        type=str,
    )
    async def sc_search(self, ctx: discord.ApplicationContext, query: str):
        await ctx.defer()
        full_json = []
        time.sleep(0.25)
        response = requests.get(
            f"https://api.scryfall.com/cards/search?q={quote(query)}",
            headers={"UserAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:95.0) Gecko/20100101 Firefox/95.0"},
        )
        full_json += (resjson := response.json())["data"]
        while resjson["has_more"]:
            time.sleep(0.25)
            response = requests.get(
                resjson["next_page"],
                headers={"UserAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:95.0) Gecko/20100101 Firefox/95.0"},
            )
            full_set_json += (resjson := response.json())["data"]
        paginator = Paginator(pages=[Page(content=f'{c["scryfall_uri"][:-3]}discord') for c in full_json])
        await paginator.respond(ctx.interaction)
        return

    @commands.slash_command(guild_ids=[guild], description="Add a card to CERA's website.")
    @discord.option(name="title", description="The title of this entry. ex. 'My Favorite Card'", type=str)
    @discord.option(
        name="set",
        description="The set code of the printing for the card. ex. '2x2' for Double Masters 2022.",
        type=str,
    )
    @discord.option(name="cn", description="The collector's number for the printing of the card.", type=str)
    @discord.option(name="description", description="A description to show in the tooltip.", type=str)
    async def sw_card(self, ctx: discord.ApplicationContext, title: str, set: str, cn: str, description: str):
        newCard = {
            "id": ctx.interaction.id,
            "title": title,
            "set": set,
            "cn": cn,
            "uri": "",
            "description": description,
            "p_id": ctx.author.id,
        }
        await ctx.defer()
        full_json = []
        time.sleep(0.25)
        response = requests.get(
            f"https://api.scryfall.com/cards/search?q={quote(f'set:{set} cn:{cn}')}",
            headers={"UserAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:95.0) Gecko/20100101 Firefox/95.0"},
        )
        full_json += (resjson := response.json())
        if full_json["object"] == "error":
            return ctx.respond("That card was not found.")
        cc = full_json["data"][0]
        try:
            if cc["layout"] == "transform" or cc["layout"] == "reversible-card":
                newCard["uri"] = cc["card_faces"][0]["image_uris"]["normal"]
            else:
                newCard["uri"] = cc["image_uris"]["normal"]
        except:
            return ctx.respond("Please don't put weird cards up, the image won't work.")
        with open(f"pagessite/src/carddata/{newCard['id']}.json", "w") as f:
            json.dump(self.bot.drafts[self.id].tojson(), f, ensure_ascii=False, indent=4)
        return ctx.respond(f"A display for {cc['name']} will be added to the site under your name the next time Moon builds the site.")


def setup(bot):
    bot.add_cog(Smokespew(bot))
