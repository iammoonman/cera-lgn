def is_pow(n):
    if n % 2 == 1:
        return False
    r = n
    while r > 1:
        r = r / 2
    return r == 1


class T:
    bracket_id = 0
    """Each node has a unique id within this tournament."""

    def __init__(self):
        self.eventID = "0"
        self.tag = ""
        self.date = ""
        self.title = ""
        self.players: list[T.P] = []
        self.nodes: list[T.N] = []
        return

    def calcRanks(self):
        # Sort nodes by round then is_loser
        # For node:
        #  For player in node, sorted winner then loser:
        #   If player not in rank list:
        #    Push to rank list with round num
        # For player in rank list:
        #  rank = len(players with greater round num) + 1
        rankedlist = []
        nds = self.nodes[:]
        nds.sort(key=lambda x: (x.round, x.loser), reverse=True)
        for n in nds:
            for player in n.match.getWinnerLoser():
                if player not in rankedlist:
                    player.lastround = n.round
                    rankedlist.append(player)
        for p in rankedlist:
            p.rank = len([q for q in rankedlist if q.lastround > p.lastround]) + 1
        return

    def addPlayer(self, P):
        self.players.append(P)

    def __json__(self):
        return {
            "eventID": self.eventID,
            "tag": self.tag,
            "date": self.date,
            "title": self.title,
            "players": [
                {
                    "playerID": p.id,
                    "rank": p.rank,
                    "wins": sum(
                        [
                            1
                            # if n.match.scores[n.match.players.index(p)]
                            # == max(n.match.scores)
                            # and min(n.match.scores) != max(n.match.scores)
                            # else 0
                            for n in self.nodes
                            if p in n.match.players
                        ]
                    ),
                    "losses": sum(
                        [
                            1
                            # if n.match.scores[n.match.players.index(p)]
                            # < max(n.match.scores)
                            # else 0
                            for n in self.nodes
                            if p in n.match.players
                        ]
                    ),
                }  # Remember to iterate through each bracket if able.
                for p in self.players
            ],
            "nodes": [b.__json__() for b in self.nodes],
        }

    def buildBracket(self):
        """Builds the nodes needed to form a bracket out of the player list."""
        tempnodes: list[T.N] = []
        # Change this to finding the min and max seed instead
        # Help the top player get the bye by removing them at the beginning
        # Also break the players down into is_pow()
        # Works well when the number of players is just over a power of two,
        # but terribly when its just under a power of two.
        # Gives the top player a bye and puts every other
        # player into a match with the next closest seed.
        # Not exactly sure how to solve.
        feeders = []
        tempplayers = self.players[:]
        tempplayers.sort(key=lambda n: n.seed, reverse=True)
        while not is_pow(len(tempplayers) + len(feeders)):
            p1 = tempplayers.pop()
            p2 = tempplayers.pop()
            feeders.append(T.N(p1=p1, p2=p2, r=-1, maxSeed=max(p1.seed, p2.seed)))
        self.nodes += feeders
        print(len(self.nodes))
        tempplayers += feeders
        tempplayers.sort(key=lambda x: x.seed if type(x) == T.P else x.max_seed)
        while len(tempplayers) > 0:
            maxplayer = tempplayers.pop()
            minplayer = tempplayers.pop(0)
            holdnode = T.N(
                p1=maxplayer if type(maxplayer) == T.P else None,
                p2=minplayer if type(minplayer) == T.P else None,
                r=0,
                maxSeed=max(
                    maxplayer.seed if type(maxplayer) == T.P else maxplayer.max_seed,
                    minplayer.seed if type(minplayer) == T.P else minplayer.max_seed,
                ),
            )
            tempnodes.append(holdnode)
            if type(maxplayer) == T.N:
                maxplayer.feeds.append(holdnode.bnid)
            if type(minplayer) == T.N:
                minplayer.feeds.append(holdnode.bnid)
        for t in tempnodes:
            self.nodes.append(t)
        print(len(self.nodes))
        # Trying to give byes properly
        # Each round must have a 2^n matches
        # While there arent 2^n matches in tempnodes + len(playoffs):
        #  Pair off a match from tempnodes, add it to playoffs
        # Then, readd the playoffs to the tempnodes
        ror = 1
        while True:
            tempnodes2 = tempnodes[:]
            if len(tempnodes2) > 1:
                # Find the highest max_seed
                # Pair it with the lowest max_seed
                # pop both

                # Make sure the top seed has the bye if able
                # If tempnodes2 is odd,
                #  check the holding var
                #  if its none, put the top seed into the var
                #  else, put the holding var into tempnodes2

                tempnodes2.sort(key=lambda n: n.max_seed)
                while len(tempnodes2) > 0:
                    maxnode: T.N = tempnodes2.pop()
                    minnode: T.N = tempnodes2.pop(0)
                    nd = T.N(
                        r=ror,
                        maxSeed=max(
                            [
                                maxnode.max_seed,
                                minnode.max_seed,
                            ]
                        ),
                    )
                    maxnode.feeds.append(nd.bnid)
                    tempnodes.remove(maxnode)
                    minnode.feeds.append(nd.bnid)
                    tempnodes.remove(minnode)
                    self.nodes.append(nd)
                    tempnodes.append(nd)
                ror += 1
            else:
                break
        print(len(self.nodes))
        for n in self.nodes:
            n.round += 1
        return

    def buildDoubleElimBracket(self):
        # buildBracket() first
        # For each round,
        #  If there's a previous round,
        #   Look at round NL
        #   Pair off losers from NW with those nodes as round (N+0.5)L
        #   Pair those nodes into round (N+1)L
        #  If there's no previous round,
        #   Pair off nodes into loser nodes in round (N+1)L
        return

    class N:
        def __init__(self, p1=None, p2=None, r=0, maxSeed=None, loser=False):
            self.bnid = T.bracket_id
            self.loser = loser
            self.round = r
            self.feeds = []
            self.match: T.M = (
                T.M(p1, p2) if p2 is not None else T.M(p1) if p1 is not None else T.M()
            )
            self.max_seed: int = (
                (
                    (max(p1.seed, p2.seed) if p2 is not None else p1.seed)
                    if p1 is not None
                    else -999
                )
                if maxSeed is None
                else maxSeed
            )
            T.bracket_id += 1
            return

        def __json__(self):
            return {
                "bnid": self.bnid,
                "round": self.round,
                "feeds": self.feeds,
                "match": {
                    "players": [str(p) for p in self.match.players],
                    "scores": self.match.scores,
                },
            }

    class M:
        def __init__(self, p1=None, p2=None):
            self.players: list[T.P] = (
                [p1, p2]
                if p1 is not None and p2 is not None
                else [p1]
                if p1 is not None and p2 is None
                else [p2]
                if p1 is None and p2 is not None
                else []
            )
            self.scores = []

        def setScores(self, scoreA, scoreB):
            self.scores = [scoreA, scoreB]

        def getWinnerLoser(self):
            w = self.scores.index(max(self.scores))
            l = 0 if w == 1 else 1
            return [self.players[w], self.players[l]]

    class P:
        def __init__(self, id, seed=0):
            self.id = id
            self.seed = seed
            self.rank = 0
            self.lastround = 0

        def __lt__(self, other):
            return self.seed > other.seed

        def __str__(self):
            return self.id

        def __eq__(self, other):
            return self.id == other.id
