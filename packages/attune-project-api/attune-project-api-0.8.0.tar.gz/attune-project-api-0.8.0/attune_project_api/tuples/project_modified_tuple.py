from typing import List

from vortex.Tuple import Tuple
from vortex.Tuple import TupleField
from vortex.Tuple import addTupleType


@addTupleType
class ModifiedItemDetails(Tuple):
    __tupleType__ = "attune_auto_project.ModifiedItemDetails"

    key: str = TupleField()
    name: str = TupleField()
    # Indicates the change to an item from the Git diff
    # Example 'M' for modified, 'D' for deleted and so on...
    # TODO: Document all the possibilities and use fixed named constants
    changeStatus: str = TupleField()

    # Hash and Equals based on key because we want each item to only appear
    # once in the change list.
    def __hash__(self) -> int:
        return hash(self.key)

    def __eq__(self, other) -> bool:
        return self.key == other.key


@addTupleType
class ProjectModifiedTuple(Tuple):
    __tupleType__ = "attune_auto_project.ProjectModifiedTuple"

    commitsOnWorkingBranch: int = TupleField()
    modifiedSteps: List[ModifiedItemDetails] = TupleField([])
    modifiedParams: List[ModifiedItemDetails] = TupleField([])
    modifiedFiles: List[ModifiedItemDetails] = TupleField([])
