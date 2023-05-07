import copy
import json
from typing import Union
import discord
from discord.ext import commands
from .draft_class import Draft
import pickle
import datetime

taglist = {
    "ptm": "Prime Time With Moon",
    "ths": "Thursday Night Draft",
    "anti": "No Tag",
}
bslash = "\n"

with open("guild.pickle", "rb") as f:
    guild: int = pickle.load(f)


def starting_em(draft: Draft):
    return discord.Embed(
        title=f"{draft.title} | ENTRY",
        fields=[
            discord.EmbedField(
                name="PLAYERS", value=f"{bslash.join([f'{p.name} | Seat: {p.seat}' for p in draft.players])}"
            )
        ],
        description=f"{draft.description}{bslash}*{taglist[draft.tag]}*",
    )


def ig_em(draft: Draft, timekeepstamp: datetime.datetime):
    return discord.Embed(
        title=f"{draft.title} | Round: {(w:=[r for r in draft.rounds if not r.completed][0]).title}",
        fields=[
            discord.EmbedField(
                inline=True,
                name=f"GAME: {match.players[0]} vs {match.players[1]}",
                value=f"G1 Winner: {draft.get_player_by_id(match.gwinners[0]) if len(match.gwinners) > 0 and match.gwinners[0] is not None else 'NONE'}{bslash}"
                + f"G2 Winner: {draft.get_player_by_id(match.gwinners[1]) if len(match.gwinners) > 1 and match.gwinners[1] is not None else 'NONE'}{bslash}"
                + f"G3 Winner: {draft.get_player_by_id(match.gwinners[2]) if len(match.gwinners) > 2 and match.gwinners[2] is not None else 'NONE'}{bslash}"
                + (f"{match.players[0]} has dropped.{bslash}" if match.drops[match.players[0].player_id] else "")
                + (f"{match.players[1]} has dropped.{bslash}" if match.drops[match.players[0].player_id] else ""),
            )
            for match in w.matches
        ]
        + [discord.EmbedField(name="ROUND TIMER", value=f"The round ends <t:{int(timekeepstamp.timestamp())}:R>.")],
        description=f"{draft.description}{bslash}*{taglist[draft.tag]}*",
    )


def end_em(draft: Draft):
    return discord.Embed(
        title=f"{draft.title} | FINAL",
        fields=[
            discord.EmbedField(
                inline=True,
                name=f"{player.name}",
                value=f"SCORE: {player.score}{bslash}"
                + f"GWP: {player.gwp:.2f}{bslash}"
                + f"OGP: {player.ogp:.2f}{bslash}"
                + f"OMP: {player.omp:.2f}",
            )
            for player in sorted(
                draft.players,
                key=lambda pl: (pl.score, pl.gwp, pl.ogp, pl.omp),
                reverse=True,
            )
        ],
        description=f"{draft.description}{bslash}*{taglist[draft.tag]}*",
    )


class Glintwing(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.drafts: dict[str, list[Draft]] = {}
        self.timekeep: dict[str, datetime.datetime] = {}
        self.pages = []

    # Have players select what color they were on the table.
    # Players react with emoji of colored squares, use custom emoji for the 10 colors.
    # When someone reacts on one already taken, clear the previous sitter of that seat.
    @commands.Cog.listener()
    async def on_reaction_add(self, reaction: discord.Reaction, user: Union[discord.Member, discord.User]):
        # print(reaction.message) # Find the id of this message's views.
        print(self.drafts.keys(), reaction.message.id)
        if type(reaction.emoji) != 'str':
            print(reaction.emoji.name)
        return

    @commands.slash_command(guilds=[guild])
    @discord.option(name="title", description="The name of the draft event.")
    @discord.option(
        name="tag",
        description="Choose a tag.",
        choices=[discord.OptionChoice(v, k) for k, v in taglist.items()],
        default="anti",
    )
    @discord.option(name="desc", description="Describe the event.", default="")
    @discord.option(
        name="rounds",
        description="The maximum number of rounds for the draft. Default is 3.",
        min_value=1,
        max_value=5,
        default=3,
    )
    async def draft(
        self,
        ctx: discord.ApplicationContext,
        title: str,
        tag: str = "anti",
        desc: str = "",
        rounds: int = 3,
    ):
        msg = await ctx.respond(content="Setting up your draft...")
        new_view = StartingView(self)
        self.drafts[msg.id] = [
            Draft(
                draftID=msg.id,
                date=datetime.datetime.today().strftime("%Y-%m-%d"),
                host=str(ctx.author.id),
                tag=tag,
                description=desc,
                title=title,
                max_rounds=rounds,
            )
        ]
        self.drafts[msg.id][-1].add_player(
            p_name=ctx.author.nick if ctx.author.nick is not None else ctx.author.name,
            p_id=str(ctx.author.id),
            is_host=True,
            seat=0,
        )
        self.timekeep[msg.id] = datetime.datetime.now()
        await msg.edit_original_response(embeds=[starting_em(self.drafts[msg.id][-1])], content="", view=new_view)
        return


class StartingView(discord.ui.View):
    def __init__(self, bot: Glintwing):
        self.bot = bot
        super().__init__(timeout=None)

    @discord.ui.button(label="JOIN", style=discord.ButtonStyle.primary, row=0)
    async def join(self, btn: discord.ui.Button, ctx: discord.Interaction):
        if ctx.message.id not in self.bot.drafts.keys():
            return
        self.bot.drafts[ctx.message.id][-1].add_player(
            ctx.user.nick if ctx.user.nick is not None else ctx.user.name,
            str(ctx.user.id),
            seat=len(self.bot.drafts[ctx.message.id][-1].players),
        )
        await ctx.message.edit(
            embeds=[starting_em(self.bot.drafts[ctx.message.id][-1])],
            view=self,
        )
        return await ctx.response.send_message(content="Interaction received.", ephemeral=True)

    @discord.ui.button(label="DROP", style=discord.ButtonStyle.danger, row=0)
    async def drop(self, btn: discord.ui.Button, ctx: discord.Interaction):
        if ctx.message.id not in self.bot.drafts.keys():
            return
        self.bot.drafts[ctx.message.id][-1].drop_player(str(ctx.user.id))
        await ctx.message.edit(
            embeds=[starting_em(self.bot.drafts[ctx.message.id][-1])],
            view=self,
        )
        return await ctx.response.send_message(content="Interaction received.", ephemeral=True)

    @discord.ui.button(label="BEGIN", style=discord.ButtonStyle.green, row=0)
    async def begin(self, btn: discord.ui.Button, ctx: discord.Interaction):
        if ctx.message.id not in self.bot.drafts.keys():
            return
        if self.bot.drafts[ctx.message.id][-1].host == str(ctx.user.id):
            if not all(x.seat > -1 for x in self.bot.drafts[ctx.message.id][-1].players):
                return await ctx.response.send_message(
                    content="Interaction received. Players are not seated.", ephemeral=True
                )
            if len(self.bot.drafts[ctx.message.id][-1].players) < 4:
                return await ctx.response.send_message(
                    content="Interaction received. Not enough players.", ephemeral=True
                )
            new_view = IG_View(self.bot)
            # self.bot.drafts[ctx.message.id] = [self.bot.drafts[ctx.message.id][-1]]
            # self.bot.timekeep[ctx.message.id] = self.bot.timekeep[ctx.message.id]
            self.bot.drafts[ctx.message.id][-1].finish_round()
            self.bot.timekeep[ctx.message.id] = datetime.datetime.now() + datetime.timedelta(minutes=60)
            new_view.after_load(ctx.message.id)
            await ctx.message.edit(
                embeds=[ig_em(self.bot.drafts[ctx.message.id][-1], self.bot.timekeep[ctx.message.id])],
                view=new_view,
            )
        return await ctx.response.send_message(content="Interaction received.", ephemeral=True)

    # @discord.ui.user_select(placeholder="ADD PLAYER", row=1)
    # async def add_player(self, select: discord.ui.Select, ctx: discord.Interaction):
    #     if self.id not in self.bot.drafts.keys():
    #         # await ctx.delete_original_message()
    #         return
    #     if self.bot.drafts[self.id][-1].host == str(ctx.user.id):
    #         user = ctx.data["resolved"]["users"][ctx.data["values"][-1]]
    #         self.bot.drafts[self.id][-1].add_player(
    #             user["nick"] if "nick" in user else user["username"],
    #             str(user["id"]),
    #         )
    #     await ctx.message.edit(
    #         embeds=[self.bot.starting_em(self.bot.drafts[self.id][-1])],
    #         view=self,
    #     )
    #     return await ctx.response.send_message(content="Interaction received.", ephemeral=True)


class IG_View(discord.ui.View):
    def __init__(self, bot: Glintwing):
        self.bot = bot
        super().__init__(timeout=None)

    def after_load(self, id):
        for p in self.bot.drafts[id][-1].players:
            self.children[4].append_option(discord.SelectOption(label=f"{p.name}", value=f"{p.player_id}"))

    @discord.ui.select(
        placeholder="Report the games you won.",
        row=1,
        min_values=1,
        max_values=1,
        options=[
            discord.SelectOption(label="you - you", value="0", description="You won both games."),
            discord.SelectOption(
                label="you - them - you",
                value="1",
                description="You won the first and third games.",
            ),
            discord.SelectOption(
                label="them - you - you",
                value="2",
                description="You lost the first game, but won overall.",
            ),
            discord.SelectOption(
                label="them - you - them",
                value="3",
                description="You won the second game, but lost the match.",
            ),
            discord.SelectOption(
                label="you - them - them",
                value="4",
                description="You won the first game, but lost overall.",
            ),
            discord.SelectOption(label="them - them", value="5", description="You lost both games."),
            discord.SelectOption(
                label="you - them",
                value="6",
                description="You tied, winning the first game.",
            ),
            discord.SelectOption(
                label="them - you",
                value="7",
                description="You tied, winning the second game.",
            ),
            discord.SelectOption(
                label="them",
                value="8",
                description="Your opponent won game 1 and the match went to time.",
            ),
            discord.SelectOption(
                label="you",
                value="9",
                description="You won game 1 and the match went to time.",
            ),
            discord.SelectOption(
                label="LATE BYE",
                value="-1",
                description="Your opponent didn't show up or had intended to drop.",
            ),
        ],
    )
    async def report(self, select: discord.ui.Select, ctx: discord.Interaction):
        if ctx.message.id not in self.bot.drafts.keys():
            return
        self.bot.drafts[ctx.message.id][-1].parse_match(str(ctx.user.id), select.values[0])
        await ctx.message.edit(
            embeds=[ig_em(self.bot.drafts[ctx.message.id][-1], self.bot.timekeep[ctx.message.id])],
            view=self,
        )
        return await ctx.response.send_message(content="Interaction received.", ephemeral=True)

    @discord.ui.button(label="DROP", style=discord.ButtonStyle.danger, row=0)
    async def drop(self, btn: discord.ui.Button, ctx: discord.Interaction):
        if ctx.message.id not in self.bot.drafts.keys():
            return
        self.bot.drafts[ctx.message.id][-1].drop_player(str(ctx.user.id))
        await ctx.message.edit(
            embeds=[ig_em(self.bot.drafts[ctx.message.id][-1], self.bot.timekeep[ctx.message.id])],
            view=self,
        )
        return await ctx.response.send_message(content="Interaction received.", ephemeral=True)

    @discord.ui.button(label="NEXT", style=discord.ButtonStyle.primary, row=0)
    async def advance(self, btn: discord.ui.Button, ctx: discord.Interaction):
        if ctx.message.id not in self.bot.drafts.keys():
            return
        if self.bot.drafts[ctx.message.id][-1].host == str(ctx.user.id):
            newRoundDraft = copy.deepcopy(self.bot.drafts[ctx.message.id][-1])
            self.bot.drafts[ctx.message.id].append(newRoundDraft)
            if self.bot.drafts[ctx.message.id][-1].finish_round():
                if len([r for r in self.bot.drafts[ctx.message.id][-1].rounds if not r.completed]) > 0:
                    self.bot.timekeep[ctx.message.id] = datetime.datetime.now() + datetime.timedelta(minutes=50)
                    await ctx.message.edit(
                        embeds=[ig_em(self.bot.drafts[ctx.message.id][-1], self.bot.timekeep[ctx.message.id])],
                        view=self,
                    )
                else:
                    with open(f"pagessite/src/data/{ctx.message.id}.json", "w") as f:
                        json.dump(self.bot.drafts[ctx.message.id][-1].tojson(), f, ensure_ascii=False, indent=4)
                    await ctx.message.edit(embeds=[end_em(self.bot.drafts[ctx.message.id][-1])], view=None)
            else:
                self.bot.drafts[ctx.message.id].pop()
                await ctx.message.edit(
                    content="Not all results reported.",
                    embeds=[ig_em(self.bot.drafts[ctx.message.id][-1], self.bot.timekeep[ctx.message.id])],
                    view=self,
                )
        return await ctx.response.send_message(content="Interaction received.", ephemeral=True)

    @discord.ui.button(label="BACK", style=discord.ButtonStyle.danger, row=0)
    async def reverse(self, btn: discord.ui.Button, ctx: discord.Interaction):
        if ctx.message.id not in self.bot.drafts.keys():
            return
        if self.bot.drafts[ctx.message.id][-1].host == str(ctx.user.id):
            if len(self.bot.drafts[ctx.message.id]) > 1:
                self.bot.drafts[ctx.message.id].pop()
            return

    @discord.ui.select(placeholder="Toggle a player's drop status. Host only.", min_values=1, max_values=1, row=2)
    async def toggle_drop(self, select: discord.ui.Select, ctx: discord.Interaction):
        if ctx.message.id not in self.bot.drafts.keys():
            return
        if str(ctx.user.id) == self.bot.drafts[ctx.message.id][-1].host or str(select.values[0]) == str(ctx.user.id):
            self.bot.drafts[ctx.message.id][-1].drop_player(str(select.values[0]))
        await ctx.message.edit(
            embeds=[ig_em(self.bot.drafts[ctx.message.id][-1], self.bot.timekeep[ctx.message.id])],
            view=self,
        )
        return await ctx.response.send_message(content="Interaction received.", ephemeral=True)

    @discord.ui.button(label="TRIM", style=discord.ButtonStyle.red, row=0)
    async def premature_end(self, btn: discord.ui.Button, ctx: discord.Interaction):
        if ctx.message.id not in self.bot.drafts.keys():
            return
        if self.bot.drafts[ctx.message.id][-1].host == str(ctx.user.id):
            self.bot.drafts[ctx.message.id][-1].max_rounds = len(self.bot.drafts[ctx.message.id][-1].rounds)
        return await ctx.response.send_message(content="Interaction received.", ephemeral=True)


def setup(bot):
    bot.add_cog(Glintwing(bot))
