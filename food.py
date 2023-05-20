from __future__ import annotations
"""

This file demonstrates the implementation of the Food Class

October 2022
"""

__author__ = "Code by Daniel Liu, Ben Abraham, Johnny Ta, Bangze Han"

from material import Material
from random_gen import RandomGen

# List of food names from https://github.com/vectorwing/FarmersDelight/tree/1.18.2/src/main/resources/assets/farmersdelight/textures/item
FOOD_NAMES = [
    "Apple Cider",
    "Apple Pie",
    "Apple Pie Slice",
    "Bacon",
    "Bacon And Eggs",
    "Bacon Sandwich",
    "Baked Cod Stew",
    "Barbecue Stick",
    "Beef Patty",
    "Beef Stew",
    "Cabbage",
    "Cabbage Leaf",
    "Cabbage Rolls",
    "Cabbage Seeds",
    "Cake Slice",
    "Chicken Cuts",
    "Chicken Sandwich",
    "Chicken Soup",
    "Chocolate Pie",
    "Chocolate Pie Slice",
    "Cod Slice",
    "Cooked Bacon",
    "Cooked Chicken Cuts",
    "Cooked Cod Slice",
    "Cooked Mutton Chops",
    "Cooked Rice",
    "Cooked Salmon Slice",
    "Dog Food",
    "Dumplings",
    "Egg Sandwich",
    "Fish Stew",
    "Fried Egg",
    "Fried Rice",
    "Fruit Salad",
    "Grilled Salmon",
    "Ham",
    "Hamburger",
    "Honey Cookie",
    "Honey Glazed Ham",
    "Honey Glazed Ham Block",
    "Horse Feed",
    "Hot Cocoa",
    "Melon Juice",
    "Melon Popsicle",
    "Milk Bottle",
    "Minced Beef",
    "Mixed Salad",
    "Mutton Chops",
    "Mutton Wrap",
    "Nether Salad",
    "Noodle Soup",
    "Onion",
    "Pasta With Meatballs",
    "Pasta With Mutton Chop",
    "Pie Crust",
    "Pumpkin Pie Slice",
    "Pumpkin Slice",
    "Pumpkin Soup",
    "Ratatouille",
    "Raw Pasta",
    "Rice",
    "Rice Panicle",
    "Roast Chicken",
    "Roast Chicken Block",
    "Roasted Mutton Chops",
    "Rotten Tomato",
    "Salmon Slice",
    "Shepherds Pie",
    "Shepherds Pie Block",
    "Smoked Ham",
    "Squid Ink Pasta",
    "Steak And Potatoes",
    "Stuffed Potato",
    "Stuffed Pumpkin",
    "Stuffed Pumpkin Block",
    "Sweet Berry Cheesecake",
    "Sweet Berry Cheesecake Slice",
    "Sweet Berry Cookie",
    "Tomato",
    "Tomato Sauce",
    "Tomato Seeds",
    "Vegetable Noodles",
    "Vegetable Soup",
]

class Food:
    """
    
    The class representing the Minecraft Game Food Object, facilitates the functionality of a Minecraft food object

    Instance Attributes:
        name (str): A string representing the name of the Food Object
        hunger_bars (int): An integer representing the number of hunger bars the Food provides the eater
        price (int): An integer that represents the price of purchasing the food
    """

    def __init__(self, name: str, hunger_bars: int, price: int) -> None:
        """
        
        The constructor method for the Food Class, initialising an instantiation of the Food Class Object

        Parameters:
            name (str): A string representing the name of the Food Object
            hunger_bars (int): An integer representing the number of hunger bars the Food provides the eater
            price (int): An integer that represents the price of purchasing the food
        """

        # Assigning the relevant paramaters to their respective instance attributes
        self.name = name
        self.hunger_bars = hunger_bars
        self.price = price
            
    def __str__(self) -> str:
        """
        
        The string Magic Method that returns the string representation of the Food Class

        Returns:
            A String representing the string representation of the Food Class Object

        Pre-Conditions (What must be true for method to be called):
            A string representation of the Object must have been called for
        
        Post-Conditions (What is true after method is callled):
            The string representation of the object has been returned
        
        Complexity:
            O(1)
        
        """

        return f"{self.name} {self.hunger_bars} {self.price}"

    @classmethod
    def random_food(cls) -> Food:
        """
        
        A Class method that returns a random Food Object

        Returns:
            A random Food Object
        
        Post-Conditions (What is true after method is callled):
            A random Food Object will be returned
        
        Complexity:
            O(1)
        """
        
        # name of food
        food_name = FOOD_NAMES[RandomGen.randint(0,len(FOOD_NAMES)-1)]
        # hunger_bars for food
        hunger_bars = RandomGen.randint(100,500)
        # price for food
        food_price = RandomGen.randint(10,40)

        return Food(food_name,hunger_bars,food_price)


if __name__ == "__main__":
    print(Food.random_food())
