import time

from model.model import Player, Game

game = Game()
print(game)
print('=' * 66)
player_1 = Player('A', game)
print(game)
print('=' * 66)

player_2 = Player('B', game)
print(game)
print('=' * 66)

player_3 = Player('C', game)
print(game)
print('=' * 66)

game.spawn_apple()
game.spawn_apple()
game.spawn_apple()
game.spawn_apple()

while True:
    game.tick()
    print(game)
    print('=' * 66)
    time.sleep(0.5)