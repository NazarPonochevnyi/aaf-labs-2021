"""
Index algorithms

"""

from graphviz import Digraph


class Index:
    def __init__(self, value=None, pointer=None):
        self.data = value
        self.pointer = pointer
        self.left = None
        self.right = None

    def to_dict(self, result={}) -> dict:
        if self.data is None:
            return {}
        result[self.data] = [None, None]
        if self.left:
            result[self.data][0] = self.left.data
            self.left.to_dict(result)
        if self.right:
            result[self.data][1] = self.right.data
            self.right.to_dict(result)
        return result

    def __str__(self) -> str:
        return str(self.to_dict({}))

    def display(self) -> dict:
        tree = self.to_dict({})
        fig = Digraph(format="png",
                      graph_attr={'ordering': 'out',
                                  'nodesep': '0.4',
                                  'ranksep': '0.5',
                                  'margin': '0.1'},
                      edge_attr={'arrowsize': '0.8'})
        temp_nodes = {n: 0 for n in tree}
        for parent in tree:
            for child in tree[parent]:
                if child:
                    fig.edge(str(parent), str(child))
                else:
                    temp_nodes[parent] += 1
                    temp_node = f"{parent}t{temp_nodes[parent]}"
                    fig.node(temp_node, style='invis')
                    fig.edge(str(parent), temp_node, style='invis')
        fig.view()
        return tree

    def insert(self, value: int, pointer: int):
        if self.data:
            if value < self.data:
                if self.left is None:
                    self.left = Index(value, pointer)
                else:
                    self.left.insert(value, pointer)
            else:
                if self.right is None:
                    self.right = Index(value, pointer)
                else:
                    self.right.insert(value, pointer)
        else:
            self.data = value
            self.pointer = pointer

    def remove(self, value: int):
        if self.data:
            if value < self.data:
                if self.left is None:
                    raise Exception("element not found")
                if self.left.data == value:
                    temp = self.left
                    if temp.left is None and temp.right is None:
                        self.left = None
                        return temp
                    if temp.left is None and temp.right is not None:
                        self.left = self.left.right
                        return temp
                    if temp.left is not None and temp.right is None:
                        self.left = self.left.left
                        return temp
                return self.left.remove(value)
            elif value > self.data:
                if self.right is None:
                    raise Exception("element not found")
                if self.right.data == value:
                    temp = self.right
                    if temp.left is None and temp.right is None:
                        self.right = None
                        return temp
                    if temp.left is None and temp.right is not None:
                        self.right = self.right.right
                        return temp
                    if temp.left is not None and temp.right is None:
                        self.right = self.right.left
                        return temp
                return self.right.remove(value)
            else:
                temp = self.data
                if self.left is None and self.right is None:
                    self.data = None
                    return temp
                elif self.left is None and self.right is not None:
                    self.data = self.right.data
                    self.right = None
                    return temp
                elif self.left is not None and self.right is None:
                    self.data = self.left.data
                    self.left = None
                    return temp
                min_value = self.right.min()
                self.data = min_value
                if self.right.data == min_value:
                    self.right = None
                    return temp
                self.right.remove(min_value)
                return temp
        else:
            raise Exception("index (binary tree) is empty")

    def search(self, value: int) -> int:
        if self.data:
            if value < self.data:
                if self.left is None:
                    return 0
                return self.left.search(value)
            elif value > self.data:
                if self.right is None:
                    return 0
                return self.right.search(value)
            return self.pointer
        else:
            raise Exception("index (binary tree) is empty")

    def min(self):
        if self.data:
            if self.left is None:
                return self.data
            return self.left.min()
        else:
            raise Exception("index (binary tree) is empty")

    def max(self):
        if self.data:
            if self.right is None:
                return self.data
            return self.right.max()
        else:
            raise Exception("index (binary tree) is empty")


if __name__ == "__main__":
    index = Index()
    print(index)
    index.insert(1, 1)
    index.insert(3, 2)
    index.insert(3, 3)
    index.insert(9, 4)
    index.insert(5, 5)
    index.insert(4, 6)
    index.remove(5)
    print(index.search(3))
    print(index.max())
    print(index.display())
