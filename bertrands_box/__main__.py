#! /usr/bin/env python3

"""Console Entry Point for Bertrand's Box Utility."""

import logging
import sys

import click

from bertrands_box import simulate
from bertrands_box.cli import CLICK_CONTEXT, setup_logging


@click.command(context_settings=CLICK_CONTEXT)
@click.argument("ROUNDS", type=int, default=1000)
@click.option("-v", "--verbose", count=True)
def cli_main(rounds: int, verbose: int = 0) -> int:
    """
    Perform a Simulation of Bertrand's Box.

    ROUNDS is the number of rounds to simulate; defaults to 1000
    """
    args = locals().items()
    setup_logging(verbose)
    logger = logging.getLogger(__name__)
    logger.debug("Running with options: %s", ", ".join(f"{k!s}={v!r}" for k, v in args))

    simulate(rounds)

    return 0


if __name__ == "__main__":
    sys.exit(cli_main())
