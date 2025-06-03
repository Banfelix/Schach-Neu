
import unittest
from engine.board import Board
from helpers.perft import perft 

class TestPerft(unittest.TestCase):
    def setUp(self):
        self.fen_data_1 = {"fen": "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1", "depth_1":20, "depth_2":400, "depth_3":8902}
        self.fen_data_3 = {"fen": "r3k2r/p1ppqpb1/bn2pnp1/3PN3/1p2P3/2N2Q1p/PPPBBPPP/R3K2R w KQkq -", "depth_1":48, "depth_2":2039}
        self.fen_data_2 = {"fen": "8/2p5/3p4/KP5r/1R3p1k/8/4P1P1/8 w - -", "depth_1":14, "depth_2":191, "depth_3":2812, "depth_4":43238}
        self.fen_data_4 = {"fen": "8/8/8/8/8/8/1k6/R3K3 b Q - 0 1", "depth_1":4, "depth_2":49, "depth_3":243, "depth_4":3991, "depth_5":20780}
        self.fen_data_5 = {"fen": "8/8/8/8/8/7K/7P/7k w - - 0 1", "depth_1":3, "depth_2":7, "depth_3":43, "depth_4":199, "depth_5":1347, "depth_6": 6249}
        self.fen_data_6 = {"fen": "r3k2r/Pppp1ppp/1b3nbN/nP6/BBP1P3/q4N2/Pp1P2PP/R2Q1RK1 w kq - 0 1", "depth_1":6, "depth_2":264, "depth_3":9467}
        self.fen_data_7 = {"fen": "k7/8/3p4/8/8/4P3/8/7K b - - 0 1", "depth_1":4, "depth_2":16, "depth_3":101, "depth_4":637, "depth_5":4271, "depth_6": 28662}
        self.fen_data_8 = {"fen": "8/8/3k4/3p4/3P4/3K4/8/8 w - - 0 ", "depth_1":5, "depth_2":25, "depth_3":180, "depth_4":1294, "depth_5":8296, "depth_6": 53138}
        print("Setup")

    def tearDown(self):
        print("Teardown")
    
    
    def test_fen_1(self):
        depth_keys = [k for k in self.fen_data_1 if k.startswith("depth_")]
        depths = sorted(int(k.split("_")[1]) for k in depth_keys)
        fen = self.fen_data_1["fen"]

        for depth in depths:
            key = f"depth_{depth}"
            board = Board(fen)
            result = perft(board, depth)
            expected = self.fen_data_1[key]

            self.assertEqual(
                result, expected,
                msg=f"Failed at depth {depth} for FEN:\n{fen}\nExpected: {expected}, Got: {result}")
            print(f"[PASS] Depth {depth}: {result} moves")
    
    
    def test_fen_2(self):
        depth_keys = [k for k in self.fen_data_2 if k.startswith("depth_")]
        depths = sorted(int(k.split("_")[1]) for k in depth_keys)
        fen = self.fen_data_2["fen"]

        for depth in depths:
            key = f"depth_{depth}"
            board = Board(fen)
            result = perft(board, depth)
            expected = self.fen_data_2[key]

            self.assertEqual(
                result, expected,
                msg=f"Failed at depth {depth} for FEN:\n{fen}\nExpected: {expected}, Got: {result}")
            print(f"[PASS] Depth {depth}: {result} moves")

    def test_fen_3(self):
        depth_keys = [k for k in self.fen_data_3 if k.startswith("depth_")]
        depths = sorted(int(k.split("_")[1]) for k in depth_keys)
        fen = self.fen_data_3["fen"]

        for depth in depths:
            key = f"depth_{depth}"
            board = Board(fen)
            result = perft(board, depth)
            expected = self.fen_data_3[key]

            self.assertEqual(
                result, expected,
                msg=f"Failed at depth {depth} for FEN:\n{fen}\nExpected: {expected}, Got: {result}")
            print(f"[PASS] Depth {depth}: {result} moves")

    def test_fen_4(self):
        depth_keys = [k for k in self.fen_data_4 if k.startswith("depth_")]
        depths = sorted(int(k.split("_")[1]) for k in depth_keys)
        fen = self.fen_data_4["fen"]

        for depth in depths:
            key = f"depth_{depth}"
            board = Board(fen)
            result = perft(board, depth)
            expected = self.fen_data_4[key]

            self.assertEqual(
                result, expected,
                msg=f"Failed at depth {depth} for FEN:\n{fen}\nExpected: {expected}, Got: {result}")
            print(f"[PASS] Depth {depth}: {result} moves")

    def test_fen_5(self):
        depth_keys = [k for k in self.fen_data_5 if k.startswith("depth_")]
        depths = sorted(int(k.split("_")[1]) for k in depth_keys)
        fen = self.fen_data_5["fen"]

        for depth in depths:
            key = f"depth_{depth}"
            board = Board(fen)
            result = perft(board, depth)
            expected = self.fen_data_5[key]

            self.assertEqual(
                result, expected,
                msg=f"Failed at depth {depth} for FEN:\n{fen}\nExpected: {expected}, Got: {result}")
            print(f"[PASS] Depth {depth}: {result} moves")

    def test_fen_6(self):
        depth_keys = [k for k in self.fen_data_6 if k.startswith("depth_")]
        depths = sorted(int(k.split("_")[1]) for k in depth_keys)
        fen = self.fen_data_6["fen"]

        for depth in depths:
            key = f"depth_{depth}"
            board = Board(fen)
            result = perft(board, depth)
            expected = self.fen_data_6[key]

            self.assertEqual(
                result, expected,
                msg=f"Failed at depth {depth} for FEN:\n{fen}\nExpected: {expected}, Got: {result}")
            print(f"[PASS] Depth {depth}: {result} moves")

    def test_fen_7(self):
        depth_keys = [k for k in self.fen_data_7 if k.startswith("depth_")]
        depths = sorted(int(k.split("_")[1]) for k in depth_keys)
        fen = self.fen_data_7["fen"]

        for depth in depths:
            key = f"depth_{depth}"
            board = Board(fen)
            result = perft(board, depth)
            expected = self.fen_data_7[key]

            self.assertEqual(
                result, expected,
                msg=f"Failed at depth {depth} for FEN:\n{fen}\nExpected: {expected}, Got: {result}")
            print(f"[PASS] Depth {depth}: {result} moves")

    def test_fen_8(self):
        depth_keys = [k for k in self.fen_data_8 if k.startswith("depth_")]
        depths = sorted(int(k.split("_")[1]) for k in depth_keys)
        fen = self.fen_data_8["fen"]

        for depth in depths:
            key = f"depth_{depth}"
            board = Board(fen)
            result = perft(board, depth)
            expected = self.fen_data_8[key]

            self.assertEqual(
                result, expected,
                msg=f"Failed at depth {depth} for FEN:\n{fen}\nExpected: {expected}, Got: {result}")
            print(f"[PASS] Depth {depth}: {result} moves")


if __name__ == "__main__":
    unittest.main()
