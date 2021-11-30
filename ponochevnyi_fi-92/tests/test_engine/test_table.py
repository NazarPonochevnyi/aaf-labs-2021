import sys

sys.path.append('../..')

from engine.table import Table


def test_table_create():
    table = Table("coordinates", [["x", False], ["y", True]])
    assert table.name == "coordinates"
    assert table.table == {}
    assert table.columns == {"x": 0, "y": 1}
    assert len(table.indexes) == 1


def test_table_insert():
    table = Table("coordinates", [["x", False], ["y", True]])
    assert table.insert([1, 2]) == [[1, 2]]
    assert table.table == {0: [1, 2]}
    assert table.insert([3, 4, 5]) == []
    assert table.table == {0: [1, 2]}
    assert len(table.indexes["y"].container) == 1


def test_table_select():
    table = Table("coordinates", [["x", False], ["y", True]])
    table.insert([1, 2])
    table.insert([3, 4])
    table.insert([5, 6])
    assert table.select([], [], []) == "+---+---+\n| x | y |\n+---+---+\n| 1 | 2 |\n| 3 | 4 |\n| 5 | 6 |\n+---+---+"
    table = Table("coordinates", [["x", True], ["y", False], ["color", False], ["type", False]])
    table.insert([1, 2, "red", "point"])
    table.insert([5, 4, "blue", "point"])
    table.insert([5, 6, "blue", "line"])
    table.insert([7, 6, "red", "line"])
    table.insert([3, 4, "red", "point"])
    table.insert([2, 9, "yellow", "point"])
    assert table.select(["x", "y"], ["yellow", "=", "color"],
                        []) == "+---+---+\n| x | y |\n+---+---+\n| 2 | 9 |\n+---+---+"
    assert table.select(["MAX(x)", "MAX(y)"], [],
                        []) == "+--------+--------+\n| MAX(x) | MAX(y) |\n+--------+--------+\n| 7      | 9      |\n+--------+--------+"
    assert table.select(["x", "y", "AVG(x)"], ["type", "=", "point"],
                        []) == "+---+---+--------+\n| x | y | AVG(x) |\n+---+---+--------+\n| 1 | 2 | 2.75   |\n| 5 | 4 | 2.75   |\n| 3 | 4 | 2.75   |\n| 2 | 9 | 2.75   |\n+---+---+--------+"
    assert table.select(["color", "x", "y", "COUNT(type)"], [], [
        "color"]) == "+--------+---+---+-------------+\n| color  | x | y | COUNT(type) |\n+--------+---+---+-------------+\n| blue   | 5 | 6 | 2           |\n| red    | 3 | 4 | 3           |\n| yellow | 2 | 9 | 1           |\n+--------+---+---+-------------+"
    assert table.select(["type", "COUNT_DISTINCT(y)", "COUNT(y)"], [], [
        "type"]) == "+-------+-------------------+----------+\n| type  | COUNT_DISTINCT(y) | COUNT(y) |\n+-------+-------------------+----------+\n| line  | 1                 | 2        |\n| point | 3                 | 4        |\n+-------+-------------------+----------+"
    assert table.select(["type", "MAX(y)", "COUNT_DISTINCT(x)"], ["color", "!=", "yellow"], [
        "type"]) == "+-------+--------+-------------------+\n| type  | MAX(y) | COUNT_DISTINCT(x) |\n+-------+--------+-------------------+\n| line  | 6      | 2                 |\n| point | 4      | 3                 |\n+-------+--------+-------------------+"
    assert table.select(["type", "color", "AVG(y)", "COUNT(x)"], [7, ">", "x"], ["type",
                                                                                 "color"]) == "+-------+--------+--------+----------+\n| type  | color  | AVG(y) | COUNT(x) |\n+-------+--------+--------+----------+\n| line  | blue   | 6.0    | 1        |\n| point | blue   | 4.0    | 1        |\n| point | red    | 3.0    | 2        |\n| point | yellow | 9.0    | 1        |\n+-------+--------+--------+----------+"


def test_table_delete():
    table = Table("coordinates", [["x", True], ["y", False]])
    table.insert([1, 2])
    table.insert([3, 4])
    table.insert([5, 6])
    assert table.delete(["x", "=", 1]) == [[1, 2]]
    assert table.table == {1: [3, 4], 2: [5, 6]}
    assert table.delete(["x", "=", 1]) == []
    assert table.table == {1: [3, 4], 2: [5, 6]}
    assert table.delete([]) == [[3, 4], [5, 6]]
    assert table.table == {}
    assert len(table.indexes["x"].container) == 0


def test_table_performance():
    from time import perf_counter
    from random import randint
    table = Table("test", [["x", True], ["y", False]])
    for _ in range(100000):
        value = randint(-1000, 1000)
        table.insert([value, value])
    start_time = perf_counter()
    table.select([], ["y", ">", 0], [])
    no_index_time = perf_counter() - start_time
    start_time = perf_counter()
    table.select([], ["x", ">", 0], [])
    index_time = perf_counter() - start_time
    assert round(index_time, 2) <= round(no_index_time, 2)
