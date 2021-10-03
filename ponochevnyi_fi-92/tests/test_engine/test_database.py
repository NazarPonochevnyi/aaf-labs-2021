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
    # TODO: select tests
    pass


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
