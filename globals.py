import json
from pathlib import Path
from objects import item, survivor


_items_dict = dict()
_survivors_dict = dict()


def get_items_dict():
    if _items_dict:
        return _items_dict

    with open('items.json', 'r') as file:
        data = json.load(file)

        for rarity in data:
            for item_type in data[rarity]:
                _items_dict[item_type['name']] = item.Item(item_type['name'])

    return _items_dict


def get_survivors_dict():
    if _survivors_dict:
        return _survivors_dict()

    with open('survivors.json', 'r') as file:
        data = json.load(file)

        for survivor in data:
            _survivors_dict[survivor['name']] = survivor.Survivor(survivor['name'],
                                                                  survivor['health'],
                                                                  survivor['health_per_level'],
                                                                  survivor['regen'],
                                                                  survivor['regen_per_level'],
                                                                  survivor['damage'],
                                                                  survivor['damage_per_level'],
                                                                  survivor['speed'],
                                                                  survivor['armor'])

    return _survivors_dict
