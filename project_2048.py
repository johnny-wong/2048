# -*- coding: utf-8 -*-
"""
Created on Wed Jul 18 19:06:31 2018

@author: Johnny Wong
"""


def test_combine():
	# no change
	assert(combine([0,0,0,0]) == ([0,0,0,0], 0))
	assert(combine([2,0,0,0]) == ([2,0,0,0], 0))
	assert(combine([2,4,8,16]) == ([2,4,8,16], 0))
	assert(combine([2,4,0,0]) == ([2,4,0,0], 0))
	assert(combine([2,4,8,16,32])) == ([2, 4, 8, 16, 32], 0)
	
	# one combine
	assert(combine([2,2,0,0]) == ([4,0,0,0], 4))
	assert(combine([2,2,2,0]) == ([4,2,0,0], 4))
	assert(combine([4,4,2,8]) == ([8,2,8,0], 8))
	assert(combine([2,4,4,8]) == ([2,8,8,0], 8))
	assert(combine([2,4,8,8]) == ([2,4,16,0], 16))
	assert(combine([2,4,8,8, 2]) == ([2,4,16,2,0], 16))
	
	# two combine
	assert(combine([2,2,2,2]) == ([4,4,0,0], 8))
	assert(combine([2,2,4,4]) == ([4,8,0,0], 12))
	assert(combine([8,8,4,4]) == ([16,8,0,0], 24))
	assert(combine([1,8,8,4,4,1]) == ([1,16,8,1,0, 0], 24))

	# Three combine
	assert(combine([1,8,8,1,4,4,2,2,4]) == ([1,16,1,8,4,4,0,0,0], 28))

	print('Combine tests passed!')

# test_combine()
def testShift():
	# no combine
	assert(shift([0, 0, 0, 1, 2, 4]) == ([1, 2, 4, 0, 0, 0], 0))
	assert(shift([1, 2, 4, 0]) == ([1, 2, 4, 0], 0))
	
	# one combine
	assert(shift([1, 2, 2, 0]) == ([1, 4, 0, 0], 4))
	assert(shift([1, 0, 2, 2]) == ([1, 4, 0, 0], 4))
	assert(shift([0, 1, 0, 1]) == ([2, 0, 0, 0], 2))
	
	# two combine
	assert(shift([0, 1, 0, 1, 2, 0, 2]) == ([2, 4, 0, 0, 0, 0, 0], 6))
	
	# three combine
	assert(shift([1, 1, 1, 1, 1, 1]) == ([2, 2, 2, 0, 0, 0], 6))
	
	print('All tests passed!')
	
# testShift()

class game:
	def __init__(self, width=4, height=4):
		self.array = [[0]*width for _ in range(height)]
		self.score = 0
		self.valid_move = True
		self.width = width
		self.height = height

	def _combine(self, array):
		'''
		Takes in an array of numbers, and assumes they are combined to the left.
		Returns the new array and the sum of any combined numbers.
		Assumes the 0s are already on the right. i.e. everything is already shifted.
		'''
		# Create a new array of the same size
		newArray = [0] * len(array)
		pointer = 0
		new_pointer = 0
		new_sum = 0
		
		while ((pointer < (len(array) - 1)) and (array[pointer] != 0)):
			first_num = array[pointer]
			second_num = array[pointer + 1]
			if first_num == second_num:
				# update number in newArray
				newArray[new_pointer] = first_num * 2
				
				# update pointer and new_pointer
				pointer += 2
				new_pointer += 1
				
				# add to sum
				new_sum += first_num * 2
			else:
				# when numbers don't match
				newArray[new_pointer] = array[pointer]

				# Update pointers
				new_pointer += 1
				pointer += 1

				if pointer == (len(array)-1):
					# Special case when it's the last two numbers
					newArray[new_pointer] = array[pointer]

		if pointer == len(array) - 1:
			# the last number
			newArray[new_pointer] = array[pointer]

		return newArray, new_sum

	def _shift(self, array):
		'''
		Shifts the array to the left and combines, returns new array and 
		sum of any combined numbers
		'''
		lengthArray = len(array)
		newArray = [0] * lengthArray
		pointer = 0
		newPointer = 0
		
		while pointer < lengthArray:
			if array[pointer] == 0:
				pointer += 1
			else:
				newArray[newPointer] = array[pointer]
				pointer += 1
				newPointer += 1

		while newPointer < lengthArray:
			newArray[newPointer] = 0
			newPointer += 1
			
		newArray, newSum = self._combine(newArray)
		
		# Check if ANYTHING changed
		array_changed = False
		i = 0

		while (i < len(array)) and not array_changed:
			if array[i] != newArray[i]:
				array_changed = True
			i += 1

		if not array_changed:
			new_sum = None

		return newArray, newSum

	def __repr__(self):
		'''
		Shows the score with the current board position.

		>>> board_1 = game()
		>>> print(game)
		'''
		char_width = self.width * 5 + 1 # Width of printed string
		horiz_line = '-' * char_width # Horizontal line
		str_score = 'Score: {}\n'.format(self.score) # Score to display

		str_rep = str_score
		str_rep += horiz_line
		for row in self.array:
			str_rep += '\n|'
			for num in row:
				str_rep += '{:^4}|'.format(num)
			str_rep += '\n' + horiz_line

		return str_rep

	def __string__(self):
		''' same as __repr__ but without calling print statement
		>>> game_1 = game()
		>>> game_1
		'''

		return self.__repr__()

	def get_row(self, row_num, reverse=False):
		''' Returns the row as a list. Left to right by default'''

		# Checks that input is valid
		if not (0 <= row_num < self.height):
			raise ValueError('row_num must be between {} and {}'.format(0, self.height - 1))
		if not isinstance(reverse, bool):
			raise TypeError('reverse must be True or False')

		if reverse:
			row = self.array[row_num][::-1]
		else:
			row = self.array[row_num]

		return row

	def get_col(self, col_num, reverse=False):
		''' Returns the col as a list. Top to bottom by default '''

		# Checks that input is valid
		if not (0 <= col_num < self.width):
			raise ValueError('row_num must be between {} and {}'.format(0, self.height - 1))
		if not isinstance(reverse, bool):
			raise TypeError('reverse must be True or False')

		col = [None] * self.height
		
		for row_idx, row in enumerate(self.array):
			col[row_idx] = row[col_num]

		if reverse:
			col = col[::-1]

		return col

	def change_num(self, row, col, new_num):
		''' Changes a specific number in the board '''
		if not (0 <= row < self.height):
			raise ValueError('row must be between {} and {}'.format(0, self.height - 1))
		elif not (0 <= col < self.width):
			raise ValueError('col must be between {} and {}'.format(0, self.width - 1))
		
		self.array[row][col] = new_num
		return None

	def change_row(self, row, new, reverse=False):
		''' Changes a specific row '''

		# Checks valid argument
		if not (0 <= row < self.height):
			raise ValueError('row must be between {} and {}'.format(0, self.height - 1))
		elif len(new) != self.width:
			raise ValueError('new row must be a list of length {}'.format(self.width))

		if reverse:
			new = new[::-1]

		self.array[row] = new

	def change_col(self, col, new, reverse=False):
		''' Changes a specific column '''
		# Checks valid argument
		if not (0 <= col < self.width):
			raise ValueError('col must be between {} and {}'.format(0, self.width - 1))
		elif len(new) != self.height:
			raise ValueError('new row must be a list of length {}'.format(self.height))

		if reverse:
			new = new[::-1]
		
		for idx, row in enumerate(self.array):
			row[col] = new[idx]

	def swipe(self, direction):
		'''
		Changes entire board, updates score. direction in (up, down, left, right)
		'''

	def swipe_horiz(self, direction):
		'''
		Left or right swipes
		'''
		if direction not in ('left', 'right'):
			raise ValueError('direction must be "left" or "right")')

		if direction == 'left':
			reverse_value = False
		else:
			reverse_value = True

		for idx in range(len(self.array)):
			old_row = self.get_row(idx, reverse_value)
			new_row, new_sum = self._shift(old_row)
			self.change_row(idx, new_row, reverse_value)

			if new_sum not in [None, 0]:
				self.score += new_sum

game_1 = game()
print(game_1)
game_1.change_row(0, [2,4,8,16])
print(game_1)
game_1.change_col(2, [4, 2, 4, 16], True)
print(game_1)
game_1.swipe_horiz('right')
print(game_1)