import json

from nextcord.ext import commands
import nextcord
from artificialintelligence.tokenizer import Tokenizer
class Datacollectionmodule(commands.Cog):
    def __init__(self, client):
        self.client = client

    #on ready
    @commands.Cog.listener()
    async def on_ready(self):
        print("Data collection module has been loaded")
        self.Tokenizer = Tokenizer()
        self.Tokenizer.load_vocab("variables/vocab.json")

    #on message
    @commands.Cog.listener("on_message")
    async def collect_data(self,message : nextcord.Message):
        data_path = "variables/dataset.json"
        content = message.content.lower().capitalize()
        #the data is a list object in json. Only append the message itself to the list, not the author or the guild
        #if the message is from the bot, do nothing
        if message.author == self.client.user:
            return
        #if the message is from a bot, do nothing
        if message.author.bot:
            return
        #if the message is from a dm, do nothing
        if message.guild is None:
            return
        #if the message is from a server, save the message to a file
        else:
            #open the file
            with open(data_path,"r") as file:
                data = json.load(file)
            #append the message to the list
            data.append(content)
            #save the file
            with open(data_path,"w") as file:
                json.dump(data,file,indent=4)
            return

    @commands.command()
    async def sanitise_data(self,ctx):
        #remove any entries that start with a command prefix
        data_path = "variables/dataset.json"
        command_prefixes = ("*","!","/",".")
        newlist = []
        with open(data_path,"r") as file:
            data = json.load(file)
        for entry in data:
            if entry[0] not in command_prefixes:
                newlist.append(entry)
        with open(data_path,"w") as file:
            json.dump(newlist,file,indent=4)
        await ctx.send("Data sanitised")
    @commands.command()
    async def printdata(self,ctx):
        data_path = "variables/dataset.json"
        with open(data_path,"r") as file:
            data = json.load(file)
        await ctx.send("Check console")
        for entry in data:
            print(entry)

    @commands.command()
    async def create_new_vocab(self,ctx):
        #import the tokenizer we just wrote at aritificalintelligence/tokenizer.py
        from artificialintelligence.tokenizer import Tokenizer
        tokenizer = Tokenizer()
        #fit the tokenizer on the data
        tokenizer.fit_on_texts_from_path("variables/dataset.json")
        #save the vocab
        tokenizer.save_vocab("variables/vocab.json")
        await ctx.send("Vocab created")

    @commands.command()
    async def add_to_vocab(self,ctx):
        #this is a test to see what happens if you try to fit in duplicate data
        data= ["Jim"]
        from keras.preprocessing.text import Tokenizer
        tokenizer = Tokenizer()
        tokenizer.fit_on_texts(data)
        tokenizer.fit_on_texts(data)
        sequences = tokenizer.texts_to_sequences(data)
        await ctx.send(f"Sequences: {sequences}")

    @commands.command()
    async def load_vocab(self,ctx):
        data_path = "variables/dataset.json"
        with open(data_path,"r") as file:
            data = json.load(file)
        self.Tokenizer.fit_on_texts(data)
        self.Tokenizer.save_vocab("variables/vocab.json")
        await ctx.send("Vocab loaded")

    @commands.command()
    async def indentvocab(self,ctx):
        #read the vocab.json and then indent it with 4 spaces
        with open("variables/vocab.json","r") as file:
            data = json.load(file)
        with open("variables/vocab.json","w") as file:
            json.dump(data,file,indent=4)
        await ctx.send("Vocab indented")

    @commands.command()
    async def text_to_sequences(self,ctx,*,text):
        #import the tokenizer we just wrote at aritificalintelligence/tokenizer.py
        from artificialintelligence.tokenizer import Tokenizer
        tokenizer = self.Tokenizer
        #load the vocab and then tokenize the message from text variable
        sequences = tokenizer.data_to_sequences([text])
        vembed = nextcord.Embed(title="Sequences",description=f"{sequences}",color=nextcord.Color.green())
        await ctx.send(embed=vembed)
        #then do the reverse and convert the sequences back to text
        text = tokenizer.sequences_to_data(sequences)
        textlist = []
        for entry in text:
            textlist.append(tokenizer.apply_basic_grammar(entry))
        text = textlist
        vembed = nextcord.Embed(title="Text",description=f"{text}",color=nextcord.Color.green())
        await ctx.send(embed=vembed)

    @commands.command()
    async def sequences_to_text(self,ctx,*,sequences):
        #import the tokenizer we just wrote at aritificalintelligence/tokenizer.py
        tokenizer = self.Tokenizer
        #load the vocab and then tokenize the message from text variable
        text = tokenizer.sequences_to_data([sequences])
        await ctx.send(f"Text: {text}")

    @commands.command()
    async def vocab_size(self,ctx):
        #import the tokenizer we just wrote at aritificalintelligence/tokenizer.py
        from artificialintelligence.tokenizer import Tokenizer
        tokenizer = self.Tokenizer
        #load the vocab and then tokenize the message from text variable
        number = len(tokenizer.tokenizer.vocab)
        await ctx.send(f"This AI knows {number} words.")

    @commands.command()
    async def data_size(self,ctx):
        datapath = "variables/dataset.json"
        with open(datapath,"r") as file:
            data = json.load(file)
        await ctx.send(f"This AI is being trained on {len(data)} messages.")

def setup(client):
    client.add_cog(Datacollectionmodule(client))