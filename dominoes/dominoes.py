from collections import namedtuple, defaultdict
from itertools import permutations

Domino = namedtuple('Domino', ['left', 'right'])


class DominoChain:
    def __init__(self, chain=None):
        self.values = [] if chain is None else chain

    def clear(self):
        self.values = []

    def copy(chain):
        return DominoChain(chain=chain.values)

    def meta_domino(self):
        return Domino(self.left, self.right)

    def is_cycle(self):
        return (self.values) and (self.left == self.right)

    @property
    def left(self):
        return self.values[0]

    @property
    def right(self):
        return self.values[-1]

    def attach(self, dominos):
        for domino in dominos:
            self.attach_one(domino)

    def attach_one(self, domino, left_first=True):
        if left_first:
            attached = self.attach_first(domino) or self.attach_left(domino) or self.attach_right(domino)
        else:
            attached = self.attach_first(domino) or self.attach_right(domino) or self.attach_left(domino)

        if not attached:
            raise ValueError("Domino {} can't be attached to {}".format(domino, self))

    def attach_first(self, domino):
        if len(self.values) == 0:
            self.values = [domino.left, domino.right]
            return True
        return False

    def attach_right(self, domino):
        if domino.right == self.left:
            self.values = [domino.right, domino.left] + self.values
            return True
        return False

    def attach_left(self, domino):
        if domino.left == self.right:
            self.values += [domino.left, domino.right]
            return True
        return False

    def __repr__(self):
        return "".join("[{} {}]".format(*domino) for domino in self)

    def __iter__(self):
        for i in range(0, len(self.values), 2):
            yield Domino(self.values[i], self.values[i+1])

def chain_brute_force(dominoes):
    initial_chain = DominoChain()
    initial_chain.attach(dominoes[0])

    domino_labels = defaultdict(list)
    for domino in dominoes:
        domino_labels[domino.left] = domino
        domino_labels[domino.right] = domino

    domino_chains = [initial_chain]
    while domino_chains:
        domino_chain = domino_chains.pop()
        left_value = domino_chain.left()
        right_value = domino_chain.right()
        for domino in domino_labels[left_value]+domino_labels[right_value]:
            new_chain = domino_chain.copy()
            new_chain.attach(domino)
            domino_chains.append(object)
        try:
            domino_chain.clear()
            domino_chain.attach(sorted_dominoes)
        if domino_chain.is_cycle():
            print("Found a domino chain with {} try.".format(nb_try))
            return domino_chain
        except ValueError:
            continue
    raise ValueError("Can't create a chain with these dominos.")


def chain(dominoes):
    return chain_brute_force(dominoes)

input_dominoes = [(1, 2), (2, 3), (3, 1), (2, 4), (2, 4)]
output_chain = chain([Domino(*d) for d in input_dominoes])
print(output_chain)
# d1 = Domino(1,2)
# d2 = Domino(2,3)
# d3 = Domino(3,1)
# c = DominoChain()
# c.attach(d1,d2,d3)
# print(c)

# from collections import defaultdict, Counter
#
# class DominoNode:
#     current_id = 0
#
#     def __init__(self, value_a, value_b):
#         self.node_id = DominoNode.current_id
#         self.left_value = value_a
#         self.right_value = value_b
#         self.left_connector = set()
#         self.right_connector = set()
#         DominoNode.current_id += 1
#
#     def find_connector(self, value):
#         if self.left_value == value:
#             return self.left_connector
#         if self.right_value == value:
#             return self.right_connector
#         raise ValueError("No connector for this value.")
#
#     def connect_to(self, other_domino_node):
#         for value in (other_domino_node.left_value, other_domino_node.right_value):
#             try:
#                 connector = self.find_connector(value)
#                 connector.add(other_domino_node)
#             except ValueError:
#                 continue
#
#     def degree(self):
#         return len(self.left_connector)+len(self.right_connector)
#
#     def __repr__(self):
#         left_nodes_id = [node.node_id for node in self.left_connector]
#         right_nodes_id = [node.node_id for node in self.right_connector]
#         return "Node {}, left:{}, right:{}".format((self.left_value, self.right_value), left_nodes_id, right_nodes_id)
#
# class DominoGraph:
#     def __init__(self, dominoes):
#         self.number_of_nodes = 0
#         self.node_labels = defaultdict(list)
#         for domino in dominoes:
#             self.insert_domino(domino)
#
#     def insert_domino(self, domino):
#         x, y = domino
#         domino_node = DominoNode(x, y)
#
#         for other_node in self.node_labels[x]:
#             self.connect(domino_node, other_node)
#         for other_node in self.node_labels[y]:
#             self.connect(domino_node, other_node)
#
#         self.node_labels[x].append(domino_node)
#         self.node_labels[y].append(domino_node)
#
#     def connect(self, domino_node_A, domino_node_B):
#         domino_node_A.connect_to(domino_node_B)
#         domino_node_B.connect_to(domino_node_A)
#
#     def path_repr(self, path):
#         #for node_id in path:
#         pass
#
#     def fleury(self):
#         current_node =
#
#
#     def __repr__(self):
#         return str([(label,str(node)) for label, node in self.node_labels.items()])
#
#
# def chain(dominoes):
#     G = DominoGraph(dominoes)
#     print(G)
#     print(G.fleury())
#
#
#
# input_dominoes = [(1, 2), (3, 1), (2, 3)]
# output_chain = chain(input_dominoes)
# print()
