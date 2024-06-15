import json
import os
from typing import Dict, Any
import toml

from lib.factory import FactoryRegistry
from tree_style import TreeStyleFactory, TreeStyleVisitor
from rectangle_style import RectangleStyleFactory, RectangleStyleVisitor
from lib.visitor import VisitorRegistry


def read_json_file(filepath: str) -> Dict:
    with open(filepath, 'r') as file:
        return json.load(file)


class FunnyJsonExplorer:
    def __init__(self, filepath: str, style: str, icon_family: str):
        self.__json_filepath: str = os.path.join(os.path.dirname(__file__), "..", filepath)
        self.__style: str = style
        self.__icon_filepath: str = os.path.join(os.path.dirname(__file__), "..", "test/icons.toml")
        self.__factory_registry = FactoryRegistry()
        self._register_abstract_factory()
        self.__visitor_registry = VisitorRegistry()
        self._register_abstract_visitor()
        self.__icon_families: Dict[str, Dict[str, str]] = self._load_icon_families()
        if icon_family not in self.__icon_families.keys():
            raise ValueError("图表簇不存在")
        self.__icon_family: Dict[str, str] = self.__icon_families[icon_family]

    def _load_icon_families(self) -> Dict[str, Dict[str, str]]:
        with open(self.__icon_filepath, 'r', encoding='utf-8') as file:
            res = toml.load(file)
        return res.get('icons')

    def _register_abstract_factory(self) -> None:
        self.__factory_registry.register("tree", TreeStyleFactory())
        self.__factory_registry.register("rectangle", RectangleStyleFactory())

    def _register_abstract_visitor(self) -> None:
        self.__visitor_registry.register("tree", TreeStyleVisitor())
        self.__visitor_registry.register("rectangle", RectangleStyleVisitor())

    def _visualize_json(self, json_data: Dict) -> None:
        now_factory = self.__factory_registry.get_factory(self.__style)
        visual_json: Any = now_factory.create(json_data)
        now_visitor = self.__visitor_registry.get_visitor(self.__style)
        print(visual_json.accept(visitor=now_visitor, prefix="", icon_family=self.__icon_family))

    def run(self) -> None:
        json_data = read_json_file(self.__json_filepath)
        self._visualize_json(json_data)
