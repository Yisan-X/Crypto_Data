from copy import deepcopy

def nested_set(dct, keys, value):
    for k in keys[:-1]:
        dct = dct.setdefault(k, {})
    dct[keys[-1]] = value
    
def nested_get(dct, keys, value = None):
    obj = deepcopy(dct)
    for k in keys:
        obj = obj.get(k)
        if obj is None:
            return value
    return obj