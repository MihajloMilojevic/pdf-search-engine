
class NodeData:
    def __init__(self, page: int, positions: list[int], number_of_occurrences: int):
        self.page = page
        self.positions = positions
        self.occurrences = number_of_occurrences