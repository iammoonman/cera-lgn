import json
import discord
from discord.ext import commands
from .draft_class import Draft
import pickle
import datetime

taglist = {
    "ptm": "Prime Time With Moon",
    "omn": "Omni's Friday Nights",
    "wks": "Wacky Sundays",
}
bslash = "\n"

with open("guild.pickle", "rb") as f:
    guild: int = pickle.load(f)


class Glintwing(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.drafts: dict[str, Draft] = {}
        self.timekeep: dict[str, datetime.datetime] = {}
        self.pages = []
        self.starting_em = lambda d: discord.Embed(
            title=f"{d.name} | {taglist[d.tag]} | ENTRY",
            fields=[
                discord.EmbedField(
                    name="PLAYERS",
                    value=f"{bslash.join([p.name for p in d.players])}",
                )
            ],
            description=f"{d.description}{bslash}*{taglist[d.tag]}*",
        )
        self.ig_em = lambda d, r: discord.Embed(
            title=f"{d.name} | {taglist[d.tag]} | Round: {(w:=[r for r in d.rounds if not r.completed][0]).title}",
            fields=[
                discord.EmbedField(
                    inline=True,
                    name=f"GAME: {i.players[0]} vs {i.players[1]}",
                    value=f"G1W: {i.players[i.gwinners[0]] if len(i.gwinners) > 0 else 'NONE'}{bslash}"
                    + f"G2 Winner: {(i.players[i.gwinners[1]] if i.gwinners[1] is not None else 'NONE') if len(i.gwinners) > 1 else 'NONE'}{bslash}"
                    + f"G3 Winner: {(i.players[i.gwinners[2]] if i.gwinners[2] is not None else 'NONE') if len(i.gwinners) > 2 else 'NONE'}{bslash}"
                    + (f"{i.players[0]} has dropped.{bslash}" if i.drops[0] else "")
                    + (f"{i.players[1]} has dropped.{bslash}" if i.drops[1] else ""),
                )
                for i in w.matches
            ]
            + [
                discord.EmbedField(
                    name="ROUND TIMER",
                    value=f"The round ends <t:{int(r.timestamp())}:R>.",
                )
            ],
            description=f"{d.description}{bslash}*{taglist[d.tag]}*",
        )
        self.end_em = lambda d: discord.Embed(
            title=f"{d.name} | {taglist[d.tag]} | FINAL",
            fields=[
                discord.EmbedField(
                    inline=True,
                    name=f"{p.name}",
                    value=f"SCORE: {p.score}{bslash}"
                    + f"GWP: {round(p.gwp,2)}{bslash}"
                    + f"OGP: {round(p.ogp,2)}{bslash}"
                    + f"OMP: {round(p.omp,2)}",
                )
                for p in sorted(
                    d.players,
                    key=lambda pl: (pl.score, pl.gwp, pl.ogp, pl.omp),
                    reverse=True,
                )
            ],
            description=f"{d.description}{bslash}*{taglist[d.tag]}*",
        )

    @commands.slash_command(guilds=[guild])
    @discord.option(name="title", description="The name of the draft event.")
    @discord.option(
        name="tag",
        description="Choose a tag.",
        choices=[discord.OptionChoice(v, k) for k, v in taglist.items()],
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
        tag: str = "",
        desc: str = "",
        rounds: int = 3,
    ):
        msg = await ctx.respond(content="Setting up your draft...")
        vw = StartingView(self)
        print(vw.id, "DRAFT")
        self.drafts[vw.id] = Draft(
            draftID=vw.id,
            date=datetime.datetime.today().strftime("%Y-%m-%d"),
            host=int(ctx.author.id),
            tag=tag,
            description=desc,
            name=title,
            max_rounds=rounds,
        )
        self.drafts[vw.id].add_player(
            p_name=ctx.author.nick if ctx.author.nick is not None else ctx.author.name,
            p_id=int(ctx.author.id),
            is_host=True,
        )
        self.timekeep[vw.id] = datetime.datetime.now()
        await msg.edit_original_message(embeds=[self.starting_em(self.drafts[vw.id])], content="", view=vw)
        return


class StartingView(discord.ui.View):
    def __init__(self, bot: Glintwing):
        self.bot = bot
        super().__init__(timeout=None)

    @discord.ui.button(label="JOIN", style=discord.ButtonStyle.primary, row=0)
    async def join(self, btn: discord.ui.Button, ctx: discord.Interaction):
        print(self.bot.drafts)
        print(self.id, "JOIN")
        if self.id not in self.bot.drafts.keys():
            # await ctx.delete_original_message()
            return
        self.bot.drafts[self.id].add_player(
            ctx.user.nick if ctx.user.nick is not None else ctx.user.name,
            int(ctx.user.id),
        )
        await ctx.message.edit(
            embeds=[self.bot.starting_em(self.bot.drafts[self.id])],
            view=self,
        )
        return await ctx.response.send_message(content="Interaction received.", ephemeral=True)

    @discord.ui.button(label="DROP", style=discord.ButtonStyle.danger, row=0)
    async def drop(self, btn: discord.ui.Button, ctx: discord.Interaction):
        print(self.id, "DROP")
        if self.id not in self.bot.drafts.keys():
            # await ctx.delete_original_message()
            return
        self.bot.drafts[self.id].drop_player(int(ctx.user.id))
        await ctx.message.edit(
            embeds=[self.bot.starting_em(self.bot.drafts[self.id])],
            view=self,
        )
        return await ctx.response.send_message(content="Interaction received.", ephemeral=True)

    @discord.ui.button(label="BEGIN", style=discord.ButtonStyle.green, row=0)
    async def begin(self, btn: discord.ui.Button, ctx: discord.Interaction):
        print("BEGIN 1")
        if self.id not in self.bot.drafts.keys():
            # await ctx.delete_original_message()
            return
        vw = IG_View(self.bot)
        self.bot.drafts[vw.id] = self.bot.drafts[self.id]
        self.bot.timekeep[vw.id] = self.bot.timekeep[self.id]
        print(self.id, vw.id, "BEGIN")
        self.bot.drafts[vw.id].do_pairings()
        self.bot.timekeep[vw.id] = datetime.datetime.now() + datetime.timedelta(minutes=60)
        await ctx.message.edit(
            embeds=[
                self.bot.ig_em(
                    self.bot.drafts[vw.id],
                    self.bot.timekeep[vw.id],
                )
            ],
            view=vw,
        )
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
        print("REPORT", self.id)
        if self.id not in self.bot.drafts.keys():
            # await ctx.delete_original_message()
            return
        self.bot.drafts[self.id].parse_match(int(ctx.user.id), select.values[0])
        await ctx.message.edit(
            embeds=[
                self.bot.ig_em(
                    self.bot.drafts[self.id],
                    self.bot.timekeep[self.id],
                )
            ],
            view=self,
        )
        return await ctx.response.send_message(content="Interaction received.", ephemeral=True)

    @discord.ui.button(label="DROP", style=discord.ButtonStyle.danger, row=0)
    async def drop(self, btn: discord.ui.Button, ctx: discord.Interaction):
        print("DROP", self.id)
        if self.id not in self.bot.drafts.keys():
            # await ctx.delete_original_message()
            return
        self.bot.drafts[self.id].drop_player(int(ctx.user.id))
        await ctx.message.edit(
            embeds=[
                self.bot.ig_em(
                    self.bot.drafts[self.id],
                    self.bot.timekeep[self.id],
                )
            ],
            view=self,
        )
        return await ctx.response.send_message(content="Interaction received.", ephemeral=True)

    @discord.ui.button(label="NEXT", style=discord.ButtonStyle.primary, row=0)
    async def advance(self, btn: discord.ui.Button, ctx: discord.Interaction):
        print("NEXT", self.id)
        if self.id not in self.bot.drafts.keys():
            # await ctx.delete_original_message()
            return
        if self.bot.drafts[self.id].host == int(ctx.user.id):
            if self.bot.drafts[self.id].finish_round():
                if len([r for r in self.bot.drafts[self.id].rounds if not r.completed]) > 0:
                    self.bot.timekeep[self.id] = datetime.datetime.now() + datetime.timedelta(minutes=50)
                    await ctx.message.edit(
                        embeds=[
                            self.bot.ig_em(
                                self.bot.drafts[self.id],
                                self.bot.timekeep[self.id],
                            )
                        ],
                        view=self,
                    )
                else:
                    print(json.dumps(self.bot.drafts[self.id].tojson()))
                    await ctx.message.edit(embeds=[self.bot.end_em(self.bot.drafts[self.id])], view=None)
            else:
                await ctx.message.edit(
                    content="Not all results reported.",
                    embeds=[
                        self.bot.ig_em(
                            self.bot.drafts[self.id],
                            self.bot.timekeep[self.id],
                        )
                    ],
                    view=self,
                )
        return await ctx.response.send_message(content="Interaction received.", ephemeral=True)


def setup(bot):
    bot.add_cog(Glintwing(bot))


if __name__ == "__main__":
    with open("token.pickle", "rb") as f:
        token = pickle.load(f)

    bot = discord.Bot()
    bot.add_cog(Glintwing(bot))

    @bot.event
    async def on_ready():
        print("hello world")

    bot.run(token)
