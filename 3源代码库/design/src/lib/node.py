"""
软件设计
    1.Composite模式 Node同时是中间节点和叶子节点。
    2.Template模式 Node的render是Composite模式中的业务（operation）方法，同时也是Template模式中的整体（play）方法
    3.继承：由多个类共同实现基类、各种xxxNode子类，持有node（Node），实现基类方法重用
    4、迭代器模式 VisitableCollection是迭代器模式的集合接口，Node实现迭代器模式的集合接口，
    NodeIterator是迭代器模式的迭代器接口
    5、访问者模式 VisitableCollection也是访问者模式的元素接口，具有accept方法接收访问者以进行双分派
"""
from abc import abstractmethod, ABC
from typing import Dict, List, Protocol


# 迭代器模式的集合接口，也是访问者模式的元素接口
class VisitableCollection(Protocol):
    @abstractmethod
    def create_iterator(self) -> 'NodeIterator':
        pass

    @abstractmethod
    def accept(self, visitor: 'Visitor', prefix: str, icon_family: Dict[str, str]) -> str:
        pass


# Node 类实现集合接口
class Node(VisitableCollection):
    def __init__(self, name: str, level: int, is_last: bool, children: List['Node']):
        self.name: str = name  # 中间节点name为key，叶子节点name为key
        self._level: int = level  # 缩进级别
        self.is_last: bool = is_last  # 是否是最后一个（兄弟）节点
        self.children: List['Node'] = children  # 初始为空列表 中间节点的children, Composite模式

    """
    @设计模式 Composite
    python有继承，子类会复用这些函数
    """

    def is_root(self) -> bool:
        return self._level == 0

    def is_leaf(self) -> bool:
        return len(self.children) == 0

    @abstractmethod
    def get_child_prefix(self, prefix: str) -> str:
        pass

    # 实现集合接口方法，返回一个迭代器
    def create_iterator(self) -> 'NodeIterator':
        return NodeIterator(self)

    def accept(self, visitor: 'Visitor', prefix: str, icon_family: Dict[str, str]) -> str:
        if self.is_leaf():
            return visitor.visit_leaf(self, prefix, icon_family)
        else:
            return visitor.visit_container(self, prefix, icon_family)





# 延迟导入
from .visitor import Visitor
from .iterator import NodeIterator
