import math
import random
from typing import Union


class Draft:
    """Represents a single event of a Swiss-system tournament."""

    def __init__(
        self,
        draftID: str,
        date: str,
        host: str,
        tag: str,
        description: str,
        title: str,
        max_rounds: int = 3,
    ):
        self.draftID: str = draftID
        """Unique ID."""
        self.date: str = date
        """Translates to the output JSON."""
        self.host: str = host
        """The Discord user ID of the host."""
        self.tag: str = tag
        """Three-character code for the category."""
        self.description: str = description
        self.title: str = title
        self.players: list[Player] = []
        self.rounds: list[Round] = []
        self.max_rounds: int = max_rounds

    def get_player_by_id(self, id: str):
        return next(player for player in self.players if player.player_id == id)

    def get_player_by_seat(self, seat: int):
        return next(filter(lambda x: x.seat == seat, self.players))

    def tojson(self):
        """Calculates the final scores of the draft and returns a JSON."""
        self.calculate()
        draftobj = {
            "id": self.draftID,
            "tag": self.tag,
            "date": self.date,
            "description": self.description,
            "title": self.title,
            "rounds": [
                {
                    "title": i.title,
                    "matches": [
                        {
                            "p_ids": [u.player_id if u.player_id != "-1" else "BYE" for u in q.players],
                            "games": [(x if x is not None else "TIE") for x in q.gwinners]
                            if "-1" not in [p.player_id for p in q.players]
                            else [],
                            "drops": {k: v for (k, v) in q.drops.items() if k != "-1"},
                            # "bye": "-1" in [p.player_id for p in q.players],
                        }
                        for q in i.matches
                    ],
                }
                for i in self.rounds
            ],
            "scores": {
                i.player_id: {
                    "id": i.player_id,
                    "points": i.score,
                    "gwp": f"{i.gwp:.2f}",
                    "ogp": f"{i.ogp:.2f}",
                    "omp": f"{i.omp:.2f}",
                }
                for i in self.players
            },
        }
        return draftobj

    def rotation_pairings(self):
        player_opponents = {}
        leng = len(self.players)
        players_sorted = [p for p in self.players if not p.dropped]
        players_sorted.sort(key=lambda p: (p.score, p.gpts), reverse=True)
        for first_player in players_sorted:
            # Players have a hierarchy of who they want to play against.
            # It starts with the player with the highest distance from them.
            # Continues with half that distance away from each of those two players.
            # Then half again away from the player and their first opponent.
            halfway_around = (first_player.seat + math.ceil(leng / 2)) % leng
            indices = [halfway_around]
            for div in [2, 4, 8, 16, 32]:
                indices.append((halfway_around + math.ceil(leng / div)) % leng)
                indices.append((halfway_around - math.floor(leng / div)) % leng)
                indices.append((first_player.seat + math.ceil(leng / div)) % leng)
                indices.append((first_player.seat - math.floor(leng / div)) % leng)
            player_opponents[first_player.player_id] = [
                self.get_player_by_seat(x)
                for x in [i for n, i in enumerate(indices) if i not in indices[:n] and i != 0]
            ]
        sorted_players = [y for y in self.players if not y.dropped]
        sorted_players.sort(key=lambda p: (p.score, p.gpts), reverse=True)
        pairs: list[list[Player]] = []
        while sorted_players:
            is_paired = False
            player = sorted_players.pop(0)
            sorted_opps = player_opponents[player.player_id]
            sorted_opps.sort(key=lambda p: (p.score, p.gpts), reverse=True)
            for opp in [x for x in sorted_opps if x in sorted_players]:
                if opp in player.opponents:
                    continue
                pairs.append([player, opp])
                is_paired = True
                sorted_players.remove(opp)
                player.opponents.append(opp)
                break
            if not is_paired:
                pairs.append([player, Player("BYE", "-1")])
        new_round = Round(title=f"{len(self.rounds) + 1}")
        new_round.matches = [Match(p=i) for i in pairs]
        self.rounds.append(new_round)
        return new_round

    def parse_match(self, p_id, result_code):
        """Parses a match result report from a player.

        "0" => player won both of their games

        "1" => player won game 1 and game 3

        "2" => player won game 2 and game 3

        "3" => player won game 2 and lost

        "4" => player won game 1 and lost

        "5" => player didnt win any games

        "6" => it was a tie, with the player winning first

        "7" => it was a tie, with the opponent winning first

        "8" => opponent won game 1 and game 2 didn't happen

        "9" => player won game 1 and game 2 didn't happen

        "-1" => player's opponent dropped late"""
        # Get the current round
        # Get p_id's match
        # Parse code into gwinners
        # DONT push results into outer player objects yet
        round = [r for r in self.rounds if r.completed == False][0]
        for match in [m for m in round.matches if p_id in [x.player_id for x in m.players]]:
            o_id = [x.player_id for x in match.players if x.player_id != p_id][0]
            # result codes
            if result_code == "0":
                match.gwinners = [p_id, p_id]
            elif result_code == "1":
                match.gwinners = [p_id, o_id, p_id]
            elif result_code == "2":
                match.gwinners = [o_id, p_id, p_id]
            elif result_code == "3":
                match.gwinners = [o_id, p_id, o_id]
            elif result_code == "4":
                match.gwinners = [p_id, o_id, o_id]
            elif result_code == "5":
                match.gwinners = [o_id, o_id]
            elif result_code == "6":
                match.gwinners = [p_id, o_id]
            elif result_code == "7":
                match.gwinners = [o_id, p_id]
            elif result_code == "8":
                match.gwinners = [o_id]
            elif result_code == "9":
                match.gwinners = [p_id]
            elif result_code == "-1" and match.drops[o_id] == True:
                self.get_player_by_id(o_id).dropped = True
                match.players = [p_id, Player("Bye", "-1")]
                match.gwinners = [p_id, p_id]
        return

    # def parse_match_list(self, p_id, result):
    #     """Parses a match result report from a player. Uses a list of player ids to reference game results, with None as a tie."""
    #     player = [p for p in self.players if p.player_id == p_id][0]
    #     round = [r for r in self.rounds if r.completed == False][0]
    #     for match in [m for m in round.matches if player in m.players]:
    #         if match.players.index(player) == 0:
    #             p_index = 0
    #             o_index = 1
    #         else:
    #             p_index = 1
    #             o_index = 0
    #         # result = [p_id,o_id,None]
    #         self.gwinners = [(p_index if i == p_id else o_index) if i is not None else None for i in result]
    #     return

    def finish_round(self):
        """Checks and completes a round in preparation of ending the event or starting a new round."""
        # Get round that isn't completed
        # Check that all games are reported
        # If so, parse scores into player list
        # Parse drops into player list
        # Toggle completed
        # do_pairings
        incomplete_rounds = [r for r in self.rounds if not r.completed]
        if len(incomplete_rounds) != 0 and len(self.rounds) != 0:
            next_incomplete_round = incomplete_rounds[0]
            for match in next_incomplete_round.matches:
                if match.gwinners == []:
                    return False
            for match in next_incomplete_round.matches:
                wasTie = len(set(match.gwinners)) == len(match.gwinners)
                wasBye = "-1" in [o.player_id for o in match.players]
                for player in match.players:
                    if (
                        player.player_id == "-1"
                    ):  # Catch fake bye player. Might not be needed, since they aren't in the players list.
                        continue
                    if wasBye:
                        player.score += 3
                        player.mcount += 1
                        player.gcount += 0
                        player.mpts += 3
                        player.gpts += 0
                        player.dropped = match.drops[player.player_id]
                        continue
                    if wasTie:
                        player.score += 1
                        player.mcount += 1
                        player.gcount += len([i for i in match.gwinners if i is not None])
                        player.mpts += 1
                        player.gpts += len([i for i in match.gwinners if i == player.player_id])
                        player.dropped = match.drops[player.player_id]
                    else:
                        won = len([i for i in match.gwinners if i == player.player_id]) > len(
                            [i for i in match.gwinners if i != player.player_id]
                        )
                        player.score += 3 if won else 0
                        player.mcount += 1
                        player.gcount += len([i for i in match.gwinners if i is not None])
                        player.mpts += 3 if won else 0
                        player.gpts += len([i for i in match.gwinners if i == player.player_id])
                        player.dropped = match.drops[player.player_id]
            next_incomplete_round.completed = True
            # Check if it's the max number of rounds
            # Check if it's impossible to make pairings <- may want to just forget about this, easier to force pairings
            # If either of those: somehow signal that the draft is over, dont make pairings
            if len(self.rounds) < self.max_rounds:
                # self.blossom_pairings()
                self.rotation_pairings()
            return True
        else:
            # Beginning the draft.
            self.rotation_pairings()
            return True

    def drop_player(self, p_id):
        """Toggles the drop status of a player. Can be called mid-draft. Does not finalize their drop."""
        # Does not allow the host to drop.
        if self.host == p_id:
            return
        if p_id not in [p.player_id for p in self.players]:
            return
        # If there are no rounds, delete player
        if len(self.rounds) == 0:
            hold = None
            for q in self.players:
                if q.player_id == p_id:
                    hold = q
                    break
            self.players.remove(hold)  # type: ignore
            # Adjust other player's seating
            for i, q in enumerate(self.players):
                q.seat = i
        else:
            # If there are rounds, go into their latest match and toggle their index in drops
            player = [p for p in self.players if p.player_id == p_id][0]
            round = [r for r in self.rounds if r.completed == False][0]
            match = [m for m in round.matches if player in m.players][0]
            match.drops[player.player_id] = not match.drops[player.player_id]
        return

    def add_player(self, p_name, p_id, seat=0, is_host=False):
        """Adds a player to the draft. Can't be called mid-draft."""
        if len(self.rounds) > 0:
            return
        p = Player(n=p_name, id=p_id, s=seat)
        if p not in self.players:
            self.players.append(p)
        return

    def calculate(self):
        for player in self.players:
            player.gwp = player.gpts / (player.gcount if player.gcount > 0 else 1)
            player.mwp = player.mpts / ((player.mcount * 3) if player.mcount > 0 else 1)
        for player in self.players:
            player.ogp = sum(h := [p.gwp if p.gwp is not None else 0 for p in player.opponents]) / (
                len(h) if len(h) > 0 else 1
            )
            player.omp = sum(j := [p.mwp if p.mwp is not None else 0 for p in player.opponents]) / (
                len(j) if len(j) > 0 else 1
            )
        return


class Round:
    """One round from the event."""

    def __init__(self, title: str):
        self.completed: bool = False
        self.matches: list[Match] = []
        self.title: str = title
        """Used if the round has a custom title."""


class Player:
    def __init__(self, n: str, id: str, s: int = 0, s_c = "chair_white"):
        self.player_id: str = id
        """Discord user ID for the player."""
        self.seat: int = s
        """Players should prefer to play against those farthest from them in the draft seating arrangement."""
        self.name: str = n
        """Used for quick access. Not output to JSON."""
        self.score: int = 0
        """Final score. 3 for wins and byes, 1 for tie, 0 for loss."""
        self.gpts: int = 0
        """Games won. Does not increment for byes."""
        self.mpts: int = 0
        """Match points. Similar to score."""
        self.gcount: int = 0
        """Total games played. Does not increment for byes."""
        self.mcount: int = 0
        """Total matches played. *Does* increment with byes."""
        self.opponents: list[Player] = []
        """Used for quick access. Not output to JSON."""
        self.dropped: bool = False
        """Global participation status. Locked in at the end of the round."""
        self.ogp: Union[float, None] = None
        """Opponent Game-Win Percentage"""
        self.omp: Union[float, None] = None
        """Opponent Match-Win Percentage"""
        self.gwp: Union[float, None] = None
        """Game-Win Percentage"""
        self.mwp: Union[float, None] = None
        """Match-Win Percentage
            
            Not output to JSON."""
        self.seat_color: str = s_c
        """Seat color. Used for initial seating from TTS."""

    def __lt__(self, other):
        if self.score == other.score:
            if self.gpts == other.gpts:
                return random.random() > 0.5
            return self.gpts < other.gpts
        return self.score < other.score

    def __repr__(self):
        return f"{self.name} ({self.score})"

    def __eq__(self, other):
        return self.player_id == other.player_id


class Match:
    """One match from the round."""

    def __init__(self, p: list[Player] = []):
        if len(p) == 0:
            raise ValueError
        self.players: list[Player] = p
        self.gwinners: list[Union[str, None]] = []
        """A list of either the player's ID or None, representing the game won by that player or not played."""
        if p[1] == Player("Bye", "-1"):
            # Automatically set score for the bye.
            self.gwinners = [self.players[0].player_id, self.players[0].player_id, None]
        self.drops = {f"{j.player_id}": False for j in p}
