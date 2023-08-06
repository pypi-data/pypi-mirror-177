"""
File that stores boilerplate code
"""

env_boilerplate = """BOT_NAME = "{bot_name}"
BOT_TOKEN = "{bot_token}"
BOT_VERSION = "{bot_version}"
PROJECT_PATH = "{project_path}"

"""

interaction_bot_boilerplate = """import disnake
from disnake.ext import commands
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

BOT_NAME = os.environ.get("BOT_NAME", "My Disnake Bot")
BOT_VERSION = os.getenv("BOT_VERSION", None)
BOT_TOKEN = os.getenv("BOT_TOKEN", "")

# You can modify these intents based on your needs.
# Refer to https://docs.disnake.dev/en/stable/api.html#disnake.Intents
intents = disnake.Intents.default()
bot = commands.InteractionBot(test_guilds=[//test_guild_id//], intents=intents)


@bot.event
async def on_ready():
    print("============")
    print(f"{BOT_NAME} is ready.")
    print(f"Bot version: {BOT_VERSION}")
    print(f"Disnake version: {disnake.__version__}")
    print("============")


@bot.slash_command(name="ping", description="Shows the bot's ping.")
async def ping(inter: disnake.MessageCommandInteraction):
    await inter.send(f"Pong! :ping_pong: `{round(bot.latency * 1000)}ms`")

"""

message_bot_boilerplate = """import disnake
from disnake.ext import commands
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

BOT_NAME = os.environ.get("BOT_NAME", "My Disnake Bot")
BOT_VERSION = os.getenv("BOT_VERSION", None)
BOT_TOKEN = os.getenv("BOT_TOKEN", "")

# You can modify these intents based on your needs.
# Refer to https://docs.disnake.dev/en/stable/api.html#disnake.Intents
intents = disnake.Intents.default()
bot = commands.Bot(
    command_prefix=commands.when_mentioned_or(//bot_prefix//),
    test_guilds=[//test_guild_id//],
    intents=intents,
)


@bot.event
async def on_ready():
    print("============")
    print(f"{BOT_NAME} is ready.")
    print(f"Bot version: {BOT_VERSION}")
    print(f"Disnake version: {disnake.__version__}")
    print("============")


@bot.command(description="Shows the bot's ping.")
async def ping(ctx: commands.Context):
    await ctx.reply(f"Pong! :ping_pong: `{round(bot.latency * 1000)}ms`")

"""

cog_boilerplate = """import disnake
from disnake.ext import commands, tasks

class //cog_name//(commands.Cog):
    def __init__(self):
        #* This will run when the cog is instantiated.
        pass

    def cog_load(self):
        print(f"//cog_name// cog has been loaded.")

        #* This will make the cog's task to run.
        self.say_hello.start()

    def cog_unload(self):
        print(f"//cog_name// cog has been unloaded.")

        #* This will make the cog's task to stop.
        if not self.say_hello.is_running():
            self.say_hello.stop()

    @commands.Cog.listener()
    async def on_ready(self):
        #* The cog will execute the code when the bot is ready.
        #! NOTE: THIS WILL ONLY TRIGGER IF THE COG IS ADDED BEFORE THE BOT IS READY.
        pass

    @tasks.loop(seconds = 10)
    async def say_hello(self):
        "Prints Hello to the console every 10 seconds."
        print('Hello!')

def setup(bot: commands.BotBase):
    bot.add_cog(//cog_name//())
"""
