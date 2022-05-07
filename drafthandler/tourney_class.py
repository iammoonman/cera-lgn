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

    def reportScore(self, pl, scr):
        # Search through rounds in reverse to find last one with the player in it
        # Replace scores in node
        rounds = list(set([o.round for o in self.nodes]))
        print(rounds)
        for r in rounds:
            roundnodes = [n for n in self.nodes if n.round == r]
            mynode = [p for p in roundnodes if pl in p.match.players][0]
            mynode.match.setScoreP(pl,scr[0])
        return self

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
        self.calcRanks()
        return {
            "eventID": self.eventID,
            "tag": self.tag,
            "date": self.date,
            "title": self.title,
            "players": [
                {
                    "playerID": p.id,
                    "rank": p.rank,
                    # "wins": sum([n.match.getScore(p) for n in self.nodes]),
                    # "losses": sum(
                    #     [
                    #         1#n.match.getScore([o for o in n.match.players if o is not p][0])
                    #         for n in self.nodes
                    #         if p in n.match.players
                    #     ]
                    # ),
                }  # Remember to iterate through each bracket if able.
                for p in self.players
            ],
            "nodes": [b.__json__() for b in self.nodes],
        }

    def cutByes(self):
        # For each node which doesn't have anything feeding into it,
        # If it's a bye,
        # Choose its winner feed
        # Put its players into that node
        # Delete the previous node
        # For each loser node,
        # If only one node feeds into it,
        # instead have that node feed into the node that the loser feeds
        # Finally, if any loser node is an entry node, delete it
        secondarynodes = sum([u.feeds for u in self.nodes], [])
        entrynodes = [u for u in self.nodes if u.bnid not in secondarynodes]
        while len(entrynodes) > 0:
            e = entrynodes.pop()
            if T.P(id="0", seed=-999) in e.match.players:
                # print("dropping a node")
                e.match.players.remove(T.P(id="0", seed=-999))
                theplayer = e.match.players.pop()
                winnode = next(
                    q for q in self.nodes if q.bnid in e.feeds and not q.loser
                )
                winnode.match.players.append(theplayer)
                self.nodes.remove(e)
        for losernode in [l for l in self.nodes if l.loser]:
            if (
                len((feeder := [y for y in self.nodes if losernode.bnid in y.feeds]))
                == 1
            ):
                feeder[0].feeds.remove(losernode.bnid)
                feeder[0].feeds.append(losernode.feeds[0])
                self.nodes.remove(losernode)
        secondarynodes = sum([u.feeds for u in self.nodes], [])
        entrynodes = [u for u in self.nodes if u.bnid not in secondarynodes]
        for n in entrynodes:
            if n.loser:
                self.nodes.remove(n)
        return

    def buildBracket(self, dropByes=True):
        """Builds the nodes needed to form a bracket out of the player list."""
        tempnodes: list[T.N] = []
        tempplayers = self.players[:]
        tempplayers.sort(key=lambda n: n.seed, reverse=True)
        # Sort the players by their seed.
        # Add bogus players AKA byes until there are 4, 8, 16, 32, etc players
        # Makes the bracket evenly distributed
        while not is_pow(len(tempplayers)):
            tempplayers.append(T.P(id="0", seed=-999))
        tempplayers.sort(key=lambda x: x.seed)
        # Pair the highest seed with the lowest seed
        # The lowest can be a bye. Each of the highest ranked players get byes when possible
        while len(tempplayers) > 0:
            maxplayer = tempplayers.pop()
            minplayer = tempplayers.pop(0)
            holdnode = T.N(
                p1=maxplayer,
                p2=minplayer,
                r=0,
                maxSeed=max(
                    maxplayer.seed,
                    minplayer.seed,
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
                    ) and dropByes:
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
                    elif T.P(id="0", seed=-999) in maxnode.match.players and dropByes:
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
                    elif T.P(id="0", seed=-999) in minnode.match.players and dropByes:
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
        # If the players list isn't a power of 2, this will explode
        # if not is_pow(len(self.players)):
        #     return
        # For each round,
        #  If there's a previous round,
        #   Look at round NL
        #   Pair off losers from NW with those nodes as round (N+0.5)L
        #   Pair those nodes into round (N+1)L
        #  If there's no previous round,
        #   Pair off nodes into loser nodes in round (N+1)L
        # Finally, pair the final winner with the last loser
        rounds = []
        for n in self.nodes:
            if n.round not in rounds:
                rounds.append(n.round)
        # print(rounds)
        rounds.sort()
        for r in rounds:
            tempnodes = [n for n in self.nodes if n.round == r and not n.loser]
            templosernodes = [n for n in self.nodes if n.round == r and n.loser]
            # print("w", tempnodes)
            # print("l", templosernodes)
            if len(templosernodes) > 0:
                # Pair off this round's loser nodes with the losers from this round
                tempnodes += templosernodes
                tempnodes.sort(key=lambda x: (x.loser, x.max_seed))
                halfagainnodes = []
                while len(tempnodes) > 1:
                    minnode: T.N = tempnodes.pop()
                    maxnode: T.N = tempnodes.pop(0)
                    nd = T.N(
                        r=r + 0.5,
                        maxSeed=max([minnode.max_seed, maxnode.max_seed]),
                        loser=True,
                    )
                    self.nodes.append(nd)
                    halfagainnodes.append(nd)
                    minnode.feeds.append(nd.bnid)
                    maxnode.feeds.append(nd.bnid)
                halfagainnodes.sort(key=lambda x: (x.loser, x.max_seed))
                while len(halfagainnodes) > 1:
                    minnode: T.N = halfagainnodes.pop()
                    maxnode: T.N = halfagainnodes.pop(0)
                    nd = T.N(
                        r=r + 1,
                        maxSeed=max([minnode.max_seed, maxnode.max_seed]),
                        loser=True,
                    )
                    self.nodes.append(nd)
                    minnode.feeds.append(nd.bnid)
                    maxnode.feeds.append(nd.bnid)
            else:
                while len(tempnodes) > 1:
                    tempnodes.sort(key=lambda x: (x.loser, x.max_seed))
                    minnode: T.N = tempnodes.pop()
                    maxnode: T.N = tempnodes.pop(0)
                    nd = T.N(
                        r=r + 1,
                        maxSeed=max([minnode.max_seed, maxnode.max_seed]),
                        loser=True,
                    )
                    self.nodes.append(nd)
                    minnode.feeds.append(nd.bnid)
                    maxnode.feeds.append(nd.bnid)
        self.nodes.sort(key=lambda x: x.round)
        biground = max([x.round for x in self.nodes])
        n1 = self.nodes[-1]
        n2 = self.nodes[-3]
        nd = T.N(r=biground, maxSeed=max([x.max_seed for x in [n1, n2]]))
        n1.feeds.append(nd.bnid)
        n2.feeds.append(nd.bnid)
        self.nodes.append(nd)
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
                "loser": self.loser,
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
            self.scores = [0, 0]  # [0 for _ in range(len(self.players))]

        def setScores(self, scoreA, scoreB):
            self.scores = [scoreA, scoreB]

        def setScoreP(self,player,score):
            self.scores[self.players.index(player)] == score
            return

        def getWinnerLoser(self):
            if self.players == []:
                return []
            w = self.scores.index(max(self.scores))
            l = 0 if w == 1 else 1
            if len(self.players) == 1:
                return [self.players[0]]
            return [self.players[w], self.players[l]]

        def getScore(self, pl):
            if pl not in self.players:
                return 0
            return self.scores[self.players.index(pl)]

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
