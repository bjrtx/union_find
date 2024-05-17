"""
 The union-find module provides a basic implementation of union-find data
structures.
"""

import itertools
from collections import Counter
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
        self._parent.setdefault(item, item)

    def __contains__(self, item: Hashable):
        return item in self._parent

    def join_many(self, *args: Hashable):
        if args:
            for other in args[1:]:
                self.join(args[0], other)

    def join(self, x: Hashable, y: Hashable):
        """
        Merges the components of items x and y. If x or y is not present in the
        data structure, it is added before the merger.
        :param x: first item
        :param y: second item
        :return: None
        """
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

    def get_component(self, x: Hashable):
        r = self._get_root(x)
        return [k for k in self._parent if self._get_root(k) == r]

    @property
    def components(self):
        return [
            list(g)
            for _, g in itertools.groupby(self._parent, key=self._get_root)
        ]