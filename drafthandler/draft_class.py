import random
from typing import TypeVar, Literal, Union
import networkx as nx


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
        self.players: list[Draft.Player] = []
        self.rounds: list[Draft.Round] = []
        self.max_rounds: int = max_rounds

    def get_player_by_id(self, id: str):
        return next(player for player in self.players if player.player_id == id)

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
                            "p_ids": [u.player_id for u in q.players],
                            "games": {
                                f"{i}": (q.players[x].player_id if x is not None else "TIE")
                                for i, x in enumerate(q.gwinners)
                            },
                            "drops": ([q.players[0].player_id] if q.drops[0] else [])
                            + ([q.players[1].player_id] if q.drops[1] else []),
                            "bye": False,
                        }
                        for q in i.matches
                    ],
                }
                for i in self.rounds
            ],
            "scores": [
                {
                    "id": i.player_id,
                    "points": i.score,
                    "gwp": f"{i.gwp:.2f}",
                    "ogp": f"{i.ogp:.2f}",
                    "omp": f"{i.omp:.2f}",
                }
                for i in self.players
            ],
        }
        return draftobj

    class Player:
        def __init__(self, n: str, id: str, s: int = 0):
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
            self.opponents: list[Draft.Player] = []
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

    class Round:
        """One round from the event."""

        def __init__(self, title: str):
            self.completed: bool = False
            self.matches: list[Draft.Round.Match] = []
            self.title: str = title
            """Used if the round has a custom title."""

        class Match:
            """One match from the round."""

            def __init__(self, p=[]):
                self.players = p
                self.gwinners: list[Union[int, None]] = []
                if p[1] == Draft.Player("Bye", "-1"):
                    # Automatically set score for the bye.
                    self.gwinners = [0, 0, None]
                self.drops = [False for i in p]

    def rotation_pairings(self):
        # For each remaining player
        for p in [y for y in self.players if not y.dropped]:
            #  make a queuestack list
            queuestack = []
            #  For each total players, but start halfway around the list, picking every other player
            for q in [
                *[y for y in self.players if not y.dropped][::2],
                *[y for y in self.players if not y.dropped][1::2],
            ]:
                #   If player is dropped, skip
                #   If player in opponents, skip
                #   If player has equal score, put at front
                #   If player has less score, put at back
                if q == p:
                    continue
                elif q in p.opponents:
                    continue
                elif p.score == q.score:
                    queuestack = [q] + queuestack
                else:
                    queuestack += [q]
            queuestack = queuestack + p.opponents
            print(p, queuestack)
        return

    def minweight_naive_pairings(self):
        # For each remaining player, define a matrix of weights for their pair against the other players
        # If the players have met, weight is 1000000.
        # Start with the player with the highest weight. Choose their least weighted player and pair off.
        playerWeights: list[tuple[Draft.Player, list[Union[tuple[int, Draft.Player], tuple[float, Draft.Player]]]]] = []
        for p in [y for y in self.players if not y.dropped]:
            # Distance between seats; more => more likely pairing
            # Difference between scores; less => more likely pairing
            half = len(self.players) / 2
            localw = [
                (
                    (10000, z)
                    if p in z.opponents
                    else (abs(z.score - p.score) + abs(half - abs(z.seat - p.seat)) / half, z)
                )
                for z in self.players
                if not z.dropped and z != p
            ]
            playerWeights.append((p, localw))
        pairs: list[list[Draft.Player]] = []
        while playerWeights:
            # Pair max weight players first to heuristically avoid byes
            playerWeights.sort(reverse=True, key=lambda x: sum([g[0] for g in x[1]]))
            highestWeightPlayer = playerWeights.pop()
            length = len(playerWeights)
            if length > 0:
                highestWeightPlayer[1].sort(key=lambda n: n[0])
                for lowestWeightedOpponentTuple in highestWeightPlayer[1]:
                    if lowestWeightedOpponentTuple[1] in [item for sublist in pairs for item in sublist]:
                        continue
                    pairs.append([highestWeightPlayer[0], lowestWeightedOpponentTuple[1]])
                    playerWeights = [o for o in playerWeights if o[0] != lowestWeightedOpponentTuple]
                    break
                if len(playerWeights) == length:
                    # No viable other player, give a bye.
                    pairs.append([highestWeightPlayer[0], Draft.Player("BYE", "-1")])
            else:
                # BYE
                pairs.append([highestWeightPlayer[0], Draft.Player("BYE", "-1")])
        new_round = Draft.Round(title=f"{len(self.rounds) + 1}")
        new_round.matches = [new_round.Match(p=i) for i in pairs]
        self.rounds.append(new_round)
        return new_round

    def blossom_pairings(self):
        G = nx.Graph()
        for p in [y for y in self.players if not y.dropped]:
            for q in [y for y in self.players if not y.dropped]:
                # Distance between seats; more => more likely pairing
                # Difference between scores; less => more likely pairing
                num_p = len(self.players) / 2
                G.add_edge(
                    p.player_id,
                    q.player_id,
                    weight=-10000
                    if q in p.opponents
                    else (-abs(p.score - q.score) - (abs(num_p - abs(p.seat - q.seat)) / num_p)),
                )
        pairs = []
        unused = [y.player_id for y in self.players if not y.dropped]
        for p in nx.max_weight_matching(G, maxcardinality=True):
            unused.remove(p[0])
            unused.remove(p[1])
            pairs.append([self.get_player_by_id(p[0]), self.get_player_by_id(p[1])])
        for x in unused:
            pairs.append([self.get_player_by_id(x), Draft.Player("BYE", "-1")])
        new_round = Draft.Round(title=f"{len(self.rounds) + 1}")
        new_round.matches = [new_round.Match(p=i) for i in pairs]
        self.rounds.append(new_round)
        self.rotation_pairings()
        return new_round

    def do_pairings(self):
        """Generates a new round based on the scores of the previous round. DO NOT CALL without checking for completeness."""
        # Make a temp list of players and pairings
        # Sort the list of players by score.
        # For each player, get the next player who:
        #  Isn't in that player's opponents list
        #  Is within 3 points of this player's score
        #  Has not dropped
        # Set up that pairing in the temp list
        # If it fails to find, restart, but then start with that player.
        # NOT SURE if it will fail to find *and* still have a possible correct pairing set.
        temp_pairings = []
        temp_players = [y for y in self.players if not y.dropped]
        temp_players.sort()
        while temp_players:
            player1 = temp_players.pop(0)
            try:
                player2 = [i for i in temp_players if i not in player1.opponents][0]
            except IndexError:
                # Checking it like this will cause more than one bye in certain situations with people dropping.
                # That is OK
                player2 = Draft.Player("BYE", "-1")
                # Recommended to just pick someone. In a weird niche situation, ignore the point restriction.
                if player1.score == max([u.score for u in self.players]):
                    try:
                        player2 = [i for i in temp_players if i not in player1.opponents][0]
                    except IndexError:
                        player2 = Draft.Player("BYE", "-1")
            temp_pairings.append([player1, player2])
            if player2.player_id != "-1":
                temp_players.remove(player2)
                player1.opponents.append(player2)
                player2.opponents.append(player1)
        new_round = Draft.Round(title=f"{len(self.rounds) + 1}")
        new_round.matches = [new_round.Match(p=i) for i in temp_pairings]
        self.rounds.append(new_round)
        return new_round

    def parse_match(self, p_id, result_code):
        """Parses a match result report from a player. Uses numbered codes 0-9 to discern result."""
        # Get the current round
        # Get p_id's match
        # Parse code into gwinners
        # DONT push results into outer player objects yet
        player = [p for p in self.players if p.player_id == p_id][0]
        round = [r for r in self.rounds if r.completed == False][0]
        for match in [m for m in round.matches if player in m.players]:
            if match.players.index(player) == 0:
                p_index = 0
                o_index = 1
            else:
                p_index = 1
                o_index = 0
            # result codes
            # 0 means the player won both of their games
            # 1 means the player won game 1 and game 3
            # 2 means the player won game 2 and game 3
            # 3 means the player won game 2
            # 4 means the player won game 1
            # 5 means the player didnt win any games
            # 6 means it was a tie, with the player winning first
            # 7 means it was a tie, with the opponent winning first
            # 8 means the opponent won game 1 and game 2 didn't happen
            # 9 means the player won game 1 and game 2 didn't happen
            # -1 means the player's opponent dropped late
            if result_code == "0":
                match.gwinners = [p_index, p_index, None]
            elif result_code == "1":
                match.gwinners = [p_index, o_index, p_index]
            elif result_code == "2":
                match.gwinners = [o_index, p_index, p_index]
            elif result_code == "3":
                match.gwinners = [o_index, p_index, o_index]
            elif result_code == "4":
                match.gwinners = [p_index, o_index, o_index]
            elif result_code == "5":
                match.gwinners = [o_index, o_index, None]
            elif result_code == "6":
                match.gwinners = [p_index, o_index, None]
            elif result_code == "7":
                match.gwinners = [o_index, p_index, None]
            elif result_code == "8":
                match.gwinners = [o_index, None, None]
            elif result_code == "9":
                match.gwinners = [p_index, None, None]
            elif result_code == "-1" and match.drops[o_index] == True:
                match.players[o_index].dropped = True
                match.players[o_index] = Draft.Player("Bye", "-1")
                match.gwinners = [p_index, p_index, None]
        return

    def parse_match_list(self, p_id, result):
        """Parses a match result report from a player. Uses a list of player ids to reference game results, with None as a tie."""
        player = [p for p in self.players if p.player_id == p_id][0]
        round = [r for r in self.rounds if r.completed == False][0]
        for match in [m for m in round.matches if player in m.players]:
            if match.players.index(player) == 0:
                p_index = 0
                o_index = 1
            else:
                p_index = 1
                o_index = 0
            # result = [p_id,o_id,None]
            self.gwinners = [(p_index if i == p_id else o_index) if i is not None else None for i in result]
        return

    def finish_round(self):
        """Checks and completes a round in preparation of ending the event or starting a new round."""
        # Get round that isn't completed
        # Check that all games are reported
        # If so, parse scores into player list
        # Parse drops into player list
        # Toggle completed
        # do_pairings
        round = [r for r in self.rounds if not r.completed][0]
        if round:
            for match in round.matches:
                if match.gwinners == []:
                    return False
            for match in round.matches:
                wasTie = len(set(match.gwinners)) == len(match.gwinners)
                wasBye = "-1" in [o.player_id for o in match.players]
                for ind, player in enumerate(match.players):
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
                        player.dropped = match.drops[ind]
                        continue
                    if wasTie:
                        player.score += 1
                        player.mcount += 1
                        player.gcount += len([i for i in match.gwinners if i is not None])
                        player.mpts += 1
                        player.gpts += len([i for i in match.gwinners if i == ind])
                        player.dropped = match.drops[ind]
                    else:
                        won = len([i for i in match.gwinners if i == ind]) > len(
                            [i for i in match.gwinners if i != ind]
                        )
                        player.score += 3 if won else 0
                        player.mcount += 1
                        player.gcount += len([i for i in match.gwinners if i is not None])
                        player.mpts += 3 if won else 0
                        player.gpts += len([i for i in match.gwinners if i == ind])
                        player.dropped = match.drops[ind]
            round.completed = True
            # Check if it's the max number of rounds
            # Check if it's impossible to make pairings <- may want to just forget about this, easier to force pairings
            # If either of those: somehow signal that the draft is over, dont make pairings
            if len(self.rounds) != self.max_rounds:
                self.blossom_pairings()
            else:
                self.calculate()
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
            seat = 0
            for q in self.players:
                if q.player_id == p_id:
                    hold = q
                    seat = q.seat
                    break
            self.players.remove(hold)  # type: ignore
            # Adjust other player's seating
            for q in self.players:
                if q.seat > seat:
                    q.seat -= 1
        else:
            # If there are rounds, go into their latest match and toggle their index in drops
            player = [p for p in self.players if p.player_id == p_id][0]
            round = [r for r in self.rounds if r.completed == False][0]
            match = [m for m in round.matches if player in m.players][0]
            match.drops[match.players.index(player)] = not match.drops[match.players.index(player)]
        return

    def add_player(self, p_name, p_id, seat=0, is_host=False):
        """Adds a player to the draft. Can't be called mid-draft."""
        if len(self.rounds) > 0:
            return
        p = Draft.Player(n=p_name, id=p_id, s=seat)
        if p not in self.players:
            self.players.append(p)
        return

    def calculate(self):
        for player in self.players:
            player.gwp = player.gpts / (player.gcount if player.gcount > 0 else 1)
            player.mwp = player.mpts / ((player.mcount * 3) if player.mcount > 0 else 1)
            # print(player.player_id, player.gpts, player.gcount, player.mpts, player.mcount)
        for player in self.players:
            player.ogp = sum(h := [p.gwp if p.gwp is not None else 0 for p in player.opponents]) / (
                len(h) if len(h) > 0 else 1
            )
            player.omp = sum(j := [p.mwp if p.mwp is not None else 0 for p in player.opponents]) / (
                len(j) if len(j) > 0 else 1
            )
        return
