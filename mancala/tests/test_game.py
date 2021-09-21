import unittest
from mancala.game import Game


class TestInit(unittest.TestCase):

    def test_player(self):
        self.assertEqual(Game().turn_player(), 1)

    def test_player(self):
        self.assertEqual(Game(None, 1).turn_player(), 1)

    def test_player(self):
        self.assertEqual(Game(None, 2).turn_player(), 2)

    def test_score(self):
        self.assertEqual(Game().score(), (0, 0))

    def test_history(self):
        self.assertEqual(Game().history(), [])

    def test_over(self):
        self.assertFalse(Game().over())

    def test_board(self):
        self.assertEqual(Game().board_render(),
                         """     4  4  4  4  4  4\n  0                    0 \n     4  4  4  4  4  4""")

    def test_board_raw(self):
        self.assertEqual(Game()._board,
                         [4, 4, 4, 4, 4, 4, 0, 4, 4, 4, 4, 4, 4, 0])


class TestMoves(unittest.TestCase):

    def test_move_00(self):
        g = Game()
        g.move(0)
        self.assertEqual(g._board,
                         [0, 5, 5, 5, 5, 4, 0, 4, 4, 4, 4, 4, 4, 0])
        self.assertEqual(g.score(), (0, 0))
        self.assertEqual(g.turn_player(), 2)
        self.assertEqual(g.history(), [
            [4, 4, 4, 4, 4, 4, 0, 4, 4, 4, 4, 4, 4, 0]
        ])


    def test_move_01(self):
        g = Game()
        g.move(1)
        self.assertEqual(g._board,
                         [4, 0, 5, 5, 5, 5, 0, 4, 4, 4, 4, 4, 4, 0])
        self.assertEqual(g.turn_player(), 2)
        self.assertEqual(g.history(), [
            [4, 4, 4, 4, 4, 4, 0, 4, 4, 4, 4, 4, 4, 0]
        ])

    def test_move_04(self):
        g = Game()
        g.move(4)
        self.assertEqual(g._board,
                         [4, 4, 4, 4, 0, 5, 1, 5, 5, 4, 4, 4, 4, 0])
        self.assertEqual(g.score(), (1, 0))
        self.assertEqual(g.turn_player(), 2)
        self.assertEqual(g.history(), [
            [4, 4, 4, 4, 4, 4, 0, 4, 4, 4, 4, 4, 4, 0]
        ])

    def test_move_11(self):
        g = Game()
        g.move(0)
        g.move(11)
        self.assertEqual(g._board,
                         [1, 6, 5, 5, 5, 4, 0, 4, 4, 4, 4, 0, 5, 1])
        self.assertEqual(g.score(), (0, 1))
        self.assertEqual(g.turn_player(), 1)
        self.assertEqual(g.history(), [
            [4, 4, 4, 4, 4, 4, 0, 4, 4, 4, 4, 4, 4, 0],
            [0, 5, 5, 5, 5, 4, 0, 4, 4, 4, 4, 4, 4, 0]
        ])

class TestOwnZone(unittest.TestCase):

    def test_player1(self):
        for i in range(0,6):
            self.assertTrue(Game.idx_player_1(i))
        for i in range(-50,0):
            self.assertFalse(Game.idx_player_1(i))
        for i in range(6,200):
            self.assertFalse(Game.idx_player_1(i))

    def test_player2(self):
        for i in range(-20,7):
            self.assertFalse(Game.idx_player_2(i))
        for i in range(7,13):
            self.assertTrue(Game.idx_player_2(i))
        for i in range(13,200):
            self.assertFalse(Game.idx_player_2(i))

    def test_own_zone(self):
        for i in range(-50, 50):
            self.assertEqual(Game.own_zone(i, True),
                             Game.idx_player_1(i))
            self.assertEqual(Game.own_zone(i, False),
                             Game.idx_player_2(i))

class TestIllegalMove(unittest.TestCase):

    def test_Illegal_empty(self):
        g = Game()
        g.move(0)
        g.move(7)
        g.move(0)
        self.assertEqual(g._board,
                         [0, 5, 5, 5, 5, 4, 0, 0, 5, 5, 5, 5, 4, 0])
        self.assertEqual(g.score(), (0, 0))
        self.assertEqual(g.turn_player(), 1)

    def test_Illegal_score_p1(self):
        g = Game()
        g.move(6)
        self.assertEqual(g._board,
                         [4, 4, 4, 4, 4, 4, 0, 4, 4, 4, 4, 4, 4, 0])
        self.assertEqual(g.score(), (0, 0))
        self.assertEqual(g.turn_player(), 1)

    def test_Illegal_score_p2(self):
        g = Game()
        g.move(13)
        self.assertEqual(g._board,
                         [4, 4, 4, 4, 4, 4, 0, 4, 4, 4, 4, 4, 4, 0])
        self.assertEqual(g.score(), (0, 0))
        self.assertEqual(g.turn_player(), 1)

    def test_Illegal_p1_choose_wrong(self):
        g = Game()
        g.move(7)
        self.assertEqual(g._board,
                         [4, 4, 4, 4, 4, 4, 0, 4, 4, 4, 4, 4, 4, 0])
        self.assertEqual(g.score(), (0, 0))
        self.assertEqual(g.turn_player(), 1)

    def test_Illegal_p2_choose_wrong(self):
        g = Game()
        g.move(0)
        g.move(2)
        self.assertEqual(g._board,
                         [0, 5, 5, 5, 5, 4, 0, 4, 4, 4, 4, 4, 4, 0])
        self.assertEqual(g.score(), (0, 0))
        self.assertEqual(g.turn_player(), 2)

class TestMoveAgain(unittest.TestCase):

    def test_last_in_end_p1(self):
        g = Game()
        g.move(2)
        self.assertEqual(g._board,
                         [4, 4, 0, 5, 5, 5, 1, 4, 4, 4, 4, 4, 4, 0])
        self.assertEqual(g.score(), (1, 0))
        self.assertEqual(g.turn_player(), 1)

    def test_last_in_end_p2(self):
        g = Game()
        g.move(0)
        g.move(9)
        self.assertEqual(g._board,
                         [0, 5, 5, 5, 5, 4, 0, 4, 4, 0, 5, 5, 5, 1])
        self.assertEqual(g.score(), (0, 1))
        self.assertEqual(g.turn_player(), 2)

class TestCapture(unittest.TestCase):

    def test_capture_p1_okay(self):
        g = Game()
        g._board = [1,0,0,4,0,0,0,2,3,0,0,1,0,0]
        g.move(0)
        self.assertEqual(g._board,
                         [0, 0, 0, 4, 0, 0, 2, 2, 3, 0, 0, 0, 0, 0])
        self.assertEqual(g.score(), (2, 0))
        self.assertEqual(g.turn_player(), 2)

    def test_capture_p2_okay(self):
        g = Game()
        g._board = [1,0,0,1,0,0,0,2,3,0,0,1,0,0]
        g._player_one = False
        g.move(11)
        self.assertEqual(g._board,
                         [0, 0, 0, 1, 0, 0, 0, 2, 3, 0, 0, 0, 0, 2])
        self.assertEqual(g.score(), (0, 2))
        self.assertEqual(g.turn_player(), 1)

    def test_capture_p1_not_okay_opp_side(self):
        g = Game()
        g._board = [1,0,0,4,1,3,0,2,0,0,0,1,0,0]
        g.move(5)
        self.assertEqual(g._board,
                         [1, 0, 0, 4, 1, 0, 1, 3, 1, 0, 0, 1, 0, 0])
        self.assertEqual(g.score(), (1, 0))
        self.assertEqual(g.turn_player(), 2)

    def test_capture_p2_not_okay_opp_side(self):
        g = Game()
        g._board = [1,0,0,1,0,0,0,2,3,0,0,1,0,0]
        g._player_one = False
        g.move(11)
        self.assertEqual(g._board,
                         [0, 0, 0, 1, 0, 0, 0, 2, 3, 0, 0, 0, 0, 2])
        self.assertEqual(g.score(), (0, 2))
        self.assertEqual(g.turn_player(), 1)

    def test_capture_p1_not_okay_empty_opp(self):
        g = Game()
        g._board = [1,0,0,0,0,1,2,1,0,0,0,0,1,2]
        g.move(0)
        self.assertEqual(g._board,
                         [0,1,0,0,0,1,2,1,0,0,0,0,1,2])
        self.assertEqual(g.score(), (2, 2))
        self.assertEqual(g.turn_player(), 2)

    def test_capture_p2_not_okay_empty_opp(self):
        g = Game()
        g._board = [1,0,0,0,0,1,2,1,0,0,0,0,1,2]
        g._player_one = False
        g.move(7)
        self.assertEqual(g._board,
                         [1,0,0,0,0,1,2,0,1,0,0,0,1,2])
        self.assertEqual(g.score(), (2, 2))
        self.assertEqual(g.turn_player(), 1)

    def test_capture_p1_not_okay_grand_slam(self):
        g = Game()
        g._board = [1,0,0,0,0,1,1,0,0,0,0,1,0,1]
        g.move(0)
        self.assertEqual(g._board,
                         [0,1,0,0,0,1,1,0,0,0,0,1,0,1])
        self.assertEqual(g.score(), (1, 1))
        self.assertEqual(g.turn_player(), 2)

    def test_capture_p2_not_okay_grand_slam(self):
        g = Game()
        g._board = [1,0,0,0,0,0,1,1,0,0,0,1,0,1]
        g._player_one = False
        g.move(11)
        self.assertEqual(g._board,
                         [1,0,0,0,0,0,1,1,0,0,0,0,1,1])
        self.assertEqual(g.score(), (1, 1))
        self.assertEqual(g.turn_player(), 1)


    def test_capture_score_not_okay(self):
        g = Game()
        g._board = [1,1,1,1,1,1,0,1,1,1,1,1,1,5]
        g.move(5)
        self.assertEqual(g._board,
                         [1,1,1,1,1,0,1,1,1,1,1,1,1,5])
        self.assertEqual(g.score(), (1, 5))
        self.assertEqual(g.turn_player(), 1)

class TestGameEnd(unittest.TestCase):

    def test_p1_Win_exact(self):
        g = Game()
        g._board = [1,0,0,0,0,1,24,0,0,0,0,0,3,5]
        g.move(5)
        self.assertEqual(g._board,
                         [1, 0, 0, 0, 0, 0, 25, 0, 0, 0, 0, 0, 3, 5])
        self.assertEqual(g.score(), (25, 5))
        self.assertTrue(g.over())

    def test_p1_Win_over(self):
        g = Game()
        g._board = [1,0,0,0,15,1,24,0,0,0,0,0,3,5]
        g.move(4)
        self.assertEqual(g._board,
                         [2, 1, 1, 1, 1, 3, 26, 1, 1, 1, 1, 1, 4, 5])
        self.assertEqual(g.score(), (26, 5))
        self.assertTrue(g.over())

    def test_p2_Win_exact(self):
        g = Game()
        g._board = [1,0,0,0,0,1,5,1,0,0,0,0,1,24]
        g._player_one = False
        g.move(12)
        self.assertEqual(g._board,
                         [1, 0, 0, 0, 0, 1, 5, 1, 0, 0, 0, 0, 0, 25])
        self.assertEqual(g.score(), (5, 25))
        self.assertTrue(g.over())

    def test_p2_Win_over(self):
        g = Game()
        g._board = [1,0,0,0,0,1,5,1,0,0,0,0,15,24]
        g._player_one = False
        g.move(12)
        self.assertEqual(g._board,
                         [3, 1, 1, 1, 1, 2, 5, 2, 1, 1, 1, 1, 1, 26])
        self.assertEqual(g.score(), (5, 26))
        self.assertTrue(g.over())

    def test_side_01_empty(self):
        g = Game()
        g._board = [0,0,0,0,0,4,20,5,0,0,0,0,10,13]
        g.move(5)
        self.assertEqual(g._board,
                         [0,0,0,0,0,0,21,0,0,0,0,0,0,31])
        self.assertEqual(g.score(), (21, 31))
        self.assertTrue(g.over())

    def test_side_02_empty(self):
        g = Game()
        g._board = [1,0,0,0,0,7,20,0,0,0,0,0,3,10]
        g._player_one = False
        g.move(12)
        self.assertEqual(g._board,
                         [0,0,0,0,0,0,30,0,0,0,0,0,0,11])
        self.assertEqual(g.score(), (30, 11))
        self.assertTrue(g.over())


class TestGameClone(unittest.TestCase):

    def game_equality(self, g_left, g_right):
        """Test if game objects are equal"""
        self.assertListEqual(g_left.board(), g_right.board())
        self.assertListEqual(g_left.history(), g_right.history())
        self.assertListEqual(g_left.moves(), g_right.moves())
        self.assertEqual(g_left.turn_player(), g_right.turn_player())

    def test_init(self):
        g = Game()
        g_dolly = g.clone()
        self.game_equality(g, g_dolly)

    def test_move_each(self):
        g = Game()
        g_dolly = g.clone()
        g.move(2)
        g_dolly.move(2)
        self.game_equality(g, g_dolly)

    def test_move_once(self):
        g = Game()
        g.move(2)
        g_dolly = g.clone()
        self.game_equality(g, g_dolly)


if __name__ == '__main__':
    unittest.main()
