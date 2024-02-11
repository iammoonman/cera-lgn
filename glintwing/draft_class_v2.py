import datetime
import json
from typing import Union


def distance(pA, pB, players):
    """Thanks, Metro!"""
    return min(abs(pB.seat - pA.seat), len(players) - pB.seat + pA.seat, len(players) - pA.seat + pB.seat)


class SwissEvent:
    def __init__(self, id, host, tag: str, description: str, title: str, cube_id: str = "", set_code: str = ""):
        self.id = id
        self.host = host
        """Discord User ID"""
        self.title = title
        self.description = description
        self.cube_id = cube_id
        """CubeCobra ID, short or long"""
        self.set_code = set_code
        """Three-character set code from Scryfall"""
        self.tag = tag
        self.round_one: list[SwissPairing] = []
        self.round_two: list[SwissPairing] = []
        self.round_three: list[SwissPairing] = []
        self.players: list[SwissPlayer] = []

    @property
    def current_round(self):
        """Returns the round index and round object for the currently played round."""
        if len(self.round_three) > 0:
            return 2, self.round_three
        if len(self.round_two) > 0:
            return 1, self.round_two
        return 0, self.round_one

    def get_player_by_id(self, id):
        for p in self.players:
            if p.id == id:
                return p
        return None

    @property
    def json(self):
        return {
            "id": f"{self.id}",
            "meta": {
                "date": f"{datetime.datetime.now(tz=datetime.timezone.utc).isoformat()}",
                "title": self.title,
                **({"tag": self.tag} if self.tag != "anti" and self.tag else {}),
                **({"description": self.description} if self.description else {}),
                **({"host": str(self.host)} if self.host else {}),
                **({"cube_id": self.cube_id} if self.cube_id else {}),
                **({"set_code": self.set_code} if self.set_code else {}),
            },
            "R_0": [{"players": [str(p.player_one.id), str(p.player_two.id) if p.player_two is not None else None][: 2 if p.player_two is not None else 1], "games": [(0 if p.game_one.id == p.player_one.id else 1) if p.game_one is not None else None, (0 if p.game_two.id == p.player_one.id else 1) if p.game_two is not None else None, (0 if p.game_three.id == p.player_one.id else 1) if p.game_three is not None else None][: 3 if p.game_three is not None else 2 if p.game_two is not None else 1 if p.game_one is not None else 0]} for p in self.round_one],
            "R_1": [{"players": [str(p.player_one.id), str(p.player_two.id) if p.player_two is not None else None][: 2 if p.player_two is not None else 1], "games": [(0 if p.game_one.id == p.player_one.id else 1) if p.game_one is not None else None, (0 if p.game_two.id == p.player_one.id else 1) if p.game_two is not None else None, (0 if p.game_three.id == p.player_one.id else 1) if p.game_three is not None else None][: 3 if p.game_three is not None else 2 if p.game_two is not None else 1 if p.game_one is not None else 0]} for p in self.round_two],
            "R_2": [{"players": [str(p.player_one.id), str(p.player_two.id) if p.player_two is not None else None][: 2 if p.player_two is not None else 1], "games": [(0 if p.game_one.id == p.player_one.id else 1) if p.game_one is not None else None, (0 if p.game_two.id == p.player_one.id else 1) if p.game_two is not None else None, (0 if p.game_three.id == p.player_one.id else 1) if p.game_three is not None else None][: 3 if p.game_three is not None else 2 if p.game_two is not None else 1 if p.game_one is not None else 0]} for p in self.round_three],
        }

    def pair_round_one(self):
        # The first round is always paired by seat.
        # 1-5, 2-6, 3-7, 4-8
        self.players.sort(key=lambda p: p.seat)
        leftover = len(self.players) % 2 == 1
        return [SwissPairing(self.players[i], self.players[x] if (x := i + len(self.players) // 2) < len(self.players) else None) for i in range(0, len(self.players) // 2)] + ([] if not leftover else [SwissPairing(self.players[-1], None)])

    def pair_round_two(self):
        """Returns pairs for a round two. Depends on round one having been played."""
        # The second round is paired by seat at best.
        # The winners and losers of 1-5 and 3-7 play against each other, and same for 2-6 and 4-8.
        #
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
        pairings: list[SwissPairing] = []
        while non_dropped_players:
            pl = non_dropped_players.pop(0)
            for opp in non_dropped_players:
                if self.match_one(pl).opponent(pl) == opp:
                    continue
                if (pl.seat + 1 == opp.seat or pl.seat - 1 == opp.seat) and len(non_dropped_players) > 3:
                    continue
                pairings.append(SwissPairing(pl, opp))
                non_dropped_players.remove(opp)
                break
            else:
                pairings.append(SwissPairing(pl, None))
        return pairings

    def pair_round_three(self):
        """Returns pairs for a round three. Depends on round two having been played."""
        # Sort by score, then game-win-percentage
        # Choose top non-prior opponent
        # Pair
        non_dropped_players = [p for p in self.players if not p.dropped]

        def sort_func(player):
            first_score, first_priority, _, _ = self.match_one(player).score(player)
            second_score, second_priority, _, _ = self.match_two(player).score(player)
            bye = self.match_two(player).is_bye()
            flawless = self.match_two(player).game_one == player and self.match_two(player).game_two == player
            clutched = self.match_two(player).game_three == player
            game_tied = self.match_two(player).game_one == player and self.match_two(player).game_two != player or self.match_two(player).game_two == player and self.match_two(player).game_one != player
            to_time = self.match_two(player).game_one == None
            flubbed = self.match_two(player).game_three != player and self.match_two(player).game_three is not None
            blown = self.match_two(player).game_one != player and self.match_two(player).game_two != player
            return (-1 * (first_score + second_score), -1 * (first_priority + second_priority), not bye, not flawless, not clutched, not game_tied, not to_time, not flubbed, not blown, player.seat)

        non_dropped_players.sort(key=sort_func)
        pairings: list[SwissPairing] = []
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

    def stats(self, player_id: str) -> tuple[float, int, float]:
        """GWP, Match Points, MWP"""
        player = self.get_player_by_id(player_id)
        game_count = 0
        score_total = 0
        game_wins_count = 0
        match_wins_count = 0
        match_count = 0
        m_one = self.match_one(player)
        m_two = self.match_two(player)
        m_three = self.match_three(player)
        # print(m_one, m_two, m_three)
        if m_one is not None:
            score, _, games, wins = m_one.score(player)
            score_total += score
            game_count += games
            game_wins_count += wins
            match_count += 1
            match_wins_count += 1 if score == 3 else 0
        if m_two is not None:
            score, _, games, wins = m_two.score(player)
            score_total += score
            game_count += games
            game_wins_count += wins
            match_count += 1
            match_wins_count += 1 if score == 3 else 0
        if m_three is not None:
            score, _, games, wins = m_three.score(player)
            score_total += score
            game_count += games
            game_wins_count += wins
            match_count += 1
            match_wins_count += 1 if score == 3 else 0
        return game_wins_count / game_count if game_count > 0 else 0, score_total, match_wins_count / match_count if match_count > 0 else 0

    def secondary_stats(self, player_id: str) -> tuple[int, float, float, float, float]:
        """Match Points, GWP, MWP, OGP, OMP"""
        # print(player_id, round)
        player = self.get_player_by_id(player_id)
        gwp, mp, mwp = self.stats(player_id)
        o_count = 0
        o_gwp_sum = 0
        o_mwp_sum = 0
        o_one = self.match_one(player).opponent(player) if self.match_one(player) is not None else None
        o_two = self.match_two(player).opponent(player) if self.match_two(player) is not None else None
        o_three = self.match_three(player).opponent(player) if self.match_three(player) is not None else None
        if o_one is not None:
            o_gwp, _, o_mwp = self.stats(o_one.id)
            o_gwp_sum += o_gwp
            o_mwp_sum += o_mwp
            o_count += 1
        if o_two is not None:
            o_gwp, _, o_mwp = self.stats(o_two.id)
            o_gwp_sum += o_gwp
            o_mwp_sum += o_mwp
            o_count += 1
        if o_three is not None:
            o_gwp, _, o_mwp = self.stats(o_three.id)
            o_gwp_sum += o_gwp
            o_mwp_sum += o_mwp
            o_count += 1
        return mp, gwp, mwp, o_gwp_sum / o_count if o_count > 0 else 0, o_mwp_sum / o_count if o_count > 0 else 0

    def match_one(self, player):
        """Returns the first round match of the given player."""
        for m in self.round_one:
            if m.player_one == player or m.player_two == player:
                return m
        return None

    def match_two(self, player):
        """Returns the second round match of the given player."""
        for m in self.round_two:
            if m.player_one == player or m.player_two == player:
                return m
        return None

    def match_three(self, player):
        """Returns the third round match of the given player."""
        for m in self.round_three:
            if m.player_one == player or m.player_two == player:
                return m
        return None


class SwissPlayer:
    def __init__(self, id: str, seat=0):
        self.id = id
        self.seat = seat
        self.dropped = False

    def __eq__(self, other):
        if other is None:
            return False
        if isinstance(other, SwissPlayer):
            return self.id == other.id
        if isinstance(other, str):
            return self.id == other
        if isinstance(other, int):
            return self.id == other
        return False

    def __repr__(self):
        return f"{self.id}"


class SwissPairing:
    def __init__(self, player_one: SwissPlayer, player_two: SwissPlayer):
        self.player_one = player_one
        self.player_two = player_two
        self.game_one: Union[SwissPlayer, None] = None
        """The winner of game one. If None, then there isn't a winner."""
        self.game_two: Union[SwissPlayer, None] = None
        """The winner of game one. If None, then there isn't a winner."""
        self.game_three: Union[SwissPlayer, None] = None
        """The winner of game one. If None, then there isn't a winner."""

    def __repr__(self):
        p1_score, _, _, _ = self.score(self.player_one)
        p2_score, _, _, _ = self.score(self.player_two)
        return f"{self.player_one} vs {self.player_two} -> {self.player_one if p1_score > p2_score else self.player_two if not self.is_tie() else 'TIE'}"

    def is_tie(self) -> bool:
        if self.game_one is not None:
            if self.game_two is None:
                # 1-0
                return False
            else:
                if self.game_two == self.game_one or self.game_three == self.game_one:
                    # 2-0 or 2-1
                    return False
                if self.game_two != self.game_one and self.game_three is None:
                    # 1-1
                    return True
                if self.game_two == self.game_three:
                    # 1-2
                    return False
        else:
            # 0-0
            return True

    def is_bye(self) -> bool:
        return self.player_two is None

    def has_player(self, player: SwissPlayer):
        return self.player_one == player or self.player_two == player

    def opponent(self, player: SwissPlayer) -> Union[SwissPlayer, None]:
        if player == self.player_one:
            return self.player_two
        if player == self.player_two:
            return self.player_one
        return None

    def score(self, player: SwissPlayer) -> tuple[int, int, int, int]:
        """match points, priority, games played, games won"""
        me = None
        op = None
        if player == self.player_one:
            me = self.player_one
            op = self.player_two
        if player == self.player_two:
            me = self.player_two
            op = self.player_one
        if me is None:
            return 0, 0, 0, 0
        if self.is_bye():
            return 3, 3, 0, 0
        if self.is_tie():
            return 1, 0, (1 if self.game_one is not None else 0) + (1 if self.game_two is not None else 0), (1 if self.game_one == me else 0) + (1 if self.game_two == me else 0)
        if me == self.game_one and me == self.game_two:
            return 3, 4, 2, 2
        if me == self.game_two and me == self.game_three:
            return 3, 2, 3, 2
        if me == self.game_one and me == self.game_three:
            return 3, 1, 3, 2
        if op == self.game_one and op == self.game_two:
            return 0, -2, 2, 0
        if op == self.game_two and op == self.game_three:
            return 0, -1, 3, 1
        if op == self.game_one and op == self.game_three:
            return 0, -1, 3, 1
        if me == self.game_one and self.game_two is None:
            return 3, 4, 1, 1
        return 0, 0, 0, 0


if __name__ == "__main__":
    # Do tests
    def test(num_players, score_round_one=None, after_round_one=lambda x: x, score_round_two=None, after_round_two=lambda x: x, score_round_three=None):
        drft = SwissEvent("", "", "", "", "")
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
        for player in sorted(drft.players, key=lambda x: drft.secondary_stats(x.id), reverse=True):
            print(player, f"PTS:{(sts:=drft.secondary_stats(player.id))[0]}|GWP:{sts[1]:.2f}|MWP:{sts[2]:.2f}|OGP:{sts[3]:.2f}|OMP:{sts[4]:.2f}")
        print("----------")
        after_round_one(drft)
        drft.round_two = drft.pair_round_two()
        if score_round_two is not None:
            score_round_two(drft.round_two)
        else:
            for pairing in drft.round_two:
                pairing.game_one = pairing.player_one
                pairing.game_two = pairing.player_one
        print(drft.round_two)
        for player in sorted(drft.players, key=lambda x: drft.secondary_stats(x.id), reverse=True):
            print(player, f"PTS:{(sts:=drft.secondary_stats(player.id))[0]}|GWP:{sts[1]:.2f}|MWP:{sts[2]:.2f}|OGP:{sts[3]:.2f}|OMP:{sts[4]:.2f}")
        print("----------")
        c = 0
        for pairing in drft.round_two:
            if pairing.player_two is None:
                c += 1
            if len(drft.players) > 4:
                assert c < 2
        after_round_two(drft)
        drft.round_three = drft.pair_round_three()
        if score_round_three is not None:
            score_round_three(drft.round_three)
        else:
            for pairing in drft.round_three:
                pairing.game_one = pairing.player_one
                pairing.game_two = pairing.player_one
        print(drft.round_three)
        for player in sorted(drft.players, key=lambda x: drft.secondary_stats(x.id), reverse=True):
            print(player, f"PTS:{(sts:=drft.secondary_stats(player.id))[0]}|GWP:{sts[1]:.2f}|MWP:{sts[2]:.2f}|OGP:{sts[3]:.2f}|OMP:{sts[4]:.2f}")
        print("----------")
        c = 0
        for pairing in drft.round_three:
            if pairing.player_two is None:
                c += 1
            if len(drft.players) > 4:
                assert c < 2
        for player in sorted(drft.players, key=lambda x: drft.secondary_stats(x.id), reverse=True):
            print(player, f"PTS:{(sts:=drft.secondary_stats(player.id))[0]}|GWP:{sts[1]:.2f}|MWP:{sts[2]:.2f}|OGP:{sts[3]:.2f}|OMP:{sts[4]:.2f}")
        print("----------")
        print(json.dumps(drft.json))

    def drop_seat(seat):
        def drp(draft):
            for player in draft.players:
                if player.seat == seat:
                    player.dropped = True
                    print(f"PLAYER {player} DROP")

        return drp

    def drop_ids(ids):
        def drp(draft):
            for player in draft.players:
                if player.id in ids:
                    player.dropped = True
                    print(f"PLAYER {player} DROP")

        return drp

    def test_first_pairs(pairs):
        def tst(draft):
            for test in pairs:
                test_pair = [SwissPlayer(test[0]), SwissPlayer(test[1]) if test[1] is not None else None]
                did_test = False
                for pair in draft.round_one:
                    if pair.player_one in test_pair or pair.player_two in test_pair:
                        assert pair.player_one in test_pair and pair.player_two in test_pair
                        did_test = True
                assert did_test == True

        return tst

    def test_second_pairs(pairs):
        def tst(draft):
            for test in pairs:
                test_pair = [SwissPlayer(test[0]), SwissPlayer(test[1]) if test[1] is not None else None]
                did_test = False
                for pair in draft.round_two:
                    if pair.player_one in test_pair or pair.player_two in test_pair:
                        assert pair.player_one in test_pair and pair.player_two in test_pair
                        did_test = True
                assert did_test == True

        return tst

    def test_third_pairs(pairs):
        def tst(draft):
            for test in pairs:
                test_pair = [SwissPlayer(test[0]), SwissPlayer(test[1]) if test[1] is not None else None]
                did_test = False
                for pair in draft.round_three:
                    if pair.player_one in test_pair or pair.player_two in test_pair:
                        assert pair.player_one in test_pair and pair.player_two in test_pair
                        did_test = True
                assert did_test == True

        return tst

    def ties(pairs):
        for i, pair in enumerate(pairs):
            if i == 0:
                pair.game_one = pair.player_one
                pair.game_two = pair.player_two
            else:
                pair.game_one = pair.player_one
                pair.game_two = pair.player_one

    test(8, after_round_one=test_first_pairs([["1", "5"], ["2", "6"], ["3", "7"], ["4", "8"]]))
    test(8, after_round_one=drop_seat(0))
    test(8, after_round_two=drop_seat(1))
    test(8, score_round_one=lambda x: ties(x), after_round_one=drop_seat(0))
    test(8, after_round_two=drop_ids(["1", "2"]))
    test(8, after_round_two=drop_ids(["1", "2", "3"]))
    test(8, after_round_two=drop_ids(["1", "2", "3", "4"]))
    test(8, after_round_one=drop_ids(["1", "4"]), after_round_two=drop_ids(["2", "7"]))
    test(7)
    test(6)
    test(6, after_round_one=drop_ids(["1"]))
