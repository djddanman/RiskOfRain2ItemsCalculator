import matplotlib.pyplot as plt
import numpy as np
import PySimpleGUI as sg
import json
from pathlib import Path

_items_dict = dict()
data = dict()
values = list()


def calculate_stack_lambda(base_value, first_item, stack_effect, stack_type, limit=None):
    if not limit:
        limit = [0, float('inf')]

    if stack_type == 'linear':
        effect = lambda i: (np.array(i) < limit[1]) * (
                base_value + (np.array(i) > 0) * first_item + (np.array(i) > 1) * (
                stack_effect * (i - 1))) + (np.array(i) >= limit[1]) * limit[0]

    elif stack_type == 'hyperbolic':
        effect = lambda n: 1 - 1 / (stack_effect * n + 1)

    elif stack_type == 'exponential':
        effect = lambda n: 1 - (1 - stack_effect) ** n

    elif stack_type == 'bandolier':
        effect = lambda n: 1 - 1 / (1 + n) ** 0.33

    elif stack_type == 'key':
        common_rarity = lambda i: 80 / (80 + 20 * n + n ** 2) * 100
        uncommon_rarity = lambda i: n * 20 / (80 + 20 * n + n ** 2) * 100
        legendary_rarity = lambda i: n ** 2 / (80 + 20 * n + n ** 2) * 100
        effect = [common_rarity, uncommon_rarity, legendary_rarity]

    elif stack_type == 'genesis':
        effect = lambda n: base_value / (
                1 - (np.array(n) > 0) * (-1) + (np.array(n) > 0) * first_item + (np.array(n) > 1) * (
                stack_effect * (n - 1)))

    elif stack_type == 'corpsebloom':
        effect = lambda n: first_item * stack_effect ** (n - 1)

    return effect


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

    values = calculate_stack_lambda(item_effect['base_value'], item_effect['first_item'], item_effect['stack_effect'],
                                    item_effect['stack_type'],
                                    item_effect['limit'] if 'limit' in item_effect else None)

    if item == 'Rusted Key':
        plt.plot(n, values[0](n), 'k-', label='Common')
        plt.plot(n, values[1](n), 'g-', label='Uncommon')
        plt.plot(n, values[2](n), 'r-', label='Legendary')
        plt.legend()
        plt.axis([0, n[-1], 0, 100])

    else:
        plt.plot(n, values(n))
        # plt.axis([0, n[-1], 0, max(values)])

    plt.xlabel('Stack Size')
    plt.ylabel(item_effect['effect'])
    plt.title(item)

    plt.show(block=True)

# TODO Finish adding Lunar items
# TODO End program or go to menu on plot close
