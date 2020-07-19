#!/usr/bin/env python3

"""
Generates a shopping list from a JSON file with recipes.
"""

import json
import re

from math import ceil
from sys import argv


def read_recipes_from_file(path):
    """
    Reads recipes from file and returns them as
    a list.
    Each recipe is a dictionary with the following fields:
        name - name of the meal.
        weight - optional, how frequently given recipe is going to be used
            with relation to the other recipes.
        ingredients - list of dictionaries, one for each ingredient.
            name
            quantity
    """

    with open(path, 'r') as infile:
        return json.loads(infile.read())


def count_available_recipes(recipes):
    """
    Returns a weighted count of recipes.
    """

    result = 0.0
    for recipe in recipes:
        if "weight" in recipe:
            result += float(recipe["weight"])
        else:
            result += 1.0
    return result


def gather_ingredients(recipes):
    """
    Gathers ingredients from a list of recipes and groups their quantities
    together.
    Result is a dictionary in form:
        ingredient name -> [(quantity, weight)...]
    Weight is the weight of corresponding meal.
    """

    ingredients = {}
    for recipe in recipes:
        for ingredient in recipe["ingredients"]:
            name = ingredient["name"]
            quantity = ingredient["quantity"]
            weight = 1.0
            if "weight" in recipe:
                weight = float(recipe["weight"])
            if name not in ingredients:
                ingredients[name] = []
            ingredients[name].append((quantity, weight))
    return ingredients


def create_shoplist(ingredients, recipes_count, meals_count):
    """
    Returns the shopping list based on given list of ingredients,
    number of recipes they come from and number of meals they're supposed to
    cover.
    """

    shoplist = {}
    re_prog = re.compile(r'([0-9\.]+)\s*(.*)')
    for ingredient, quantities in ingredients.items():
        units = {}
        for quantity_info in quantities:
            quantity = quantity_info[0]
            weight = quantity_info[1]
            groups = re_prog.match(quantity).groups()
            amount = float(groups[0])
            unit = groups[1]
            if unit not in units:
                units[unit] = 0.0
            units[unit] += amount * weight
        shoplist[ingredient] = []
        for unit, amount in units.items():
            total_amount = amount * (meals_count / recipes_count)
            shoplist[ingredient].append((unit, total_amount))
    return shoplist


def print_shoplist(shoplist):
    """
    Prints a shoplist in human-friendly format.
    """

    for ingredient, units in shoplist.items():
        print("{}:".format(ingredient))
        for unit in units:
            print("\t{}\t{}".format(ceil(unit[1]), unit[0]))


def main():
    """
    Prints shopping list based on list of recipes provided
    as first argument to the script.
    """

    recipes = read_recipes_from_file(argv[1])
    recipes_count = count_available_recipes(recipes)
    ingredients = gather_ingredients(recipes)

    meals_count = float(input("How many meals?\n"))

    shoplist = create_shoplist(ingredients, recipes_count, meals_count)

    print_shoplist(shoplist)


if __name__ == '__main__':
    main()
