from __future__ import annotations
from enum import Enum
from random import randrange
from typing import Set, Tuple, Optional


class Location:
    def __init__(self, x: int, y: int):
        self.x: int = x
        self.y: int = y

    def __add__(self, other: Location) -> Location:
        return Location(self.x + other.x, self.y + other.y)

    def __sub__(self, other: Location) -> Location:
        return Location(self.x - other.x, self.y - other.y)

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

    def __init__(self, name, location, game, score):
        self.name: str = name
        self.game: Game = game
        self.location: Location = location
        self.score: int = score
        self.move: Optional[Direction] = None

    def add_score(self) -> None:
        self.score += 1

    def __key(self) -> Tuple[str]:
        return tuple(self.name)

    def __hash__(self) -> int:
        return hash(self.__key())

    def __eq__(self, other) -> bool:
        if isinstance(other, Player):
            return self.__key() == other.__key()
        return NotImplemented


class Game:

    def __init__(self, width=8, height=8, apples=4, walls=8):
        self.width: int = width
        self.height: int = height
        self.apple_locs: Set[Location] = set()
        self.wall_locs: Set[Location] = set()
        self.players: Set[Player] = set()

        for _ in range(0, apples):
            self._spawn_apple()

        for _ in range(0, walls):
            self._create_walls()

    def register(self, name: str) -> Player:
        player = Player(name, self._free_location(), self, 0)

        if player in self.players:
            raise ValueError("Player name has already been taken")

        self.players.add(player)

        return player

    def _spawn_apple(self) -> None:
        self.apple_locs.add(self._free_location())

    def _create_walls(self) -> None:
        self.wall_locs.add(self._free_location())

    def tick(self):
        for player in self.players:
            if not player.move:
                continue

            new_loc = player.location + player.move.value
            player.move = None

            if not self.contains_location(new_loc):
                continue

            if new_loc in self.wall_locs:
                continue

            if any(new_loc == p.location for p in self.players):
                continue

            player.location = new_loc

            if new_loc in self.apple_locs:
                self.apple_locs.remove(new_loc)
                self._spawn_apple()
                player.add_score()

    def contains_location(self, location: Location) -> bool:
        return 0 <= location.x < self.width and 0 <= location.y < self.height

    def running(self) -> bool:
        # return not any(player.score > 50 for player in self.players)
        # return len(self.apple_locs) != 0
        return True

    def _free_location(self) -> Location:
        while True:
            random_x = randrange(0, self.width)
            random_y = randrange(0, self.height)

            rand_loc = Location(random_x, random_y)

            if rand_loc in self.apple_locs:
                continue

            if rand_loc in self.wall_locs:
                continue

            if any(rand_loc == p.location for p in self.players):
                continue

            return rand_loc

    def __str__(self):
        board = [[' '] * self.width for _ in range(self.height)]

        for apple_loc in self.apple_locs:
            board[apple_loc.y][apple_loc.x] = '*'

        for wall_loc in self.wall_locs:
            board[wall_loc.y][wall_loc.x] = '■'

        for player in self.players:
            board[player.location.y][player.location.x] = player.name

        game_stage = '\n'.join(' '.join(row) for row in board)

        score_board = ' || '.join(f"{p.name}: {p.score}" for p in self.players)

        return '\n'.join([game_stage, score_board])
