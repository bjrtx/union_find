"""
 The union-find module provides a basic implementation of union-find data
structures.
"""

import itertools
from collections import Counter, defaultdict
from typing import Hashable


class UnionFindStructure:
    """
    Basic union-find data structure for hashable types with rank heuristics and
    path compression.
    """

    def __init__(self):
        self._parent = {}
        self._rank = Counter()

    def _get_root(self, x: Hashable):
        p = self._parent.get(x)
        if p is not None and p != x:
            p = self._parent[x] = self._get_root(p)
        return p

    def insert(self, item: Hashable):
        """
        Inserts an item in the data structure if it is not already present.
        :param item: item to insert
        :return: None
        """
        self._parent.setdefault(item, item)

    def __contains__(self, item: Hashable):
        return item in self._parent

    def join(self, x: Hashable, y: Hashable, *args: Hashable):
        """
        Merges the components of all input items. Any item not present in the
        data structure is added before the merger.
        :param x: first item
        :param y: second item
        :param args: any additional items
        :return: None
        """
        self._join(x, y)
        for other in args:
            self._join(x, other)

    def _join(self, x: Hashable, y: Hashable):
        self.insert(x)
        self.insert(y)
        root_x, root_y = self._get_root(x), self._get_root(y)
        if root_x != root_y:
            if self._rank[root_x] < self._rank[root_y]:
                self._parent[root_x] = root_y
            else:
                self._parent[root_y] = root_x
                if self._rank[root_x] == self._rank[root_y]:
                    self._rank[root_x] += 1

    def get_component(self, item: Hashable) -> list[Hashable]:
        """
        Returns all items in the same component as the input item.
        :param item: item whose component is sought.
        :return: a list of all items in the component.
        """
        r = self._get_root(item)
        return [k for k in self._parent if self._get_root(k) == r]

    @property
    def components(self) -> list[list[Hashable]]:
        """
        The components in the data structure as a list of lists.
        """
        d = defaultdict(list)
        for item in self._parent:
            d[self._get_root(item)].append(item)
        return list(d.values())
