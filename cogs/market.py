import discord
from discord.ext import commands
from .data import NATURAL_RESOURCES_DICT, CONSUMABLES_DICT, TOOLS_DICT, GATHERERS_DICT, MILITARY_DICT, BOOSTING_DICT, BUILDINGS_DICT

# ModuleNotFoundError handler
class MarketErrorHandler(commands.Cog):
    """
    Handles discord.py's `/cogs` exception thrower
    """
    def __init__(self, client: commands.Bot):
        self.client = client
        
    @commands.Cog.listener()
    async def on_ready(self):
        print("(LOADED): market.py")

# =============================================== [ RootMarket ] ===============================================

class Market():
    """
    Class responsible for generating the UI of `/market`
    """
    def generate_embed(self, img, msg, color):
        """
        Generate an `Embed` object for the UI of `/market`
        """
        market_embed = discord.Embed(title="Market", description=msg, color=color)
        market_embed.set_image(url=img)
        
        return market_embed
        
    def generate_view(self, goods_callback, services_callback, buildings_callback, sell_callback):
        """
        Generate a `View` object (consisting of buttons) for the UI of `/market`
        """
        view = discord.ui.View()
        goods_button = discord.ui.Button(style=discord.ButtonStyle.danger, label="Goods")
        services_button = discord.ui.Button(style=discord.ButtonStyle.blurple, label="Services")
        buildings_button = discord.ui.Button(style=discord.ButtonStyle.green, label="Buildings")
        sell_button = discord.ui.Button(style=discord.ButtonStyle.gray, label="Sell")
        
        buttons = [(goods_button, goods_callback), 
                          (services_button, services_callback),
                          (buildings_button, buildings_callback),
                          (sell_button, sell_callback)]
        
        for tup in buttons:
            button, callback_func = tup[0], tup[1]
            button.callback = callback_func
            view.add_item(item=button)
            
        return view

# =============================================== [ MarketGoods ] ===============================================

class MarketGoods():
    def __init__(self):
        self.goods_msg = None
        self.color = None
        self.market_callback = None
        self.chosen_item = None
    
    def generate_embed(self, msg, color):
        """
        Class responsible for generating the UI of the callback of
        the `Goods` button from `/market`
        """
        self.goods_msg, self.color = msg, color
        embed = discord.Embed(title="Goods", description=self.goods_msg, color=self.color)
        return embed
        
    def generate_view(self, market_callback):
        """
        Generate a `View` object (consisting of buttons) for the UI of `/market`
        """
        view = discord.ui.View()
            
        natural_resources = []
        for name, details in NATURAL_RESOURCES_DICT.items():
            value = name
            label = value + f" (${str(details['cost'])})"
            option = discord.SelectOption(label=label, value=value)
            natural_resources.append(option)
            
        consumables = []
        for name, details in CONSUMABLES_DICT.items():
            value = name
            label = value + f" (${str(details['cost'])})"
            option = discord.SelectOption(label=label, value=value)
            consumables.append(option)
            
        tools = []
        for name, details in TOOLS_DICT.items():
            value = name
            label = value + f" (${str(details['cost'])})"
            option = discord.SelectOption(label=label, value=value)
            tools.append(option)
            
        # Dropdown objects
        natural_resources_dropdown = discord.ui.Select(placeholder='Natural Resources', options=natural_resources)
        consumables_dropdown = discord.ui.Select(placeholder='Consumables', options=consumables)
        tools_dropdown = discord.ui.Select(placeholder='Tools', options=tools)
        
        dropdowns = [natural_resources_dropdown, consumables_dropdown, tools_dropdown]
        for dropdown in dropdowns:
            dropdown.callback = self.purchase_confirmation
            view.add_item(dropdown)    
            
        # "Return to Market" button
        market_button = discord.ui.Button(style=discord.ButtonStyle.gray, label="Return to Market")
        self.market_callback = market_callback
        market_button.callback = self.market_callback
        view.add_item(market_button)
            
        return view
    
    async def purchase_confirmation(self, inter):
        self.chosen_item = inter.data['values'][0]  # Extract the selected value
        dictionaries = [NATURAL_RESOURCES_DICT, CONSUMABLES_DICT, TOOLS_DICT]
        for dictionary in dictionaries:
            for name, details in dictionary.items():
                if name == self.chosen_item:
                    cost = details["cost"]
                    break
        msg = f"You have chosen to purchase '{self.chosen_item}' for $" + str(cost)
        embed = discord.Embed(title="Are you sure?", description=msg, color=self.color)
    
        view = discord.ui.View()
        yes_button = discord.ui.Button(style=discord.ButtonStyle.green, label="Yes")
        no_button = discord.ui.Button(style=discord.ButtonStyle.danger, label="No")
        buttons = [(yes_button, self.yes_callback),
                   (no_button, self.no_callback)]
        for tup in buttons:
            button, callback_func = tup[0], tup[1]
            button.callback = callback_func
            view.add_item(item=button)
    
        await inter.response.edit_message(embed=embed, view=view)
        
    async def yes_callback(self, inter):
        # await inter.response.edit_message(f"You have successfully purchased {self.chosen_item}")
        msg = f"You have successfully purchased {self.chosen_item}!"
        embed = discord.Embed(title="Transaction complete.", description=msg, color=self.color)
        view = discord.ui.View()
        market_button = discord.ui.Button(style=discord.ButtonStyle.gray, label="Return to Market")
        market_button.callback = self.market_callback
        view.add_item(market_button)
        await inter.response.edit_message(embed=embed, view=view)
    
    async def no_callback(self, inter):
        embed = self.generate_embed(msg=self.goods_msg, color=self.color)
        view = self.generate_view(market_callback=self.market_callback)
        await inter.response.edit_message(embed=embed, view=view)

# =============================================== [ MarketServices ] ===============================================

class MarketServices():
    def __init__(self):
        self.services_msg = None
        self.color = None
        self.market_callback = None
        self.chosen_item = None
    
    def generate_embed(self, msg, color):
        """
        Class responsible for generating the UI of the callback of
        the `Goods` button from `/market`
        """
        self.services_msg, self.color = msg, color
        embed = discord.Embed(title="Services", description=self.services_msg, color=self.color)
        return embed
        
    def generate_view(self, market_callback):
        """
        Generate a `View` object (consisting of buttons) for the UI of `/market`
        """
        view = discord.ui.View()
            
        gatherers = []
        for name, details in GATHERERS_DICT.items():
            value = name
            label = value + f" (${str(details['cost'])})"
            option = discord.SelectOption(label=label, value=value)
            gatherers.append(option)
            
        military = []
        for name, details in MILITARY_DICT.items():
            value = name
            label = value + f" (${str(details['cost'])})"
            option = discord.SelectOption(label=label, value=value)
            military.append(option)
            
        boosting = []
        for name, details in BOOSTING_DICT.items():
            value = name
            label = value + f" (${str(details['cost'])})"
            option = discord.SelectOption(label=label, value=value)
            boosting.append(option)
        
        # Dropdown objects
        gatherers_dropdown = discord.ui.Select(placeholder='Gatherers', options=gatherers)
        military_dropdown = discord.ui.Select(placeholder='Military', options=military)
        boosting_dropdown = discord.ui.Select(placeholder='Boosting', options=boosting)
        
        dropdowns = [gatherers_dropdown, military_dropdown, boosting_dropdown]
        for dropdown in dropdowns:
            dropdown.callback = self.purchase_confirmation
            view.add_item(dropdown)    
            
        # "Return to Market" button
        market_button = discord.ui.Button(style=discord.ButtonStyle.gray, label="Return to Market")
        self.market_callback = market_callback
        market_button.callback = self.market_callback
        view.add_item(market_button)
            
        return view
    
    async def purchase_confirmation(self, inter):
        self.chosen_item = inter.data['values'][0]  # Extract the selected value
        service_desc = "Description not found."
        dictionaries = [GATHERERS_DICT, MILITARY_DICT, BOOSTING_DICT]
        for dictionary in dictionaries:
            for name, details in dictionary.items():
                if name == self.chosen_item:
                    service_desc = details["description"]
                    break
        service_desc += f"\n\nClick 'Yes' to confirm the purchase. Otherwise, click 'No'"
        embed = discord.Embed(title=self.chosen_item, description=service_desc, color=self.color)
    
        view = discord.ui.View()
        yes_button = discord.ui.Button(style=discord.ButtonStyle.green, label="Yes")
        no_button = discord.ui.Button(style=discord.ButtonStyle.danger, label="No")
        buttons = [(yes_button, self.yes_callback),
                   (no_button, self.no_callback)]
        for tup in buttons:
            button, callback_func = tup[0], tup[1]
            button.callback = callback_func
            view.add_item(item=button)
    
        await inter.response.edit_message(embed=embed, view=view)
        
    async def yes_callback(self, inter):
        # await inter.response.edit_message(f"You have successfully purchased {self.chosen_item}")
        msg = f"You have successfully purchased {self.chosen_item}!"
        embed = discord.Embed(title="Transaction complete.", description=msg, color=self.color)
        view = discord.ui.View()
        market_button = discord.ui.Button(style=discord.ButtonStyle.gray, label="Return to Market")
        market_button.callback = self.market_callback
        view.add_item(market_button)
        await inter.response.edit_message(embed=embed, view=view)
    
    async def no_callback(self, inter):
        embed = self.generate_embed(msg=self.services_msg, color=self.color)
        view = self.generate_view(market_callback=self.market_callback)
        await inter.response.edit_message(embed=embed, view=view)
        
# =============================================== [ MarketBuildings ] ===============================================

class MarketBuildings():
    def __init__(self):
        self.buildings_msg = None
        self.color = None
        self.market_callback = None
        self.chosen_item = None
    
    def generate_embed(self, msg, color):
        """
        Class responsible for generating the UI of the callback of
        the `Goods` button from `/market`
        """
        self.buildings_msg, self.color = msg, color
        embed = discord.Embed(title="Buildings", description=self.buildings_msg, color=self.color)
        return embed
        
    def generate_view(self, market_callback):
        """
        Generate a `View` object (consisting of buttons) for the UI of `/market`
        """
        view = discord.ui.View()
            
        buildings = []
        for name, details in BUILDINGS_DICT.items():
            value = name
            label = value + f" (${str(details['cost'])})"
            option = discord.SelectOption(label=label, value=value)
            buildings.append(option)
        
        # Dropdown objects
        buildings_dropdown = discord.ui.Select(placeholder='Buildings', options=buildings)
        buildings_dropdown.callback = self.purchase_confirmation
        view.add_item(buildings_dropdown)    
            
        # "Return to Market" button
        market_button = discord.ui.Button(style=discord.ButtonStyle.gray, label="Return to Market")
        self.market_callback = market_callback
        market_button.callback = self.market_callback
        view.add_item(market_button)
            
        return view
    
    async def purchase_confirmation(self, inter):
        self.chosen_item = inter.data['values'][0]  # Extract the selected value
        service_desc = "Description not found."
        dictionaries = [BUILDINGS_DICT]
        for dictionary in dictionaries:
            for name, details in dictionary.items():
                if name == self.chosen_item:
                    service_desc = details["description"]
                    break
        service_desc += f"\n\nClick 'Yes' to confirm the purchase. Otherwise, click 'No'"
        embed = discord.Embed(title=self.chosen_item, description=service_desc, color=self.color)
    
        view = discord.ui.View()
        yes_button = discord.ui.Button(style=discord.ButtonStyle.green, label="Yes")
        no_button = discord.ui.Button(style=discord.ButtonStyle.danger, label="No")
        buttons = [(yes_button, self.yes_callback),
                   (no_button, self.no_callback)]
        for tup in buttons:
            button, callback_func = tup[0], tup[1]
            button.callback = callback_func
            view.add_item(item=button)
    
        await inter.response.edit_message(embed=embed, view=view)
        
    async def yes_callback(self, inter):
        # await inter.response.edit_message(f"You have successfully purchased {self.chosen_item}")
        msg = f"You have successfully purchased {self.chosen_item}!"
        embed = discord.Embed(title="Transaction complete.", description=msg, color=self.color)
        view = discord.ui.View()
        market_button = discord.ui.Button(style=discord.ButtonStyle.gray, label="Return to Market")
        market_button.callback = self.market_callback
        view.add_item(market_button)
        await inter.response.edit_message(embed=embed, view=view)
    
    async def no_callback(self, inter):
        embed = self.generate_embed(msg=self.buildings_msg, color=self.color)
        view = self.generate_view(market_callback=self.market_callback)
        await inter.response.edit_message(embed=embed, view=view)
    
# Setup function
async def setup(client):
    await client.add_cog(MarketErrorHandler(client))