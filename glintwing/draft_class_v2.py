from typing import Union


class SwissEvent:
    def __init__(self):
        self.id = ""
        self.host = ""
        self.round_one = []
        self.round_two = []
        self.round_three = []
        self.players = []

    def __json__(self):
        return ""

    def pair_round_one(self):
        # Pair per seat
        # 1-5, 2-6, 3-7, 4-8
        self.players.sort(key=lambda p: p.seat)
        leftover = len(self.players) % 2 == 1
        return [SwissPairing(self.players[i], self.players[x] if (x := i + len(self.players) // 2) < len(self.players) else None) for i in range(0, len(self.players) // 2)] + ([] if not leftover else [SwissPairing(self.players[-1], None)])

    def pair_round_two(self):
        # Get winning players; bye counts as 2-0
        # Get losing and tying players
        # Pair up winning players, 2-0s first, then 2-1s
        # If any left over,
        # Pair up leftover with the top losing player, 1-1s then 0-0s then 1-2s then 0-2s
        # Pair up losing players, 1-2s first
        # Bye to the leftover player
        non_dropped_players = [p for p in self.players if not p.dropped]

        def sort_func(player):
            bye = self.match_one(player).is_bye()
            flawless = self.match_one(player).game_one == player and self.match_one(player).game_two == player
            clutched = self.match_one(player).game_three == player
            game_tied = self.match_one(player).game_one == player and self.match_one(player).game_two != player or self.match_one(player).game_two == player and self.match_one(player).game_one != player
            to_time = self.match_one(player).game_one == None
            flubbed = self.match_one(player).game_three != player and self.match_one(player).game_three is not None
            blown = self.match_one(player).game_one != player and self.match_one(player).game_two != player
            return (not bye, not flawless, not clutched, not game_tied, not to_time, not flubbed, not blown, player.seat)

        non_dropped_players.sort(key=sort_func)
        pairings = []
        while non_dropped_players:
            pl = non_dropped_players.pop(0)
            for opp in non_dropped_players:
                if self.match_one(pl).opponent(pl) == opp or (pl.seat + 1 == opp.seat or pl.seat - 1 == opp.seat):
                    continue
                pairings.append(SwissPairing(pl, opp))
                non_dropped_players.remove(opp)
                break
            else:
                pairings.append(SwissPairing(pl, None))
        return pairings

    def pair_round_three(self):
        # Sort by score, then game-win-percentage
        # Choose top non-prior opponent
        # Pair
        non_dropped_players = [p for p in self.players if not p.dropped]

        def sort_func(player):
            first_score, first_priority = self.match_one(player).score(player)
            second_score, second_priority = self.match_two(player).score(player)
            bye = self.match_two(player).is_bye()
            flawless = self.match_two(player).game_one == player and self.match_two(player).game_two == player
            clutched = self.match_two(player).game_three == player
            game_tied = self.match_two(player).game_one == player and self.match_two(player).game_two != player or self.match_two(player).game_two == player and self.match_two(player).game_one != player
            to_time = self.match_two(player).game_one == None
            flubbed = self.match_two(player).game_three != player and self.match_two(player).game_three is not None
            blown = self.match_two(player).game_one != player and self.match_two(player).game_two != player
            return (-1 * (first_score + second_score), -1 * (first_priority + second_priority), not bye, not flawless, not clutched, not game_tied, not to_time, not flubbed, not blown, player.seat)

        non_dropped_players.sort(key=sort_func)
        pairings = []
        while non_dropped_players:
            pl = non_dropped_players.pop(0)
            for opp in non_dropped_players:
                if self.match_one(pl).opponent(pl) == opp or self.match_two(pl).opponent(pl) == opp:
                    continue
                pairings.append(SwissPairing(pl, opp))
                non_dropped_players.remove(opp)
                break
            else:
                pairings.append(SwissPairing(pl, None))
        return pairings

    def stats(self, player_id):
        pass

    def match_one(self, player):
        for m in self.round_one:
            if m.player_one == player or m.player_two == player:
                return m
        return None

    def match_two(self, player):
        for m in self.round_two:
            if m.player_one == player or m.player_two == player:
                return m
        return None

    def match_three(self, player):
        for m in self.round_three:
            if m.player_one == player or m.player_two == player:
                return m
        return None


class SwissPlayer:
    def __init__(self, id, seat=0):
        self.id = id
        self.seat = seat
        self.dropped = False

    def __eq__(self, other):
        if other is None:
            return False
        return self.id == other.id

    def __repr__(self):
        return f"{self.id}"  # @{self.seat}"


class SwissPairing:
    def __init__(self, player_one, player_two):
        self.player_one = player_one
        self.player_two = player_two
        self.game_one = None
        self.game_two = None
        self.game_three = None

    def __repr__(self):
        p1_score, _ = self.score(self.player_one)
        p2_score, _ = self.score(self.player_two)
        return f"{self.player_one}|{p1_score} vs {self.player_two}|{p2_score}"

    def is_tie(self) -> bool:
        if (self.game_one == self.player_one or self.game_one == self.player_two) and self.game_one != self.game_two and self.game_three is None:
            return True
        if self.game_one is None and self.game_two is None:
            return True
        return False

    def is_bye(self) -> bool:
        return self.player_two is None

    def opponent(self, player) -> Union[SwissPlayer, None]:
        if player == self.player_one:
            return self.player_two
        if player == self.player_two:
            return self.player_one
        return None

    def score(self, player) -> (int, int):
        if player is None:
            return 0, 0
        if self.is_bye():
            return 3, 3
        if self.is_tie():
            return 1, 0
        if player == self.game_one and player == self.game_two:
            return 3, 4
        if player == self.game_two and player == self.game_three:
            return 3, 2
        if player == self.game_one and player == self.game_three:
            return 3, 1
        return 0, 0


if __name__ == "__main__":
    # Do tests
    def test(num_players, score_round_one=None, after_round_one=lambda x: x, score_round_two=None, after_round_two=lambda x: x, score_round_three=None):
        drft = SwissEvent()
        drft.players = [SwissPlayer(f"{i + 1}", i) for i in range(0, num_players)]
        print(drft.players)
        drft.round_one = drft.pair_round_one()
        if score_round_one is not None:
            score_round_one(drft.round_one)
        else:
            for pairing in drft.round_one:
                pairing.game_one = pairing.player_one
                pairing.game_two = pairing.player_one
        print(drft.round_one)
        after_round_one(drft)
        drft.round_two = drft.pair_round_two()
        if score_round_two is not None:
            score_round_two(drft.round_two)
        else:
            for pairing in drft.round_two:
                pairing.game_one = pairing.player_one
                pairing.game_two = pairing.player_one
        print(drft.round_two)
        after_round_two(drft)
        drft.round_three = drft.pair_round_three()
        if score_round_three is not None:
            score_round_three(drft.round_three)
        else:
            for pairing in drft.round_three:
                pairing.game_one = pairing.player_one
                pairing.game_two = pairing.player_one
        print(drft.round_three)

    def drop_seat(seat):
        def drp(draft):
            for player in draft.players:
                if player.seat == seat:
                    player.dropped = True

        return drp

    def test_first_pairs(pairs):
        def tst(draft):
            for test in pairs:
                did_test = False
                for pair in draft.round_one:
                    if pair.player_one in test or pair.player_two in test:
                        assert pair.player_one in test and pair.player_two in test
                        did_test = True
                assert did_test == True

        return tst

    def test_second_pairs(pairs):
        def tst(draft):
            for test in pairs:
                did_test = False
                for pair in draft.round_two:
                    if pair.player_one in test or pair.player_two in test:
                        assert pair.player_one in test and pair.player_two in test
                        did_test = True
                assert did_test == True

        return tst

    def test_third_pairs(pairs):
        def tst(draft):
            for test in pairs:
                did_test = False
                for pair in draft.round_three:
                    if pair.player_one in test or pair.player_two in test:
                        assert pair.player_one in test and pair.player_two in test
                        did_test = True
                assert did_test == True

        return tst

    test(
        8,
        after_round_one=test_first_pairs(
            [
                [SwissPlayer("1"), SwissPlayer("5")],
                [SwissPlayer("2"), SwissPlayer("6")],
                [SwissPlayer("3"), SwissPlayer("7")],
                [SwissPlayer("4"), SwissPlayer("8")],
            ]
        ),
    )
    test(8, after_round_one=drop_seat(0), after_round_two=test_second_pairs([[SwissPlayer("3"), SwissPlayer("5")], [SwissPlayer("6"), SwissPlayer("8")], [SwissPlayer("2"), SwissPlayer("4")], [SwissPlayer("7"), None]]))
    test(8, after_round_two=drop_seat(1))
