def is_pow(n):
    """Returns whether a number is a power of two."""
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
        """Three character code to categorize this event."""
        self.date: str = ""
        """String representation of the date of the event."""
        self.title = ""
        self.players: list[T.P] = []
        self.nodes: list[T.N] = []
        return

    def node_from_bnid(self, bnid: str):
        """Retrieves a node from the bracket matching the id, or False."""
        for n in self.nodes:
            if n.bnid == bnid:
                return n
        return False

    def reportScore(self, pl: str, scr: str):
        """Reports a score identifier to the last game the player played."""
        # Search through rounds in reverse to find last one with the player in it
        # Replace scores in node
        theplayer = [i for i in self.players if i.p_id == pl][0]
        rounds = list(set([o.round for o in self.nodes]))
        rounds.sort(key=lambda x: float(x), reverse=False)
        for r in rounds:
            roundnodes = [n for n in self.nodes if n.round == r]
            mynode = [p for p in roundnodes if theplayer in p.match.players]
            if len(mynode) > 0:
                mynode[0].match.setScores(theplayer, scr)
        return self

    def push_matches(self):
        """For each match with results, send the players to the appropriate nodes."""
        # For each node,
        # If match.scores is not empty,
        # Push winner into the first node in the feeds list
        # If len(feeds) > 1, push loser into the second node
        for n in self.nodes:
            if w := n.match.getWinnerLoser():
                if w == [None]:
                    continue
                for i, b in enumerate(n.feeds):
                    nd = self.node_from_bnid(b)
                    if None in nd.match.players and w[i] not in nd.match.players:
                        nd.match.players.remove(None)
                        nd.match.players.append(w[i])
        return

    def calcRanks(self):
        """Gives each player a numerical ranking based on their position in the bracket."""
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
                if player not in rankedlist and player is not None:
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
                    "playerID": p.p_id,
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
        """Removes extraneous bye and empty nodes from the nodes list."""
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
                if len(winnode.match.players) == 2:
                    winnode.match.players.remove(None)
                winnode.match.players.insert(0, theplayer)
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
                max_seed=max(
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
                            max_seed=max([p1.seed, p2.seed]),
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
                            max_seed=max([p1.seed, minnode.max_seed]),
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
                            max_seed=max([p2.seed, maxnode.max_seed]),
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
                            max_seed=max(
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
        """Adds loser bracket nodes from the normal bracket nodes in the nodes list."""
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
                        max_seed=max([minnode.max_seed, maxnode.max_seed]),
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
                        max_seed=max([minnode.max_seed, maxnode.max_seed]),
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
                        max_seed=max([minnode.max_seed, maxnode.max_seed]),
                        loser=True,
                    )
                    self.nodes.append(nd)
                    minnode.feeds.append(nd.bnid)
                    maxnode.feeds.append(nd.bnid)
        self.nodes.sort(key=lambda x: x.round)
        biground = max([x.round for x in self.nodes])
        n1 = self.nodes[-1]
        n2 = self.nodes[-3]
        nd = T.N(r=biground, max_seed=max([x.max_seed for x in [n1, n2]]))
        n1.feeds.append(nd.bnid)
        n2.feeds.append(nd.bnid)
        self.nodes.append(nd)
        return

    class N:
        def __init__(self, p1=None, p2=None, r=0, max_seed=None, loser=False):
            self.bnid = T.bracket_id
            self.loser = loser
            self.round = r
            self.feeds = []
            """BNID pointers to the nodes that this node will feed its winner and loser respectively."""
            self.match: T.M = T.M(p1, p2)
            self.max_seed: int = max(
                p1.seed if p1 is not None else -999,
                p2.seed if p2 is not None else -999,
                max_seed if max_seed is not None else -999,
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
            self.players = [p1, p2]
            self.scores = []

        def setScores(self, player, result_code: str):
            """Sets the score for the match from the perspective of the player."""
            if self.players.index(player) == 0:
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
            if result_code == "0":
                self.scores = [p_index, p_index]
            elif result_code == "1":
                self.scores = [p_index, o_index, p_index]
            elif result_code == "2":
                self.scores = [o_index, p_index, p_index]
            elif result_code == "3":
                self.scores = [o_index, p_index, o_index]
            elif result_code == "4":
                self.scores = [p_index, o_index, o_index]
            elif result_code == "5":
                self.scores = [o_index, o_index]
            elif result_code == "6":
                self.scores = [p_index, o_index]
            elif result_code == "7":
                self.scores = [o_index, p_index]

        def getWinnerLoser(self):
            """Returns the winning player and losing player in that order, or [None]."""
            if self.scores.count(0) > self.scores.count(1):
                return [self.players[0], self.players[1]]
            elif self.scores.count(0) < self.scores.count(1):
                return [self.players[1], self.players[0]]
            else:
                return [None]

        def getScore(self, pl):
            if pl not in self.players:
                return 0
            return self.scores.count(self.players.index(pl))

    class P:
        def __init__(self, id: str, seed: int = 0):
            self.p_id = id
            self.seed = seed
            """Although not behaviorally different, a seed of 1 is the worst, and a high seed is the best.
            
            These should be unique to each player."""
            self.rank = 0
            self.lastround = 0

        def __lt__(self, other):
            return self.seed > other.seed

        def __str__(self):
            return self.p_id

        def __eq__(self, other):
            return self.p_id == other.p_id if other is not None else False
