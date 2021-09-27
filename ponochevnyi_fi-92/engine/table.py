"""
Table algorithms

"""

from engine.index import Index
from terminaltables import AsciiTable
import operator


class Table:
    OPERATORS = {
        "<": operator.lt,
        "<=": operator.le,
        "=": operator.eq,
        "!=": operator.ne,
        ">": operator.gt,
        ">=": operator.ge
    }

    def __init__(self, name: str, columns: list[list[str, bool]]):
        self.name = name
        self.table = []
        self.columns = {}
        self.indexes = {}
        for i, (col_name, with_index) in enumerate(columns):
            self.columns[col_name] = i
            if with_index:
                self.indexes[col_name] = Index(col_name)

    def insert(self, values: list[int]) -> list[list[int]]:
        inserted_rows = []
        if len(values) == len(self.columns):
            self.table.append(values)
            inserted_rows.append(values)
            # indexes updates
        return inserted_rows

    def select(self, columns: list[str], condition: list[str], group_columns: list[str]) -> str:
        if not columns:
            columns = self.columns
        columns_ids = [self.columns[column] for column in columns]
        use_where = len(condition) == 3 and condition[1] in Table.OPERATORS.keys()
        data = [columns]
        for row in self.table:
            if use_where:
                op1, oper, op2 = condition
                if op1 in self.columns.keys():
                    op1 = row[self.columns[op1]]
                if op2 in self.columns.keys():
                    op2 = row[self.columns[op2]]
                if not Table.OPERATORS[oper](op1, op2):
                    continue
            response_row = [row[i] for i in columns_ids]
            data.append(response_row)
        pr_table = AsciiTable(data)
        return pr_table.table

    def delete(self, condition: list) -> list[list[int]]:
        deleted_rows, i = [], 0
        use_where = len(condition) == 3 and condition[1] in Table.OPERATORS.keys()
        while i < len(self.table):
            if use_where:
                row = self.table[i]
                op1, oper, op2 = condition
                if op1 in self.columns.keys():
                    op1 = row[self.columns[op1]]
                if op2 in self.columns.keys():
                    op2 = row[self.columns[op2]]
                if not Table.OPERATORS[oper](op1, op2):
                    i += 1
                    continue
            deleted_rows.append(self.table.pop(i))
        return deleted_rows


if __name__ == "__main__":
    table = Table("coordinates", [["x", False], ["y", False]])
