def append(*lists):
    return [e for l in lists for e in l]


def concat(lists):
    return append(*lists)


def filter_clone(function, xs):
    return [e for e in xs if function(e)]


def length(xs):
    count = 0
    for _ in xs:
        count += 1
    return count

def map_clone(function, xs):
    return [function(e) for e in xs]


def foldl(function, xs, acc):
    result = acc
    for value in xs:
        result = function(result, value)
    return result


def foldr(function, xs, acc):
    return foldl(lambda x, y: function(y, x), reverse(xs), acc)


def reverse(xs):
    return [e for e in iterate_reverse(xs)]


def iterate_reverse(xs):
    i = -1
    while True:
        try:
            yield xs[i]
        except IndexError:
            break
        i -= 1
