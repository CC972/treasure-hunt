from enum import Enum
from random import randrange
from typing import Dict, Set, Tuple


class Location:
    def __init__(self, x: int, y: int):
        self.x: int = x
        self.y: int = y

    def __add__(self, other):
        return Location(self.x + other.x, self.y + other.y)

    def __key(self) -> Tuple[int, int]:
        return self.x, self.y

    def __hash__(self) -> int:
        return hash(self.__key())

    def __eq__(self, other) -> bool:
        if isinstance(other, Location):
            return self.__key() == other.__key()
        return NotImplemented


class Direction(Enum):
    UP = Location(0, -1)
    DOWN = Location(0, 1)
    LEFT = Location(-1, 0)
    RIGHT = Location(1, 0)


class Player:

    def __init__(self, name, game):
        self.name = name
        self.game = game

        game.register(self)

    def move(self) -> Direction:
        return [Direction.UP, Direction.DOWN, Direction.LEFT, Direction.RIGHT][randrange(0, 4)]

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        return self.name == other.name


class Game:

    def __init__(self, width=8, height=8):
        self.width = width
        self.height = height
        self.apple_locs: Set[Location] = set()
        self.player_locs: Dict[Player, Location] = dict()

    def register(self, player: Player) -> None:
        if player in self.player_locs:
            raise ValueError("player name has already been taken")

        self.player_locs[player] = self._free_location()

    def spawn_apple(self) -> None:
        self.apple_locs.add(self._free_location())

    def tick(self) -> None:
        for player, player_loc in self.player_locs.items():
            new_loc = player_loc + player.move().value

            if not self._game_contains(new_loc):
                continue

            if new_loc in self.player_locs.values():
                continue

            if new_loc in self.apple_locs:
                self.apple_locs.remove(new_loc)
                # self.spawn_apple()

            self.player_locs[player] = new_loc

    def _game_contains(self, location: Location) -> bool:
        return 0 <= location.x < self.width and 0 <= location.y < self.height

    def _free_location(self) -> Location:
        while True:
            random_x = randrange(0, self.width)
            random_y = randrange(0, self.height)

            rand_loc = Location(random_x, random_y)

            if rand_loc in self.apple_locs:
                continue

            if rand_loc in self.player_locs.values():
                continue

            return rand_loc

    def __str__(self):
        board = [[' '] * self.width for _ in range(self.height)]

        for apple_loc in self.apple_locs:
            board[apple_loc.y][apple_loc.x] = '*'

        for player, player_loc in self.player_locs.items():
            board[player_loc.y][player_loc.x] = player.name

        return '\n'.join('|| ' + ' '.join(row) + ' ||' for row in board)
