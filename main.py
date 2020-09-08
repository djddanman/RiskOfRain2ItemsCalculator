import matplotlib.pyplot as plt
import numpy as np
import PySimpleGUI as sg
import json, Item
from pathlib import Path

_items_dict = dict()

values = list()
AP_round = {"common": {"Armor-Piercing Rounds": {"property": "Damage to Bosses (Percent)", "base_value": 1, "first_item": 0.2, "stack_effect": 0.2, "stack_type": "linear"}}}
stun_grenade= {'common': {'Stun Grenade': {"property": "Chance to Stun", 'base_value': 0, "first_item": 0.05, "stack_effect": 0.05, "stack_type": "hyperbolic"}}}

def calculate_stack(base_value, first_item, stack_effect, stack_type, n):
    if stack_type == 'linear':
        value = base_value + (first_item if n > 0 else 0) + (stack_effect * (n - 1) if n > 1 else 0)
    elif stack_type == 'hyperbolic':
        value = 1 - 1 / (stack_effect * n + 1)
    elif stack_type == 'exponential':
        value = base_value * stack_effect ** n

    return value


def get_items_dict():
    global _items_dict

    if _items_dict:
        return _items_dict

    with open(Path(__file__).absolute().parent / 'items.json', 'r') as file:
        data = json.load(file)
        items = dict()

        for rarity in data:
            for item in data[rarity]:
                _items_dict[item] = Item()



#def select_item_gui():



if __name__ == '__main__':

    items_dict = get_items_dict()

    item = stun_grenade["common"]["Stun Grenade"]

    n = np.arange(0, 50, 1)
    stack_type = item['stack_type']
    for i in n:
        values.append(calculate_stack(item['base_value'], item['first_item'], item['stack_effect'], item['stack_type'], i))
    plt.plot(n, values)

    plt.show()
