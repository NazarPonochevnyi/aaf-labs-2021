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
    AGGREGATIONS = {
        "COUNT": lambda column: len(column),
        "COUNT_DISTINCT": lambda column: len(set(column)),
        "MAX": lambda column: max(column),
        "AVG": lambda column: sum(column) / len(column)
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
        columns_map = []
        for column in columns:
            possible_agg_name = column.split('(')[0]
            if possible_agg_name in Table.AGGREGATIONS:
                column_name = column[column.index('(') + 1: column.index(')')]
                columns_map.append([Table.AGGREGATIONS[possible_agg_name], self.columns[column_name]])
            else:
                columns_map.append([None, self.columns[column]])
        aggregation_lists = {}
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
            response_row = []
            for i, (agg_func, col_id) in enumerate(columns_map):
                if agg_func is not None:
                    aggregation_lists.setdefault(i, []).append(row[col_id])
                response_row.append(row[col_id])
            data.append(response_row)
        if aggregation_lists:
            for i, (agg_func, col_id) in enumerate(columns_map):
                if agg_func is not None:
                    aggregation_lists[i] = agg_func(aggregation_lists[i])
            start_i = 1 if len(aggregation_lists) < len(columns) else -1
            for row in data[start_i:]:
                for agg_col_id in aggregation_lists:
                    row[agg_col_id] = aggregation_lists[agg_col_id]
            if len(aggregation_lists) == len(columns):
                data = [data[0], data[-1]]
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
    table = Table("coordinates", [["x", False], ["y", True]])
    table.insert([1, 2])
    table.insert([5, 4])
    table.insert([5, 6])
    print(table.select(["AVG(x)", "MAX(x)", "COUNT(x)", "COUNT_DISTINCT(x)"], [], []))