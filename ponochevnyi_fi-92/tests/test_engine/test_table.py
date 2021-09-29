import sys
sys.path.append('../..')

from engine.table import Table


def test_table_create():
    table = Table("coordinates", [["x", False], ["y", True]])
    assert table.name == "coordinates"
    assert table.table == []
    assert table.columns == {"x": 0, "y": 1}
    assert len(table.indexes) == 1


def test_table_insert():
    table = Table("coordinates", [["x", False], ["y", True]])
    assert table.insert([1, 2]) == [[1, 2]]
    assert table.table == [[1, 2]]
    assert table.insert([3, 4, 5]) == []
    assert table.table == [[1, 2]]


def test_table_select():
    table = Table("coordinates", [["x", False], ["y", True]])
    table.insert([1, 2])
    table.insert([3, 4])
    table.insert([5, 6])
    assert table.select([], [], []) == "+---+---+\n| x | y |\n+---+---+\n| 1 | 2 |\n| 3 | 4 |\n| 5 | 6 |\n+---+---+"


def test_table_delete():
    table = Table("coordinates", [["x", False], ["y", True]])
    table.insert([1, 2])
    table.insert([3, 4])
    table.insert([5, 6])
    assert table.delete(["x", "=", 1]) == [[1, 2]]
    assert table.table == [[3, 4], [5, 6]]
    assert table.delete(["x", "=", 1]) == []
    assert table.table == [[3, 4], [5, 6]]
    assert table.delete([]) == [[3, 4], [5, 6]]
    assert table.table == []
