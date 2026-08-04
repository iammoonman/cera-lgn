import random
import discord
from discord.ext import commands
import requests
from stonewood import logger
import gzip
from flamewave import s3_has_object, upload_to_s3, strip_uri, to_grid
import io
import time
import json
import typing
import asyncio
import functools
import threading


def threaded_decorator(function):
    def inner_function(*args):
        function_thread = threading.Thread(target=function, args=args)
        function_thread.start()

    return inner_function


@threaded_decorator
def blocking_func():
    f = open("default-cards.jsonl", "r", encoding="utf8")
    i = 0
    for j in f:
        did_upload = False
        card = json.loads(j)
        if card["oversized"] or card["lang"] not in ["en", "ph", "dw", "qya"] or (card["digital"] and not card["set_type"] == "alchemy") or card["layout"] == "art_series" or card["set_type"] == "memorabilia" or card["set_type"] == "minigame" or card["image_status"] == "missing" or card["image_status"] == "lowres" or ("promo_types" in card and "thick" in card["promo_types"]) or ("promo_types" in card and "datestamped" in card["promo_types"]) or ("promo_types" in card and "thick" in card["promo_types"]):
            # logger.info(f"Skipping a missing image.")
            continue
        if "card_faces" in card.keys() and card["layout"] in ["transform", "modal_dfc", "battle", "double_faced_token", "reversible_card"]:
            image_uri_A = to_grid(card["card_faces"][0]["image_uris"]["normal"])
            image_uri_B = to_grid(card["card_faces"][1]["image_uris"]["normal"])
            if not s3_has_object(strip_uri(image_uri_A)):
                logger.info(f'Uploading card image for {card["card_faces"][0]["name"]}')
                img_resp = requests.get(image_uri_A, headers={"User-Agent": "CERA-LGN/0.0", "Accept": "image/webp"})
                upload_to_s3(io.BytesIO(img_resp.content), strip_uri(image_uri_A))
                did_upload = True
            # else:
            #     logger.info(f"Skipping {card["card_faces"][0]["name"]}")
            if not s3_has_object(strip_uri(image_uri_B)):
                logger.info(f'Uploading card image for {card["card_faces"][1]["name"]}')
                img_resp = requests.get(image_uri_B, headers={"User-Agent": "CERA-LGN/0.0", "Accept": "image/webp"})
                upload_to_s3(io.BytesIO(img_resp.content), strip_uri(image_uri_B))
                did_upload = True
            # else:
            #     logger.info(f"Skipping {card["card_faces"][1]["name"]}")
        else:
            image_uri = to_grid(card["image_uris"]["normal"])
            if not s3_has_object(strip_uri(image_uri)):
                logger.info(f'Uploading card image for {card["name"]} as {strip_uri(image_uri)}')
                img_resp = requests.get(image_uri, headers={"User-Agent": "CERA-LGN/0.0", "Accept": "image/webp"})
                upload_to_s3(io.BytesIO(img_resp.content), strip_uri(image_uri))
                did_upload = True
            # else:
            #     logger.info(f"Skipping {card["name"]}")
        if did_upload:
            i += 1
            time.sleep(2)
    f.close()
    logger.info(f"Done uploading {i} images.")


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
        resp = requests.get("https://api.scryfall.com/bulk-data", headers={"User-Agent": "CERA-LGN/0.0", "Accept": "*/*"})
        body = resp.json()
        download_uri = None
        if "data" not in body:
            logger.info(f"Failed to get cards: {body}")
            return await ctx.send(content="Updating default_cards failed. Contact Moon.")
        for direction in body["data"]:
            if direction["type"] == "default_cards":
                download_uri = direction["jsonl_download_uri"]
        if download_uri is None:
            return await ctx.send(content="Updating default_cards failed. Contact Moon.")
        deep_resp = requests.get(download_uri, headers={"User-Agent": "CERA-LGN/0.0", "Accept": "*/*"})
        with open("default-cards.jsonl", "w") as fd:
            decompressed_string = gzip.decompress(deep_resp.content).decode("utf-8")
            fd.write(decompressed_string)

    @commands.slash_command(name="image-update", description="Updates the image cache with any potential new images.")
    async def image(self, ctx: discord.ApplicationContext):
        await ctx.defer()
        if str(ctx.author.id) != "237059875073556481":
            await ctx.respond(content="Blocked so that this command doesn't get spammed. <@237059875073556481>, update the image cache!")
            return
        blocking_func()
        await ctx.respond(content=f"Updating the image cache! This may take a while. Please be patient.")


def setup(bot):
    bot.add_cog(Stonewood(bot))
