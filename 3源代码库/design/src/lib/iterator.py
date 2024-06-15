from abc import ABC, abstractmethod
from typing import List

from .node import VisitableCollection, Node


class IteratorInterface(ABC):
    @abstractmethod
    def __init__(self, root: VisitableCollection):
        pass

    @abstractmethod
    def __iter__(self):
        pass

    @abstractmethod
    def __next__(self):
        pass


"""
@设计模式 迭代器模式
NodeIterator是具体迭代器
"""


# 迭代器接口,接口声明了遍历集合所需的操作： 获取下一个元素、 获取当前位置和重新开始迭代等。
class NodeIterator(IteratorInterface):
    def __init__(self, root: Node):
        super().__init__(root)
        self.__stack: List[(Node, str, int)] = [(root, "", -1)]

    def __iter__(self):
        return self

    def __next__(self):
        while self.__stack:
            node, prefix, child_index = self.__stack.pop()
            child_prefix: str = node.get_child_prefix(prefix)
            if child_index == -1:
                self.__stack.append((node, prefix, 0))
                return node, prefix
            elif child_index < len(node.children):
                self.__stack.append((node, prefix, child_index + 1))
                self.__stack.append((node.children[child_index], child_prefix, -1))
        raise StopIteration
