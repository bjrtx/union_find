from union_find import UnionFindStructure


def test_init():
    ds = UnionFindStructure()
    ds.join(1, 2, 3, 4)
    ds.join('one', 'two', 'three', 'four', 'five')
    assert len(ds.components) == 2
    ds.join(True, False)
    assert len(ds.components) == 3
