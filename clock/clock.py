"""This is an exercise from https://exercism.io/my/tracks/python."""


class Clock:
    """A 24-hours format clock."""
    def __init__(self: 'Clock', hour: int, minute: int) -> None:
        self.hour = (hour + minute//60) % 24
        self.minute = minute % 60

    def __repr__(self) -> str:
        return "{:02d}:{:02d}".format(self.hour, self.minute)

    def __eq__(self: 'Clock', other: object) -> bool:
        try:
            return self.hour == other.hour and self.minute == other.minute
        except AttributeError:
            raise NotImplementedError("Clock doesn't support comparison with {}".format(type(other)))

    def __add__(self: 'Clock', minutes: int) -> 'Clock':
        return Clock(self.hour, self.minute + minutes)

    def __sub__(self: 'Clock', minutes: int) -> 'Clock':
        return self.__add__(-minutes)
