import game2048
import random

class BotPlayer:
    def __init__(self, bot):

        if 'decide_move' not in dir(bot):
            raise ValueError('bot must have "decide_move" method')

        self.bot = bot

    def play(self):
        ''' 
        Runs bot over game until game over. Returns the game
        '''
        while self.bot.game.get_playing():
            move = self.bot.decide_move()
            self.bot.game.swipe(move)

    def get_game(self):
        return self.game

class RandomBot:
    def __init__(self, game):
        if not isinstance(game, game2048.Game):
            raise TypeError('game must be of type Game defined in game2048.py')

        self.game = game
    
    def decide_move(self):
        ''' Returns up, down, left, right '''
        valid_moves = self.game.get_valid_moves().copy()
        if len(valid_moves) == 0:
            return 'quit'

        choice = random.choice(valid_moves)

        return choice

class OrderBot:
    '''
    Simply has a preferred order of directions to swipe.
    Will try each direction until one works.
    Default will try and build from bottom corner.
    '''
    def __init__(self, game):
        if not isinstance(game, game2048.Game):
            raise TypeError('game must be of type Game defined in game2048.py')

        self.game = game
    
    def decide_move(self):
        ''' Returns up, down, left, right '''
        valid_moves = self.game.get_valid_moves().copy()
        preference = ['right', 'down', 'left', 'up']

        if len(valid_moves) == 0:
            return 'quit'

        for direction in preference:
            if direction in valid_moves:
                choice = direction
                break

        return choice

class LowerRightBot:
    '''
    Very similar to OrderBot, but tries to swipe down after swiping right
    '''
    def __init__(self, game):
        if not isinstance(game, game2048.Game):
            raise TypeError('game must be of type Game defined in game2048.py')

        self.game = game
        self.prev_move = ''
    
    def decide_move(self):
        ''' Returns up, down, left, right '''
        valid_moves = self.game.get_valid_moves().copy()
        preference = ['right', 'down', 'left', 'up']

        if len(valid_moves) == 0:
            return 'quit'

        if self.prev_move == 'right':
            if 'right' in valid_moves:
                valid_moves.remove('right') 

        for direction in preference:
            if direction in valid_moves:
                choice = direction
                break

        return choice

# game_1 = game2048.Game()

# rule_bot = LowerRightBot(game_1)
# bot_player = BotPlayer(game_1, rule_bot)
# bot_player.play()