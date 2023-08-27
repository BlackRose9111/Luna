from nextcord.ext import commands
import nextcord
#maybe instead of gtts I should use pyttsx3
import pyttsx3


class LunaTTS(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.voice_client = None


    #on ready
    @commands.Cog.listener()
    async def on_ready(self):
        print("Luna TTS module has been loaded")
        self.engine = pyttsx3.init()
        self.engine.setProperty("rate",150)
        self.engine.setProperty("volume",1)
        print(self.engine.getProperty("voices"))
        self.engine.setProperty("voice",self.engine.getProperty("voices")[1].id)


    async def join_vc(self,ctx):
        #join the voice channel the user is in, if it already is in the same voice channel, do nothing
        voice_channel = ctx.author.voice.channel
        if self.voice_client is None:
            await voice_channel.connect()
            self.voice_client = ctx.voice_client
        elif self.voice_client.channel != voice_channel:
            await self.voice_client.move_to(voice_channel)
            self.voice_client = ctx.voice_client



    @commands.command()
    async def tts(self,ctx,*,text):
        #use pyttsx3 to turn the text into speech, play it in the voice channel the user is in. If the user is not in a voice channel, return a message saying that the user is not in a voice channel

        await self.join_vc(ctx)

        #save the audio as an mp3 file
        self.engine.save_to_file(text,"tts.mp3")
        self.engine.runAndWait()
        voice_client = ctx.voice_client
        voice_client.play(nextcord.FFmpegPCMAudio("tts.mp3"))



def setup(client):
    client.add_cog(LunaTTS(client))