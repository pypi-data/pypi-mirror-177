from __future__ import annotations

import logging
import re
from datetime import datetime
from typing import Callable, Tuple, Dict, List, AnyStr

from robot.libraries.BuiltIn import BuiltIn
from robot.result import TestCase as RTestResult
from robot.running import TestSuite as RTestSuite, TestCase as RTestCase, Keyword as RKeyword

from robotframework_practitest.utils.logger import logger
from robotframework_practitest.models.practi_test.data_formatters import practi_test_duration
from robotframework_practitest.models.robot.helpers import format_kw_list, get_name, formate_test_tags, \
    PT_DATE_TIME_FORMAT, get_tag_mapping
from robotframework_practitest.models.robot.html_decoder import HTMLDecoder
from robotframework_practitest.services.configuration import get_default_value
from robotframework_practitest.utils.misc_utils import flat_lists, get_error_info

VARIABLE_REGEX = re.compile(r'([\$@&]{[a-zA-Z0-9_\-\s]+\})')


def convert(item: RTestSuite | RTestCase | RKeyword):
    return PTestSuite(item)


def get_parents_path(item: RTestSuite | RTestCase | RKeyword):
    result = []
    while item.parent:
        result.append(item.parent.name)
        item = item.parent
    result.reverse()
    return result


def extract_kw_results(results: RTestResult) -> dict:
    for kw_res in results.body:
        print(f"{kw_res}")
    return {}


def format_suite_test_description(item: PTestSuite | PTestCase):
    description = []
    if item.doc:
        description.append(f"{item.doc}")
    if item.has_setup:
        description.append("Setup:\n\t{}".format(format_kw_list([item.setup.name] + list(item.setup.args))))
    if item.has_teardown:
        teardown_kws = [item.teardown.name] + list(item.teardown.args)
        description.append("Teardown:\n\t{}".format(format_kw_list(teardown_kws)))
    return '\n'.join(description)


def extract_variables(*params):
    for pattern in params:
        variables = VARIABLE_REGEX.findall(pattern)
        if variables:
            for var_match in variables:
                try:
                    yield pattern.replace(var_match, BuiltIn().get_variable_value(var_match, var_match))
                except Exception as e:
                    logger.error(f"{e}")
        else:
            yield pattern


class PKeyword:
    def __init__(self, item: RKeyword):
        self.name = getattr(item, 'name', item.type)
        self.tags = tuple(*getattr(item, 'tags', ()))
        self.parent = get_parents_path(item)
        self.doc = getattr(item, 'doc', '')
        # self.args = tuple(extract_variables(*getattr(item, 'args', [])))
        self.args = getattr(item, 'args', ())
        self.teardown = PKeyword(item.teardown) if getattr(item, 'teardown', None) else None

    def __repr__(self):
        return f"{self.name}({self.args})"

    def __str__(self):
        return f"{self.name}({', '.join(self.args)})"

    @property
    def has_teardown(self):
        return self.teardown is not None


class PTestCase:
    def __init__(self, item: RTestCase, **kwargs):
        name_formatter = kwargs.get('name_formatter', None)
        self.name = item.name if name_formatter is None else name_formatter(item.name)
        self.tags = item.tags + get_tag_mapping().get('AUTO', {}).get('tags', [])
        self.doc = item.doc
        self.parent = get_parents_path(item)
        self.template = getattr(item, 'template', None)
        self.setup = PKeyword(item.setup) if item.setup else None
        self.teardown = PKeyword(item.teardown) if item.teardown else None
        self.body = [PKeyword(k) for k in item.body]

    def __repr__(self):
        return f"{self.name}({self.body})"

    def __str__(self):
        return f"{self.name}({', '.join([f'{b}' for b in self.body])})"

    @property
    def all_tags(self):
        return self.tags + [list(k.tags) for k in self.body if k.tags]

    @property
    def has_setup(self):
        return self.setup is not None

    @property
    def has_teardown(self):
        return self.teardown is not None

    @property
    def steps(self):
        return [{'name': k.name, 'description': k.doc} for k in self.body]

    @property
    def pt_name(self):
        return get_name(self.name, *self.parent)

    @property
    def pt_tags(self) -> Tuple[List[str], Dict[str, AnyStr]]:
        return formate_test_tags(*self.tags)

    @property
    def pt_description(self):
        return format_suite_test_description(self)

    def update_variable_scope_from_tags(self, **pt_fields):
        for var, value in pt_fields.items():
            try:
                if isinstance(value, tuple) and isinstance(value[0], Callable):
                    yield var, value[0](*self.pt_tags) or value[1]
                else:
                    yield var, value
            except Exception as e:
                f, li = get_error_info()
                logger.error(f"{e}; File: {f}:{li}")


class PTestResult(PTestCase):
    def __init__(self, item: RTestResult):
        super().__init__(item)
        self.status = item.status + ('PED' if item.status == 'SKIP' else 'ED')
        self.starttime = item.starttime
        self.endtime = item.endtime
        self.elapsedtime = item.elapsedtime / 1000
        self.message = item.message

    @property
    def automated_execution_output(self):
        prefix = f"{self.status} " if self.status.startswith('SKIP') else ""
        with HTMLDecoder() as hd:
            hd.feed(self.message)
            return prefix + f"{hd}"

    @property
    def duration(self):
        return practi_test_duration(self.elapsedtime)

    def steps(self, *case_steps):
        result = []
        for k in case_steps:
            k.update(**{'status': self.status})
            result.append(dict(**{"name": k.get('name'), "expected-results": self.status}))
        return result

    @property
    def exit_code(self):
        return 0 if self.status in ('PASSED', 'SKIPPED') else 1


class PTestSuite:
    def __init__(self, item: RTestSuite, **kwargs):
        self.name = item.name
        self.doc = item.doc
        self.parent = get_parents_path(item)
        self.tests = [PTestCase(t, **kwargs) for t in item.tests]
        self.suites = [PTestSuite(s) for s in item.suites]
        self.setup = PKeyword(item.setup) if item.setup else None
        self.teardown = PKeyword(item.teardown) if item.teardown else None

    def test_set_name(self, **kwargs):
        name = self.name.strip()
        delimiter = kwargs.get('delimiter', '/')
        start_level = kwargs.get('level', get_default_value('PT_TEST_NAME_LEVEL'))
        path = list([re.sub(r'^[\d]+[\s|_]+', '', p) for p in self.parent])
        run_id = kwargs.get('run_id', None)
        result = []
        if path:
            result.append("{}".format(f"Path: {delimiter.join(path[start_level:])}"))
        if run_id:
            if run_id == 'datetime':
                result.append(f"TS: {datetime.now().strftime(PT_DATE_TIME_FORMAT)}")
            else:
                result.append(f"ExternalID:{run_id}")
        return f"{name} ({' '.join(result)})" if result else name

    @property
    def is_data_driver(self) -> bool:
        return len(self.tests) == 1 and self.tests[0].template is not None

    @property
    def tags(self) -> list:
        return []

    def all_tags(self, *exclusions):
        exclude_prefix = [tag.get('prefix', None) for tag in get_tag_mapping().values() if tag.get('prefix', None)]
        return set(self._all_tags(list(exclusions), exclude_prefix))

    def _all_tags(self, exclusions=None, exclude_prefix=None):
        if exclude_prefix is None:
            exclude_prefix = []
        if exclusions is None:
            exclusions = []
        return flat_lists(exclusions, exclude_prefix, [s._all_tags(exclusions, exclude_prefix) for s in self.suites],
                          [t.tags for t in self.tests])

    def all_tests(self, attr=None):
        for suite in self.suites:
            if suite.is_data_driver:
                continue
            for test in suite.all_tests(attr):
                yield test
        for test in self.tests:
            yield getattr(test, attr) if attr else test

    @property
    def tests_count(self):
        return sum([s.tests_count for s in self.suites]) + len(self.tests)

    @property
    def has_setup(self):
        return self.setup is not None

    @property
    def has_teardown(self):
        return self.teardown is not None

    @staticmethod
    def update_variable_scope_from_tags(*tags, **pt_fields):
        for var, value in pt_fields.items():
            try:
                if isinstance(value, tuple) and isinstance(value[0], Callable):
                    yield var, value[0](*tags) or value[1]
                else:
                    yield var, value
            except Exception as e:
                f, li = get_error_info()
                logger.error(f"{e}; File: {f}:{li}")

    def __str__(self):
        return self.name
