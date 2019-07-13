from collections import OrderedDict
from itertools import tee

def sorted_dict(input):
    # Returns a dictionary sorted by keys.
    return OrderedDict(sorted(input.items()))

def dict_search(d, value):
    if not isinstance(d, dict):
        raise ValueError('dict_search requires dictionary')

    pass

def pairwise(iterable):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)