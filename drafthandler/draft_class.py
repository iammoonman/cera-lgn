class Draft:
    def __init__(
        self,
        draftID: int,
        date: str,
        host: int,
        tag: str,
        description: str,
        name: str,
        max_rounds: int = 3,
    ):
        self.draftID = draftID
        self.date = date
        self.host = host
        self.tag = tag
        self.description = description
        self.name = name
        self.players = []
        self.rounds = []
        self.max_rounds = max_rounds

    def tojson(self):
        """Calculates the final scores of the draft and returns a JSON."""
        self.calculate()
        draftobj = {
            "draftID": self.draftID,
            "tag": self.tag,
            "date": self.date,
            "title": self.name,
            "rounds": [
                {
                    "roundNUM": i.title,
                    "complete": i.completed,
                    "matches": [
                        {
                            "players": [u.player_id for u in q.players],
                            "winners": q.gwinners,
                            "drops": q.drops,
                        }
                        for q in i.matches
                    ],
                }
                for i in self.rounds
            ],
            "players": [
                {
                    "playerID": i.player_id,
                    "score": i.score,
                    "gwp": round(i.gwp, 2),
                    "ogp": round(i.ogp, 2),
                    "omp": round(i.omp, 2),
                }
                for i in self.players
            ],
        }
        return draftobj

    class Player:
        def __init__(self, n, id):
            self.player_id = id
            self.name = n
            self.score = 0
            """Final match score. 3 for wins and byes, 1 for tie, 0 for loss."""
            self.gpts = 0
            """Games won. Does not increment for byes."""
            self.mpts = 0
            """Match points. Similar to score."""
            self.gcount = 0
            """Total games played. Does not increment for byes."""
            self.mcount = 0
            """Total matches played. *Does* increment with byes."""
            self.opponents = []
            self.dropped = False
            self.ogp = None
            self.omp = None
            self.gwp = None
            self.mwp = None

        def __lt__(self, other):
            if self.score != other.score:
                return self.score < other.score
            elif self.gpts != other.gpts:
                return self.gpts < other.gpts
            else:
                return self.name < other.name

        def __repr__(self):
            return self.name + " (" + str(self.score) + ")"

        def __eq__(self, other):
            return self.player_id == other.player_id

    class Round:
        def __init__(self, title):
            self.completed = False
            self.matches = []
            self.title = title

        class Match:
            def __init__(self, p=[]):
                self.players = p
                self.gwinners = []
                self.drops = [False for i in p]
                if p[1] == Draft.Player("Bye", "-1"):
                    self.gwinners = [0, 0, None]

    def do_pairings(self):
        """Generates a new round based on the scores of the previous round. DO NOT CALL BY ITSELF."""
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
        self.players.sort()
        temp_players = [y for y in self.players if not y.dropped]
        while temp_players:
            player1 = temp_players.pop(0)
            try:
                player2 = [i for i in temp_players if i not in player1.opponents and abs(i.score - player1.score) <= 3][
                    0
                ]
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
        new_round = Draft.Round(title=len(self.rounds) + 1)
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
                self.do_pairings()
            else:
                self.calculate()
            return True

    def drop_player(self, p_id):
        """Toggles the drop status of a player. Can be called mid-draft. Does not finalize their drop."""
        # Does not allow the host to drop.
        if self.host == p_id:
            return
        # If there are no rounds, delete player
        if len(self.rounds) == 0:
            hold = None
            for q in self.players:
                if q.player_id == p_id:
                    hold = q
                    break
            self.players.remove(hold)
        else:
            # If there are rounds, go into their latest match and toggle their index in drops
            player = [p for p in self.players if p.player_id == p_id][0]
            round = [r for r in self.rounds if r.completed == False][0]
            match = [m for m in round.matches if player in m.players][0]
            match.drops[match.players.index(player)] = not match.drops[match.players.index(player)]
        return

    def add_player(self, p_name, p_id, is_host=False):
        """Adds a player to the draft. Can't be called mid-draft."""
        if len(self.rounds) > 0:
            return
        p = Draft.Player(n=p_name, id=p_id)
        if p not in self.players:
            self.players.append(p)
        return

    def calculate(self):
        for player in self.players:
            player.gwp = player.gpts / (player.gcount if player.gcount > 0 else 1)
            player.mwp = player.mpts / ((player.mcount * 3) if player.mcount > 0 else 1)
            print(player.player_id, player.gpts, player.gcount, player.mpts, player.mcount)
        for player in self.players:
            player.ogp = sum(h := [p.gwp for p in player.opponents]) / (len(h) if len(h) > 0 else 1)
            player.omp = sum(j := [p.mwp for p in player.opponents]) / (len(j) if len(j) > 0 else 1)
        return


# dr = Draft(1, "TODAY", "ME", "TAG", "NOPE", "THE")
# dr.add_player("A", "1")
# dr.add_player("B", "2", True)
# dr.add_player("C", "3")
# dr.add_player("D", "4")
# dr.do_pairings()
# dr.parse_match("1", "0")
# dr.parse_match("3", "1")
# if dr.finish_round():
#     print("n4", dr.rounds)
# else:
#     print("NOT DONE")
# dr.parse_match("1", "0")
# dr.parse_match("2", "1")
# if dr.finish_round():
#     print("n4", dr.rounds)
# else:
#     print("NOT DONE")
# dr.parse_match("1", "0")
# dr.parse_match("2", "1")
# if dr.finish_round():
#     print("n4", dr.rounds)
# else:
#     print("NOT DONE")
# import json

# print(json.dumps(dr.tojson()))
# THE ORDER IS:
# add_players
# if finish_round, then continue
# remember: FINISH_ROUND  CALLS  DO_PAIRINGS
