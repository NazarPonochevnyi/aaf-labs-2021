"""
Command Line Interface to work with SQL database

"""

from database import DB


class CLI:
    def __init__(self, **params):
        """
        Initialise CLI

        :param params:
        run: bool
        """
        self.db = DB()
        if params.get('run'):
            while True:
                command = input("> ")
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
        response = "Lorem ipsum"
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
        tokens = []
        return tokens


if __name__ == "__main__":
    print("hello world")
