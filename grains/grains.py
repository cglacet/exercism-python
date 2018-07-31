BOARD_SIZE = 64

def raise_if_out_bounds(function):
    def decorator(integer_number):
        if not (1 <= integer_number <= BOARD_SIZE):
            raise ValueError("No case here, you are out of the board bounds.")
        return function(integer_number)
    return decorator

@raise_if_out_bounds
def on_square(integer_number):
    return 2**(integer_number-1)

@raise_if_out_bounds
def total_after(integer_number):
    return 2**(integer_number)-1
