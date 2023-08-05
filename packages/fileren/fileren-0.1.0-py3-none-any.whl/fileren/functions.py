import argparse

from rich.prompt import Prompt


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-p",
        "--path",
        type=str,
        help="Path to the directory with files",
        required=False,
    )
    parser.add_argument(
        "-r",
        "--regex",
        type=str,
        help="Pattern to search",
        required=False,
    )
    parser.add_argument(
        "-n",
        "--new_string",
        type=str,
        help="New text",
        required=False,
    )
    args = parser.parse_args()

    path = (
        Prompt.ask(
            "Path to file of directory with files",
            default="./",
        )
        if args.path is None
        else args.path
    )
    return path, args.regex, args.new_string
