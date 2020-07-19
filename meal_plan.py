#!/usr/bin/env python3

import json
import re
from pprint import pprint
from sys import argv

data = ''
with open(argv[1], 'r') as f:
    data = f.read()

meals = json.loads(data)
nmeals = len(meals)

ingredients = {}
for meal in meals:
    for ingredient in meal["ingredients"]:
        name = ingredient["name"]
        quantity = ingredient["quantity"]
        if name not in ingredients:
            ingredients[name] = []
        ingredients[name].append(quantity)

# shoplist = {}
# for ingredient in ingredients:
    

pprint(ingredients)