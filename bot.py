import game2048
import random

class BotPlayer:
	def __init__(self, game, bot):
		if not isinstance(game, game2048.Game):
			raise TypeError('game must be of type Game defined in game2048.py')

		if 'decide_move' not in dir(bot):
			raise ValueError('bot must have "decide_move" method')

		self.game = game
		self.bot = bot

	def play(self):
		''' 
		Runs bot over game until game over. Returns the game
		'''
		while self.game.get_playing():
			move = self.bot.decide_move()
			self.game.swipe(move)

	def get_game(self):
		return self.game

class RandomBot:
	def __init__(self, game):
		if not isinstance(game, game2048.Game):
			raise TypeError('game must be of type Game defined in game2048.py')

		self.game = game
	
	def decide_move(self):
		''' Returns up, down, left, right '''
		valid_moves = self.game.get_valid_moves()
		if len(valid_moves) == 0:
			return 'quit'

		choice = random.choice(valid_moves)

		return choice


game_1 = game2048.Game()
random_bot = RandomBot(game_1)

bot_player = BotPlayer(game_1, random_bot)
bot_player.play()
print(bot_player.get_game())
