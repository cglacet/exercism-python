def collatz_steps(number):
    if number <= 0:
        raise ValueError("We need a positive integer here.")
    return run_collatz_steps(number, 0)

def run_collatz_steps(number, time):
    if number == 1:
        return time
    if number%2 == 0:
        number //= 2
    else:
        number = number*3+1
    return run_collatz_steps(number, time+1)
