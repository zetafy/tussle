import asyncio
import os
import discord
from discord.ext import commands
from discord import app_commands
import json
import time
from dotenv import load_dotenv, dotenv_values
# Merge test
load_dotenv()

class aclient(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(command_prefix='.', intents=intents)
        self.synced = False
        self.all_cogs = []
        self.active_cogs = []
        
    async def setup_hook(self) -> None:
        for filename in os.listdir('./cogs'):
            if filename.endswith('.py'):
                self.all_cogs.append(filename[:-3])
                # Uncomment the following as labelde to get error tracebacks.
                try: # uncomment
                    await self.load_extension(f'cogs.{filename[:-3]}')
                    self.active_cogs.append(filename[:-3])
                except: # uncomment
                    print(f"Failed to load: {filename[:-3]}") # uncomment

    async def on_ready(self):
        # await self.wait_until_ready()
        # if not self.synced:
        #     await client.tree.sync()
        #     self.synced = True
        #await client.change_presence(status=discord.Status.do_not_disturb, activity=discord.Game(name="Maintenance break !")) 
        #Maintenance Break
        #await self.change_presence(status=disco rd.Status.do_not_disturb, activity=discord.Game(name="Maintenance break !"))
        #Default
        self.startTime = time.time()
        with open("config.json",'r') as f:
            configs = json.load(f)

        configs["startTime"] = time.time() # Get bot start epoch time

        with open("config.json",'w') as f:
            json.dump(configs, f, indent=4)

        await client.change_presence(status=discord.Status.idle, activity=discord.Activity(type=discord.ActivityType.watching, name="Space colonies flourish!"))
        print("... Tussle is now online! ...")

client = aclient()
client.run(os.environ.get("token"))