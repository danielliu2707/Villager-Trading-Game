from __future__ import annotations
"""

This file represents the implementation of the Game class, representing the Minecraft Game Object

October 2022
"""

__author__ = "Code by Daniel Liu, Ben Abraham, Johnny Ta, Bangze Han"

from player import Player
from trader import Trader, RandomTrader, RangeTrader, HardTrader
from material import Material
from cave import Cave
from food import Food
from random_gen import RandomGen
from hash_table import LinearProbeTable
from heap import MaxHeapTuple
from aset import ASet
from constants import EPSILON


class Game:
    """

    This class implements the game object for a Minecraft Game, able to facilitate the basic functionality of a minecraft game

    Class Attributes:
        MIN_MATERIALS (int): An integer representing the minimum amount of material objects
        MAX_MATERIALS (int): An integer representing the maximum amount of material objects
        MIN_CAVES (int): An integer representing the minimum amount of cave objects
        MAX_CAVES (int): An integer representing the maximum amount of cave objects
        MIN_TRADERS (int): An integer representing the minimum amount of trader objects
        MAXTRADERS (int): An integer representing the maximum amount of trader objects

    Instance Attributes:
        materials (None |  of Material Objects): A collection of Material Objects pertaining to the instantiation of the game object
        traders (None |  of Trader Objects): A collection of Trader Objects pertaining to the instantiation of the game object
        caves (None | __ of cave Objects): A collection of Cave Objects pertaining to the instantiation of the game object
    """

    MIN_MATERIALS = 5
    MAX_MATERIALS = 10

    MIN_CAVES = 5
    MAX_CAVES = 10

    MIN_TRADERS = 4
    MAX_TRADERS = 8

    MIN_FOOD = 2
    MAX_FOOD = 5

    def __init__(self) -> None:
        """"
        
        This is the constructor method for the Game Class, which initialises a new instance of the game object
        """
        
        self.materials = None
        self.traders = None
        self.caves = None

    def initialise_game(self) -> None:
        """
        
        This is the method that initialises all game objects: Materials, Caves, Traders.
        """

        N_MATERIALS = RandomGen.randint(self.MIN_MATERIALS, self.MAX_MATERIALS)
        self.generate_random_materials(N_MATERIALS)
        print("Materials:\n\t", end="")
        print("\n\t".join(map(str, self.get_materials())))

        N_CAVES = RandomGen.randint(self.MIN_CAVES, self.MAX_CAVES)
        self.generate_random_caves(N_CAVES)
        print("Caves:\n\t", end="")
        print("\n\t".join(map(str, self.get_caves())))

        N_TRADERS = RandomGen.randint(self.MIN_TRADERS, self.MAX_TRADERS)
        self.generate_random_traders(N_TRADERS)
        print("Traders:\n\t", end="")
        print("\n\t".join(map(str, self.get_traders())))

    def initialise_with_data(self, materials: list[Material], caves: list[Cave], traders: list[Trader]):
        """
        
        This method is the method that llows the user to create a game object with their own sets of given data

        Parameters:
            materials (list[Material]): A list of Material Objects
            caves: list[Cave]: A list of Cave Objects
            traders: List[Trader]: A list of Trader Objects
        """

        self.set_materials(materials)
        self.set_caves(caves)
        self.set_traders(traders)

    def set_materials(self, mats: list[Material]) -> None:
        """
        
        This is the method that sets the materials instance attribute

        Parameters:
            mats (Lists of Material Objects): A list of Material Objects
        """
        
        self.materials = mats

    def set_caves(self, caves: list[Cave]) -> None:
        """
        
        This is the method that sets the caves instance attribute

        Parameters:
            caves (Lists of Cave Objects): A list of Cave Objects
        """
        
        self.caves = caves

    def set_traders(self, traders: list[Trader]) -> None:
        """
        
        This is the method that sets the traders instance attribute

        Parameters:
            traders (Lists of Trader Objects): A list of Trader Objects
        """
        
        for trader in traders:
            if trader.deal is None:
                trader.generate_deal()
        self.traders = traders

    def get_materials(self) -> list[Material]:
        """
        
        This is the method that gets the value of the material instance attribute

        Returns:
            The Value of the Material Instance Attribute
        """
        
        return self.materials

    def get_caves(self) -> list[Cave]:
        """
        
        This is the method that gets the value of the caves instance attribute

        Returns:
            The Value of the Cave Instance Attribute
        """
        
        return self.caves

    def get_traders(self) -> list[Trader]:
        """
        
        This is the method that gets the value of the trader instance attribute

        Returns:
            The Value of the Trader Instance Attribute
        """
        
        return self.traders

    def generate_random_materials(self, amount):
        """
        This Method generates a random value for the material instance attribute
        Generates <amount> random materials using Material.random_material
        Generated materials will all have different names and different mining_rates.

        Parameters:
            amount (int): An integer representing the number of random materials to generate
        """

        output_material_list = []

        filter_list = []

        for _ in range(amount):
           
            # We have material to be added
            # 1) See if list is empty
            # 2) append both the material name and rate to filter list
            # 3) While material_to_be_added.rate is in filter_list OR material_to_be_added.name is in filter_list
                #material_to_be_added = Material.random_material()
            # 4) append output_material_list with material_to_be_added
            # 5) Set and end

             material_to_be_added = Material.random_material()
             filter_list.append(material_to_be_added.name)
             filter_list.append(material_to_be_added.mining_rate)

             if output_material_list != []:
                 while material_to_be_added.mining_rate in filter_list or material_to_be_added.name in filter_list:
                    material_to_be_added = Material.random_material()   
                 output_material_list.append(material_to_be_added)
                 filter_list.append(material_to_be_added.name)
                 filter_list.append(material_to_be_added.mining_rate)
             else:
                 output_material_list.append(material_to_be_added)

        self.set_materials(output_material_list)

    def generate_random_caves(self, amount):
        """
        This method generates a random number of cave objects
        Generates <amount> random caves using Cave.random_cave
        Generated caves will all have different names
        
        Parameters:
            amount (int): An integer representing the number of random materials to generate
        """
        
        cave_list = []
        filter_list = []
        for _ in range(amount):
            cave_to_be_added = Cave.random_cave(self.materials)

            if cave_list != []:

                filter_list.append(cave_to_be_added.name)

                while cave_to_be_added.name in filter_list:
                    cave_to_be_added = Cave.random_cave(self.materials)

                cave_list.append(cave_to_be_added)

            else:
                cave_list.append(cave_to_be_added)
                filter_list.append(cave_to_be_added.name)
        self.set_caves(cave_list)

    def generate_random_traders(self, amount):
        """

        This methods generates a random amount of trader objects
        Generates <amount> random traders by selecting a random trader class
        and then calling <TraderClass>.random_trader()
        and then calling set_all_materials with some subset of the already generated materials.
        Generated traders will all have different names
        
        Parameters:
            amount (int): An integer representing the number of random materials to generate
        """

        trader_index_int = RandomGen.randint(0, 2)
        trader_class = ['RandomTrader', 'RangeTrader', 'HardTrader']
        rand_trader_class = trader_class[trader_index_int]

        traders_list = []
        for _ in range(amount):
            material_list_trader = []
            for material in self.materials:
                if RandomGen.random_chance(0.5):
                    material_list_trader.append(material)
            if rand_trader_class == 'RandomTrader':
                trader = RandomTrader.random_trader()
            elif rand_trader_class == 'RangeTrader':
                trader = RangeTrader.random_trader()
            else:
                trader = HardTrader.random_trader()
            trader.set_all_materials(material_list_trader)
            trader.generate_deal()
            traders_list.append(trader)
        self.set_traders(traders_list)

    def finish_day(self):
        """

        This method simulates the end of the Minecraft Day
        """

        for cave in self.get_caves():
            if cave.quantity > 0 and RandomGen.random_chance(0.2):
                cave.remove_quantity(RandomGen.random_float() * cave.quantity)
            else:
                cave.add_quantity(round(RandomGen.random_float() * 10, 2))
            cave.quantity = round(cave.quantity, 2)


class SoloGame(Game):
    """
    
    This child class of the Game Class represents the instantiation of a Solo Minecraft Game Object

    Class Attributes:
        {Inherits all Class Attributes from Parent Class: Game}

    Instance Attributes:
        {Inherits all instance attributes from Parent Class: Game}
        player (Player Object): A PLayer Object representing the solo player in the Solo Minecraft Game
    """

    def initialise_game(self) -> None:
        """
            
        This method initialises the Solo Minecraft Game
        """

        super().initialise_game()
        self.player = Player.random_player()
        self.player.set_materials(self.get_materials())
        self.player.set_caves(self.get_caves())
        self.player.set_traders(self.get_traders())

    def initialise_with_data(self, materials: list[Material], caves: list[Cave], traders: list[Trader],
                             player_names: list[str], emerald_info: list[float]):
        """
        
        This method initialises the Solo Minecraft Game with data provided by the user

        Parameters:
            materials (list[Material]): A list of Material objects
            caves (list[Cave]): A list of cave objects
            traders (list[Trader]): A list of traders objects
            player names: (list[int]): A list of strings representing the names of the players
            emerald_info: (list[float]): A list of float decimals
        """

        super().initialise_with_data(materials, caves, traders)
        self.player = Player(player_names[0], emeralds=emerald_info[0])
        self.player.set_materials(self.get_materials())
        self.player.set_caves(self.get_caves())
        self.player.set_traders(self.get_traders())

    def simulate_day(self):
        """
        
        This method simulates a day of the Solo Minecraft Game
        """

        # 1. Traders make deals
        print("Traders Deals:\n\t", end="")
        print("\n\t".join(map(str, self.get_traders())))
        # 2. Food is offered
        food_num = RandomGen.randint(self.MIN_FOOD, self.MAX_FOOD)
        foods = []
        for _ in range(food_num):
            foods.append(Food.random_food())
        print("\nFoods:\n\t", end="")
        print("\n\t".join(map(str, foods)))
        self.player.set_foods(foods)
        # 3. Select one food item to purchase
        food, balance, caves = self.player.select_food_and_caves()
        print(food, balance, caves)
        # 4. Quantites for caves is updated, some more stuff is added.
        self.verify_output_and_update_quantities(food, balance, caves)

    def verify_output_and_update_quantities(self, food: Food | None, balance: float,
                                            caves: list[tuple[Cave, float]]) -> None:
        """
        
        This method updates the quantities of food, caves, and balances of the Game Attributes via outputs from the Player select food and caves method.

        Parameters:
            food (food | None): A food object or a None Type
            balance (float): A decimal representing the balance of the player after a day of Mining
            caves (list[tuple[Cave, float]]): A list of paired Cave's and decimal quantity mined from those caves
        """

        if food.price > self.player.balance and caves != []:
            raise ValueError("Insufficient funds")

        self.player.balance = balance

        for i in range(len(caves)):
            # caves is a list of tuple elements where the tuples consist of (material_mined, quantity_mined)
            material_of_cave = caves[i][0].material.name  # material object
            quantity_mined = caves[i][1]  # quantity mined

            if self.caves[i].material.name == material_of_cave:
                if quantity_mined <= self.caves[i].quantity:
                    self.caves[i].quantity -= quantity_mined
                else:
                    self.caves[i].quantity = 0


class MultiplayerGame(Game):
    """
    
    This child class of the Game Class represents the instantiation of a Solo Minecraft Game Object

    Class Attributes:
        {Inherits all Class Attributes from Parent Class: Game}
        MIN_PLAYERS (int): An integer representing the minimum number of players
        MAX_PLAYERS (int): An integer representing the maximum number of players

    Instance Attributes:
        {Inherits all instance attributes from Parent Class: Game}
        players (List[Player Objects]): A PLayer Object representing the solo player in the Solo Minecraft Game
    """
    
    MIN_PLAYERS = 2
    MAX_PLAYERS = 5

    def __init__(self) -> None:
        """
        
        The constructor method for the MultiplayerGame Child Class of the Game Parent Class
        """

        super().__init__()
        self.players = []

    def initialise_game(self) -> None:
        """
        
        This method initialises the MultiplayerGame Object with the relevant data it needs
        """

        super().initialise_game()
        N_PLAYERS = RandomGen.randint(self.MIN_PLAYERS, self.MAX_PLAYERS)
        self.generate_random_players(N_PLAYERS)
        for player in self.players:
            player.set_materials(self.get_materials())
            player.set_caves(self.get_caves())
            player.set_traders(self.get_traders())
        print("Players:\n\t", end="")
        print("\n\t".join(map(str, self.players)))

    def generate_random_players(self, amount) -> None:
        """
        
        This method generates a random number of players for the MultiplayerGame Object

        Parameters:
            amount (int): An integer representing the number of random players to generate
        """
        
        for _ in range(amount):
            self.players.append(Player.random_player())

    def initialise_with_data(self, materials: list[Material], caves: list[Cave], traders: list[Trader],
                             player_names: list[str], emerald_info: list[float]):
        """
        
        This method sets the MultiplayerGame Object with given data from the user

        Parameters:
            materials (list[Material]): A list of Material objects
            caves (list[Cave]): A list of cave objects
            traders (list[Trader]): A list of traders objects
            player names: (list[int]): A list of strings representing the names of the players
            emerald_info: (list[float]): A list of float decimals
            
        """
        
        super().initialise_with_data(materials, caves, traders)
        for player, emerald in zip(player_names, emerald_info):
            self.players.append(Player(player, emeralds=emerald))
            self.players[-1].set_materials(self.get_materials())
            self.players[-1].set_caves(self.get_caves())
            self.players[-1].set_traders(self.get_traders())
        print("Players:\n\t", end="")
        print("\n\t".join(map(str, self.players)))

    def simulate_day(self):
        """
        
        This method simulates a day of the Solo Minecraft Game
        """

        # 1. Traders make deals
        print("Traders Deals:\n\t", end="")
        print("\n\t".join(map(str, self.get_traders())))
        # 2. Food is offered
        offered_food = Food.random_food()
        print(f"\nFoods:\n\t{offered_food}")
        # 3. Each player selects a cave - The game does this instead.
        foods, balances, caves = self.select_for_players(offered_food)
        # 4. Quantities for caves is updated, some more stuff is added.
        self.verify_output_and_update_quantities(foods, balances, caves)

    def select_for_players(self, food: Food) -> tuple[list[Food|None], list[float], list[tuple[Cave, float]|None]]:

        """
        Approach:
        Step 1: From a player, pull the traders and materials
        Step 2: Initialise a hash table, and iterate through all trader deals.
                If a material is not in, just insert material and its corresponding price.
                Otherwise, just compare, if the price is higher than what is in the hash table, update.

        Step 3: Then, iterate through all materials, and check if they have a price in the hash table.
                If there is no price, simply insert it to the max price hash table and set the price to 0
        These steps(1-3) have a time complexity of O(M+T) where M is the #Materials, and T is #Traders.
                        For example: If traders = [(trader1: ("Prismarine", 10)), (trader2: ("Gold", 5))]
                                    materials = [(Prismarine, 10), (Gold,3), (Iron,22)]
                        Max price hash table will look like [("Prismarine", 10), ("Gold", 5), ("Iron", 0)]

        Step 4: Initialise a cave array, and iterate through all the caves.
                For each cave, calculate the emeralds gained from mining the cave (ignoring food price).
                This is the min(cave quantity, or the hunger bars / mining_rate of the material) * price of material.
                Save this result into a variable (called mineable).
                Append cave array with (mineable, (cave, cave_capacity)).
                This step will take O(C) time, where C is the amount of caves.
                E.g if prismarine has price of $10, cave quantity is 15 and food has 100 hunger bars
                    We can only mine hunger bars / material.mining_rate at most.
                    Our prismarine mining_rate is 10, so our quantity mineable is simple 100 / 10 = 10
                    Take the lower of quantity mineable and quantity in the cave. In this case, the cave quantity is 15
                    So the lower is 10.
                    we can only get 10*10 = 100 emeralds
                    example_array = [(100, (Prismarine,15)), (40, (Gold,6)), (0, (Iron,11.1)]

        Step 5: Initialise a max heap, which has been modified to take in a (key, item) pair.
                Using the cave array, create the heap bottom up.
                Root node has the cave with the highest amount of emeralds earned for mining it (wrt to food given).
                This step will take O(C) time, where C is the amount of caves

        Step 6: Then, we iterate through each player and check if they can afford the food.
                If they can afford the food, continue, otherwise just update with None.
                Then, get the most efficient cave by calling get_max with the heap.
                Save the results, and what we do with them depends on:
                If the player loses emeralds mining the cave:
                    Update with None
                    Reinsert the most efficient cave into the heap.
                    This will take O(log C) time, due to insertion.

                Elif the player mines the entire cave
                    Simply just update caves_plundered with the cave and the cave quantity
                    Update emeralds earned with max_emeralds + player balance
                    This will take O(1) time.

                Elif the player partially mines the cave:
                    We find the quantity remaining in the cave, and save the difference
                    Update caves_plundered with the cave and the difference.
                    Update the cave quantity with the quantity remaining.
                    Update the caves' mineable;
                    This is the min(cave quantity, or the hunger bars / mining_rate of the material) * price of material.
                    Reinsert the cave into the heap
                    This will take O(log C) time, due to insertion.

                For example:
                    Steve has 14 emeralds and can afford Raw Beef which has a price of 10 emeralds and 100 hunger bars.
                    Calling get_max, we pull res = (100, (Prismarine,15)).
                    Our emerald gain, or mineable, is res[0] = 100
                    Then, calculate the quantity lost by dividing the emerald gain by mining_rate, which is 10.
                    Since the cave would still have 5 emeralds left, we go to the partially mined case.
                    Then, we recalculate Step 4's mineable.
                    Our prismarine mining_rate is 10, so our quantity mineable based on food is simple 100 / 10 = 10
                    Our quantity is now 15-10, 5, so mineable based on cave capacity is 5*10 = 50
                    Take the lower of quantity mineable and quantity in the cave.
                    This will be 5 * 10 = 50
                    So our new quantity is 5, we update this into a temporary variable.
                    Then, we reinsert this cave into the max heap.
                    cave_heap.add(50,(cave,5))
                    Calculate our results
                    player_caves_plundered.append(Cave, 10)
                    player_food.append(Raw Beef)
                    Steve's balance will be player.balance + max_emeralds - food.price)
                    player_emeralds.append(10 + 100 - 14)
                    
        :pre: Must have at least 1 player in self.players, with its traders, materials, and caves initialised.
        :food: Food object containing the only food purchasable for each player
        :return: player_food, a list containing what food was bought for each player
                player_emeralds, a list containing emerald balances for each player
                player_caves_plundered a list containing cave plundered and amount mined for each player
        :complexity: O(M + T + C + P * log C), where M=#Materials, T=#Traders, C=#Caves, P=#Players.

        """
        # Initialise result lists
        player_emeralds = []
        player_food = []
        player_caves_plundered = []

        # Get traders from first player
        max_prices = LinearProbeTable(len(self.players[0].traders))
        traders_in_game = self.players[0].traders
        materials_in_game = self.players[0].material
        caves_in_game = self.players[0].caves

        # Finding max prices O(T + M)
        # Iterate through all materials sold by traders, add the maximum price for each material into max_prices.
        for mats in traders_in_game.keys():
            for deal in traders_in_game[mats]:
                # In hashtable so add if it is larger
                try:
                    if max_prices[mats] < deal:
                        max_prices[mats] = deal
                # Not in hashtable so just insert it
                except KeyError:
                    max_prices[mats] = deal

        # If not selling material, add into max price as 0
        for material in materials_in_game:
            try:
                if max_prices[material.name]:
                    pass
            except KeyError:
                max_prices[material.name] = 0
        # Get all caves, also create max heap to store
        # Find the max amount of emeralds you can get from cave with the food, let this be heap key
        # Then, store the cave object as the item
        # O(C) time complexity
        cave_array = []
        for mats in caves_in_game.keys():
            for cave in caves_in_game[mats]:
                price = max_prices[cave.material.name]
                # Finding total emeralds that can be gained from the cave
                total = price * cave.quantity
                # Find amount actually mineable with the food from the cave
                mineable = total
                if cave.quantity and cave.material.mining_rate:
                    mineable = min(total, food.hunger_bars / (cave.material.mining_rate * cave.quantity) * total)
                cave_capacity = cave.quantity
                cave_array.append((mineable, (cave,cave_capacity)))

        # Create heap bottom up, O(C) time complexity
        cave_heap = MaxHeapTuple(len(cave_array))
        cave_heap.bottom_up(cave_array)

        # For each player, get most optimal cave
        for player in self.players:
            if player.balance > food.price:
                optimal_res = cave_heap.get_max()
                # Stored as (key, item) -> (emeralds gained wrt to food hunger bar, cave object)
                max_emeralds = optimal_res[0]
                max_cave = optimal_res[1][0]
                max_cave_quantity = optimal_res[1][1]
                # print(max_cave)
                # If optimal cave quantity is not the total amount in the cave, reinsert the cave with updated amount.
                # O(log C) time
                # If we lose emeralds, just don't mine, and reinsert the max into heap.
                if max_emeralds - food.price < - EPSILON:
                    player_food.append(None)
                    player_emeralds.append(player.balance)
                    player_caves_plundered.append((None, 0))
                    cave_heap.add(optimal_res)

                elif not (max_cave_quantity * max_prices[max_cave.material.name] - max_emeralds < EPSILON):
                    # Update new quantity remaining
                    quantity_lost = max_emeralds / max_prices[max_cave.material.name]
                    max_cave_quantity = max_cave.quantity - quantity_lost
                    price = max_prices[max_cave.material.name]
                    # Update the new max price
                    total = price * max_cave_quantity
                    mineable = total
                    # Avoid division by 0
                    if max_cave.material.mining_rate and max_cave_quantity:
                        mineable = min(total,food.hunger_bars / (max_cave.material.mining_rate * max_cave_quantity) * total)
                    cave_heap.add((mineable, (max_cave,max_cave_quantity)))
                    # Update results for the day
                    player_food.append(food)
                    player_emeralds.append(player.balance + max_emeralds - food.price)
                    player_caves_plundered.append((max_cave, quantity_lost))

                # Mined the whole cave
                else:
                    player_food.append(food)
                    player_emeralds.append(player.balance + max_emeralds - food.price)
                    player_caves_plundered.append((max_cave, max_cave.quantity))

            # Cant afford food :c, just update with None
            else:
                player_food.append(None)
                player_emeralds.append(player.balance)
                player_caves_plundered.append((None, 0))

        return player_food, player_emeralds, player_caves_plundered

    def verify_output_and_update_quantities(self, foods: list[Food | None], balances: list[float],
                                            caves: list[tuple[Cave, float] | None]) -> None:
        """
        Verify output of select_for_players

        :complexity: O(P * C * O(comp==)) where P is number of players, C is the number of caves plundered 
        """
        for player_index in range(len(self.players)):
            self.players[player_index].balance = balances[player_index]
            if foods[player_index] and caves[player_index]:
                for i in range(len(caves[player_index])):
                    # caves is a list of tuple elements where the tuples consist of (Cave object, quantity_mined)
                    material_of_cave = caves[player_index][0].material.name  # material name
                    quantity_mined = caves[player_index][1]  # quantity mined
                    if self.caves[i].material.name == material_of_cave:
                        if quantity_mined <= self.caves[i].quantity:
                            # Update cave quantities
                            self.caves[i].quantity -= quantity_mined
                        else:
                            self.caves[i].quantity = 0

if __name__ == "__main__":
    r = RandomGen.seed  # Change this to set a fixed seed.
    RandomGen.set_seed(123)
    print(r)

    # g = SoloGame()
    # g.initialise_game()

    # g.simulate_day()
    # g.finish_day()

    # g.simulate_day()
    # g.finish_day()

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
    waldo.sell = (fishing_rod,
              7.44)  # This is how my solution can hackily set the selling price - your solution does NOT need to support the same.
    orson = RandomTrader("Orson Hoover")
    orson.add_material(gold)
    orson.generate_deal()
    orson.sell = (gold,
              7.70)  # This is how my solution can hackily set the selling price - your solution does NOT need to support the same.
    lea = RandomTrader("Lea Carpenter")
    lea.add_material(prismarine)
    lea.generate_deal()
    lea.sell = (prismarine,
            7.63)  # This is how my solution can hackily set the selling price - your solution does NOT need to support the same.
    ruby = RandomTrader("Ruby Goodman")
    ruby.add_material(netherite)
    ruby.generate_deal()
    ruby.sell = (netherite,
             9.78)  # This is how my solution can hackily set the selling price - your solution does NOT need to support the same.
    mable = RandomTrader("Mable Hodge")
    mable.add_material(gold)
    mable.generate_deal()
    mable.sell = (gold,
              5.40)  # This is how my solution can hackily set the selling price - your solution does NOT need to support the same.

    traders = [
    waldo,
    orson,
    lea,
    ruby,
    mable,
    ]

    g = MultiplayerGame()
    g.initialise_with_data(materials, caves, traders, ["Alexey", "Jackson", "Saksham", "Brendon"], [50, 14, 35, 44])
    # Avoid simulate_day - This regenerates trader deals and foods.
    foods, balances, caves = g.select_for_players(Food("Cooked Chicken Cuts", 100, 19))
    g.verify_output_and_update_quantities(foods, balances, caves)
    for player in g.players:
        print(player)
    # Foods = [
    # Cooked Chicken Cuts
    # None
    # Cooked Chicken Cuts
    # Cooked Chicken Cuts
    # ]
    # Balances = [
    # 97.46341463414635
    # 14
    # 55.12
    # 52.62718158187894
    # ]
    # Caves = [
    # (<Cave: Boulderfall Cave. 10 of [Prismarine Crystal: 11.48🍗/💎]>, 8.710801393728223)
    # None
    # (<Cave: Castle Karstaag Ruins. 4 of [Netherite Ingot: 20.95🍗/💎]>, 4)
    # (<Cave: Orotheim. 6 of [Fishing Rod: 26.93🍗/💎]>, 3.7133308577794284)
    # ]
