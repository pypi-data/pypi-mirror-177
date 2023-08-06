"""
This file is in charge of creating cogs and registering them in the bot's main file.
"""
import os
from pathlib import Path

from dotenv import load_dotenv
from rich.console import Console

from disnake.ext.bracord.boilerplate import cog_boilerplate
from disnake.ext.bracord.utils import bot_name_to_folder, find_env_file

console = Console()


def init_cog(cog_name: str):
    """Starts the process of initializing a cog."""

    cog_content = cog_boilerplate.replace("//cog_name//", cog_name)

    res = add_cog_load(cog_name)
    if res > 0:
        return res

    # * User is inside project's bot folder
    if "cogs" in os.listdir("./"):
        with open(f"./cogs/{cog_name}.py", encoding="utf-8", mode="w") as f:
            f.write(cog_content)

        return 0

    # * User is in project's root folder.
    elif ".env" in os.listdir("./"):
        # Get bot's folder name

        load_dotenv("./.env")
        bot_name = os.getenv("BOT_NAME", "")
        bot_folder = bot_name_to_folder(bot_name)

        console.log(bot_name)
        console.log(bot_folder)
        if bot_folder not in os.listdir("./"):
            console.print(
                "[bold red]Could not find bot's project folder.\nDoes your bot folder name matches your bot's name?"
            )
            return 1

        with open(
            f"./{bot_folder}/cogs/{cog_name}.py", encoding="utf-8", mode="w"
        ) as f:
            f.write(cog_content)
        return 0

    env_path = find_env_file()

    if env_path is None:
        console.print(
            "[bold red]Could not find project's [bold cyan].env[/bold cyan] file.\nAre you sure you are in the correct directory?"
        )
        return 1

    load_dotenv(env_path)
    bot_root = os.getenv("PROJECT_PATH")
    bot_folder = bot_name_to_folder(os.getenv("BOT_NAME", ""))

    if bot_root is None:
        console.print(
            "[bold red]We could not find the project's root folder. Please run [bold cyan]bracord verify[/bold cyan] to fix this issues."
        )
        return 1

    bot_root = Path(bot_root).resolve()
    console.log(bot_root)
    with open(
        f"{bot_root}/{bot_folder}/cogs/{cog_name}.py", encoding="utf-8", mode="w"
    ) as f:
        f.write(cog_content)
    return 0


def add_cog_load(cog_name: str):
    """Makes the cog to load on the bot's file."""

    # check if env file is in the working dir

    env_path = None
    if ".env" in os.listdir("./"):
        env_path = "./.env"

    else:
        env_path = find_env_file()

    if env_path is None:
        console.print(
            "[bold red]Could not find project's [bold cyan].env[/bold cyan] file.\nAre you sure you are in the correct directory?"
        )
        return 1

    load_dotenv(env_path)
    project_root_folder = Path(env_path).parent.resolve()
    bot_folder_name = bot_name_to_folder(os.getenv("BOT_NAME", ""))
    bot_file_path = project_root_folder / bot_folder_name / "__init__.py"

    file_content = None
    with open(bot_file_path, encoding="utf-8", mode="r") as f:
        file_content = f.read()

    with open(bot_file_path, encoding="utf-8", mode="w") as f:
        bot_folder_name = bot_name_to_folder(os.getenv("BOT_NAME", ""))
        f.write(file_content)
        f.write(f'bot.load_extension("{bot_folder_name}.cogs.{cog_name}")\n\n')

    return 0
