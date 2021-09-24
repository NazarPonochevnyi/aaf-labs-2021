"""
Command Line Interface to work with SQL database

"""

import re
from engine.database import DB


class CLI:
    NAMES = r"[a-zA-Z][a-zA-Z0-9_]*"
    COMMANDS = {"CREATE", "INSERT", "SELECT", "DELETE"}
    SPECIAL_WORDS = {"INDEXED", "INTO", "FROM", "WHERE"}

    def __init__(self, **params):
        """
        Initialise CLI

        :param params:
        run: bool
        """
        self.db = DB()
        if params.get('run'):
            while True:
                commands = input("> ")
                for command in commands.split(';'):
                    if command:
                        response = self.query(command)
                        print(response)

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
        tokens, i = [], 0
        while i < len(parts) and parts[i].upper() not in CLI.COMMANDS:
            i += 1
        if i >= len(parts):
            raise Exception("command not found")
        command_name = parts[i].upper()
        tokens.append(command_name)
        i += 1
        if command_name == "CREATE":
            if re.match(CLI.NAMES, parts[i]) and not parts[i] in CLI.SPECIAL_WORDS:
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
                    if parts[i] in CLI.SPECIAL_WORDS:
                        raise Exception("INDEXED before column name")
                    if i + 1 < len(parts):
                        next_word = parts[i + 1]
                        for ch in ['(', ')', ',', ';', '.']:
                            if ch in next_word:
                                next_word = next_word.replace(ch, '')
                        is_indexed = next_word in CLI.SPECIAL_WORDS
                    else:
                        is_indexed = False
                    columns.append([parts[i], is_indexed])
                    i += is_indexed
                i += 1
            tokens.append(columns)
        elif command_name == "INSERT":
            if i < len(parts) and parts[i] in CLI.SPECIAL_WORDS:
                i += 1
            if i < len(parts) and re.match(CLI.NAMES, parts[i]):
                tokens.append(parts[i])
                i += 1
            else:
                raise Exception("invalid table name")
            values = []
            while i < len(parts):
                for ch in ['(', ')', ',', ';', '.']:
                    if ch in parts[i]:
                        parts[i] = parts[i].replace(ch, '')
                if parts[i].isnumeric():
                    values.append(int(parts[i]))
                i += 1
            tokens.append(values)
        elif command_name == "SELECT":
            pass
        elif command_name == "DELETE":
            if i < len(parts) and parts[i] in CLI.SPECIAL_WORDS:
                i += 1
            if i < len(parts) and re.match(CLI.NAMES, parts[i]):
                for ch in ['(', ')', ',', ';', '.']:
                    if ch in parts[i]:
                        parts[i] = parts[i].replace(ch, '')
                tokens.append(parts[i])
                i += 1
            else:
                raise Exception("invalid table name")
            if i < len(parts) and parts[i] in CLI.SPECIAL_WORDS:
                i += 1
            condition = []
            while i < len(parts):
                for ch in ['(', ')', ',', ';', '.']:
                    if ch in parts[i]:
                        parts[i] = parts[i].replace(ch, '')
                if parts[i].isnumeric():
                    condition.append(int(parts[i]))
                else:
                    if parts[i] in CLI.SPECIAL_WORDS:
                        raise Exception("invalid column name in WHERE")
                    condition.append(parts[i])
                i += 1
            tokens.append(condition)
        return tokens


if __name__ == "__main__":
    c = \
    """
        DELETE measurements WHERE id != 2;

    """
    print(CLI.parse_command(c))
