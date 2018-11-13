import game2048
import unittest

class TestSwipes(unittest.TestCase):

	def test_combine(self):
		game_1 = game2048.Game()

		# no change
		self.assertEqual(game_1._combine([0,0,0,0]), ([0,0,0,0], 0))
		self.assertEqual(game_1._combine([2,0,0,0]), ([2,0,0,0], 0))
		self.assertEqual(game_1._combine([2,4,8,16]), ([2,4,8,16], 0))
		self.assertEqual(game_1._combine([2,4,0,0]), ([2,4,0,0], 0))
		self.assertEqual(game_1._combine([2,4,8,16,32]), ([2, 4, 8, 16, 32], 0))
		
		# one combine
		self.assertEqual(game_1._combine([2,2,0,0]), ([4,0,0,0], 4))
		self.assertEqual(game_1._combine([2,2,2,0]), ([4,2,0,0], 4))
		self.assertEqual(game_1._combine([4,4,2,8]), ([8,2,8,0], 8))
		self.assertEqual(game_1._combine([2,4,4,8]), ([2,8,8,0], 8))
		self.assertEqual(game_1._combine([2,4,8,8]), ([2,4,16,0], 16))
		self.assertEqual(game_1._combine([2,4,8,8, 2]), ([2,4,16,2,0], 16))
		
		# two combine
		self.assertEqual(game_1._combine([2,2,2,2]), ([4,4,0,0], 8))
		self.assertEqual(game_1._combine([2,2,4,4]), ([4,8,0,0], 12))
		self.assertEqual(game_1._combine([8,8,4,4]), ([16,8,0,0], 24))
		self.assertEqual(game_1._combine([1,8,8,4,4,1]), ([1,16,8,1,0, 0], 24))

		# Three combine
		self.assertEqual(game_1._combine([1,8,8,1,4,4,2,2,4]), ([1,16,1,8,4,4,0,0,0], 28))

	def test_shift(self):
		game_1 = game2048.Game()
		# no combine
		self.assertEqual(game_1._shift([0, 0, 0, 1, 2, 4]), ([1, 2, 4, 0, 0, 0], 0))
		self.assertEqual(game_1._shift([1, 2, 4, 0]), ([1, 2, 4, 0], 0))
		
		# one combine
		self.assertEqual(game_1._shift([1, 2, 2, 0]), ([1, 4, 0, 0], 4))
		self.assertEqual(game_1._shift([1, 0, 2, 2]), ([1, 4, 0, 0], 4))
		self.assertEqual(game_1._shift([0, 1, 0, 1]), ([2, 0, 0, 0], 2))
		
		# two combine
		self.assertEqual(game_1._shift([0, 1, 0, 1, 2, 0, 2]), ([2, 4, 0, 0, 0, 0, 0], 6))
		
		# three combine
		self.assertEqual(game_1._shift([1, 1, 1, 1, 1, 1]), ([2, 2, 2, 0, 0, 0], 6))

class TestEndgame(unittest.TestCase):
	def test_no_moves_shift(self):
		''' Tests move shift validity'''
		# No empty spaces to move at all
		game_1 = game2048.Game()
		game_1.change_row(0, [2, 4, 2, 4])
		game_1.change_row(1, [4, 2, 4, 2])
		game_1.change_row(2, [2, 4, 2, 4])
		game_1.change_row(3, [4, 2, 4, 2])

		self.assertEqual(game_1.valid_moves_shift(), (False, False, False, False))
		
		# One empty space in corner
		game_1.change_row(0, [0, 4, 2, 4])
		game_1.change_row(1, [4, 2, 4, 2])
		game_1.change_row(2, [2, 4, 2, 4])
		game_1.change_row(3, [4, 2, 4, 2])

		self.assertEqual(game_1.valid_moves_shift(), (True, False, True, False))

		# One empty space on edge
		game_1.change_row(0, [2, 4, 2, 4])
		game_1.change_row(1, [0, 2, 4, 2])
		game_1.change_row(2, [2, 4, 2, 4])
		game_1.change_row(3, [4, 2, 4, 2])

		self.assertEqual(game_1.valid_moves_shift(), (True, True, True, False))

		# One empty space in centre
		game_1.change_row(0, [2, 4, 2, 4])
		game_1.change_row(1, [4, 0, 4, 2])
		game_1.change_row(2, [2, 4, 2, 4])
		game_1.change_row(3, [4, 2, 4, 2])

		self.assertEqual(game_1.valid_moves_shift(), (True, True, True, True))

	def test_no_move_combine(self):
		''' Test moves for combine validity'''
		game_1 = game2048.Game()

		# Nothing to combine
		game_1.change_row(0, [2, 4, 2, 4])
		game_1.change_row(1, [4, 2, 4, 2])
		game_1.change_row(2, [2, 4, 2, 4])
		game_1.change_row(3, [4, 2, 4, 2])

		self.assertEqual(game_1.valid_moves_combine(), (False, False, False, False))

		# Something to combine but have to shift
		game_1.change_row(0, [2, 4, 2, 4])
		game_1.change_row(1, [4, 0, 4, 2])
		game_1.change_row(2, [2, 4, 2, 4])
		game_1.change_row(3, [4, 2, 4, 2])

		self.assertEqual(game_1.valid_moves_combine(), (False, False, False, False))

		# Combine vertically
		game_1.change_row(0, [2, 8, 2, 4])
		game_1.change_row(1, [4, 8, 4, 2])
		game_1.change_row(2, [2, 4, 2, 4])
		game_1.change_row(3, [4, 2, 4, 2])

		self.assertEqual(game_1.valid_moves_combine(), (True, True, False, False))

		# Combine horizontally
		game_1.change_row(0, [2, 8, 8, 4])
		game_1.change_row(1, [4, 2, 4, 2])
		game_1.change_row(2, [2, 4, 2, 4])
		game_1.change_row(3, [4, 2, 4, 2])

		self.assertEqual(game_1.valid_moves_combine(), (False, False, True, True))

		# Combine both ways
		game_1.change_row(0, [2, 4, 2, 4])
		game_1.change_row(1, [4, 4, 4, 2])
		game_1.change_row(2, [2, 4, 2, 4])
		game_1.change_row(3, [4, 2, 4, 2])

		self.assertEqual(game_1.valid_moves_combine(), (True, True, True, True))

	def test_overall_valid(self):
		game_1 = game2048.Game()

		# Invalid everywhere
		game_1.change_row(0, [2, 4, 2, 4])
		game_1.change_row(1, [4, 2, 4, 2])
		game_1.change_row(2, [2, 4, 2, 4])
		game_1.change_row(3, [4, 2, 4, 2])
		game_1.update_valid_moves()
		self.assertEqual(game_1.valid_udlr, (False, False, False, False))

		# Valid vertical
		game_1.change_row(0, [8, 4, 2, 4])
		game_1.change_row(1, [8, 2, 4, 2])
		game_1.change_row(2, [2, 4, 2, 4])
		game_1.change_row(3, [4, 2, 4, 2])
		game_1.update_valid_moves()
		self.assertEqual(game_1.valid_udlr, (True, True, False, False))

		# Valid horizontal
		game_1.change_row(0, [8, 8, 2, 4])
		game_1.change_row(1, [4, 2, 4, 2])
		game_1.change_row(2, [2, 4, 2, 4])
		game_1.change_row(3, [4, 2, 4, 2])
		game_1.update_valid_moves()
		self.assertEqual(game_1.valid_udlr, (False, False, True, True))

		# Valid everywhere
		game_1.change_row(0, [8, 8, 2, 4])
		game_1.change_row(1, [4, 4, 4, 2])
		game_1.change_row(2, [2, 4, 2, 4])
		game_1.change_row(3, [4, 2, 4, 2])
		game_1.update_valid_moves()
		self.assertEqual(game_1.valid_udlr, (True, True, True, True))		

		# Valid right up only
		game_1.change_row(0, [2, 4, 2, 0])
		game_1.change_row(1, [4, 2, 4, 2])
		game_1.change_row(2, [2, 4, 2, 4])
		game_1.change_row(3, [4, 2, 4, 2])
		game_1.update_valid_moves()
		self.assertEqual(game_1.valid_udlr, (True, False, False, True))

		# Valid down left only
		game_1.change_row(0, [2, 4, 2, 4])
		game_1.change_row(1, [4, 2, 4, 2])
		game_1.change_row(2, [2, 4, 2, 4])
		game_1.change_row(3, [0, 2, 4, 2])
		game_1.update_valid_moves()
		self.assertEqual(game_1.valid_udlr, (False, True, True, False))

		# Not valid up
		game_1.change_row(0, [2, 4, 2, 4])
		game_1.change_row(1, [4, 2, 4, 2])
		game_1.change_row(2, [2, 4, 2, 4])
		game_1.change_row(3, [4, 0, 4, 2])
		game_1.update_valid_moves()
		self.assertEqual(game_1.valid_udlr, (False, True, True, True))

		# Not valid down
		game_1.change_row(0, [2, 4, 0, 4])
		game_1.change_row(1, [4, 2, 4, 2])
		game_1.change_row(2, [2, 4, 2, 4])
		game_1.change_row(3, [4, 2, 4, 2])
		game_1.update_valid_moves()
		self.assertEqual(game_1.valid_udlr, (True, False, True, True))

		# Not valid left
		game_1.change_row(0, [2, 4, 2, 4])
		game_1.change_row(1, [4, 2, 4, 2])
		game_1.change_row(2, [2, 4, 2, 0])
		game_1.change_row(3, [4, 2, 4, 2])
		game_1.update_valid_moves()
		self.assertEqual(game_1.valid_udlr, (True, True, False, True))

		# Not valid right
		game_1.change_row(0, [2, 4, 2, 4])
		game_1.change_row(1, [4, 2, 4, 2])
		game_1.change_row(2, [0, 4, 2, 4])
		game_1.change_row(3, [4, 2, 4, 2])
		game_1.update_valid_moves()
		self.assertEqual(game_1.valid_udlr, (True, True, True, False))

if __name__ == '__main__':
    unittest.main()