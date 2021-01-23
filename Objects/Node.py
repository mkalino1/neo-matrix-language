from abc import ABC

class Node(ABC):
    def accept(self, visitor):
        raise NotImplementedError(f'{self.__class__.__name__} not implemented')

