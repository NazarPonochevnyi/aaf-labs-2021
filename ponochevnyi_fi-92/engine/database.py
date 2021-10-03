"""
Database structure

"""

from engine.table import Table


class DB:
    @staticmethod
    def check_int_list(values: list) -> bool:
        for element in values:
            if not isinstance(element, int):
                return False
        return True

    def check_condition(self, table_name: str, condition: list) -> bool:
        if condition:
            if len(condition) != 3:
                return False
            if condition[1] not in Table.OPERATORS:
                return False
            for element in (condition[0], condition[2]):
                if isinstance(element, int):
                    continue
                if isinstance(element, str) and element in self.tables[table_name].columns:
                    continue
                return False
        return True

    def __init__(self):
        self.tables = {}

    def create(self, table_name: str, columns: list[list[str, bool]]) -> str:
        """
        CREATE command

        :param table_name:
        :param columns:
        :return:
        """
        self.tables[table_name] = Table(table_name, columns)
        return f"Table '{table_name}' has been created"

    def insert(self, table_name: str, values: list[int]) -> str:
        """
        INSERT command

        :param table_name:
        :param values:
        :return:
        """
        if table_name in self.tables:
            if DB.check_int_list(values):
                if len(values) == len(self.tables[table_name].columns):
                    inserted_rows = self.tables[table_name].insert(values)
                    return f"{len(inserted_rows)} row(s) has been inserted into '{table_name}'"
                return "invalid amount of values to insert"
            return "invalid values to insert"
        return f"'{table_name}' table not found"

    def select(self, table_name: str, columns: list[str], condition: list[str], group_columns: list[str]) -> str:
        """
        SELECT command

        :param table_name:
        :param columns:
        :param condition:
        :param group_columns:
        :return:
        """
        if table_name in self.tables:
            selection = self.tables[table_name].select(columns, condition, group_columns)
            return selection
        return f"'{table_name}' table not found"

    def delete(self, table_name: str, condition: list) -> str:
        """
        DELETE command

        :param table_name:
        :param condition:
        :return:
        """
        if table_name in self.tables:
            if self.check_condition(table_name, condition):
                deleted_rows = self.tables[table_name].delete(condition)
                return f"{len(deleted_rows)} row(s) have been deleted from the '{table_name}' table"
            return "invalid condition to delete"
        return f"'{table_name}' table not found"


if __name__ == "__main__":
    db = DB()
    print(db.create("coordinates", [["x", False], ["y", True]]))
    print(db.create("measurements", [["id", True], ["height", False], ["weight", False]]))
    print(db.insert("measurements", [1, 3, 7]))
    print(db.insert("measurements", [1, 5, 4]))
    print(db.insert("measurements", [1, 4, 9]))
    print(db.insert("measurements", [2, 6, 4]))
    print(db.insert("measurements", [2, 2, 8]))
    print(db.insert("coordinates", [8, 3]))
    print(db.insert("coordinates", [9, 1]))
    print(db.insert("coordinates", [4, 6]))
    print(db.select("coordinates", [], [], []))
    print(db.select("measurements", ["MAX(height)", "MAX(weight)", "id"], ["weight", "<=", 8], ["id"]))
    print(db.delete("coordinates", ["x", ">=", 8]))
    print(db.delete("measurements", []))
