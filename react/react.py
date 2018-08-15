from abc import ABCMeta


class Observable(metaclass=ABCMeta):
    """Classes that inherit that abstract class will be able to handle callbacks
    registration/removal. Listeners can be warned of any change by calling `Observable.has_changed`."""
    def __init__(self):
        self.callbacks = set()
        self.all_notified_callbacks = set()

    def has_changed(self):
        for callback in self.callbacks:
            callback(self)
        for callback in self.all_notified_callbacks:
            callback()

    def add_callback(self, callback):
        self.callbacks.add(callback)
    on_change = add_callback

    def remove_callback(self, listener_id):
        try:
            self.callbacks.remove(listener_id)
        except KeyError as key_e:
            ValueError("You aren't a subscriber of this cell:", key_e)

    def add_all_notified_callback(self, callback):
        self.all_notified_callbacks.add(callback)


class Cell(Observable):
    """A cell is more or less an observable `int`."""
    def __init__(self, initial_value):
        self._value = initial_value
        super().__init__()

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        self._value = new_value

    def __repr__(self):
        return str(self.value)

    @staticmethod
    def _get_value(other):
        if isinstance(other, Cell):
            return other.value
        return other

    def __eq__(self, other):
        return self.value == self._get_value(other)

    def __hash__(self):
        return self.value

    def __lt__(self, other):
        return self.value < self._get_value(other)

    def __add__(self, other):
        return self.value + self._get_value(other)

    def __sub__(self, other):
        return self.value - self._get_value(other)

    def __mul__(self, other):
        return self.value * self._get_value(other)

    __rsub__ = __sub__
    __radd__ = __add__
    __rmul__ = __mul__


def observed(method):
    def decorated_method(self, *args, **kwargs):
        old_value = getattr(self, method.__name__)
        result = method(self, *args, **kwargs)
        new_value = getattr(self, method.__name__)
        if old_value != new_value:
            print("Notify all {} -> {}".format(old_value, new_value))
            self.has_changed()
        return result
    return decorated_method


class InputCell(Cell):
    @property
    def value(self):
        return self._value

    @value.setter
    @observed
    def value(self, new_value):
        self._value = new_value

class ComputeCell(Cell):
    def __init__(self, inputs, compute_function, name="cell"):
        super().__init__(compute_function(inputs))
        self.compute_function = compute_function
        self.inputs = inputs
        self.name = name
        self.old_value = self.value
        for input_cell in inputs:
            input_cell.add_callback(self.update_value)
            input_cell.add_all_notified_callback(self.on_computation_done)

    def on_computation_done(self):
        if self.value != self.old_value:
            self.old_value = self.value
            self.has_changed()

    def update_value(self, cell):
        self.value = self.compute_function(self.inputs)

    def __repr__(self):
        return "{}={}".format(self.name, super().__repr__())
