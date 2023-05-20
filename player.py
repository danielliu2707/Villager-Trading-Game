from __future__ import annotations
"""

This file represents the implementation of the Player class, representing the Minecraft Player Object

October 2022
"""

__author__ = "Code by Daniel Liu, Ben Abraham, Johnny Ta, Bangze Han"

from operator import index
from hash_table import LinearProbeTable
from random_gen import RandomGen
from cave import Cave
from material import Material
from trader import Trader
from food import Food
from trader import RandomTrader
from heap import MaxHeapTuple
from constants import EPSILON

# List taken from https://minecraft.fandom.com/wiki/Mob
PLAYER_NAMES = [
    "Steve",
    "Alex",
    "ɘᴎiɿdoɿɘH",
    "Allay",
    "Axolotl",
    "Bat",
    "Cat",
    "Chicken",
    "Cod",
    "Cow",
    "Donkey",
    "Fox",
    "Frog",
    "Glow Squid",
    "Horse",
    "Mooshroom",
    "Mule",
    "Ocelot",
    "Parrot",
    "Pig",
    "Pufferfish",
    "Rabbit",
    "Salmon",
    "Sheep",
    "Skeleton Horse",
    "Snow Golem",
    "Squid",
    "Strider",
    "Tadpole",
    "Tropical Fish",
    "Turtle",
    "Villager",
    "Wandering Trader",
    "Bee",
    "Cave Spider",
    "Dolphin",
    "Enderman",
    "Goat",
    "Iron Golem",
    "Llama",
    "Panda",
    "Piglin",
    "Polar Bear",
    "Spider",
    "Trader Llama",
    "Wolf",
    "Zombified Piglin",
    "Blaze",
    "Chicken Jockey",
    "Creeper",
    "Drowned",
    "Elder Guardian",
    "Endermite",
    "Evoker",
    "Ghast",
    "Guardian",
    "Hoglin",
    "Husk",
    "Magma Cube",
    "Phantom",
    "Piglin Brute",
    "Pillager",
    "Ravager",
    "Shulker",
    "Silverfish",
    "Skeleton",
    "Skeleton Horseman",
    "Slime",
    "Spider Jockey",
    "Stray",
    "Vex",
    "Vindicator",
    "Warden",
    "Witch",
    "Wither Skeleton",
    "Zoglin",
    "Zombie",
    "Zombie Villager",
    "H̴͉͙̠̥̹͕͌̋͐e̸̢̧̟͈͍̝̮̹̰͒̀͌̈̆r̶̪̜͙̗̠̱̲̔̊̎͊̑̑̚o̷̧̮̙̗̖̦̠̺̞̾̓͆͛̅̉̽͘͜͝b̸̨̛̟̪̮̹̿́̒́̀͋̂̎̕͜r̸͖͈͚̞͙̯̲̬̗̅̇̑͒͑ͅi̶̜̓̍̀̑n̴͍̻̘͖̥̩͊̅͒̏̾̄͘͝͝ę̶̥̺̙̰̻̹̓̊̂̈́̆́̕͘͝͝"
]


class Player():
    """

    This Class represents the Player object, facilitating the functionality of a Minecraft Player
    
    Class Attributes:
        DEFAULT_EMERALDS (int): An integer representing the default amount of emeralds for a player if a paramter is not passed through the init constructor method
        MIN_EMERALDS (int): An integer representing the minimum amount of emeralds a player can have
        MAX_EMERALDS (int): An integer representing the maximum amount of emerals a player can have
    
    Instance attributes:
        name (str): The string representing 
    """
    DEFAULT_EMERALDS = 50
    MIN_EMERALDS = 14
    MAX_EMERALDS = 40

    def __init__(self, name, emeralds=None) -> None:
        self.name = name
        self.balance = self.DEFAULT_EMERALDS if emeralds is None else emeralds
        self.caves = None
        self.caves_length = 0
        self.traders = None
        self.material = []
        self.foods = []
        self.item_sold = 0
        self.hunger = 0

    def set_traders(self, traders_list: list[Trader]) -> None:
        self.traders = LinearProbeTable(len(traders_list))
        for i in range(len(traders_list)):
            if traders_list[i].deal:
                if (traders_list[i].deal[0].name in self.traders.keys()):
                    if (traders_list[i].deal[1] not in self.traders[traders_list[i].deal[0].name]):
                        first_quantity = self.traders[traders_list[i].deal[0].name]  # save first quantity in memory
                        first_quantity.append(traders_list[i].deal[1])
                else:
                    self.traders[traders_list[i].deal[0].name] = [traders_list[i].deal[1]]  # -> price for the deal

    def set_foods(self, foods_list: list[Food]) -> None:
        self.foods = foods_list

    @classmethod
    def random_player(self) -> Player:
        return Player(PLAYER_NAMES[RandomGen.randint(0, len(PLAYER_NAMES) - 1)])

    def set_materials(self, materials_list: list[Material]) -> None:
        # for i in range(len(materials_list)):
        #    self.hash_table_player[materials_list[i].name] = materials_list[i].mining_rate
        self.material = materials_list

    def set_caves(self, caves_list: list[Cave]) -> None:
        self.caves = LinearProbeTable(len(caves_list))
        self.caves_length = len(caves_list)
        for i in range(len(caves_list)):
            if (caves_list[i].material.name in self.caves.keys()):
                if (caves_list[i] not in self.caves[caves_list[i].material.name]):
                    first_quantity = self.caves[caves_list[i].material.name]  # save first quantity in memory
                    first_quantity.append(
                        caves_list[i])  # set the value as a value of a container with both quantity values
            else:
                self.caves[caves_list[i].material.name] = [caves_list[i]]  # Tuple (cave_material, material_quantity)

    def select_food_and_caves(self) -> tuple[Food | None, float, list[tuple[Cave, float]]]:
        """
        First find maximum selling prices for each material for each trader by iterating through every deal
        and every material sold. O(T+M) time.
        For example: If traders = [(trader1: ("Prismarine", 10)), (trader2: ("Gold", 5))]
                        materials = [(Prismarine, 11), (Gold,3), (Iron,22)]
                    Max price hash table will look like [("Prismarine", 10), ("Gold", 5), ("Iron", 0)]

        Then, iterate through each food option (and select it if the player can buy it with their current balance).
        Get the amount of hunger bars it can receive. O(F).
        After selecting a food, for each cave, generate how efficient it is to mine a cave. This is the max price/material.mining_rate.
        This will take O(C) time. Store the cave object and efficiency into an array.
        For example: Prismarine has a price of 10 and mining_rate of 11, so its efficiency will be 10/11
                    This will be appended to efficiency_array(10/11, cave_object)

        Then construct a bottom_up max heap, with the most efficient cave at the top and the efficiency as the key.
        This will also take another O(C) time.
        Keep calling get_max on the heap to get the most efficient cave to mine, add the cave mined into a temporary list.
        This will have a worst case of O(C) time, and best case of O(1).
        Subtract hunger with efficiency*quantity mined, until it runs out of hunger bars.
        When that happens, find the ratio required to reach a hunger stat of 0, and multiply the quantity and emeralds earned by the ratio.
        If the result emeralds earned is greater than 0 or the max, update the max emerald and caves plundered.
        This entire sequence will have O(F * 3C) time.
        For example: Say the prismarine cave has 10 quantity, and the gold cave has 5 quantity.
                    We have 120 hunger bars
                    So call get_max on the cave to retrieve the prismarine
                    The prismarine has a mining_rate of 10, and we can mine 10 prismarine, costing us 100 hunger bars.
                    So it mines the entire prismarine cave, adding 100 emeralds to the temporary emerald balance.
                    We have 20 hunger bars remaining.
                    Retrieve the next most efficient, the gold, but it has a capacity of 5.
                    Since the cost of mining_rate of gold is 5, it costs 5*5 = 25 hunger bars to mine the entire gold cave.
                    So we must calculate a ratio, and find that we can only retrieve 4 gold from the cave.
                    Add 5*4 emeralds to the temporary balance.
                    Since we are out of hunger bars, we check if the emerald balance is higher than the current maximum/0, whichever is higher.
                    If that is the case, we update the food, and the caves plundered.

        :complexity: O(M + T + F * 3C), where M = number of materials, T = number of traders, F = number of foods, and C = number of caves
        :return: the food purchased, and a list of caves plundered and the amounts mined from the cave
        """
        max_emeralds = 0
        max_food = None
        caves_plundered = []

        max_prices = LinearProbeTable(len(self.traders))
        # Finding max prices O(T + M)
        # Iterate through all materials sold by traders, add the maximum price for each material into max_prices.
        for mats in self.traders.keys():
            for deal in self.traders[mats]:
                # In hashtable so add if it is larger
                try:
                    if max_prices[mats] < deal - EPSILON:
                        max_prices[mats] = deal
                # Not in hashtable so just insert it
                except KeyError:
                    max_prices[mats] = deal

        # If not selling material, add into max price as 0
        for material in self.material:
            try:
                if max_prices[material.name]:
                    pass
            except KeyError:
                max_prices[material.name] = 0

        # Iterate through food, and calculate largest emerald gain for each food.
        # O(F * 3C)
        for food in self.foods:
            if food.price < self.balance - EPSILON:
                max_emeralds = 0
                cur_emeralds = -food.price
                self.hunger = food.hunger_bars
                # Iterate through caves and create a max heap
                cave_efficiency = MaxHeapTuple(self.caves_length)
                efficiency_array = []
                # Iterate through all caves (O(C)) time where C is the number of caves
                for mats in self.caves.keys():
                    for cave in self.caves[mats]:
                        # For each cave, calculate amount and efficiency
                        efficiency = max_prices[cave.material.name] / cave.material.mining_rate
                        # Append cave and efficiency as a pair
                        efficiency_array.append((efficiency, cave))
                # Construct O(C) max heap based on efficiency
                cave_efficiency.bottom_up(efficiency_array)
                temp_plundered = []
                # Mine till hungry, keep calling get_max()
                # Worst case O(C), best case O(1)
                while self.hunger > 0 + EPSILON:
                    # Get cave object
                    cave = cave_efficiency.get_max()[1]
                    # Calculate hunger loss and emerald gain
                    hunger_loss = cave.material.mining_rate * cave.quantity
                    emerald_gain = cave.quantity * max_prices[cave.material.name]
                    # Assume cave is mined completely
                    quantity_mined = cave.quantity
                    # Enough hunger points, just subtract from self.hunger
                    if hunger_loss < self.hunger:
                        self.hunger -= hunger_loss
                        # Increment earned emeralds
                        cur_emeralds += emerald_gain
                    # Not enough hunger points, calculate ratio to get hunger to = 0.
                    else:
                        ratio = self.hunger / hunger_loss
                        # Avoiding floating point shenanigans, set to 0
                        self.hunger = 0
                        # Apply ratio to emeralds earned and quantity mined
                        cur_emeralds += emerald_gain * ratio
                        quantity_mined = quantity_mined * ratio
                    # Append cave object and quantity mined to plundered
                    temp_plundered.append((cave,quantity_mined))
                if cur_emeralds > max_emeralds + EPSILON:
                    # If this results in new max emerald gain, update return values
                    caves_plundered = temp_plundered
                    max_emeralds = cur_emeralds
                    max_food = food
        self.item_sold += self.balance + max_emeralds
        return max_food, self.item_sold, caves_plundered

    def __str__(self) -> str:
        return f'{self.name} has {self.balance} emeralds'  # Subject to change


if __name__ == "__main__":
    print(Player("Steve"))
    print(Player("Alex", emeralds=1000))

    p = Player("Alexey", emeralds=50)

    gold = Material("Gold Nugget", 27.24)
    netherite = Material("Netherite Ingot", 20.95)
    fishing_rod = Material("Fishing Rod", 26.93)
    ender_pearl = Material("Ender Pearl", 13.91)
    prismarine = Material("Prismarine Crystal", 11.48)

    materials = [
        gold,
        netherite,
        fishing_rod,
        ender_pearl,
        prismarine,
    ]
    p.set_materials(materials)
    caves = [
        Cave("Boulderfall Cave", prismarine, 10),
        Cave("Castle Karstaag Ruins", netherite, 4),
        Cave("Glacial Cave", gold, 3),
        Cave("Orotheim", fishing_rod, 6),
        Cave("Red Eagle Redoubt", fishing_rod, 3),
    ]
    waldo = RandomTrader("Waldo Morgan")
    waldo.add_material(fishing_rod)
    waldo.generate_deal()
    waldo.deal = (fishing_rod,
                  7.44)  # This is how my solution can hackily set the selling price - your solution does NOT need to support the same.
    orson = RandomTrader("Orson Hoover")
    orson.add_material(gold)
    orson.generate_deal()
    orson.deal = (gold,
                  7.70)  # This is how my solution can hackily set the selling price - your solution does NOT need to support the same.
    lea = RandomTrader("Lea Carpenter")
    lea.add_material(prismarine)
    lea.generate_deal()
    lea.deal = (prismarine,
                7.63)  # This is how my solution can hackily set the selling price - your solution does NOT need to support the same.
    ruby = RandomTrader("Ruby Goodman")
    ruby.add_material(netherite)
    ruby.generate_deal()
    ruby.deal = (netherite,
                 9.78)  # This is how my solution can hackily set the selling price - your solution does NOT need to support the same.
    mable = RandomTrader("Mable Hodge")
    mable.add_material(gold)
    mable.generate_deal()
    mable.deal = (gold,
                  5.40)  # This is how my solution can hackily set the selling price - your solution does NOT need to support the same.
    p.set_caves(caves)
    traders = [
        waldo,
        orson,
        lea,
        ruby,
        mable,
    ]

    # Avoid simulate_day - This regenerates trader deals and foods.
    p.set_traders(traders)
    foods = [
        Food("Cabbage Seeds", 106, 30),
        Food("Fried Rice", 129, 24),
        Food("Cooked Chicken Cuts", 424, 19),
    ]
    p.set_foods(foods)
    print(p.caves_length)
    print(p.select_food_and_caves())

    # Food = Cooked Chicken Cuts
    # Balance = 209.
    # Caves = [
    # (<Cave: Castle Karstaag Ruins. 4 of [Netherite Ingot: 20.95🍗/💎]>, 4.0),
    # (<Cave: Red Eagle Redoubt. 3 of [Fishing Rod: 26.93🍗/💎]>, 3.0),
    # (<Cave: Glacial Cave. 3 of [Gold Nugget: 27.24🍗/💎]>, 3.0),
    # (<Cave: Boulderfall Cave. 10 of [Prismarine Crystal: 11.48🍗/💎]>, 10.0),
    # (<Cave: Orotheim. 6 of [Fishing Rod: 26.93🍗/💎]>, 2.335313776457482),
    # ]
