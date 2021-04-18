from collections import namedtuple
from pathlib import Path
from typing import Dict, List

from dataclasses import dataclass


@dataclass()
class DataStructure_ToHoldCallsAndCallees(object):
    Node = namedtuple('Node', ('sequence_number', 'child', 'parent'))
    modules: Dict[str, Dict[str, List[Node]]]

    def append(self, file: Path, function: str, node: Node):
        file_str = file.__str__()
        self.modules[file_str][function] = node

    def __str__(self):
        return f"{self.modules.items()}"