def is_armstrong(number):
    return sum(int(x)**len(str(number)) for x in str(number)) == number
