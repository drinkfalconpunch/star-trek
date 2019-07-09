from collections import OrderedDict

def sorted_dict(input):
    # Returns a dictionary sorted by keys.
    return OrderedDict(sorted(input.items()))

def dict_search(d, value):
    if not isinstance(d, dict):
        raise ValueError('dict_search requires dictionary')

    pass