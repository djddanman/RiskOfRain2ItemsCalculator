class Item:
    def __init__(self, name, limit=None, proc=False):
        self.name = name
        #self.rarity = rarity

    def __str__(self):
        return '{}'.format(self.name)

# class Effect:
#     def __init__(self, effect, base_value, first_item, stack_effect, stack_type, limit=None, proc=False):
#         self.effect = effect
#         self.base_value = base_value
#         self.first_item = first_item
#         self.stack_effect = stack_effect
#         self.stack_type = stack_type
#         self.limit = limit
#         self.proc = proc
