import asyncio
import json
import os
import discord
import glintwing
import datetime
from discord.ext import commands
import pymongo

from glintwing.draft_class_v2 import SwissEvent
from stonewood import logger

bslash = "\n"
seat_order = ["chair_white", "chair_brown", "chair_red", "chair_orange", "chair_yellow", "chair_green", "chair_teal", "chair_blue", "chair_purple", "chair_pink"]
"""Names of the seat emojis in order."""


def grab_draft(id: str):
    logger.info(f"Getting draft with id: {id}")
    client = pymongo.MongoClient(os.environ["external_mongo"])
    db = client.get_database("LimitedPerspective")
    coll = db["Event"]
    d = coll.find_one({"id": f"{id}"})
    if d is None:
        logger.warning(f"Failed to get draft with id: {id}")
        return None
    e = glintwing.SwissEvent(id=f"{id}", channel_id=str(d["meta"].get("channel_id")), host=d["meta"].get("host"), tag=d["meta"].get("tag"), description=d["meta"].get("description"), title=d["meta"].get("title"), cube_id=d["meta"].get("cube_id"), rounds=[d["R_0"], d["R_1"], d["R_2"]], set_code=d["meta"].get("set_code"), seats=d.get("players"), round_times=d["meta"].get("round_times"))
    return e


def put_draft(draft: SwissEvent):
    logger.info(f"Updating draft with id: {draft.id}")
    client = pymongo.MongoClient(os.environ["external_mongo"])
    db = client.get_database("LimitedPerspective")
    coll = db["Event"]
    coll.replace_one({"id": f"{draft.id}"}, dict(draft), upsert=True)


taglist = {}


def get_tags():
    logger.info("Getting tags...")
    global taglist
    r = {}
    client = pymongo.MongoClient(os.environ["external_mongo"])
    db = client.get_database("LimitedPerspective")
    coll = db["Tags"]
    d = coll.find({})
    if d is None:
        logger.warning("Failed to find tags.")
        return {}
    for entry in d:
        r[entry["id"]] = entry["label"]
    taglist = r
    logger.info("Registered tags.")
    return r


async def get_name(bot: discord.Bot, id, guild_id=None) -> str:
    # g = None
    u = await bot.get_or_fetch_user(int(id))
    # if guild_id is not None:
    #     g = bot.fetch_guild(guild_id)
    #     if g is not None:
    #         u = bot.get
    if u is not None:
        return u.display_name
    return "Unknown User"


async def starting_em(draft: glintwing.SwissEvent, bot: discord.Bot, guild_id):
    taglist = get_tags()
    return discord.Embed(
        title=f"{draft.title} | ENTRY",
        fields=[
            discord.EmbedField(
                name="PLAYERS",
                value=f"{bslash.join([f'{await get_name(bot, p.id, guild_id)} | Seat: {p.seat + 1}' for p in sorted(draft.players, key=lambda x: x.seat)])}",
            ),
        ],
        description=f"{draft.description}{bslash}*{taglist[draft.tag] if draft.tag in taglist else 'unknown tag'}*{bslash}Don't share seats!",
    )


async def intermediate_em(draft: glintwing.SwissEvent, bot: discord.Bot, guild_id):
    taglist = get_tags()
    r, n = draft.current_round
    return discord.Embed(
        title=f"{draft.title} | Round {r + 1}",
        fields=[
            discord.EmbedField(
                inline=True,
                name=f"GAME: {await get_name(bot, match.player_one.id, guild_id) + ' (' + str(draft.secondary_stats(match.player_one.id)[0]) + ')' if match.player_one is not None else ''} vs {await get_name(bot, match.player_two.id, guild_id) + ' (' + str(draft.secondary_stats(match.player_two.id)[0]) + ')' if match.player_two is not None else 'BYE'}",
                value=f"G1W: {await get_name(bot, match.game_one.id, guild_id) if match.game_one is not None else ''}{bslash}G2W: {await get_name(bot, match.game_two.id, guild_id) if match.game_two is not None else ''}{bslash}G3W: {await get_name(bot, match.game_three.id, guild_id) if match.game_three is not None else ''}" + ((f"{bslash}{await get_name(bot, match.player_one.id, guild_id)} has dropped." if match.player_one.dropped else "") if match.player_one is not None else "") + ((f"{bslash}{await get_name(bot, match.player_two.id, guild_id)} has dropped." if match.player_two.dropped else "") if match.player_two is not None else ""),
            )
            for match in n
        ]
        + [discord.EmbedField(name="ROUND TIMER", value=f"The round ends <t:{int((draft.round_times[r] + datetime.timedelta(minutes=50)).timestamp())}:R>.")],
        description=f"{draft.description}{bslash}*{taglist[draft.tag] if draft.tag in taglist else 'unknown tag'}*",
    )


async def end_em(draft: glintwing.SwissEvent, bot: discord.Bot, guild_id):
    taglist = get_tags()
    return discord.Embed(
        title=f"{draft.title} | FINAL",
        fields=[
            discord.EmbedField(
                inline=True,
                name=f"{await get_name(bot, player.id, guild_id)}",
                value=f"SCORE: {(stats:=draft.secondary_stats(player.id))[0]}{bslash}GWP: {stats[1]:.2f}{bslash}OGP: {stats[3]:.2f}{bslash}OMP: {stats[4]:.2f}",
            )
            for player in sorted(draft.players, key=lambda pl: draft.secondary_stats(pl), reverse=True)
        ],
        description=f"{draft.description}{bslash}*{taglist[draft.tag] if draft.tag in taglist else 'unknown tag'}*",
    )


class Glintwing(commands.Cog):
    def __init__(self, bot: discord.Bot):
        self.bot = bot
        self.bot.add_view(StartingView(bot))
        self.bot.add_view(IG_View(bot))

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction: discord.Reaction, user: discord.User):
        if user.id == self.bot.user.id:
            return
        this_draft = grab_draft(reaction.message.id)
        if this_draft is None:
            return
        if len(this_draft.round_one) == 0:
            if type(reaction.emoji) is not str:
                if reaction.emoji.name not in seat_order:
                    return
                this_player = this_draft.get_player_by_id(f"{user.id}")
                if this_player is None:
                    return
                for idx, color in enumerate(seat_order):
                    if color == reaction.emoji.name:
                        for player in this_draft.players:
                            if player.seat == idx:
                                player.seat = len(this_draft.players)
                                logger.info(f"Moving player {this_player} to seat {len(this_draft.players)}")
                                break
                        this_player.seat = idx
                        logger.info(f"Moving player {this_player} to seat {idx}")
                new_view = StartingView(self.bot)
                await reaction.message.edit(embeds=[await starting_em(this_draft, self.bot, reaction.message.guild.id)], view=new_view)
                await reaction.message.remove_reaction(reaction.emoji, user)
                put_draft(this_draft)
            else:
                reaction.remove(user)
        return

    @commands.slash_command()
    @discord.option(name="title", description="The name of the draft event.")
    # @discord.option(name="tag", description="Choose a tag.", choices=[discord.OptionChoice(v, k) for k, v in taglist.items()], default="anti")  # This isn't going to work.
    @discord.option(name="desc", description="Describe the event.", default="")
    @discord.option(name="cube_id", description="The CubeCobra id for the cube you're playing.", default="")
    @discord.option(name="set_code", description="The set code of the set you're playing, for example `woe` for Wilds of Eldraine.", default="")
    async def draft(self, ctx: discord.ApplicationContext, title: str, desc: str = "", cube_id: str = "", set_code: str = ""):
        # tag: str = ""
        await ctx.respond(content="Setting up your draft...")
        new_view = StartingView(self.bot)
        msg = await ctx.interaction.original_response()
        this_draft = glintwing.SwissEvent(id=str(msg.id), channel_id=str(msg.channel.id), host=str(ctx.author.id), tag="", description=desc, title=title, set_code=set_code, cube_id=cube_id)
        put_draft(this_draft)
        await ctx.interaction.edit_original_response(embeds=[await starting_em(this_draft, self.bot, ctx.guild_id)], content="", view=new_view)
        await asyncio.gather(
            msg.add_reaction("<:seat_white:1104759507311145012>"),
            msg.add_reaction("<:seat_brown:1104759527808708698>"),
            msg.add_reaction("<:seat_red:1104759572696141915>"),
            msg.add_reaction("<:seat_orange:1104759633693909092>"),
            msg.add_reaction("<:seat_yellow:1104759560905969804>"),
            msg.add_reaction("<:seat_green:1104759586369572874>"),
            msg.add_reaction("<:seat_teal:1104759619739471955>"),
            msg.add_reaction("<:seat_blue:1104759698076479539>"),
            msg.add_reaction("<:seat_purple:1104759602274381884>"),
            msg.add_reaction("<:seat_pink:1104759547228336138>"),
        )
        return


class StartingView(discord.ui.View):
    def __init__(self, bot: Glintwing):
        self.bot = bot
        super().__init__(timeout=None)

    @discord.ui.button(label="JOIN", style=discord.ButtonStyle.primary, row=0, custom_id="JOIN_BUTTON")
    async def join(self, btn: discord.ui.Button, ctx: discord.Interaction):
        this_draft = grab_draft(ctx.message.id)
        if this_draft is None:
            return
        if len(this_draft.players) == 10:
            return
        if str(ctx.user.id) in this_draft.players:
            return await ctx.response.send_message(content="Interaction received.", ephemeral=True)
        this_draft.players.append(glintwing.SwissPlayer(id=f"{ctx.user.id}", seat=len(this_draft.players)))
        for i, player in enumerate(sorted(this_draft.players, key=lambda p: p.seat)):
            player.seat = i
        logger.info(f"Adding player {ctx.user.id} to draft {ctx.message.id}")
        put_draft(this_draft)
        await ctx.message.edit(embeds=[await starting_em(this_draft, self.bot, ctx.guild_id)], view=self)
        return await ctx.response.send_message(content="Interaction received.", ephemeral=True)

    @discord.ui.button(label="DROP", style=discord.ButtonStyle.danger, row=0, custom_id="DROP_BUTTON")
    async def drop(self, btn: discord.ui.Button, ctx: discord.Interaction):
        this_draft = grab_draft(ctx.message.id)
        if this_draft is None:
            return
        this_draft.players = [y for y in filter(lambda x: x.id != f"{ctx.user.id}", this_draft.players)]
        put_draft(this_draft)
        await ctx.message.edit(embeds=[await starting_em(this_draft, self.bot, ctx.guild_id)], view=self)
        return await ctx.response.send_message(content="Interaction received.", ephemeral=True)

    @discord.ui.button(label="BEGIN", style=discord.ButtonStyle.green, row=0, custom_id="BEGIN_BUTTON")
    async def begin(self, btn: discord.ui.Button, ctx: discord.Interaction):
        this_draft = grab_draft(ctx.message.id)
        if this_draft is None:
            return
        if this_draft.host == str(ctx.user.id):
            if not all(x.seat > -1 for x in this_draft.players):
                logger.warning(f"Host attempted to run a draft with some players at negative seats. {ctx.message.id}")
                return await ctx.response.send_message(content="Interaction received. Players are not seated.", ephemeral=True)
            if len(this_draft.players) < 4 or len(this_draft.players) > 10:
                logger.warning(f"Host attempted to run a draft with too many or too few players. {ctx.message.id}")
                return await ctx.response.send_message(content="Interaction received. Not enough players or too many players.", ephemeral=True)
            logger.info(f"Starting draft {ctx.message.id} with host {ctx.user.id}")
            new_view = IG_View(self.bot)
            this_draft = this_draft
            this_draft.round_one = this_draft.pair_round_one()
            put_draft(this_draft)
            await ctx.message.edit(embeds=[await intermediate_em(this_draft, self.bot, ctx.guild_id)], view=new_view)
            await ctx.message.clear_reactions()
        return await ctx.response.send_message(content="Interaction received.", ephemeral=True)


class IG_View(discord.ui.View):
    def __init__(self, bot: Glintwing):
        self.bot = bot
        super().__init__(timeout=None)

    @discord.ui.select(
        placeholder="Report the games you won.",
        row=1,
        min_values=1,
        max_values=1,
        options=[
            discord.SelectOption(label="you - you", value="aa0", description="You won both games."),
            discord.SelectOption(label="you - them - you", value="aba", description="You won the first and third games."),
            discord.SelectOption(label="them - you - you", value="baa", description="You lost the first game, but won overall."),
            discord.SelectOption(label="them - you - them", value="bab", description="You won the second game, but lost the match."),
            discord.SelectOption(label="you - them - them", value="abb", description="You won the first game, but lost overall."),
            discord.SelectOption(label="them - them", value="bb0", description="You lost both games."),
            discord.SelectOption(label="you - them", value="ab0", description="You tied, winning the first game."),
            discord.SelectOption(label="them - you", value="ba0", description="You tied, winning the second game."),
            discord.SelectOption(label="them", value="b00", description="Your opponent won game 1 and the match went to time."),
            discord.SelectOption(label="you", value="a00", description="You won game 1 and the match went to time."),
            discord.SelectOption(label="UNSET", value="000", description="Removes previously entered result."),
        ],
        custom_id="REPORT_SELECT",
    )
    async def report(self, select: discord.ui.Select, ctx: discord.Interaction):
        this_draft = grab_draft(ctx.message.id)
        if this_draft is None:
            return
        round_num, this_round = this_draft.current_round
        selection = select.values[0]
        for pairing in this_round:
            if pairing.player_one is None or pairing.player_two is None:
                continue
            if pairing.player_one.id == str(ctx.user.id):
                if selection[0:1] == "a":
                    pairing.game_one = pairing.player_one
                elif selection[0:1] == "b":
                    pairing.game_one = pairing.player_two
                elif selection[0:1] == "0":
                    pairing.game_one = None
                if selection[1:2] == "a":
                    pairing.game_two = pairing.player_one
                elif selection[1:2] == "b":
                    pairing.game_two = pairing.player_two
                elif selection[1:2] == "0":
                    pairing.game_two = None
                if selection[2:3] == "a":
                    pairing.game_three = pairing.player_one
                elif selection[2:3] == "b":
                    pairing.game_three = pairing.player_two
                elif selection[2:3] == "0":
                    pairing.game_three = None
            elif pairing.player_two.id == str(ctx.user.id):
                if selection[0:1] == "a":
                    pairing.game_one = pairing.player_two
                elif selection[0:1] == "b":
                    pairing.game_one = pairing.player_one
                elif selection[0:1] == "0":
                    pairing.game_one = None
                if selection[1:2] == "a":
                    pairing.game_two = pairing.player_two
                elif selection[1:2] == "b":
                    pairing.game_two = pairing.player_one
                elif selection[1:2] == "0":
                    pairing.game_two = None
                if selection[2:3] == "a":
                    pairing.game_three = pairing.player_two
                elif selection[2:3] == "b":
                    pairing.game_three = pairing.player_one
                elif selection[2:3] == "0":
                    pairing.game_three = None
        put_draft(this_draft)
        await ctx.message.edit(embeds=[await intermediate_em(this_draft, self.bot, ctx.guild_id)], view=self)
        return await ctx.response.send_message(content="Interaction received.", ephemeral=True)

    @discord.ui.button(label="DROP", style=discord.ButtonStyle.danger, row=0, custom_id="DROP_BUTTON_INGAME")
    async def drop(self, btn: discord.ui.Button, ctx: discord.Interaction):
        this_draft = grab_draft(ctx.message.id)
        if this_draft is None:
            return
        round_num, this_round = this_draft.current_round
        this_player = this_draft.get_player_by_id(str(ctx.user.id))
        this_player.dropped = True
        put_draft(this_draft)
        await ctx.message.edit(embeds=[await intermediate_em(this_draft, self.bot, ctx.guild_id)], view=self)
        return await ctx.response.send_message(content="Interaction received.", ephemeral=True)

    @discord.ui.button(label="NEXT", style=discord.ButtonStyle.primary, row=0, custom_id="NEXT_BUTTON")
    async def advance(self, btn: discord.ui.Button, ctx: discord.Interaction):
        this_draft = grab_draft(ctx.message.id)
        if this_draft is None:
            return
        if this_draft.host == str(ctx.user.id):
            round_num, this_round = this_draft.current_round
            logger.info(f"Advancing draft {ctx.message.id} from round {round_num}")
            if round_num == 0:
                this_draft.round_two, was_imperfect = this_draft.pair_round_two()
                if was_imperfect:
                    logger.warning(f"Pairing for draft {this_draft.id} was imperfect.")
                    await ctx.response.send_message(content="These pairings were randomized after the bot failed to pair the players according to typical pairings rules. Contact Moon if you believe this is incorrect.", ephemeral=True)
                await ctx.message.edit(embeds=[await intermediate_em(this_draft, self.bot, ctx.guild_id)], view=self)
            if round_num == 1:
                this_draft.round_thr, was_imperfect = this_draft.pair_round_three()
                if was_imperfect:
                    logger.warning(f"Pairing for draft {this_draft.id} was imperfect.")
                    await ctx.response.send_message(content="These pairings were randomized after the bot failed to pair the players according to typical pairings rules. Contact Moon if you believe this is incorrect.", ephemeral=True)
                await ctx.message.edit(embeds=[await intermediate_em(this_draft, self.bot, ctx.guild_id)], view=self)
            if round_num == 2:
                e = await end_em(this_draft, self.bot, ctx.guild_id)
                await ctx.message.edit(embeds=[e], view=None)
                # with open(f"glintwing/{ctx.message.id}.json", "w") as f:
                #     json.dump(dict(this_draft), f, ensure_ascii=False, indent=4)
            put_draft(this_draft)
        return await ctx.response.send_message(content="Interaction received.", ephemeral=True)

    @discord.ui.button(label="BACK", style=discord.ButtonStyle.danger, row=0, custom_id="BACK_BUTTON")
    async def reverse(self, btn: discord.ui.Button, ctx: discord.Interaction):
        this_draft = grab_draft(ctx.message.id)
        if this_draft is None:
            return
        if this_draft.host == str(ctx.user.id):
            round_num, this_round = this_draft.current_round
            logger.info(f"Retreating draft {ctx.message.id} from round {round_num}")
            if round_num == 1:
                this_draft.round_two = []
                logger.info(f"Deleting round two of draft: {ctx.message.id}")
            if round_num == 2:
                this_draft.round_thr = []
                logger.info(f"Deleting round three of draft: {ctx.message.id}")
            put_draft(this_draft)
            await ctx.message.edit(embeds=[await intermediate_em(this_draft, self.bot, ctx.guild_id)], view=self)
        return await ctx.response.send_message(content="Interaction received.", ephemeral=True)

    @discord.ui.select(placeholder="Toggle a player's drop status. Host only.", select_type=discord.ComponentType.user_select, row=2, custom_id="TOGGLE_SELECT")
    async def toggle_drop(self, select: discord.ui.Select, ctx: discord.Interaction):
        this_draft = grab_draft(ctx.message.id)
        if this_draft is None:
            return
        if str(ctx.user.id) == this_draft.host or str(select.values[0].id) == str(ctx.user.id):
            round_num, this_round = this_draft.current_round
            myplayer = this_draft.get_player_by_id(str(select.values[0]))
            if myplayer is not None:
                myplayer.dropped = True
            else:
                logger.warning(f"The host of draft {ctx.message.id} tried to drop a player not in the draft: {str(select.values[0].id)}")
            logger.info(f"Host dropped player {select.values[0].id} from draft {ctx.message.id}")
            put_draft(this_draft)
            await ctx.message.edit(embeds=[await intermediate_em(this_draft, self.bot, ctx.guild_id)], view=self)
        return await ctx.response.send_message(content="Interaction received.", ephemeral=True)

    @discord.ui.button(label="END", style=discord.ButtonStyle.red, row=0, custom_id="END_BUTTON")
    async def premature_end(self, btn: discord.ui.Button, ctx: discord.Interaction):
        this_draft = grab_draft(ctx.message.id)
        if this_draft is None:
            return
        if this_draft.host == str(ctx.user.id):
            logger.info(f"Ending draft {ctx.message.id} early")
            e = await end_em(this_draft, self.bot, ctx.guild_id)
            await ctx.message.edit(embeds=[e], view=None)
            # with open(f"glintwing/{ctx.message.id}.json", "w") as f:
            #     json.dump(dict(this_draft), f, ensure_ascii=False, indent=4)
            put_draft(this_draft)
        return await ctx.response.send_message(content="Interaction received.", ephemeral=True)

    @discord.ui.button(label="REFRESH", style=discord.ButtonStyle.gray, row=0, custom_id="REFRESH")
    async def refresh_draft(self, btn: discord.ui.Button, ctx: discord.Interaction):
        this_draft = grab_draft(ctx.message.id)
        if this_draft is None:
            return
        await ctx.message.edit(embeds=[await intermediate_em(this_draft, self.bot, ctx.guild_id)], view=self)
        return await ctx.response.send_message(content="Interaction received.", ephemeral=True)


def setup(bot):
    bot.add_cog(Glintwing(bot))
