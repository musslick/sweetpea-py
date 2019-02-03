from abc import ABC, abstractmethod
from typing import List


"""
Generic interface for constraints.
"""
class Constraint(ABC):

    @abstractmethod
    def apply(self, block, backend_request) -> None:
        pass

    """
    Some constraints accept shorthand representations. (Like accepting a whole factor, rather than individual
    factor and level name pairs.)

    desugar is responsible for returning the desugared representation of a constraint. When a block is
    constructed, it will desugar all constraints, replacing them with their desuagared versions before
    proceding.
    """
    def desugar(self) -> List:
        return [self]
