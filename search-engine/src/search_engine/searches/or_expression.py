from .base_search import BaseSearch

class OrExpression(BaseSearch):
    def __init__(self, left: BaseSearch, right: BaseSearch):
        self.left = left
        self.right = right

    def search(self, search_engine):
        left_result = self.left.search(search_engine)
        right_result = self.right.search(search_engine)
        return left_result.union(right_result)