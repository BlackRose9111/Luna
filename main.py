import nextcord
from nextcord.ext import commands,tasks

from system.filemanager import filemanager
import os

owner_ids = [240027656949596160, 1068287199688278166]
bot_name = "Luna"
bot_time_zone = "Europe/Istanbul"
bot = commands.AutoShardedBot(command_prefix="!",
                              strip_after_prefix=True,
                              case_insensitive=True,
                              intents=nextcord.Intents.all(),
                              owner_ids=owner_ids)


run_time = 0
TOKEN = ""



@bot.event
async def on_ready():
    print("Luna launched")
    parallel_loop.start()
    database_connect()


def database_connect():
    pass


def database_keepalive():
    pass


@tasks.loop(seconds=1)
async def parallel_loop():
    global run_time
    run_time += 1
    database_keepalive()

def get_token():
    global TOKEN
    try:
        TOKEN = filemanager.get_value_from_json(key="token",alias="token",debug=False)
        if TOKEN is None:
            raise Exception("Token is None")
    except:
        TOKEN = None

    if TOKEN is None:
        while True:
            a = input("Bot Token was not found, please enter it by hand:")
            if a is not None and a != "":
                TOKEN = a
                print("Token entered successfully")
                filemanager.change_or_add_value_on_json(new_value=TOKEN,alias="token",debug=True,key="token")
                break

def load_module(modulename):
    try:
        bot.load_extension(modulename)
    except Exception as e:
        print(f"Failed to load module {modulename} with error {e}")

def load_all_modules():
    for file in os.listdir("modules"):
        #if ends with .py
        if file.endswith(".py"):
            load_module(f"modules.{file[:-3]}")
            print(f"Loaded module {file[:-3]}")

get_token()
load_all_modules()
bot.run(TOKEN)




print("Goodbye! <3")




