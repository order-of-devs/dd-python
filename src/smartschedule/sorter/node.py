from __future__ import annotations


from dataclasses import dataclass, field
from typing import Optional, Generic, TypeVar

T = TypeVar('T')


@dataclass(frozen=True)
class Node(Generic[T]):
    name: str
    dependencies: set[Node[T]] = field(default_factory=set)
    content: Optional[T] = None

    def depends_on(self, node: Node[T]) -> Node[T]:
        new_dependencies = self.dependencies.copy()
        new_dependencies.add(node)
        return Node(self.name, new_dependencies, self.content)

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    def __eq__(self, other):
        if not isinstance(other, Node):
            return False
        return self.name == other.name

    def __hash__(self):
        return hash(self.name)
