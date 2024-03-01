"""A Simulation of Bertrand's Box."""

__author__ = """Matthew Wyant"""
__email__ = "me@zanfar.com"
__copyright__ = "Copyright 2024, Matthew Wyant"
__credits__ = [__author__]
__license__ = "GPL-3.0-plus"
__version__ = "0.1.0"
__version_info__ = (0, 1, 0)
__maintainer__ = __author__
__status__ = "Prototype"


import random
from dataclasses import dataclass, field
from enum import Enum, auto
from math import floor, log
from typing import NamedTuple, Sequence


class Coin(int, Enum):
    """Possible Coin Types."""

    GOLD = auto()
    SILVER = auto()


@dataclass
class BoxDef:
    """Box Details."""

    name: str
    coins: list[Coin] = field(default_factory=list)


class DrawResult(NamedTuple):
    """Results of one Draw (Round)."""

    box_name: str
    first_coin: Coin
    second_coin: Coin


DEFAULT_ROUNDS = 1_000

BOXES = [
    BoxDef("A", [Coin.GOLD, Coin.GOLD]),
    BoxDef("B", [Coin.GOLD, Coin.SILVER]),
    BoxDef("C", [Coin.SILVER, Coin.SILVER]),
]


def perform_draw(boxes: Sequence[BoxDef]) -> DrawResult:
    """Perform a draw."""
    box = random.choice(boxes)
    coins = box.coins.copy()
    random.shuffle(coins)

    return DrawResult(
        box.name,
        coins[0],
        coins[1],
    )


def simulate(rounds: int = DEFAULT_ROUNDS) -> None:
    """Perform the N-round Simulation and Print the Results."""
    box_counts = {b.name: 0 for b in BOXES}
    first_coin_counts = {c: 0 for c in Coin}
    second_coin_counts = {c: 0 for c in Coin}
    coin_counts = {first: {second: 0 for second in Coin} for first in Coin}

    count_len = floor(log(rounds) / log(10)) + 1
    coin_len = max(len(c.name) for c in Coin)

    for _ in range(rounds):
        result = perform_draw(BOXES)

        box_counts[result.box_name] += 1
        first_coin_counts[result.first_coin] += 1
        second_coin_counts[result.second_coin] += 1
        coin_counts[result.first_coin][result.second_coin] += 1

    print(f"In {rounds} drawings:")

    print()
    for box_name, box_count in sorted(box_counts.items()):
        print(
            f"Box {box_name:1s}: {box_count:{count_len}d} "
            f"({box_count/rounds*100:4.2f}%)",
        )

    print()
    for coin, count in sorted(first_coin_counts.items()):
        print(
            f"First Draw {coin.name:{coin_len}s}: {count:{count_len}d} "
            f"({count/rounds*100:4.2f}%)",
        )

    print()
    for coin, count in sorted(second_coin_counts.items()):
        print(
            f"Second Draw {coin.name:{coin_len}s}: {count:{count_len}d} "
            f"({count/rounds*100:4.2f}%)",
        )

    for first_coin, second_results in sorted(coin_counts.items()):
        subtotal = sum(second_results.values())

        print()
        for second_coin, second_count in sorted(second_results.items()):
            print(
                f"{first_coin.name:{coin_len}s} -> {second_coin.name:{coin_len}s}: "
                f"{second_count:{count_len}d} ({second_count/subtotal*100:4.2f}%)",
            )
