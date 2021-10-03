import sys
sys.path.append('../..')

from engine.database import DB


def test_db_table_create():
    db = DB()
    response = db.create("coordinates", [["x", False], ["y", True]])
    assert "coordinates" in db.tables
    assert response == "Table 'coordinates' has been created"


def test_db_table_insert():
    db = DB()
    db.create("coordinates", [["x", False], ["y", True]])
    db.create("measurements", [["id", True], ["height", False], ["weight", False]])
    assert db.insert("test", [1, 2]) == "'test' table not found"
    assert db.insert("coordinates", [1, "two"]) == "invalid values to insert"
    assert db.insert("measurements", [1, 3]) == "invalid amount of values to insert"
    assert db.insert("measurements", [1, 3, 7]) == "1 row(s) has been inserted into 'measurements'"


def test_db_table_select():
    db = DB()
    db.create("measurements", [["id", True], ["height", False], ["weight", False]])
    db.insert("measurements", [1, 3, 7])
    db.insert("measurements", [1, 5, 4])
    db.insert("measurements", [1, 4, 9])
    db.insert("measurements", [2, 6, 4])
    db.insert("measurements", [2, 2, 8])
    assert db.select("measurements", [], [], ["height"]) == "invalid columns or aggregations to select"
    assert db.select("measurements", ["volume"], [], []) == "invalid columns or aggregations to select"
    assert db.select("measurements", ["MIN(height)"], [], []) == "invalid columns or aggregations to select"
    assert db.select("measurements", ["AVG(height)", "weight", "id"], [], ["id"]) == "invalid columns or aggregations to select"
    assert db.select("measurements", [], [0, "^", 1], []) == "invalid condition to select"
    assert db.select("measurements", ["AVG(height)"], [], ["volume"]) == "invalid group columns to group by"
    assert db.select("measurements", [], [], []) == "+----+--------+--------+\n| id | height | weight |\n+----+--------+--------+\n| 1  | 3      | 7      |\n| 1  | 5      | 4      |\n| 1  | 4      | 9      |\n| 2  | 6      | 4      |\n| 2  | 2      | 8      |\n+----+--------+--------+"
    assert db.select("measurements", ["MAX(height)", "MAX(weight)", "id"], ["weight", "<=", 8], ["id"]) == "+-------------+-------------+----+\n| MAX(height) | MAX(weight) | id |\n+-------------+-------------+----+\n| 5           | 7           | 1  |\n| 6           | 8           | 2  |\n+-------------+-------------+----+"


def test_db_table_delete():
    db = DB()
    db.create("coordinates", [["x", False], ["y", True]])
    db.insert("coordinates", [8, 3])
    db.insert("coordinates", [9, 1])
    db.insert("coordinates", [4, 6])
    assert db.delete("none", []) == "'none' table not found"
    assert db.delete("coordinates", [1]) == "invalid condition to delete"
    assert db.delete("coordinates", [1, "&", 0]) == "invalid condition to delete"
    assert db.delete("coordinates", [8, "<=", "z"]) == "invalid condition to delete"
    assert db.delete("coordinates", [(1, 2), "<=", "y"]) == "invalid condition to delete"
    assert db.delete("coordinates", ["x", ">=", 8]) == "2 row(s) have been deleted from the 'coordinates' table"
    assert db.delete("coordinates", []) == "1 row(s) have been deleted from the 'coordinates' table"
