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
        tempplayers = self.players[:]
        tempplayers.sort(key=lambda n: n.seed, reverse=True)
        # Sort the players by their seed.
        # Add bogus players AKA byes until there are 4, 8, 16, 32, etc players
        # Makes the bracket evenly distributed
        while not is_pow(len(tempplayers)):
            tempplayers.append(T.P(id="0", seed=-999))
        tempplayers.sort(key=lambda x: x.seed if type(x) == T.P else x.max_seed)
        # Pair the highest seed with the lowest seed
        # The lowest can be a bye. Each of the highest ranked players get byes when possible
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
        ror = 1
        # Start pairing off all the node pairs into the next round
        while True:
            tempnodes2 = tempnodes[:]
            if len(tempnodes2) > 1:
                # Pair the worst player available with the best player available
                # If both of the nodes have byes, combine them into a new node without byes
                # If one of the nodes has a bye,
                # delete the bye node and just put that player into the new node
                # Otherwise, feed the two nodes into a new node
                tempnodes2.sort(key=lambda n: n.max_seed)
                while len(tempnodes2) > 0:
                    maxnode: T.N = tempnodes2.pop()
                    minnode: T.N = tempnodes2.pop(0)
                    if (
                        T.P(id="0", seed=-999) in maxnode.match.players
                        and T.P(id="0", seed=-999) in minnode.match.players
                    ):
                        p1 = [i for i in maxnode.match.players if i.id != "0"][0]
                        p2 = [i for i in minnode.match.players if i.id != "0"][0]
                        nd = T.N(
                            p1=p1,
                            p2=p2,
                            r=ror,
                            maxSeed=max([p1.seed, p2.seed]),
                        )
                        self.nodes.remove(maxnode)
                        self.nodes.remove(minnode)
                        self.nodes.append(nd)
                        tempnodes.append(nd)
                        tempnodes.remove(maxnode)
                        tempnodes.remove(minnode)
                    elif T.P(id="0", seed=-999) in maxnode.match.players:
                        p1 = [i for i in maxnode.match.players if i.id != "0"][0]
                        nd = T.N(
                            p1=p1,
                            r=ror,
                            maxSeed=max([p1.seed, minnode.max_seed]),
                        )
                        self.nodes.remove(maxnode)
                        self.nodes.append(nd)
                        tempnodes.append(nd)
                        tempnodes.remove(maxnode)
                        tempnodes.remove(minnode)
                        minnode.feeds.append(nd.bnid)
                    elif T.P(id="0", seed=-999) in minnode.match.players:
                        p2 = [i for i in minnode.match.players if i.id != "0"][0]
                        nd = T.N(
                            p2=p2,
                            r=ror,
                            maxSeed=max([p2.seed, maxnode.max_seed]),
                        )
                        self.nodes.remove(minnode)
                        self.nodes.append(nd)
                        tempnodes.append(nd)
                        tempnodes.remove(maxnode)
                        tempnodes.remove(minnode)
                        maxnode.feeds.append(nd.bnid)
                    else:
                        nd = T.N(
                            r=ror,
                            maxSeed=max(
                                [
                                    maxnode.max_seed,
                                    minnode.max_seed,
                                ]
                            ),
                        )
                        self.nodes.append(nd)
                        tempnodes.append(nd)
                        tempnodes.remove(minnode)
                        tempnodes.remove(maxnode)
                        maxnode.feeds.append(nd.bnid)
                        minnode.feeds.append(nd.bnid)
                ror += 1
            else:
                break
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
