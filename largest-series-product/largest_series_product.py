def largest_product(series, size):
    raise_if_non_valid(series, size)

    if size == 0:
        return 1

    series = int_list(series)

    current_digits_window = series[:size]
    max_product = prod(current_digits_window)
    for digit in series[size:]:
        current_digits_window.pop(0)
        current_digits_window.append(digit)
        max_product = max(max_product, prod(current_digits_window))
    return max_product

def int_list(series):
    return [ int(char) for char in series ]

def prod(series):
    product = 1
    for digit in series:
        product *= digit
    return product

def raise_if_non_valid(series, size):
    if size < 0:
        raise ValueError("Size needs to be positive.")
    if size > len(series):
        raise ValueError("Size needs to be smaller than the series lenght.")
