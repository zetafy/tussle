# TEMPORARY MODULE FOR DATA STORAGE BEFORE DATABASE IS MADE

import discord
from discord.ext import commands

# ModuleNotFoundError handler
class DataErrorHandler(commands.Cog):
    """
    Handles discord.py's `/cogs` exception thrower
    """
    def __init__(self, client: commands.Bot):
        self.client = client
        
    @commands.Cog.listener()
    async def on_ready(self):
        print("(LOADED): data.py")
        
async def setup(client):
    await client.add_cog(DataErrorHandler(client))

# =============================================== [ Goods Data ] ===============================================

NATURAL_RESOURCES_DICT = {
    "Wood": {
        "cost": 0,
    },
    "Coal": {
        "cost": 0,
    },
    "Iron": {
        "cost": 0,
    }
}

CONSUMABLES_DICT = {
    "Loads of Bread": {
        "cost": 0,
    },
    "Loads of Beef": {
        "cost": 0,
    },
    "Loads of Fish": {
        "cost": 0,
    }
}

TOOLS_DICT = {
    "A": {
        "cost": 0,
    },
    "B": {
        "cost": 0,
    },
    "C": {
        "cost": 0,
    }
}
    
# =============================================== [ Services Data ] ===============================================
GATHERERS_DICT = {
    "Farmer": {
        "cost": 0,
        "description": "Produces 1 wheat every 5 seconds"
    },
    "Miner": {
        "cost": 0,
        "description": "Produces 1 stone and one of iron, copper, or diamond every 5 seconds"
    },
}

MILITARY_DICT = {
    "Pilot": {
        "cost": 0,
        "description": "Can be used to man a spaceship",
    },
    "Soldier": {
        "cost": 0,
        "description": "Increases your colony's outgoing damage by 10"
    },
    "Medic": {
        "cost": 0,
        "description": "Increases the health of your troop's health in raids by 10"
    }
}

BOOSTING_DICT = {
    "Businessman": {
        "cost": 0,
        "description": "Increases your income rate by 2%",
    },
    "Food Scientist": {
        "cost": 0,
        "description": "Decreases the rate at which the hunger level decreases"
    }
}

# =============================================== [ Building Data ] ===============================================
BUILDINGS_DICT = {
    "Farmland": {
        "cost": 0,
        "description": "Produces a 2 wheats and one of beef, pork, or fish meat every second"
    },
    "Wood Factory": {
        "cost": 0,
        "description": "Produces 1 wood every second"
    }
}