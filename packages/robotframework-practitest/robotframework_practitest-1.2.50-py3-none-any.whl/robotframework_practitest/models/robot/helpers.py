from __future__ import annotations

import re
from datetime import datetime
from enum import Enum
from typing import Mapping, AnyStr, Callable, Tuple, List, Dict

from robot.libraries.BuiltIn import BuiltIn
from robot.api import logger as robot_logger
from robotframework_practitest.utils.misc_utils import get_error_info
from robotframework_practitest.utils.logger import logger
from robotframework_practitest.services.configuration import get_default_value
from robotframework_practitest.models.practi_test.client import PT_PRODUCT_URL


class PT_MANAGED_ITEMS(Enum):
    Test = 'TEST_FIELDS'
    TestSet = 'TEST_SET_FIELDS'
    # Instance = 'INSTANCE_FIELDS'


TEST_ALLOWED_CREATE_ATTEMPTS = 3

TAG_MAPPING = {}
# TAG_MAPPING = dict(
#     TEST={'prefix': 'Test-'},
#     FIELD={'prefix': 'Custom-', 'delimiter': '-'}
# )

PT_DATE_TIME_FORMAT = "%d-%m-%Y %H:%M:%S"


def set_tag_mapping(tag_mapping):
    global TAG_MAPPING
    TAG_MAPPING = tag_mapping


def get_tag_mapping():
    global TAG_MAPPING
    return TAG_MAPPING


TEST_FIELDS = {}


def set_test_fields(test_fields):
    global TEST_FIELDS
    TEST_FIELDS = test_fields


def get_test_fields():
    global TEST_FIELDS
    return TEST_FIELDS


TEST_SET_FIELDS = {}


def set_test_set_fields(test_set_fields):
    global TEST_SET_FIELDS
    TEST_SET_FIELDS = test_set_fields


def get_test_set_fields():
    global TEST_SET_FIELDS
    return TEST_SET_FIELDS


def get_test_steps_info(*keywords):
    return [{'name': k.name, 'description': k.doc} for k in keywords]


def get_related_test_display_ids(*tag_list):
    test_map = get_tag_mapping().get('TEST')
    return [t.replace(test_map.get('prefix'), '') for t in tag_list if t.startswith(test_map.get('prefix'))]


def get_related_fields(*tag_list, **tag_mapping) -> Mapping[AnyStr, AnyStr]:
    test_map = tag_mapping.get('FIELD')
    field_data = [t.replace(test_map.get('prefix'), '').split('-', 1)
                  for t in tag_list if t.startswith(test_map.get('prefix'))]
    return {t[0]: t[1] for t in field_data}


def get_common_robot_tags(*tag_list, **kwargs):
    return [t for t in tag_list if all([not t.startswith(p) for p in [f.get('prefix') for f in get_tag_mapping().values()]])]


def get_field_by_tag(name, *tags):
    return get_related_fields(*tags).get(name, None)


def update_variable_scope_from_tags(default):
    def _(*tags, **variables):
        for var, value in variables.items():
            try:
                if isinstance(value, tuple) and isinstance(value[0], Callable):
                    yield var, get_related_fields(*tags, **get_tag_mapping().get(var, None)) or value[1]
                else:
                    yield var, value
            except Exception as e:
                f, li = get_error_info()
                logger.error(f"{e}; File: {f}:{li}")


class FieldUpdate(Enum):
    TAGS = update_variable_scope_from_tags,
    ROBOT_TAGS = get_common_robot_tags

    @staticmethod
    def from_string(pattern: str, default):
        return FieldUpdate[pattern.upper()]


def formate_test_tags(*tag_list) -> Tuple[List[str], Dict[str, AnyStr]]:
    def _except_fields(item):
        return any((item.startswith(f.get('prefix', '_')) for f in get_tag_mapping().values()))

    field_map = get_tag_mapping().get('FIELD')
    tags = sorted([t for t in tag_list if not _except_fields(t)])
    custom_fields = {i[0]: i[1] for i in
                     [t.replace(field_map.get('prefix'), '').split(field_map.get('delimiter'))
                      for t in tag_list if t.startswith(field_map.get('prefix'))]}
    return tags, custom_fields


def format_kw_list(kws: list):
    result = ''
    for index, item in enumerate(kws):
        if index == 0:
            result += item
        elif item == 'AND':
            result += '\n\t' + item
        else:
            result += '\n\t\t' + item
    return result


def get_robot_variables_map(fields: list, *fields_map, **variables):
    for field in [f for f in fields_map if f.get('name') in fields]:
        robot_variable = field.get('variable', None)
        if robot_variable:
            value = variables.get(robot_variable, field.get('default', None))
            yield field.get('name'), value


def _clean_path(clean_regex, *path, **kwargs):
    delimiter = kwargs.get('delimiter', '/')
    return delimiter.join([re.sub(clean_regex, '', p) for p in path])


def get_name(name, *path, **kwargs):
    name = name.strip()
    delimiter = kwargs.get('delimiter', '/')
    start_level = kwargs.get('level', get_default_value('PT_TEST_NAME_LEVEL'))
    path = list([re.sub(r'^[\d]+[\s|_]+', '', p) for p in path])
    run_id = kwargs.get('run_id', None)
    result = []
    if path:
        result.append("{}".format(f"Path:{delimiter.join(path[start_level:])}"))
    if run_id:
        if run_id == 'datetime':
            result.append(f"TS: {datetime.now().strftime(PT_DATE_TIME_FORMAT)}")
        else:
            result.append(f"ExternalID:{run_id}")
    return f"{name} ({' '.join(result)})" if result else name


def publish_to_metadata(report_name, *meta_collection):
    meta_msg = "{}".format(
        '\n\t'.join(["[{url}|TestSet#{display_id}]".format(num=i + 1, **n)
                     for i, n in enumerate([dict(url=PT_PRODUCT_URL.format(**m), **m) for m in meta_collection])]))
    BuiltIn().set_suite_metadata(report_name, meta_msg)


def log_report(report_name, test_mapping=None, *meta_collection):
    log_msg = "{}:\n\t{}{}".format(
        report_name,
        '\n\t'.join(["{num:02d}. Suite: {suite} -> <a href=\"{url}\">TestSet#{display_id}</a>".format(num=i + 1, **n)
                     for i, n in enumerate([dict(url=PT_PRODUCT_URL.format(**m), **m) for m in meta_collection])]),
        f"\n\nTest list:\n{test_mapping}" if test_mapping else ''
    )
    robot_logger.warn(log_msg, html=True)


DATA_DRIVER_FIELD_DELIMITER = r',|\|'


def data_driver_test_name_formatter(test_name):
    return re.split(DATA_DRIVER_FIELD_DELIMITER, test_name)[0].strip()
