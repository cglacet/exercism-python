import random
from string import ascii_uppercase

ALPHABET_SIZE = len(ascii_uppercase)

class Robot(object):
    names_used = set()

    def __init__(self):
        self.boot()

    def boot(self):
        name = Robot.rand_name()
        while name in Robot.names_used:
            name = Robot.rand_name()
        Robot.names_used.add(name)
        self.name = name
        self.on = True

    def shutdown(self):
        self.on = False

    def reset(self):
        self.shutdown()
        self.boot()

    def rand_name():
        return rand_letters(2)+rand_digits(3)

def rand_digits(nb_digits):
    return ''.join([ str(random.randint(0,9)) for _ in range(nb_digits) ])

def rand_letters(nb_letters):
    return ''.join([ ascii_uppercase[random.randint(0,ALPHABET_SIZE-1)] for _ in range(nb_letters) ])
