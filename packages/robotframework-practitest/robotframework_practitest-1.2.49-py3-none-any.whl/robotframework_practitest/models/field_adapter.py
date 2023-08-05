from __future__ import annotations

from enum import Enum
from typing import Iterable, Dict, Any, List, Tuple

from robot.libraries.BuiltIn import BuiltIn

from .robot.wrappers import PTestSuite, PTestCase


class PT_FieldTypes(Enum):
    Custom = 'custom'
    System = 'system'

    @staticmethod
    def from_str(string: str):
        return PT_FieldTypes[string.capitalize() if string else PT_FieldTypes.Custom.name]


def extract_robot_tag(item: PTestSuite | PTestCase) -> Iterable[str]:
    if isinstance(item, PTestSuite):
        return list(item.all_tags())
    elif isinstance(item, PTestCase):
        return item.pt_tags[0]


def extract_robot_suite_name(item: PTestSuite | PTestCase) -> Dict[str, Any]:
    return item.name


class FieldMapping(Enum):
    robot_tags = 'extract_robot_tag'
    robot_suite_name = 'extract_robot_suite_name'

    @staticmethod
    def from_str(mapper):
        callback_name = FieldMapping[mapper.lower()].value
        return globals()[callback_name]


class FieldFormatters(Enum):
    coma_separated_string = lambda *items: ', '.join(items)

    @staticmethod
    def from_str(formatter):
        try:
            FieldFormatters[formatter.lower()]
        except KeyError:
            return lambda item: item


class StaticField:
    def __init__(self, **kwargs):
        self.type = self.__class__.__name__
        self.name = kwargs.get('name', kwargs.get('id', None))
        self.default = kwargs.get('default', None)
        self.formatter = FieldFormatters.from_str(kwargs.get('formatter', ''))
        self.match_value = kwargs.get('match_value', None)

    def __call__(self, *args, **kwargs) -> Dict[str, Any]:
        return {self.name: self.formatter(self.default)}


class MappedField(StaticField):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.map_cb = FieldMapping.from_str(kwargs.get('map'))

    def __call__(self, *args, **kwargs):
        return {self.name: self.map_cb(*args, **kwargs)}


class VariableField(StaticField):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.variable = kwargs.get('variable')
        assert self.variable, f"{self.type} -> Variable name missing"

    @property
    def decorated(self):
        return f"${{{self.variable}}}"

    def __call__(self, *args, **kwargs):
        value = BuiltIn().get_variable_value(self.decorated, self.default)
        try:
            assert value is not None, f"{self.type}: Variable '{self.variable}' are mandatory"
        except AssertionError as e:
            if self.default is None:
                raise

        return {self.name: value}


class MappingType(Enum):
    Mapped = MappedField
    Variable = VariableField
    Static = StaticField

    @staticmethod
    def from_setting(**field):
        if field.get('map', None):
            return MappingType.Mapped.value(**field)
        if field.get('variable', None):
            return MappingType.Variable.value(**field)
        return MappingType.Static.value(**field)


def fields_factory(fields: Iterable[Dict]):
    result = {PT_FieldTypes.System: [], PT_FieldTypes.Custom: []}

    for field in fields:
        try:
            type_ = PT_FieldTypes.from_str(field.get('type', None))
            assert type_
            result[type_].append(MappingType.from_setting(**field))
        except Exception as e:
            print(f"{e}")
            raise
    return result


def update_fields(fields: Dict[PT_FieldTypes, List[StaticField]], item: PTestSuite | PTestCase) -> \
        Tuple[Dict[str, StaticField], Dict[str, StaticField], List[str]]:
    result = {}
    for category, fields_collection in fields.items():
        result.setdefault(category, {})
        for field in fields_collection:
            result[category].update(**field(item))

    if isinstance(item, PTestCase):
        tags, extra_cf = item.pt_tags
        result[PT_FieldTypes.Custom].update(**extra_cf)
    else:
        tags = item.all_tags()

    return result[PT_FieldTypes.System], result[PT_FieldTypes.Custom], tags


__all__ = [
    'fields_factory',
    'update_fields'
]
