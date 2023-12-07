import discord
from discord.ext import commands
from discord import app_commands
from discord import ui
from datetime import datetime
import os
import mysql.connector as sql
from .market import Market, MarketGoods, MarketServices, MarketBuildings

class Game(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client
        
    @commands.Cog.listener()
    async def on_ready(self):
        print("(LOADED): game.py/Game")
        
    @commands.command()
    async def sync(self, ctx) -> None:
        fmt = await ctx.bot.tree.sync(guild = ctx.guild)
        await ctx.send(f"(game.py) Synced {len(fmt)} commands.")
        
    @app_commands.command(name="profile", description="View your profile and space colony stats.")
    async def profile(self, inter: discord.Interaction, user: discord.User = None):
        if user == None:
            user = inter.user
        profileEmbed = discord.Embed(title=f"{user.name}'s Profile", description="Basic info", color=discord.Colour.gold())
        profileEmbed.add_field(name = "Colony", value = "Elon Musk colony")
        profileEmbed.set_footer(text="Global rank #7", icon_url=user.display_avatar.url)
        await inter.response.send_message(embed=profileEmbed)    
        
    # =============================================== [ MARKET ] ===============================================
    @app_commands.command(name="market", description="Purchase or sell goods.")
    async def market(self, inter: discord.Interaction):
        
        user = inter.user.name # fetch username
    
        # Go Back callbacks
        async def market_callback(inter):
            await inter.response.send_message(view=market_view, embed=market_embed)
    
        # >>>> `Goods` callbacks <<<<
        async def goods_natural_resources(inter):
            await inter.response.send_message("Callback: market/goods/natural_resources")
            
        async def goods_consumables(inter):
            await inter.response.send_message("Callback: market/goods/consumables")
            
        async def goods_tools(inter):
            await inter.response.send_message("Callback: market/goods/tools")
        
        # async def goods_dropdown_callback(self, interaction, value):
        #     await interaction.response.send_message(f'You selected: {value}', ephemeral=True)
        
        async def goods(inter):
            """
            Replaces the message sent by `/market` with
            an embed that serves as the UI for buying goods.
            """
            market_goods = MarketGoods()
            message = f"What type of goods would you like to buy?"
            embed = market_goods.generate_embed(msg=message,
                                                color=discord.Colour.dark_magenta())
            view = market_goods.generate_view(market_callback=market_callback)
                
            await inter.response.edit_message(view=view, embed=embed)
            
        # `Services` callback
        async def services(inter):
            """
            Replaces the message sent by `/market` with
            an embed that serves as the UI for buying services.
            """
            market_services = MarketServices()
            message = f"What type of service would you like to buy?\n\nClick on a service to preview the benefits you can get!"
            embed = market_services.generate_embed(msg=message,
                                                color=discord.Colour.dark_magenta())
            view = market_services.generate_view(market_callback=market_callback)
            await inter.response.edit_message(view=view, embed=embed)
            
        # `Buildings` callback
        async def buildings(inter):
            """
            Replaces the message sent by `/market` with
            an embed that serves as the UI for buying buildings.
            """
            market_buildings = MarketBuildings()
            message = f"What type of building would you like to buy?\n\nClick on a building to preview the benefits you can get!"
            embed = market_buildings.generate_embed(msg=message,
                                                color=discord.Colour.dark_magenta())
            view = market_buildings.generate_view(market_callback=market_callback)
            await inter.response.edit_message(view=view, embed=embed)
            
        # `Sell` callback
        async def sell(inter):
            """
            Replaces the message sent by `/market` with
            an embed that serves as the UI for selling purchased assets.
            """
            await inter.response.send_message("Callback: market-sell (Awaiting DB)")
        
        # Market UI
        market = Market()
        message = f"Welcome to the market, {user}!\n What would you like to buy/sell?"
        market_embed = market.generate_embed(img="https://i.ibb.co/b6BDh1X/Sell.png",
                                             msg=message,
                                             color=discord.Colour.dark_magenta())
        market_view = market.generate_view(goods_callback=goods,
                                           services_callback=services,
                                           buildings_callback=buildings,
                                           sell_callback=sell)
            
        await inter.response.send_message(view=market_view, embed=market_embed)
        
async def setup(client):
    await client.add_cog(Game(client))