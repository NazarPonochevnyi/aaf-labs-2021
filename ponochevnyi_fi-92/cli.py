"""
Command Line Interface to work with SQL database

"""

import re
from engine.database import DB
import operator


class CLI:
    NAMES = r"[a-zA-Z][a-zA-Z0-9_]*"
    COMMANDS = {"CREATE", "INSERT", "SELECT", "DELETE"}
    SPECIAL_WORDS = {"INDEXED", "INTO", "FROM", "WHERE", "GROUP_BY"}
    OPERATORS = {
        "<=": operator.le,
        "!=": operator.ne,
        ">=": operator.ge,
        "<": operator.lt,
        "=": operator.eq,
        ">": operator.gt
    }
    LIST_OPERATORS = list(OPERATORS.keys())

    class GetOutOfLoop(Exception):
        pass

    def __init__(self, **params):
        """
        Initialise CLI

        :param params:
        run: bool
        """
        self.db = DB()
        if params.get('run'):
            print("Welcome to NazarSQL!\n",
                  " (use 'EXIT;' command to quit\n",
                  " and 'SHOW [table] [column];' command to show the index)")
            input_text = ""
            try:
                while True:
                    input_text += ' ' + input("> ").strip()
                    if ';' in input_text:
                        for command in input_text.split(';'):
                            if command:
                                command = command.strip()
                                if command.upper() == "EXIT":
                                    raise CLI.GetOutOfLoop
                                if "SHOW" in command.upper():
                                    try:
                                        _, table_name, column_name = command.split()
                                        response = str(self.db.tables[table_name].indexes[column_name])
                                    except Exception as e:
                                        response = "Error: {}".format(str(e))
                                    print(response)
                                    input_text = ""
                                    continue
                                try:
                                    response = self.query(command)
                                except IndexError:
                                    response = "Error: invalid command"
                                except Exception as e:
                                    response = "Error: {}".format(str(e))
                                print(response)
                                input_text = ""
            except CLI.GetOutOfLoop:
                pass

    def query(self, command: str) -> str:
        """
        Query command to database

        :param command:
        command: str
        :return:
        response: str
        """
        tokens = CLI.parse_command(command)
        command_name = tokens[0]
        if command_name == "CREATE":
            _, table_name, columns = tokens
            response = self.db.create(table_name, columns)
        elif command_name == "INSERT":
            _, table_name, values = tokens
            response = self.db.insert(table_name, values)
        elif command_name == "SELECT":
            _, table_name, columns, condition, group_columns = tokens
            response = self.db.select(table_name, columns, condition, group_columns)
        elif command_name == "DELETE":
            _, table_name, condition = tokens
            response = self.db.delete(table_name, condition)
        else:
            response = "Command not found"
        return response

    @staticmethod
    def parse_command(command: str) -> list:
        """
        Parsing any string to list of tokens

        :param command:
        command: str
        :return:
        tokens: list
        """
        parts = command.split()
        parts = list(filter(lambda x: x != '', sum([part.split(',') for part in parts], [])))
        for i, part in enumerate(parts):
            if part not in CLI.LIST_OPERATORS:
                check_list = [oper in part for oper in CLI.LIST_OPERATORS]
                if any(check_list):
                    oper = CLI.LIST_OPERATORS[check_list.index(True)]
                    insert_part = part.split(oper)
                    insert_part.insert(1, oper)
                    parts = parts[:i] + list(filter(lambda x: x != '', insert_part)) + parts[i + 1:]
                    break
        tokens, i = [], 0
        while i < len(parts) and parts[i].upper() not in CLI.COMMANDS:
            i += 1
        if i >= len(parts):
            raise Exception("command not found")
        command_name = parts[i].upper()
        tokens.append(command_name)
        i += 1
        if command_name == "CREATE":
            if re.match(CLI.NAMES, parts[i]) and not parts[i].upper() in CLI.SPECIAL_WORDS:
                tokens.append(parts[i])
                i += 1
            else:
                raise Exception("invalid table name")
            columns = []
            while i < len(parts):
                for ch in ['(', ')', ',', ';', '.']:
                    if ch in parts[i]:
                        parts[i] = parts[i].replace(ch, '')
                if re.match(CLI.NAMES, parts[i]):
                    if parts[i].upper() in CLI.SPECIAL_WORDS:
                        raise Exception("INDEXED before column name")
                    if i + 1 < len(parts):
                        next_word = parts[i + 1]
                        for ch in ['(', ')', ',', ';', '.']:
                            if ch in next_word:
                                next_word = next_word.replace(ch, '')
                        is_indexed = next_word.upper() == "INDEXED"
                    else:
                        is_indexed = False
                    columns.append([parts[i], is_indexed])
                    i += is_indexed
                i += 1
            tokens.append(columns)
        elif command_name == "INSERT":
            if i < len(parts) and parts[i].upper() in CLI.SPECIAL_WORDS:
                i += 1
            if i < len(parts) and re.match(CLI.NAMES, parts[i]) and not parts[i].upper() in CLI.SPECIAL_WORDS:
                tokens.append(parts[i])
                i += 1
            else:
                raise Exception("invalid table name")
            values = []
            while i < len(parts):
                for ch in ['(', ')', ',', ';', '.']:
                    if ch in parts[i]:
                        parts[i] = parts[i].replace(ch, '')
                if parts[i].lstrip("+-").isnumeric():
                    values.append(int(parts[i]))
                i += 1
            tokens.append(values)
        elif command_name == "SELECT":
            columns = []
            while i < len(parts) and parts[i].upper() != "FROM":
                upartsi = parts[i].upper()
                if "COUNT" in upartsi or "COUNT_DISTINCT" in upartsi or "MAX" in upartsi or "AVG" in upartsi:
                    for ch in [',', ';', '.']:
                        if ch in parts[i]:
                            parts[i] = parts[i].replace(ch, '')
                    end_i = i + 1
                    full_part = ''.join(parts[i:end_i])
                    while '(' not in full_part or ')' not in full_part:
                        end_i += 1
                        full_part = ''.join(parts[i:end_i])
                    end_sw_index = full_part.index('(')
                    columns.append(full_part[:end_sw_index].upper() + full_part[end_sw_index:])
                    i = end_i
                else:
                    for ch in ['(', ')', ',', ';', '.']:
                        if ch in parts[i]:
                            parts[i] = parts[i].replace(ch, '')
                    if parts[i] == '*':
                        columns = []
                        i += 1
                    elif re.match(CLI.NAMES, parts[i]) and parts[i].upper() not in CLI.SPECIAL_WORDS:
                        columns.append(parts[i])
                        i += 1
                    else:
                        raise Exception("invalid column name")
            if i < len(parts) and parts[i].upper() == "FROM":
                i += 1
            if i < len(parts) and re.match(CLI.NAMES, parts[i]) and not parts[i].upper() in CLI.SPECIAL_WORDS:
                for ch in ['(', ')', ',', ';', '.']:
                    if ch in parts[i]:
                        parts[i] = parts[i].replace(ch, '')
                tokens.append(parts[i])
                tokens.append(columns)
                i += 1
            else:
                raise Exception("invalid table name")
            condition = []
            if i < len(parts) and parts[i].upper() == "WHERE":
                i += 1
                while i < len(parts) and len(condition) < 3:
                    for ch in ['(', ')', ',', ';', '.']:
                        if ch in parts[i]:
                            parts[i] = parts[i].replace(ch, '')
                    if parts[i].lstrip("+-").isnumeric():
                        condition.append(int(parts[i]))
                    else:
                        if parts[i].upper() in CLI.SPECIAL_WORDS:
                            raise Exception("invalid column name in WHERE")
                        condition.append(parts[i])
                    i += 1
            tokens.append(condition)
            group_columns = []
            if i < len(parts) and parts[i].upper() == "GROUP_BY":
                i += 1
                while i < len(parts):
                    for ch in ['(', ')', ',', ';', '.']:
                        if ch in parts[i]:
                            parts[i] = parts[i].replace(ch, '')
                    if re.match(CLI.NAMES, parts[i]) and not parts[i].upper() in CLI.SPECIAL_WORDS:
                        group_columns.append(parts[i])
                        i += 1
                    else:
                        raise Exception("invalid group column name")
            tokens.append(group_columns)
        elif command_name == "DELETE":
            if i < len(parts) and parts[i].upper() in CLI.SPECIAL_WORDS:
                i += 1
            if i < len(parts) and re.match(CLI.NAMES, parts[i]) and not parts[i].upper() in CLI.SPECIAL_WORDS:
                for ch in ['(', ')', ',', ';', '.']:
                    if ch in parts[i]:
                        parts[i] = parts[i].replace(ch, '')
                tokens.append(parts[i])
                i += 1
            else:
                raise Exception("invalid table name")
            if i < len(parts) and parts[i].upper() in CLI.SPECIAL_WORDS:
                i += 1
            condition = []
            while i < len(parts):
                for ch in ['(', ')', ',', ';', '.']:
                    if ch in parts[i]:
                        parts[i] = parts[i].replace(ch, '')
                if parts[i].lstrip("+-").isnumeric():
                    condition.append(int(parts[i]))
                else:
                    if parts[i].upper() in CLI.SPECIAL_WORDS:
                        raise Exception("invalid column name in WHERE")
                    condition.append(parts[i])
                i += 1
            tokens.append(condition)
        return tokens


if __name__ == "__main__":
    client = CLI(run=True)
