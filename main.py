import time
import curses
from typing import List, Type

from model.bot import RandomBot, SimpleGreedyBot, BotInterface, NonDeterministicGreedyBot, BreadthFirstBot
from model.game import Player, Game

stdscr = curses.initscr()
stdscr.nodelay(True)

game: Game = Game(width=64, height=32, apples=1000, walls=128)
bots: List[BotInterface] = []


def register_player(name: str, bot_class: Type[BotInterface]):
    bots.append(bot_class(game.register(name)))


register_player('C', BreadthFirstBot)
register_player('U', BreadthFirstBot)
register_player('T', BreadthFirstBot)
register_player('E', BreadthFirstBot)
register_player('B', BreadthFirstBot)
register_player('O', BreadthFirstBot)
register_player('N', BreadthFirstBot)
register_player('S', BreadthFirstBot)

while game.running():
    for bot in bots:
        bot.solve()

    player_moves = " || ".join(f"{p.name}: {p.move}" for p in game.players) + '\n'

    game.tick()

    stdscr.addstr(0, 0, player_moves)
    stdscr.addstr(3, 0, str(game))

    stdscr.refresh()

    time.sleep(0.2)

    if stdscr.getch() == 3:
        break

curses.endwin()