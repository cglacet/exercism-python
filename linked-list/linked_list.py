""" This is an exercise from https://exercism.io/my/tracks/python """


class Node:
    """Each node also holds a link to the previous node."""
    def __init__(self, value, succeeding=None, previous=None):
        self.value = value
        self.succeeding = succeeding
        self.previous = previous

    def __repr__(self):
        return str(self.value)


class LinkedList:
    """A linked list is a collection of data elements called nodes.
    In a doubly linked list each node also holds a link to the previous node"""
    def __init__(self):
        self.head = None
        self.tail = self.head

    def push(self, value):
        self.tail.previous = Node(value, previous=self.tail.previous, succeeding=None)

    def unshift(self, value):
        succeeding = self.head
        self.head = Node(value, succeeding=succeeding)
        succeeding.previous = self.head

    def pop(self):
        value, self.tail = self.tail.value, self.tail.previous
        if self.tail is not None:
            self.tail.succeeding = None
        return value

    def shift(self):
        value, self.head = self.head.value, self.head.succeeding
        if self.head is not None:
            self.head.succeeding = None
        return value

    def __iter__(self):
        node = self.head
        while node.succeeding is not None:
            node = node.succeeding
            yield node

    def __repr__(self):
        items = ', '.join(str(n) for n in self)
        return f"[{items}]"


ll = LinkedList()
ll.push(2)
print(ll)
print(ll.head, ll.tail)
ll.push(3)
print(ll)
print(ll.head, ll.tail)
a = ll.pop()
print(ll)
print(a)
ll.unshift(1)
print(ll)
b = ll.shift()
print(ll)
print(b)
