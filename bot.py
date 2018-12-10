import game2048

class bot:
	def __init__(self, game):
		if not isinstance(game, game2048.Game):
			raise TypeError('game must be of type Game defined in game2048.py')

		self.game = game
	
	def decide_move(self):
		pass


game_1 = game2048.Game()
bot_1 = bot(game_1)

