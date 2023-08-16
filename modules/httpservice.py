import threading

import flask
from nextcord.ext.commands import Cog

import main


class httpservice(Cog):
    def __init__(self, bot):
        self.bot = bot
        self.app = flask.Flask(main.bot_name)


    @Cog.listener()
    async def on_ready(self):
        print("HTTP Service Cog is ready")
        self.add_paths()
        self.thread = threading.Thread(target=self.start_server, daemon=True)
        self.thread.start()


    def start_server(self):
        self.app.run(host="0.0.0.0", port=64000, debug=False)
        #uvicorn.run(self.app,host="0.0.0.0",port=65000)


    def add_paths(self):
        self.app.add_url_rule("/test", "test", self.test)

    def test(self):
        return "test"

def setup(bot):
    bot.add_cog(httpservice(bot))