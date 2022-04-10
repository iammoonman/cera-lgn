import interactions
import draft_class
from datetime import datetime
import requests
import re

import pickle

with open("token.pickle", "rb") as f:
    token = pickle.load(f)

bot = interactions.Client(token=token)

events = []
drafts = {}
timekeep = {}


@bot.event
async def on_ready():
    print("Logged in as")
    # print(bot.user.name)
    # print(bot.user.id)
    print("------")


# ---------------------------------------------------------------------------------------------#
# ---------------------------------------------------------------------------------------------#
# ---------------------------------------------------------------------------------------------#
# ---------------------------------------------------------------------------------------------#
# ---------------------------------------------------------------------------------------------#

button0 = interactions.Button(
    style=interactions.ButtonStyle.PRIMARY, label="JOIN", custom_id="JOIN"
)


@bot.component(button0)
async def btn0_response(ctx):
    """Join the draft"""
    print(ctx.message.id, "JOIN")
    drafts[str(ctx.message.id)].add_player(ctx.author.nick, int(ctx.author.user.id))
    # TypeError: 'list' object is not callable
    await ctx.edit(
        embed=starting_embed(drafts[str(ctx.message.id)]), components=starting_buttons()
    )
    return


# ---------------------------------------------------------------------------------------------#
# ---------------------------------------------------------------------------------------------#

button1 = interactions.Button(
    style=interactions.ButtonStyle.DANGER, label="DROP", custom_id="DROP_PRE"
)


@bot.component(button1)
async def btn1_response(ctx):
    """Drop from the draft before it begins"""
    print(ctx.message.id, "DROP_PRE")
    # Check if the user is the host
    drafts[str(ctx.message.id)].drop_player(int(ctx.user.id))
    await ctx.edit(
        embed=starting_embed(drafts[str(ctx.message.id)]), components=starting_buttons()
    )
    return


# ---------------------------------------------------------------------------------------------#
# ---------------------------------------------------------------------------------------------#

button2 = interactions.Button(
    style=interactions.ButtonStyle.SECONDARY, label="DROPKICK", custom_id="DROPKICK"
)


@bot.component(button2)
async def btn2_response(ctx):
    """Kick all from the draft"""
    print(ctx.message.id, "DROP_KICK")
    # Check if the user is the host
    if int(ctx.user.id) == drafts[str(ctx.message.id)].host:
        drafts[str(ctx.message.id)].players = [
            p
            for p in drafts[str(ctx.message.id)]
            if int(p.player_id) == drafts[str(ctx.message.id)].host
        ]
    await ctx.edit(
        embed=starting_embed(drafts[str(ctx.message.id)]), components=starting_buttons()
    )
    return


# ---------------------------------------------------------------------------------------------#
# ---------------------------------------------------------------------------------------------#

button3 = interactions.Button(
    style=interactions.ButtonStyle.DANGER, label="CANCEL", custom_id="CANCEL"
)


@bot.component(button3)
async def btn3_response(ctx: interactions.context.ComponentContext):
    """Cancel the draft"""
    print(ctx.message.id, "CANCEL")
    print(ctx.author.user.id, "HOST")
    print(drafts[str(ctx.message.id)].host, "HOST 2")
    # Check if the user is the host
    if int(ctx.author.user.id) == drafts[str(ctx.message.id)].host:
        del drafts[str(ctx.message.id)]
        await ctx.delete()
    return


# ---------------------------------------------------------------------------------------------#
# ---------------------------------------------------------------------------------------------#

button4 = interactions.Button(
    style=interactions.ButtonStyle.SUCCESS, label="BEGIN", custom_id="BEGIN"
)


@bot.component(button4)
async def btn4_response(ctx):
    """Begin the draft"""
    print(ctx.message.id, "BEGIN")
    # Check if the user is the host
    if int(ctx.user.id) == drafts[str(ctx.message.id)].host:
        drafts[str(ctx.message.id)].do_pairings()
        timekeep[str(ctx.message.id)] = datetime.now() + datetime.timedelta(minutes=50)
        # Edit the message so that it shows the pairings and the score buttons
        await ctx.edit(
            embed=ig_embed(
                drafts[str(ctx.message.id)].name,
                [r for r in drafts[str(ctx.message.id)].rounds if not r.completed][0],
                round_end=timekeep[str(ctx.message.id)],
            ),
            components=in_draft_buttons(),
        )
    return


# ---------------------------------------------------------------------------------------------#
# ---------------------------------------------------------------------------------------------#

starting_buttons = [button0, button1, button2, button3, button4]


button5 = interactions.Button(
    style=interactions.ButtonStyle.PRIMARY, label="NEXT_ROUND", custom_id="NEXT_ROUND"
)


@bot.component(button5)
async def btn5_response(ctx):
    """Advance to the next round"""
    print(ctx.message.id, "NEXT_ROUND")
    # Check if the user is the host
    if int(ctx.user.id) == drafts[str(ctx.message.id)].host:
        timekeep[str(ctx.message.id)] = datetime.now() + datetime.timedelta(minutes=50)
        # Add a check to see if the third round has been played, then swap to posting the final results and send the json to dm.
        if drafts[str(ctx.message.id)].finish_round():
            roundsearch = [
                r for r in drafts[str(ctx.message.id)].rounds if not r.completed
            ]
            if len(roundsearch) > 0:
                await ctx.edit(
                    embed=ig_embed(
                        drafts[str(ctx.message.id)].name,
                        roundsearch[0],
                        round_end=timekeep[str(ctx.message.id)],
                    ),
                    components=in_draft_buttons(),
                )
            else:
                await ctx.edit(embed=end_embed(drafts[str(ctx.message.id)]))
                # Send the json to the owner
                print(drafts[str(ctx.message.id)].tojson())
                member = interactions.Member(
                    **await bot.http.get_member(guild_id=id, member_id=ctx.user.id),
                    _client=bot.http,
                )
                await member.send(drafts[str(ctx.message.id)].tojson())
        else:
            await ctx.edit(
                content="Not all results reported.",
                embed=ig_embed(
                    drafts[str(ctx.message.id)].name,
                    [r for r in drafts[str(ctx.message.id)].rounds if not r.completed][
                        0
                    ],
                    round_end=timekeep[str(ctx.message.id)],
                ),
                components=in_draft_buttons(),
            )
    return


# ---------------------------------------------------------------------------------------------#
# ---------------------------------------------------------------------------------------------#

select0 = interactions.SelectMenu(
    options=[
        interactions.SelectOption(
            label="self - self", value="0", description="You won both games."
        ),
        interactions.SelectOption(
            label="self - opponent - self",
            value="1",
            description="You won the first and third games.",
        ),
        interactions.SelectOption(
            label="opponent - self - self",
            value="2",
            description="You lost the first game, but reverse swept the match.",
        ),
        interactions.SelectOption(
            label="opponent - self - opponent",
            value="3",
            description="You won the second game, but lost the match.",
        ),
        interactions.SelectOption(
            label="self - opponent - opponent",
            value="4",
            description="You won the first game, but got reverse swept to lose.",
        ),
        interactions.SelectOption(
            label="opponent - opponent", value="5", description="You lost both games."
        ),
        interactions.SelectOption(
            label="self - opponent",
            value="6",
            description="You tied, and won the first game.",
        ),
        interactions.SelectOption(
            label="opponent - self",
            value="7",
            description="You tied, and won the second game.",
        ),
    ],
    placeholder="Choose the games you won.",
    custom_id="WINSELECT",
    min_values=1,
    max_values=1,
)


@bot.component(select0)
async def sel0_response(ctx):
    """Select the winners of the author's match"""
    print(ctx.message.id, "WINNINGS")
    drafts[str(ctx.message.id)].parse_match(int(ctx.user.id), ctx.data.values[0])
    await ctx.edit(
        embed=ig_embed(
            drafts[str(ctx.message.id)].name,
            [r for r in drafts[str(ctx.message.id)].rounds if not r.completed][0],
            round_end=timekeep[str(ctx.message.id)],
        ),
        components=in_draft_buttons(),
    )
    return


# ---------------------------------------------------------------------------------------------#
# ---------------------------------------------------------------------------------------------#

button6 = interactions.Button(
    style=interactions.ButtonStyle.DANGER, label="DROP", custom_id="DROP_IG"
)


@bot.component(button6)
async def btn6_response(ctx):
    """Drop from the draft while it is running"""
    print(ctx.message.id, "DROP_IG")
    drafts[str(ctx.message.id)].drop_player(int(ctx.user.id))
    await ctx.edit(
        embed=ig_embed(
            drafts[str(ctx.message.id)].name,
            [r for r in drafts[str(ctx.message.id)].rounds if not r.completed][0],
            round_end=timekeep[str(ctx.message.id)],
        ),
        components=in_draft_buttons(),
    )
    return


# ---------------------------------------------------------------------------------------------#
# ---------------------------------------------------------------------------------------------#

in_draft_buttons = [button5, select0, button6]

# ---------------------------------------------------------------------------------------------#
# ---------------------------------------------------------------------------------------------#
# ---------------------------------------------------------------------------------------------#
# ---------------------------------------------------------------------------------------------#
# ---------------------------------------------------------------------------------------------#


def starting_embed(draft):
    embed = interactions.Embed(
        title="{} | {}".format(draft.name, draft.tag),
        fields=[
            interactions.EmbedField(
                name="PLAYERS",
                value="{}".format([p.name for p in draft.players]),
                inline=False,
            )
        ],
        footer=interactions.EmbedFooter(text=draft.description),
    )
    return embed


def ig_embed(name, round, round_end):
    embed = interactions.Embed(
        title=name + " | Round: " + round.title,
        fields=[
            interactions.EmbedField(
                name="GAME",
                value=str(i.players[0])
                + " vs "
                + str(i.players[1])
                + "\n"
                + (
                    "G1:"
                    + i.players[i.gwinners[0]]
                    + "\nG2:"
                    + i.players[i.gwinners[1]]
                    + "\nG3:"
                    + (i.players[i.gwinners[2]] if i.gwinners[2] != None else "NONE")
                    if i.gwinners != []
                    else ""
                ),
            )
            for i in round.matches
        ]
        + [
            interactions.EmbedField(
                name="ROUND TIMER", value="<t:" + round_end.timestamp() + ">"
            )
        ],
    )
    return embed


def end_embed(draft):
    playerlist = "Name | POINTS | GWP | OGP | OMP"
    for i, p in enumerate(draft.players):
        playerlist += p
        playerlist += " | " + p.score
        playerlist += " | " + p.gwp
        playerlist += " | " + p.ogp
        playerlist += " | " + p.omp
        if i < len(draft.players) - 1:
            playerlist += "\n"
    embed = interactions.Embed(
        title=draft.name + " | FINAL",
        fields=[interactions.EmbedField(name="SCORES", value=playerlist)],
    )
    return


# ---------------------------------------------------------------------------------------------#
# ---------------------------------------------------------------------------------------------#
# ---------------------------------------------------------------------------------------------#
# ---------------------------------------------------------------------------------------------#
# ---------------------------------------------------------------------------------------------#


@bot.command(
    name="draft",
    description="Start a draft event.",
    options=[
        interactions.Option(
            type=interactions.OptionType.STRING,
            name="tag",
            description="Choose a tag to organize this draft.",
            required=False,
            choices=[
                interactions.Choice(name="omni", value="Omni's Friday Nights"),
            ],
        ),
        interactions.Option(
            type=interactions.OptionType.STRING,
            name="title",
            description="The name of the draft event.",
            required=False,
        ),
        interactions.Option(
            type=interactions.OptionType.STRING,
            name="description",
            description="Write a description for the draft.",
            required=False,
        ),
    ],
)
async def draft(ctx: interactions.CommandContext, tag, title, description):
    """Begins the draft command sequence."""
    msg = await ctx.send(content="Setting up your draft.")
    drafts[str(msg.id)] = draft_class.Draft(
        draftID=1,
        date=datetime.today().strftime("%Y-%m-%d"),
        host=int(ctx.author.user.id),
        tag=tag,
        description=description,
        name=title,
    )
    drafts[str(msg.id)].add_player(
        p_name=ctx.author.nick
        if ctx.author.nick is not None
        else ctx.author.user.username,
        p_id=int(ctx.author.user.id),
        is_host=True,
    )
    await msg.edit(
        embeds=[starting_embed(drafts[str(msg.id)])],
        components=[button0, button1, button2, button3, button4],
        content="",
    )
    print(drafts[str(msg.id)].players)
    return


# ---------------------------------------------------------------------------------------------#
# ---------------------------------------------------------------------------------------------#
# ---------------------------------------------------------------------------------------------#
# ---------------------------------------------------------------------------------------------#
# ---------------------------------------------------------------------------------------------#


bot.start()
