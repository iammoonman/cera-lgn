import datetime
import json
from typing import Union


def distance(pA, pB, players):
    return min(abs(pB.seat - pA.seat), len(players) - pB.seat + pA.seat, len(players) - pA.seat + pB.seat)


class SwissEvent:
    def __init__(self, id: str, host: str, tag: str, description: str, title: str, cube_id: str = "", set_code: str = ""):
        self.id = id
        self.host = host
        self.title = title
        self.description = description
        self.cube_id = cube_id
        self.set_code = set_code
        self.tag = tag
        self.round_one = []
        self.round_two = []
        self.round_three = []
        self.players = []
    
    def get_player_by_id(self, id):
        for p in self.players:
            if p.id == id:
                return p
        return None

    def to_json(self):
        return json.dumps(
            {
                "id": self.id,
                "meta": {
                    "date": f"{datetime.datetime.now().isoformat()}-5:00",
                    "title": self.title,
                    **({"tag": self.tag} if self.tag != "anti" and self.tag else {}),
                    **({"description": self.description} if self.description else {}),
                    **({"host": self.host} if self.host else {}),
                    **({"cube_id": self.cube_id} if self.cube_id else {}),
                    **({"set_code": self.set_code} if self.set_code else {}),
                },
                "R_0": [{"players": [p.player_one.id, p.player_two.id if p.player_two is not None else None], "games": [p.game_one, p.game_two, p.game_three]} for p in self.round_one],
                "R_1": [{"players": [p.player_one.id, p.player_two.id if p.player_two is not None else None], "games": [p.game_one, p.game_two, p.game_three]} for p in self.round_two],
                "R_2": [{"players": [p.player_one.id, p.player_two.id if p.player_two is not None else None], "games": [p.game_one, p.game_two, p.game_three]} for p in self.round_three],
            }
        )

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

    def stats(self, player_id) -> (float, float):
        game_total = 0
        score_total = 0
        wins_total = 0
        m_one = self.match_one(SwissPlayer(player_id))
        m_two = self.match_two(SwissPlayer(player_id))
        m_three = self.match_three(SwissPlayer(player_id))
        if m_one is not None:
            score, _, games, wins = m_one.score(SwissPlayer(player_id))
            game_total += games
            score_total += score
            wins_total += wins
        if m_two is not None:
            score, _, games, wins = m_one.score(SwissPlayer(player_id))
            game_total += games
            score_total += score
            wins_total += wins
        if m_three is not None:
            score, _, games, wins = m_one.score(SwissPlayer(player_id))
            game_total += games
            score_total += score
            wins_total += wins
        return wins_total / game_total, score_total

    def secondary_stats(self, player_id) -> (float, float):
        gwp, mwp = self.stats(player_id)
        opponent_total = 0
        gwp_sum = 0
        mwp_sum = 0
        o_one = self.match_one(SwissPlayer(player_id)).opponent(SwissPlayer(player_id))
        o_two = self.match_two(SwissPlayer(player_id)).opponent(SwissPlayer(player_id))
        o_three = self.match_three(SwissPlayer(player_id)).opponent(SwissPlayer(player_id))
        if o_one is not None:
            gwp, mwp = self.stats(SwissPlayer(player_id))
            gwp_sum += gwp
            mwp_sum += mwp
            opponent_total += 1
        if o_two is not None:
            gwp, mwp = self.stats(SwissPlayer(player_id))
            gwp_sum += gwp
            mwp_sum += mwp
            opponent_total += 1
        if o_three is not None:
            gwp, mwp = self.stats(SwissPlayer(player_id))
            gwp_sum += gwp
            mwp_sum += mwp
            opponent_total += 1
        return mwp, gwp, gwp_sum / opponent_total, mwp_sum / opponent_total

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
        p1_score, _, _, _ = self.score(self.player_one)
        p2_score, _, _, _ = self.score(self.player_two)
        return f"{self.player_one} vs {self.player_two} -> {self.player_one if p1_score > p2_score else self.player_two if not self.is_tie() else self.player_two}"

    def is_tie(self) -> bool:
        if (self.game_one == self.player_one or self.game_one == self.player_two) and self.game_one != self.game_two and self.game_three is None:
            return True
        if self.game_one is None and self.game_two is None:
            return True
        return False

    def is_bye(self) -> bool:
        return self.player_two is None
    
    def has_player(self, player):
        return self.player_one == player or self.player_two == player

    def opponent(self, player) -> Union[SwissPlayer, None]:
        if player == self.player_one:
            return self.player_two
        if player == self.player_two:
            return self.player_one
        return None

    def score(self, player) -> (int, int, int, int):
        """match points, priority, games played, games won"""
        if player is None:
            return 0, 0, 0, 0
        if self.is_bye():
            return 3, 3, 0, 0
        if self.is_tie():
            return 1, 0, (1 if self.game_one is not None else 0) + (1 if self.game_two is not None else 0), (1 if self.game_one == player else 0) + (1 if self.game_two == player else 0)
        if player == self.game_one and player == self.game_two:
            return 3, 4, 2, 2
        if player == self.game_two and player == self.game_three:
            return 3, 2, 3, 2
        if player == self.game_one and player == self.game_three:
            return 3, 1, 3, 2
        return 0, 0, 0, 0


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
        c = 0
        for pairing in drft.round_three:
            if pairing.player_two is None:
                c += 1
            if len(drft.players) > 4:
                assert c < 2
        print("----------")

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

    test(8, after_round_one=test_first_pairs([["1", "5"], ["2", "6"], ["3", "7"], ["4", "8"]]))
    test(8, after_round_one=drop_seat(0))
    test(8, after_round_two=drop_seat(1))
    test(8, after_round_two=drop_ids(["1", "2"]))
    test(8, after_round_two=drop_ids(["1", "2", "3"]))
    test(8, after_round_two=drop_ids(["1", "2", "3", "4"]))
    test(8, after_round_one=drop_ids(["1", "4"]), after_round_two=drop_ids(["2", "7"]))
    test(7)
    test(6)
    test(6, after_round_one=drop_ids(["1"]))
