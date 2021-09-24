import sys
sys.path.append('..')

from cli import CLI


def test_parse_create():
    assert CLI.parse_command("\tCREATE\n    measurements (\nid INDEXED, height INDEXED, weight);") == ["CREATE", "measurements",
                                                                                              [["id", True],
                                                                                               ["height", True],
                                                                                               ["weight", False]]]

    assert CLI.parse_command("INSERT INTO measurements (1, 180, 75);") == ["INSERT", "measurements", [1, 180, 75]]
    assert CLI.parse_command("INSERT measurements (2, 175, 72);.") == ["INSERT", "measurements", [2, 175, 72]]

    assert CLI.parse_command("DELETE FROM cats;") == ["DELETE", "cats", []]
    assert CLI.parse_command("DELETE measurements WHERE height >= 190;") == ["DELETE", "measurements", ["height", ">=", 190]]
    assert CLI.parse_command("DELETE measurements WHERE id != 2;") == ["DELETE", "measurements", ["id", "!=", 2]]
