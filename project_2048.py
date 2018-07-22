# -*- coding: utf-8 -*-
"""
Created on Wed Jul 18 19:06:31 2018

@author: Johnny Wong
"""
   

def combine(array):
	# Create a new array of the same size
	newArray = [0] * len(array)
	pointer = 0
	new_pointer = 0
	new_sum = 0
	
	while ((pointer < (len(array) - 1)) and (array[pointer] != 0)):
		first_num = array[pointer]
		second_num = array[pointer + 1]
		if first_num == second_num:
			#print('there is a match with {} and {}'.format(pointer, pointer + 1))
			# update number in newArray
			newArray[new_pointer] = first_num * 2
			
			# update pointer and new_pointer
			pointer += 2
			new_pointer += 1
			
			# add to sum
			new_sum += first_num * 2
			#print('pointer = {}\nnew_pointer = {}'.format(pointer, new_pointer))
		else:
			#print('no match with {} and {}'.format(pointer, pointer + 1))
			# when numbers don't match
			newArray[new_pointer] = array[pointer]
			
			
			# Update pointers
			new_pointer += 1
			pointer += 1
			
			if pointer == (len(array)-1):
				#print('last two numbers don\'t match')
				# Special case when it's the last two numbers
				newArray[new_pointer] = array[pointer]
			#print('pointer = {}\nnew_pointer = {}'.format(pointer, new_pointer))
		
	if pointer == len(array) - 1:
		# the last number
		newArray[new_pointer] = array[pointer]
	#print('\n')
		
	return newArray, new_sum

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

	print('All tests passed!')

test_combine()

def shift(array):
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
		
	newArray, newSum = combine(newArray)
	
	return newArray, newSum

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
	
testShift()