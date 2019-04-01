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
    print(acc)
    result = acc
    for value in xs:
        acc = function(acc, value)
    return acc


def foldr(function, xs, acc):
    return foldl(lambda x, y: function(y, x), reverse(xs), acc)


def reverse(xs):
    return [e for e in iterate_reverse(xs)]


def iterate_reverse(xs):
    i = -1
    while True:
        try:
            yield xs[i]
            i -= 1
        except IndexError:
            return

a = [1,2,3,4]
other = [0]
print(foldl(lambda acc, v: acc+a, a, other))
print(other)
