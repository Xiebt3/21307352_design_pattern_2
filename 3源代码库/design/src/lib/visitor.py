from abc import ABC, abstractmethod
from typing import Dict

from .node import Node


# noinspection PyMethodMayBeStatic


class Visitor(ABC):
    """
    visit_leaf和visit_container是访问者模式的访问者方法，也是模板方法模式的模板方法，模板方法定义了算法流程。
    这是考虑到树形和矩形对于叶子节点和中间节点的渲染实在有太多重复逻辑，如果只使用访问者方法而不使用模板方法，
    也即如果只是将visit相关函数简单地定为抽象函数，则在子类会出现大量重复代码，
    也即不采用模板方法会违背Don't Repeat Yourself原则，在多个地方修改相同的逻辑时，容易遗漏或不一致，代码维护成本高
    注意将中间节点和叶子节点视作了访问者模式的两个不同的元素（尽管实际上它们都是Node），因此visit中间节点和visit叶子节点对应两个不同visit函数
    """

    def visit_leaf(self, node: Node, prefix: str, icon_family: Dict[str, str]) -> str:
        leaf_icon: str = icon_family.get("leaf", "")
        return self._render_node_line(node, prefix, leaf_icon)

    def visit_container(self, node: Node, prefix: str, icon_family: Dict[str, str]) -> str:
        container_icon: str = icon_family.get("container", "")
        result = ""
        iterator = node.create_iterator()  # 在迭代器完成遍历，遍历时已经获得了前缀的信息，也只能在遍历时获得前缀信息
        for current_node, prefix in iterator:
            if current_node.is_leaf():
                result += self.visit_leaf(current_node, prefix, icon_family)
            else:
                result += self._render_node_line(current_node, prefix, container_icon)
        return self._fix_render(node, result)

    @abstractmethod
    def _get_label(self, node: Node, icon: str) -> str:
        pass

    @abstractmethod
    def _render_node_line(self, node: Node, prefix: str, icon: str) -> str:
        pass

    @abstractmethod
    def _fix_render(self, node: Node, res: str) -> str:
        pass


class VisitorRegistry:
    def __init__(self):
        self.__visitors = {}

    def register(self, style: str, visitor: Visitor):
        self.__visitors[style] = visitor

    def get_visitor(self, style: str) -> Visitor:
        return self.__visitors[style]
