import json
from draft_class import Draft

test_draft = Draft("test", "", "1", "anti", "", "", 3)
test_draft.add_player("1", is_host=True, p_id="1", seat=0)
test_draft.add_player("2", p_id="2", seat=1)
test_draft.add_player("3", p_id="3", seat=2)
test_draft.add_player("4", p_id="4", seat=3)
test_draft.add_player("5", p_id="5", seat=4)
test_draft.add_player("6", p_id="6", seat=5)
test_draft.add_player("7", p_id="7", seat=6)
test_draft.add_player("8", p_id="8", seat=7)
test_draft.finish_round()
for match in test_draft.rounds[0].matches:
    test_draft.parse_match(match.players[0].player_id, "0")
    print(f"{match.players} {match.gwinners}")
print('---------------')
test_draft.finish_round()
for match in test_draft.rounds[1].matches:
    test_draft.parse_match(match.players[0].player_id, "0")
    print(f"{match.players} {match.gwinners}")
print('---------------')
test_draft.finish_round()
for match in test_draft.rounds[2].matches:
    test_draft.parse_match(match.players[0].player_id, "0")
    print(f"{match.players} {match.gwinners}")
print('---------------')
test_draft.finish_round()
print(test_draft.players)
print(json.dumps(test_draft.tojson()))
print('---------------')
print('---------------')
print('---------------')
test_draft_2 = Draft("test", "", "1", "anti", "", "", 3)
test_draft_2.add_player("1", is_host=True, p_id="1", seat=0)
test_draft_2.add_player("2", p_id="2", seat=1)
test_draft_2.add_player("3", p_id="3", seat=2)
test_draft_2.add_player("4", p_id="4", seat=3)
test_draft_2.add_player("5", p_id="5", seat=4)
test_draft_2.add_player("6", p_id="6", seat=5)
test_draft_2.add_player("7", p_id="7", seat=6)
test_draft_2.add_player("8", p_id="8", seat=7)
test_draft_2.add_player("9", p_id="9", seat=8)
test_draft_2.add_player("10", p_id="10", seat=9)
test_draft_2.finish_round()
for match in test_draft_2.rounds[0].matches:
    test_draft_2.parse_match(match.players[0].player_id, "0")
    print(f"{match.players} {match.gwinners}")
print('---------------')
test_draft_2.drop_player('2')
test_draft_2.finish_round()
for match in test_draft_2.rounds[1].matches:
    test_draft_2.parse_match(match.players[0].player_id, "7")
    print(f"{match.players} {match.gwinners}")
print('---------------')
test_draft_2.drop_player('3')
test_draft_2.drop_player('4')
test_draft_2.finish_round()
for match in test_draft_2.rounds[2].matches:
    test_draft_2.parse_match(match.players[0].player_id, "0")
    print(f"{match.players} {match.gwinners}")
print('---------------')
test_draft_2.finish_round()
print(test_draft_2.players)
print(json.dumps(test_draft_2.tojson()))
print('---------------')
print('---------------')
print('---------------')
test_draft_3 = Draft("test", "", "1", "anti", "", "", 3)
test_draft_3.add_player("1", is_host=True, p_id="1", seat=0)
test_draft_3.add_player("2", p_id="2", seat=1)
test_draft_3.add_player("3", p_id="3", seat=2)
test_draft_3.add_player("4", p_id="4", seat=3)
test_draft_3.add_player("5", p_id="5", seat=4)
test_draft_3.add_player("6", p_id="6", seat=5)
test_draft_3.finish_round()
for match in test_draft_3.rounds[0].matches:
    test_draft_3.parse_match(match.players[0].player_id, "0")
    print(f"{match.players} {match.gwinners}")
print('---------------')
test_draft_3.finish_round()
for match in test_draft_3.rounds[1].matches:
    test_draft_3.parse_match(match.players[0].player_id, "0")
    print(f"{match.players} {match.gwinners}")
print('---------------')
test_draft_3.finish_round()
for match in test_draft_3.rounds[2].matches:
    test_draft_3.parse_match(match.players[0].player_id, "0")
    print(f"{match.players} {match.gwinners}")
print('---------------')
test_draft_3.finish_round()
print(test_draft_3.players)
print(json.dumps(test_draft_3.tojson()))
print('---------------')
print('---------------')
print('---------------')