import unittest
from engine.piecelist import PieceList  


class TestPieceList(unittest.TestCase):

    def setUp(self):
        self.piecelist = PieceList()

    def test_initial_state(self):
        self.assertEqual(len(self.piecelist), 0)

    def test_add_piece(self):
        self.piecelist.addPiece(10)
        self.assertEqual(len(self.piecelist), 1)
        self.piecelist.addPiece(32)
        self.assertEqual(len(self.piecelist), 2)
        self.assertEqual(self.piecelist[0], 10)
        self.assertEqual(self.piecelist[1], 32)
        self.assertEqual(self.piecelist.map[10], 0)
        self.assertEqual(self.piecelist.map[32], 1)

    def test_remove_piece(self):
        self.piecelist.addPiece(12)
        self.piecelist.addPiece(20)
        self.piecelist.removePiece(12)
        self.assertEqual(len(self.piecelist), 1)
        self.assertEqual(self.piecelist[0], 20)
        self.assertEqual(self.piecelist.map[12], 0)
        self.assertNotIn(12, self.piecelist.occupied_squares)
        self.assertNotIn(12, self.piecelist.map)

    def test_move_piece(self):
        self.piecelist.addPiece(2)
        self.piecelist.addPiece(5)
        self.piecelist.movePiece(5, 25)
        self.assertEqual(self.piecelist[1], 25)
        self.assertEqual(self.piecelist.map[25], 1)
        self.assertNotIn(5, self.piecelist.occupied_squares)
        self.assertNotIn(5, self.piecelist.map)

    def test_get_item(self):
        self.piecelist.addPiece(33)
        self.assertEqual(self.piecelist[0], 33)

if __name__ == "__main__":
    unittest.main()