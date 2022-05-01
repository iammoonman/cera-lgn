import interactions
import draft_class
from datetime import datetime
from datetime import timedelta
import requests
import re

# import logging

# logging.basicConfig(level=logging.DEBUG)

import pickle

with open("token.pickle", "rb") as f:
    token = pickle.load(f)

bot = interactions.Client(token=token)

events = []
drafts = {}
timekeep = {}
bslash = "\n"
guild = 0
with open("guild.pickle", "rb") as f:
    guild = pickle.load(f)


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
"""Join the draft"""


@bot.component(button0)
async def btn0_response(ctx: interactions.ComponentContext):
    """Join the draft"""
    # If draft is inactive, delete the message.
    if str(ctx.message.id) not in drafts.keys():
        await ctx.message.delete()
        return
    print(ctx.message.id, "JOIN")
    drafts[str(ctx.message.id)].add_player(
        ctx.author.nick if ctx.author.nick is not None else ctx.author.user.username,
        int(ctx.author.user.id),
    )
    await ctx.edit(
        embeds=[starting_embed(drafts[str(ctx.message.id)])],
        components=starting_buttons,
    )
    return await ctx.send("Interaction recieved.", ephemeral=True)


# ---------------------------------------------------------------------------------------------#
# ---------------------------------------------------------------------------------------------#

button1 = interactions.Button(
    style=interactions.ButtonStyle.DANGER, label="DROP", custom_id="DROP_PRE"
)
"""Drop from the draft before it begins"""


@bot.component(button1)
async def btn1_response(ctx: interactions.ComponentContext):
    """Drop from the draft before it begins"""
    # If draft is inactive, delete the message.
    if str(ctx.message.id) not in drafts.keys():
        await ctx.message.delete()
        return
    print(ctx.message.id, "DROP_PRE")
    drafts[str(ctx.message.id)].drop_player(int(ctx.author.user.id))
    await ctx.edit(
        embeds=[starting_embed(drafts[str(ctx.message.id)])],
        components=starting_buttons,
    )
    return await ctx.send("Interaction recieved.", ephemeral=True)


# ---------------------------------------------------------------------------------------------#
# ---------------------------------------------------------------------------------------------#


@bot.message_command(name="DROPKICK", scope=guild)
async def dropkick(ctx: interactions.CommandContext):
    """Kick all from the draft"""
    print(ctx.target.id, "DROP_KICK")
    if type(ctx.target) == interactions.Message:
        if str(ctx.target.id) in drafts.keys():
            if int(ctx.author.user.id) == drafts[str(ctx.target.id)].host:
                # 'Draft' object is not iterable
                for p in drafts[str(ctx.target.id)].players:
                    drafts[str(ctx.target.id)].drop_player(int(p.player_id))
                await ctx.target.edit(
                    embeds=[starting_embed(drafts[str(ctx.target.id)])],
                    components=starting_buttons,
                )
    return await ctx.send("Interaction recieved.", ephemeral=True)


# ---------------------------------------------------------------------------------------------#
# ---------------------------------------------------------------------------------------------#


@bot.message_command(name="CANCEL", scope=guild)
async def cancel(ctx: interactions.CommandContext):
    """Cancel the draft"""
    print(ctx.target.id, "CANCEL")
    if type(ctx.target) == interactions.Message:
        if str(ctx.target.id) in drafts.keys():
            if int(ctx.author.user.id) == drafts[str(ctx.target.id)].host:
                del drafts[str(ctx.target.id)]
                await ctx.target.delete()
    return await ctx.send("Interaction recieved.", ephemeral=True)


# ---------------------------------------------------------------------------------------------#
# ---------------------------------------------------------------------------------------------#

button4 = interactions.Button(
    style=interactions.ButtonStyle.SUCCESS, label="BEGIN", custom_id="BEGIN"
)
"""Begin the draft"""


@bot.component(button4)
async def btn4_response(ctx: interactions.ComponentContext):
    """Begin the draft"""
    # If draft is inactive, delete the message.
    if str(ctx.message.id) not in drafts.keys():
        await ctx.message.delete()
        return
    print(ctx.message.id, "BEGIN")
    # Check if the user is the host
    if int(ctx.author.user.id) == drafts[str(ctx.message.id)].host:
        print(ctx.message.id, "SENDING")
        drafts[str(ctx.message.id)].do_pairings()
        timekeep[str(ctx.message.id)] = datetime.now() + timedelta(minutes=50)
        # Edit the message so that it shows the pairings and the score buttons
        await ctx.message.edit(
            embeds=[
                ig_embed(
                    name=drafts[str(ctx.message.id)].name,
                    round=[
                        r for r in drafts[str(ctx.message.id)].rounds if not r.completed
                    ][0],
                    round_end=timekeep[str(ctx.message.id)],
                )
            ],
            components=in_draft_buttons,
        )
    return await ctx.send("Interaction recieved.", ephemeral=True)


# ---------------------------------------------------------------------------------------------#
# ---------------------------------------------------------------------------------------------#

starting_buttons = [button0, button1, button4]
"""Buttons for preparing draft."""


button5 = interactions.Button(
    style=interactions.ButtonStyle.PRIMARY, label="NEXT_ROUND", custom_id="NEXT_ROUND"
)
"""Advance to the next round"""


@bot.component(button5)
async def btn5_response(ctx):
    """Advance to the next round"""
    # If draft is inactive, delete the message.
    if str(ctx.message.id) not in drafts.keys():
        await ctx.message.delete()
        return
    print(ctx.message.id, "NEXT_ROUND")
    # Check if the user is the host
    if int(ctx.author.user.id) == drafts[str(ctx.message.id)].host:
        timekeep[str(ctx.message.id)] = datetime.now() + timedelta(minutes=50)
        # Add a check to see if the third round has been played, then swap to posting the final results and send the json to dm.
        if drafts[str(ctx.message.id)].finish_round():
            roundsearch: list[draft_class.Draft.Round] = [
                r for r in drafts[str(ctx.message.id)].rounds if not r.completed
            ]
            if len(roundsearch) > 0:
                await ctx.edit(
                    embeds=[
                        ig_embed(
                            drafts[str(ctx.message.id)].name,
                            roundsearch[0],
                            round_end=timekeep[str(ctx.message.id)],
                        )
                    ],
                    components=in_draft_buttons,
                )
            else:
                await ctx.edit(
                    embeds=[end_embed(drafts[str(ctx.message.id)])], components=[]
                )
                # Send the json to the owner
                print(drafts[str(ctx.message.id)].tojson())
                # member = interactions.Member(
                #     **await bot.http.get_member(guild_id=id, member_id=ctx.user.id),
                #     _client=bot.http,
                # )
                # await member.send(drafts[str(ctx.message.id)].tojson())
        else:
            await ctx.edit(
                content="Not all results reported.",
                embeds=[
                    ig_embed(
                        drafts[str(ctx.message.id)].name,
                        [
                            r
                            for r in drafts[str(ctx.message.id)].rounds
                            if not r.completed
                        ][0],
                        round_end=timekeep[str(ctx.message.id)],
                    )
                ],
                components=in_draft_buttons,
            )
    return await ctx.send("Interaction recieved.", ephemeral=True)


# ---------------------------------------------------------------------------------------------#
# ---------------------------------------------------------------------------------------------#

select0 = interactions.SelectMenu(
    options=[
        interactions.SelectOption(
            label="you - you", value="0", description="You won both games."
        ),
        interactions.SelectOption(
            label="you - them - you",
            value="1",
            description="You won the first and third games.",
        ),
        interactions.SelectOption(
            label="them - you - you",
            value="2",
            description="You lost the first game, but won overall.",
        ),
        interactions.SelectOption(
            label="them - you - them",
            value="3",
            description="You won the second game, but lost the match.",
        ),
        interactions.SelectOption(
            label="you - them - them",
            value="4",
            description="You won the first game, but lost overall.",
        ),
        interactions.SelectOption(
            label="them - them", value="5", description="You lost both games."
        ),
        interactions.SelectOption(
            label="you - them",
            value="6",
            description="You tied, winning the first game.",
        ),
        interactions.SelectOption(
            label="them - you",
            value="7",
            description="You tied, winning the second game.",
        ),
    ],
    placeholder="Choose the games you won.",
    custom_id="WINSELECT",
    min_values=1,
    max_values=1,
)
"""Select the winners of the author's match"""


@bot.component(select0)
async def sel0_response(ctx: interactions.ComponentContext, choices):
    """Select the winners of the author's match"""
    # If draft is inactive, delete the message.
    if str(ctx.message.id) not in drafts.keys():
        await ctx.message.delete()
        return
    print(ctx.message.id, "WINNINGS")
    drafts[str(ctx.message.id)].parse_match(int(ctx.author.user.id), ctx.data.values[0])
    await ctx.edit(
        embeds=[
            ig_embed(
                drafts[str(ctx.message.id)].name,
                [r for r in drafts[str(ctx.message.id)].rounds if not r.completed][0],
                round_end=timekeep[str(ctx.message.id)],
            )
        ],
        components=in_draft_buttons,
    )
    return await ctx.send("Interaction recieved.", ephemeral=True)


# ---------------------------------------------------------------------------------------------#
# ---------------------------------------------------------------------------------------------#

button6 = interactions.Button(
    style=interactions.ButtonStyle.DANGER, label="DROP", custom_id="DROP_IG"
)
"""Drop from the draft while it is running"""


@bot.component(button6)
async def btn6_response(ctx: interactions.ComponentContext):
    """Drop from the draft while it is running"""
    # If draft is inactive, delete the message.
    if str(ctx.message.id) not in drafts.keys():
        await ctx.message.delete()
        return
    print(ctx.message.id, "DROP_IG")
    try:
        drafts[str(ctx.message.id)].drop_player(int(ctx.author.user.id))
    except IndexError:
        pass
    await ctx.edit(
        embeds=[
            ig_embed(
                drafts[str(ctx.message.id)].name,
                [r for r in drafts[str(ctx.message.id)].rounds if not r.completed][0],
                round_end=timekeep[str(ctx.message.id)],
            )
        ],
        components=in_draft_buttons,
    )
    return await ctx.send("Interaction recieved.", ephemeral=True)


# ---------------------------------------------------------------------------------------------#
# ---------------------------------------------------------------------------------------------#

in_draft_buttons = [
    interactions.ActionRow(components=[button5, button6]),
    interactions.ActionRow(components=[select0]),
]
"""Buttons for round in progress."""

# ---------------------------------------------------------------------------------------------#
# ---------------------------------------------------------------------------------------------#
# ---------------------------------------------------------------------------------------------#
# ---------------------------------------------------------------------------------------------#
# ---------------------------------------------------------------------------------------------#


def starting_embed(draft: draft_class.Draft):
    longtext = [p.name for p in draft.players]
    embed = interactions.Embed(
        title=f"{draft.name} | {draft.tag}",
        fields=[
            interactions.EmbedField(
                name="PLAYERS",
                value=f"{bslash.join(longtext)}",
                inline=False,
            )
        ],
        footer=interactions.EmbedFooter(text=draft.description),
    )
    return embed


def ig_embed(name, round: draft_class.Draft.Round, round_end):
    embed = interactions.Embed(
        title=f"{name} | Round: {round.title}",
        fields=[
            interactions.EmbedField(
                inline=True,
                name=f"GAME: {i.players[0]} vs {i.players[1]}",
                value=f"G1 Winner: {i.players[i.gwinners[0]] if len(i.gwinners) > 0 else 'NONE'}{bslash}"
                + f"G2 Winner: {(i.players[i.gwinners[1]] if i.gwinners[1] is not None else 'NONE') if len(i.gwinners) > 1 else 'NONE'}{bslash}"
                + f"G3 Winner: {(i.players[i.gwinners[2]] if i.gwinners[2] is not None else 'NONE') if len(i.gwinners) > 2 else 'NONE'}",
            )
            for i in round.matches
        ]
        + [
            interactions.EmbedField(
                name="ROUND TIMER",
                value=f"The round ends <t:{int(round_end.timestamp())}:R>.",
            )
        ],
    )
    return embed


def end_embed(draft: draft_class.Draft):
    embed = interactions.Embed(
        title=f"{draft.name} | FINAL",
        description=draft.description,
        fields=[
            interactions.EmbedField(
                inline=True,
                name=f"{p.name}",
                value=f"SCORE: {p.score}{bslash}"
                + f"GWP: {round(p.gwp,2)}{bslash}"
                + f"OGP: {round(p.ogp,2)}{bslash}"
                + f"OMP: {round(p.omp,2)}",
            )
            for p in sorted(
                draft.players,
                key=lambda pl: (pl.score, pl.gwp, pl.ogp, pl.omp),
                reverse=True,
            )
        ],
    )
    return embed


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
            name="title",
            description="The name of the draft event.",
            required=True,
        ),
        interactions.Option(
            type=interactions.OptionType.STRING,
            name="description",
            description="Write a description for the draft.",
            required=True,
        ),
        interactions.Option(
            type=interactions.OptionType.STRING,
            name="tag",
            description="Choose a tag to organize this draft.",
            required=False,
            choices=[
                interactions.Choice(name="omni", value="Omni's Friday Nights"),
                interactions.Choice(name="ptm", value="Prime Time with Moon"),
            ],
        ),
        interactions.Option(
            type=interactions.OptionType.INTEGER,
            name="rounds",
            description="The maximum number of rounds for the draft. Default is 3.",
            min_value=1,
            max_value=5,
            required=False,
        ),
    ],
    scope=guild,
)
async def draft(ctx: interactions.CommandContext, title, description, tag="", rounds=3):
    """Begins the draft command sequence."""
    msg = await ctx.send(content="Setting up your draft.")
    print(msg.id, "DRAFT")
    drafts[str(msg.id)] = draft_class.Draft(
        draftID=1,
        date=datetime.today().strftime("%Y-%m-%d"),
        host=int(ctx.author.user.id),
        tag=tag,
        description=description,
        name=title,
        max_rounds=rounds,
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
        components=starting_buttons,
        content="",
    )
    return await ctx.send("Interaction recieved.", ephemeral=True)


# ---------------------------------------------------------------------------------------------#
# ---------------------------------------------------------------------------------------------#
# ---------------------------------------------------------------------------------------------#
# ---------------------------------------------------------------------------------------------#
# ---------------------------------------------------------------------------------------------#


bot.start()
