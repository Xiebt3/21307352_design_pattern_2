"""
软件设计
    1.AbstractFactory模式：AbstractFactory是抽象工厂接口，和TreeStyleFactory等xxxFactory是具体的抽象工厂，它们一起实现抽象工厂
    2.Factory模式：AbstractFactory的_create是Factory模式的方法。
    3.Builder模式：AbstractFactory是Builder
    AbstractFactory的_create是Builder模式的结果方法(getResult)
    _create、create_node是Builder的部分方法(buildPartX).
    4.Registry模式：FactoryRegistry是Registry模式的实现
"""
from abc import abstractmethod
from typing import List, Any

from .node import Node


class AbstractFactory:
    def create(self, json_data: Any) -> Node:
        return self._create("root", json_data, 0, True)

    # @设计模式 Factory, Builder(getResult, buildPartX)
    def _create(self, name: str, json: Any, level: int, is_last: bool) -> Node:
        if isinstance(json, dict):
            # 中间节点渲染为NodeContainer，其children列表非空
            children = []
            for index, (key, value) in enumerate(json.items()):
                child_is_last = index == len(json) - 1
                children.append(self._create(key, value, level + 1, child_is_last))
            return self._create_node(name, level, is_last, children)
        else:
            node_name = name if json is None else f"{name}:{json}"
            return self._create_node(node_name, level, is_last, [])

    # @设计模式 Builder(buildPartX)
    @abstractmethod
    def _create_node(self, name: str, level: int, is_last: bool, children: List[Node]) -> Node:
        raise NotImplementedError("必须在子类中实现")


class FactoryRegistry:
    def __init__(self):
        self.__factories = {}

    def register(self, style: str, factory: AbstractFactory):
        self.__factories[style] = factory

    def get_factory(self, style: str) -> AbstractFactory:
        return self.__factories[style]
