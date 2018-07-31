def sum_of_multiples(limit, multiples):
    multiples_found = set()
    for multiple in multiples:
        for i in range(1, 1+(limit-1)//multiple):
            multiples_found.add(multiple*i)
    return sum(multiples_found)
