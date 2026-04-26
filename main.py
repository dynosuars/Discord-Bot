import os
import discord
import json
import asyncio
import random

from Rtypes.reponses import responses
from dotenv import load_dotenv



client = discord.Client(intents=discord.Intents.all())
load_dotenv()



@client.event
async def on_ready():
    global res, prefix
    
    print("Parsing responses")
    res = responses.parse("ext/responses.json")
    prefix = "han"
    if(res is not None):
        print("Responses loaded succesfully")
    
    print(f"Logged in {client.user.name}")
    
    print(f" {client.user.name} init...")
    await client.change_presence(
        status=discord.Status.online,
        activity=discord.Game("Playing with minors")
    )

@client.event
async def on_message(ctx: discord.message.Message):
    if(ctx.author == client.user):
        pass

    if(ctx.content.lower().startswith(prefix)):
        msg = ctx.content[(len(prefix + " ")):]
        print(msg)
        responded = False
        for reponse in res["responses"]:
            if(reponse.check_condition(msg)):
                await ctx.channel.send(random.choices(reponse.response, reponse.weights)[0])
                responded = True
                break
        if(not responded):
            await ctx.channel.send(random.choices(res["default"])[0])
    
if(__name__ == "__main__"):
    client.run(os.environ["TOKEN"])
