from __future__ import annotations

import random
from collections import namedtuple
from typing import List, Optional, Set, FrozenSet

from model.game import Player, Direction, Location


class BotInterface:

    def __init__(self, player: Player):
        self.player = player
        self.game = player.game

    def solve(self) -> None:
        pass


class RandomBot(BotInterface):

    def solve(self) -> None:
        self.player.move = random.choice(list(Direction))


class SimpleGreedyBot(BotInterface):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._apples_snapshot: FrozenSet[Location] = frozenset()
        self._best_apple: Optional[Location] = None

    def solve(self) -> None:
        vector: Location = self._best_apple_loc() - self.player.location
        possible_moves: List[Direction] = self._possible_moves(vector)
        self.player.move = self._choose_move(possible_moves)

    @staticmethod
    def _choose_move(possible_moves: List[Direction]) -> Optional[Direction]:
        if possible_moves:
            return possible_moves[0]
        return None

    @staticmethod
    def _possible_moves(vector: Location) -> List[Direction]:
        possible_moves: List[Direction] = []

        if vector.x < 0:
            possible_moves.append(Direction.LEFT)
        elif vector.x > 0:
            possible_moves.append(Direction.RIGHT)

        if vector.y < 0:
            possible_moves.append(Direction.UP)
        elif vector.y > 0:
            possible_moves.append(Direction.DOWN)

        return possible_moves

    def _best_apple_loc(self) -> Location:
        if self._apples_snapshot != self.game.apple_locs:
            self._apples_snapshot = frozenset(self.game.apple_locs)
            self._best_apple = min(self.game.apple_locs,
                                   key=lambda loc: loc.distance(self.player.location),
                                   default=None)

        return self._best_apple


class NonDeterministicGreedyBot(SimpleGreedyBot):

    @staticmethod
    def _choose_move(possible_moves: List[Direction]) -> Optional[Direction]:
        if possible_moves:
            return random.choice(possible_moves)
        return None


class BreadthFirstBot(BotInterface):

    class Node:
        def __init__(self, parent: Optional[BreadthFirstBot.Node], location: Location):
            self.parent = parent
            self.location = location

    def __init__(self, player: Player):
        super().__init__(player)
        self._apples_snapshot: FrozenSet[Location] = frozenset()
        self._instructions: List[Location] = []

    def solve(self):
        if self._apples_snapshot != self.game.apple_locs:
            self._apples_snapshot = frozenset(self.game.apple_locs)
            self._instructions = self._path_to_closest_apple()

        if not self._instructions:
            return

        if self._instructions[-1] == self.player.location:
            self._instructions.pop()

        self.player.move = Direction(self._instructions[-1] - self.player.location)

    def _path_to_closest_apple(self) -> List[Location]:
        visited_locs: Set[Location] = set()
        frontier: List[BreadthFirstBot.Node] = [BreadthFirstBot.Node(None, self.player.location)]

        while frontier:
            new_frontier = []

            for node in frontier:
                for direction in Direction:
                    new_loc: Location = node.location + direction.value

                    if not self.game.contains_location(new_loc):
                        continue

                    if new_loc in self.game.wall_locs:
                        continue

                    if new_loc in visited_locs:
                        continue

                    visited_locs.add(new_loc)

                    new_node = BreadthFirstBot.Node(node, new_loc)

                    if new_loc in self.game.apple_locs:
                        path: List[Location] = []

                        while new_node:
                            path.append(new_node.location)
                            new_node = new_node.parent

                        return path

                    new_frontier.append(new_node)

            frontier = new_frontier

        return []








