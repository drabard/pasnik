#!/usr/bin/env python3

import json
import re
from math import ceil

from pprint import pprint
from sys import argv

data = ''
with open(argv[1], 'r') as f:
    data = f.read()

meals_list = json.loads(data)
nmeals = 0.0
for meal in meals_list:
    if "weight" in meal:
        nmeals += float(meal["weight"])
    else:
        nmeals += 1.0

ingredients = {}
for meal in meals_list:
    for ingredient in meal["ingredients"]:
        name = ingredient["name"]
        quantity = ingredient["quantity"]
        weight = 1.0
        if "weight" in meal:
            weight = float(meal["weight"])
        if name not in ingredients:
            ingredients[name] = []
        ingredients[name].append((quantity, weight))

nplanned_meals = float(input("How many meals?\n"))
meal_weight = nplanned_meals/nmeals;

shoplist = {}
re_prog = re.compile('([0-9\.]+)\s*(.*)')
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
        total_amount = amount * meal_weight
        shoplist[ingredient].append((unit, total_amount))

for ingredient, units in shoplist.items():
    print("{}:".format(ingredient))
    for unit in units:
        print("\t{}\t{}".format(ceil(unit[1]), unit[0]))