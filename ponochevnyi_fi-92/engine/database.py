"""
Database algorithms and structure

"""


class DB:
    def __init__(self):
        pass

    def create(self, table_name: str, columns: list[list[str, bool]]) -> str:
        """
        CREATE command

        :param table_name:
        :param columns:
        :return:
        """
        return f"Created '{table_name}' table with " \
               f"'{columns}' columns."

    def insert(self, table_name: str, values: list[int]) -> str:
        """
        INSERT command

        :param table_name:
        :param values:
        :return:
        """
        return f"Inserted into '{table_name}' table values " \
               f"({','.join(map(str, values))})."

    def select(self, table_name: str, columns: list[str], condition: list[str], group_columns: list[str]) -> str:
        """
        SELECT command

        :param table_name:
        :param columns:
        :param condition:
        :param group_columns:
        :return:
        """
        return f"Selected N rows from '{table_name}' table, " \
               f"'{','.join(columns)}' columns with '{''.join(map(str, condition))}' condition " \
               f"and '{','.join(group_columns)}' grouping."

    def delete(self, table_name: str, condition: list) -> str:
        """
        DELETE command

        :param table_name:
        :param condition:
        :return:
        """
        return f"Deleted from '{table_name}' table values where " \
               f"'{''.join(map(str, condition))}'."


if __name__ == "__main__":
    db = DB()
