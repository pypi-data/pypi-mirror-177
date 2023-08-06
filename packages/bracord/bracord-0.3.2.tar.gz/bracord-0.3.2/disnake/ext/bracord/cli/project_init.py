"""
This file manages and creates bracord projects.
"""

import os
from pathlib import Path

from rich.console import Console

from disnake.ext.bracord.boilerplate import (
    interaction_bot_boilerplate,
    message_bot_boilerplate,
)
from disnake.ext.bracord.utils import bot_name_to_folder, gen_project_env_file

console = Console()


def init_base_project(
    use_slash: bool,
    bot_name: str,
    bot_token: str,
    bot_version: str,
    test_guild_id: int,
    bot_prefix: str,
):
    """Initializes the base file structure for a Discord Bot."""

    console.print("[bold bright_blue]Creating file structure...")

    bot_folder = bot_name_to_folder(bot_name)

    # Create the folder for the bot's code as a python module structure
    os.mkdir(f"./{bot_folder}")
    os.mkdir(f"./{bot_folder}/cogs")

    project_path = Path("./")
    gen_project_env_file(
        bot_name=bot_name,
        bot_token=bot_token,
        bot_version=bot_version,
        project_path=project_path,
    )

    # Create file to start the bot.
    with open("./bot.py", encoding="utf-8", mode="w") as f:
        f.write(
            f"""from {bot_folder} import bot, BOT_TOKEN

if __name__ == "__main__":
    bot.run(BOT_TOKEN)
"""
        )

    if use_slash:
        init_interaction_bot(test_guild_id=test_guild_id, bot_folder=bot_folder)

    else:
        init_message_bot(
            bot_prefix=bot_prefix, test_guild_id=test_guild_id, bot_folder=bot_folder
        )

    console.print("[bold bright_green]The project was created succesfully.\n\n")
    console.print(
        f"[bold bright_blue]To run your bot, use [bold cyan]python bot.py[/bold cyan]\nThe bot's code is under the folder called [bold cyan]{bot_folder}[/bold cyan]"
    )


def init_interaction_bot(test_guild_id: int, bot_folder: str):
    """Creates the init file for a Interaction Bot (aka. a bot that will only use application commands)"""

    with open(f"./{bot_folder}/__init__.py", encoding="utf-8", mode="w") as f:
        bot_code = interaction_bot_boilerplate.replace(
            "//test_guild_id//", str(test_guild_id)
        )
        f.write(bot_code)


def init_message_bot(bot_prefix: str, test_guild_id: int, bot_folder: str):
    """Creates the init file for a Message Bot (aka. a bot that uses prefixes)"""

    with open(f"./{bot_folder}/__init__.py", encoding="utf-8", mode="w") as f:
        bot_code = message_bot_boilerplate.replace(
            "//test_guild_id//", str(test_guild_id)
        ).replace("//bot_prefix//", f'"{bot_prefix}"')
        f.write(bot_code)
