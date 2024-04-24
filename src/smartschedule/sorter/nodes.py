from dataclasses import dataclass, field
from typing import TypeVar, Generic, Collection

from src.smartschedule.sorter.node import Node

T = TypeVar('T')


@dataclass(frozen=True)
class Nodes(Generic[T]):
    nodes: set[Node[T]] = field(default_factory=set)

    def __init__(self, *nodes: set[Node[T]]):
        object.__setattr__(self, 'nodes', nodes)

    def all(self):
        return frozenset(self.nodes)

    def add(self, node: Node[T]):
        new_nodes = self.nodes | {node}
        return Nodes(new_nodes)

    def with_all_dependencies_present_in(self, nodes: Collection[Node[T]]):
        nodes_set = set(nodes)
        new_nodes = {n for n in self.nodes if n.dependencies.issubset(nodes_set)}
        return Nodes(new_nodes)

    def remove_all(self, nodes: Collection[Node[T]]):
        remaining_nodes = self.nodes - set(nodes)
        return Nodes(remaining_nodes)

    def __repr__(self):
        return f"Nodes{{node={self.nodes}}}"
