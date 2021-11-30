"""
Index algorithms

"""

from sortedcontainers import SortedDict


class Index:
    def __init__(self):
        self.container = SortedDict()

    def __str__(self) -> str:
        return str(self.container)

    def insert(self, value: int, pointer: int):
        self.container.setdefault(value, set()).add(pointer)

    def update(self, value: int, old_pointer: int, new_pointer: int):
        self.container[value].remove(old_pointer)
        self.container[value].add(new_pointer)

    def remove(self, value: int, pointers: set = None) -> set:
        if pointers is None:
            return self.container.pop(value, set())
        pointers &= self.container[value]
        self.container[value] -= pointers
        if not self.container[value]:
            del self.container[value]
        return pointers

    def search(self, value: int, operator: str = '=') -> set:
        if operator == '=':
            return self.container.get(value, set())
        if operator == '!=':
            temp = self.container.pop(value, set())
            response = set.union(*self.container.values())
            if temp:
                self.container[value] = temp
            return response
        if value in self.container:
            i = self.container.index(value)
            if operator == '<':
                return set.union(*self.container.values()[:i])
            if operator == '<=':
                return set.union(*self.container.values()[:i + 1])
            if operator == '>':
                return set.union(*self.container.values()[i + 1:])
            if operator == '>=':
                return set.union(*self.container.values()[i:])
            raise Exception("operator not found")
        i = self.container.bisect(value)
        operator = operator.replace('=', '')
        if operator == '<':
            return set.union(*self.container.values()[:i])
        if operator == '>':
            return set.union(*self.container.values()[i:])
        raise Exception("operator not found")

    def min(self) -> int:
        return min(self.container)

    def max(self) -> int:
        return max(self.container)


if __name__ == "__main__":
    index = Index()
    print(index)
    index.insert(1, 1)
    index.insert(3, 2)
    index.insert(3, 3)
    index.insert(9, 4)
    index.insert(5, 5)
    index.insert(4, 6)
    index.insert(5, 7)
    print(index.remove(5))
    print(index.search(3))
    print(index.max())
    print(index)
