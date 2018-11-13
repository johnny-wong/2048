import game2048

def test_combine():
	game_1 = game2048.Game()

	# no change
	assert(game_1._combine([0,0,0,0]) == ([0,0,0,0], 0))
	assert(game_1._combine([2,0,0,0]) == ([2,0,0,0], 0))
	assert(game_1._combine([2,4,8,16]) == ([2,4,8,16], 0))
	assert(game_1._combine([2,4,0,0]) == ([2,4,0,0], 0))
	assert(game_1._combine([2,4,8,16,32])) == ([2, 4, 8, 16, 32], 0)
	
	# one combine
	assert(game_1._combine([2,2,0,0]) == ([4,0,0,0], 4))
	assert(game_1._combine([2,2,2,0]) == ([4,2,0,0], 4))
	assert(game_1._combine([4,4,2,8]) == ([8,2,8,0], 8))
	assert(game_1._combine([2,4,4,8]) == ([2,8,8,0], 8))
	assert(game_1._combine([2,4,8,8]) == ([2,4,16,0], 16))
	assert(game_1._combine([2,4,8,8, 2]) == ([2,4,16,2,0], 16))
	
	# two combine
	assert(game_1._combine([2,2,2,2]) == ([4,4,0,0], 8))
	assert(game_1._combine([2,2,4,4]) == ([4,8,0,0], 12))
	assert(game_1._combine([8,8,4,4]) == ([16,8,0,0], 24))
	assert(game_1._combine([1,8,8,4,4,1]) == ([1,16,8,1,0, 0], 24))

	# Three combine
	assert(game_1._combine([1,8,8,1,4,4,2,2,4]) == ([1,16,1,8,4,4,0,0,0], 28))

	print('Combine tests passed!')

def test_shift():
	game_1 = game2048.Game()
	# no combine
	assert(game_1._shift([0, 0, 0, 1, 2, 4]) == ([1, 2, 4, 0, 0, 0], 0))
	assert(game_1._shift([1, 2, 4, 0]) == ([1, 2, 4, 0], 0))
	
	# one combine
	assert(game_1._shift([1, 2, 2, 0]) == ([1, 4, 0, 0], 4))
	assert(game_1._shift([1, 0, 2, 2]) == ([1, 4, 0, 0], 4))
	assert(game_1._shift([0, 1, 0, 1]) == ([2, 0, 0, 0], 2))
	
	# two combine
	assert(game_1._shift([0, 1, 0, 1, 2, 0, 2]) == ([2, 4, 0, 0, 0, 0, 0], 6))
	
	# three combine
	assert(game_1._shift([1, 1, 1, 1, 1, 1]) == ([2, 2, 2, 0, 0, 0], 6))
	
	print('Shift tests passed!')
	
test_shift()
test_combine()
	