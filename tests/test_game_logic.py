"""Tests for game_logic.py fixes: player-tile sync, anti-pushback, end-game."""
import pytest
from board import Board
from game_logic import LabyrinthEnv, Player


def make_env():
    return LabyrinthEnv(Board())


# ---------------------------------------------------------------------------
# Bug 1: Player-tile sync on push
# ---------------------------------------------------------------------------

class TestPlayerTileSync:

    def test_player_moves_left_with_row(self):
        env = make_env()
        env.players[0].position = (1, 3)
        env.step(1, {'type': 'push', 'direction': 'left', 'position': 1})
        assert env.players[0].position == (1, 2)

    def test_player_moves_right_with_row(self):
        env = make_env()
        env.players[0].position = (3, 2)
        env.step(1, {'type': 'push', 'direction': 'right', 'position': 3})
        assert env.players[0].position == (3, 3)

    def test_player_moves_up_with_column(self):
        env = make_env()
        env.players[0].position = (4, 1)
        env.step(1, {'type': 'push', 'direction': 'up', 'position': 1})
        assert env.players[0].position == (3, 1)

    def test_player_moves_down_with_column(self):
        env = make_env()
        env.players[0].position = (2, 3)
        env.step(1, {'type': 'push', 'direction': 'down', 'position': 3})
        assert env.players[0].position == (3, 3)

    def test_player_not_on_pushed_row_stays(self):
        env = make_env()
        env.players[0].position = (2, 4)  # row 2, not row 1
        env.step(1, {'type': 'push', 'direction': 'left', 'position': 1})
        assert env.players[0].position == (2, 4)

    def test_player_wraps_when_pushed_off_left(self):
        env = make_env()
        env.players[0].position = (1, 0)
        env.step(1, {'type': 'push', 'direction': 'left', 'position': 1})
        assert env.players[0].position == (1, 6)

    def test_player_wraps_when_pushed_off_right(self):
        env = make_env()
        env.players[0].position = (3, 6)
        env.step(1, {'type': 'push', 'direction': 'right', 'position': 3})
        assert env.players[0].position == (3, 0)

    def test_player_wraps_when_pushed_off_top(self):
        env = make_env()
        env.players[0].position = (0, 1)
        env.step(1, {'type': 'push', 'direction': 'up', 'position': 1})
        assert env.players[0].position == (6, 1)

    def test_player_wraps_when_pushed_off_bottom(self):
        env = make_env()
        env.players[0].position = (6, 3)
        env.step(1, {'type': 'push', 'direction': 'down', 'position': 3})
        assert env.players[0].position == (0, 3)

    def test_multiple_players_on_same_row_all_move(self):
        env = make_env()
        env.players[0].position = (1, 1)
        env.players[1].position = (1, 4)
        env.step(1, {'type': 'push', 'direction': 'left', 'position': 1})
        assert env.players[0].position == (1, 0)
        assert env.players[1].position == (1, 3)


# ---------------------------------------------------------------------------
# Bug 2: Anti-pushback check
# ---------------------------------------------------------------------------

class TestAntiPushback:

    def test_immediate_reverse_push_raises(self):
        env = make_env()
        env.step(1, {'type': 'push', 'direction': 'left', 'position': 1})
        with pytest.raises(ValueError, match="No pushback allowed"):
            env.step(1, {'type': 'push', 'direction': 'right', 'position': 1})

    def test_reverse_push_different_lane_is_allowed(self):
        env = make_env()
        env.step(1, {'type': 'push', 'direction': 'left', 'position': 1})
        # Reverse direction but different lane — should not raise
        env.step(2, {'type': 'push', 'direction': 'right', 'position': 3})

    def test_same_direction_same_lane_is_allowed(self):
        env = make_env()
        env.step(1, {'type': 'push', 'direction': 'left', 'position': 1})
        # Same direction is not a pushback
        env.step(2, {'type': 'push', 'direction': 'left', 'position': 1})

    def test_up_down_pushback_raises(self):
        env = make_env()
        env.step(1, {'type': 'push', 'direction': 'up', 'position': 3})
        with pytest.raises(ValueError, match="No pushback allowed"):
            env.step(2, {'type': 'push', 'direction': 'down', 'position': 3})

    def test_first_push_always_allowed(self):
        env = make_env()
        # last_push starts as None; any push must be valid
        env.step(1, {'type': 'push', 'direction': 'right', 'position': 5})

    def test_anti_pushback_resets_each_turn(self):
        env = make_env()
        env.step(1, {'type': 'push', 'direction': 'left', 'position': 1})
        env.step(2, {'type': 'push', 'direction': 'left', 'position': 3})
        # Now the last push was left/3, so right/1 should be allowed
        env.step(3, {'type': 'push', 'direction': 'right', 'position': 1})


# ---------------------------------------------------------------------------
# Bug 3: End-game / home-base return
# ---------------------------------------------------------------------------

class TestEndGame:

    def test_is_done_returns_false_initially(self):
        env = make_env()
        done, winner = env.is_done()
        assert done is False
        assert winner is None

    def test_is_done_false_when_tokens_collected_but_not_home(self):
        env = make_env()
        player = env.players[0]
        player.cards.clear()
        player.current_card = 'HOME'
        player.position = (3, 3)  # not at home (0,0)
        done, winner = env.is_done()
        assert done is False

    def test_is_done_true_when_at_home_with_home_card(self):
        env = make_env()
        player = env.players[0]
        player.cards.clear()
        player.current_card = 'HOME'
        player.position = player.home  # (0, 0)
        done, winner = env.is_done()
        assert done is True
        assert winner == player.id

    def test_collect_token_sets_home_sentinel_on_last_card(self):
        env = make_env()
        player = env.players[0]
        # Give the player exactly one card and simulate collecting it
        last_token = player.current_card
        player.cards = __import__('collections').deque([last_token])
        player.current_card = last_token
        # Place that token on tile (2, 2) temporarily
        env.board.tiles[2][2].token = last_token
        player.collect_token(last_token)
        assert player.current_card == 'HOME'
        assert len(player.cards) == 0

    def test_player_home_positions_are_correct(self):
        env = make_env()
        homes = {p.id: p.home for p in env.players}
        assert homes[1] == (0, 0)
        assert homes[2] == (0, 6)
        assert homes[3] == (6, 0)
        assert homes[4] == (6, 6)

    def test_winner_is_correct_player(self):
        env = make_env()
        # Make player 3 the winner
        p3 = env.players[2]
        p3.cards.clear()
        p3.current_card = 'HOME'
        p3.position = p3.home
        done, winner = env.is_done()
        assert done is True
        assert winner == 3
