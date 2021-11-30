import sys
sys.path.append('../..')

from engine.index import Index


def test_index_create():
    index = Index()
    assert len(index.container) == 0
    assert str(index) == "SortedDict({})"


def test_index_insert():
    index = Index()
    index.insert(1, 0)
    index.insert(5, 1)
    index.insert(-7, 2)
    index.insert(5, 3)
    index.insert(0, 4)
    index.insert(19, 5)
    index.insert(5, 6)
    index.insert(-99, 7)
    assert len(index.container) == 6
    assert index.container.bisect(0) == 3
    assert index.container.iloc[0] == -99 and index.container.iloc[-1] == 19
    assert index.min() == -99 and index.max() == 19
    assert len(index.container[5]) == 3


def test_index_update():
    index = Index()
    index.insert(1, 0)
    index.insert(5, 1)
    index.insert(5, 2)
    assert index.container[1] == {0} and index.container[5] == {1, 2}
    index.update(1, 0, -1)
    index.update(5, 1, 0)
    assert index.container[1] == {-1} and index.container[5] == {0, 2}


def test_index_search():
    index = Index()
    index.insert(1, 0)
    index.insert(1, 1)
    index.insert(5, 2)
    index.insert(-7, 3)
    index.insert(5, 4)
    index.insert(0, 5)
    index.insert(19, 6)
    index.insert(5, 7)
    index.insert(0, 8)
    index.insert(-99, 9)
    index.insert(-99, 10)
    assert index.search(-1) == set()
    assert index.search(0, "=") == {5, 8}
    assert index.search(-1, "!=") == {i for i in range(11)}
    assert -1 not in index.container
    assert index.search(1, "!=") == {i for i in range(2, 11)}
    assert 1 in index.container
    assert index.search(-1, "<") == {9, 10, 3}
    assert index.search(-7, "<") == {9, 10}
    assert index.search(-1, "<=") == {9, 10, 3}
    assert index.search(-99, "<=") == {9, 10}
    assert index.search(2, ">") == {2, 4, 7, 6}
    assert index.search(5, ">") == {6}
    assert index.search(2, ">=") == {2, 4, 7, 6}
    assert index.search(1, ">=") == {0, 1, 2, 4, 7, 6}


def test_index_remove():
    index = Index()
    index.insert(0, 0)
    index.insert(5, 1)
    index.insert(-7, 2)
    index.insert(5, 3)
    index.insert(0, 4)
    index.insert(5, 5)
    assert index.remove(-1) == set()
    assert index.remove(-7) == {2}
    assert index.remove(5, {1, 2, 3}) == {1, 3}
    assert index.remove(5, {5}) == {5}
    assert len(index.container) == 1 and index.container[0] == {0, 4}
