"""
Table algorithms

"""

from terminaltables import AsciiTable
from engine.index import Index
from itertools import product
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

    def __init__(self, name: str, columns: list):
        self.name = name
        self.table = {}
        self.row_id = 0
        self.columns = {}
        self.indexes = {}
        for i, (col_name, with_index) in enumerate(columns):
            self.columns[col_name] = i
            if with_index:
                self.indexes[col_name] = Index()

    def insert(self, values: list) -> list:
        inserted_rows = []
        if len(values) == len(self.columns):
            row_i = self.row_id
            for col_name in self.indexes:
                i = self.columns[col_name]
                self.indexes[col_name].insert(values[i], row_i)
            self.table[row_i] = values
            self.row_id += 1
            inserted_rows.append(values)
        return inserted_rows

    def select(self, columns: list, condition: list, group_columns: list) -> str:
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
        rows_ids, use_where = set(self.table.keys()), False
        if len(condition) == 3 and condition[1] in Table.OPERATORS.keys():
            use_where = True
            op1, oper, op2 = condition
            if (op1 in self.columns.keys()) != (op2 in self.columns.keys()):
                if (op1 in self.columns.keys()) and (op1 in self.indexes.keys()):
                    use_where = False
                    rows_ids = self.indexes[op1].search(op2, oper)
                elif (op2 in self.columns.keys()) and (op2 in self.indexes.keys()):
                    use_where = False
                    if '<' in oper:
                        oper = oper.replace('<', '>')
                    elif '>' in oper:
                        oper = oper.replace('>', '<')
                    rows_ids = self.indexes[op2].search(op1, oper)
        data = [columns]
        use_group_index = all((g_column in self.indexes.keys() for g_column in group_columns))
        if len(group_columns) == 1 and use_group_index:
            g_column, groups = group_columns[0], {}
            for key, value in self.indexes[g_column].container.items():
                group_key = (key,)
                groups[group_key] = value.copy()
                if not use_where:
                    groups[group_key] &= rows_ids
                if groups[group_key]:
                    for row_id in groups[group_key].copy():
                        row = self.table[row_id]
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
                                aggregation_lists.setdefault(group_key, {}).setdefault(i, []).append(row[col_id])
                            response_row.append(row[col_id])
                        groups[group_key] = response_row
                else:
                    del groups[group_key]
        else:
            groups = {}
            groups_map = [self.columns[g_column] for g_column in group_columns]
            for row_id in rows_ids:
                row = self.table[row_id]
                if use_where:
                    op1, oper, op2 = condition
                    if op1 in self.columns.keys():
                        op1 = row[self.columns[op1]]
                    if op2 in self.columns.keys():
                        op2 = row[self.columns[op2]]
                    if not Table.OPERATORS[oper](op1, op2):
                        continue
                response_row = []
                group_key = tuple(row[col_id] for col_id in groups_map)
                for i, (agg_func, col_id) in enumerate(columns_map):
                    if agg_func is not None:
                        if group_key:
                            aggregation_lists.setdefault(group_key, {}).setdefault(i, []).append(row[col_id])
                        else:
                            aggregation_lists.setdefault(i, []).append(row[col_id])
                    response_row.append(row[col_id])
                if group_key:
                    groups[group_key] = response_row
                else:
                    data.append(response_row)
        if group_columns:
            for group_key in groups:
                for i, (agg_func, col_id) in enumerate(columns_map):
                    if agg_func is not None:
                        groups[group_key][i] = agg_func(aggregation_lists[group_key][i])
            data += list(groups.values())
            data[1:] = sorted(data[1:], key=lambda row: tuple(row[columns.index(g_column)] for g_column in group_columns if g_column in columns))
        else:
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

    def delete(self, condition: list) -> list:
        deleted_rows, rows_ids, use_where = [], set(self.table.keys()), False
        if len(condition) == 3 and condition[1] in Table.OPERATORS.keys():
            use_where = True
            op1, oper, op2 = condition
            if (op1 in self.columns.keys()) != (op2 in self.columns.keys()):
                if (op1 in self.columns.keys()) and (op1 in self.indexes.keys()):
                    use_where = False
                    rows_ids = self.indexes[op1].search(op2, oper)
                elif (op2 in self.columns.keys()) and (op2 in self.indexes.keys()):
                    use_where = False
                    if '<' in oper:
                        oper = oper.replace('<', '>')
                    elif '>' in oper:
                        oper = oper.replace('>', '<')
                    rows_ids = self.indexes[op2].search(op1, oper)
        for row_id in rows_ids.copy():
            row = self.table[row_id]
            if use_where:
                op1, oper, op2 = condition
                if op1 in self.columns.keys():
                    op1 = row[self.columns[op1]]
                if op2 in self.columns.keys():
                    op2 = row[self.columns[op2]]
                if not Table.OPERATORS[oper](op1, op2):
                    continue
            for col_name in self.indexes:
                col_id = self.columns[col_name]
                self.indexes[col_name].remove(row[col_id], {row_id})
            deleted_rows.append(self.table.pop(row_id))
        return deleted_rows


if __name__ == "__main__":
    table = Table("coordinates", [["x", False], ["y", True], ["color", False], ["type", False]])
    table.insert([1, 2, "red", "point"])
    table.insert([5, 4, "blue", "point"])
    table.insert([5, 6, "blue", "line"])
    table.insert([7, 6, "red", "line"])
    table.insert([3, 4, "red", "point"])
    table.insert([2, 9, "yellow", "point"])
    print(table.select(["type", "MAX(y)", "COUNT_DISTINCT(x)"], ["color", "!=", "yellow"], ["type"]))
    table.delete(["x", "<=", "y"])
    print(table.select([], [], []))
