class NodeNotFoundError(Exception):
    def __init__(self, ids):
        super().__init__(f"Node(s) with ID(s): {ids} not found.")

class EdgeNotFoundError(Exception):
    def __init__(self, ids):
        super().__init__(f"Edge(s) with ID(s): {ids} not found.")
