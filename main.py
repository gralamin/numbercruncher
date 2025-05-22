import logging
import argparse
import sys

from util import setup_logging
from cardservice import get_set
from crunch import crunch

logger = logging.getLogger(__name__)


def create_parser():
    """Creates an ArgumentParser for the script."""
    parser = argparse.ArgumentParser(
        description="Number crunch a given set for a different Card."
    )

    parser.add_argument(
        "--set",
        "-s",
        type=str,
        help="MTG set code 'set' (up to 3 characters).",
        metavar="SET",
    )

    parser.add_argument(
        "--card",
        "-c",
        type=str,
        help="The card name.",
        metavar="CARD",
    )

    return parser


def validate_args(args):
    """Validates the provided arguments."""
    if args.set and len(args.set) > 3:
        raise argparse.ArgumentTypeError(
            "'set' argument cannot be longer than 3 characters."
        )


def get_args():
    parser = create_parser()
    args = parser.parse_args()
    try:
        validate_args(args)
        return args
    except argparse.ArgumentTypeError as e:
        print(f"Error: {e}")
        print(parser.format_help())
        return None


def main():
    setup_logging()
    args = get_args()
    if not args:
        return 9
    set_to_ask = args.set
    card_to_ask = args.card
    cards = get_set(set_to_ask)
    logger.info(f"Searching for {card_to_ask} in {set_to_ask}")
    exit_code = 0
    for result in crunch(cards, card_to_ask):
        result.display()
        exit_code = max(exit_code, result.exitcode())
    else:
        exit_code = 2
    return exit_code


if __name__ == "__main__":
    # Exit codes:
    # 0 - values found
    # 1 - exact card match found
    # 2 - No values found
    # 9 - Invalid arguments
    sys.exit(main())
