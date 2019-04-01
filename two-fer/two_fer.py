"""This is an exercise from https://exercism.io/my/tracks/python."""


def two_fer(name: str = "you") -> str:
    """Returns 'One for X, one for me.' with X being either 'you' or the string
    provided as argument.
    """
    return f"One for {name}, one for me."
