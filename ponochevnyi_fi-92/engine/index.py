"""
Index algorithms

"""


class Node:
    def __init__(self, value: int):
        self.left = None
        self.data = value
        self.right = None


class Index:
    def __init__(self, name: str):
        self.name = name

    @staticmethod
    def create_node(data: int) -> Node:
        return Node(data)

    def insert(self, node: Node, data: int) -> Node:
        """
        Insert function
        """
        if node is None:
            return Index.create_node(data)
        if data < node.data:
            node.left = self.insert(node.left, data)
        elif data > node.data:
            node.right = self.insert(node.right, data)
        return node

    def search(self, node: Node, data: int) -> Node:
        """
        Search function
        """
        if node is None or node.data == data:
            return node
        if node.data < data:
            return self.search(node.right, data)
        else:
            return self.search(node.left, data)

    def delete(self, node: Node, data: int) -> Node:
        """
        Delete function
        """
        # TODO: delete function in BTree
        pass


if __name__ == "__main__":
    index = Index("id")
