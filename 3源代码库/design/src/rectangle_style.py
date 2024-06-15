from typing import List

from lib.factory import AbstractFactory
from lib.node import Node, NodeIterator
from lib.visitor import Visitor


class RectangleStyleFactory(AbstractFactory):
    def __init__(self):
        super().__init__()

    def _create_node(self, name: str, level: int, is_last: bool, children: List[Node]) -> 'RectangleStyleNode':
        return RectangleStyleNode(name, level, is_last, children)


class RectangleStyleNode(Node):
    def __init__(self, name: str, level: int, is_last: bool, children: List[Node]):
        super().__init__(name, level, is_last, children)

    def get_child_prefix(self, prefix: str) -> str:
        return prefix + ("" if self._level == 0 else "│ ")


class RectangleStyleVisitor(Visitor):
    """
        输出矩形（rectangle），形如：
        ┌─oranges────────────────────────────────┐
        │ ├─mandarin─────────────────────────────┤
        │ │ ├─clementine─────────────────────────┤
        │ │ ├─tangerine:cheap & juicy!───────────┤
        ├─apples─────────────────────────────────┤
        │ ├─gala─────────────────────────────────┤
        └─└─pink lady────────────────────────────┘
    """

    def _get_label(self, node: Node, icon: str) -> str:
        symbol: str = '└─' if node.is_last and node.is_leaf() else '├─'
        return "{}{}{}".format(symbol, icon, node.name)

    def _render_node_line(self, node: Node, prefix: str, icon: str) -> str:
        if node.is_root():
            return ""  # 根节点不输出
        label: str = self._get_label(node, icon)
        suffix: str = '─' * (40 - len(prefix) - len(label))
        return "{}{}{}─┤\n".format(prefix, label, suffix)

    def _fix_render(self, node: Node, res: str) -> str:
        lines = res.split('\n')
        lines = lines[:-1]  # 每行都有\n，所以最后一个lines为空
        if node.is_root():
            if lines:
                # 1)最后一行超出的symbol "│ " "─┤"置换为"└─" "─┘"
                lines[-1] = lines[-1].replace("│ ", "└─").replace("─┤", "─┘")
                # 2)第一行超出的symbol "├─" "─┤"置换为"┌─" "─┐"
                lines[0] = lines[0].replace("├─", "┌─").replace("─┤", "─┐")
                # 3)中间行将"└─"置换为"├─"
                for i in range(1, len(lines) - 1):
                    lines[i] = lines[i].replace("└─", "├─")
                lines.append("")
            return "\n".join(lines)
        else:
            return res


