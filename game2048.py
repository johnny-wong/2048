# -*- coding: utf-8 -*-
"""
Created on Wed Jul 18 19:06:31 2018

@author: Johnny Wong
"""

import random

class Game:
	def __init__(self, width=4, height=4):
		self.array = [[0] * width for _ in range(height)]
		self.score = 0
		self.playing = True
		self.width = width
		self.height = height
		# Up, down, left, right move validity
		self.valid_udlr = (True, True, True, True)

		# Generate 2 numbers randomly to start
		self.generate_random()
		self.generate_random()

		self.update_valid_moves()

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

		str_rep += '\n'
		return str_rep

	def __string__(self):
		''' 
		same as __repr__ but without calling print statement
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
		Changes entire board, updates score. direction in (up, down, left, right, quit)
		'''
		if direction not in ['up', 'down', 'left', 'right', 'quit']:
			raise ValueError('direction must be up, down, left, right, quit')


		if direction == 'quit':
			self.end_game()
			return None
		elif direction in ['up', 'down']:
			self.swipe_vert(direction)
		elif direction in ['left', 'right']:
			self.swipe_horiz(direction)

		self.generate_random()
		self.update_valid_moves()

		print(self)

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

		for idx in range(self.height):
			old_row = self.get_row(idx, reverse_value)
			new_row, new_sum = self._shift(old_row)
			self.change_row(idx, new_row, reverse_value)

			self.score += new_sum

	def swipe_vert(self, direction):
		'''
		Up or down swipes
		'''
		if direction not in ('up', 'down'):
			raise ValueError('direction must be "up" or "down")')

		if direction == 'up':
			reverse_value = False
		else:
			reverse_value = True

		for idx in range(self.width):
			old_col = self.get_col(idx, reverse_value)
			new_col, new_sum = self._shift(old_col)
			self.change_col(idx, new_col, reverse_value)

			self.score += new_sum

	def generate_random(self):
		'''
		Randomly generates a 2 or 4 and puts it in a random empty space. 
		If no spaces available, returns the string 'end'
		'''
		num_empty, empty_coords = self.count_empty()

		if num_empty == 0:
			return 'End'

		if random.random() < 0.2:
			new_num = 4
		else:
			new_num = 2
		
		placement = random.randint(0, num_empty-1)

		row, col = empty_coords[placement]

		self.change_num(row, col, new_num) 

	def count_empty(self):
		'''
		Count the number of empty places on the board. Returns the number of 
		empty spaces and a list of the coordinates of those empty spaces.
		'''
		empty_coords = []
		count = 0
		for row_idx, row in enumerate(self.array):
			for col_idx, num in enumerate(row):
				if num == 0:
					count += 1
					empty_coords.append((row_idx, col_idx))

		return count, empty_coords

	def get_next_move(self):
		''' Get the user's input. Will ignore any unrecognised commands'''
		possible_moves = ('up', 'down', 'left', 'right')
		valid_moves = [direction for direction, valid in zip(possible_moves, 
			self.valid_udlr) if valid]

		if len(valid_moves) == 0:
			# No more valid moves
			return 'quit'

		next_move = None
		while (next_move not in valid_moves) and (next_move != 'quit'):
			next_move = input('What is your next move? (up, down, left, right, quit)\n')

		return next_move

	def start_game(self):
		print(self)
		while self.playing == True:
			next_move = self.get_next_move()
			self.swipe(next_move)

	def update_valid_moves(self):
		''' Update what the available moves are from the current position'''
		shift_valid = self.valid_moves_shift()
		combine_valid = self.valid_moves_combine()

		valid_overall = tuple(shift or combine for shift, combine in zip(
			shift_valid, combine_valid))

		self.valid_udlr = valid_overall

	def valid_moves_combine(self):
		''' Checks whether a move is valid due to being able to combine with 
		adjacent tile. Returns a tuple with the up, down, left, right validity'''

		# Only need to check to the right and down 1, so only check for the upper left
		horiz_valid = False
		vert_valid = False

		# row and column indexes
		row = 0
		col = 0

		while (not (horiz_valid and vert_valid)) and (row < self.height):
			col = 0
			while (not (horiz_valid and vert_valid)) and (col < self.width):
				tile_value = self.array[row][col]

				if ((not horiz_valid) and 
					(col != self.width - 1)): # Can't/don't need to check last col
					right_tile = self.array[row][col + 1]
					if tile_value == right_tile:
						horiz_valid = True
				
				if ((not vert_valid) and 
					(row != self.height - 1)): # Can't/don't need to check last row
					down_tile = self.array[row + 1][col]
					if tile_value == down_tile:
						vert_valid = True

				col += 1
			row += 1

		up_valid = vert_valid
		down_valid = vert_valid
		left_valid = horiz_valid
		right_valid = horiz_valid

		return up_valid, down_valid, left_valid, right_valid

	def valid_moves_shift(self):
		''' Checks whether a move is valid due to being able to shift. 
		Returns a tuple with the up, down, left, right validity'''
		num_empty, empty_coords = self.count_empty()

		up_valid = False
		down_valid = False
		left_valid = False
		right_valid = False

		if num_empty == 0:
			return False, False, False, False
		else:
			for coord in empty_coords:
				row = coord[0]
				col = coord[1]

				if not up_valid:
					if row < self.height - 1:
						up_valid = True

				if not down_valid:
					if row > 0:
						down_valid = True

				if not left_valid:
					if col < self.width - 1:
						left_valid = True

				if not right_valid:
					if col > 0:
						right_valid = True

				if up_valid and down_valid and left_valid and right_valid:
					break

		return up_valid, down_valid, left_valid, right_valid
	
	def end_game(self):
		''' Prints end game message'''
		print('GAME OVER, final score: {}'.format(self.score))
		self.playing = False
		print(self)

if __name__ == '__main__':

	game_1 = Game(width=3, height=2)
	game_1.start_game()
