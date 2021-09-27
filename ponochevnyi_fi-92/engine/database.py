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
                inserted_rows = self.tables[table_name].insert(values)
                return f"{len(inserted_rows)} row(s) has been inserted into '{table_name}'"
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
            deleted_rows = self.tables[table_name].delete(condition)
            return f"{len(deleted_rows)} row(s) have been deleted from the '{table_name}' table"
        return f"'{table_name}' table not found"


if __name__ == "__main__":
    db = DB()
