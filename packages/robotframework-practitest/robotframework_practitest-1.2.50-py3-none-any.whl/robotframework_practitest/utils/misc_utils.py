from __future__ import annotations

import inspect
import os
import sys
from typing import Generator
import tempfile

from robot.libraries.BuiltIn import BuiltIn
from robot.model import Tags


def retrieve_name(var) -> str:
    callers_local_vars = inspect.currentframe().f_back.f_locals.items()
    return [var_name for var_name, var_val in callers_local_vars if var_val is var][0]


def get_error_info():
    exc_type, exc_obj, exc_tb = sys.exc_info()
    file_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    return file_name, exc_tb.tb_lineno


def read_variables(*var_names):
    return dict(_read_api_info(*var_names))


def _read_api_info(*var_names):
    robot_vars = BuiltIn().get_variables(True)
    for var_name in var_names:
        name, mandatory, default = var_name.as_tuple
        if mandatory:
            assert name in robot_vars.keys(), f"Mandatory variable '{name}' missing"
        value = robot_vars.get(name, default)
        BuiltIn().set_global_variable(f"${var_name.Name}", value)
        yield var_name.Name, value


def flat_lists(exclusions: list = [], exclude_prefix: list = [], *lists):
    result = []
    for sub_item in lists:
        if isinstance(sub_item, (list, tuple, Tags, Generator)):
            result.extend(flat_lists(exclusions, exclude_prefix, *sub_item))
        else:
            if not any([sub_item.startswith(ex) for ex in exclude_prefix]) and sub_item not in exclusions:
                result.append(sub_item)
    return result


TEMP_DIR = None


def write_to_temp_file(data, suffix=None, prefix='temp', name=None, mode='w+'):
    global TEMP_DIR
    if not TEMP_DIR:
        TEMP_DIR = tempfile.mkdtemp()

    file_name = "{prefix}{name}{suffix}".format(prefix=f'{prefix}_' if prefix else '',
                                                name=f'{name}_' if name else '',
                                                suffix=suffix if suffix else '')
    file_path = os.path.join(TEMP_DIR, file_name)
    with open(file_path, mode, encoding='utf-8') as stream:
        stream.write(data)
    return file_path
