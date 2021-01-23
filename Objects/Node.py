from abc import ABC

class Node(ABC):
    def accept(self, visitor):
        raise NotImplementedError

