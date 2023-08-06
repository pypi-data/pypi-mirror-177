"""
This file stores the different CLI commands.
"""

import os
from pathlib import Path

from dotenv import load_dotenv
from rich.console import Console
from rich.prompt import Confirm, IntPrompt, Prompt

from disnake.ext.bracord.cli.cog_init import init_cog
from disnake.ext.bracord.cli.project_init import init_base_project
from disnake.ext.bracord.utils import gen_project_env_file

console = Console()


def cog():
    """Command that runs when `bracord cog` is ran."""

    # TODO: Regex to check a valid class name.
    valid = False
    cog_name = None

    while not valid:
        cog_name = Prompt.ask("[bold bright_yellow]Enter the name of your cog").strip()

        if " " in cog_name:
            console.print("[bold red]Do not use spaces in cog names.")
            continue

        valid = True

    console.print("[bold bright_blue]Creating cog...")
    res = init_cog(cog_name=cog_name)

    if res > 0:
        return res

    console.print(f"[bold green]Successfully created {cog_name}.py")
    return 0


def init_project():
    """Command that runs when `bracord init` is ran."""
    bot_name = Prompt.ask("[bold bright_yellow]Enter the name of your bot")
    bot_token = Prompt.ask("[bold bright_yellow]Enter your bot's token")
    bot_version = Prompt.ask(
        "[bold bright_yellow]Enter the version of your bot", default="0.1.0"
    )

    use_slash = Confirm.ask(
        "[bold bright_yellow]Do you want to use Slash Commands only?"
    )

    bot_prefix = None
    if not use_slash:
        bot_prefix = Prompt.ask("[bold bright_yellow]Enter your bot's command prefix")

    test_guild_id = IntPrompt.ask(
        "[bold bright_yellow]Enter the ID of your bot's test server (leave this empty to set it up later)",
        show_default=None,
        default="",
    )

    init_base_project(
        use_slash=use_slash,
        bot_name=bot_name,
        bot_token=bot_token,
        bot_version=bot_version,
        test_guild_id=test_guild_id,
        bot_prefix=bot_prefix,
    )
    return 0


def verify_project():
    """Verifies if all keys in the .env file are set. Fixes them if they are not found."""

    if ".env" not in os.listdir("./"):
        console.print(
            "[bold red]Could not find project's [bold cyan].env[/bold cyan] file.\nAre you sure you are in the correct directory?"
        )
        return 1

    load_dotenv("./.env")
    console.print(
        "[bold bright_blue]Verifying project's [bold cyan].env[/bold cyan] file..."
    )

    bot_name = os.getenv("BOT_NAME")
    bot_token = os.getenv("BOT_TOKEN")
    bot_version = os.getenv("BOT_VERSION")
    project_path = os.getenv("PROJECT_PATH")
    broken = False

    if bot_name is None:
        broken = True
        console.print("[bold red]Could not find bot's name.")
        bot_name = Prompt.ask("[bold yellow]Enter the bot's name")

    # TODO: Regex that checks if the token is valid? (follows a token format, but may not be a working token.)
    if bot_token is None:
        broken = True
        console.print("[bold red]Could not find bot's token.")
        bot_token = Prompt.ask("[bold yellow]Enter the bot's token")

    if bot_version is None:
        broken = True
        console.print("[bold red]Could not find bot's version.")
        bot_version = Prompt.ask(
            "[bold yellow]Enter the bot's version", default="0.1.0"
        )

    if project_path is None:
        broken = True
        console.print("[bold red]Could not find bot's project path.")
        path = Path("./").parent

        is_correct_path = Confirm.ask(
            f'[bold yellow]Is [bold cyan]"{str(path.resolve())}"[/bold cyan] the correct project\'s path?'
        )

        if not is_correct_path:
            path = Prompt.ask(
                "[bold yellow]Enter the path to the project's root folder"
            )
            path = Path(path)

            if not path.exists():
                console.print("[bold red]Please enter a valid path.")
                return 2

        project_path = path

    # Generate a new .env file
    if not broken:
        console.print("[bold green]All looks good.")
        return 0

    console.print("[bold bright_blue]Fixing [bold cyan].env[/bold cyan] file...")
    gen_project_env_file(
        bot_name=bot_name,
        bot_token=bot_token,
        bot_version=bot_version,
        project_path=project_path,
    )

    console.print("[bold bright_green]Successfully fixed the file.")
    return 0
