from collections import OrderedDict

def sorted_dict(input):
    # Returns a dictionary sorted by keys.
    return OrderedDict(sorted(input.items()))