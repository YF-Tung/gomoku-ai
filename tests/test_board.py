import unittest
from src.gomoku.board.board import Board
from src.gomoku.board.player import Player, PlayerType

class TestBoard(unittest.TestCase):
    def setUp(self):
        self.board = Board()

    def test_empty_board(self):
        for i in range(self.board.size):
            for j in range(self.board.size):
                self.assertEqual(self.board.board[i][j], 0)

    def test_make_move(self):
        self.assertTrue(self.board.make_move(7, 7))
        self.assertNotEqual(self.board.board[7][7], 0)
        self.assertFalse(self.board.make_move(7, 7))  # Can't move twice on same spot

    def test_win_horizontal(self):
        # Directly set up a horizontal win for black
        for i in range(5):
            self.board.board[7][i] = PlayerType.BLACK.value
        self.assertTrue(self.board.check_win(7, 4))

if __name__ == '__main__':
    unittest.main() 