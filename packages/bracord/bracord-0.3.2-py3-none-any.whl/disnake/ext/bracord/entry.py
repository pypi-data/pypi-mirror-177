"""
This file is responsible for handling the CLI.
"""

import argparse
import sys

from disnake.ext.bracord.cli.console_commands import cog, init_project, verify_project

commands = {
    "cog": cog,
    "init": init_project,
    "verify": verify_project,
}

parser = argparse.ArgumentParser(
    prog="bracord",
    description="A Disnake framework written in Python that speeds the development of Discord bots.",
    add_help=True,
)

parser.add_argument(
    "command",
    help="The command you want to run.",
    choices=commands.keys(),
)


def main():
    """Main function entry poinn"""
    args = parser.parse_args()

    # Run the command the user selected.
    sys.exit(commands[args.command]())
