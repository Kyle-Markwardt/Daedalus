"""Tests for board.py fixes."""
import pytest
from board import Board, Tile


class TestExcessTilePool:
    """Bug 4: excess tile must come from the 34-tile shuffled pool, not hardcoded 'straight'."""

    def test_excess_tile_is_not_always_straight(self):
        # Run many inits — the excess tile type should vary across games
        types_seen = set()
        for _ in range(50):
            b = Board()
            types_seen.add(b.excess_tile.type)
        assert len(types_seen) > 1, "Excess tile is always 'straight'; pool fix not applied"

    def test_excess_tile_counts_tiles_correctly(self):
        # Board has 49 cells, 16 fixed → 33 movable on board + 1 excess = 34 movable tiles total
        b = Board()
        on_board = sum(1 for row in b.tiles for tile in row if tile is not None)
        assert on_board == 49, f"Expected 49 tiles on board, got {on_board}"
        assert b.excess_tile is not None

    def test_excess_tile_has_valid_type(self):
        for _ in range(20):
            b = Board()
            assert b.excess_tile.type in ('straight', 'corner', 'T')

    def test_excess_tile_orientation_is_valid(self):
        for _ in range(20):
            b = Board()
            assert b.excess_tile.orientation in (0, 90, 180, 270)


class TestPushRowAndColumn:
    """Sanity checks that push mechanics are still correct after the excess tile fix."""

    def setup_method(self):
        self.board = Board()

    def test_push_row_left_shifts_tiles(self):
        row = 1
        original_col1 = self.board.tiles[row][1]
        self.board.push_tile('left', row)
        assert self.board.tiles[row][0] is original_col1

    def test_push_row_right_shifts_tiles(self):
        row = 3
        original_col5 = self.board.tiles[row][5]
        self.board.push_tile('right', row)
        assert self.board.tiles[row][6] is original_col5

    def test_push_column_up_shifts_tiles(self):
        col = 1
        original_row1 = self.board.tiles[1][col]
        self.board.push_tile('up', col)
        assert self.board.tiles[0][col] is original_row1

    def test_push_column_down_shifts_tiles(self):
        col = 3
        original_row5 = self.board.tiles[5][col]
        self.board.push_tile('down', col)
        assert self.board.tiles[6][col] is original_row5
