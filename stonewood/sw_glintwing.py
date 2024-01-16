import asyncio
import json
import discord
import glintwing
import datetime

from glintwing.draft_class_v2 import SwissPlayer

taglist = {
    "ptm": "Prime Time With Moon",
    "ths": "Thursday Night Draft",
    "deb": "Draft Every Block",
    "anti": "No Tag",
}
bslash = "\n"
seat_order = ["chair_white", "chair_brown", "chair_red", "chair_orange", "chair_yellow", "chair_green", "chair_teal", "chair_blue", "chair_purple", "chair_pink"]
"""Names of the seat emojis in order."""


def get_name(bot: discord.Bot, id, guild_id=None) -> str:
    g = None
    u = bot.get_user(id)
    if guild_id is not None:
        g = bot.get_guild(guild_id)
        if g is not None:
            u = g.get_member(id)
    if u is not None:
        return u.display_name
    return "Unknown User"


def starting_em(draft: glintwing.SwissEvent, bot: discord.Bot, guild_id):
    return discord.Embed(
        title=f"{draft.title} | ENTRY",
        fields=[
            discord.EmbedField(
                name="PLAYERS",
                value=f"{bslash.join([f'{get_name(bot, p.id, guild_id)} | Seat: {p.seat}' for p in sorted(draft.players, key=lambda x: x.seat)])}",
            ),
        ],
        description=f"{draft.description}{bslash}*{taglist[draft.tag]}*{bslash}Don't share seats!",
    )


def intermediate_em(draft: glintwing.SwissEvent, timekeepstamp: datetime.datetime, bot: discord.Bot, round_num, round, guild_id):
    return discord.Embed(
        title=f"{draft.title} | Round {round_num + 1}",
        fields=[
            discord.EmbedField(
                inline=True,
                name=f"GAME: {get_name(bot, match.player_one.id, guild_id) + ' (' + str(draft.secondary_stats(match.player_one.id)[0], round_num) + ')' if match.player_one is not None else ''} vs {get_name(bot, match.player_two.id, guild_id) + ' (' + str(draft.secondary_stats(match.player_two.id)[0], round_num) + ')' if match.player_two is not None else 'BYE'}",
                value=f"G1W: {get_name(bot, match.game_one.id, guild_id) if match.game_one is not None else ''}{bslash}G2W: {get_name(bot, match.game_two.id, guild_id) if match.game_two is not None else ''}{bslash}G3W: {get_name(bot, match.game_three.id, guild_id) if match.game_three is not None else ''}" + ((f"{bslash}{get_name(bot, match.player_one.id, guild_id)} has dropped." if match.player_one.dropped else "") if match.player_one is not None else "") + ((f"{bslash}{get_name(bot, match.player_two.id, guild_id)} has dropped." if match.player_two.dropped else "") if match.player_two is not None else ""),
            )
            for match in round
        ]
        + [discord.EmbedField(name="ROUND TIMER", value=f"The round ends <t:{int(timekeepstamp.timestamp())}:R>.")],
        description=f"{draft.description}{bslash}*{taglist[draft.tag]}*",
    )


def end_em(draft: glintwing.SwissEvent, bot: discord.Bot, guild_id):
    return discord.Embed(
        title=f"{draft.title} | FINAL",
        fields=[
            discord.EmbedField(
                inline=True,
                name=f"{get_name(bot, player.id, guild_id)}",
                value=f"SCORE: {(stats:=draft.secondary_stats(player.id))[0]}{bslash}GWP: {stats[1]:.2f}{bslash}OGP: {stats[3]:.2f}{bslash}OMP: {stats[4]:.2f}",
            )
            for player in sorted(draft.players, key=lambda pl: draft.secondary_stats(pl), reverse=True)
        ],
        description=f"{draft.description}{bslash}*{taglist[draft.tag]}*",
    )


class Glintwing(discord.ext.commands.Cog):
    def __init__(self, bot: discord.Bot):
        self.bot = bot
        self.drafts: dict[str, glintwing.SwissEvent] = {}
        self.timekeep: dict[str, datetime.datetime] = {}

    @discord.ext.commands.Cog.listener()
    async def on_reaction_add(self, reaction: discord.Reaction, user: discord.User):
        if reaction.message.id not in self.drafts.keys() or user.id == self.bot.user.id:
            return
        this_draft = self.drafts[reaction.message.id]
        if len(this_draft.round_one) == 0:
            if type(reaction.emoji) != "str":
                if reaction.emoji.name not in seat_order:
                    return
                this_player = this_draft.get_player_by_id(user.id)
                if this_player is None:
                    return
                for idx, color in enumerate(seat_order):
                    if color == reaction.emoji.name:
                        for player in this_draft.players:
                            if player.seat == idx:
                                player.seat = len(this_draft.players)
                                break
                        this_player.seat = idx
                new_view = StartingView(self)
                await reaction.message.edit(embeds=[starting_em(self.drafts[reaction.message.id], self.bot, reaction.message.guild.id)], view=new_view)
                await reaction.message.remove_reaction(reaction.emoji, user)
        return

    @discord.ext.commands.slash_command()
    @discord.option(name="title", description="The name of the draft event.")
    @discord.option(name="tag", description="Choose a tag.", choices=[discord.OptionChoice(v, k) for k, v in taglist.items()], default="anti")
    @discord.option(name="desc", description="Describe the event.", default="")
    @discord.option(name="cube_id", description="The CubeCobra id for the cube you're playing.", default="")
    @discord.option(name="set_code", description="The set code of the set you're playing, for example `woe` for Wilds of Eldraine.", default="")
    async def draft(self, ctx: discord.ApplicationContext, title: str, tag: str = "anti", desc: str = "", cube_id: str = "", set_code: str = ""):
        await ctx.respond(content="Setting up your draft...")
        new_view = StartingView(self)
        msg = await ctx.interaction.original_response()
        self.drafts[msg.id] = glintwing.SwissEvent(id=msg.id, host=str(ctx.author.id), tag=tag, description=desc, title=title, set_code=set_code, cube_id=cube_id)
        self.timekeep[msg.id] = datetime.datetime.now()
        await ctx.interaction.edit_original_response(embeds=[starting_em(self.drafts[msg.id], self.bot, ctx.guild_id)], content="", view=new_view)
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

    @discord.ui.button(label="JOIN", style=discord.ButtonStyle.primary, row=0)
    async def join(self, btn: discord.ui.Button, ctx: discord.Interaction):
        if ctx.message.id not in self.bot.drafts.keys():
            return
        if len(self.bot.drafts[ctx.message.id].players) == 10:
            return
        this_draft = self.bot.drafts[ctx.message.id]
        if ctx.user.id in this_draft.players:
            return await ctx.response.send_message(content="Interaction received.", ephemeral=True)
        this_draft.players.append(glintwing.SwissPlayer(ctx.user.id, len(this_draft.players)))
        for i, player in enumerate(sorted(this_draft.players, key=lambda p: p.seat)):
            player.seat = i
        await ctx.message.edit(embeds=[starting_em(self.bot.drafts[ctx.message.id], self.bot.bot, ctx.guild_id)], view=self)
        return await ctx.response.send_message(content="Interaction received.", ephemeral=True)

    @discord.ui.button(label="DROP", style=discord.ButtonStyle.danger, row=0)
    async def drop(self, btn: discord.ui.Button, ctx: discord.Interaction):
        if ctx.message.id not in self.bot.drafts.keys():
            return
        self.bot.drafts[ctx.message.id].players = [y for y in filter(lambda x: x.id != ctx.user.id, self.bot.drafts[ctx.message.id].players)]
        await ctx.message.edit(embeds=[starting_em(self.bot.drafts[ctx.message.id], self.bot.bot, ctx.guild_id)], view=self)
        return await ctx.response.send_message(content="Interaction received.", ephemeral=True)

    @discord.ui.button(label="BEGIN", style=discord.ButtonStyle.green, row=0)
    async def begin(self, btn: discord.ui.Button, ctx: discord.Interaction):
        if ctx.message.id not in self.bot.drafts.keys():
            return
        if self.bot.drafts[ctx.message.id].host == str(ctx.user.id):
            if not all(x.seat > -1 for x in self.bot.drafts[ctx.message.id].players):
                return await ctx.response.send_message(content="Interaction received. Players are not seated.", ephemeral=True)
            if len(self.bot.drafts[ctx.message.id].players) < 4 or len(self.bot.drafts[ctx.message.id].players) > 10:
                return await ctx.response.send_message(content="Interaction received. Not enough players or too many players.", ephemeral=True)
            new_view = IG_View(self.bot)
            this_draft = self.bot.drafts[ctx.message.id]
            this_draft.round_one = this_draft.pair_round_one()
            self.bot.timekeep[ctx.message.id] = datetime.datetime.now() + datetime.timedelta(minutes=60)
            new_view.after_load(ctx.message.id, ctx.guild_id)
            await ctx.message.edit(embeds=[intermediate_em(self.bot.drafts[ctx.message.id], self.bot.timekeep[ctx.message.id], self.bot.bot, 0, this_draft.round_one, ctx.guild_id)], view=new_view)
            await ctx.message.clear_reactions()
        return await ctx.response.send_message(content="Interaction received.", ephemeral=True)


class IG_View(discord.ui.View):
    def __init__(self, bot: Glintwing):
        self.bot = bot
        super().__init__(timeout=None)

    def after_load(self, id, guild_id):
        for p in self.bot.drafts[id].players:
            self.children[4].append_option(discord.SelectOption(label=f"{get_name(self.bot.bot, p.id, guild_id)}", value=f"{p.id}"))

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
    )
    async def report(self, select: discord.ui.Select, ctx: discord.Interaction):
        if ctx.message.id not in self.bot.drafts.keys():
            return
        this_draft = self.bot.drafts[ctx.message.id]
        round_num, this_round = this_draft.current_round
        selection = select.values[0]
        for pairing in this_round:
            if pairing.player_one is None or pairing.player_two is None:
                continue
            if pairing.player_one.id == ctx.user.id:
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
            elif pairing.player_two.id == ctx.user.id:
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
        await ctx.message.edit(embeds=[intermediate_em(self.bot.drafts[ctx.message.id], self.bot.timekeep[ctx.message.id], self.bot.bot, round_num, this_round, ctx.guild_id)], view=self)
        return await ctx.response.send_message(content="Interaction received.", ephemeral=True)

    @discord.ui.button(label="DROP", style=discord.ButtonStyle.danger, row=0)
    async def drop(self, btn: discord.ui.Button, ctx: discord.Interaction):
        if ctx.message.id not in self.bot.drafts.keys():
            return
        this_draft = self.bot.drafts[ctx.message.id]
        round_num, this_round = this_draft.current_round
        this_player = this_draft.get_player_by_id(ctx.user.id)
        this_player.dropped = True
        await ctx.message.edit(embeds=[intermediate_em(self.bot.drafts[ctx.message.id], self.bot.timekeep[ctx.message.id], self.bot.bot, round_num, this_round, ctx.guild_id)], view=self)
        return await ctx.response.send_message(content="Interaction received.", ephemeral=True)

    @discord.ui.button(label="NEXT", style=discord.ButtonStyle.primary, row=0)
    async def advance(self, btn: discord.ui.Button, ctx: discord.Interaction):
        if ctx.message.id not in self.bot.drafts.keys():
            return
        if self.bot.drafts[ctx.message.id].host == str(ctx.user.id):
            this_draft = self.bot.drafts[ctx.message.id]
            round_num, this_round = this_draft.current_round
            if round_num == 0:
                this_draft.round_two = this_draft.pair_round_two()
                self.bot.timekeep[ctx.message.id] = datetime.datetime.now() + datetime.timedelta(minutes=50)
                await ctx.message.edit(embeds=[intermediate_em(self.bot.drafts[ctx.message.id], self.bot.timekeep[ctx.message.id], self.bot.bot, 1, this_draft.round_two, ctx.guild_id)], view=self)
            if round_num == 1:
                this_draft.round_three = this_draft.pair_round_three()
                self.bot.timekeep[ctx.message.id] = datetime.datetime.now() + datetime.timedelta(minutes=50)
                await ctx.message.edit(embeds=[intermediate_em(self.bot.drafts[ctx.message.id], self.bot.timekeep[ctx.message.id], self.bot.bot, 2, this_draft.round_three, ctx.guild_id)], view=self)
            if round_num == 2:
                await ctx.message.edit(embeds=[end_em(self.bot.drafts[ctx.message.id], self.bot.bot, ctx.guild_id)], view=None)
                with open(f"glintwing/{ctx.message.id}.json", "w") as f:
                    json.dump(self.bot.drafts[ctx.message.id].json, f, ensure_ascii=False, indent=4)
        return await ctx.response.send_message(content="Interaction received.", ephemeral=True)

    @discord.ui.button(label="BACK", style=discord.ButtonStyle.danger, row=0)
    async def reverse(self, btn: discord.ui.Button, ctx: discord.Interaction):
        if ctx.message.id not in self.bot.drafts.keys():
            return
        if self.bot.drafts[ctx.message.id].host == str(ctx.user.id):
            this_draft = self.bot.drafts[ctx.message.id]
            round_num, this_round = this_draft.current_round
            if round_num == 2:
                this_draft.round_three = []
                round_num = 1
            if round_num == 1:
                this_draft.round_two = []
                round_num = 0
            await ctx.message.edit(embeds=[intermediate_em(self.bot.drafts[ctx.message.id], self.bot.timekeep[ctx.message.id], self.bot.bot, round_num, this_round, ctx.guild_id)])
        return await ctx.response.send_message(content="Interaction received.", ephemeral=True)

    @discord.ui.select(placeholder="Toggle a player's drop status. Host only.", min_values=1, max_values=1, row=2)
    async def toggle_drop(self, select: discord.ui.Select, ctx: discord.Interaction):
        if ctx.message.id not in self.bot.drafts.keys():
            return
        if str(ctx.user.id) == self.bot.drafts[ctx.message.id].host or str(select.values[0]) == str(ctx.user.id):
            this_draft = self.bot.drafts[ctx.message.id]
            round_num, this_round = this_draft.current_round
            myplayer = this_draft.get_player_by_id(select.values[0])
            myplayer.dropped = True
            await ctx.message.edit(embeds=[intermediate_em(self.bot.drafts[ctx.message.id], self.bot.timekeep[ctx.message.id], self.bot.bot, round_num, this_round, ctx.guild_id)], view=self)
        return await ctx.response.send_message(content="Interaction received.", ephemeral=True)

    @discord.ui.button(label="END", style=discord.ButtonStyle.red, row=0)
    async def premature_end(self, btn: discord.ui.Button, ctx: discord.Interaction):
        if ctx.message.id not in self.bot.drafts.keys():
            return
        if self.bot.drafts[ctx.message.id].host == str(ctx.user.id):
            with open(f"glintwing/{ctx.message.id}.json", "w") as f:
                json.dump(self.bot.drafts[ctx.message.id], f, ensure_ascii=False, indent=4)
            await ctx.message.edit(embeds=[end_em(self.bot.drafts[ctx.message.id].json, self.bot.bot, ctx.guild_id)], view=None)
        return await ctx.response.send_message(content="Interaction received.", ephemeral=True)


def setup(bot):
    bot.add_cog(Glintwing(bot))
