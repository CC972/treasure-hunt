import curses
import statistics
import time
from typing import List, Type

from model.bot import BotInterface, BreadthFirstSearchBot, DepthFirstSearchBot
from model.game import Game, Direction

stdscr = curses.initscr()
stdscr.nodelay(True)
curses.noecho()
curses.start_color()
curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)

game: Game = Game(width=64, height=32, apples=16, walls=128)
bots: List[BotInterface] = []


def register_player(name: str, bot_class: Type[BotInterface]):
    bots.append(bot_class(game.register(name)))


register_player('C', DepthFirstSearchBot)
# register_player('U', BreadthFirstBot)
# register_player('T', BreadthFirstBot)
# register_player('E', BreadthFirstBot)
# register_player('B', BreadthFirstBot)
# register_player('O', BreadthFirstBot)
# register_player('N', BreadthFirstBot)
# register_player('S', BreadthFirstBot)

chi = game.register('L')
last_move = None

while game.running():
    for bot in bots:
        bot.execute()

    player_moves = " || ".join(f"{p.name}: {getattr(p.move, 'name', None)}" for p in game.players) + '\n'
    player_stats = " || ".join(f"{b.player.name}: {statistics.mean(b.times) * 1000:.3}" for b in bots) + '\n'
    player_scores = " || ".join(f"{p.name}: {p.score}" for p in game.players)

    game.tick()

    stdscr.addstr(0, 0, player_moves)
    stdscr.addstr(2, 0, player_stats)

    game_rows = str(game).split('\n')

    for y, row in enumerate(game_rows[:-1], start=5):
        for x, char in enumerate(row):
            # if char == ' ' and x and x < len(row) and row[x-1] == '■':
            #     char = '■'

            col_pair = curses.color_pair(3)
            if char == '*':
                col_pair = curses.color_pair(1)
            elif char == '■':
                col_pair = curses.color_pair(2)

            stdscr.addch(y, x, char, col_pair)

    stdscr.addstr(5 + len(game_rows) + 1, 0, game_rows[-1])

    stdscr.refresh()

    time.sleep(0.1)

    press = stdscr.getch()
    if press == 3:
        break
    elif press == ord('w'):
        last_move = Direction.UP
    elif press == ord('a'):
        last_move = Direction.LEFT
    elif press == ord('s'):
        last_move = Direction.DOWN
    elif press == ord('d'):
        last_move = Direction.RIGHT
    chi.move = last_move

time.sleep(2)
curses.endwin()