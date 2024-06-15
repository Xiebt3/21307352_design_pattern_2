from typing import List

from lib.node import Node, NodeIterator
from lib.factory import AbstractFactory
from lib.visitor import Visitor


class TreeStyleFactory(AbstractFactory):
    def __init__(self):
        super().__init__()

    def _create_node(self, name: str, level: int, is_last: bool, children: List[Node]) -> 'TreeStyleNode':
        return TreeStyleNode(name, level, is_last, children)


class TreeStyleNode(Node):
    def __init__(self, name: str, level: int, is_last: bool, children: List[Node]):
        super().__init__(name, level, is_last, children)

    #def create_iterator(self) -> 'NodeIterator':
    #    return TreeStyleNodeIterator(self)

    def get_child_prefix(self, prefix: str) -> str:
        if self.is_root():
            return prefix
        elif self.is_last:
            return prefix + "  "
        else:
            return prefix + "│ "


# noinspection PyMethodMayBeStatic
class TreeStyleVisitor(Visitor):
    """
        输出树形（tree），形如：
        ├─ oranges
        │  └─ mandarin
        │     ├─ clementine
        │     └─ tangerine: cheap & juicy!
        └─ apples
           ├─ gala //叶节点
           └─ pink lady
        每一行的prefix是由上一行的prefix决定的，如果是最后一个（兄弟）节点，那么prefix是“  ”否则是“│ ”
    """

    def _get_label(self, node: Node, icon: str) -> str:
        symbol: str = '└─' if node.is_last else '├─'
        return "{}{}{}".format(symbol, icon, node.name)

    def _render_node_line(self, node: Node, prefix: str, icon: str) -> str:
        if node.is_root():
            return ""  # 根节点不输出
        else:
            return "{}{}\n".format(prefix, self._get_label(node, icon))

    def _fix_render(self, node: Node, res: str) -> str:
        return res


