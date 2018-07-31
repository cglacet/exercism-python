from collections import Counter

class Garden(object):

    PLANTS = ["Grass", "Clover", "Radishes", "Violets"]
    PLANTS_NAMES = { name[0]:name for name in PLANTS }
    DEFAULT_CHILDREN_NAMES = [ "Alice", "Bob", "Charlie", "David", "Eve", "Fred", "Ginny", "Harriet", "Ileana", "Joseph", "Kincaid", "Larry"]
    NB_PLANTS_PER_CHILD = 2

    def __init__(self, diagram, students=None):
        if students is not None:
            self.students = sorted(students)
        else:
            self.students = Garden.DEFAULT_CHILDREN_NAMES
        self.childrens_plants = { child_name:[] for child_name in self.students }
        for child_name, plants_shortnames in self.retrieve_childrens_plants(diagram):
            plants_names = [ Garden.PLANTS_NAMES[p] for p in plants_shortnames ]
            childs_collection = self.childrens_plants[child_name]
            childs_collection += plants_names

    def plants(self, child_name):
        return self.childrens_plants[child_name]

    def retrieve_childrens_plants(self, diagram):
        plant_lines = Garden.retrieve_plant_line(diagram)
        for plant_line in plant_lines:
            childrens_plants = self.retrieve_childrens_plants_in_line(plant_line)
            yield from childrens_plants

    def retrieve_plant_line(diagram):
        return diagram.split("\n")

    def retrieve_childrens_plants_in_line(self, plant_line):
        split_line = zip(*[iter(plant_line)]*Garden.NB_PLANTS_PER_CHILD)
        return zip(self.students, split_line)

def flatten_list(list):
    return [ elem for sub_list in list for elem in sub_list  ]

garden = Garden("VVRCGG\nVVCCGG")
print([ p for p in garden.plants("Bob") ])
