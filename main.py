import matplotlib.pyplot as plt
import numpy as np
import PySimpleGUI as sg
import json
from pathlib import Path

_items_dict = dict()
data = dict()

values = list()


def calculate_stack(base_value, first_item, stack_effect, stack_type, n, limit=None):
    value = int()

    if stack_type == 'linear':
        value = base_value + (first_item if n > 0 else 0) + (stack_effect * (n - 1) if n > 1 else 0)
        if limit and value > limit:
            return limit

    elif stack_type == 'hyperbolic':
        value = 1 - 1 / (stack_effect * n + 1)

    elif stack_type == 'exponential':
        value = 1 - (1 - stack_effect) ** n

    elif stack_type == 'bandolier':
        value = 1 - 1 / (1 + n) ** 0.33

    elif stack_type == 'key':
        net_rarity = 80 + 20 * n + n ** 2
        common_rarity = 80 / net_rarity
        uncommon_rarity = n * 20 / net_rarity
        legendary_rarity = n ** 2 / net_rarity
        value = [common_rarity, uncommon_rarity, legendary_rarity]

    return value


def get_items_dict():
    global _items_dict
    global data

    if _items_dict:
        return _items_dict

    with open(Path(__file__).absolute().parent / 'items.json', 'r') as file:
        data = json.load(file)

    return data


def select_item_gui(items_dict):
    select_item_list = list()
    for rarity in items_dict:
        for item in items_dict[rarity]:
            select_item_list.append(item)

    layout = [[sg.Combo(select_item_list, size=[30, 1], default_value=select_item_list[0]),
               sg.OK()]]

    window = sg.Window('Select Item', layout)
    event, values = window.read()
    window.close()

    item = values[0]

    rarity = ''
    for r in items_dict:
        if item in items_dict[r]:
            rarity = r
            break

    select_effect_list = list()
    for effect in items_dict[rarity][item]:
        select_effect_list.append(effect)

    layout = [[sg.Combo(select_effect_list, size=[30, 1], default_value=select_effect_list[0]),
               sg.OK()]]

    window = sg.Window('Select Effect', layout)
    event, values = window.read()
    window.close()

    effect = values[0]

    return item, rarity, effect


if __name__ == '__main__':
    items_dict = get_items_dict()

    item, rarity, effect = select_item_gui(items_dict)
    item_effect = items_dict[rarity][item][effect]

    upper_bound = item_effect['limit'][1] + 2 if 'limit' in item_effect else 26

    n = np.arange(0, upper_bound, 1)
    stack_type = item_effect['stack_type']

    for i in n:
        value = calculate_stack(item_effect['base_value'], item_effect['first_item'], item_effect['stack_effect'],
                                item_effect['stack_type'], i,
                                item_effect['limit'][0] if 'limit' in item_effect else None)
        if item == 'Rusted Key':
            value = [x * 2 for x in value]
        elif '%' in item_effect['effect']:
            value = value * 100
        values.append(value)

    if item == 'Rusted Key':
        plt.plot(n, [i[0] for i in values], label ='Common')
        plt.plot(n, [i[1] for i in values], label='Uncommon')
        plt.plot(n, [i[2] for i in values], label='Legendary')
        plt.legend()

    else:
        plt.plot(n, values, label=['Common', 'Uncommon', 'Legendary'] if item == 'Rusted Key' else None)

    plt.xlabel('Stack Size')
    plt.ylabel(item_effect['effect'])
    plt.title(item)

    plt.show()
