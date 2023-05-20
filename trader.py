from __future__ import annotations
from abc import abstractmethod, ABC
from material import Material
from random_gen import RandomGen
from avl import AVLTree
from heap import MaxHeapMats

__author__ = "Code by Daniel Liu, Ben Abraham, Johnny Ta, Bangze Han"

# Generated with https://www.namegenerator.co/real-names/english-name-generator
TRADER_NAMES = [
    "Pierce Hodge",
    "Loren Calhoun",
    "Janie Meyers",
    "Ivey Hudson",
    "Rae Vincent",
    "Bertie Combs",
    "Brooks Mclaughlin",
    "Lea Carpenter",
    "Charlie Kidd",
    "Emil Huffman",
    "Letitia Roach",
    "Roger Mathis",
    "Allie Graham",
    "Stanton Harrell",
    "Bert Shepherd",
    "Orson Hoover",
    "Lyle Randall",
    "Jo Gillespie",
    "Audie Burnett",
    "Curtis Dougherty",
    "Bernard Frost",
    "Jeffie Hensley",
    "Rene Shea",
    "Milo Chaney",
    "Buck Pierce",
    "Drew Flynn",
    "Ruby Cameron",
    "Collie Flowers",
    "Waldo Morgan",
    "Winston York",
    "Dollie Dickson",
    "Etha Morse",
    "Dana Rowland",
    "Eda Ryan",
    "Audrey Cobb",
    "Madison Fitzpatrick",
    "Gardner Pearson",
    "Effie Sheppard",
    "Katherine Mercer",
    "Dorsey Hansen",
    "Taylor Blackburn",
    "Mable Hodge",
    "Winnie French",
    "Troy Bartlett",
    "Maye Cummings",
    "Charley Hayes",
    "Berta White",
    "Ivey Mclean",
    "Joanna Ford",
    "Florence Cooley",
    "Vivian Stephens",
    "Callie Barron",
    "Tina Middleton",
    "Linda Glenn",
    "Loren Mcdaniel",
    "Ruby Goodman",
    "Ray Dodson",
    "Jo Bass",
    "Cora Kramer",
    "Taylor Schultz",
]


class Trader(ABC):

    def __init__(self, name: str) -> None:
        """
        
        This is the constructor magic method for the Trader Class, initializing a Trader Object

        Parameters:
            name (str): A string representing the name of the Trader
        """

        self.name = name
        self.materials = None
        self.trader_type = None
        self.deal = None

    def get_trader_type(self):
        """
        Returns the Trader's type
        :complexity: O(1)
        
        """
        return self.trader_type

    @classmethod
    def random_trader(cls):
        pass

    @abstractmethod
    def set_all_materials(self, mats: list[Material]) -> None:
        pass

    @abstractmethod
    def add_material(self, mat: Material) -> None:
        pass

    def is_currently_selling(self) -> bool:
        """
        Checks if the Trader has a current deal
        :complexity: O(1)
        
        """
        if self.deal:
            return True
        return False

    def current_deal(self) -> tuple[Material, float]:
        """
        Returns the Trader's current deal
        :complexity: O(1)
        
        """
        if self.deal:
            return self.deal
        else:
            raise ValueError('No deal found')

    @abstractmethod
    def generate_deal(self) -> None:
        pass

    def stop_deal(self) -> None:
        """
        Resets the Trader's deal to None
        :complexity: O(1)
        
        """
        self.deal = None

    def __str__(self) -> str:
        try:
            return f"<{self.trader_type}: {self.name} buying [{self.deal[0]}🍗/💎] for {self.deal[1]}💰>"
        except:
            return f"<{self.trader_type}: {self.name}>"


class RandomTrader(Trader):
    def __init__(self, name: str = None):
        """
        
        This is the constructor magic method for the HardTrader Class, initializing a RandomTrader Object

        Parameters:
            name (str): A string representing the name of the RandomTrader
        """
        Trader.__init__(self, name)
        self.trader_type = 'RandomTrader'
        # Using lists
        self.materials = []

    @classmethod
    def random_trader(cls):
        """
        Generate a random trader in RandomTrader class.
        :complexity: O(1)
        """
        # Generate random trader based on RandomTrader
        name_of_trade = TRADER_NAMES[RandomGen.randint(0, len(TRADER_NAMES) - 1)]
        trader_to_return = RandomTrader(name_of_trade)
        return trader_to_return

    def set_all_materials(self, mats: list[Material]) -> None:
        """
        Add a list of materials to the RandomTrader.
        :complexity: O(1)
        """
        self.materials = mats

    def add_material(self, mat: Material) -> None:
        """
        Add a material to the self.materials list
        :complexity: O(1)
        """
        self.materials.append(mat)

    def generate_deal(self) -> None:
        """
        Generates a deal for the RandomTrader
        :complexity: O(1)
        """
        material_for_deal = self.materials[RandomGen.randint(0, len(self.materials) - 1)]
        buy_price = round(2 + 8 * RandomGen.random_float(), 2)
        self.deal = (material_for_deal, buy_price)


class RangeTrader(Trader):
    """


    
    {Inherits all instance attributes from Parent Class: Game}


    """
    def __init__(self, name: str = None):
        """
        
        This is the constructor magic method for the RangeTrader Class, initializing a RangeTrader Object

        Parameters:
            name (str): A string representing the name of the RangeTrader
        """
        Trader.__init__(self, name)
        self.trader_type = 'RangeTrader'
        self.materials = AVLTree()

    @classmethod
    def random_trader(cls):
        """
        Generate a random trader in RangeTrader class.
        """
        name_of_trade = TRADER_NAMES[RandomGen.randint(0, len(TRADER_NAMES) - 1)]
        trader_to_return = RangeTrader(name_of_trade)
        return trader_to_return

    def set_all_materials(self, mats: list[Material]) -> None:
        """
        Add a list of materials to the HardTrader.
        :complexity: O(log n) where n is the number of nodes in the AVLTree
        """
        # Adding all materials into the tree
        tree = AVLTree()
        for mat in mats:
            tree[mat.mining_rate] = mat
        self.materials = tree

    def add_material(self, mat: Material) -> None:
        """
        Add a material to the AVLTree.
        :complexity: O(log n) where n is the number of nodes in the AVLTree
        """
        self.materials[mat.mining_rate] = mat

    def generate_deal(self) -> None:
        """
        Generate a deal based on random integers i and j.
        These integers will create a sorted list of ith to jth easiest to mine materials.
        This is

        :complexity: O(j-i+log n) where n is the number of nodes in the AVLTree, j and i are the random integers.
        """
        # Generate random i,j integers
        i = RandomGen.randint(0, len(self.materials) - 1)
        j = RandomGen.randint(i, len(self.materials) - 1)

        # Generate materials in i,jth easiest range
        material_list = self.materials_between(i, j)
        material_for_deal = material_list[RandomGen.randint(0, len(material_list)-1)]
        buy_price = round(2 + 8 * RandomGen.random_float(), 2)
        self.deal = (material_for_deal, buy_price)

    def materials_between(self, i: int, j: int) -> list[Material]:
        """
        Generate materials between i and jth indices.
        Simply uses the range_between method in AVLTree, which has
        :complexity: O(j-i + log(n)), where n is the number of nodes in the tree
        """
        return self.materials.range_between(i,j)

class HardTrader(Trader):
    # For hard trader, use a max heap.
    def __init__(self, name: str = None):
        """
        
        This is the constructor magic method for the HardTrader Class, initializing a HardTrader Object

        Parameters:
            name (str): A string representing the name of the HardTrader
        """
        Trader.__init__(self, name)
        self.trader_type = 'HardTrader'
        self.materials = MaxHeapMats(1000)

    @classmethod
    def random_trader(cls):
        """
        Generates a random trader in HardTrader class.
        """
        name_of_trade = TRADER_NAMES[RandomGen.randint(0, len(TRADER_NAMES) - 1)]
        trader_to_return = HardTrader(name_of_trade)
        return trader_to_return

    def add_material(self, mat: Material) -> None:
        """
        Add a material to the materials heap.
        :complexity: O(log n), where n is the number of elems in the heap.
        """
        self.materials.add(mat)

    def set_all_materials(self, mats: list[Material]) -> None:
        """
        Add a list of materials to the HardTrader.
        Uses a bottom up heap construction

        Pre-Conditions (What must be true for method to be called):
            A list of materials must be passed through as the argument
        
        Post-Conditions (What is true after method is callled):
            self.material will be populated with the elements of the list

        :mats: list of materials to set
        :complexity: O(n), where n is the number of elems in the heap
        """
        self.materials.bottom_up(mats)

    def generate_deal(self) -> None:
        """
        Generates a deal for the HardTrader
        
        Pre-Conditions (What must be true for method to be called):
            self.materials must not be empty
        
        Post-Conditions (What is true after method is callled):
            self.deal is set to a tuple of the material and buy price

        :complexity: O(1)
        """
        material_for_deal = self.materials.get_max() # material at the top of the heap
        buy_price = round(2 + 8 * RandomGen.random_float(), 2) #deal price calculation
        self.deal = (material_for_deal, buy_price)


if __name__ == "__main__":
    trader = HardTrader("Jackson")
    # print(trader)
    trader.set_all_materials([
        Material("Coal", 4.5),
        Material("Diamonds", 3),
        Material("Redstone", 20),
    ])
    trader.generate_deal()
    print(trader)
    trader.generate_deal()
    print(trader)
    trader.generate_deal()
    print(trader)
    trader.stop_deal()
    print(trader)
