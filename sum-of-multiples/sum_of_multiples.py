def sum_of_multiples(limit, divisors):
    return sum({m for d in divisors for m in multiples_of(limit, d)})


def multiples_of(limit, x):
    return [x*i for i in range(1, 1+(limit-1)//x)]
