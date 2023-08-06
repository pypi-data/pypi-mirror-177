import os
from pathlib import Path
from typing import Optional

from disnake.ext.bracord.boilerplate import env_boilerplate


def bot_name_to_folder(bot_name: str):
    """Converts the name of a bot to a valid folder name."""

    return bot_name.lower().replace(" ", "_")


def gen_project_env_file(
    bot_name: str,
    bot_token: str,
    bot_version: str,
    project_path: Path,
    output_path: str = "./.env",
):
    with open(output_path, encoding="utf-8", mode="w") as f:
        env_content = env_boilerplate.format(
            bot_name=bot_name,
            bot_token=bot_token,
            bot_version=bot_version,
            project_path=str(project_path.resolve()).replace("\\", "/"),
        )
        f.write(env_content)


def find_env_file() -> Optional[str]:
    """Searches in all parent dirs until the .env file of a project is found."""
    # * Search in parent folders until we reach top-most folder or we find the .env file.
    cwd = os.getcwd()
    found = False

    while not found:
        last_dir = Path("./").resolve()
        os.chdir("../")

        if ".env" in os.listdir("./"):
            with open("./.env", encoding="utf-8", mode="r") as f:
                # BOT_NAME is the first variable in a project's .env file

                line = f.readline()
                if "BOT_NAME" in line:
                    found = True

        # There are no more parent folders
        if str(Path("./").resolve()) == str(last_dir):
            break

    if not found:
        return None

    path = Path("./.env").resolve()
    os.chdir(cwd)
    return path
