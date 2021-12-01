import sys
sys.path.append('..')

from cli import CLI


def test_parse_create():
    assert CLI.parse_command("\tCREATE\n    measurements (\n id INDEXED, height  INDEXED,  weight ) ; ") == ["CREATE",
                                                                                                       "measurements",
                                                                                                       [["id", True],
                                                                                                        ["height",
                                                                                                         True],
                                                                                                        ["weight",
                                                                                                         False]]]
    assert CLI.parse_command("create measurements (id indeXed ,height,weight") == ["CREATE", "measurements",
                                                                                                       [["id", True],
                                                                                                        ["height",
                                                                                                         False],
                                                                                                        ["weight",
                                                                                                         False]]]


def test_parse_insert():
    assert CLI.parse_command("\n INSERT INTo  measurements ( 1,  180, -75 ) ; ") == ["INSERT", "measurements", [1, 180, -75]]
    assert CLI.parse_command("InSERT measurements (0 , +175, 72);.") == ["INSERT", "measurements", [0, 175, 72]]


def test_parse_select():
    assert CLI.parse_command("sELECT * FRoM measurements;") == ["SELECT", "measurements", [], [], []]
    assert CLI.parse_command("SELECT height, weight FROM measurements WHERE id = +1;") == ["SELECT", "measurements",
                                                                                          ["height", "weight"],
                                                                                          ["id", "=", 1], []]
    assert CLI.parse_command("SELECT height,COUNT( id), aVg ( weight)\n  FROM measurements\n  GROUP_BY  \nheight,weight;") == [
        "SELECT", "measurements", ["height", "COUNT(id)", "AVG(weight)"], [], ["height", "weight"]]
    assert CLI.parse_command(
        "SELECT weight, COUNT (id) \n  FROM measurements\n  WHERE height>= 170\n  GROUP_BY weight;") == ["SELECT",
                                                                                                        "measurements",
                                                                                                        ["weight",
                                                                                                         "COUNT(id)"],
                                                                                                        ["height", ">=",
                                                                                                         170],
                                                                                                         ["weight"]]


def test_parse_delete():
    assert CLI.parse_command("DELETE FROM cats;") == ["DELETE", "cats", []]
    assert CLI.parse_command("DELETE measurements WHERE height >= 190;") == ["DELETE", "measurements",
                                                                             ["height", ">=", 190]]
    assert CLI.parse_command("DELETE measurements WHERE id !=2;") == ["DELETE", "measurements", ["id", "!=", 2]]
    assert CLI.parse_command("delete measurements where x=-1") == ["DELETE", "measurements", ["x", "=", -1]]


def test_db_query():
    client = CLI()
    assert client.query("Create temp (x,y);") == "Table 'temp' has been created"
    assert client.query("INSERT INTO temp (1, 2);") == "1 row(s) has been inserted into 'temp'"
    assert client.query("select * froM temp where x=1;") == "+---+---+\n| x | y |\n+---+---+\n| 1 | 2 |\n+---+---+"
    assert client.query("delete from temp;") == "1 row(s) have been deleted from the 'temp' table"
