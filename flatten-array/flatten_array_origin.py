import collections

def flatten(iterable):
    return list(iterate_elements(iterable))

def iterate_elements(item):
    if item is None:
        return
    if is_list_like(item):
        for sub_item in item:
            yield from iterate_elements(sub_item)
    else:
        yield item

def is_list_like(item):
    try:
        iter(item)
        return not isinstance(item, str)
    except TypeError:
        return False
