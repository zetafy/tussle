# This cog contains all bot config commands.
# All commands here are either restricted to lead devs only, or registered staff (moderators/admin)
import discord
from discord.ext import commands
from discord import app_commands
from discord import ui
import json
import time
from datetime import datetime

class cogsManageView(discord.ui.View):
    def __init__(self):
        super().__init__()
    
    @discord.ui.button(label="Load Cog", emoji="<:enter:1179670134823063603>",style=discord.ButtonStyle.blurple,custom_id="loadCog")
    async def cogs_load(self, inter: discord.Interaction, loadButton: discord.ui.Button):
        await inter.response.edit_message("~~ Load cog view supposed to be here ~~")

    @discord.ui.button(label="Unload Cog", emoji="<:enter:1179670134823063603>",style=discord.ButtonStyle.blurple,custom_id="unloadCog")
    async def cogs_load(self, inter: discord.Interaction, unloadButton: discord.ui.Button):
        await inter.response.edit_message("~~ Unload cog view supposed to be here ~~")



class panelMainView(discord.ui.View):
    def __init__(self, client):
        super().__init__()
        self.client = client

    @discord.ui.button(label="Manage Cogs", emoji="<:enter:1179670134823063603>",style=discord.ButtonStyle.blurple,custom_id="cogManage")
    async def cog_manage(self, inter: discord.Interaction, proceedButton: discord.ui.Button):
        cogsEmbed = discord.Embed(title="All Cogs",description="Live view of all cogs.", color=discord.Colour.gold())
        dotEmojis = ["<:greendot:1152388148064686150>", "<:orangedot:1152388117131694202>", "<:reddot:1152388087456997396>"]
        cogsStatus = ""
        # All active cogs first
        for i in self.client.active_cogs:
            cogsStatus += f"{dotEmojis[0]} {i}\n"

        for j in self.client.all_cogs:
            if j not in self.client.active_cogs:
                cogsStatus += f"{dotEmojis[2]} {j}\n" 
        
        cogsEmbed.add_field(name="Cogs Status",value=cogsStatus, inline=True)
        await inter.response.edit_message(embed=cogsEmbed, view=cogsManageView())


class config(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("(LOADED): config.py/config")

    def getDevIDs(self):
        with open("config.json",'r') as f:
            ids = json.load(f)
        return ids["devIDs"]
    
    def getUptime(self):
        with open("config.json",'r') as f:
            configs = json.load(f)
        # startTime = configs["startTime"]
        sec = int(round(time.time()-self.client.startTime))
        days, remainder = divmod(sec, 86400)
        hours, remainder = divmod(remainder, 3600)
        minutes, seconds = divmod(remainder, 60)
        uptime_str = f"{days:02}:{hours:02}:{minutes:02}:{seconds:02}"
        return uptime_str
    
    # DEV OPS COMMAND
    @app_commands.command(name="panel", description="View bot's control panel, and manage its settings (authorized devs only)")
    async def panel(self, inter: discord.Interaction):
        '''
        The "control panel" of the bot, only accessible and usable by authorized devs.
        Contains comprehensive status of the bot's functionality and performance.
        Used to detect if any maintenance is required, and first source of identifying issues reported.
        '''
        ids = self.getDevIDs()
        if inter.user.id not in ids:
            return
        
        dotEmojis = ["<:greendot:1152388148064686150>", "<:orangedot:1152388117131694202>", "<:reddot:1152388087456997396>"]
        ping = round(self.client.latency*1000, 1)
        emoji = ""
        if ping <= 50:
            emoji = dotEmojis[0]
        if ping > 75 and ping <= 150:
            emoji = dotEmojis[1]
        else:
            emoji = dotEmojis[2]
        panelEmb = discord.Embed(title="Tussle Control Panel",description="<:caution:1179668960329859093> This panel contains sensitive information only devs should be able to view! Please ensure you are in a private channel.",color=discord.Colour.red())
        panelEmb.add_field(name="Client Latency", value=f"{emoji} \t{ping}ms", inline=True)
        panelEmb.add_field(name="Uptime", value=self.getUptime(), inline=True)
        cogsStat = len(self.client.active_cogs)/len(self.client.all_cogs)
        emj = ""
        if cogsStat == 1:
            emj = dotEmojis[0]
        elif cogsStat > 0.5:
            emj = dotEmojis[1]
        else:
            emj = dotEmojis[2]
        panelEmb.add_field(name="Cogs status", value=f"{emj} {len(self.client.active_cogs)} / {len(self.client.all_cogs)} active cogs", inline = False)
        panelEmb.timestamp = datetime.now()
        await inter.response.send_message(embed=panelEmb, view=panelMainView(self.client), ephemeral=True)



    # @commands.command()
    # async def sync(self, ctx):
    #     '''
    #     Sync command: syncs the command tree to discord's cache.
    #     Only allowed to be run by lead devs. 
    #     Run this command when you:
    #     - updated a slash command's parameters, name, or description
    #     - Added/removed a slash command
    #     You don't have to sync if the logic of an existing slash command has been updated.

    #     -----
    #     parameters:
    #         self
    #         ctx
    #     returns:
    #         None
    #     '''
    #     # Checking if command ran is by authorized dev
    #     ids = self.getDevIDs()
    #     if ctx.author.id not in ids:
    #         return
        
    #     print("Syncing commands")
    #     await self.client.tree.sync()
    #     await ctx.reply("Successfully synced commands.")

async def setup(client:commands.Bot) -> None:
    await client.add_cog(config(client))