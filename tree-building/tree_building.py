from collections import defaultdict

class Record():
    def __init__(self, record_id, parent_id):
        if record_id == 0 and parent_id != 0:
            raise ValueError("First record should have it self as parent.")
        if record_id != 0 and parent_id >= record_id:
            raise ValueError("Record {} can't have {} as parent (parent ID >= record ID).".format(record_id, parent_id))
        self.record_id = record_id
        self.parent_id = parent_id

class Node():
    def __init__(self, node_id):
        self.node_id = node_id
        self.children = []

    def add_child(self, node):
        self.children.append(node)

def BuildTree(records):
    if not records:
        return None

    records.sort(key=lambda r: r.record_id)
    records_ids = [record.record_id for record in records]

    max_id = records_ids[-1]
    min_id = records_ids[0]
    if max_id != len(records_ids) - 1 or min_id != 0:
        error_message = "Record IDs should go from {} to {} not from {} to {}"
        raise ValueError(error_message.format(0, len(records_ids) - 1, min_id, max_id))

    nodes = {i: Node(i) for i in records_ids}
    for record in records[1:]:
        nodes[record.parent_id].add_child(nodes[record.record_id])

    return nodes[0]
