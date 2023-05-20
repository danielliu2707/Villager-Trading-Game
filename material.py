"""

This file demonstrates the implementation of the Material Class

October 2022
"""

__author__ = "Code by Daniel Liu, Ben Abraham, Johnny Ta, Bangze Han"

from random_gen import RandomGen

# Material names taken from https://minecraft-archive.fandom.com/wiki/Items
RANDOM_MATERIAL_NAMES = [
    "Arrow",
    "Axe",
    "Bow",
    "Bucket",
    "Carrot on a Stick",
    "Clock",
    "Compass",
    "Crossbow",
    "Exploration Map",
    "Fire Charge",
    "Fishing Rod",
    "Flint and Steel",
    "Glass Bottle",
    "Dragon's Breath",
    "Hoe",
    "Lead",
    "Map",
    "Pickaxe",
    "Shears",
    "Shield",
    "Shovel",
    "Sword",
    "Saddle",
    "Spyglass",
    "Totem of Undying",
    "Blaze Powder",
    "Blaze Rod",
    "Bone",
    "Bone meal",
    "Book",
    "Book and Quill",
    "Enchanted Book",
    "Bowl",
    "Brick",
    "Clay",
    "Coal",
    "Charcoal",
    "Cocoa Beans",
    "Copper Ingot",
    "Diamond",
    "Dyes",
    "Ender Pearl",
    "Eye of Ender",
    "Feather",
    "Spider Eye",
    "Fermented Spider Eye",
    "Flint",
    "Ghast Tear",
    "Glistering Melon",
    "Glowstone Dust",
    "Gold Ingot",
    "Gold Nugget",
    "Gunpowder",
    "Ink Sac",
    "Iron Ingot",
    "Iron Nugget",
    "Lapis Lazuli",
    "Leather",
    "Magma Cream",
    "Music Disc",
    "Name Tag",
    "Nether Bricks",
    "Paper",
    "Popped Chorus Fruit",
    "Prismarine Crystal",
    "Prismarine Shard",
    "Rabbit's Foot",
    "Rabbit Hide",
    "Redstone",
    "Seeds",
    "Beetroot Seeds",
    "Nether Wart Seeds",
    "Pumpkin Seeds",
    "Wheat Seeds",
    "Slimeball",
    "Snowball",
    "Spawn Egg",
    "Stick",
    "String",
    "Wheat",
    "Netherite Ingot",
]

class Material:
    """
    
    This is the Class that facilitates the Materials of the Minecraft game, representing the Material Object of the game

    Instance Attributes:
        name (str): A string representing the name of the Material Object
        mining_rate (float): A decimal that represents the rate of hunger bars the it costs to obtain one of the material
    """
    
    def __init__(self, name: str, mining_rate: float) -> None:
        """
        Initialises the material with a name and the mining rate associated to it

        Parameters:
            name (str): A string representing the name of the Material Object
            mining_rate (float): A decimal that represents the rate of hunger bars the it costs to obtain one of the material
        
        :complexity: O(1)
        """

        self.name = name
        self.mining_rate = mining_rate
    
    def __str__(self) -> str:
        """

        String method for the material 

        Returns:
            The String Representation of the Material Object

        Pre-Conditions (What must be true for method to be called):
            A string representation of the Object must have been called for
        
        Post-Conditions (What is true after method is callled):
            The string representation of the object has been returned
        
        Complexity:
            O(1)
        
        :complexity: O(1)
        """

        return f"{self.name}: {self.mining_rate}"

    @classmethod
    def random_material(cls):
        """
        
        Class method that returns a random material from the material list

        Returns:
            A Material Object that represents a randomly generated Material Object
        
        :complexity: O(1)
        """

        return Material(RANDOM_MATERIAL_NAMES[RandomGen.randint(0,len(RANDOM_MATERIAL_NAMES)-1)],(RandomGen.random_float())*100)

if __name__ == "__main__":
    
    print(Material("Coal", 4.5))
    print(Material.random_material())
